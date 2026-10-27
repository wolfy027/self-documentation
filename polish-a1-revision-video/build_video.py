"""Build the Polish A1 revision video from the lesson script in content.py.

Pipeline: synthesise narration (RHVoice) -> lay out a timeline -> render one
slide per reveal step (Pillow) -> mux with ffmpeg (chapters + loudness norm).

Usage: python3 build_video.py [--out DIR] [--no-video]
"""

import argparse
import functools
import hashlib
import math
import re
import subprocess
import wave
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import content

W, H = 1280, 720
SR = 24000
FPS = 10
TAIL = 0.5  # seconds of breathing room after each step's narration
PAD_X = 48
BODY_TOP, BODY_BOTTOM = 140, 656
GAP = 9

# voice kind -> (RHVoice profile, rate %)
VOICES = {
    'en': ('bdl', 100),
    'pl': ('magda', 90),
    'ps': ('magda', 68),
    'nt': ('natan', 90),
}

COLORS = {
    'a': (255, 196, 61),  # amber highlight
    'm': (96, 175, 255),  # masculine
    'f': (255, 126, 182),  # feminine
    'n': (94, 234, 190),  # neuter
    'g': (74, 222, 128),  # correct / go
    'r': (255, 107, 107),  # watch out
    'w': (244, 247, 255),  # white
}
BG_TOP, BG_BOT = (11, 18, 36), (27, 39, 68)
CARD, CARD_HOT = (26, 38, 64), (39, 58, 96)
WHITE, MUTED, SOFT = (244, 247, 255), (147, 164, 195), (205, 216, 238)

FONT_DIR = Path('/usr/share/fonts/truetype/liberation')
FONT_FILES = {
    'r': 'LiberationSans-Regular.ttf',
    'b': 'LiberationSans-Bold.ttf',
    'i': 'LiberationSans-Italic.ttf',
}
TOKEN = re.compile(r'\{(?:([a-z]+)\|)?([^}]*)\}')


@dataclass
class Frame:
    """One still image shown for `dur` seconds."""

    scene: int
    rows: list
    hot: int
    start: float
    dur: float
    overlay: int | None = None
    path: Path | None = None


@dataclass
class Plan:
    """Everything needed to render and mux the video."""

    frames: list = field(default_factory=list)
    audio: list = field(default_factory=list)
    chapters: list = field(default_factory=list)  # (title, start, end)


# --------------------------------------------------------------------- audio
def _wav_to_array(path):
    with wave.open(str(path), 'rb') as wav:
        raw = wav.readframes(wav.getnframes())
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def _trim(arr, thresh=0.01):
    idx = np.flatnonzero(np.abs(arr) > thresh)
    if idx.size == 0:
        return arr
    return arr[max(idx[0] - 240, 0) : idx[-1] + 480]


def _normalise(arr, target_rms=0.09):
    voiced = arr[np.abs(arr) > 0.02]
    if voiced.size == 0:
        return arr
    arr = arr * (target_rms / float(np.sqrt(np.mean(voiced**2))))
    peak = float(np.max(np.abs(arr)))
    return arr * (0.95 / peak) if peak > 0.95 else arr


def synth(kind, text, cache):
    """Return mono float audio for `text` spoken in voice `kind` (cached)."""
    profile, rate = VOICES[kind]
    key = hashlib.sha1(f'{profile}|{rate}|{text}'.encode()).hexdigest()[:20]
    path = cache / f'{key}.wav'
    if not path.exists():
        subprocess.run(
            ['RHVoice-test', '-p', profile, '-r', str(rate), '-o', str(path)],
            input=text.encode('utf-8'),
            check=True,
            capture_output=True,
        )
    return _normalise(_trim(_wav_to_array(path)))


def silence(sec):
    """Return `sec` seconds of silence."""
    return np.zeros(int(round(sec * SR)), dtype=np.float32)


def chime():
    """Short two-note chime that marks the start of a chapter."""
    t = np.arange(int(0.9 * SR)) / SR
    env = np.exp(-4.5 * t)
    wave_a = np.sin(2 * math.pi * 659.25 * t) * env
    wave_b = np.sin(2 * math.pi * 987.77 * np.clip(t - 0.12, 0, None))
    wave_b *= np.exp(-4.5 * np.clip(t - 0.12, 0, None)) * (t > 0.12)
    return (0.18 * (wave_a + wave_b)).astype(np.float32)


def tick():
    """One-second countdown tick (a soft click at the start)."""
    t = np.arange(int(0.06 * SR)) / SR
    click = 0.25 * np.sin(2 * math.pi * 1200 * t) * np.exp(-60 * t)
    return np.concatenate([click, silence(1.0 - 0.06)]).astype(np.float32)


def narration(segments, cache):
    """Concatenate narration segments into a single array."""
    parts = []
    for kind, val in segments:
        if kind == 'gap':
            parts.append(silence(val))
        else:
            parts.append(synth(kind, val, cache))
            parts.append(silence(0.12))
    return np.concatenate(parts) if parts else silence(0.0)


def prefetch(scenes, cache):
    """Synthesise every unique segment in parallel before layout."""
    jobs = {
        (k, v)
        for scene in scenes
        for step in scene.steps
        for k, v in step.narr
        if k != 'gap'
    }
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda job: synth(job[0], job[1], cache), sorted(jobs)))
    return len(jobs)


# ------------------------------------------------------------------- timeline
def build_plan(scenes, cache):
    """Turn scenes into timed frames, one audio array and chapter marks."""
    plan = Plan()
    now = 0.0
    for s_idx, scene in enumerate(scenes):
        chapter_start = now
        rows = []
        for st_idx, step in enumerate(scene.steps):
            if step.clear:
                rows = []
            rows = rows + step.rows
            hot = len(step.rows)
            audio = narration(step.narr, cache)
            if st_idx == 0:
                audio = np.concatenate([chime(), silence(0.25), audio])
            dur = math.ceil((len(audio) / SR + TAIL) * FPS) / FPS
            audio = np.concatenate([audio, silence(dur - len(audio) / SR)])
            plan.frames.append(Frame(s_idx, rows, hot, now, dur))
            plan.audio.append(audio)
            now += dur
            for sec in range(step.cd, 0, -1):
                plan.frames.append(Frame(s_idx, rows, 0, now, 1.0, overlay=sec))
                plan.audio.append(tick())
                now += 1.0
        plan.chapters.append((scene.title, chapter_start, now))
    return plan


# ------------------------------------------------------------------ rendering
@functools.cache
def font(style, size):
    """Cached Liberation Sans font."""
    return ImageFont.truetype(str(FONT_DIR / FONT_FILES[style]), size)


def parse(text, default):
    """Split `{k|text}` markup into (text, colour) runs."""
    runs, pos = [], 0
    for match in TOKEN.finditer(text):
        if match.start() > pos:
            runs.append((text[pos : match.start()], default))
        runs.append((match.group(2), COLORS[match.group(1) or 'a']))
        pos = match.end()
    if pos < len(text):
        runs.append((text[pos:], default))
    return runs


def run_width(runs, style, size):
    """Pixel width of marked-up runs."""
    return sum(font(style, size).getlength(t) for t, _ in runs)


def draw_text(draw, cell, text, style, size, fill, align='l', min_size=13):
    """Draw marked-up text in cell=(x, y_centre, width), shrinking to fit."""
    x, yc, width = cell
    runs = parse(text, fill)
    while size > min_size and run_width(runs, style, size) > width:
        size -= 1
    total = run_width(runs, style, size)
    if align == 'c':
        x += (width - total) / 2
    for chunk, colour in runs:
        draw.text((x, yc), chunk, font=font(style, size), fill=colour, anchor='lm')
        x += font(style, size).getlength(chunk)


def wrap(text, style, size, width):
    """Greedy word-wrap on marked-up text (markup spans kept intact)."""
    lines, cur = [], ''
    for word in re.findall(r'\{[^}]*\}[^\s]*|[^\s]+', text):
        trial = f'{cur} {word}'.strip()
        if run_width(parse(trial, WHITE), style, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


KIND_H = {'card': 80, 'pair': 66, 'conj': 58, 'rule': 66, 'head': 34, 'list': 56}
CARD_W = {
    'card': [0.34, 0.33, 0.33],
    'pair': [0.5, 0.5],
    'conj': [0.2, 0.42, 0.38],
    'rule': [0.31, 0.37, 0.32],
}


def row_height(row):
    """Pixel height of a row (before the inter-row gap)."""
    kind = row['k']
    if kind == 'note':
        lines = wrap(row['c'], 'r', 27, W - 2 * PAD_X - 60)
        return 28 + 34 * len(lines)
    if kind == 'big':
        return row.get('h', 120)
    if kind == 'grid':
        base = 62 + (24 if row.get('p') else 0) + (24 if row.get('e') else 0)
        return row.get('h', base)
    return KIND_H[kind]


def cell_boxes(y_mid, widths):
    """Return [(x, y_centre, width)] for each column of a row."""
    inner = W - 2 * PAD_X - 36
    x, boxes = PAD_X + 18, []
    for frac in widths:
        boxes.append((x, y_mid, inner * frac - 12))
        x += inner * frac
    return boxes


def shared_widths(rows):
    """Common column fractions for the 3-column card rows on one slide."""
    cards = [r for r in rows if r['k'] == 'card' and not r.get('w')]
    if not cards:
        has_rule = any(r['k'] == 'rule' and not r.get('w') for r in rows)
        return CARD_W['rule'] if has_rule else None
    base = [('b', 36), ('i', 27), ('r', 27)]
    nat = [0.0, 0.0, 0.0]
    for row in cards:
        for idx, (sty, size) in enumerate(base):
            nat[idx] = max(nat[idx], run_width(parse(row['c'][idx], WHITE), sty, size))
    for row in rows:
        if row['k'] == 'head' and not row.get('w') and len(row['c']) == 3:
            for idx, cell in enumerate(row['c']):
                nat[idx] = max(nat[idx], run_width(parse(cell, WHITE), 'b', 20))
    nat = [width + 30 for width in nat]
    total = sum(nat)
    return [width / total for width in nat]


def draw_row(draw, row, y, hot, accent, shared=None):
    """Draw one row at top y; returns nothing."""
    kind, h = row['k'], row_height(row)
    ymid = y + h / 2
    left, right = PAD_X, W - PAD_X
    if kind == 'head':
        widths = (
            row.get('w')
            or (shared if shared and len(row['c']) == 3 else None)
            or [1 / len(row['c'])] * len(row['c'])
        )
        for box, txt in zip(cell_boxes(ymid, widths), row['c']):
            draw_text(draw, box, txt, 'b', 20, MUTED, row.get('al', 'l'))
        return
    if kind == 'big':
        draw_text(
            draw,
            (left, ymid, right - left),
            row['c'],
            'b' if row.get('b', True) else 'r',
            row.get('s', 56),
            COLORS[row.get('col', 'w')] if row.get('col') else WHITE,
            'c',
        )
        return
    fill = CARD_HOT if hot else CARD
    draw.rounded_rectangle((left, y, right, y + h), 14, fill=fill)
    edge = COLORS[row['col']] if row.get('col') else accent
    draw.rounded_rectangle((left, y, left + 7, y + h), 3, fill=edge)
    if kind == 'note':
        lines = wrap(row['c'], 'r', 27, right - left - 60)
        for i, line in enumerate(lines):
            cy = y + 14 + 17 + 34 * i
            draw_text(draw, (left + 28, cy, right - left - 60), line, 'r', 27, SOFT)
    elif kind in ('card', 'pair', 'conj', 'rule'):
        styles = {
            'card': [('b', 36, WHITE), ('i', 27, COLORS['a']), ('r', 27, SOFT)],
            'pair': [('b', 35, WHITE), ('r', 29, SOFT)],
            'conj': [('r', 27, MUTED), ('b', 36, WHITE), ('r', 26, SOFT)],
            'rule': [('b', 34, WHITE), ('b', 33, (150, 205, 255)), ('r', 26, MUTED)],
        }[kind]
        widths = row.get('w') or (shared if kind == 'card' and shared else None)
        widths = widths or CARD_W[kind]
        cells = zip(cell_boxes(ymid, widths), row['c'], styles)
        for idx, (box, txt, (sty, size, colour)) in enumerate(cells):
            tint = COLORS[row['col']] if row.get('col') and idx == 0 else colour
            draw_text(draw, box, txt, sty, size, tint)
    elif kind == 'list':
        n = len(row['c'])
        for box, txt in zip(cell_boxes(ymid, [1 / n] * n), row['c']):
            draw_text(draw, box, txt, 'r', 29, WHITE)
    elif kind == 'grid':
        n = len(row['c'])
        widths = row.get('w') or [1 / n] * n
        boxes = cell_boxes(ymid, widths)
        has_p, has_e = bool(row.get('p')), bool(row.get('e'))
        offset = -(12 if has_p else 0) - (12 if has_e else 0)
        for i, (box, txt) in enumerate(zip(boxes, row['c'])):
            x0, _, bw = box
            main_y = ymid + offset
            draw_text(draw, (x0, main_y, bw), txt, 'b', row.get('s', 31), WHITE, 'c')
            if has_p:
                py = main_y + 29
                draw_text(draw, (x0, py, bw), row['p'][i], 'i', 20, COLORS['a'], 'c')
            if has_e:
                ey = main_y + 29 + (24 if has_p else 0)
                draw_text(draw, (x0, ey, bw), row['e'][i], 'r', 21, SOFT, 'c')


def gradient():
    """Vertical background gradient (cached as an image)."""
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    for ch in range(3):
        arr[:, :, ch] = np.linspace(BG_TOP[ch], BG_BOT[ch], H)[:, None]
    return Image.fromarray(arr)


@functools.lru_cache(maxsize=1)
def background():
    """Cached background image."""
    return gradient()


def mmss(sec):
    """Format seconds as M:SS."""
    return f'{int(sec) // 60}:{int(sec) % 60:02d}'


def render(frame, scenes, total, chapters):
    """Render one frame to a PIL image."""
    scene = scenes[frame.scene]
    accent = COLORS[scene.accent]
    img = background().copy()
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 4), fill=(245, 245, 245))
    draw.rectangle((0, 4, W, 8), fill=(220, 20, 60))
    if not scene.cover:
        pill = f'CHAPTER {frame.scene} OF {len(scenes) - 1}'
        draw.text((PAD_X, 26), pill, font=font('b', 18), fill=accent, anchor='lm')
        draw.text((PAD_X, 62), scene.title, font=font('b', 40), fill=WHITE, anchor='lm')
        draw.text((PAD_X, 104), scene.sub, font=font('r', 22), fill=MUTED, anchor='lm')
        draw.rounded_rectangle((PAD_X, 124, PAD_X + 90, 128), 2, fill=accent)
    heights = [row_height(r) for r in frame.rows]
    used = sum(heights) + GAP * (len(heights) - 1)
    room = BODY_BOTTOM - BODY_TOP
    if used > room:
        raise ValueError(f'{scene.title}: rows need {used}px but only {room}px fit')
    y = BODY_TOP + (room - used) / 2 if scene.cover else BODY_TOP
    first_hot = len(frame.rows) - frame.hot
    shared = shared_widths(frame.rows)
    for i, row in enumerate(frame.rows):
        draw_row(draw, row, y, i >= first_hot and frame.hot > 0, accent, shared)
        y += heights[i] + GAP
    if frame.overlay:
        cx, cy = W - 120, H - 140
        draw.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=(20, 30, 52))
        draw.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), outline=accent, width=6)
        draw.text(
            (cx, cy - 2),
            str(frame.overlay),
            font=font('b', 78),
            fill=accent,
            anchor='mm',
        )
    bar_y = H - 34
    draw.rounded_rectangle((PAD_X, bar_y, W - PAD_X, bar_y + 8), 4, fill=(40, 54, 86))
    span = W - 2 * PAD_X
    done = PAD_X + span * frame.start / total
    draw.rounded_rectangle(
        (PAD_X, bar_y, max(done, PAD_X + 8), bar_y + 8), 4, fill=accent
    )
    for _, start, _ in chapters[1:]:
        tx = PAD_X + span * start / total
        draw.line((tx, bar_y - 3, tx, bar_y + 11), fill=(120, 140, 180), width=2)
    draw.text(
        (PAD_X, H - 12),
        'Polish A1 revision',
        font=font('r', 16),
        fill=MUTED,
        anchor='lm',
    )
    draw.text(
        (W - PAD_X, H - 12),
        f'{mmss(frame.start)} / {mmss(total)}',
        font=font('r', 16),
        fill=MUTED,
        anchor='rm',
    )
    return img


# ------------------------------------------------------------------- outputs
def write_wav(path, arr):
    """Write mono float audio as 16-bit PCM."""
    # pylint: disable=no-member
    pcm = (np.clip(arr, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes(pcm.tobytes())


def write_chapters(path, chapters):
    """ffmetadata with one CHAPTER block per scene."""
    lines = [';FFMETADATA1', 'title=Polish A1 - full revision', 'artist=Claude']
    for title, start, end in chapters:
        lines += [
            '[CHAPTER]',
            'TIMEBASE=1/1000',
            f'START={int(start * 1000)}',
            f'END={int(end * 1000) - 1}',
            f'title={title}',
        ]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def strip(text):
    """Remove {colour|...} markup from on-screen text."""
    return TOKEN.sub(lambda m: m.group(2), text)


def write_cheat_sheet(path, scenes):
    """Dump every on-screen row to a markdown revision sheet."""
    out = ['# Polish A1 - revision cheat sheet', '']
    for scene in scenes:
        if scene.cover:
            continue
        out += [f'## {scene.title}', f'*{scene.sub}*', '']
        for step in scene.steps:
            for row in step.rows:
                if row['k'] == 'note':
                    out.append(f'> {strip(row["c"])}')
                elif row['k'] == 'grid':
                    for i, cell in enumerate(row['c']):
                        bits = [strip(cell)]
                        bits += [f'`{row["p"][i]}`'] if row.get('p') else []
                        bits += [row['e'][i]] if row.get('e') else []
                        out.append('- ' + ' - '.join(bits))
                elif row['k'] != 'big':
                    out.append('- ' + ' | '.join(strip(c) for c in row['c'] if c))
        out.append('')
    path.write_text('\n'.join(out), encoding='utf-8')


def mux(plan, audio_path, out_dir, meta_path, mp4_path):
    """Encode frames + audio into the final mp4."""
    listing = out_dir / 'frames.txt'
    lines = []
    for frame in plan.frames:
        lines += [f"file '{frame.path}'", f'duration {frame.dur:.3f}']
    lines.append(f"file '{plan.frames[-1].path}'")
    listing.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    subprocess.run(
        [
            'ffmpeg',
            '-y',
            '-loglevel',
            'error',
            '-f',
            'concat',
            '-safe',
            '0',
            '-i',
            str(listing),
            '-i',
            str(audio_path),
            '-i',
            str(meta_path),
            '-map',
            '0:v',
            '-map',
            '1:a',
            '-map_metadata',
            '2',
            '-vf',
            f'fps={FPS},format=yuv420p',
            '-c:v',
            'libx264',
            '-preset',
            'slow',
            '-crf',
            '27',
            '-tune',
            'stillimage',
            '-g',
            '100',
            '-af',
            'loudnorm=I=-17:TP=-2.5:LRA=9,aresample=44100',
            '-c:a',
            'aac',
            '-b:a',
            '56k',
            '-ac',
            '1',
            '-movflags',
            '+faststart',
            '-shortest',
            str(mp4_path),
        ],
        check=True,
    )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', default='build', help='working/output directory')
    parser.add_argument('--no-video', action='store_true', help='audio + timing only')
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    cache = out_dir / 'audio_cache'
    frames_dir = out_dir / 'frames'
    for folder in (cache, frames_dir):
        folder.mkdir(parents=True, exist_ok=True)

    scenes = content.SCENES
    print(f'synthesised {prefetch(scenes, cache)} unique segments')
    plan = build_plan(scenes, cache)
    total = sum(f.dur for f in plan.frames)
    print(f'total duration: {mmss(total)} ({total:.1f}s), {len(plan.frames)} frames')
    for title, start, end in plan.chapters:
        print(f'  {mmss(start)}  {end - start:6.1f}s  {title}')
    if args.no_video:
        return

    problems = []
    for idx, frame in enumerate(plan.frames):
        frame.path = frames_dir / f'f{idx:04d}.png'
        try:
            render(frame, scenes, total, plan.chapters).save(frame.path)
        except ValueError as err:
            problems.append(f'frame {idx} @ {mmss(frame.start)}: {err}')
    if problems:
        raise SystemExit('layout problems:\n' + '\n'.join(problems))
    audio_path = out_dir / 'narration.wav'
    write_wav(audio_path, np.concatenate(plan.audio))
    meta_path = out_dir / 'chapters.txt'
    write_chapters(meta_path, plan.chapters)
    write_cheat_sheet(out_dir / 'polish_a1_cheat_sheet.md', scenes)
    mp4_path = out_dir / 'polish_a1_revision.mp4'
    mux(plan, audio_path, out_dir, meta_path, mp4_path)
    print(f'wrote {mp4_path}')


if __name__ == '__main__':
    main()

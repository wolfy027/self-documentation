# Polish A1 revision video

A 20-minute revision video covering all of Polish A1 for English speakers:
pronunciation, greetings, to be, gender and plurals, adjectives, present tense
verbs, questions and negation, the four A1 cases, prepositions of place,
numbers and time, survival vocabulary, false friends, past and future, a café
roleplay and an 8-question quiz with countdown timers.

| File | What it is |
| --- | --- |
| `polish_a1_revision.mp4` | The video (1280x720, 20:02, 17 chapters you can skip between) |
| `polish_a1_cheat_sheet.md` | Every phrase and table from the video as text |
| `content.py` | The lesson script: on-screen rows and narration, one place |
| `build_video.py` | Builds audio, slides and the mp4 from `content.py` |

## How it was made

- Narration: RHVoice. English narrator `bdl`; Polish voices `magda` (normal
  and slow) and `natan` (second speaker in dialogues).
- Slides: Pillow, one image per reveal step. ffmpeg muxes images + audio,
  adds chapter marks and normalises loudness.
- Pronunciation: every Polish item has an English-friendly respelling on
  screen (CAPS = stressed syllable). Key phrases are said twice, normal then
  slow, with a pause to repeat.

The Polish voice is synthetic. Use the video for structure and repetition, and
check tricky sounds (nasal vowels, sz/cz/rz, soft ś/ć/ź) against a native
speaker in class.

## Rebuild

```bash
sudo apt-get install -y ffmpeg rhvoice rhvoice-english rhvoice-polish
pip install numpy pillow
python3 build_video.py --out build            # full video
python3 build_video.py --out build --no-video # timing check only
```

Edit `content.py`, rebuild, done. Synthesised segments are cached in
`build/audio_cache`, so small edits rebuild quickly.

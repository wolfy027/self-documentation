"""Shared building blocks for the lesson scripts (content_a1.py, content_a2.py).

Narration atoms (en, pl, ps, nt, gap, drill, say) return (voice, text)
segments; row atoms (card, pair, conj, rule, head, note, big, grid, lst) return
dicts that build_video.py renders. step() and Scene group them into chapters.

Markup in on-screen text: {text} = amber highlight, {m|text} masculine blue,
{f|text} feminine pink, {n|text} neuter green, {g|text} green, {r|text} red.
Phonetic respellings are for English speakers: CAPS = stressed syllable,
ah/eh/ee/oh/oo as in father/bed/see/go/boot, ih = the 'i' in bit,
sh/zh/ch/ts as in English, j = 'j' in jam, 'ny' = the 'ny' in canyon.
In English narration, [[...]] marks words spoken by the Polish voice.
"""

import re
from dataclasses import dataclass, field


# ------------------------------------------------------------ narration atoms
def en(text):
    """English narrator; [[Polish]] spans are spoken by the Polish voice."""
    parts = re.split(r'\[\[(.+?)\]\]', text)
    return [
        ('pl' if idx % 2 else 'en', part)
        for idx, part in enumerate(parts)
        if re.search(r'\w', part)
    ]


def pl(text):
    """Polish voice (female), normal speed."""
    return ('pl', text)


def ps(text):
    """Polish voice (female), slow."""
    return ('ps', text)


def nt(text):
    """Polish voice (male) for the second speaker in dialogues."""
    return ('nt', text)


def ns(text):
    """Polish voice (male), slow."""
    return ('ns', text)


def gap(sec):
    """Silence."""
    return ('gap', sec)


def drill(text):
    """Normal, then slow, then a pause to repeat aloud."""
    return [pl(text), gap(0.3), ps(text), gap(1.3)]


def say(polish, english):
    """Polish phrase followed by its English meaning."""
    return [pl(polish), gap(0.15), en(english), gap(0.2)]


# ------------------------------------------------------------------ row atoms
def card(pol, phon, eng, col=None, w=None):
    """Polish | pronunciation | meaning."""
    return {'k': 'card', 'c': [pol, phon, eng], 'col': col, 'w': w}


def pair(left, right, col=None, w=None):
    """Two columns."""
    return {'k': 'pair', 'c': [left, right], 'col': col, 'w': w}


def conj(pron, form, eng, col=None):
    """Pronoun | form | meaning."""
    return {'k': 'conj', 'c': [pron, form, eng], 'col': col}


def rule(left, example, eng, col=None, w=None):
    """Rule | example sentence | meaning."""
    return {'k': 'rule', 'c': [left, example, eng], 'col': col, 'w': w}


def head(*cells, w=None, al='l'):
    """Muted column headings (no card); al='c' centres them over grids."""
    return {'k': 'head', 'c': list(cells), 'w': w, 'al': al}


def note(text, col=None):
    """Wrapped callout."""
    return {'k': 'note', 'c': text, 'col': col}


def big(text, size=56, col=None, h=None):
    """Large centred text."""
    return {'k': 'big', 'c': text, 's': size, 'col': col, 'h': h or size + 30}


def grid(cells, p=None, e=None, size=31, w=None, h=None):
    """Row of cells with optional pronunciation and English lines."""
    return {'k': 'grid', 'c': cells, 'p': p, 'e': e, 's': size, 'w': w, 'h': h}


def lst(*cells):
    """Plain left-aligned list row."""
    return {'k': 'list', 'c': list(cells)}


# ------------------------------------------------------------------ structure
@dataclass
class Step:
    """One reveal: rows added to the slide plus what is said."""

    rows: list
    narr: list
    clear: bool = False
    cd: int = 0  # countdown seconds after narration (quiz)


@dataclass
class Scene:
    """A chapter."""

    title: str
    sub: str
    accent: str
    steps: list = field(default_factory=list)
    cover: bool = False


def flat(items):
    """Flatten nested narration lists."""
    out = []
    for item in items:
        if isinstance(item, list):
            out += flat(item)
        else:
            out.append(item)
    return out


def step(rows, *narr, clear=False, cd=0):
    """Build a Step, flattening narration helpers."""
    return Step(rows, flat(narr), clear, cd)


def quiz(num, total, question, q_narr, answer, explain, a_narr, cd=5):  # noqa: PLR0917
    """Question slide with a countdown, then the revealed answer."""
    return [
        step(
            [head(f'QUESTION {num} OF {total}', al='c'), big(question, 50, 'w', 190)],
            q_narr,
            gap(0.2),
            clear=True,
            cd=cd,
        ),
        step(
            [big(answer, 60, 'g', 120), big(explain, 29, None, 56)],
            pl(answer),
            gap(0.25),
            a_narr,
        ),
    ]

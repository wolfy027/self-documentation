# Polish revision videos (A1 + A2)

Revision videos for English speakers learning Polish, with on-screen
English-friendly pronunciation, slow repeats, quizzes and chapter marks.

| File | What it is |
| --- | --- |
| `polish_a1_revision.mp4` | A1, 20:02, 17 chapters |
| `polish_a2_revision.mp4` | A2, 37:47, 32 chapters |
| `polish_a1_cheat_sheet.md` / `polish_a2_cheat_sheet.md` | Every phrase and table from each video as text |
| `content_a1.py` / `content_a2.py` | The lesson scripts: on-screen rows and narration |
| `lesson.py` | Shared helpers the scripts are written with |
| `build_video.py` | Builds audio, slides and the mp4 from a lesson script |

## What A2 covers

- **Sounds:** voicing assimilation, nasal vowels before consonants, stress exceptions
- **Cases:** all seven cases, softening rules, vocative, the dative in depth
- **Plurals:** virile vs non-virile, genitive plural and counting (incl. numbers for groups of men), dative/instrumental/locative plural
- **Pronouns and verbs:** pronouns in every case, swój and siebie, verbs that govern a case, tricky presents, wiedzieć/znać/umieć/móc
- **Tenses:** verb aspect, the full past tense, both futures
- **Moods and structures:** motion verbs and prefixes, imperative, conditional, comparatives and adverbs, modal/impersonal phrases, linking words and który, some-/no- pronouns
- **Numbers and time:** big numbers, ordinals, dates, time, prepositions of time
- **Real life:** weather, doctor, travel and hotels, work/phone/email, shopping and describing people, restaurant, free time and opinions, celebrations
- **Practice:** a listening story, two role-plays, a 14-question quiz and a recap

## How it is made

- Narration uses RHVoice: the English narrator is `bdl`, and the Polish voices are
  `magda` (normal and slow) and `natan` (second speaker, story).
- Slides are rendered with Pillow, one image per reveal step. ffmpeg muxes the
  images and audio, adds chapter marks and normalises loudness.
- The Polish voice is synthetic. Use the videos for structure and repetition,
  and check tricky sounds with a native speaker.

## Rebuild

```bash
sudo apt-get install -y ffmpeg rhvoice rhvoice-english rhvoice-polish
pip install numpy pillow
python3 build_video.py --level a2 --out build            # full video
python3 build_video.py --level a2 --out build --no-video # timing check only
```

Outputs land in `build/<level>/`. Synthesised speech is cached in
`build/audio_cache`, so edits to a lesson script rebuild quickly. If any slide
has more content than fits, the build lists it and stops.

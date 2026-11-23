---
name: video-essay
description: "Video-essay and documentary-style YouTube editor: script-first, voice-over-led edits with archival footage, B-roll, quote cards, maps, timelines, charts and chapter cards, cut at the pace of an argument (4-8 s shots), filmic grade, sourced on-screen attribution and YouTube chapters. Use when the user says: video essay, documentary-style YouTube video, explain this topic in depth, narrated essay, history/analysis/film-analysis video, edit my VO with archive footage, chapter cards. Default skin essay-mode; any Video Studio skin works."
license: MIT
---

# Video Essay

An argument told in pictures: VO leads, every visual is evidence, chapters keep the viewer oriented.

- **Best for:** analysis, history, film/media essays, science and culture deep dives
- **Inputs:** the recorded VO (or on-camera narration), archival clips/stills and B-roll in a folder, sources list, optional music
- **Default skin:** `essay-mode` · alternatives `doc-real`, `paper-cut`, `swiss-poster` (use `--no-matte` without a presenter)
- **Formats:** 16:9 1920x1080 master, chapters text, `captions.srt`; optional 9:16 teaser
- **Duration target:** 10-40 min; genre preset `video-essay`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre video-essay`.
- The `--genre` preset sets autocut's pause cut (0.6 s) and run.py respects it; pass `--max-gap` only to override.
- **Fair use:** quote clips briefly and comment on them; credit sources on screen; never present someone's claim out of context. Keep a `sources.md`.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| cold open | 0-5 | the most intriguing image or question, before any title |
| thesis | 5-10 | what this video argues, in one sentence |
| chapters | 10-85 | 3-6 chapters, each: claim -> evidence (clip/quote/chart) -> implication |
| turn / counter-argument | 85-92 | the strongest objection, answered |
| conclusion | 92-100 | thesis restated as an insight; end on an image, not "thanks for watching" |

- **Pacing:** ASL 4-8 s; a visual change at least every 6 s. Let a key archival moment play 8-12 s with its own sound. Slow down for the emotional chapter, quicken in montage sections.
- **Cut rules:** cut the VO first (radio edit), then picture. Visuals land 0.1 s before the words that need them. Pauses between chapters are allowed (0.6-1 s).
- **J/L cuts:** archival sound up under the end of a VO line (J) so the clip "speaks"; L-cut the VO over the next visual.
- **Transitions:** cut; dip to black or a chapter card between chapters; dissolves for time passing.
- **Music/SFX:** score bed 24-28 LU under VO, changes mood per chapter; drop it for the revelation. SFX almost none (page-turn on cards).
- **Colour:** unify archive and new footage: `documentary-natural` 0.5 or `fuji-eterna` 0.6; archive can stay as is with `sepia` for flashbacks.
- **Captions:** sidecar SRT; on-screen text only for quotes, names, dates and sources.
- **Client judges:** clarity of the argument, research visuals, accuracy, chapters that make sense.
- **Common mistakes:** visuals that decorate instead of prove, unattributed quotes, music wall-to-wall, a 2-minute intro, uncredited clips.

## Make the edit

With a narration video (on-camera or a VO muxed over a still - see `faceless-explainer` for the TTS route):

```bash
python CORE/scripts/run.py narration.mp4 --style SKILLS/essay-mode --genre video-essay \
  --smart-cuts --retakes --model small --prompt "names, places" --work essay --stop-after plan
python CORE/scripts/story.py outline --work essay --genre video-essay      # paper edit: topic shifts = chapter candidates
python CORE/scripts/broll.py --work essay --library archive/ --frequency high --merge essay/plan.json
python CORE/scripts/editor.py review essay/plan.json --genre video-essay --fix
python CORE/scripts/render.py essay/plan.json --frames 2,60,180,400
python CORE/scripts/render.py essay/plan.json
python CORE/scripts/finish.py essay/plan.json --platform youtube
```

`broll.py` matches archive file names to spoken words; name files for what they show (`berlin-wall-1989.mp4`, `newspaper-headline.jpg`) or add `NAME.txt` keyword files. Place the important evidence shots by hand in `cutaways` (`{"src": "../archive/speech.mp4", "start": 84.2, "end": 95.0, "srcStart": 12}`).

## Refine the plan

- **Chapter cards:** `{"type": "titlecard", "kicker": "Chapter 2", "title": "The Money", "start": 312.0, "end": 315.0}`; also top-level `"chapters": [{"start": 0, "title": "..."}, ...]`.
- **Quotes:** `{"type": "quote", "text": "exact words", "author": "Name", "role": "Source, year"}` held for reading time (>= 1 s per 4 words).
- **Evidence:** `linechart`, `bars`, `barrace` for data (cite the source in a `chip` underneath); `map` with `pins` for places (stylised); `steps` for timelines.
- **Highlighting a document:** `text` with `"fx": {"name": "highlight", "target": "key phrase"}`.
- **Attribution:** a `chip` "Footage: Archive name" in a corner for every borrowed clip.
- **Sound:** `"audio": {"voice": {"eq": "broadcast", "deess": true}}`, `"music": {"src": "score.wav", "under": 26, "duck": "speech-aware"}`.
- **Look:** `"color": {"look": "fuji-eterna", "intensity": 0.6}`, `"finish": {"grain": 7, "vignette": 0.3, "letterbox": 0}`.

## Deliver

```bash
python CORE/scripts/deliver.py essay/plan.json --to youtube --out-dir essay/deliver
python CORE/scripts/qc.py essay/deliver/final_youtube.mp4 --plan essay/plan.json --platform youtube
```

- Paste `chapters.txt` and `sources.md` into the description; upload `captions.srt`.
- Teaser: cut a 45 s vertical from the cold open with `retention-reel`.

## Check before delivering

- Every claim on screen has a source; every quote is verbatim and in context.
- Chapters valid (first at 0:00, >= 3, each >= 10 s) and match the cards.
- VO intelligible over music everywhere; archive audio levels matched.
- `qc.py` passes; no black frames between cutaways.
- Tell the user: runtime, chapter list, sources used, files.

## Example requests

- "Edit my video essay narration with this archive folder, chapter cards and a timeline graphic."
- "Documentary-style YouTube video about the 2008 crash from my VO and these charts."
- "Make it feel like a film essay - filmic grade, quotes on screen, chapters."

---
name: interview-doc
description: "Documentary / interview editor: transcribes the interviews, builds a paper edit and a radio edit (the story in sound first), then covers every interview cut with B-roll, a second angle or a punch-in, with J/L cuts, room tone, light filler removal and a constructed-quote (Frankenbite) guard; delivers the film, a textless version, captions and a music cue sheet. Use when the user says: documentary edit, interview film, edit my interviews into a story, mini-doc, brand documentary, paper edit, radio edit, cover the jump cuts with B-roll, oral history. Default skin doc-real; any Video Studio skin works."
license: MIT
---

# Interview Documentary

Real people, their real words, shaped into a story that is honest and moving.

- **Best for:** mini-docs, brand documentaries, oral histories, profiles, NGO stories, YouTube documentaries
- **Inputs:** interview recordings (A-cam, optional B-cam), B-roll and archive in a folder, names/titles of everyone, music (licensed)
- **Default skin:** `doc-real` · alternatives `essay-mode`, `minimal-mono`, `news-desk`
- **Formats:** 16:9 1920x1080 master, textless version, captions (SRT/VTT), music cue sheet, 9:16 cutdowns
- **Duration target:** 3-30 min (shorts 3-8, festival 15-30+); genre preset `interview-doc`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre interview-doc`.
- The `--genre` preset sets autocut's pause cut (0.9 s) and run.py respects it; pass `--max-gap` only to override.
- **Ethics (non-negotiable):** no Frankenbites - never splice words from different sentences into a statement the person did not make. Reordering whole answers is allowed only when the meaning stays true; flag every such move to the user. Reaction shots must not change what someone meant. Release forms for everyone on camera.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| cold open | 0-5 | the most human moment or the central question |
| world / character | 5-20 | who, where, what life looked like |
| inciting question | 20-30 | what changed / what is at stake |
| development | 30-70 | the journey, obstacles, other voices |
| climax | 70-85 | the hardest or truest moment, given room to breathe |
| resolution | 85-100 | what it means now; end on an image or a line, not a summary |

- **Workflow:** transcribe -> paper edit (pick soundbites in `paper_edit.md`) -> radio edit (sound only, no pictures; it must work with eyes closed) -> cover -> fine cut -> lock -> grade/mix.
- **Pacing:** interview shots 5-15 s, B-roll 2-5 s; breathe 1-3 s after an emotional line (silence, a wide, B-roll with ambience).
- **Cut rules:** cut at the end of a thought; keep breaths before emotional lines; remove only um/uh (`keep-natural`). Keep the person sounding like themselves.
- **Every interview cut is covered:** B-roll overlapping 0.5-1 s each side, a B-cam angle, or a >= 1.2x punch-in. Otherwise it is a jump cut and `editor.py review` flags it.
- **J/L cuts:** next speaker's voice under the end of B-roll (J); a line continuing over a location (L); 0.3-1 s.
- **Transitions:** cuts; dissolves for time passing; dip to black between chapters.
- **Music/SFX:** score bed 26-30 LU under voices, entering on emotional turns and leaving before the important line; ambience under all B-roll; no SFX.
- **Colour:** `documentary-natural` 0.5 or `fuji-eterna` 0.5; match A- and B-cam; skin true.
- **Captions:** sentence-case subtitles (preset `clean` or sidecar), <= 17 cps; name supers (lower thirds) on first appearance.
- **Client judges:** story, truthfulness, emotional arc, everyone looking dignified.
- **Common mistakes:** Frankenbites, uncovered jump cuts, wall-to-wall music, B-roll that illustrates literally every noun, cutting the pause before the tears, wrong name spellings.

## Make the edit

Selects and paper edit per interview:

```bash
python CORE/scripts/selects.py --work int_maria --input maria.mp4 --model small
#  edit int_maria/paper_edit.md: [x] keep / [ ] drop, reorder lines into the story order
python CORE/scripts/selects.py --work int_maria --apply --input maria.mp4 --format 16:9
#  -> int_maria/selects_spec.json (FRANKENBITE warnings: read them, confirm meaning with the user)
```

Combine the interviews' selects into one radio-edit spec (`doc.json`: concatenate the `clips` of each `selects_spec.json` in story order; add `jcut`/`lcut` 0.3-0.8 s between speakers), then:

```bash
python CORE/scripts/run.py - --timeline doc.json --style SKILLS/doc-real --genre interview-doc \
  --smart-cuts --format 16:9 --work doc --stop-after plan
python CORE/scripts/story.py outline --work doc --genre interview-doc       # check the arc against the structure
python CORE/scripts/broll.py --work doc --library broll/ --frequency med --merge doc/plan.json   # covers cuts first
python CORE/scripts/editor.py review doc/plan.json --genre interview-doc --fix   # uncovered jump cuts, pacing
python CORE/scripts/render.py doc/plan.json --frames 5,60,180,300
python CORE/scripts/render.py doc/plan.json
python CORE/scripts/finish.py doc/plan.json --platform youtube
```

`broll.json` lists `uncovered_joins`: cover each by hand (a `cutaways` entry spanning the cut) or a `speaker.zooms` punch-in (scale >= 1.2) starting at the cut.

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Names:** `{"type": "lowerthird", "name": "Maria Okafor", "role": "Nurse, Lagos", "start": 12.0, "end": 16.5}` at each first appearance.
- **Cover cuts:** `"cutaways": [{"src": "../broll/hands-sewing.mp4", "start": 41.4, "end": 45.0, "srcStart": 3}]` (start >= 0.5 s before the join, end >= 0.5 s after).
- **Punch-in:** `"speaker": {"zooms": [{"start": 63.2, "end": 75.0, "scale": 1.2}]}` from the cut to the next cut.
- **Breathing room:** after the climax line, a 2-3 s wide/B-roll with ambience and no music.
- **Archive/quotes:** `quote` only with the exact words; `chip` with the archive credit.
- **Audio:** `"audio": {"voice": {"denoise": "light", "eq": "warm", "deess": true}}, "roomTone": true`, `"music": {"src": "score.wav", "under": 28, "duck": "speech-aware"}`.
- **Look:** `"color": {"look": "documentary-natural", "intensity": 0.5, "match": "hero_frame.png"}`.
- **Captions:** `{"type": "captions", "preset": "clean", "cpsMax": 17}` or none (sidecar only).
- **Footage clean-up:** dim interviews: `--denoise light` (video noise; the voice has its own `audio.voice.denoise`), e.g. `python CORE/scripts/prep.py int01.mp4 --work fix/int01 --denoise light` and use `fix/int01/source.mp4` in `doc.json`; observational handheld B-roll: `--stabilize`; fluorescent offices: `--deflicker`.
- **Privacy:** blur people who did not sign a release, screens, documents and plates with `"blurs": [{"x", "y", "w", "h", "start", "end"}]` (output pixels, top-left box; `"pixelate": true` for a mosaic).

## Deliver

```bash
python CORE/scripts/deliver.py doc/plan.json --to youtube --out-dir doc/deliver
python CORE/scripts/qc.py doc/deliver/final_youtube.mp4 --plan doc/plan.json --platform youtube
python CORE/scripts/export_edl.py doc --out-dir doc/handoff --title "DOC_TITLE"     # if a colourist/mixer takes over
```

- **Textless:** copy the plan, remove lower thirds/quotes/captions, `"outputFile": "doc_textless.mp4"`, render + finish, deliver `prores-422hq` if requested.
- **Music cue sheet:** `cue_sheet.md` - for each music use: track, composer/library, licence, in/out timecode, duration (read the `music` block / premix list).
- **Clearances log:** every B-roll/archive source and its licence; release forms on file.

## Check before delivering

- No constructed quotes; every reordered answer listed and approved; reactions honest.
- No uncovered interview jump cut (`review.md` clean); room tone under every audio edit.
- Names/titles/places triple-checked; captions match the audio.
- Music never covers an important line; `qc.py` passes.
- Tell the user: structure with times, reordering decisions, deliverables, file paths.

## Example requests

- "Make a 10-minute documentary from these three interviews and the B-roll folder."
- "Paper edit first - show me the soundbites you'd use and the story order."
- "Cover all the jump cuts in my interview with B-roll and add name supers."

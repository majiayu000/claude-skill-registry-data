---
name: vox-pop
description: "Vox-pop and street-interview editor: puts the question on screen, then many short answers grouped by intent (yes / no / surprising / funny), each trimmed to its strongest sentence, joined with quick J-cuts, name and location supers, and a closing answer that lands - in 16:9 and 9:16. Use when the user says: vox pop, street interviews, man-on-the-street video, asking strangers, public opinion video, what do people think about X, campus/event interviews, survey video. Answers must not be cut to flip their meaning; everyone on camera needs consent. Default skin news-desk; any Video Studio skin works."
license: MIT
---

# Vox Pop

One question, many voices, grouped so the range of opinion becomes a story.

- **Best for:** street interviews, event/campus questions, brand "what do you think" pieces, social Q&A series
- **Inputs:** interview clips (one per person is easiest), the question, first names / locations people agreed to show, release forms
- **Default skin:** `news-desk` · alternatives `bold-bounce`, `doc-real`, `halo-cut`
- **Formats:** 16:9 1920x1080 master + 9:16 cutdown; `captions.srt` (street audio: captions matter)
- **Duration target:** 45 s - 4 min; genre preset `vox-pop`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre vox-pop`.
- The `--genre` preset sets autocut's pause cut (0.5 s) and run.py respects it; pass `--max-gap` only to override.
- **Ethics:** an answer appears as an answer to the question shown (not to a different one); never trim "I don't think it's bad" into "it's bad"; respect people who asked not to be shown; blur bystanders' faces only if needed (plan `blurs`, see Refine).

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| question card | 0-6 | the question on screen (and asked aloud once) |
| group A | 6-36 | answers with one intent (e.g. "yes"), fastest and clearest first |
| group B | 36-66 | the contrasting intent |
| surprise / outlier | 66-86 | the unexpected or funniest answer |
| closing answer | 86-100 | the line that sums it up or makes people comment |

- **Pacing:** each answer 2-5 s (one sentence); ASL 2-5 s; runs of 3-4 rapid one-word answers are great.
- **Cut rules:** start each answer on its first meaningful word (drop "um, well, I guess"); end on the strong word. Keep the person's real tone.
- **J/L cuts:** the next person's first word 0.1-0.3 s under the end of the previous face (J) keeps it rolling; group changes get a hard cut or a question card.
- **Transitions:** cuts; whip only between locations if the series uses it.
- **Music/SFX:** light bed 26 LU under, ducked; a `pop` on the question card; no laugh effects.
- **Colour:** street footage varies: auto-correct each clip, `documentary-natural` 0.4.
- **Captions:** always (noisy street audio) - preset `boxed` (9:16) or `clean` (16:9); names via supers.
- **Client judges:** range of voices, pace, fairness, readable captions.
- **Common mistakes:** all answers the same intent, long answers, captions missing on wind-blown audio, names wrong, cutting someone into saying the opposite.

## Make the edit

Transcribe every answer, then write the order:

```bash
python CORE/scripts/run.py - --clips vox/*.mp4 --auto story --style SKILLS/news-desk --genre vox-pop \
  --smart-cuts --format 16:9 --model small --work vp --stop-after timeline
#  read vp/timeline.json + vp/words.json: which answer is which person, what they said
```

`--auto story` keeps the speech regions of each clip in file order. Re-order by intent in a hand spec (`vp_spec.json`, times = each clip's source seconds, `jcut: 0.2` on each answer), then:

```bash
python CORE/scripts/run.py - --timeline vp_spec.json --style SKILLS/news-desk --genre vox-pop \
  --smart-cuts --format 16:9 --work vp2 --stop-after plan
python CORE/scripts/editor.py review vp2/plan.json --genre vox-pop --fix
python CORE/scripts/render.py vp2/plan.json --frames 1,8,20,40
python CORE/scripts/render.py vp2/plan.json
python CORE/scripts/finish.py vp2/plan.json --platform youtube
```

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Question card:** `{"type": "titlecard", "kicker": "We asked Mumbai", "title": "Would you take a 4-day week for less pay?", "start": 0, "end": 2.8}`; repeat as a small `chip` top-left for the rest of the video.
- **Supers:** `{"type": "lowerthird", "name": "Aarav", "role": "Student, Pune", "start": 3.1, "end": 5.4}` per person (first names only unless they agreed to more).
- **Group labels (optional):** a `chip` "YES" / "NO" at each group's start.
- **Tally:** a `poll` or `donut` at the end with the real count of answers you filmed (`"options": [{"label": "Yes", "pct": 62}, {"label": "No", "pct": 38}]`), labelled "of the people we asked" - never as a survey result.
- **Captions:** `{"type": "captions", "preset": "boxed", "cpsMax": 17}`; fix mis-heard words in `plan.words` (street audio).
- **Sound:** `"audio": {"voice": {"denoise": true, "eq": "clear"}}`, `"roomTone": true`, `"music": {"src": "bed.mp3", "under": 26, "duck": "speech-aware"}`.
- **Look:** `"color": {"look": "documentary-natural", "intensity": 0.4}`.
- **Bystanders:** blur faces of people in the background who did not consent with `"blurs": [{"x": 1420, "y": 260, "w": 200, "h": 240, "start": 31.0, "end": 34.5}]` (output pixels, top-left box; `"pixelate": true` for a mosaic; one box per answer). Check each in the `--frames` stills.

## Deliver

```bash
python CORE/scripts/deliver.py vp2/plan.json --to youtube,reels --out-dir vp2/deliver
python CORE/scripts/qc.py vp2/deliver/final_reels.mp4 --plan vp2/plan.json --platform reels
```

- For a native 9:16, rebuild the spec with `"format": "9:16"` and `"reframe": "face"` on every clip.
- Keep `releases.md`: person, clip file, consent given (yes/no, how).

## Check before delivering

- Every answer answers the question shown and keeps its meaning.
- Names and places correct; nobody shown who declined.
- Captions on every answer, synced; audio intelligible over street noise.
- `qc.py` passes; tell the user: number of answers used, grouping, files.

## Example requests

- "Cut my street interviews into a 90-second vox pop - question card, yes answers, no answers, funniest at the end."
- "Vertical vox pop with big captions and first-name supers."
- "Make our event interviews into a quick 'what did you think' video."

---
name: news-explainer
description: "News and explainer editor for Claude: turns a presenter clip, voice-over or interview into a sourced, inverted-pyramid explainer (key fact first, why it matters, context, data, what next) with attribution on screen, charts and maps, neutral music, accurate captions, a 16:9 master and vertical cutdowns. Use when the user says 'make a news explainer', 'explain this story', 'news update video', 'breakdown of what happened', 'market news short', 'fact-based explainer with sources', 'turn this report into a video'. Runs on video-studio-core (transcribe, autocut, charts, colour, deliver, QC). Not for opinion rants dressed as news."
license: MIT
---

# News Explainer

The fact first, the source on screen, the context after, and nothing the evidence doesn't support.

- **Best for:** news updates, market and policy explainers, "what happened and why", research summaries, local news
- **Inputs:** presenter clip or VO, the sources (links, documents, data), optional B-roll/maps/stills with their licences
- **Default skin:** `news-desk` · alternatives `data-story`, `essay-mode`, `swiss-poster` (needs `--no-matte` or a matte)
- **Formats:** 16:9 master, 9:16 cutdowns
- **Durations:** 60 s-8 min master; 30-60 s cutdowns
- **Genre preset:** `--genre news-explainer`

## Before you start

- Needs **video-studio-core** in the same skills folder (`CORE`); `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- **Sourcing is the job.** Get the source for every number, quote and claim before editing. Each data graphic carries a
  source chip ("Source: ONS, Oct 2026"). If a claim has no source, raise it with the user; do not illustrate it.
- Quotes of real people: their real words, in context, no frankenbites (`story.py reorder` flags them).
- Footage and photos must be the user's, licensed, or clearly fair-use commentary with credit. No logos or screenshots
  styled to look like a real outlet's broadcast, and never a "LIVE" or "BREAKING" badge on a recorded explainer.
- Private individuals, minors and victims: blur or omit unless the user confirms consent or clear public interest.

## How a pro cuts this

**Structure (inverted pyramid, % of length)**

| beat | % | what |
| --- | --- | --- |
| key fact | 10 | the news in one sentence, on screen as a headline, in the first 3 s |
| why it matters | 15 | who is affected and how much |
| context | 35 | how we got here: timeline, map, background |
| data / evidence | 25 | the numbers as charts, each with its source; quotes with attribution |
| what next | 15 | what happens next, what is unknown, where to read more |

**Pacing.** ASL 3-6 s, visual change at least every 5 s (graphic, B-roll, punch-in). Max gap 0.4 s, fillers removed,
retakes removed. Calm, not frantic: a news explainer earns trust by not shouting.

**Cut rules.**
- No hype hook: the hook is the fact itself. No greeting, no "in this video".
- Every jump cut in a presenter piece is fine at this pace, but cover interview cuts with B-roll or a graphic.
- Hold a chart until it has been read (>= 4 s), and say the number while it is on screen.
- Separate fact from analysis visibly (presenter on camera for analysis, graphics for facts).
- Never change a quote's meaning with the shot around it (Kuleshov) or by trimming its qualifier.

**Transition grammar.** Straight cuts; J/L cuts 2-4 frames on presenter joins; a short dissolve only between sections.
No whips, glitches or flashes.

**Music and sound.** Neutral bed at -28 dB under speech, ducked; none under quotes from victims or sensitive topics.
SFX very low (a soft `ui-tap` on a chart reveal at most). Dialogue clear: `broadcast` EQ, de-ess.

**Colour.** Natural: `documentary-natural` at 0.4-0.5 (or `none`). No stylised looks on real-world footage.

**Captions.** Two-line sentence-case subtitles (`"preset": "clean"`, <= 20 cps), names and numbers checked against the
sources. Sidecar SRT for YouTube. Lower third for every person who speaks, with role.

**What the client judges.** Accuracy, attribution on screen, clarity, and speed to publish.

**Common mistakes.** A number on screen without a source; a misleading thumbnail or headline; a chart axis that
exaggerates; old footage presented as new (label "File footage, 2023"); stock music too dramatic; captions with
mis-heard names; "BREAKING" on a non-breaking story.

## Make the edit

```bash
python CORE/scripts/run.py presenter.mp4 --style SKILLS/news-desk --genre news-explainer --format 16:9 --smart-cuts --retakes --prompt "ONS, Reserve Bank, Priya Rao" --model base --work nx --stop-after plan
python CORE/scripts/story.py outline --work nx --genre news-explainer    # sentences + the genre beat map
python CORE/scripts/render.py nx/plan.json --frames 1,4,8,13,15
python CORE/scripts/render.py nx/plan.json
python CORE/scripts/finish.py nx/plan.json --platform youtube
```

The genre preset sets the pause cut (0.4 s). With a B-roll folder
(files named after what they show) add `--broll broll/` and stop with `--stop-after broll` instead of `plan`
(`--stop-after plan` exits before the B-roll step).

**Reorder so the key fact leads** (when the presenter buried it):
`python CORE/scripts/story.py reorder --work nx --order "s4,s1-s3,s5-s9" --genre news-explainer --format 16:9`,
then `python CORE/scripts/run.py - --timeline nx/story_timeline.json --style SKILLS/news-desk --genre news-explainer --format 16:9 --model base --work nx2 --stop-after plan`.
Check `nx/story_flags.md`: whole sentences only.

**No presenter on camera:** record or synthesise the VO (`python CORE/scripts/tts.py --script vo.txt --out vo/voice.wav --words`;
label synthetic voices as such), then follow the `faceless-explainer` skill (VO + B-roll + captions) and keep every sourcing rule above.

## Refine the plan

The draft from news-desk adds a "BREAKING" ticker, a "LIVE" chip and a lower third filled with the first sentence.
Replace them:

- **Delete** the `chip` "LIVE" and fix the `ticker`: `{"type": "ticker", "label": "EXPLAINER", "text": "Small business · three costly mistakes · what to fix first", "y": 1000}`
  (y about 1000 keeps it inside a 1080 frame; 1040 clips).
- **Lower third:** `{"type": "lowerthird", "name": "Priya Rao", "role": "Small-business analyst", "className": "nd-lt", "start": 0.3, "end": 4.5}`.
- **Key-fact headline:** `{"type": "headline", "text": "3 mistakes, $10,000 lost", "start": 0, "end": 2.6, "x": 1560, "y": 250, "w": 600, "in": "maskUp", "out": "fade"}` — keep it off the face.
- **Data + source:** `{"type": "bars", "title": "Growth after fixing all three", "items": [{"label": "Before", "value": 100}, {"label": "After", "value": 150, "highlight": true}], "suffix": "%", "start": 11.6, "end": 15.5, "x": 1580, "y": 420, "w": 600, "h": 460}`
  and right under it `{"type": "chip", "text": "Source: speaker's own figures, 2026", "x": 1580, "y": 700, "start": 11.6, "end": 15.5, "style": {"fontSize": "24px"}}`.
  Trends: `linechart`; shares: `donut`; places: `map` (a stylised dot map, **not** real geography: label it, or use a
  real map image with credit as an `image` element).
- **Captions:** `{"type": "captions", "preset": "clean", "y": 870}` above the ticker.
- **Fix split numbers in `words`:** Whisper writes "$10" ",000." and "50" "%" as separate words; the creator captions
  show "$10 ,000" unless you merge them (join the text, keep the first start and the last end). Check every auto
  `counter` for the same reason.
- **Colour/sound:** `"color": {"look": "documentary-natural", "intensity": 0.5}`, `"finish": {"grain": 0}`,
  `"audio": {"voice": {"eq": "broadcast", "deess": true}}`, `"music": {"src": "neutral.wav", "under": 24, "duck": "speech-aware"}`.
- `python CORE/scripts/editor.py review nx/plan.json --genre news-explainer` — its "no hook text in 5 s" note is solved by the headline.
- **Protect identities:** blur private individuals, minors, plates and documents in footage with `"blurs": [{"x": 300, "y": 220, "w": 220, "h": 260, "start": 18.0, "end": 22.5, "pixelate": true}]` (output pixels, top-left box). It sits under the graphics, so the lower third stays sharp.

## Deliver

```bash
python CORE/scripts/deliver.py nx/plan.json --to youtube,shorts --out-dir nx/deliver
python CORE/scripts/qc.py nx/deliver/final_youtube.mp4 --plan nx/plan.json --platform youtube --strict
python CORE/scripts/qc.py nx/deliver/final_shorts.mp4 --platform shorts    # no --plan: the plan is 16:9, the file is reframed
```

`final_shorts.mp4` from a 16:9 plan is a blurred-fill reframe; for a real vertical cutdown re-run the pipeline with
`--format 9:16` on the chosen section. Put every source link in the description (start from `post.md`, which only
drafts from the transcript: add the sources yourself). Re-check `post.md` titles: no claim the video doesn't support.

## Check before delivering

- Every number, name, date and quote on screen matches its source; every data graphic has a source chip.
- No graphic covers a face; ticker and captions don't overlap; nothing outside the 5% title-safe area.
- Charts honest: bars start at zero, units shown, period labelled.
- Archive or file footage is labelled; nothing implies "live" or "breaking".
- `qc.py`: loudness -14 LUFS / -1 dBTP, captions within 20 cps, no flash frames.
- Tell the user which claims you could not verify.

## Example requests

- "Make a 3-minute explainer from my recording about the new tax rule, sources are in this doc."
- "Turn this market update into a 16:9 video with charts and a 45-second vertical."
- "News-style breakdown of what happened at the council meeting, lower thirds for each speaker."

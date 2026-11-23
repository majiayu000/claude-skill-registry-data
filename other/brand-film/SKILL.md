---
name: brand-film
description: "Brand film editor for Claude: turns founder and team interviews, product and place B-roll and a licensed track into a 2-3 min mission-driven hero film plus 60 s and 30 s cutdowns and social verticals, with brand-guide lower thirds and colour-matched cameras. Use when the user says 'make our brand film', 'company story video', 'about us video', 'manifesto film', 'founder story', 'corporate film for the website', 'cut a hero video and a 30 second version', or hands over interview footage plus brand colours/logo. Runs on video-studio-core (transcribe, selects, story, timeline, B-roll, colour, mix, deliver, QC)."
license: MIT
---

# Brand Film

The company's reason to exist in 2-3 minutes: people first, product second, logo last.

- **Best for:** about-us films, founder stories, manifesto films, recruiting films, corporate hero videos
- **Inputs:** 1-4 interviews (founder, team, customer), B-roll of people/product/place, logo PNG, brand fonts and colours, one licensed track
- **Default skin:** `frame-studio` · alternatives `kinetic-launch`, `doc-real`, `minimal-mono` (and `logo-sting` for the end sting)
- **Formats:** 16:9 hero master, 9:16 and 4:5 cutdowns
- **Durations:** hero 90-180 s, cutdowns 60 s and 30 s
- **Genre preset:** `--genre brand-film` (`python CORE/scripts/editor.py genre brand-film`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py` and fix what it reports.
- Ask for: the one sentence the film must leave behind, the brand guide (hex colours, fonts, logo lockup and clear
  space), names and job titles exactly as they should appear, the music licence, legal claims that need approval.
- Every person on camera has signed a release. Statements of fact ("#1 in India", "40% faster") need a source the
  client can stand behind; flag them, don't invent them.

## How a pro cuts this

**Structure (hero, % of length)**

| beat | % | what goes here |
| --- | --- | --- |
| hook | 8 | one striking image or line that is not the logo; the question the film answers |
| problem / world | 17 | the world before: the customer's pain, the founder's frustration |
| mission / solution | 35 | why the company exists, how it works, shown not told |
| proof / people | 25 | team, customers, results, real moments |
| vision + logo | 15 | where it goes next, final line, logo lockup and URL |

**Pacing.** ASL 3-6 s; interview shots 5-10 s, B-roll 2-4 s; a visual change at least every 5 s. Breathe 1-2 s after
the emotional line before the next idea.

**Cut rules.**
- Paper edit first: build the story from soundbites (`story.py outline`, `selects.py`), radio edit, then cover.
- No visible jump cuts: cover every interview join with B-roll (>= 0.5 s each side), a second angle or a >= 1.2x punch-in.
- J-cut the next speaker 0.3-1 s under B-roll; L-cut a strong line over the people it is about.
- Keep the best performance, not the cleanest take. Light filler removal; keep the breath before a key line.
- No frankenbites: never join words from different answers into a claim the person did not make.

**Transition grammar.** Straight cuts and split edits; one dissolve family for time/mood shifts; match cuts between
ideas if the footage offers them. No whips, glitches or flashy wipes.

**Music and sound.** Licensed track as a bed (~-22 dB), ducked under speech, lifted in B-roll gaps; build to the
vision section and land the logo on a downbeat (`fitTo: "beats"`, `endButton: true`). Room tone under every join.
SFX low (about 4/min): a soft whoosh into the logo at most.

**Colour.** Match cameras first (`color.match` to one hero frame), skin before look. `kodak-2383` for cinematic,
`clean-commercial` or `cool-corporate` for tech, `portra` for warm human brands. Intensity 0.5-0.7.

**Captions.** Brand-font subtitles, `"preset": "clean"`, sentence case, <= 17 cps. Lower thirds in brand colours.

**What the client judges.** Brand compliance (fonts, colours, logo), executives looking good, message clarity.

**Common mistakes.** Opening on the logo; a CEO monologue with no pictures; stock-looking B-roll that decorates;
mismatched skin between cameras; music that fights the voice; wrong job title in a lower third.

## Make the edit

```bash
# one interview: transcribe, cut, draft plan (brand-film max gap is 0.5 s)
python CORE/scripts/run.py founder.mp4 --style SKILLS/frame-studio --genre brand-film --format 16:9 --smart-cuts --retakes --logo logo.png --title "Built for makers" --work bf --stop-after plan
# paper edit: hooks, structure, order
python CORE/scripts/story.py outline --work bf --genre brand-film
python CORE/scripts/story.py reorder --work bf --order "s7,s1-s5,s9-s12" --genre brand-film --format 16:9 --out bf/story_timeline.json
python CORE/scripts/run.py - --timeline bf/story_timeline.json --style SKILLS/frame-studio --genre brand-film --format 16:9 --music track.wav --broll broll/ --work bf2 --stop-after broll
python CORE/scripts/render.py bf2/plan.json --frames 2,15,40,80,120
python CORE/scripts/render.py bf2/plan.json
python CORE/scripts/finish.py bf2/plan.json --platform youtube
```

Several interviews or long takes: `python CORE/scripts/selects.py --work sel --input interviews.mp4`, tick
`paper_edit.md`, `python CORE/scripts/selects.py --work sel --apply --format 16:9`, then
`run.py - --timeline sel/selects_spec.json ...` as above. `--broll` only runs when you stop after `broll` (or later).

**Cutdowns:** reorder a shorter paper edit (`story.py reorder ... --out bf/cut30.json`), build it in its own work folder
with `--duration 30`, `--format 9:16` for the vertical. Rebuild the 30 s around one idea; do not just trim the hero.

## Refine the plan

- **Captions:** keep one `captions` element with `"preset": "clean"`, brand font via `style`
  (`{"fontFamily": "Inter"}`), or remove it for the hero and deliver sidecar SRT instead.
- **Lower thirds:** `{"type": "lowerthird", "name": "Asha Mehta", "role": "Co-founder & CEO", "start": 4.2, "end": 8.5, "in": "maskUp"}`
  at each person's first line; brand colours in `theme.vars` (`"--c-accent": "#0057FF"`).
- **Colour:** `"color": {"look": "kodak-2383", "intensity": 0.6, "match": "hero_frame.png"}`, `"finish": {"grain": 3, "vignette": 0.3}`.
- **Music:** `"music": {"src": "track.wav", "under": 20, "duck": "speech-aware", "fitTo": "beats", "endButton": true}`, `"roomTone": true`.
- **Voice:** `"audio": {"platform": "youtube", "voice": {"denoise": "light", "eq": "broadcast", "deess": true}}`.
- **Logo end card:** `{"type": "image", "image": "{logo}", "start": 112, "end": 118, "in": "fade", "w": 520}` or a
  `titlecard` with the final line; land it on a downbeat.
- **Numbers:** check every `counter` make_plan added (value and label must match what is said); fix or delete.
- Remove auto `card`/`chip` elements that don't fit a brand film (subscribe chips, list cards).
- `python CORE/scripts/editor.py review bf2/plan.json --genre brand-film` and fix every uncovered jump cut it lists.
- Check B-roll `cutaways` placement in the `--frames` stills (they show the cutaway on screen).

## Deliver

```bash
python CORE/scripts/deliver.py bf2/plan.json --to youtube,linkedin,prores-422hq --out-dir bf2/deliver --burn no
python CORE/scripts/deliver.py bf30/plan.json --to reels,linkedin --out-dir bf30/deliver
python CORE/scripts/qc.py bf2/deliver/final_youtube.mp4 --plan bf2/plan.json --platform youtube --strict
```

Hand over: hero 16:9, 60 s and 30 s cutdowns, verticals, `captions.srt`, a textless master if they will re-version
(remove text elements, render again), and the music licence. Name files `brand_hero_v003_16x9.mp4`.

## Check before delivering

- Every name and title spelled as the client wrote it; logo clear space respected; colours match the brand hex.
- Skin matches across cameras on the contact sheet and in the full render; no uncovered jump cut.
- Every claim has a source; no constructed quotes; releases on file.
- `qc.py` passes (-14 LUFS, -1 dBTP), music ends on a resolved bar, captions <= 17 cps.

## Example requests

- "Here are three interviews and our B-roll, make a 2-minute brand film for the homepage."
- "Cut a 30-second and a vertical version of the founder story for LinkedIn."
- "Use our brand colours and font for the lower thirds and end on the logo."

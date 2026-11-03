---
name: nextphase-screenshare
description: >-
  Edit a LONG-FORM 16:9 talking-head video (YouTube) in the SCREENSHARE style: the video behaves like
  a live screen-share call. The camera is a panel that TRAVELS (never cuts) between full frame, a
  half-screen card beside a real interface, and a 300px corner card while a big UI does the demo. The
  screen shares are PLAYED for the creator — rebuilt UIs with a scripted cursor, typing and clicks,
  plus real captured websites — on a breathing dot-field ground in the creator's own colours. Measured
  layout mix (16% full camera / 39% half / 35% demo), a layout change every ~8s, captions locked in
  one place. Uses HyperFrames (HTML→MP4), all free. Invoke when the user drops a recording and asks to
  edit it with nextphase-screenshare / "the screenshare style", or asks to set up / re-theme this
  skill.
---

## Video Studio (read first; overrides the rest of this file)

This skill is installed in Video Studio (`Edits/.claude/skills/`), from the NextPhase / creator packs
Bryan downloaded on 2026-10-31. Video Studio's `CLAUDE.md` wins wherever the two disagree.

- **Start from the studio job, never an intake.** Jobs come from the studio page (`jobs/<id>/job.json`).
  This skill runs when the job's `style` is `screen-share-demo`. Never ask "short or long?" or "which style?":
  the page already asked. (`nextphase-studio`'s intake is not used here.)
- **One transcript:** `projects/<id>/transcript/words.json` (WhisperX). Don't run this skill's own transcriber.
- **Brand:** `styles/brand.json` (purple `#8B5CF6` / `#C4B5FD` / `#4C1D95`, Inter + Playfair Display)
  replaces this skill's default colours. Generate its theme/tokens from it.
- **Show the motion graphics before rendering (Bryan's rule):** design first, show stills of each graphic over
  the real frame in batches (the `design` → `graphics` stages, `graphics.json`), wait for approval, then render.
- **Sounds and music:** the studio's library (`styles/sfx.json`, `node studio/sfx.mjs place`) on the locked
  picture; music only from tracks Bryan owns or licensed.
- **Windows Git Bash, not macOS/WSL:** `python` not `python3`; a venv's Python is `Scripts/python.exe`;
  long paths fail, so map a short drive (`cmd //c "subst R: <winpath>"`). Run this skill's setup/doctor script
  only the first time the style is used, and ask before any download over ~500 MB.
- **Where work goes:** editing work in `projects/<id>/`, deliverables in `jobs/<id>/`.
- Its setup asks brand questions: answer them from `styles/brand.json` (dark, purple) instead of asking Bryan again.


# nextphase-screenshare

A talking head goes in; an edit comes out that looks like **the creator joined
a call with the viewer and shared their screen** — except nobody recorded a
screen. Every "open this, click that, type this" line is played back as a
rebuilt interface with a cursor doing exactly what they say, and every website
they mention is the real page, captured and scrolled. The camera never cuts
away to make room: it travels into a half-screen card, into the corner, and
back out.

---

## 0 · FIRST: read `brand/brand.md`

```bash
cat ~/.claude/skills/nextphase-screenshare/brand/brand.md
```

**If it says `STATUS: UNFILLED`, stop and run setup before touching any video.**
Ask these as ONE numbered list, then wait for the answers. Never guess one.

1. **Your channel** — name, @handle, the niche you're in, and who watches
   (e.g. "Garden Lab, @gardenlab, home gardening, beginners with a balcony").
2. **Ground** — **bright** (warm paper), **dark**, or **classic** (plain white,
   no dot field).
3. **Accent colour** — orange, green, blue, purple, pink, red, yellow, teal,
   or your exact brand hex. Optionally a second brand colour (it becomes the
   highlighter).
4. **Font feel** — **clean** modern (Inter), **condensed** bold (Barlow
   Condensed), **serif** editorial (Fraunces), or name any Google Font.
5. **Research** — how much should Claude go and find on its own?
   **0** "I bring everything" · **1** light: verify every number and claim,
   capture every site/product named · **2** deep: also find real examples,
   docs, clips for each point, and flag clip rights.
6. **Token budget** — **lean** (cheapest), **balanced**, or **max** (best
   quality, most tokens). §4 says exactly what changes.
7. **Captions** on/off · **sound effects** on/off · **music** on/off.
8. **Camera card side** — **left**, **right**, or **swap** between beats.

Then write the answers and theme:

```bash
SK=~/.claude/skills/nextphase-screenshare
python3 $SK/scripts/make-theme.py --json '{"filled":true,"channel":"…","handle":"@…",
  "niche":"…","audience":"…","ground":"bright|dark|classic","accent":"orange|…|#RRGGBB",
  "accent2":null,"font":"clean|condensed|serif|<Google Font>","research":0|1|2,
  "tokens":"lean|balanced|max","captions":true,"sfx":true,"music":false,
  "camera_side":"left|right|swap","language":"en"}'
python3 $SK/scripts/make-preview.py          # 13s preview in their colours, opens it
```

make-theme.py contrast-checks the accent on the chosen ground and nudges its
lightness if it would not read — **tell the user when it does** (the report
says so). Show them the preview and ask if the colours are right. Re-theme any
time by re-running the same two commands; existing videos keep the theme they
were created with.

Before editing a video, confirm with the user (one line) if they want any of
brand.md's settings different *for this video* — then edit the project's own
`brand.json` snapshot, not the skill's.

---

## 1 · The look in one paragraph

A warm paper (or dark, or white) ground with a slow-breathing dot skyline
across its lower half. A real interface sits on it as a rounded card with a
neutral shadow, and the camera sits beside it as a tall card — or parked as a
300px square in the corner while the interface goes big. A cursor moves
through the UI, text types itself in, a page scrolls, a file appears on the
word that names it. Every ~8 seconds the layout changes, and the camera
*travels* there over 11–14 frames on a solved ease, rounding its corners as it
goes. One caption, always in the same place. Your accent marks the one thing
that matters in a frame; green means a win, red means a cost. No emojis, no
decoration, nothing that isn't real.

---

## 2 · Hard rules

1. **Never hardcode a colour or font.** Compositions import `assets/tokens.css`
   (generated from brand.json) and use `--ss-*` variables only. Rebuilt demo UIs
   are the one exception: they are media and carry the app's own colours.
2. **The camera travels, it never cuts.** Full ↔ corner in 11/10 frames,
   half ↔ half in 14, anything else in 11–12, all on `cubic-bezier(.42,0,.66,1)`
   (solved against measured widths), radius ramping with progress. Full-bleed
   footage has square corners. `reference/motion-grammar.md` §1.
3. **Real media only.** Every beat that supports a point shows something real:
   a rebuilt UI of a real product (against current screenshots), a real page
   capture, a file the creator supplied, a real number. A beat with nothing real
   to show stays on the camera. **Check every capture actually rendered content**
   — login walls and scroll-reveal pages come back blank but plausible.
4. **No random people as b-roll.** Show a person only when that person is the
   subject of the line.
5. **No emojis anywhere on screen.** Draw the mark (CSS tile, small SVG).
6. **Every on-screen word comes from THIS video's transcript**, in the
   creator's vocabulary. The template's example copy is placeholder.
7. **Verify facts while sourcing** (research level 1+). Caption live numbers,
   flag stale or false claims — including ad-libs — before they reach a render.
   Flag any third-party clip whose rights are unclear.
8. **Animate transforms and opacity only** (plus the camera's `clip-path`).
   Never `top/left/width/height`. Everything on ONE paused GSAP timeline;
   `immediateRender:false` on every `fromTo`.
9. **Nothing publishes.** Deliver `out/final.mp4`, open it for review, stop.
   Never upload, post or schedule without explicit approval.

---

## 3 · Research level (brand.json `research`)

| level | what you do on your own | what you never do |
|---|---|---|
| **0 · I bring everything** | use only files/links the creator gave; rebuild UIs only from what they showed you | browse, search, or pull clips |
| **1 · Light** (default) | verify every number, date, price, claim and ad-lib against a primary source; capture every site and product named (scripts/capture.js); rebuild named products against current screenshots | pull video clips |
| **2 · Deep** | everything in 1, plus find real supporting examples for each point (docs pages, launch posts, good/bad examples), short clips where they add something, and a rights note for each clip | ship a clip with unclear rights without flagging it |

At every level, put what you could not verify in PLAN.md "Facts to verify"
and ask, rather than guessing.

## 4 · Token budget (brand.json `tokens`)

| | **lean** | **balanced** (default) | **max** |
|---|---|---|---|
| reading | this file + only the reference named for the step you're on | the references the step needs | every reference file before planning |
| subagents | none | for sourcing when there are 5+ captures | parallel subagents for sourcing and fact-checking |
| planning | a compact layout table | full PLAN.md | full PLAN.md + per-beat source list |
| demos | reuse one demo across HALF → CORNER; fewest distinct demos that keep a change every ~8s | one demo per distinct action | one demo per action, snapshot-checked before render |
| previews | `hf snapshot` stills or one 540p draft of the segment you changed | 540p draft per segment | full-quality render of every segment |
| final render | once, at the end | once, plus fixes | as many passes as needed |
| gates | check-screenshare.sh before the final render | + check-contrast on the final | every gate on every render |

Lean still follows every hard rule — it saves tokens on *process*, never on
what reaches the screen.

---

## 5 · Layouts — the measured mix

| `cam` | camera rect | share target | what's on the surface |
|---|---|---|---|
| `FULL` | 1920×1080, r0 | 14–18% | nothing — the caption only (breathers, chapter openers) |
| `HALF` | 560×740 at x60 or x1300, y60, r28 | 36–42% | one UI card 1184×740 on the other side |
| `CORNER` | 300×300, 60px off the corner, r40 | 32–38% | a big UI (up to 1480×740) doing the demo |
| PAGE | `CORNER` + `box="ss-bleedsafe"` | ~4% | a full-width page running under the card |
| no-cam | — | ~6% | a full-screen graphic (chapter card, document) |

- **A layout change every 7–9s**, and a content change inside a layout about
  every 5s. Uniform alternation is as wrong as a 40-second hold.
- `camera_side: swap` alternates HALF sides; `left`/`right` pin both the half
  and the corner card.
- ~40% of graphics time has something moving; the rest holds still to be read.
- The geometry is exact (60+1184+56+560+60 = 1920) and every panel stops at
  y=800 so the caption band is always clear.

Full detail: `reference/demo-mix.md` (the variant), `reference/layouts.md`
(devices and composition patterns).

## 6 · What goes on screen

- **Played screen shares** (`demos/make_demos.py`, helpers in `demolib.py`):
  `mv`, `click`, `type`, `show`/`hide`, timed in demo-local seconds to word
  onsets. Rendered to `assets/broll/<name>.mp4`, placed with `panel()`.
- **Real sites**: `scripts/capture.js` tall capture → scrolled inside a rebuilt
  browser (`d3_page`).
- **Devices** (`devices.py`): `panel`, `shot`, `window`, `callout`, `compare`,
  `board`, `lst`, `big`, plus marks (highlighter, underline, circle) drawn once
  over a still. Markup reference: `components/screenshare-system.html`.
- A "bad example" is one you make, labelled on screen as made for this video.

## 7 · Captions (if on)

Centred, cap-top locked at y=848 on every layout, 80px, 2–6 words, median
hold ~18 frames, a 2-frame cross-fade (never a hard cut), never swapping
mid-travel (build.py enforces it). On the ground: `--ss-ink`. On footage:
white with a soft shadow, gated by `check-contrast.py`. One accented word per
caption at most, and only when it is doing a job (`live` / `win` / `cost`).
`reference/captions.md`.

## 8 · Sound

sfx on: one quiet synthesised transient per layout change, nothing else —
build.py writes the cues. Music on: one ducked bed the creator supplies in
`assets/music/`. Both off: voice only. `reference/sound-design.md`.

## 9 · Build order

`reference/workflow.md` has every command. Short version:

1. brand.md check (§0) → `scripts/new-video.sh <recording>`
2. `scripts/transcribe.py` → `scripts/tighten-cuts.py` → **transcript-tight.json
   is the only timing source**
3. Inventory the footage; say so if it can't carry the cards
4. **Plan the layout track in PLAN.md and get a "go"**
5. Capture real sites, build + render the played shares
6. `make_captions.py` → `spec.py` → `build.py`
7. `check-screenshare.sh` → `render.sh --preview` → `render.sh`
8. `finish.sh` → open `out/final.mp4` → **stop**

## 10 · The ways this goes wrong

1. **The camera cuts instead of travelling.** It stops being a share.
2. **A thin beat** — typeset text pretending to be media. Go to the camera.
3. **A held layout** past ~12s, or a metronome of identical 8s beats.
4. **A rebuilt UI that invents features**, or a capture that came back blank.
5. **The accent used for mood.** Point at each coloured thing and say its job.
6. **Graphics timed to the original transcript** instead of the tight one —
   everything lands slightly early.

---

## File map

```
brand/brand.json        your answers (source of truth)   brand/brand.md  what to read first
assets/tokens.css       generated theme                  assets/ss.css   the component CSS
assets/fonts/           vendored open-licence fonts      assets/vendor/  GSAP (fetched by doctor.sh)
sfx/                    synthesised sounds + peaks.json
template/               copied into every new video: build.py devices.py spec.py
                        make_captions.py finish.sh demos/{demolib,make_demos}.py
scripts/doctor.sh       check/fix the toolchain          scripts/make-theme.py   answers -> theme
scripts/make-preview.py theme preview                    scripts/new-video.sh    start a project
scripts/transcribe.py   long-file-safe transcript        scripts/tighten-cuts.py dead air out
scripts/capture.js      real page captures               scripts/render-demos.sh / render.sh
scripts/check-*.{sh,py} gates                            scripts/concat-segments.sh mix-sfx.sh mix-bgm.sh
reference/              demo-mix (the variant) · motion-grammar · layouts · captions ·
                        look · typography · sound-design · workflow · reference-log
```

---
name: zak
description: >-
  Edit a talking-head video in the ZAK style — a rounded window floating on pure black with equal air
  above and below it, one Didone serif line set once in the air above, and tight white
  two-to-four-word captions that hard-cut inside the window with no shadow of any kind. The camera
  never moves: no drift, no push-in, no transitions, nothing eases. Warm low-key plate. Runs at 16:9
  (the studio default) or 9:16 (the aspect it was measured in). Uses HyperFrames (HTML→MP4). This is
  the fifth house style alongside `nextphase-long-editing` (coral dotted grid), `motiongraphics`
  (violet glow), `persa` (warm film grade) and `vibecode` (cobalt cut-paper). In Video Studio the
  style comes from the studio job; never ask.
---

## Video Studio (read first; overrides the rest of this file)

This skill is installed in Video Studio (`Edits/.claude/skills/`), from the NextPhase / creator packs
Bryan downloaded on 2026-10-31. Video Studio's `CLAUDE.md` wins wherever the two disagree.

- **Start from the studio job, never an intake.** Jobs come from the studio page (`jobs/<id>/job.json`).
  This skill runs when the job's `style` is `floating-window`. Never ask "short or long?" or "which style?":
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


# ZAK — editing style

A talking head goes in; an edit comes out where **the framing is the design**.
There is no grid, no stage, no collage, no accent colour and no motion. There
is a black field, one rounded window sitting in it with real air above and
below, a serif line in that air, and words that change three times a second.

**⚠ Before editing ANY video, ask the user which style:**
`zak` (this skill) · `persa` · `nextphase` (`nextphase-long-editing`) ·
`motiongraphics` · `vibecode`. Never assume, never infer it from the footage.
Record the answer at the top of `PLAN.md`.

> ### Where this look comes from
> Reverse-engineered frame by frame from one reel Jade supplied:
> **REF-A** — `instagram.com/p/Db2RzkxvWpz/` — 1080×1920, 30fps, 39.9s,
> creator `zacharyronusac`.
>
> Every number in `assets/tokens.css` marked MEASURED was read off it, and the
> tokens were verified by rendering them back through headless Chrome and
> diffing against the source frame — **the window, the title and the caption
> all land within 1px** (`reference/stills/09-reference-vs-tokens.png`).
>
> ⚠ **It is one reel.** Geometry and type are trustworthy to the pixel. The
> grade was measured in one room under one lamp and is a target range, not a
> calibrated curve. The scene vocabulary past the single locked frame is
> **invented**, and `reference/layouts.md` marks every scene measured or
> derived. `reference/reference-log.md` has the method, the raw readings, and
> a table mapping each finding to where it is written up.
>
> ⚠ **That reel is another creator's work.** Zak is the *technique*. Their
> words and their room are theirs — `scripts/check-zak.sh` fails the render if
> their copy resurfaces.

---

## ⛔ Seven hard rules

1. **Never hardcode a colour, font or duration.** Import `assets/tokens.css`;
   use its variables only. Never mix zak tokens with another style's.
2. **The caption HARD-CUTS.** Zero frames. No fade, no scale, no pop, no
   per-word reveal. 53 out of 53 measured changes landed on a single frame.
3. **The caption has NO shadow, NO stroke and NO box.** That is measured, not
   an omission — see `reference/captions.md` §2. It reads only because the
   plate under it is dark, so **when it is hard to read, fix the plate.**
   `python3 scripts/check-contrast.py` gates this on every render.
4. **Nothing moves.** No drift, no push-in, no parallax, no eased anything.
   Measured at 0px over 40 seconds. The one exception is the 6-frame full
   bleed, used once or twice in a whole video.
5. **A caption is 2–4 words.** A one-word caption is `persa`, not zak.
6. **Every word on screen is derived from THIS video.** Kit copy in
   `components/` is placeholder and the reference copy belongs to another
   creator. Run `bash scripts/check-zak.sh videos/<name>` before every render.
7. **Nothing publishes without explicit approval.** Deliver rendered + scored,
   open it for review, stop there.

**Read `reference/` before building** — `captions.md` (**the core of the style
— read this first**) · `layouts.md` (the frame, the scenes, and the 16:9
derivation) · `look.md` · `typography.md` · `motion-grammar.md` ·
`sound-design.md` · `workflow.md` · `reference-log.md`.

---

## 1 · The look in one paragraph

**A pure-black field with one rounded window in it, equal air above and below,
and a single serif line in the upper air that is set once and never changes.**
Inside the window: warm, low-key footage that never touches white, and two to
four white words in a brutally tight grotesque that replace themselves every
twenty-odd frames. Two colours — black and white. Two typefaces. One move in
the entire video. Everything else is a hard cut carried by a sound.

---

## 2 · The frame

**1920×1080 @30fps is the default** for this studio. The style was *measured*
at 1080×1920, so `:root` in `tokens.css` carries those numbers and `.zk-16x9`
overrides the five that do not transfer.

```html
<div class="zk-frame zk-16x9"> … </div>   <!-- long-form  -->
<div class="zk-frame">         … </div>   <!-- vertical   -->
```

| | 9:16 — measured | 16:9 — derived |
|---|---|---|
| Window | **968 × 968**, a square | **1720 × 732**, a 2.35:1 scope letterbox |
| Side margin | 56px (5.19%) | 100px (5.19%) — the same |
| Air above / below | **476 / 476**, equal to the pixel | **174 / 174**, equal |
| Corner radius | 70px | 70px — the same *absolute* size |
| Title line | Playfair 56px, 66px above the window | Playfair 46px, 21px above |
| Caption | Inter 700, 63px, −0.065em | Inter 700, **80px**, −0.065em |

**Read `reference/layouts.md` §5 before building wide.** The 16:9 window is a
genuine re-crop of the source, not a scale — `zak-plate.sh` takes a `crop-y`
because a talking head wants headroom thrown away, not chin. And the 16:9
caption size is **the one token in the style that was chosen by eye rather than
derived**; the reasoning, and why arithmetic gives two answers 3× apart, is
written up there and in the tokens file.

### ⭐ Three things follow from the ground being literally `#000000`
- **No drop shadow on the window.** There is nothing behind it to catch one.
- **No border, no rim, no glow.** The radius is the only edge treatment.
- **Nothing lives in the bottom air.** It is empty for all 40 seconds of the
  reference. No bar, no handle, no logo. The air *is* the design.

### ⭐ `.zk-frame` on the composition root
Type is sized in `cqh` so one scale serves both aspects, and `cqh` resolves
against a size container. Without `.zk-frame` every string renders at a
fraction of its size and the layout still looks plausible — which is why it is
the first thing to check when a scene looks subtly wrong. Never size type in
`%`: that resolves against the parent's font-size and fails the same way.

---

## 3 · The scenes

Scene 1 is measured. **Scenes 2–5 are derived** — invented so long-form has a
rotation, keeping everything that was measured intact. Full spec in
`reference/layouts.md` §3.

| # | Scene | For |
|---|---|---|
| 1 | **Locked Window** | the rest beat — and it is most of the runtime |
| 2 | **Media Window** | the window holds the real resource instead of the face |
| 3 | **Split Window** | the face and the thing, at once, one outer radius |
| 4 | **Title Card** | the chapter break — empty window, serif line carries it |
| 5 | **Full Bleed** | **the one move.** 6 frames. Once or twice per video. |

**Never the same scene twice in a row. Never hold one past ~20s.** But note
what the reference does: it holds *one* shot for 39.9 seconds. This style is
supposed to sit still, and cutting every three seconds is the amateur read of
it. Hold 6–15s at a stretch.

### ⭐ REAL MEDIA, NOT TYPESET TEXT
Every beat that supports a point shows a real resource — a screen recording,
real product UI, a docs or pricing page, a repo card. **≥1 per 20s, minimum 8.**
- **Check every screenshot actually rendered content.** Login-walled and
  JS-heavy pages come back blank and ship as empty windows.
- **No random humans as b-roll.** Cut to a person only when that person *is*
  the subject of the line.
- **Never use emojis.** There is no accent colour here to build a mark from —
  a designed mark is white type, a white rule, or nothing.
- Re-encode every sourced clip to **30fps CFR** and verify with `ffprobe`.

### ⭐ COPY IS DERIVED, NEVER INHERITED
Every string comes from the speaker's own words at their onset in
`transcript-tight.json`, the real thing named in that beat, or a verified
figure. **Write the actual copy into `PLAN.md`, per beat, before authoring.**

---

## 4 · The two things that make it zak

### The caption system
2–4 words, white, Inter 700 at **−0.065em**, hard-cutting on a single frame
every ~22 frames, in a fixed position, with **no shadow of any kind**.

```bash
python3 scripts/build-captions.py assets/transcript-tight.json \
    --out seg-01-cold-open/captions.html --offset <segment start>
python3 scripts/check-contrast.py out/seg-01.mp4
```

The builder derives its hold target from the transcript's own speech rate — the
measured 22 frames is what 2–4 words *cost* at the reference speaker's ~240
wpm, not a metronome. It reports rate, holds and words-per-caption against the
reference and warns on anything out of range.

The checker is the one that matters. The caption has no shadow, so the plate is
the only thing making it readable; a bright plate kills it **silently**, and
the render still succeeds. It is calibrated: the reference reads 125.1 against
a ceiling of 150, and a brightened copy of the same reel fails on every frame.
`reference/captions.md` §2.

### The stillness
Nothing drifts. Nothing pushes in. Nothing eases. Measured at 0px of drift and
0% of scale change across 40 seconds, with the title line static to within JPEG
noise. **This is the exact opposite of `motiongraphics`, and carrying that
skill's continuous-drift habit over is the most common way a zak comp goes
wrong.** `check-zak.sh` fails a tween on `.zk-plate` or a transform on
`.zk-window`.

---

## 5 · Motion

`reference/motion-grammar.md`. The whole table:

| Move | Frames @30fps |
|---|---|
| **Caption change** | **0 — it hard-cuts** |
| Window contents change | 0 |
| Scene change | 0 |
| Camera drift / push-in | **0 — there is none** |
| Window → full bleed | **6** — the only animation in the style |

**The cut is the transition. If a cut needs help, the help is a sound.**

⚠ GSAP `fromTo` defaults to `immediateRender:true` and will apply a later
beat's `from` state at frame 0. Always pass `immediateRender:false` — with a
single tween in the whole piece, a failure here is total.

---

## 6 · Sound

`reference/sound-design.md`. Zak has **no visual transitions at all**, so sound
is doing the job a transition does elsewhere — it is what makes a hard cut read
as intentional. **~6–10 cues/min: transitions only, quiet transients.**

**Never cue a caption change.** At 80 changes a minute it is unlistenable, and
it is the most tempting mistake in the style.

Reuse the sibling palette and **call the mixer by its path inside that skill
folder** — never copy it into a video folder:
```bash
bash ../nextphase-long-editing/scripts/mix-sfx.sh out/visual.mp4 out/sfx.mp4 sfx-cues.txt
bash ../nextphase-long-editing/scripts/mix-bgm.sh  out/sfx.mp4    out/final.mp4 assets/music/bed.mp3
```

---

## 7 · The workflow

Full detail in `reference/workflow.md`. Prefix **every** bash step with:
```bash
export PATH="$HOME/.nvm/versions/node/v24.18.0/bin:$HOME/.local/bin:$PATH"
```

0. **Ask which style.** Locate `videos/<name>/`, `VIDEO.md`, `assets/recording.mp4`.
1. **Transcribe** → chunk anything over ~90s, gap-check minute by minute.
2. **Tighten** → `transcript-tight.json` is now the only timing source.
3. **Reframe + grade** the plate (`zak-plate.sh`). **No matte step** — zak does
   not cut the subject out; reaching for `rvm-matte.py` here is persa habit.
4. **`PLAN.md`** — scenes per beat, the real on-screen copy, the media list.
   **Get a "go" before authoring.**
5. **Source real media**, verify facts, normalise to 30fps CFR.
6. **Author** per chapter. Symlink assets into each `seg-NN/`; HyperFrames
   rejects `../assets/`. Build captions with `build-captions.py`.
7. **Per segment:** `lint` (0 errors) → **`check-zak.sh` (exit 0)** →
   `snapshot` → **read the contact sheet and fix** → `render -q high -f 30` →
   **`check-contrast.py` (exit 0)**.
8. **Concat** via `../nextphase-long-editing/scripts/concat-segments.sh` —
   chapter timestamps come from real rendered durations, never from `PLAN.md`.
   Relay the source audio after the concat (AAC priming drifts ~38ms per join).
9. **Sound:** SFX pass, then the ducked bed.
10. **Deliver:** `out/final.mp4` · `out/chapters.txt` · `out/<name>.srt`.
    Report rendered + scored, open for review. **Publish nothing without approval.**

---

## Files in this skill

- `assets/tokens.css` — the measured design tokens and every zak class.
  **Import into every composition.** (CSS comments do not nest — never write a
  closing marker inside one of its header blocks, or the whole sheet silently
  stops applying.)
- `components/zak-system.html` — **the whole style on one page**: all five
  scenes at real proportions in both aspects, the type table, the cadence
  table, and a list of what breaks it. Open this first; it is the fastest way
  to see what the style *is*. Open it beside `reference/stills/`.
- `reference/` — `captions.md` · `layouts.md` · `look.md` · `typography.md` ·
  `motion-grammar.md` · `sound-design.md` · `workflow.md` · `reference-log.md`.
- `reference/stills/` — the source evidence: full frames, a 1fps contact sheet,
  3× type crops, a 4× corner crop, an 8-frame strip across a caption hard cut,
  **the tokens-vs-reference round-trip**, and the derived 16:9 form.
- `scripts/zak-plate.sh` — reframe a source into the window and grade it.
- `scripts/build-captions.py` — transcript → hard-cut 2–4 word phrase captions.
- `scripts/check-contrast.py` — **the gate that matters.** Run on every render;
  the caption has no shadow and dies silently on a bright plate.
- `scripts/check-zak.sh` — the static render gate. Run before every render.
- Everything else is **shared with `nextphase-long-editing`** — tighten,
  mix-sfx, mix-bgm, concat-segments. Call them by their path in that folder;
  never copy them into a video folder.

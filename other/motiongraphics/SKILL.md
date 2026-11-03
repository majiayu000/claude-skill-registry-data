---
name: motiongraphics
description: >-
  Edit a LONG-FORM 16:9 talking-head video in the MOTIONGRAPHICS style — a dark violet/magenta glow
  look built from lit glass tiles, self-building node diagrams, slam headlines on wiping violet bars,
  real media presented as rimmed cards on lit stages, continuous camera drift, and light-leak
  flash-through transitions. Uses HyperFrames (HTML→MP4) plus the HyperFrames catalog. This is the
  alternative to `nextphase-long-editing` (the coral dark-dotted-grid house style). Invoke when the
  user drops a recording and picks the "motiongraphics" style. In Video Studio the style comes from
  the studio job; never ask.
---

## Video Studio (read first; overrides the rest of this file)

This skill is installed in Video Studio (`Edits/.claude/skills/`), from the NextPhase / creator packs
Bryan downloaded on 2026-10-31. Video Studio's `CLAUDE.md` wins wherever the two disagree.

- **Start from the studio job, never an intake.** Jobs come from the studio page (`jobs/<id>/job.json`).
  This skill runs when the job's `style` is `glow-motion`. Never ask "short or long?" or "which style?":
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


# MOTIONGRAPHICS — long-form editing style (16:9)

A talking-head + screen recording goes in; a chaptered edit comes out where **the
motion graphics are the show**. Where `nextphase-long-editing` dresses footage with
coral cards on a dotted grid, this style builds **objects on a lit stage**: everything
glows, everything is a surface with a rim, and the camera never fully stops moving.

**⚠️ Before editing ANY video, ask the user which style:**
`motiongraphics` (this skill) or `nextphase` (`nextphase-long-editing`). Never assume.

> ### Where this look comes from
> It was reverse-engineered frame-by-frame from two reference edits. Every colour,
> size and duration in `assets/tokens.css` is **measured**, not invented:
> - **REF-A** — `youtube.com/watch?v=vwlK6MbdAto`, 0:00–3:10 — violet + coral,
>   diagram-led, no captions, long clean face beats.
> - **REF-B** — `youtube.com/watch?v=xkj74ykB9Fw`, 0:00–0:50 — magenta, glow/3D-led,
>   captions always on, faster cadence.
>
> They are the same language at two temperatures. This skill is that language.
> `reference/reference-log.md` has the shot-by-shot breakdown with timecodes — read it
> when you need to know *exactly* how a beat was done.

**⛔ Five hard rules**
1. **Never hardcode a colour, font or duration.** Import `assets/tokens.css`; use its
   variables only. The measured cadence is what makes an edit read as this style.
2. **Animate transforms only** — `opacity, x, y, scale, scaleX/Y, rotation` — plus
   `filter: blur()`. Bars, rings and rails grow with `scaleX` + `transform-origin`,
   never `width`. Animating `top/left/width/height` stutters and fails lint.
3. **Nothing has a hard edge without a halo.** A shape with no glow is not in this
   style. Every lit edge is `--mg-stroke` (2px) and carries a `--mg-glow-*`.
4. **Every word on screen is derived from THIS video.** The copy in `components/` is
   placeholder — it exists so the bricks render. Never let it survive into a segment.
   Run `bash scripts/check-placeholders.sh videos/<name>` before every render; it exits
   non-zero if kit copy is still there.
5. **Nothing publishes without explicit approval.** Deliver rendered + scored, open it
   for review, stop there.

**Read `reference/` before building** — `look.md` (the visual language) ·
`motion-grammar.md` (measured motion, read before animating anything) ·
`layouts.md` (the ten scenes and the rotation) · `motion-library.md` (**17 motion
devices** that fill those scenes) · `catalog-map.md` (which HyperFrames catalog block to
reach for) · `sound-design.md` · `workflow.md` (the build pipeline) · `reference-log.md`
(the frame-by-frame source study).

---

## 0 · The frame

**1920×1080, 30fps.** Margin `--mg-pad` 96px × 54px title-safe. Same safe zones as
`nextphase-long-editing`, so a recording can be cut either way.

| Zone | Box | Rule |
|---|---|---|
| Title-safe | inset 96 × 54 | No text or mark outside this, ever. |
| Camera bubble | `1364,738 → 1864,1020` | Reserved on screen-stage layouts. |
| Circle bubble | Ø420, free-placed | ⌁ REF-A 162s. The persona variant. |
| Point stack | `96,300 → 800,860` | Left third. The speaker keeps the right. |
| Caption band | centred `y 880–990` | Nothing else lives here. |

---

## 1 · The look in one paragraph

Near-black tinted violet (`--mg-base`), **never flat** — every scene has a light
source: a centre bloom, a bottom-edge glow, a soft S-curve ribbon, or two edge rails.
Objects are **lit surfaces**: a violet glass tile with a white rim brightest along its
bottom edge; a near-black pill with a 2px lavender stroke glowing in and out; a panel
outlined in `--mg-violet`. Type is **heavy italic caps** when it slams and a clean
grotesque when it is read. One accent per frame — violet *or* magenta — with coral
reserved for brand marks. Full detail: `reference/look.md`.

---

## 2 · The ten scenes, and the rotation

Full spec in `reference/layouts.md`.

| # | Scene | Face? | For |
|---|---|---|---|
| 1 | **Clean Face** | full | the rest beat — and it is 30–40% of the runtime |
| 2 | **Face + Floating Panels** | full | labelled semi-transparent UI drifting over footage |
| 3 | **Face + Point Stack** | full | a violet headline over white bullets, left third |
| 4 | **Face + Stat Card** | full | a glass stat card with a count-up, near the hand |
| 5 | **Face + Brand Lockup** | full | co-brand lower third, held long |
| 6 | **Diagram Takeover** | none | the system builds itself on the gear field |
| 7 | **Slam Card** | none | one headline + one hero media on the bloom |
| 8 | **Screen Stage** | bubble | real recording as a rimmed card, camera follows the cursor |
| 9 | **Object Stage** | none | glass tiles / 3D objects with real camera moves |
| 10 | **Persona Circle** | circle | circular bubble + typed quote + typed name |

### ⭐ THE ROTATION — the retention rule
**Never the same scene twice in a row. Never hold one past ~25s. Every scene change
carries a transition AND a sound.**

⌁ But note what the references actually do: **Clean Face is used generously** — REF-A
holds it for 8–12s at a stretch between graphic beats. Wall-to-wall graphics is the
amateur read. The graphics land, make their point, and **leave fast** (`--mg-dur-exit`
is 3 frames). The frame breathing between beats is what makes the next one hit.

### ⭐ REAL MEDIA, NOT TYPESET TEXT
Every beat that supports a point shows a **real resource** — a screenshot, a real
product UI, a repo card, real footage, a docs or pricing page — presented as a
`.mg-media` card on a stage, never full-bleed and never letterboxed. The Point Stack
(scene 3) is the one sanctioned text-only support beat.
- **≥1 real media per 25s of finished video, minimum 10.**
- **Check every screenshot actually rendered content** before using it. Login-walled
  and JS-heavy pages come back blank and ship as empty panels.
- **No random humans as b-roll.** Only cut to a person when that person *is* the
  subject of the line.
- **Never use emojis.** Build designed marks — a coral-asterisk doc icon, a CSS glyph,
  a small SVG pictogram in the `--mg-magenta` tile style.

### ⭐ COPY IS DERIVED, NEVER INHERITED
The bricks ship with realistic-looking text so they look like something in a browser.
**None of it describes the video being edited.** A brick is a *shape and a motion*; the
words in it are scaffolding to be thrown away.

Every string that reaches the screen comes from one of exactly four places:

| On screen | Comes from |
|---|---|
| A caption, headline or slam | **The speaker's own words**, at their onset in `transcript-tight.json`. Trim to fit; never paraphrase into something they didn't say. |
| A label on a diagram, pill, tile or list | **The thing actually being described in that beat** — the real tool, step, cost or objection named in the audio. |
| A stat, name, handle or quote | **The real, verified figure or the real person.** Sourced and fact-checked, never invented and never carried over. |
| Media inside a card | **The real screenshot or clip** from `assets/broll/`. A grey placeholder panel is an unfinished shot, not a design choice. |

**Write the actual copy into `PLAN.md`, per beat, before authoring.** A beat whose copy
is still "the brick's words" is not ready to build. This is also where a factual error
gets caught cheaply — on a plan line, not in a render.

⚠️ Some kit copy was lifted from the reference edits and belongs to **other creators**.
Those names have been neutralised in `components/`, and `check-placeholders.sh` flags
them as `BORROWED` if any copy resurfaces. Another creator's name in a monetized
client-facing video is not a cosmetic mistake.

### CAPTIONS — a per-video switch, decided in `PLAN.md`
The references disagree, deliberately: **REF-A has none**, **REF-B has them
constantly**. Both work. Pick one per video and hold it:
- **`captions: off`** (REF-A) — the graphics carry the meaning. Denser diagrams,
  longer clean-face holds. The more premium read.
- **`captions: on`** (REF-B) — the accumulating style: the phrase builds word by word,
  already-said words bold white, the newest word lighter, and **key words get a
  `--mg-magenta-hi` highlight box or violet colour on their own onset**. Position per
  the safe-zone table; centred mid-frame on takeover scenes, bottom band over the face.

Either way, **ship a separate `.srt`** for the whole video. That's the accessibility
layer and it is not the same thing as burned captions.

### SILENCE-TIGHTENING — do this FIRST
Reuse `../nextphase-long-editing/scripts/tighten-cuts.py`. After it runs,
`assets/transcript-tight.json` is **the only timing source**. Timing against the
original transcript is the single most common way this edit goes wrong — it shows up
as "the graphics are all slightly early", never as an error.

---

## 3 · Motion — the measured cadence

Read `reference/motion-grammar.md` before animating anything. The five that define the
style:

| Move | Timing | What it is |
|---|---|---|
| **Word build** | ⌁ word fades 0→1 in `--mg-dur-word` (8f), onsets `--mg-dur-cadence` (7f) apart | A title assembles one word at a time **while the whole line continuously re-centres**. The re-centring is the tell. |
| **Bar wipe** | ⌁ `--mg-dur-wipe` (12f), `scaleX 0→1` from left | The violet highlight bar opens behind a slam word, **leading edge brightest**. |
| **Light leak** | ⌁ `--mg-dur-leak` (12f): bloom 5f → white-out 3f → reveal 4f | The signature transition. A violet-white streak washes the frame and the next scene is already in place behind it. |
| **Ring draw** | ⌁ `--mg-dur-ring` (18f), starting ~0.5s *after* the lockup settles | The conic progress ring sweeps clockwise. Late arrival is deliberate. |
| **Camera pull-back** | ⌁ continuous, `ease:"none"`, across the whole scene | The title lands large and everything shrinks as content arrives beneath it. One unbroken zoom-out — **not** discrete re-fit steps. |

**Three standing rules:**
- **Nothing on screen is ever perfectly still.** A held scene carries a continuous slow
  drift — scale `1.00→1.04` over its whole life, `--mg-ease-drift` (linear). This is the
  difference between "a motion graphic" and "a slide".
- **Enter slow, leave fast.** Entrances are `--mg-ease-out` over ~0.3–0.6s. Exits are
  `--mg-dur-exit` — 3 frames. Elements are *gone*, not dissolved.
- **Overlap the handoff by `--mg-overlap` (2f).** ⌁ In REF-B the incoming headline is
  already on screen while the outgoing tiles are still sliding off. Never leave a gap.

**Timing anchors:** every graphic enters **on, or a hair after, the tight-transcript
word onset** it illustrates — never before. Round-number timings are banned. Exit at
the OUT word + 0.3s; cap a support graphic at 10s, then evolve it rather than let it sit.

---

## 4 · Building — HyperFrames + the catalog

All the HyperFrames skills are installed, and the **372-item catalog** is available.
`reference/catalog-map.md` maps every pattern in this style to the catalog blocks that
already implement it — reach there first, restyle with `tokens.css`, and only hand-build
what the catalog misses.

```bash
export PATH="$HOME/.nvm/versions/node/v24.18.0/bin:$HOME/.local/bin:$PATH"   # every step
npx --yes hyperframes catalog --search "<pattern>"      # find it
npx --yes hyperframes add <name>                        # install into the segment
```

**`components/mg-system.html` is the whole style on one page** — all ten scenes, the light
leak, all seventeen devices, the palette, the materials and the cadence table, every one of
them live. Open that first; it is the fastest way to see what the style *is*. The two kits
below are the same material split by purpose:

- **`components/mg-blocks.html`** — the ten **scene layouts** (`layouts.md`).
- **`components/mg-motion-library.html`** — **17 motion devices** (`motion-library.md`):
  cursor cards, tag clouds, blur swaps, wave charts, ladder climbs, alert flashes, orb
  count-ups, skeleton fills, chip marquees, orbit hubs, notification pile-ups, 3D
  numbered grids and more. Scenes are *where* a beat is staged; devices are *what moves
  in it*. **One device per beat** — two is a collision, not a composition.

Bricks are starting points, not a cage.

---

## 5 · Sound

`reference/sound-design.md`. Reuse the palette and mixer from the sibling skill —
**call the script by its path inside that skill folder**, never copy it:
```bash
bash ../nextphase-long-editing/scripts/mix-sfx.sh out/visual.mp4 out/sfx.mp4 sfx-cues.txt
bash ../nextphase-long-editing/scripts/mix-bgm.sh  out/sfx.mp4    out/final.mp4 assets/music/bed.mp3
```
- **Density ~12–20 cues per minute.** Every layout change carries a sound. No silent cuts.
- **The light-leak always gets a sound** — `swoosh` on the bloom with a `riser` tail
  cresting on the white-out. It is the loudest transition in the style; treat it as one.
- SFX sit ~13–15 dB under voice peaks; the music bed ~22–26 dB under. Calibrate with
  `ffmpeg -af volumedetect`, don't guess.

---

## 6 · The workflow

Full detail in `reference/workflow.md`. The skeleton:

0. **Ask which style.** Then locate `videos/<name>/`, `VIDEO.md`, `assets/recording.mp4`.
1. **Transcribe** → gap-check minute by minute (Parakeet silently drops audio).
2. **Tighten** → `transcript-tight.json` is now the only timing source.
3. **`PLAN.md`** — chapters with word onsets, the scene assigned to each beat, the
   caption switch, the re-hook marks, the media shopping list. **Get a "go" before authoring.**
4. **Source real media** (≥1/25s, min 10). Verify facts. Normalise every sourced clip
   to **30fps CFR** and check with `ffprobe` — sourced clips come back at 24/25/50/60 or VFR.
5. **Author per-chapter compositions** — `seg-01-…/`, one per chapter. Symlink assets
   into each segment folder; HyperFrames rejects `../assets/`.
6. **Per segment:** `lint` (0 errors) → **`check-placeholders.sh` (must exit 0)** →
   `snapshot --at <times>` → **read the contact sheet and fix** → `render -q high -f 30`.
7. **Concat + chapters** via `../nextphase-long-editing/scripts/concat-segments.sh` —
   chapter timestamps come from real rendered durations, never from `PLAN.md`.
8. **Sound:** SFX pass, then the ducked bed.
9. **Deliver:** `out/final.mp4` · `out/chapters.txt` · `out/<name>.srt`. Report
   rendered + scored, open it for review. **Publish nothing without approval.**

---

## Files in this skill

- `assets/tokens.css` — the measured design tokens. **Import into every composition.**
  (CSS comments do not nest — never write a `*/` inside one of its header blocks, or the
  whole sheet silently stops applying and every scene renders unstyled.)
- `components/mg-system.html` — **everything, one page.** Start here.
- `components/mg-blocks.html` — the brick kit: all ten scenes on a real 1920×1080 stage,
  animated at the measured durations. Open it in a browser. Append `?still` (or hit
  **freeze**) to hold every scene at its settled state for comparison.
- `reference/look.md` · `motion-grammar.md` · `layouts.md` · `motion-library.md` ·
  `catalog-map.md` · `sound-design.md` · `workflow.md` · `reference-log.md`.
- `reference/stills/` — the source evidence: four frame-by-frame transition strips at
  30fps plus nine key stills, including 3× zooms on a node pill and a glass tile.
  **Open the matching still beside `mg-blocks.html?still` when tuning a scene.**
- `scripts/check-placeholders.sh` — **the render gate.** Fails if kit copy or a borrowed
  name survives into a segment. Run it before every render.
- Other scripts are **shared with `nextphase-long-editing`** — tighten, mix-sfx, mix-bgm,
  concat-segments, the RVM background remover. Call them by their path in that folder.

---
name: graphics-plan
description: >
  Step 3 of the content pipeline. Use once a job has a flattened rough
  cut (outputs/.roughcut.mp4) and needs on-screen graphics — plans the
  video beat by beat BEFORE building anything, then builds the
  HyperFrames composition as short seamless parts on one shared
  timeline. Covers both 9:16 short-form and 16:9 long-form. Delegates
  actual HyperFrames HTML authoring to the vendor hyperframes-core /
  hyperframes-creative / hyperframes-animation / hyperframes-registry
  skills already installed in .claude/skills/ — this skill enforces the
  pipeline-specific discipline around them (plan-first, safe zones,
  part-based rendering, version pinning).
---

# Graphics plan

Plan the whole video beat by beat first. Do not open an HTML file before
the beat sheet exists — that's how you end up rebuilding a whole
timeline because a foundational scene decision changed halfway through.

Prerequisite: `projects/<job>/outputs/.roughcut.mp4` and
`outputs/.transcript.json` must exist (from `/rough-cut`'s full-render
path). If they don't, stop and go run
`.claude/skills/rough-cut/scripts/assemble_rough_cut.sh <job>` first.

## 1. Resume or start `hf-graphics/PROJECT.md`

This file was created empty by `/intake`. Read it now — if beats are
already filled in from a prior session, resume from there instead of
re-planning. If this is the first pass, fill in the Format section (9:16
or 16:9) and delete the row you're not using.

## 2. Beat sheet, before any HTML

Read `outputs/.transcript.json` (the canonical transcript — never
`transcript/words.json`, never re-transcribe) and walk it beat by beat:
what's being said, what should appear on screen, and when it should
fire. Fill in `hf-graphics/PROJECT.md`'s beat sheet table completely
before writing any composition file. Each row becomes one "part."

For short-form (9:16, 1080x1920): every beat's on-screen content must
respect the safe zone — **no key visuals in the top 200px or bottom
300px; face, captions, and graphics stay inside y 200–1620.**

## 3. Scaffold the shared timeline

```bash
.claude/skills/graphics-plan/scripts/scaffold-graphics.sh <job-name> <9x16|16x9>
```

Creates `hf-graphics/index.html` (a **thin** orchestrator — slots,
timing, audio only, per `hyperframes-core/references/composition-patterns.md`),
a `compositions/` directory for one sub-composition file per beat, and
two render scripts with the HyperFrames version **pinned literally**
inside them (read from the repo's `skills-lock.json` at scaffold time).
That pin does not move on its own — see § 5.

## 4. Build one part per beat

Check `presets/<format>.md`'s **Approved motion components** table
first — for short-form, `presets/components/lower-third-card.html`
(stat/quote callouts) and `presets/components/cinematic-rise.html`
(sparing hook emphasis) are already reviewed and approved; copy and
fill in their `__PLACEHOLDER__` tokens rather than inventing a new
treatment for the same job. Running dialogue captions use
embedded-captions' default anchor rail, not a component here.

For each beat sheet row, write `compositions/part-NN.html` as a real
HyperFrames sub-composition — read `/hyperframes-core` for the
composition contract (`data-start`, `data-composition-id`,
`data-width`, `data-height` on the root are mandatory since 0.7.42, or
the render capture dies), `/hyperframes-creative` for design/typography/
palette decisions, `/hyperframes-animation` for motion, and
`/hyperframes-registry` for any named look/effect (search there before
hand-building anything that sounds like a common treatment). Wire each
part into `index.html`'s root as a `data-composition-src` slot at its
beat's `data-start`/`data-duration`.

After each part, render just that part to check it:

```bash
hf-graphics/render-part.sh compositions/part-03.html
```

This is the whole reason for the shared-timeline-plus-parts structure:
**a tweak re-renders one part, not the whole video.**

## 5. Moving the HyperFrames version pin

Never hand-edit a skill file, and never let a render float to latest —
`npx` without a pinned version has broken the composition contract mid-
job before (0.7.42 added the mandatory root attributes above; 0.7.67
shipped a change reverted in 0.7.68). If a job's render scripts need a
newer pin:

1. `scripts/update-hyperframes-skills.sh <new-version>` at the repo
   root — reviews the SKILL.md diff and asks before touching anything.
2. Re-render **one** part of **this** job with the new version and
   review it before editing that job's `render-part.sh` / `render-
   final.sh` pin.
3. Only then move the pin in this job's scripts, and only this job's —
   other in-flight jobs keep their own reviewed pin until you repeat
   this for them too.

## 6. Final render

Once every part is reviewed individually:

```bash
hf-graphics/render-final.sh
```

Writes `outputs/<job>-graphics.mp4` at full quality. Continue to
`/second-pass` for review, or straight to `/captions` (short-form) /
`/music` / `/export` if no changes are called.

**Audio passthrough check:** the timeline's audio track is the already-
polished dialogue from `assemble_rough_cut.sh` (+10dB gain -> -6dBFS
limiter -> AAC 256k). HyperFrames' own render must not silently
re-encode it below 256k — check the rendered file's audio bitrate
(`ffprobe -show_entries stream=bit_rate <file>`) and if it dropped below
256k, fix the render's audio output settings before shipping.

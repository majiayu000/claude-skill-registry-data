---
name: vawe-page
description: "Write an HTML page that renders to an mp4 video, programmatic video and motion graphics as code with CSS, SVG, canvas or three.js. Author a vawe page film: one films/<name>/page.html the renderer seeks frame by frame. Load before writing or editing any page.html: audio tags, the spring helpers, and the page-code mistakes a first draft makes. The page contract itself is in AGENTS.md."
effort: medium
license: Apache-2.0
---

# vawe-page: write the page

Run this skill inside a vawe checkout: `AGENTS.md`, `taste/` and `bin/vawe` live there. With no checkout, get one: `git clone https://github.com/vawe-hq/vawe.git && cd vawe && npm install && bin/vawe-dev doctor`.

A film is one HTML page; the renderer seeks it, screenshots every frame and mixes the audio offline.
The contract (duration meta, seek, aspect, literals) is in `AGENTS.md`. Start with
`bin/vawe new <name>`; this skill holds the code a first draft gets wrong. Taste pitfalls are in
`taste/build/DIGEST.md`. When the length comes out of the work, write `<meta name="duration" content="auto">` (the last move plus a hold), then `bin/vawe dev <page> --lock-length` fixes the number; a page driven by `window.seek` alone needs a number.

This file is `skills/vawe-page/SKILL.md` in the repo. Use `bin/vawe` verbs, never raw ffmpeg or Chrome (`bin/vawe --help`).
Order: (1) the brief, facts only. (2) Study the references (`bin/vawe refs frames`, Read `~/.vawe/refs/frames/<id>/*.png`
at full size), then fill brief.md "Taken from": 4 to 6 named frame paths and what each gives. Then study how they move:
`bin/vawe frame <ref-id> --cuts` on 2 refs, Read the strips, name 3 moves with the ref id and cut second. (3) Write
`films/<name>/DESIGN.md` and `films/<name>/kit/`: ground layers, and each moving part (word, mark, bar, card, icon,
wordmark) as its own element. Start from a PROVEN combo in `prompts/skill-combos.md` (record `Combo: <name>`; swap at most one rung, with a reason). The skill ladder, one skill per rung in order (`command npx -y ui-skills get <slug>`):
builder (`leonxlnx/soft-skill` or `emilkowalski/emil-design-eng`: the product UI and kit parts as a real, beautiful interface),
type (`jakubkrehel/better-typography` or `pbakaus/typeset`), colour (`pbakaus/colorize` or `jakubkrehel/better-colors`),
depth (`mengto/beautiful-shadows` or `mengto/progressive-blur`), then frame: compose the video frame with vawe's own rules
(about 1 line and 2 or 3 things, ground never flat, an eye path). The frame rejects web-page patterns (nav, CTA button, pill,
eyebrow, section padding), never by skipping the builder rung. Write one DESIGN.md line per rung: `Skill <rung>: <slug>: what it
decided`, or `Skipped <rung>: <reason>`, a reason that cites a reference frame path or a SPEC.md line (`bin/vawe` advises on a missing rung). Product UI inside the film is a designed
interface with real-looking data, never placeholder bars. For an invented product the UI is invented but designed.
An owner decision that differs from a house default goes under `## Declared` in DESIGN.md, one `- key: value` line each: `font`, `type-scale` (percent cap height of read text), `ui-scale` (percent for UI that is the subject, put in a `data-ui` element), `camera` (`still` or `free`). The acceptance rows and the judge follow the line and print it (`harness/lib/design-decls.mjs`).
DESIGN.md also names colour roles (ground, text, muted, one scarce accent, positive, negative), type roles (mono for every numeral; the measured brand weights) and a negative list (no nav or footer chrome, no second accent, no `back`, `bounce` or `elastic` easing unless the brand is a toy brand).
Kit format: `kit/kit.css` holds `:root` tokens (palette roles, light positions) and one rule per part (`.ground-*`,
light devices, `.grain`, `.lockup`, `.word`, `.line`), each moving part its own element; `kit/kit.html` is an optional
sheet that shows every part once. Example: `films/examples/colour-sting/DESIGN.md` and `kit/`. (4) Build each `data-world` as a static state from the kit (`bin/vawe frame <page> --world all`): about 1 line and 2 or 3 things, and a
ground that is never flat (a light, grain or depth device named from a reference frame, changed at each world turn).
(5) Fill the brief's "Ideas" first (`guides/IDEATE.md`: 4 ideas from 4 devices per beat and cut, a typicality number, a pick that is not the most typical), then the Board: a plan for time, not frames. Rhythm (cuts not all equal: one under 0.4 s, one over 0.9 s),
the spectacle second (also `<meta name="spectacle">`; recipe 15 in `prompts/moves/RECIPES.md`), a named move per cut
(overlap, camera, what carries the eye, which arrivals overshoot: `EASE.nudge` for ordinary ones, `EASE.pop` for the hero),
a handoff per cut (`vawe-transitions`), and sound: small effects on actions, no bed (`taste/craft/sound.md`; `bin/vawe sound`).
`bin/vawe frame <page> --board` lists what the taste docs say about the plan (doc line, measured value, fix). (6) Then the Shots rows, the
motion and `bin/vawe dev`. The camera holds still by default and moves only with a reason (the spectacle, a reveal): a hold stays alive through an element motion (typing, a counter, a glint), not a camera drift. The motion is done when overshoot-share, live-hold, constant-camera and seam-variety are clean or waived with a
reason, and you have Read `bin/vawe frame <page> --cuts` for every cut (and `bin/vawe frame <page> --moment <s> --onion`/`--velocity` on the
spectacle second), checked each cut against `taste/craft/motion-craft.md` and the principles in `core/motion/README.md` (anticipation on the hero, follow-through and overlap, eased spacing, arcs, secondary action, exits faster than entrances), fixed what reads flat and written a row per cut in the brief's "Motion pass". `bin/vawe` names the next
stage after each step; `bin/vawe ship` warns while the Board or the Motion pass is unfilled.
A film that uses the lens (`core/surfaces/lens.js`, `prompts/moves/lens.md`) picks its look by sight: `bin/vawe frame <page> --looks --at <s>` shows the page under every look, then set `look: '<name>'` in the lens options.

```html
<meta name="message" content="zero fees">    <!-- the one thing to remember -->
<meta name="spectacle" content="6.2">        <!-- the second of the one big moment; quiet before it -->
<audio src="assets/click.wav" data-at="0.4"></audio>   <!-- a recorded effect; a loop src only if the user gives a track -->
<audio data-synth="pluck" data-at="0.85"></audio>   <!-- a quiet tick on one key word, default gain -->
<audio data-synth="swell" data-at="1.66"></audio>   <!-- the one soft swell, ends on the cut -->
<audio src="assets/vo.wav" data-role="vo" data-at="1.0"></audio>
```

`data-trim` and `data-trim-end` cut a clip to the part you want, so there is no need for ffmpeg. `bin/vawe sound <track> --cuts <page>` gives the beat grid, the hits and each cut's frame offset for a track the user gave.

## Sound is felt, not noticed

A recorded effect first, otherwise no cue; a synth tick or one swell only when you choose it, never a bed (`taste/craft/sound.md`). `data-gain` is absolute dB and replaces the voice default (`DEFAULT_GAIN_DB` in `core/audio/kit.mjs`; a `src` file defaults to 0 dB): write it only to move one cue on purpose. Cue the first and the last key word, not every word. Name each beat once in CSS (`--beat-2: 1.85s`) and read it from every delay in that beat, so one edit moves the beat. What you write is what you hear: no normalising, and `<meta name="loudness" content="-14">` opts in to a delivery target. The mix warns when one cue peaks more than 6 dB above the median, and `bin/vawe check review <page> --final` warns outside -30 to -12 LUFS.

## Moves to copy

`prompts/moves/README.md`: the proven moves, grouped by job (reveal a title, change between shots,
point the eye, product moments), each a CSS and WAAPI snippet with a 1 s clip. Copy one; do not
approximate it by eye.

## Springs and tables

Start every entrance, exit and group from `core/motion/presets.js` (`enter`, `leave`, `stagger`,
`layer`, `BANDS`): they land on real curves, exit shorter than the entrance (rule exits-shorter) and stagger 30 to 80 ms,
and the `bin/vawe dev` motion lint names each move that breaks those rules.

```js
import { spring, track, approach, kf, springLinear, springDuration, SPRINGS, rng } from '../../core/motion/springs.js';
el.animate([...], { duration: springDuration(k, d) * 1000, easing: springLinear(k, d), fill: 'both' });
const x = track(t, [[0, 100], [1.2, 640]], 170, 26);   // a spring per target change
const zoom = approach(t * 30, 1, 1.35, 0.15);          // 15 percent of the gap per frame
const rot = kf(t * 30, [[0, 0], [24, 90], [60, 90]], 'easeInOutCubic');
```

Never approximate a curve with `cubic-bezier()`: a hand-fitted bezier starts too hard and stops too
early, and the motion reads jerky. Use the After Effects eases in `EASE` (`core/motion/presets.js`):
`land` to arrive, `landSoft` for a move under 0.4 s, `launch` or `leave` to exit, `glide` for a drift,
`settle`, `swap`, `carry`, `pop`. The ease and the time for each job (a title, a panel, an exit, a
camera move) are in the table in `taste/craft/motion-craft.md`. Each is an exact CSS `linear()` easing,
and plain CSS reads it as `var(--ease-land)`, `var(--ease-launch)` (the renderer sets them on `:root`);
in `window.seek` or `vawe.onFrame` code use `easeFn(name)`, a function of 0..1. Multi-key motion: `keys()`.
Under `vawe.layoutSeek` (the measure and layout probes) skip only canvas painting in `window.seek` and `vawe.onFrame`; still set every element's position, size and text, since the probes read the DOM.

```js
import { EASE } from '../../core/motion/presets.js';
el.animate([{ translate: '0 40px' }, { translate: '0 0' }], { duration: 700, easing: EASE.land, fill: 'both', delay: 1200 });
document.documentElement.style.setProperty('--ease-land', EASE.land); // CSS: animation-timing-function: var(--ease-land)
```

`SPRINGS.snappy` for leading edges, `heavy` for big type and logos, `playful` only when the brief
asks for overshoot. Full reference: `core/motion/README.md`.

## Before the first draft

1. Pick the film type in `guides/ROUTING.md`; `bin/vawe new <name> --from prompts/<t>.md`.
2. Write the beat table (`prompts/beat-sheet.md`): time, message, the one thing that moves, the cue.
3. Make the five stills that define the look. Fix cramped, overlapping or unreadable before motion.
4. Check frames with `bin/vawe frame <page> --vs <ref.mp4> --at s,s,s` (about 4 s for 4 frames).
   Never render a whole range to look at a few frames. `bin/vawe dev <page> --from s --to s` is for motion.
   A recreation is done when `bin/vawe check coverage <film.mp4> --ref <ref.mp4>` exits 0.
5. Hand the draft to a fresh session: `vawe-critique`.

## Contract details

- `<meta name="fps">` is optional: your frame-table rate. The render rate is separate (60 final, 30 draft) and frames are fractional.
- `--vw`/`--vh` (px lengths), `<html data-aspect>` and `window.vawe` are set before your scripts run.
- Text checks skip `aria-hidden="true"` and `data-chrome` text only when it is texture by measure: cap height under 2% of the frame, the same words 3 or more times, or `data-texture="why"` (12 characters or more). Any other hidden text is checked as copy. A `data-chrome` texture keeps the 2.5% cap floor and no read hold (`taste/rules/readable-text-size.md`).

## Waivers

A rule broken for cause is declared in the page with its reason, nowhere else. Checks advise; only determinism, banned items
and a reason that does not count refuse. One code per check, scoped to the seconds: `static-window@a-b`, `tile-run@a-b`,
`tail-tiles@a-b`, `world-held@a-b` (the old `dead-air` waives nothing). A reason names where (a world id of the page or a second)
and what was measured (a number with its unit). "intentional", "by design", "deliberate", "stylistic", "fine", "ok" and "as intended"
do not count, and nor does one reason copied to 3 or more waivers. The draft lists every refused waiver; the judge sees every waiver.
`<script type="application/json" id="authoring">{"allow": ["world-held@3.5-6.2"], "_why": {"world-held@3.5-6.2": "world s4, 2.7 s: the wordmark is the last beat and a caret ticks on it"}}</script>`

## Page-code mistakes a first draft makes

1. A live clock. `Date.now()` or a running `requestAnimationFrame` loop instead of t. The frame is a
   function of the seek; anything else renders differently on every run.
2. State carried between frames (`x += dx`). Frame 400 must not need frame 399.
3. `Math.random()` for a still element, so it boils. Use `rng(seed)` and seed per element.
4. A network font. Bundle the face in `films/<name>/assets/` and `@font-face` it; the renderer
   waits for `document.fonts.ready`, not for the network.
5. `var()` inside the `animation` shorthand: Chromium drops the whole declaration silently. Write
   the longhands. `bin/vawe check anim-traps <page>` finds this and six more.
6. No end keyframe. A `@keyframes` rule with no `100%` slides back after it ends.
7. Opacity or filter on a `preserve-3d` element flattens it. Fade the wrapper.
8. A layout in fixed pixels for 16:9. Use `--vw`/`--vh`, container units and `[data-aspect]`
   selectors, then draft `--aspect 9:16` once before the final.
9. `fill: both` (or `backwards`) on an animation with a delay shows its first keyframe from frame 0;
   use `forwards` unless it should sit there before it starts.
10. `--vw` and `--vh` hold a unit (`1920px`): write `calc(var(--vh) * 0.11)`, never `* 0.11px`. A capture
    scaled below 0.6 loses its type: crop instead.
11. A module-level `await` of something else than an image decode, a `fetch` or `document.fonts.ready`
    (a promise you made, a dynamic `import()`): the renderer waits only for those three, so frame 0 is
    painted before your `vawe.onFrame` exists. Await the three, or register the hook first and await inside it.

## Commands

`bin/vawe dev <page> [--aspect --from --to --silent]`: half size, 30 fps, with sound (a window is silent).
`bin/vawe ship <page> [--aspect all]` needs a fresh review (`bin/vawe critique <page> --fresh`, or `bin/vawe critique <page>` in a separate terminal) and the person's OK on the plan and the draft: show the draft (`bin/vawe frame <draft>`) in plain words (map: harness/lib/plain-words.mjs) and end with "If you like it, type /vawe-approve". It runs in the background; wait with `bin/vawe wait <page>`
(one call returns within 3.5 minutes with a progress line each minute; if it says STILL RUNNING, call it again); before it do the work it names (fill the Board and
Motion pass rows, Read the `bin/vawe frame <page> --cuts` grids, prepare the critique notes). Fix the verdict worst first on drafts (`bin/vawe dev`, then
`bin/vawe critique <page> --fresh`) until PASS, then ship once more. Fix what the final check and the acceptance rows name;
read the judge once and never tune to it (its score is not a target). Poll once per call and work on the last draft between polls.
`bin/vawe critique <page> [--ref mp4]`: the fresh look (`vawe-critique`; with `--ref`, `vawe-reference`).
Templates: `guides/ROUTING.md`. Long films: `prompts/directors-brief-long-form.md`.

---
name: motion-review
description: Use when reviewing a film's source or a diff to its index.html or timeline.js, before a render, or when asked whether a film follows the motion rules.
---

Review a film's source, or a diff to it, for rule breaks. One line per finding: location, what, the fix. The best outcome is a film that renders the same every time and shows only real things.

## Run first
`python3 ENGINE/lint.py <slug>` (ENGINE is `../../engine/`). It finds the mechanical breaks and prints them in the format below. Keep every line it prints; then read index.html, timeline.js, shotlist.md and CLAUDE.md yourself for what a regex can't see.

## Format
`<file>:L<line>: <tag> <what>. <fix>.` Blocking tags first, then polish, then verify.

Blocking (the film is wrong or will render differently next time):
- `clock:` not a pure function of time: CSS animation/transition, timers, rAF, wall clocks, Math.random, a variable carried between draw() calls.
- `fade:` opacity on a curve, crossfade, blur-in. Name the shape change that replaces it (rise, pop, flood, morph).
- `look:` a banned default: gradient, glow, 3D, particles, centered title on a gradient, corner labels, frame borders.
- `redraw:` product UI built from divs, SVG or canvas instead of a crop from shots/. Lint can only flag it to verify; once you confirm it, it blocks. Name the crop to use or the page state to shoot.
- `invent:` a number, price or date on screen with no facts.md row; a `fact` row with no source or date; an `example` shown without its "Example" label; a name, quote or logo with no source.
- `cue:` a missing or misspelled cue, a sound after the end, a picture cue in seconds.
- `asset:` a missing image, voice line or kit sound; a sound not in kit/AUDIO.md; a shots/ image with no provenance.json entry (captured films).
- `voice:` TTS not written into CLAUDE.md, or a caption that shows the pronounce.json spelling.

Polish (it renders, but it breaks the craft rules):
- `blur:` will-change or transform-scaled crops on anything the camera zooms.
- `crop:` a hard-coded 1920x1080 layout that won't reframe to 1:1 or 9:16.
- `beat:` a literal beat instead of a named cue.
- `sync:` a click without `"peakFirst": true`, an effect with no event on screen, two effects under 200 ms apart.
- `hold:` a gap between cues longer than 1.5 beats with nothing moving (from timeline.js or shotlist.md).
- `hide:` `visibility: visible` on a child: it shows through a hidden parent. Use `inherit`.
- `swap:` text inside a morphing shape that doesn't enter after the morph starts and leave before the next.

## Examples
Bad: "The animation timing might feel a little off in places; consider revisiting the easing."

Good: `index.html:L212: fade label opacity follows sp(). Rise it out of the pill's edge: translateY from swapIn().`

Good: `index.html:L88: redraw pricing table built from 14 divs. Crop shots/pricing.png, box in crops.js.`

Good: `index.html:L310: invent '₹10 lakh' on screen has no facts.md row. Add | ₹10 lakh | <source> | <date> | fact | or cut it.`

Good: `timeline.js:L0: sync click at beat 7 syncs to its loudest hit. add "peakFirst": true.`

Good: `index.html:L44: beat camera key at literal beat 15. Name it s01.home in cues.`

## Score
End with `score: <B> blocking, <P> polish, <V> to verify.` Nothing found: `Clean. Render it.`

## Boundaries
Scope: the motion rules and the film's source. Taste, pacing and how the render looks belong to motion-check. Performance is out of scope. Lists findings, applies nothing: fixing belongs to whoever built the film. One-shot.

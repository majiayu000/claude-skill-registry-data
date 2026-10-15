---
name: motion-craft
description: "Use when deciding how a film beat looks and moves — motion density (a gesture in progress at every moment: 0.75 s gesture-free max, CTA still ≤ 1.2 s, beats every 0.5-1 s, ≥ 1 onset/s) with read time ≥ 0.25 s/word, one primary gesture with subordinate details, the two film types (cut-based edit, one continuous object), scene transitions without opacity blends, easing and springs (ζ ≥ 0.85, ≤ 3 % overshoot, springSum, dual-edge), ink/paper/one-accent color with area-weighted contrast and type as a large object, and the single-source ban list (every decorative effect banned); also the rubric source motion-critic scores against."
versions:
  fuse-motion: "1.0.0"
user-invocable: false
references: references/focus-hierarchy.md, references/timing-holds.md, references/continuous-take.md, references/easing-springs.md, references/color-type-video.md, references/anti-slop-video.md
related-skills: motion-method, motion-art-direction, motion-review, motion-render, fuse-design:design-motion
---

<objective>
The craft rules for film motion — what moves, for how long, on which curve, in which color, at what type size — and the bans that separate a directed film from generic "AI motion". `motion-expert` applies them while building each beat; `motion-critic` scores against the same rules through `motion-review`, so a rule stated here is a rule the draft is judged on.

It does not own UI motion tokens: easing curves and the glossary live in `fuse-design:design-motion` and are pointed to, never copied. UI micro-durations from that skill (100-500 ms) do not apply to film read time. And readable never means frozen: a purposeful gesture is in progress at every moment — no span over 0.75 s without one, the final CTA still ≤ 1.2 s — and nothing "drifts" to fake life; a long read becomes more beats.
</objective>

# Motion Craft

## Agent Workflow (MANDATORY)

| Step | Who | What |
|------|-----|------|
| Before choosing curves | read `fuse-design:design-motion` → [motion-tokens.md](../../../design-expert/skills/design-motion/references/motion-tokens.md) | Reuse the named easing tokens |
| Naming an effect | [animation-glossary.md](../../../design-expert/skills/design-motion/references/animation-glossary.md) | Exact term in beats and handoff |
| Building a scene | `motion-art-direction` templates first: [composition-grid](../motion-art-direction/references/templates/composition-grid.md), [kinetic-type](../motion-art-direction/references/templates/kinetic-type.md), [cut-rhythm](../motion-art-direction/references/templates/cut-rhythm.md) | Grid, entrances and cut times that already enforce these rules |
| Draft review | `motion-critic` via `motion-review` | Scores these rules with frame refs |
| Scripts | `fuse-ai-pilot:sniper` | Code validation after scene/render edits |

---

## Overview

| Area | Core rule | Reference |
|------|-----------|-----------|
| **Focus** | One primary gesture at a time, smaller details (rules, underlines, counters) may move with it; frame 0 at full value; behaviours rotate, never opacity-only | [focus-hierarchy.md](references/focus-hierarchy.md) |
| **Timing & density** | Gesture in progress at every moment: ≤ 0.75 s gesture-free, CTA still ≤ 1.2 s, beats every 0.5-1 s, ≥ 1 onset/s; ≥ 0.25 s per word on screen; long copy → more beats; no drift | [timing-holds.md](references/timing-holds.md) |
| **Continuous take** | Cut-based edit or one continuous object (morph, cursor, content swap); no opacity blend; one curve; loops with matched velocity | [continuous-take.md](references/continuous-take.md) |
| **Easing** | No linear motion; springs ζ ≥ 0.85, overshoot ≤ 3 %, one swing at most; springSum; dual-edge squash/stretch | [easing-springs.md](references/easing-springs.md) |
| **Color & type** | Ink / paper / one accent (OKLCH); area-weighted contrast ≥60 L; a ≥50 % dark/accent plane on 1 beat in 3; no neutral mid-tones; TYPE_SCALE ≥4; never centered | [color-type-video.md](references/color-type-video.md) |
| **Anti-slop** | Single-source ban list, each absolute ban mapped to a hard-fail ID; no `look.md` exception | [anti-slop-video.md](references/anti-slop-video.md) |

---

## Critical Rules

1. **One primary gesture at a time** — smaller, subordinate details (a rule, an underline, a counter, a motion path) may move with it; two big moves at once = no focus.
2. **Frame 0 is the statement** — the opening line is on screen at full value at t = 0; no blank, logo or fading-in first frame.
3. **Continuous purposeful motion, readable, never drifting** — a gesture in progress at every moment: no span > 0.75 s without one, the final CTA still ≤ 1.2 s, beats every 0.5-1 s on the grid, ≥ 1 onset/s; every word ≥ 0.25 s on screen, long copy split into more beats. No slow push, no ambient loop.
4. **No opacity blends** — no crossfade, no dissolve, no opacity-only reveal. Transitions are a shape morph, a hard-edged mask wipe, push/swap, or a hard cut on the grid; one fixed curve for every morph and the camera (field example: 0.8 s `cubic-bezier(.45,0,.15,1)`).
5. **Kinetic type and objects, rotated** — letter/word stagger, slam, scale jump 3-4× → set size, split along a plane; one recurring geometric actor; objects that assemble and transform; never the same behaviour on two consecutive beats.
6. **No linear motion** — except constant-rate indicators (progress fill, cursor travel at typing speed).
7. **Springs: ζ ≥ 0.85, overshoot ≤ 3 %, one swing at most** — presets 320/31 (UI, ζ 0.87), 170/23 (containers, 0.88), 120/19 (heavy type, 0.87); snappy expo-out arrivals.
8. **Ink / paper / one accent, no neutral mid-tones** — no fill at OKLCH L 30-85 with C < 0.03; the two largest planes differ by ≥60 L; at least one beat in three is ≥50 % dark or accent field; body text ≥7:1.
9. **Type as a large object, never centered** — TYPE_SCALE ≥4 on hero frames, flush-left or edge-anchored, at least one crop/bleed; px at the 1080-wide output; judge legibility at 360-390 px.
10. **Every decorative effect is banned** — gradient backgrounds, decorative blur, glow, shadow, grain, glass/chrome, ambient 3D, particles, bouncy easing. Four bounded allowances: content-swap blur ≤ 0.1 s ≤ 8 px, master motion blur, overshoot ≤ 3 %, purposeful 3D (flat or lit faces, justified). The list lives only in [anti-slop-video.md](references/anti-slop-video.md); `look.md` cannot re-enable any of it. Hard-fails: `motion-review` → [hard-fails.md](../motion-review/references/hard-fails.md).
11. **UI tokens are pointed to, never copied** — and UI micro-durations never set film read time.

---

## Architecture

```
Beat (from motion-method beats.md)
├── gestures         → focus-hierarchy.md   (one primary + subordinate details, how it enters)
├── motion           → easing-springs.md    (curve or spring preset)
├── timing           → timing-holds.md      (≤ 0.75 s gesture-free, CTA still ≤ 1.2 s, read time, split long reads)
├── into next scene  → continuous-take.md   (morph, mask wipe, push, grid cut, loop, gotchas)
├── color / type     → color-type-video.md  (ink/paper/accent, planes, type scale, safe zone)
└── self-check       → anti-slop-video.md   (bans + hard-fail IDs before the stills stage)
```

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Focus hierarchy** | [focus-hierarchy.md](references/focus-hierarchy.md) | Deciding what moves, how it enters, what stays still |
| **Timing & density** | [timing-holds.md](references/timing-holds.md) | Gesture-free span ≤ 0.75 s, CTA still ≤ 1.2 s, ≥ 1 onset/s; read time; splitting a long read |
| **Continuous take** | [continuous-take.md](references/continuous-take.md) | Scene-to-scene transitions, camera, loops; pops, detached cursor, counter smear |
| **Easing & springs** | [easing-springs.md](references/easing-springs.md) | Choosing a curve or spring preset; why UI durations don't apply |
| **Color & type for video** | [color-type-video.md](references/color-type-video.md) | Planes and contrast, accent field, type scale, composition, 9:16 safe zone |
| **Anti-slop (video)** | [anti-slop-video.md](references/anti-slop-video.md) | Self-check before stills; the single-source ban list and its hard-fail IDs |

### Templates

This skill ships no templates: its rules land in the beat map (`motion-method` → `references/templates/beats.md`) and in the scene, built from the `motion-art-direction` templates (composition-grid, kinetic-type, cut-rhythm) on `motion-render`'s seek/capture/encode mechanics.

### Pointed-to references (fuse-design, never copied)

| File | Use |
|------|-----|
| [motion-tokens.md](../../../design-expert/skills/design-motion/references/motion-tokens.md) | Named easing curves and UI spring configs |
| [animation-glossary.md](../../../design-expert/skills/design-motion/references/animation-glossary.md) | Feel → term vocabulary for beats and handoff |

---

## Best Practices

### DO
- Write each beat's primary gesture, its details, its behaviour and its curve into the beat map before coding.
- Check legibility on a 390 px-wide frame, not the master.
- Name each effect with the glossary term ("shared-element transition", "origin-aware scale").
- Let the critic's scores trace back to a numbered rule here.
- Start a handoff only once the previous drawing has fully landed; swap counters as whole values.

### DON'T
- Copy `motion-tokens.md` values into this plugin — link them.
- Use 200-300 ms UI timings as film read time.
- Leave a span over 0.75 s with no gesture (CTA still over 1.2 s), or keep it "alive" with a drift or an ambient loop.
- Blend two states by opacity, or reveal by opacity alone.
- Add a second accent "for variety", or a grey panel "for depth".
- Center the hero, set every line at the same size, or reuse one entrance on every beat.
- Reach for a banned effect "just for the intro" — `look.md` never makes it allowed.

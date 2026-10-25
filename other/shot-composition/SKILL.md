---
name: shot-composition
description: This skill should be used when the user asks to "compose a frame", "set up a grid", "plan shot composition", "place the focal point", "decide where elements enter and exit", "add a parallax/camera move", "adapt a layout for 16:9 / 9:16 / 1:1", or "keep content inside safe areas". Covers grids, safe areas, focal hierarchy, and 2D/3D camera framing.
version: 0.1.0
---

# Shot Composition

Stage the frame and move the camera: grid systems, safe areas, focal hierarchy, negative space, parallax layering, and how layout guides the eye over time. Produces composition notes, layer structure (bg/mid/fg), and concrete camera-move plans with numbers.

## When to use

- Defining a frame's layout, focal point, and negative space.
- Planning element enter/exit directions and motion paths.
- Designing camera push/pull, pan, follow, and parallax moves.
- Adapting one composition across 16:9, 9:16, and 1:1 with safe areas.

## Decision tree

```
What are you staging?
├─ A static frame's layout
│   └─ set grid → place ONE focal point on a thirds power point
│      → rank hierarchy (size>contrast>color>position) → reserve negative space
├─ Where things enter / leave
│   └─ follow reading direction; nearest edge; ease-out in, ease-in out
│      (new content → from right/below; back/undo → reverse it)
├─ A sense of depth / a camera move
│   └─ split into bg/mid/fg layers (the three motion layers)
│      → ONE camera move per beat (push | pan | follow | parallax), ease-in-out
└─ One comp across aspects (16:9 / 9:16 / 1:1)
    └─ master in 16:9, focal in the center band → RESTACK (don't crop) for 9:16
       → keep critical content inside title-safe margins
```

**Cross-reference — apply the shared frameworks.** This skill is the spatial half of `animation-principles`. Apply them explicitly:

- **1/3 Rule** (`animation-principles`) has two forms and this skill uses both *spatially*: (a) *Composition thirds* — place the focal point on a rule-of-thirds power point (33%/67%); (b) *Distance* — no element travels more than ~1/3 of the frame without an intermediate keyframe or a scale/opacity change, so entrances stay readable.
- **Three motion layers** (`animation-principles`: Primary / Secondary / Ambient) map directly onto depth: **foreground = Primary** (the move the eye follows), **midground = Secondary** (the subject + supporting reactions), **background = Ambient** (slow, low-contrast life). Parallax speed scales with that role.
- Settle the **Three Pillars** (Emotional intent / Visual narrative / Motion craft) and the chosen **Motion Personality** (`motion-art-direction`) *before* numbering a camera move — premium wants slow long pushes, energetic wants whip-pans.

## Core workflow

### 1. Establish a grid

A grid gives alignment and rhythm. Default to a **12-column grid** for landscape web/video (it divides into halves, thirds, quarters, sixths) with gutters and outer margins. For a 1920px-wide frame: outer margin 80-120px, 12 columns, gutter 24-32px.

```
content_width = frame_width - 2 * margin
column_width  = (content_width - (cols - 1) * gutter) / cols
```

Example (1920 wide, margin 100, gutter 24, 12 cols): content 1720, column = (1720 - 11*24)/12 = 121.3px.

A **baseline grid** (vertical rhythm) of 8px is the standard spacing unit; size and space everything in multiples of 8 (8/16/24/32/48/64) for visual cohesion.

### 2. Place the focal point

Use the **rule of thirds**: divide the frame into a 3x3 grid; place the primary subject on a third-line or at an intersection (the "power points"), not dead center — unless the piece deliberately uses symmetry for stillness/formality. The intersections roughly fall at 33%/67% horizontally and vertically.

Build **visual hierarchy** in this priority order to direct the eye: **size > contrast > color > position**. The biggest, highest-contrast element wins attention first. Establish exactly one primary focal point per frame; secondary elements support, never compete.

### 3. Use negative space as rhythm

Do not fill the frame. Generous negative space around the focal point makes it read as premium and confident, and gives motion room to breathe. Whitespace is an active compositional element, not leftover.

### 4. Layer the scene (bg / mid / fg) for depth and parallax

Split the composition into depth layers: **background** (slowest, lowest contrast, often desaturated/blurred), **midground** (the subject), **foreground** (fastest, may blur as it crosses). Parallax = moving layers at different speeds to simulate depth.

These depth layers ARE the `animation-principles` **three motion layers** projected onto Z — each layer's role dictates its speed, contrast, and how much motion it earns:

| Depth | Motion layer | Parallax speed | Contrast / focus | What lives here |
|---|---|---|---|---|
| Background | Ambient | 0.1–0.3x | low, often desaturated/blurred | sky, gradient, texture, set dressing |
| Midground | Secondary | 0.5–0.7x | mid; supports the subject | subject's environment, supporting elements |
| Foreground | Primary | 1.0–1.5x | sharp on subject; FG props blur as they cross | the hero subject + closest props |

Foreground may exceed 1.0 to read as very close. The Primary move is the one the eye follows; never give two layers competing primary motion.

### 5. Camera language (works in 2D and 3D)

- **Push / pull** — scale into or away from the subject (dolly). Builds intimacy or reveals context. 800-2000ms, ease-in-out.
- **Pan / tilt / move** — translate the frame across the scene. Reveals space, follows action.
- **Follow** — keep a moving subject framed (often slightly off-center, leading the motion).
- **Parallax** — layered move that sells depth.

**One shot, one intent.** Don't push + pan + rotate simultaneously — combined moves read as chaotic. Pick the single move that serves the beat. Inline timing essentials: camera moves use ease-in-out (`cubic-bezier(0.65, 0, 0.35, 1)`); never `linear` except continuous loops; slower is more cinematic.

### 6. Enter/exit direction carries meaning

Motion that follows reading direction (left-to-right, top-to-bottom in LTR locales) feels natural and smooth; reversing it creates tension or signals "back/undo." Match the direction to the intent:
- New content arriving -> enter from the right / from below.
- Dismissing / going back -> exit right or down, or reverse the entrance.
- Drilling deeper -> scale up / push in.

Elements should usually enter and exit through the nearest frame edge with a slight overshoot on enter (ease-out) and acceleration on exit (ease-in).

### 7. Safe areas and multi-aspect adaptation

Keep all critical content (text, logos, faces, CTAs) inside a **title-safe margin** so nothing gets clipped or hidden behind platform UI.

| Aspect | Use | Title-safe margin | Notes |
|---|---|---|---|
| 16:9 | YouTube, web hero | ~5% all sides | broadcast title-safe historically 10% |
| 9:16 | Reels, TikTok, Stories | top ~12-14%, bottom ~18-20%, sides ~6% | platform UI eats top and bottom |
| 1:1 | feed posts | ~6-8% all sides | symmetric |
| 4:5 | feed (taller) | ~6% sides, ~8% top/bottom | maximizes feed real estate |

Design the **focal point centered enough** that it survives all crops, then let secondary elements reflow per aspect. For 16:9 -> 9:16, restack horizontal arrangements vertically rather than just cropping the sides off.

## Worked examples

### GOOD — product hero, 16:9 → 9:16

> **Brief**: app launch hero, Premium personality, must work as a web hero and a Reel.
>
> - **Grid**: 1920×1080, margin 100, gutter 24, 12 cols. Phone mockup spans cols 7–11 (right power-column).
> - **Focal**: phone screen on the right thirds intersection (1280, 360) — not centered. One focal point; the headline (cols 1–5) is secondary, lower contrast.
> - **Depth (three motion layers)**: bg = soft gradient drift, 0.2x, Ambient. mid = phone mockup, 0.6x, Secondary stage. fg = one out-of-focus UI chip drifting past, 1.2x + 3px blur, reads as Primary depth cue.
> - **Camera**: single push-in, scale 1.0→1.10 over 1600ms ease-in-out, origin on the phone screen — matches Premium (slow, no overshoot). No pan added.
> - **9:16 adapt**: restack — headline moves *above* the phone, phone pulled up to the upper-middle to clear the bottom 19% CTA/nav zone, type +20%. Focal survives the crop because it started in the center band.
>
> Why it works: one focal point, depth roles assigned, one camera move, safe-area-aware reflow instead of a blind crop.

### ANTI-PATTERN — the "everything centered, everything moving" frame

> - Phone mockup dead-center, headline centered above, logo centered below → three elements fighting on the same axis, no hierarchy, no power point.
> - All three layers slide left at the same 1.0x speed → no parallax, no depth, reads as "the whole template moved" (violates the **1/3 Rule / distance**: a full-width slide with no intermediate keyframe).
> - Camera does push + pan + slight rotate at once → chaotic, no single intent.
> - 9:16 made by cropping the 16:9 sides → headline and logo clipped, phone too low behind the nav bar.
>
> Fix: pick one focal power point, assign each layer a depth role + distinct parallax speed, one camera move, and restack for vertical instead of cropping.

## Common mistakes

| Symptom | Why | Fix |
|---|---|---|
| Frame feels flat / "the template moved" | all layers move at one speed; no depth roles | assign bg/mid/fg the Ambient/Secondary/Primary roles + 0.2/0.6/1.2x parallax |
| Eye doesn't know where to look | 2+ elements at equal size/contrast, all centered | one focal point on a thirds power point; rank size>contrast>color>position |
| Camera move reads as chaotic | push + pan + rotate combined | one move per beat; pick the one that serves the intent |
| Content clipped on phones | designed for 16:9, cropped to 9:16 | restack vertically; keep critical content in title-safe margins (top 13% / bottom 19% on 9:16) |
| Entrance reads as "slide", not "event" | element travels >1/3 of frame in one unbroken move | break with an intermediate keyframe or pair travel with scale/opacity (1/3 Rule, distance) |
| Looks cheap / cramped | frame filled edge to edge | reserve negative space around the focal point; it's an active element |
| Motion fights the story | numbers chosen before intent | settle Three Pillars + Motion Personality first, then number the move |

## Deliverable — a composition plan

A good composition plan is handed to an implementation skill (`gsap-web`, `remotion-video`, `after-effects`) and contains:

- **Frame spec**: aspect(s), resolution, fps, grid (cols / margin / gutter), baseline unit.
- **Focal point**: coordinates (px or %) on a thirds power point + the hierarchy ranking of every element.
- **Layer map**: each element assigned bg/mid/fg → Ambient/Secondary/Primary, with parallax speed.
- **Enter/exit**: per element — edge, direction, easing family, and whether travel exceeds 1/3 (and how it's broken).
- **Camera move**: the single move, its property + from→to values, duration, easing, transform-origin.
- **Safe areas**: title-safe margins per target aspect + the restack plan for vertical.
- **Cross-refs**: which Motion Personality and which Pillars decisions drive the timing.

### Before you finish — checklist

- [ ] Exactly one primary focal point, on a thirds power point (or deliberate symmetry).
- [ ] Hierarchy ranked (size > contrast > color > position); secondaries don't compete.
- [ ] Negative space reserved around the focal point.
- [ ] Every element assigned a depth layer (bg/mid/fg = Ambient/Secondary/Primary) with a parallax speed.
- [ ] One camera move, not stacked; eased (not linear unless a loop); 800–2000ms for hero moves.
- [ ] Entrances/exits use nearest edge, follow reading direction, ease-out in / ease-in out.
- [ ] No element travels >1/3 of frame without an intermediate keyframe or scale/opacity change.
- [ ] Critical content inside title-safe margins for every target aspect; vertical is restacked, not cropped.
- [ ] Motion Personality + Three Pillars settled before any number was chosen.

## Quick reference

| Need | Default |
|---|---|
| Grid | 12 columns, 8px baseline, multiples of 8 spacing |
| Focal placement | rule-of-thirds power point, not dead center |
| Hierarchy order | size > contrast > color > position |
| Depth layers | bg / mid / fg, parallax 0.2x / 0.6x / 1.2x |
| Camera | one move at a time, ease-in-out, 800-2000ms |
| Enter / exit | follow reading direction; ease-out in, ease-in out |
| 9:16 safe | top 12%, bottom 18%, sides 6% |

## Reference files

- `references/camera-and-grids.md` — grid math with worked numbers, full safe-area percentage tables per aspect, parallax layering code (CSS scroll + JS pointer + Three.js), and named camera-move recipes (push-in, whip-pan, orbit, dolly-zoom) with keyframe values.

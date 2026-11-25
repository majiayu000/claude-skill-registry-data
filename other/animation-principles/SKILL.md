---
name: animation-principles
description: This skill should be used when the user asks to "make this animation feel natural", "fix motion that feels stiff/floaty/cheap", "my animation looks robotic", "choose an easing curve", "how do I use the Graph Editor", "add overshoot or bounce", "Easy Ease isn't enough", "make snappy motion", "pick a duration for this transition", "stagger a list animation", "sync animation to a beat", or "review motion for good timing". It is the tech-agnostic foundation for deciding how something should move.
version: 0.1.0
---

# Motion Principles

Decide how something should move so it feels right — independent of the tool used to build it. This skill answers timing, easing, spacing, weight, and rhythm. It does not pick a tech stack; it produces concrete numbers (durations, cubic-bezier curves, stagger offsets, spring configs) ready to hand to any implementation.

## When to use

- Motion feels stiff, floaty, mechanical, robotic, or cheap and needs diagnosis.
- Choosing a clip or transition's duration, easing curve, and stagger offset.
- Reviewing whether motion respects physics intuition (weight, follow-through, arcs).
- Synchronizing keyframes to a musical beat or edit accent.

## Three pillars — settle these before any number

Every piece of motion should answer three questions *before* you pick a duration or curve. Skip them and you get technically-correct motion that feels like nothing. These are the shared vocabulary the rest of the collection refers back to.

| Pillar | The question | What it drives |
|---|---|---|
| **Emotional intent** | What should the viewer *feel*? (joy, calm, urgency, trust, elegance) | Easing, duration, amplitude/overshoot |
| **Visual narrative** | What's the micro-story? Setup → action → resolution | Sequencing, staging, what enters when |
| **Motion craft** | How do we make it believable? | Physics, secondary motion, arcs, follow-through |

## Three motion layers — depth, not flatness

Flat motion = only the main thing moves. Believable motion runs three layers at once:

- **Primary** — the main action the eye follows (the hero move).
- **Secondary** — supporting richness reacting to the primary (a shadow shifting, an icon nudging, a label settling late).
- **Ambient** — background life that never demands attention (slow gradient drift, a low-contrast pulse).

> The judgment layer (`motion-art-direction`) calls these **Hero / Support / Texture** — same three layers, ranked for *what earns motion*. Primary≈Hero, Secondary≈Support, Ambient≈Texture.

## Core principles

### Easing is the single biggest lever

Linear motion reads as robotic. Reserve `linear` for continuous loops (spinners, marquees, infinite scroll) only. Everything an eye perceives as a discrete event needs acceleration.

Match the curve to the action:
- **Enter / appear** -> ease-out (fast start, gentle settle). Object arrives with energy and decelerates into place. `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Exit / disappear** -> ease-in (gentle start, fast end). Object accelerates away. `cubic-bezier(0.7, 0, 0.84, 0)`.
- **Move / reposition (stays on screen)** -> ease-in-out (symmetric). `cubic-bezier(0.65, 0, 0.35, 1)`.
- **Playful / branded** -> slight overshoot. `cubic-bezier(0.34, 1.56, 0.64, 1)` (the `1.56` pushes past 1.0, creating an overshoot-and-settle that reads as "weight").

Rule of thumb: the eye forgives a slow start far less than a slow end. When in doubt, decelerate into rest.

**Hand-shaping easing (After Effects).** When keyframing by hand rather than supplying a curve, the same principles map to the Graph Editor: shape the Speed Graph so the ends flatten toward zero, and push deceleration influence to 80–90% for a snappy launch and smooth settle. `F9` (Easy Ease) is only a 33% symmetric starting point — make it asymmetric. See `references/easing-graph-editor.md` for Graph Editor reading, handle/influence techniques, and step-by-step overshoot, anticipation, and bounce recipes (including a decaying-bounce expression).

### Timing communicates weight and importance

| Element | Duration |
|---|---|
| Micro-interaction (hover, toggle, tap feedback) | 100-200ms |
| UI transition (panel, modal, page region) | 200-400ms |
| Hero / large element / full-screen | 400-800ms |
| Cinematic camera move | 800-2000ms |

Distance and size scale duration. A small icon moving 20px and a full-bleed panel moving 800px should NOT share a duration — the panel needs more time or it looks weightless. A practical scaling: keep perceived velocity roughly constant by adding ~30-50% duration when distance or area roughly doubles. Heavy objects start slowly and overshoot less; light objects snap and may bounce.

### Spacing and stagger create rhythm

Never reveal a list, grid, or group all at once — it reads as a single flat event. Stagger each child's start.

- Lists / sequential items: **40-80ms** between items.
- Dense grids: **20-40ms** (more items, less per-item delay, or the tail drags).
- Cap total reveal at roughly **600-800ms** for a group; if `count * offset` exceeds that, shrink the offset or switch to a distance-based stagger (items further from an origin point start later).
- Stagger direction should follow the eye: top-to-bottom, or radiating from a focal point.

**The 1/3 Rule (two forms, both universal):**
- *Distance* — no element travels more than ~1/3 of the screen without an intermediate keyframe or a scale/opacity change. Long unbroken slides read as "the template moved," not "something happened."
- *Simultaneity* — with 3+ elements, keep no more than ~1/3 in active motion at once. The rest hold or move as ambient. Everything moving together = noise with no focal point.

### Anticipation and follow-through sell physical motion

- **Anticipation**: a tiny counter-move before the main action (a button dips `scale 0.95` before popping, a character crouches before jumping). 60-120ms is enough.
- **Follow-through / overlapping action**: trailing parts keep moving after the main body stops (a hero card lands, then its shadow and label settle 40-80ms later). Stagger the settle of attached elements rather than stopping everything on the same frame.
- **Arcs**: natural movement curves; pure straight-line translation of an organic object looks mechanical. Add a slight arc to x/y or animate a path.

### Beat-sync and rhythm

When motion accompanies audio, land impact keyframes (a hit, a cut, a reveal) on the beat, not between beats. At 120 BPM a beat is 500ms; an eighth-note grid is 250ms. Quantize key moments to that grid. For edits without music, establish a visual pulse (e.g. one major event per ~500-800ms) so the piece breathes consistently.

### Spring vs. duration-based motion

Springs (mass / stiffness / damping) self-determine duration and feel more physical for interactive, interruptible motion (drag-release, gestures). Duration+easing is better for choreographed, timeline-locked sequences (video, scroll-tied reveals) where exact sync matters. A snappy default spring: `stiffness 300, damping 30, mass 1`. See `references/easing-curves.md` for a full spring table.

## Diagnosing common failures

- **Feels stiff/robotic** -> using `linear` or symmetric easing on an enter; switch to ease-out.
- **Feels floaty/sluggish** -> duration too long or ease-out too gentle; cut duration 30%, sharpen the curve.
- **Feels cheap/janky** -> everything appears at once (no stagger), or all elements share one duration regardless of size.
- **Feels mechanical despite easing** -> no anticipation, no follow-through, straight-line paths; add arcs and overlap.

## Quick reference

| Need | Use |
|---|---|
| Enter | `cubic-bezier(0.16, 1, 0.3, 1)`, 300-500ms |
| Exit | `cubic-bezier(0.7, 0, 0.84, 0)`, 200-300ms |
| Move | `cubic-bezier(0.65, 0, 0.35, 1)`, 300-400ms |
| Branded pop | `cubic-bezier(0.34, 1.56, 0.64, 1)`, 400-600ms |
| List stagger | 40-80ms per item, cap ~700ms total |
| Loop only | `linear` |

## Reference files

- `references/easing-curves.md` — named cubic-bezier library with exact values, spring configs (Framer/react-spring/iOS), and per-element-type duration guidance.
- `references/easing-graph-editor.md` — After Effects Graph Editor craft: speed graph vs value graph, easing handles and influence/velocity numbers, and step-by-step snappy, overshoot, anticipation, and bounce recipes.
- `references/twelve-principles.md` — all 12 Disney principles, each with a concrete, numeric motion-graphics example.

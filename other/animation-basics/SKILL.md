---
name: animation-basics
description: Animation theory covering the 12 principles of animation and timing guidance. Use when designing motion, choosing easing approaches, or improving animation quality.
---

# 12 Principles of Animation

## 1. Squash and Stretch

Stretch in the area of more movement, squash on collision. Always conserve area — if you stretch one axis, compress the other.

## 2. Anticipation

Build up energy before action, like a spring loading. Can be combined with squash and stretch.

## 3. Staging

- Avoid competing for stage presence — one action at a time draws focus.
- Use the Camera to zoom into interesting areas.
- Insert pauses to let the viewer process information.
- Let text remain on screen long enough to read (up to 3x the time it takes to read aloud).

## 4. Straight Ahead and Pose to Pose

Pose to pose: define the key states (start, end, a few in-between holds) and let tweens fill the gaps. This is the default for code-driven motion: each `yield*` is a pose. Use straight-ahead, frame-by-frame motion (physics, procedural noise, springs) for organic or chaotic movement such as particles, liquids or confetti.

## 5. Follow Through and Overlapping Action

Drag adds realism. The main body leads; appendages follow with delay. This communicates mass. Use different timing functions for leading vs trailing parts. Skew can sell the effect.

## 6. Slow In and Slow Out

Essential for realism. Objects ease into and out of motion. Exception: collisions — ease only on the outward motion, not at impact. When motion is very fast, no inbetween frames may be needed — perfect for swapping icons or SVGs at the midpoint.

## 7. Arc

Move in arcs instead of straight lines when appropriate, especially when gravity is involved.

## 8. Secondary Action

Supplementary actions that support the main action. Example: a background element pulsing while the foreground element transitions.

## 9. Timing

Duration and spacing set weight and mood. A heavy object takes longer to start and stop; a light one snaps. Fast timing reads as energetic, slow timing as calm or heavy. Hold important poses long enough to register. See Timing Guidance below for concrete durations.

## 10. Exaggeration

Not more distorted — more convincing. Quick motions need bigger exaggeration to be noticed at all.

## 11. Solid Drawing

Avoid parallel lines for a more natural, dynamic look. Exception: graphs and data visualizations where parallel structure is intentional.

## 12. Appeal

Keep it simple. Do not add too many details. Clarity and readability beat complexity.

---

# Timing Guidance

Pick easing by the role of the animation:

| Role | Easing | Duration |
|---|---|---|
| Entrance (element appears) | ease-out (`easeOutCubic`) | 0.3–0.5s |
| Exit (element leaves) | ease-in (`easeInCubic`) | 0.2–0.3s |
| In-place change (move, resize, color) | ease-in-out (`easeInOutCubic`) | 0.3–0.8s |
| Emphasis (pulse, pop) | ease-out with overshoot (`easeOutBack`) | 0.2–0.3s |
| Stagger between grouped items | — | 40–80ms per word, 100–150ms per element |

- Never animate opacity alone for an entrance: combine it with a transform (rise,
  scale, or masked reveal). No entrance should exceed ~0.8s.
- A quick ease-in-out animation lets you swap icons or SVGs at the 50% mark — the fastest point of movement where the change is least noticeable.
- Use arc-based interpolation for movements that should follow a curved path, especially with gravity.


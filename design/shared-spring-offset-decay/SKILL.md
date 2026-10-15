---
name: shared-spring-offset-decay
description: Coordinate a moving surface and its content with shared spring progress and a decaying relative offset. Use when content should preserve its initial placement, gradually settle into its final alignment, and move with the surface during overshoot.
---

# Shared Spring with Offset Decay

## Pattern

For elements that should arrive and rebound as one visual unit, derive their relative placement
from the surface's spring progress. Express the initial alignment difference as an offset that
smoothly approaches its final value:

```text
p = spring progress from 0 to 1
q = clamp(p, 0, 1)
w = (1 - q) * (1 - q^4)
offset = finalOffset + (initialOffset - finalOffset) * w
contentPosition = surfaceAnchor(p) + offset
```

Measure both offsets in the same coordinate space. Choose an anchor that makes the relationship
clear; a text-box center is useful for centering. Convert to rendering coordinates afterward:
`left = centerX - textWidth / 2`. Account for parent scaling when painting in local coordinates.

## Why

A shared progress value keeps placement synchronized with the surface's timing and interruption.
The decaying offset preserves the departure while allowing internal alignment to change.
For the example curve, `w(0) = 1`, `w(1) = 0`, and `w'(1) = 0`: relative displacement and velocity
settle smoothly, so content shares the surface's overshoot without a phase switch.

The fourth-power factor keeps early motion close to linear offset decay and concentrates the
alignment adjustment later. Treat the exponent as a design choice, not a universal constant.
Clamp only the offset's progress; retain the surface's spring overshoot. A return below 1 produces
a small, smoothly reintroduced offset rather than restarting the animation.

## Application

- Apply the pattern to axes that need relative alignment. Keep other layout rules, such as a
  multiline first-line inset, independent when they serve a different visual purpose.
- Preserve text dimensions and wrapping when glyph scaling or reflow would distract from motion.
- Derive anchor displacement from scrolling or retargeting consistently for the surface and content.
- Validate initial placement, containment, handoff, and relative motion through overshoot at reduced
  playback speed. Include short content, long content, and extreme surface-to-content size ratios.

The offset curve coordinates motion; it does not guarantee containment during every size change.
Check the intermediate geometry, especially if the surface's size also overshoots.

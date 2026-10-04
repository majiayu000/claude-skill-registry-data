---
name: remotion-dynamic-frame-logic
description: Interpolating values based on frame index in Remotion. Use when mapping current frame counts to style properties like opacity, translation, or rotation.
version: "1.0.0"
verified_date: 2026-06-01
category: core
---

# Remotion Dynamic Frame Logic

## Purpose
Enforce precise mathematical interpolation recipes mapping frame counts directly to CSS styling vectors.

## When to Use This Skill
- Animating elements based on linear interpolation keys over time.
- Configuring translation bounds, opacity levels, and scaling sweeps per frame index.

## Output Format / Delivery
Provide high-performance, responsive React inline style mappings.

## Behavior Rules
1. **Always use clamp extrapolation flags** to avoid value overshoot out of bounds.
2. **Never interpolate heavy calculations on every frame manually** — use Remotion's `interpolate` utility.

## Maintenance Notes
This skill is locked for Remotion interpolation.

---

## Phase 1: Interpolation Logic Setup

```typescript
import { interpolate, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
```
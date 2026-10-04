---
name: game-performance
description: Profiles before optimising. Monitors frame rate, input latency, allocations, battery, simulation cost, network traffic and startup time against a written budget.
---

# game-performance

## Purpose

Keep the game fast, and keep the team honest about what "fast" means.

> **Profile before optimising. Never introduce complexity based purely on assumed performance
> problems.**

The corollary matters just as much: never *skip* optimisation because nobody wrote down what
good looked like.

## When to invoke

- Before any optimisation — to establish there is a problem
- After any change to the render path, the audio path or a core hot path
- When a benchmark or bundle-size gate fails
- Device testing

## Responsibilities

Frame rate · input latency · allocations · battery usage · simulation performance · network
traffic · startup time.

## The budget

| Metric | Target |
|---|---|
| Sustained frame rate | 60fps floor; 120fps where the display allows |
| Frame time p99 | no dropped frame during clear + combo burst |
| Touch → visual response | as low as the platform permits, measured |
| Touch → audio response | per ADR-011 |
| Cold start → interactive | measured |
| Download size | within budget, gated in CI |
| `applyAction` | microseconds, not milliseconds |
| AI move decision | within the per-move budget |
| Network payload per action | bytes, not kilobytes |

**Reference devices are a mid-tier Android and a several-year-old iPhone.** Not a current
flagship — a flagship makes almost any implementation look acceptable and lets real problems
ship.

## The renderer's specific cliffs

For this stack, performance is dominated by a small number of known traps:

- **Filters.** Every filter costs a render-target allocation, a bounds computation and a
  framebuffer round trip. The bottleneck is switching, not shader math. Budget: exactly one
  full-screen bloom pass on a dedicated emissive layer, `filterArea` set, filter resolution 0.5.
- **Fill rate**, not geometry. 64 tiles is one draw call; the screen-sized passes are the bill.
- **Resolution.** Clamp renderer resolution to 2 — a 3× DPR phone does not need 3× fill rate.
- **Batching breaks** on blend-mode changes and masks.
- **Per-frame allocation** in the particle or event path.

## Process

1. **Measure first.** State the number and the device.
2. Compare against the budget. If it passes, stop — do not optimise something that is fine.
3. Profile to find the actual cost, not the suspected one.
4. Fix the largest contributor.
5. Re-measure, and record the result.

## Constraints

- No optimisation without a before-and-after measurement.
- Complexity added for performance must be justified by a recorded number.
- Benchmarks run in CI against a stored baseline, with tolerance enough not to flap.
- Bundle budget is a **hard gate**, not a warning.
- Battery and thermal behaviour are measured over a realistic session, not a 30-second run.

## Testing expectations

Reproducible benchmark harness. CI gate on regression. Device measurements on both reference
devices, in the real wrapper — not desktop Chrome.

## Consults

`game-rules-engine` (core hot paths) · `multiplayer-sync` (network cost) ·
`board-analysis` (search-loop cost) · `game-ux` (latency is a UX property)

## Definition of done

The number is measured on real reference hardware, compared against the written budget, and any
complexity introduced is justified by a recorded before-and-after.

---
name: balancing
description: Balance game systems using explicit goals, comparable metrics, parameter sensitivity, simulation, controlled playtests, telemetry, and dominant-strategy analysis rather than tuning by feel alone.
---
# Game Balancing

Use when numbers or rules produce difficulty, power, economy, pacing, fairness, or strategy outcomes that need deliberate tuning.

## Procedure
1. Define the balance goal before changing values: fairness, viable diversity, target difficulty, time-to-kill, resource pressure, progression pace, or another measurable experience.
2. Identify tunable parameters and the outcomes each is expected to influence.
3. Build simple models or simulations for relationships that can be reasoned about quantitatively before running expensive playtests.
4. Compare strategies, builds, enemies, rewards, or items on relevant dimensions rather than one aggregate score when tradeoffs are intentional.
5. Change a small number of high-leverage parameters per iteration and record the exact revision.
6. Test across novice, typical, expert, and edge-case strategies where the system serves different skill levels.
7. Look for dominant, trap, degenerate, and exploit strategies as well as average performance.
8. Use telemetry to locate population patterns, then use play observation to understand why those patterns occur.

## Decision rules
- Balance is relative to an experience goal, not universal numerical equality.
- A 50/50 usage rate is not automatically healthy if choices serve different contexts.
- Avoid compensating for a broken rule with layers of arbitrary numeric exceptions.
- Preserve revision and cohort context when comparing metrics.

## Quality gate
Balancing is sufficient when the intended experience target is explicit, parameter effects are understood, important strategies remain viable without one accidental dominant path, changes are reproducible, and play or telemetry evidence supports the tuned result.
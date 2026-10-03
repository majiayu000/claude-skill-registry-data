---
name: supervisor-readiness
description: Maintain or extend the advisory supervisor-readiness layer that summarizes safe-operational health, watch items, and readiness state for long-running paper or testnet observation without changing execution behavior. Use when working on supervisor decision-support fields, readiness summaries, or operator-facing health/watch tables.
---

# Supervisor Readiness

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **Layers 9–10** operational health / observability; readiness is **not** **L7** risk replacement.
- **`AGENTS.md`** — advisory by default; hard risk and kill switches stay authoritative; traceable labels.

## Purpose

Use this skill to keep the repository's supervisor-readiness signals coherent, low-noise, and operator-usable.

This layer exists to describe operational health and watch conditions. It is not a hidden circuit breaker replacement and it must not silently alter trading behavior.

## Use When

Use this skill when:
- editing supervisor-related decision-support fields
- normalizing readiness labels such as `healthy`, `caution`, `degraded`, or `blocked`
- surfacing watch items in operator summaries, analytics, or experiment review
- deriving readiness stability from journaled runs
- extending provider-stack, liquidity, retry, or context-availability watch items from existing runtime data only

## Do Not Use When

Do not use this skill for:
- weakening hard risk controls
- auto-pausing or auto-enabling loops without an explicit task
- changing execution adapter behavior
- inventing health states that the codebase does not actually produce

## Safety Contract

- Supervisor readiness remains advisory unless the task explicitly adds controlled gating.
- Existing kill switches, breakers, and hard risk rules remain authoritative.
- Watch items must be short, truthful, and explainable from real runtime state.
- Paper-first defaults remain intact.

## Primary Workflow

1. Inspect the current supervisor or autonomy payload that already exists.
2. Reuse journaled fields before adding new runtime writes.
3. Normalize labels and watch items into short operator language.
4. Keep analytics compact and trend-oriented.
5. Verify no execution or risk behavior changed.
6. Prefer one shared readiness model across overview, analytics, and experiment review.

## Required Checks

- Readiness labels map cleanly to actual runtime states.
- Watch items do not leak raw debug structures into the primary UI.
- Long-running health summaries stay separate from trade approval logic.
- Operator-facing wording stays descriptive, not alarmist.

## Expected Output

- `Supervisor Layer:` what changed in readiness or watch summaries.
- `Operator Surface:` how readiness became easier to inspect.
- `Safety Check:` explicit note that readiness stayed advisory.

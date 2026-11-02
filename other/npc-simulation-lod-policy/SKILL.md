---
name: npc-simulation-lod-policy
description: Define simulation levels of detail for large NPC populations while preserving gameplay-significant outcomes and deterministic promotion.
---

# Npc Simulation Lod Policy

## Goal

Scale thousands of NPCs by allocating update frequency and model detail according to relevance, distance, and current obligations.

## Inputs to inspect

NPC systems, world regions, perception requirements, scheduled obligations, multiplayer rules if any, and performance budgets.

## Workflow

1. Classify NPC work into decision-critical, near-field interactive, regional, background, and dormant categories. Define what each tier must still simulate rather than treating distant NPCs as frozen.
2. Identify authoritative events that cannot be skipped, including committed trades, travel arrivals, needs crossing thresholds, combat transitions, and quest or faction changes.
3. Design promotion/demotion rules using hysteresis so NPCs do not churn tiers at boundaries. Keep tier transitions explicit and preserve pending actions and timers.
4. Use coarse time-step integration for background populations only where the model supports it. Reconcile elapsed time on promotion and cap catch-up work to prevent a burst of thousands of updates.
5. Profile representative population sizes and distributions, including dense cities, region borders, mass travel, and all-NPC promotion after teleport or reload.

## Validation checklist

- [ ] Tier changes preserve NPC identity, current task, obligations, and required event ordering.
- [ ] Background simulation has bounded CPU cost and no unbounded catch-up loop.
- [ ] Promotion causes no impossible jumps in position, needs, economy, or social state.
- [ ] Gameplay-visible NPCs use sufficiently detailed simulation when player actions can affect them.
- [ ] Population correctness is measured alongside frame time; no performance-only pass can hide lost events.

## Required output

Deliver a tier table with update rates, retained state, transition triggers, deferred work, test scenarios, and measured CPU cost by population size.

## Boundaries and failure handling

Do not assume far-away means irrelevant; do not use distance alone if economy, mission, story, or multiplayer authority needs higher fidelity.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.

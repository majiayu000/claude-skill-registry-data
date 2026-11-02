---
name: npc-agent-decision-budget
description: Allocate and verify CPU budgets for NPC perception, memory retrieval, planning, and actions across large simulated populations.
---

# NPC Agent Decision Budget

## Goal

Scale NPC decision-making with population while ensuring important agents remain responsive and the simulation degrades predictably under load.

## Inputs to inspect

Agent update scheduler, perception cadence, memory access, planner complexity, priority classes, population metrics and frame budget.

## Workflow

1. Inventory per-agent decision stages and measure CPU time, memory traffic and queue wait by population size and agent role.
2. Define update frequencies and maximum work per tick for active, nearby, background and dormant agent tiers; specify what each tier is allowed to skip.
3. Stress sudden population increases, dense settlements, long path requests and expensive memory queries while tracking tail latency and missed decision deadlines.
4. Test fairness and aging so lower-priority agents eventually update and emergency/mission-critical agents receive their declared service level.
5. Add aggregate counters and budget regression scenarios that compare decisions completed, backlog age and cost per simulated agent.

## Validation checklist

- [ ] Budgets are measured by stage and by population tier, not averaged across all agents only.
- [ ] Background throttling does not silently break essential state transitions or world invariants.
- [ ] Queue age and starvation are visible, especially for agents that remain relevant but low priority.
- [ ] The overload policy is bounded and has a documented recovery behavior.

## Required output

An NPC tier/update policy, stage-level cost profile, fairness metrics and repeatable population stress test.

## Boundaries and failure handling

Do not run a full LLM or expensive planner for every agent every frame; preserve lightweight and bounded decision paths where the design permits.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.

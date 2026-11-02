---
name: npc-state-machine-design
description: "Designs testable NPC state machines with explicit transitions and recovery. Use when villagers, enemies, workers, or companions become stuck or act unpredictably."
---

# Npc State Machine Design

## Use when
NPC behavior is buried in conditionals, causing invalid transitions, repeated actions, or dead-end states.

## Workflow
1. Define the NPC's observable states, active goals, permitted transitions, entry/exit effects, and interruption rules.
2. Separate sensing, state transition evaluation, action execution, and dialogue selection into testable stages.
3. Specify timeout, retry, unreachable-target, resource-unavailable, and despawn/reload recovery behavior.
4. Create table-driven tests for each transition and representative event sequences.

## Required output
A state diagram or transition table, transition guards, failure recovery rules, and test cases.

## Validation
- Every state has valid exits or a documented intentional terminal condition.
- Actions are not executed twice merely because a transition is re-evaluated.
- Interrupted and restored NPCs return to a valid state.

## Guardrails
Do not invoke an expensive language model on every simulation tick; reserve generative calls for suitable, bounded decisions.

---
name: npc-goal-lifecycle
description: Design NPC goal creation, persistence, interruption, completion, and failure transitions so long-running behavior remains coherent.
---

# Npc Goal Lifecycle

## Goal

Prevent agents from retaining stale goals, repeating completed tasks, or getting stuck after world changes.

## Inputs to inspect

NPC action/goal system, scheduler, navigation, world events, priorities, and save/load behavior.

## Workflow

1. Define goal states such as proposed, accepted, active, suspended, succeeded, failed, cancelled, and expired; specify legal transitions and terminal-state rules.
2. Record goal owner, target identity/version, preconditions, deadline/timeout, completion evidence, and expected side effects.
3. Map interruption events such as target destruction, path invalidation, inventory changes, threats, faction changes, and NPC LOD demotion to a transition or revalidation rule.
4. Ensure goal transitions are idempotent and that completion effects commit once even when animation or asynchronous work is delayed.
5. Test interrupted/reloaded goals, deleted targets, repeated completion events, priority preemption, and recovery after temporarily unavailable resources.

## Validation checklist

- [ ] Terminal goals cannot silently reactivate without a new decision.
- [ ] Target references are validated before action and after world changes.
- [ ] Priority preemption preserves resumable progress only where defined.
- [ ] Completion side effects are applied at a stable commit point and cannot duplicate.
- [ ] Save/LOD transitions preserve goal state according to explicit policy.

## Required output

Deliver a goal state diagram, transition table, stale-reference policy, side-effect contract, and interruption test suite.

## Boundaries and failure handling

Do not use an unbounded boolean set for goal progress; do not let NPCs keep acting on destroyed or inaccessible targets.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.

---
name: unreal-build-ai
description: Build Unreal decisions, perception and navigation using selected Behavior Trees, StateTree, EQS and Smart Objects with cancellable ownership.
engines: [UNREAL]
---

# Unreal Build AI

## When to use

Implement Unreal agent decisions, perception, navigation queries and contextual interactions. Mass entity storage/processing remains separate from decision authoring.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-ai` before edits or tool launches. Require effective engine `UNREAL` and `compatible: true`; revalidate task overrides/output scope. Requesting this skill never selects an engine.

Read release, selected AI plugins, controller/pawn topology, decision framework, navigation data, authority and agent budgets. Behavior Tree versus StateTree is a project decision. Record context/evidence in resolved `.hephaera/.cache/tasks/<task>/`; preserve `ENGINE.md`.

## Workflow

1. Map decision, observation, blackboard/state, movement and action authority. Distinguish server decisions from replicated presentation and define missing-controller/target/path outcomes.
2. Implement selected Behavior Tree tasks/services/decorators or StateTree tasks/transitions with explicit enter/tick/success/failure/abort. Shared node templates cannot accidentally retain per-agent mutable state.
3. Retire observations on perception expiry, target destruction, team change and world streaming. Revalidate eligibility at authoritative action time rather than trusting cached perception.
4. Configure navigation agents, filters/costs, dimensions and generation against movement constraints. Route requests through existing movement ownership; cancel only the request owned by the decision.
5. Use EQS only when selected and justified. Bound query frequency/candidates, track decision generation and discard stale asynchronous results.
6. For selected Smart Objects own reservation/claim handles. Release on abort, death, target loss and travel; failed or expired claims return bounded outcomes instead of endless retries.
7. Budget perception, decision ticks, path requests and backoff. Use debugger/visual-log evidence to find state errors before adding polling or raising update rates.

Read [decision and cancellation boundaries](references/decision-navigation-cancellation.md) when authoring tasks or navigation integration.

## Verification

Test success, unreachable/missing target, latent abort, expired observations, claim contention and world teardown. Use real native AI/navigation assets. Record representative agent counts and cost; a Behavior Tree abort fixture cannot certify unexercised StateTree, EQS or Smart Objects.

## Output

Decision graph/data ownership, native-authored tasks/assets, resource/cancellation policy and scoped runtime/profile evidence. Record environment, expected/observed outcomes and blocked/not-run checks.

## Boundaries

No automatic plugin enablement, engine changes or binary-asset synthesis. Match host APIs and target platform, preserve gameplay authority, budgets and approval/publication gates.

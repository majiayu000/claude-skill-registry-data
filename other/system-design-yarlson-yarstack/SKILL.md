---
name: system-design
description: Design the smallest system or feature architecture that satisfies stated current requirements, for a greenfield product or a new capability in an existing codebase. Use when the user wants a proposed design with components, non-goals, and growth triggers; not for investigating existing behavior, settling one open decision, or planning phases.
---

# System Design

Produce the smallest design that satisfies today's stated requirements and name what would justify more. Every component, process, dependency, and abstraction is a cost that must buy a named requirement.

## Fix the constraints

1. Extract the actors, the jobs they need done, and the observable outcomes that define success.
2. Record load, data volume, team size, delivery horizon, deployment target, and hard constraints such as compliance, latency, or an existing platform. When a value is unknown, assume the smallest plausible value, write the assumption down, and design for it. Never design for unknown scale.
3. In an existing codebase, find the owning module, its current contract, conventions, runtime shape, and deployment path before proposing anything. Use `system-investigate` when current behavior is unclear.
4. Write non-goals: capabilities, scales, and actors the design intentionally excludes.

## Design from the baseline

1. Start from the baseline: one deployable process, the datastore already in use or the most boring option, synchronous calls, no new infrastructure. For a feature, the baseline is a change inside the owning module.
2. Add a component, process, queue, cache, service boundary, framework, or dependency only when a stated requirement or measured constraint fails without it. Name that requirement next to the addition.
3. Spend design effort on decisions that are expensive to reverse, such as the storage model, public contracts, and tenancy. Keep everything else deferrable.
4. Reject additions justified by scalability, extensibility, flexibility, future-proofing, best practice, or how a larger organization solves the problem. Reject an abstraction with one consumer.
5. Give each module one decision to own and one representation to hide. Do not split by technical layer or workflow step when one ordinary change would then touch every piece; a layer that hides a decision, such as a storage or protocol adapter, is a valid module.

## Check the design

1. Walk each actor's main job through the design end to end. Remove anything the walk does not touch.
2. Apply failure, retry, idempotency, migration, rollout, and security requirements only where a walk crosses a trust boundary, a state change, or an external system. Record the rest as deferred with the trigger that makes each relevant.
3. Estimate processes, external dependencies, modules, and rough lines of code. When the estimate exceeds what the team can build and operate within the horizon, cut components or scope, not quality.
4. State the strongest simpler alternative and the named requirement it fails. If it fails none, adopt it.

Use `architecture-refine` when the user must choose between remaining options, `technical-spike` for a blocking external fact, `alternatives-explore` for a contrarian bet, and `plan-create` to turn the accepted design into phases. Do not implement, write a plan, or edit repository documents unless authorized.

## Result

Report the requirements and assumptions with values, non-goals, each component with the requirement it satisfies, the data flow for each main job, deferred concerns with triggers, the size estimate, the rejected simpler alternative, and open decisions. Finish when every component traces to a requirement and every excluded concern has a trigger.

---
name: brainstorming
description: Resolve design decisions before implementation when requirements, contracts, or product trade-offs need clarification; scale the process to existing decisions and task risk.
---

# Brainstorming

Use this skill to resolve design decisions that affect the requested outcome. First inspect the relevant code, requirements, and existing decisions.

## Choose the necessary depth

- Proceed with implementation when the intended behavior and constraints are clear and remaining choices are routine and reversible. File count or a behavior change alone does not require a design approval loop.
- For substantial work, write a scaled design covering the actual contracts, failure modes, verification, and rollout. Reuse an approved spec or existing plan rather than generating another.
- Ask focused questions only for unresolved decisions that materially change product behavior, scope, compatibility, data handling, security, cost, or rollback. Discover file locations and existing conventions yourself.
- Offer alternatives when there is a real trade-off. Do not manufacture multiple designs for an already specified outcome.
- Continue independent authorized work while a necessary answer is pending. Do not perform a dependent action until its required decision or approval is available.

## Authorization and handoff

The user's request and prior decisions establish the authorized scope. Do not ask for the same approval twice, and do not infer permission for unrelated external actions. Repository-specific security, data, and release requirements remain in force.

Save a design in the repository's established location when it will help implementation or future review. Use `writing-plans` when sequencing needs a durable implementation plan and that skill is available. For an implementation request, continue through implementation and relevant verification after resolving the design. For a design-only request, deliver the design and stop at that requested boundary.

Before handoff, check scope, unresolved assumptions, and the evidence needed for completion. If an instruction prevents progress, identify its exact file and requirement rather than attributing the stop vaguely to the skill.

Read [visual-companion.md](visual-companion.md) only when a visual design companion is useful and requested or accepted.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for upstream attribution and licensing.

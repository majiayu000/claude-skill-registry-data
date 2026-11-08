---
name: architect
description: Design types, interfaces, and module boundaries for an explicit architecture request or an unresolved consequential design choice.
disable-model-invocation: true
---

# Architect

Resolve the design question before implementation.
A mechanical caller or signature change does not need a design exercise.

## Scope

Inspect the relevant contracts and consumers.
Use [How](../how/SKILL.md) when an architectural explanation would resolve a material uncertainty.
Reuse an existing source model instead of repeating subsystem exploration.

Sketch only the types, signatures, or module boundaries needed to assess the decision.
Compare distinct designs when the user requests alternatives or consequential uncertainty remains.
Use independent candidates when separate expertise justifies the cost and delegation is available.
Do not require a fixed candidate count or an unavailable comparison skill.
For a requested multi-candidate review, use [the candidate brief](references/subagent-prompt.md) and [design rationale](references/rationale-template.md).

Assess interface depth, ownership, and consumer requirements.
Use [design red flags](references/design-red-flags.md) when a proposed abstraction needs review.
Use [architecture guidance](../../programming/references/architecture/architecture-planning.md) for prerequisite and dependency decisions.

## Completion

For design-only requests, return the recommendation, necessary sketch, tradeoffs, and unresolved decisions.
For authorized implementation, continue through [Programming](../../programming/SKILL.md) without another approval gate.
Pause when the user requests a checkpoint or a missing decision materially changes scope.

If implementation disproves the design, reassess the affected assumption.
Revise the sketch or compare another design when evidence warrants it.
Do not restart the complete investigation for an ordinary parameter correction.

Use [verification guidance](../../programming/references/verification-before-completion.md) to assess the result and reuse valid evidence.

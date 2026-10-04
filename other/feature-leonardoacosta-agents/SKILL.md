---
name: feature
description: Refine an accepted idea into a validated, approved OpenSpec-compatible change without imposing vendor-specific governance or task tracking.
---

# Feature

Create an executable change definition. OpenSpec-compatible artifacts are the interchange format; this skill is not an OpenSpec vendor workflow.

## Stages

1. Load the request and any exploration record.
2. Discover repository instructions, active changes, relevant capabilities, implementation surfaces, tests, and dependencies.
3. Resolve genuine product and architecture decisions. Ask only for judgment that repository or Context7 evidence cannot settle.
4. Define scope, non-scope, actors, behavior, edge cases, user actions, dependencies, touched capabilities, migration needs, and acceptance evidence.
5. Draft `proposal.md`, requirement/capability deltas, optional `design.md`, and ordered `tasks.md` under the repository's change directory.
6. Make task dependencies explicit. Do not add universal DB/API/UI/E2E phases.
7. Validate artifact structure, requirement scenarios, task readiness, paths, and dependency consistency.
8. Present the change for approval. Do not begin implementation before approval.

## Required quality

Every material requirement needs observable behavior and failure/edge scenarios. Every unresolved human action is either resolved during authoring or represented as a dependent proposal boundary. Out-of-scope behavior is explicit. Tasks include scope and verification instructions.

## Do not include

Beads, vendor-specific issue IDs, mandatory ambiguity lenses, constitution audits, telemetry, or hidden governance passes. Those belong to separate skills when explicitly requested.

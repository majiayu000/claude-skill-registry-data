---
name: improve
description: Audit a codebase or prepare an implementation plan for a specified improvement.
license: MIT
metadata:
  author: shadcn
  version: "1.2.0"
---

# Improve

Return evidence-backed recommendations or a self-contained plan for the requested scope.
User instructions define the deliverable and override these defaults.

## Select the route

- Audit or roadmap: use [Audit](references/audit.md).
- Create or revise a plan: use [Plans](references/plans.md).
- Apply findings or execute a plan: use [Execution](references/closing-the-loop.md) and [Programming](../programming/SKILL.md).
- Reconcile existing plans or publish requested issues: use [Plan maintenance](references/closing-the-loop.md).

Read only the route needed for the current task.
An audit does not require a plan, repository scoreboard, or source changes.
An explicit request to apply findings authorizes the selected implementation scope without another approval gate.

## Scope and evidence

Inspect the source and contracts needed to answer the question.
Distinguish observed defects from inferred risks and optional product directions.
Support each recommendation with a source location, concrete cost, and confidence.
State material tradeoffs and limits.

Keep audit operations read-only.
Write plan files only when requested.
Report credential locations without secret values.
Do not commit, push, or publish without authorization.

Use repository checks that address the affected contract.
Record unavailable checks and unresolved assumptions instead of inventing commands or results.

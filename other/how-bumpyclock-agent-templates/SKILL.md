---
name: how
description: Explain codebase behavior, ownership, or architecture from source evidence.
---

# How

Answer the codebase question at the level needed for a useful mental model.
An explanation or design recommendation is read-only unless the user also requests changes.

## Direct answer

Inspect the relevant entry points, contracts, callers, and documented decisions.
Trace the path needed to answer the question.
Distinguish observed behavior, documented intent, and inferred rationale.
State unresolved uncertainty rather than invent a reason.

Return the supported answer and useful source locations.
For a decision, give a recommendation and its tradeoffs.
A narrow question needs neither a repository map nor a full architecture report.

## Complex questions

Use [Complex investigation](references/complex-investigation.md) when several independent paths or substantial source context need synthesis.
Use [Architecture critique](references/critique-rubric.md) for a requested critique or an unresolved design tradeoff.
These routes do not require delegation or a separate explanation artifact.

Do not create a prototype, edit source, commit, or open a pull request unless the task authorizes that action.

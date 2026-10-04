---
name: validate-change
description: Validate an implemented change against its agreed acceptance criteria before closing, syncing or archiving it. Use when work looks finished and needs a satisfied/failed/pending decision per criterion. This is distinct from lint, tests (verify-change) and OpenSpec structural validation.
---

# validate-change

Read normative criteria, the exact implemented revision, technical results and
review findings. Use [references/evidence.md](references/evidence.md) to maintain
acceptance in the existing dossier. You may update evidence/tasks; do not fix the
implementation, change criteria to fit a failure or publish.

## Steps

1. For every required criterion, compare the expected scenario and need with the
   observed API/data/effects, UI interaction/navigation or operational result.
   Check defined error/recovery paths.
2. Reuse current technical evidence when it already demonstrates the criterion
   instead of rerunning green suites. Fullstack contracts require the real
   boundary; do not invent a screen for backend-only work.
3. Route problems: implementation failures return to their owner; a changed or
   wrong requirement returns to define-change. Continue independent criteria
   when an environment blocks one.
4. Decide globally against the Definition of Done: every required criterion
   satisfied on the final revision, impact checks passed, relevant findings
   resolved, contracts/docs/ADRs current, tasks linked to evidence and owned
   resources cleaned.
5. Only after verified/validated closure, use openspec-sync-specs/archive as
   applicable. Apply this acceptance preflight before invoking them.

## Output

| Criterion | Status (satisfied/failed/pending/blocked) | Evidence (revision, command or observation) |
| --- | --- | --- |

Follow the table with the global decision and its reason, and the next owner for
each non-satisfied criterion.

## Gotchas

- A technically green implementation that contradicts acceptance fails.
- A failed/pending required check, stale evidence, an unresolved relevant finding
  or explicitly required UAT still pending prevents global validation.
- Do not mark a required criterion not applicable merely to close it.
- Agent acceptance is not human approval; request human judgment only if it is
  required and unresolved.
- Task checkboxes, OpenSpec validation and archive are administrative signals.
  If upstream wording reports `all_done` or offers archive, read it as
  structural state only.
- Cancellation or an explicitly requested incomplete archive stays labeled
  incomplete and must not promote unaccepted behavior.
- Merge, release and deploy keep their own scope and authorization.
- OpenSpec skills and opsx commands are upstream-managed; do not edit them. Use
  the available interaction/progress capability and repository-locked CLI.

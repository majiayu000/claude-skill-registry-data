---
name: sdd-review
description: >
  Independent, traceable code review of one SDD Composy task in review_required
  against its approved PRD, stories, TechSpec, evidence, and project rules, with
  stable findings and severities. Use when a task passed QA and evidence — 'revisar
  a TASK-003', 'code review da task', 'review this task's diff'. Do NOT use for code
  review outside an SDD workspace (use the host code review), for QA (sdd-qa), or
  for verification (sdd-verify).
metadata:
  version: 0.1.0
---

# SDD Review

This portable skill performs an independent code review of one task in `review_required`: an
explicit base and target diff scope against the approved contracts (requirements, stories,
architecture), the task evidence, and the project rules. Read `templates/codereview.md` and render it, keeping its
frontmatter keys and headings exactly (translate prose only).

Language: before writing human-facing prose, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Procedure

1. Validate that the declared base, target, and changed paths are explicit and confined. Stop on
   an ambiguous or expanded diff scope.
2. Read only the approved contracts, current task evidence, and applicable project rules. Do not
   change them or infer approval from their existence.
3. Run and record the exact verification commands, environment, exit codes, and confined evidence
   paths.
4. Check skill conformity: confirm the change was produced through the SDD task contract and its
   skills, not around them (no adapter bypass, no edited approvals).
5. Record every finding with a stable ID, severity (`BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`),
   file and line, evidence, and rule citations or contract citations. Do not silently fix, hide,
   or rewrite a finding; an unapproved change requires a new review.
6. Produce an OKF v0.2 `CODE_REVIEW` report. A complete human-approved report records
   `scripts/sdd_tasks.py evidence <state> <TASK-ID> review --status approved` and transitions to
   `verify_required`; any blocker, missing evidence, scope ambiguity, contract violation, or
   non-conformity records `review --status rejected` and transitions to `rejected --reason <text>`.

## Read when

- `references/quality.md` — writing the report (evidence and gate semantics shared with QA).

## Output

Return the report path, exact base/target scope, approved contracts consumed, findings and
severities, cited rules, commands and exit codes, skill conformity, blocker status, the
no-silent-fix result, lifecycle status, and permitted next transition. Keep generation and
verification actors separate. Do not edit source, requirements, stories, architecture, task
evidence, or the review to make checks pass, and do not stop user-owned services.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.

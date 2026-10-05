---
name: sdd-verify
description: >
  Adversarial verification of one SDD Composy task in verify_required: reproduce
  every claim with fresh commands, build the truth table, refute stale evidence, and
  produce the verdict that gates complete. Use when review is done and the task
  claims to be finished — 'verificar a TASK-003', 'a task está pronta mesmo?', 'is
  this task really complete'. Do NOT use for QA, code review, or a general 'verify
  my work' outside an SDD task.
metadata:
  version: 0.1.0
---

# SDD Verify

This portable skill is the adversarial gate for a task in `verify_required`: independently
reproduce every required claim with a fresh command, build the truth table, and attempt to refute
the earlier evidence. Read `templates/verdict.md` and render it, keeping its frontmatter keys and
headings exactly (translate prose only).

Language: before writing human-facing prose, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Contract

Record confined evidence paths, SHA-256 digests, exit codes, and environment, and keep generation
and verification actors separate. Use only `PASS`, `FAIL`, `STALE`, `ENVIRONMENT_FAILURE`, and
`NOT_RUN` verdicts; classify an environment failure separately from a failed test. Reject stale,
contradictory, missing, or hash-inconsistent evidence.

Only all-fresh `PASS` claims with non-blocking QA/review and explicit human approval approve the
verdict (`verdict: COMPLETE`), record `scripts/sdd_tasks.py evidence <state> <TASK-ID> verify
--status approved` and `trace --status consistent`, and request the guarded task transition
`verify_required -> complete` (the `COMPLETE` workflow stage); every other outcome sets the
verdict to `REJECTED`, records `verify --status rejected`, and moves the task to
`rejected --reason <blocker>`, with a sanitized blocker and next action. Do not silently change claims, contracts, or source,
and do not stop user-owned services.

## Read when

- `references/verification.md` — writing the verdict (verdict semantics, staleness, refutation).

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.

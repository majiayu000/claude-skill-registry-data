---
name: sdd-quick
description: >
  Deliver a small bounded change inside an initialized SDD Composy workspace through
  the quick path: at most five implementation files, a registered TASK, TDD,
  evidence, trace, and a verified verdict, escalating otherwise. Use for a precise
  objective with no existing task — 'ajuste rápido via SDD', 'quick fix under SDD',
  'small change to X in the SDD flow'. Do NOT use for an already registered task
  (sdd-execute), for architecture, migrations, or destructive work, or in
  repositories without SDD Composy (other plugins' quick).
metadata:
  version: 0.1.0
---

# SDD Quick

Use this portable skill (`$sdd-quick` in Codex mentions) only for a precise bounded objective in
an initialized SDD Composy workspace. A quick task is a controlled entry path into the normal SDD
flow, not a shortcut around review, evidence, or verification.

Language: before writing human-facing prose, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Required protocol

1. Inspect repository instructions and preserve unrelated changes.
2. Reject or `ESCALATE` before edits if more than five implementation files, architecture,
   migration, destructive work, scope change, or unknown verification is involved. When a
   machine-readable eligibility decision is needed, use the side-effect-free gate
   `scripts/sdd_quick.py <contract.json>`.
3. Read `templates/quick-contract.md` and render the OKF `QUICK_CONTRACT` from it (keep its keys and headings), assign a `Q-*` identifier
   (the Q-ID), and register a normal `TASK-*` record: render `tasks/prd-<slug>/task-<id>.md` from
   `templates/task.md` and run `scripts/sdd_tasks.py import`; quick work never bypasses task
   lifecycle gates and records its gate evidence with `sdd_tasks.py evidence`.
4. Write and run a failing test before implementation (TDD). If it cannot be run, escalate.
5. Implement only within the closed allowed-file list and run the known verification.
6. Collect acceptance evidence, review, and verification. Append semantic events with
   `scripts/sdd_trace.py record <repo-root> --event <event.json>` only after their actions
   succeed; never write `trace.json` directly.
7. Create the OKF `QUICK_REPORT` from `templates/quick-report.md`, link all evidence from the
   bundle index, verify the trace and artifact integrity, and publish a `COMPLETE` verified
   verdict only when every gate passes. Otherwise report `ESCALATED`, `REJECTED`, or `CAVEATS`.

Never record prompts, output dumps, environment variables, secrets, models, or private paths. Do
not silently expand scope. If quick work needs a task synchronization, the plan-bound
`CONFIRM-SDD-SYNC-…` token of `sdd-sync` still applies.

## Read when

- `references/quick.md` — the eligibility gate is unclear, or when writing the contract (step 3)
  and the report (step 7).

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.

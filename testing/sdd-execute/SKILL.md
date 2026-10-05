---
name: sdd-execute
description: >
  Implement exactly one SDD Composy task in the ready state with dependency
  preflight, TDD RED evidence, allowed paths, real verification commands, and the
  guarded transition to qa_required. Use when a ready task should be executed —
  'executar a TASK-003', 'implementar a próxima tarefa', 'run task 4'. Do NOT use
  for changes without an approved task (sdd-quick), for autonomous multi-stage
  correction (sdd-loop), or for QA, review, or verification.
metadata:
  version: 0.1.0
---

# SDD Execute

This portable skill implements exactly one `ready` task. The bundled `scripts/sdd_execute.py`
functions `preflight`, `run_command`, and `finish` are the deterministic execution boundary;
preserve their result fields and never create test-only bypasses.

Language: before writing human-facing prose, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Contract

- Require exactly one `ready` task and a successful dependency preflight.
- Require TDD RED evidence before implementation, enforce the task's allowed paths, and run the
  declared verification commands, each as a real command. Record sanitized stdout/stderr, exit codes,
  SHA-256 evidence, environment ownership, and cleanup.
- Never modify approved contracts or user-owned processes.

On success, record the passing verification run with `scripts/sdd_tasks.py evidence <state>
<TASK-ID> tests --status passed --ref <command-record>` and request the guarded
`running -> qa_required` transition. A concrete dependency, environment, QA, evidence, or cleanup
blocker becomes `blocked`; a scope violation or rejected contract becomes `rejected` (both through
`transition ... --reason <text>`, from `ready` or `running`). Record the exact reason and next action, and stop on any QA or review
blocker.

## Read when

- `references/execution.md` — before the first `run_command` of a task (preflight fields, TDD
  evidence, path and command rules, outcome classification).
- `references/states.md` — a transition other than `running -> qa_required` is needed.
- The approved task contract (`tasks/prd-<slug>/task-<id>.md`) — always, it is the input.

## Output

Return the execution result, evidence manifest, changed paths, ownership and cleanup status, and
the permitted next lifecycle action.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.

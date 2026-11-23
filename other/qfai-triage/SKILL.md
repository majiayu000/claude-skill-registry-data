---
name: qfai-triage
title: QFAI Triage (Requests that end without a tracked change)
description: "Use when invoked by name or handed a QFAI work order for a request ending with no tracked change but its deliberation record, open questions and approval row: a question, a duplicate, missing information, a split, automated reports, a security report, an operation only a person can run or the user named on finished work, or authorized cleanup of current-task temporary directories."
argument-hint: "<the request, as it was reported>"
allowed-tools: [Read, Glob, Grep, Write, Bash, TodoWrite, Task, Agent]
steps:
  - triage-dedupe
  - triage-request-info
  - triage-investigate
  - triage-answer
  - triage-decompose
  - triage-cluster
  - triage-security-intake
  - triage-handoff
  - triage-owned-cleanup
  - triage-operate
  - triage-close
requires: []
mode: execution-focused
---

## /qfai-triage - Requests that end without a tracked change

Run the entry check of
`.qfai/assistant/rule/shared-skill-operating-baseline.md#workflow-run-entry-check`
first.

This skill answers, closes, splits or hands over a request, or carries out an
operation the user named, and changes no file git tracks except the ones the
Reviewer Gate below allows. Work the request needs is recorded as a follow-up request,
never done here except the exact current-task temporary cleanup that
`triage-owned-cleanup` permits, after rechecking existing user authority and
repository-local scope, and the named operation `triage-operate` runs. No other
triage step executes an operation, and `triage-handoff` still waits for the
person's reported result.

## Inputs

- The request, as it was reported, and any item it names.
- The project's documents, code and history, read only.
- `.qfai/assistant/rule/*`.
- Before an agent decision, search the records for a turned-down option, as
  `.qfai/assistant/rule/references/deliberation-record.md` says.

Every step follows `.qfai/assistant/rule/shared-skill-operating-baseline.md`
and `.qfai/assistant/rule/shared-skill-delegation-baseline.md`. Questions to
the user follow
`.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.
A step whose `What it writes` says "No file git tracks" still writes the run's
deliberation record when it asks the user a question or takes an agent decision.

## Steps

Invoked by name, run the steps in this order, as
`.qfai/assistant/rule/shared-skill-operating-baseline.md#a-parent-skill-invoked-by-name`
states: read `.qfai/assistant/step/<name>/STEP.md` for the current step only,
run it, then move to the next.

| Step                     | What it does                                                               | Skipped when                                                                     |
| ------------------------ | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `triage-dedupe`          | Finds the same or a successor item, and links it                           | The request neither may repeat an existing item nor rests on a premise that aged |
| `triage-request-info`    | Asks for the facts the request is missing                                  | The request states every fact its handling needs                                 |
| `triage-investigate`     | Reads internals, history and outside facts to find the answer              | The documents and code as they stand answer the question                         |
| `triage-answer`          | Answers, citing what shows the answer                                      | The request asks no question                                                     |
| `triage-decompose`       | Splits the request into child requests with their dependencies             | The request is one piece of work                                                 |
| `triage-cluster`         | Groups automated reports by signature                                      | The request is not a set of automated reports                                    |
| `triage-security-intake` | Takes a vulnerability report in privately                                  | The request reports no exploitable weakness                                      |
| `triage-handoff`         | Gives a person the steps of an operation only they can run                 | The request needs no operation that only a person can run                        |
| `triage-owned-cleanup`   | Removes authorized current-task temporary directories and verifies absence | The request is not the specific repository-local cleanup the step permits        |
| `triage-operate`         | Runs the operation the user named on finished work, and reports its result | The request names no operation                                                   |
| `triage-close`           | Records the outcome and each follow-up, and closes                         | Only `triage-security-intake` ran: the fix follows it, so the request stays open |

Invoked by name, the skill ends at this stage. It starts no other stage and
routes no follow-up: a request to carry a follow-up out goes to `qfai-run`.

Inside an `npx qfai workflow` run, the work order lists the steps to run and
this file adds nothing to it.

## Review

Invoked by name, the skill runs no review: its steps change no tracked file
other than the ones the Reviewer Gate allows.
Each step's `## Gate` section says what passes it.

### Reviewer Gate

A tracked file the stage changed fails the review, whatever the change was,
except these:

- the run's deliberation record and the `open-questions.md` rows the run
  wrote, which `triage-close` commits locally and does not push;
- the approval row, if any, that `qfai-run` records in `decisions.md` before
  `triage-handoff` runs.

`triage-owned-cleanup` keeps its own check that tracked contents and the index
are unchanged.

## Completion

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#completion-contract-shared`.
**Smallest applicable smoke check** (this skill's override):
`git status --porcelain --untracked-files=no` lists no file the stage did not
find changed when it started, and the commits the stage made touch only the
run's deliberation record, the `open-questions.md` rows the run wrote and the
`decisions.md` approval row the Reviewer Gate allows.

The report states the outcome `triage-close` recorded and lists each follow-up
request. It never says a tracked change is done. `cleaned` says only that the
named temporary targets were removed and their absence and unchanged tracked
contents and index were verified; unfinished cleanup cannot use it.
Ask for the next action only when
proceeding requires the user's answer, as `.agents/rules/user-questions.md`
§ 6 sets out. A closure-only report needs no question. Under a no-question mode,
list any remaining actions instead.

## Default Autopilot Policy

- hard-required:
  - triage request (the request to answer, close, split or hand over; an empty request is asked for, never guessed)

project_memory:

- Triage changes no tracked file except the run's deliberation record and `open-questions.md` rows, which `triage-close` commits locally, and the approval row `qfai-run` records in `decisions.md` before `triage-handoff`.
- Only `triage-owned-cleanup` and `triage-operate` execute an operation.
- Other work it finds is a follow-up request.
- A follow-up is recorded, never routed inside the run that found it.
- A security report stays private until the fix is ready to disclose.

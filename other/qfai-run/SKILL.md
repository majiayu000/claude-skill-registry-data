---
name: qfai-run
title: QFAI Run (Change request entry)
description: "Use when the user asks for a change, a fix, an investigation of the codebase, a question about the project or an operation on finished work in plain words and names no stage skill. Plans every such request, the lightest included, with `npx qfai workflow plan` and runs the plan's steps in order to its end."
argument-hint: "<the change, in your own words>"
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash, TodoWrite, Task, Agent]
steps: []
requires: [common-policy-check, common-review-cycle]
mode: execution-focused
---

## /qfai-run - Change request entry

In a git worktree, read and follow the worktree's own `.qfai/assistant/skill/qfai-run/SKILL.md`, whatever copy the host loaded. Follow the CLI plan's steps in order. Read no reference up front; each line says when.

- `references/extraction.md`: for an extraction step 1 does not give.
- `references/plan.md`: for a plan field this file does not name, or a refused plan.
- `references/operator-screens.md`: when a line below or a step names it, such as to ask or report.
- `references/stage-points.md`: at a step the plan marks with a point.
- Run the launcher preflight before planning, `--order` included. When this checkout has `node_modules/.bin/qfai` and no merge since its install changed the lockfile or `package.json`, it passes and `npx qfai` (or `node_modules/.bin/qfai` when PATH reachability is uncertain) is the launcher; read nothing more for it.
  Otherwise, as for a Plug'n'Play project, read `.qfai/assistant/rule/references/launcher-preflight.md`. If the launcher is missing or preflight fails, read `references/operator-screens.md` for recovery.
- Read `references/codex-cloud-install.md` before configuring an environment-owned Install script or Start skill, or preparing dependencies for a fresh checkout. Use the reviewed target's successful preparation and canonical proof before planning.

## What this skill never does

- Choose a route, which the CLI's decision rules take from the extraction, or
  name one, a stage kind or an internal identifier to the user.
- Put request text on a command line. `plan` reads only the extraction.
- Add, drop or reorder a step the plan names, or run a stage outside the scope.
- Push, open a pull request, merge, deploy, migrate production or spend
  money without the user's own instruction or a project policy naming it.

## Mode

Read `workflow.mode` in `qfai.config.yaml` first. No key means `active`; unlisted
values plan nothing.

| Mode     | What this skill does                                                                 |
| -------- | ------------------------------------------------------------------------------------ |
| `active` | The work below                                                                       |
| `shadow` | State what the request asks and why. Write nothing, and say that nothing was written |
| `off`    | Plan nothing. The user invokes the stage skills by name                              |

## Request kinds

- For independent targets under one goal, read `references/operator-screens.md`
  before planning or switching during a wait.
- Plan changes, questions, proposals to decide and reports to close. Questions plan answers without changes; nonrequests get no plan.
  An automated notice (task, wake-up, CI) is no request; one that delivers a requested result resumes the waiting step.
- Replies with a requested answer or result, including failure, resume the same step without
  a new invocation. An independent new request is planned; read `references/operator-screens.md`
  for replies.
- `stop`: end the work at once and list every open decision as open.
- A request naming a stage skill: invoke that skill by name.

## The work

1. **Extract.** A question one read answers is `{ intent: question-why, qualifiers: [session-answerable] }`
   (or `question-how`, `question-help`); an operation on finished work, or on a device or system the session reaches, that the session runs itself and
   that deletes nothing is `{ intent: order, artifacts: [] }`. Write every other required list field as `[]`, since `plan` refuses an omitted one, with `confidence: high`; neither needs a reference.
   Read any other request as `references/extraction.md` sets out. Then run the launcher preflight above; after it passes, hand the extraction to `npx qfai workflow plan --in <file>`, or `--in -`.
   The session-run operation that deletes nothing, read above as `{ intent: order, artifacts: [] }`, goes to `npx qfai workflow plan --order` instead, with no file; an order read through `references/extraction.md` keeps `--in`.
2. **Candidates.** When `plan` returns `candidates`, put one single-select
   question, each option saying in the user's words what that route will do,
   then run `npx qfai workflow plan --route <route>` with the same `--in` for the chosen one, keeping the candidate's `decisionPoints`.
3. **Scope.** With two or more scopes, ask which to run as `references/operator-screens.md` says,
   and run only its stages. With one scope, no scopes, or a branch destination's plan, ask
   nothing and run every stage.
4. **Announce.** Before the first stage, give the goal, the chosen stages in order in plain words,
   and the files the work may change. Ask nothing. On a route that changes files, a branch destination's included, then search once per run for open work on the same problem
   before any edit, as `references/operator-screens.md` says, and on a match wait for the user. Then run `common-policy-check` once, unless the
   plan's one step is `triage-answer` or `triage-operate`. On a route that changes no file, one that
   closes, answers or asks, it reads and reports and writes nothing.
5. **Run the stages.** Run each stage in plan order, and each of its steps in
   order, as `.qfai/assistant/rule/shared-skill-operating-baseline.md#running-steps` says.
   Note each step's status for the final report; when a step is short or passes without edits, read `references/operator-screens.md`.
   Do the work and write every artifact yourself. Start a sub-agent only for the two reasons the delegation baseline states: an independent judgement, or parallel units that pass the parallel-unit gate. A worker starts no finder, griller or reviewer: run each step that starts one yourself, as the delegation baseline's Session Agent Protocol says.
   At a step the plan marks with a point, follow `references/stage-points.md`:
   - **Release point.** Ask the user to approve the release before the step `releasePoint` names.
   - **Decision point.** Put each critical decision at a step `decisionPoints` names to the user.
   - **Branch point.** Move to the destination a step `branchPoints` names, and plan it at once.
6. **Review.** After a stage whose `review` is `spec`, `requirements-reviewer` reviews; for `code`,
   `implementation-reviewer`. Only a contract or screen change no earlier review read adds
   `architecture-reviewer` or `product-surface-reviewer`, as `common-review-cycle` lists; no one else
   joins. A review whose target's only edits resolve the conflicts of a merge or branch update between
   reviewed sides, or a route code review of a small literal-only change, as `common-review-cycle` defines, gets no reviewer. A conflict resolution the plan's own edit stage made in the story tree, a contract or a register still gets one.
   No agent reviews its own work; no step adds a review. Each returns PASS or REVISE.
   Fix or answer each finding once; a behaviour fix gets one re-review, as `common-review-cycle` says. Stop a step that exceeds the request.
7. **Approvals.** An approval of a critical decision or a release is one `decisions.md` row only when it is hard to reverse, would surprise a reader without context, and was the result of a real trade-off:
   what was approved, who approved it, when, and the chosen option's label, in the `qfai-sdd` decisions template's short form. Otherwise the final report states the approval with the same items. A decision you took appends no row.
   When the release change is produced outside this run (by a release workflow or bot), record its approval in the final report in the same short form, and, when it is to be a row, list the row as a pending follow-up;
   the next change that touches `decisions.md` appends the row, and a `qfai-run` that writes `decisions.md` appends any pending approval row first.
8. **A finding no stage serves.** Stop, and name the finding, its owner and the stage skill to invoke by name.
9. **Commit.** `verify-commit` runs last, after any release point; never pushes. A push, pull request, merge or branch update the user asks for after the plan ends is planned next as `{ intent: order, artifacts: [] }` with `npx qfai workflow plan --order`, and its `triage-operate` delivers it.
10. **Session feedback.** When the final report closes the user's last task and nothing waits on them, follow `.agents/rules/session-feedback.md` once.

## Under a no-question mode

Nothing is asked. The plan's narrowest scope, or the first candidate and its narrowest scope, is taken and reported as an assumption.
An open-work match is taken as continue and listed first in the report as an assumption. An uncovered question-only move to tracked-file repair instead stops that target
with a report and no tracked open question, as `references/stage-points.md` says.
A critical decision or a release point becomes one `open-questions.md` row,
the step stops before the change that depends on it, and the report lists the
decision as open. A third branch move, or one from a scope that leaves stages out, stops the work.

## User Questions (AskUserQuestion Protocol)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.

## Inputs Priority

- P1: `.qfai/assistant/rule/*`
- P2: the plan `npx qfai workflow plan` returns
- P3: the story tree under `<paths.specsDir>` and the contracts under `<paths.contractsDir>`
- P4: the user's request

## Sub-agent Delegation

Follow `.qfai/assistant/rule/shared-skill-delegation-baseline.md`.

## Work Orders Summary

When parts ran in parallel, use the summary in `references/operator-screens.md`.

## Default Autopilot Policy

- auto-decide:
  - output formatting
  - equivalent-option pick
- ask-user:
  - each critical decision at a decision point, and each release point
  - the candidate question, the scope question, a third branch move, any branch move from a narrower scope, and an open-work match
- hard-required:
  - change request (the user's own words; an empty request is asked for, never guessed)

## Completion Contract (Shared)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#completion-contract-shared`. **Smallest applicable smoke check**: the chosen scope's `verify-qfai-gate` and `verify-repo-gate` gates. With none, run no gate and report it. Unavailable gates are UNRUN, never PASS.

At stage boundaries, follow `references/reached-step-observations.md` in the existing report.

If requested evidence handover must precede archive, read `references/evidence-delivery.md`
and complete receiving proof first. Missing access leaves handover pending and originals
retained; ordinary completion requires no unsolicited upload.

project_memory:

- The user names no stage after the first request.
- The plan is fixed by its route and the extraction's artifacts; the session runs every step of the chosen scope.

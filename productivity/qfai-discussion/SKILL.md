---
name: qfai-discussion
title: QFAI Discussion (Exploration Planner)
description: "Use when invoked by name or handed a QFAI work order. Its subject is a product idea or problem whose scope is not settled yet."
argument-hint: "<idea-or-problem> [--auto]"
allowed-tools: [Read, Glob, Write, TodoWrite, Task, Agent, Bash]
steps: [discussion-research, discussion-interview]
requires: []
mode: interactive-by-default
---

## /qfai-discussion - Exploration Planner

Run the entry check of
`.qfai/assistant/rule/shared-skill-operating-baseline.md#workflow-run-entry-check`
first.

Interviews the user about a product idea or problem and keeps what was asked
and answered in the run's deliberation record, so `/qfai-sdd` can write the
story tree from it. The record is a memo, written as
`.qfai/assistant/rule/references/deliberation-record.md` says.

## User Questions (AskUserQuestion Protocol)

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.

## Inputs Priority

When unsure, read inputs in this order:

- P1: `.qfai/assistant/rule/*`, and `.qfai/assistant/skill/qfai-grilling/SKILL.md` before the interview
- P2: `.qfai/assistant/rule/agent-selection.md`, the cards under `.qfai/assistant/agent/`, and project context under `<paths.specsDir>/01_policy/**` and `<paths.contractsDir>/**`
- P3: what the project already settled (`qfai.config.yaml`, `<paths.specsDir>/decisions.md`, `<paths.specsDir>/open-questions.md`, `<paths.specsDir>/02_business-flow/**`, and `<paths.contractsDir>/**`)

## Steps

Run the steps in this order, as
`.qfai/assistant/rule/shared-skill-operating-baseline.md#a-parent-skill-invoked-by-name`
states: read `.qfai/assistant/step/<id>/STEP.md` for the current step only, run
it, then move to the next. A work order runs the steps it names, as
`.qfai/assistant/rule/shared-skill-operating-baseline.md#a-plans-steps`
states.

| Step                   | File                                                | Runs                                                  |
| ---------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| `discussion-research`  | `.qfai/assistant/step/discussion-research/STEP.md`  | Always, first                                         |
| `discussion-interview` | `.qfai/assistant/step/discussion-interview/STEP.md` | Always: concept, scope, stakeholders, and constraints |

An interview that ends `stopped` ends the run: no later step runs, and every
open decision is reported as open.

## What the stage writes

The run's deliberation record, and one `<paths.specsDir>/open-questions.md`
row for each question the stage left open. Nothing else: no other story-tree
file, no policy file, no contract and no root `DESIGN.md`. A brand theme the
user chose is an Interview row of the record; `/qfai-sdd`'s `common-design-md`
step writes `DESIGN.md` from it later.

## Review

None. The output is a memo, so the skill runs no review after its last step,
invoked by name or in a route.

## Completion

Invoked by name, the skill ends after `discussion-interview`: that step
commits locally only the run's deliberation record and the `open-questions.md`
rows the run wrote, and pushes nothing. The report names the record's path, or
says the run wrote no record.

## Completion Message & Next Actions

End the turn with a question listing the next actions, `/qfai-sdd` recommended, as `.agents/rules/user-questions.md` § 6 sets out. Under a no-question mode, list them in the report instead.

## Default Autopilot Policy

The entries below govern the default user interview. Only an actual user
delegation recorded under
`.agents/rules/grilling.md#explicit-delegation-for-a-discussion` enables the
delegated `adopted` path. No-question mode alone does not enable it; missing
inputs and uncovered human decisions retain their ordinary blocking behavior.

- ask-user:
  - every decision the interview puts on the frontier, over every topic in `references/discussion-coverage-checklist.md`. Running the interview is what this skill performs, so these are its own operations
  - the confirmation that closes the session
- hard-required:
  - a usable requirement source
  - an identifiable affected BF or an explicit decision to create one

project_memory:

- The stage writes the run's deliberation record and its `open-questions.md` rows, and nothing else.
- Root DESIGN.md is not a discussion output: `/qfai-sdd`'s `common-design-md` step authors it.
- Discussion is planner-first: never pick a single visual winner; carry exploration references as deviate-from inputs, not imitate-this.

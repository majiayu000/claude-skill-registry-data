---
name: qfai-maintain
title: QFAI Maintain (Non-normative edits)
description: "Use when invoked by name or handed a QFAI work order. Use it for a change to wording, a typo, a code comment or document prose that is meant to change no behaviour."
argument-hint: "<the text or comment to change>"
allowed-tools: [Read, Glob, Grep, Write, Edit, Bash, TodoWrite, Task, Agent]
steps: [maintain-edit]
requires: [common-review-cycle]
mode: execution-focused
---

## /qfai-maintain - Non-normative edits

Run the entry check of
`.qfai/assistant/rule/shared-skill-operating-baseline.md#workflow-run-entry-check`
first.

## Inputs

- The text or comment to change, and the write scope the request or the work
  order gives.
- `.qfai/assistant/rule/*`.
- Before an agent decision, search the records for a turned-down option, as
  `.qfai/assistant/rule/references/deliberation-record.md` says.

Questions to the user follow
`.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`.

## Steps

- `maintain-edit` makes the edit inside the write scope, or stops before an
  edit with a semantic effect.

Run the steps as
`.qfai/assistant/rule/shared-skill-operating-baseline.md#running-steps`
sets out: read `.qfai/assistant/step/<name>/STEP.md` for the current step only,
run it, then the next. No step is skipped.

## Review

After the last step, run one review through `common-review-cycle`: the code
review, by `implementation-reviewer`. The reviewer rules on the
diff and on the no-behaviour-change judgement, and never reviews an edit it
made. A REVISE sends the finding back to the step's author.

### Reviewer Gate

An edit that would change a story, a contract or a decision is not this
skill's, and stops.

## Completion

Follow `.qfai/assistant/rule/shared-skill-operating-baseline.md#completion-contract-shared`.
**Smallest applicable smoke check** (this skill's override): the project's
Markdown and link checks run over the changed files, each exiting 0. A check the
project does not have is UNRUN, not a pass.

The stage returns what `maintain-edit` lists under "What the stage returns".
Ask for the next action only when proceeding requires the user's answer, as
`.agents/rules/user-questions.md` § 6 sets out. A completion-only report needs
no question. Under a no-question mode, list any remaining actions instead.

## Default Autopilot Policy

- hard-required:
  - edit target (the text or comment to change; an empty target is asked for, never guessed)

project_memory:

- A maintenance edit changes what a reader reads, never what a program or an agent does.
- A semantic effect found before an edit stops the edit; in a run it blocks the run, naming the owner skill.
- The reviewer of the diff is never the agent that made it.

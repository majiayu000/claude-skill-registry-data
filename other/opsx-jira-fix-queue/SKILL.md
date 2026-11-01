---
name: opsx-jira-fix-queue
version: "2.1.0"
user-invocable: true
category: development
tags: [jira, openspec, batch, workflow]
description: "Triggers when the user says「opsx 批量修复」「批量 opsx-jira-fix」「opsx-jira-fix-queue」「opsx-jira-fix-batch」「批量 OpenSpec Jira 修复」/ opsx batch fix, batch OpenSpec Jira fix, opsx-jira-fix-queue, opsx-jira-fix-batch. Thin trigger shell: parse Jira IDs/URLs and enqueue them into goal-driven-queue with Engine opsx-jira-fix-workflow. Does not run fixes or merge. Do NOT use for a single issue (opsx-jira-fix-workflow) or a non-Jira queue (goal-driven-queue)."
dependencies:
  - goal-driven-queue
---

# OPSX Jira Bug Queue Enqueue Shell

> Trigger-only shell. Queue lifecycle, relationship pass, isolation, caps, and acceptance live in `goal-driven-queue`. This skill parses a Jira list and hands it to that skill's **Jira list-enqueue shortcut** with `Engine: opsx-jira-fix-workflow` already frozen.
>
> Related-issue persistence in OpenSpec `design.md` is the **child engine's** job after dispatch (`opsx-jira-fix-workflow` receives relationship-pass notes in the card supply). This shell does not write OpenSpec artifacts.

**Activate only when the user explicitly requests an OPSX batch Jira fix.** Loading this skill MUST NOT start a queue run.

## Prerequisite Skill Check

Scan available skills. If `goal-driven-queue` is missing, abort immediately with install guidance (`npx skills add FuDesign2008/open-skills -g --skill goal-driven-queue --yes`). No silent fallback.

## Duties

1. Split the input into distinct Jira IDs/URLs.
2. Load `goal-driven-queue` and run its **Jira list-enqueue shortcut** with `Engine: opsx-jira-fix-workflow` frozen on every card.
3. Stop when that shortcut stops (cards written, one batch approval event). Do not start consumption. Do not call `opsx-jira-fix-workflow`. Do not write a parallel progress file.

## Red Flags

- Looping `opsx-jira-fix-workflow` from this skill
- Starting the queue because the list was parsed
- Sharing one OpenSpec change or one branch across in-progress cards (the queue forbids that)
- Re-implementing relationship detection here

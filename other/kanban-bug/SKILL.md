---
name: kanban-bug
description: 'Kanban bug workflow — triage and document a defect with reproduction, expected/actual result, severity, root cause and regression coverage before handing off to kanban-plan. Use when a work item has kind: bug.'
---

# Kanban Bug — Triage and fix a defect

Argument: `<bug_name>`.

A bug goes through the same state machine and approval gate as a feature, but Phase 1 must record enough to reproduce it and to stop it coming back.

## 1. Verify

```bash
kf status --change {bug_name}
kf show {bug_name}
```

Only use this skill when the metadata says `kind: bug` and the work item is in `brainstorm`. If the bug is already in `planning`, `backlog`, `implementation`, `testing` or `review`, resume the matching skill; do not recreate artifacts.

## 2. Triage contract

Read and fill `phase-1-spec-requirement.md` using the bug template (`kf instruct spec-requirement --change {bug_name}`):

- Severity and the affected environments.
- Reproduction steps that are deterministic enough to follow.
- Actual result and expected result.
- What the fix covers and what it does not, plus acceptance criteria for the behaviour a regression must protect.
- Suspected root cause when there is evidence for one; when there is not, say it is undetermined.
- Regression test strategy and acceptance criteria that can be checked.
- The related feature when you can identify it, and the docs impact: which file needs changing and why, or that no docs change is needed.

- **Sibling entry points**: list what else reaches the broken code. Review will ask which of them the fix covers, so naming them here is cheaper than discovering them later.

Do not guess a root cause to make the report look finished. If you cannot reproduce it, report the blocker plainly and never assume the bug is PASS.

Write the reproduction so someone else can run it and watch it fail. Review re-runs it rather than trusting the report, so steps that only work on your machine come back as a finding.

## 3. Human confirmation

Summarise the bug, its severity, the reproduction, the impact, the expected fix and the regression test for the user. Only once the user confirms do you set the frontmatter to `status: confirmed` and run:

```bash
kf stage {bug_name} planning
```

Then load `kanban-plan` on its bug branch. The bug report is the execution contract: do not create an implementation plan, a use-case index, narratives, a diagram, a test plan or a feature report. Planning still needs human approval, and the user still chooses start or backlog.

## 4. Handoff

```text
Bug report confirmed. Load kanban-plan on the bug branch to approve the triage contract and ask start or backlog; keep the reproduction and the regression test inside the approved scope.
```

A FAIL or a REJECT, in testing or in review, sends the item back to implementation. `REQUIREMENT_BUG` still stops for the user to decide; do not use it in place of a bug report.

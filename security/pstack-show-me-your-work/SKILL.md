---
name: pstack-show-me-your-work
description: "Keep a concise, append-only decision and evidence trail for long or multi-phase work. Use when the user needs to audit choices, pivots, verification, or a handoff later."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/show-me-your-work
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Show me your work

Log consequential decisions and checkpoints, not every command.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## One local trail

Use an existing trail when present or create a task-owned TSV in the designated scratch/output location. Keep it outside publication unless explicitly included in the delivery. Separate concurrent writers by file; reconcile under one owner.

Use these columns:

| Column | Value |
| --- | --- |
| ts | ISO 8601 timestamp |
| run | Actual chat/run identifier, or a declared local identifier |
| phase | Workstream or checkpoint |
| decision | Concrete action or choice |
| why | Reason for the choice |
| evidence | Resolving path, source location, SHA, result artifact, or link |
| result | Observed result or explicit unverified status |

Replace tabs and line breaks within cells. Prefix cells beginning with =, +, -, or @ with an apostrophe when the TSV may be opened in a spreadsheet. Keep secrets out of the trail.

## Append and audit

Append at the decision: chosen fork, completed unit, failed check, reverted attempt, changed hypothesis, or blocker. A correction appends a superseding row identifying the original; it does not rewrite history.

A new run records its start and inherited state. Read existing rows before resuming and verify only claims that matter to the next action. Audit your own rows against the transcript or direct artifacts. State when transcript access is unavailable.

An authorized independent reviewer can inspect weak evidence, skipped verification, or scope drift using the active chat model. Sequential self-review is disclosed and does not claim independence.

## Deliver

Link the preserved trail and name the decisions or gaps the user should inspect. Do not say reviewed, tests passed, or deployed without evidence supporting that exact event and version.

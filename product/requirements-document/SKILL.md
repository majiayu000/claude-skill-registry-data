---
name: requirements-document
category: pm
description: Use when a product decision or feature needs a written record - what to capture in a task document (PRD, decision record) and where to attach it, since TaskTrooper has no epic
---
# Requirements Documents

## Overview

Some decisions and specs are too big for a task description and need a durable document. The failure mode is either not writing one (decisions get lost) or attaching PRDs to every subtask (noise).

**Core principle:** TaskTrooper has no epic. One document on the analiz task a feature goes through; task descriptions carry the per-task detail for small direct work.

## Use add_task_document for

- **PRDs:** context, goals, user stories, AC, out of scope, non-goals with rationale, open questions.
- **Wireframe notes / API contract drafts** before development.
- **Decision records** for significant product choices (what, why, alternatives rejected).

## Where it lives

TaskTrooper has no epic/parent task type. For a feature that goes through analiz, attach the PRD to the **analiz task** with `add_task_document`. Every implementation task the architect derives from it carries `derived_from: ["A-N"]`, which is how `list_task_documents A-N` reaches the developer working that task. For small direct work with no analiz, the task's own `description` is the PRD — don't open a document for it.

## Structure

```
## Context        — the problem, who has it, why now
## Goals          — measurable outcomes
## User Stories   — As [persona], I want [capability], so that [outcome]
## Acceptance Criteria — observable, per acceptance-criteria-gwt
## Out of Scope   — explicitly excluded
## Non-Goals      — deliberately not solved here, with the reason
## Open Questions — tagged blocking/non-blocking and who answers; only genuinely open ones — never a question you can answer from context
```

## Worked Example

A "Reporting v1" analiz task gets one PRD via `add_task_document` on the analiz task itself: context (boards are opaque past 200 tasks), goals (3 reports), user stories, AC per report, out of scope (exports, scheduling), non-goals (a BI tool — rationale: no usage data locally to justify it), open questions (retention window — blocking, needs the stakeholder). The implementation tasks the architect creates carry `derived_from: ["A-N"]`; they don't each re-attach the document.

## Common Mistakes

- No document for a significant decision → it's lost in comments.
- A PRD re-attached to every implementation task instead of living once on the analiz task → noise.
- Missing "Out of Scope" / "Open Questions" → scope creep and hidden unknowns.
- An "epic" or "parent task" in your plan — the type doesn't exist; use an analiz task.

## Red Flags

- A big product choice with no decision record.
- The same document attached to five tasks.

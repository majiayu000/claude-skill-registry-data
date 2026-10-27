---
name: ralph-feedback-batch-protocol
description: Ralph-v2 post-iteration feedback batch protocol for creating feedback directories, authoring feedbacks.md, and advancing a session into replanning. Use when processing human feedback after an iteration or resuming Ralph from feedback artifacts.
---

# Ralph Feedback Batch Protocol

Use this skill when a Ralph-v2 workflow is at rest and a human provides structured feedback for a new iteration.

## Directory Layout

Feedback batches live at:

`.ralph-sessions/<SESSION_ID>/iterations/<N+1>/feedbacks/<yyyyMMdd-HHmmss>/`

Artifacts such as logs or screenshots should be stored beside `feedbacks.md`.

## `feedbacks.md` Template

```markdown
---
iteration: <N+1>
timestamp: <ISO8601>
previous_iteration: <N>
---

# Feedback Batch: <timestamp>

## Critical Issues
- [ ] **ISS-001**: Description
  - Evidence: app.log, lines 45-60
  - Suggested Fix: ...

## Quality Issues
- [ ] **Q-001**: Description

## New Requirements
- Feature X

## Artifacts Index
| File | Description |
|------|-------------|
| app.log | Server logs |
```

## Orchestrator Transition Rules

When feedback is detected for iteration `N+1`:

1. Record `PREVIOUS_STATE = metadata.yaml.orchestrator.state`.
2. Set `iteration = N+1`.
3. Update `metadata.yaml`:
   - `orchestrator.state: REPLANNING`
   - `orchestrator.previous_state: <PREVIOUS_STATE>`
   - `iteration: <N+1>`
4. Enter the replanning workflow.
5. Let Planner decide whether to take the `knowledge-promotion` fast path or the full replanning pipeline.
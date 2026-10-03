---
name: workflow-to-issues
description: Use when the user asks to break an approved PRD or plan into implementation issues.
---

# Workflow To Issues

This skill wraps the Matt Pocock `to-issues` phase.

## Required Flow

1. Read `.agents/skills/to-issues/SKILL.md`.
2. Checkpoint the run to `current_skill=to-issues`.
3. Draft tracer-bullet vertical slices.
4. Quiz the user on granularity and dependencies.
5. Publish only after approval.

Do not create issues before approval. Do not create horizontal layer slices.

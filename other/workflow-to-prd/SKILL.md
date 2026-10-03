---
name: workflow-to-prd
description: Use when the user asks to turn agreed workflow context into a PRD.
---

# Workflow To PRD

This skill wraps the Matt Pocock `to-prd` phase.

## Required Flow

1. Read `.agents/skills/to-prd/SKILL.md`.
2. Confirm grilling has reached shared understanding.
3. Checkpoint the run to `current_skill=to-prd`.
4. Synthesize from existing context and repo inspection.
5. Check testing seams with the user before treating the PRD as ready.

Do not interview from scratch. Do not publish external issues unless explicitly
asked.

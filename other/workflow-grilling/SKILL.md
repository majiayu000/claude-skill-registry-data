---
name: workflow-grilling
description: Use when a tracked workflow is in grilling or needs one context-aware question before PRD, issues, implementation, or review.
---

# Workflow Grilling

This skill wraps the Matt Pocock `grilling` phase.

## Required Flow

1. Read `.agents/skills/grilling/SKILL.md`.
2. Confirm the tracker run is `current_skill=grilling`.
3. Ask exactly one context-aware question.
4. Include your recommended answer with that question.
5. If the answer is discoverable from repo files, read the files instead of
   asking.

Do not ask multiple questions. Do not implement. Do not move phases until the
user explicitly confirms shared understanding or asks for the next phase.

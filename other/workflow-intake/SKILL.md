---
name: workflow-intake
description: Use when workflow state must be created, locked, resumed, or repaired before asking the user a workflow question.
---

# Workflow Intake

Use this skill to create durable tracker state before conversation continues.

## Required Flow

1. Read `AGENTS.md`, `skills/control-repo-manager/SKILL.md`, and the relevant
   repo skill under `skills/<skill-id>/SKILL.md`.
2. Read `.agents/skills/grilling/SKILL.md`.
3. Run tracker status internally with `node scripts/control-repo.mjs
   tracker-status`.
4. Create or lock a tracker session and workflow run internally.
5. Write or attach a context manifest under `ops/workflow-runs/` proving the
   ECC files, repo skill, tracker files, and Matt Pocock phase file were loaded.
6. Checkpoint the run to `current_skill=grilling`.
7. Hand off to `skills/workflow-grilling/SKILL.md`.

Do not ask the user to run commands. Do not use Python. Do not implement during
intake.

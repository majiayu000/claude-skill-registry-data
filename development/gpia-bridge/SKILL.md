---
name: gpia-bridge
description: Bridge Codex requests to the local GPIA system. Use when the user invokes /GPIA, asks to hand off a task to the GPIA agent, or needs PASS protocol execution, capsule tracking, or GPIA-specific runs (quick/analyze/create).
---

# GPIA Bridge

Use this skill to route tasks from Codex to the local GPIA agent in this repo.

## Quick start

- For a single task, run:
  `python skills/automation/gpia-bridge/scripts/run_gpia_task.py --task "<task>"`
- For a specific mode:
  - `--mode quick` (no PASS protocol)
  - `--mode analyze`
  - `--mode create`
  - `--mode full` (default, PASS protocol)

## Workflow

1) Confirm the user wants GPIA (look for `/GPIA` or a direct handoff request).
2) Execute the task via `run_gpia_task.py` unless the user asked for interactive mode.
3) Return the GPIA response, capsule id, and pass/assist counts.
4) If GPIA returns a PASS-style block in the response, summarize the missing needs and ask the user how to proceed.

## Interactive mode

If the user wants a live session, launch:
`python gpia.py`
Then use the GPIA commands (`/status`, `/quick`, `/analyze`, `/create`, `/capsule`, `/capsules`).

## Notes

- GPIA uses local models via `configs/models.yaml` and the skill index in `skills/INDEX.json`.
- Rebuild the index after adding skills: `python skills/system/skill-indexer/scripts/index_skills.py`.

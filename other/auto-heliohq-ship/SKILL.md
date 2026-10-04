---
name: auto
version: 0.1.0
description: >
  Run Ship's full production workflow from raw requirement to PR: design, dev,
  E2E, review, QA, refactor, and handoff. Use only for explicit /ship:auto,
  auto pipeline requests, or end-to-end delivery.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# Ship: Auto

Full staged workflow for explicit end-to-end production delivery.

## Execution

Your cwd is the user's repo, not the plugin — a bare relative path will
not find the orchestrator. Set `SKILL_DIR` to this skill's base
directory (announced as "Base directory for this skill" when the skill
loaded), then run the shared stage-aware orchestrator:

```bash
SKILL_DIR="<base directory from the skill invocation>"
SHIP_ORCH="$SKILL_DIR/../../scripts/auto-orchestrate.sh"
if [ -f .ship/ship-auto.local.md ]; then
  bash "$SHIP_ORCH" resume
else
  bash "$SHIP_ORCH" init '<user requirement goes here>'
fi
```

Then follow the `/ship:auto` dispatch loop: read `PROMPT_FILE`, dispatch the
agent, classify the report card, and call `complete <PHASE>`.

## Standalone Skill Boundary

`/ship:auto` is only for full end-to-end runs. For a single phase (design, dev,
E2E, review, QA, refactor, handoff), invoke that `/ship:*` skill directly
instead of routing through auto.

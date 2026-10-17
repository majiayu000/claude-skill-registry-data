---
name: revert-on-extended-red
description: When stuck in red for >5 turns or >3 failed runs without progress, propose reverting the latest production-code edits to restore green and try a smaller step. Use to escape unproductive red sessions.
---

# Revert on extended red

If the orchestrator has been in `red` for more than 5 turns OR more than 3 failed test runs without recovering to green, it has hit `extended-red`. At this point:

1. **Stop editing.** More edits dig the hole deeper.
2. **Read the recent file_edits.** Use `turn_search({ type: "file_edit", since: "<phase-start>" })`.
3. **Propose a revert.** Identify the production-code edits made during this red phase and propose reverting them.
4. **Restart with a smaller step.** Once green is restored, write a *smaller* failing test — one that asserts a less ambitious behavior — and try again.

The orchestrator records the revert decision in a hypothesis explaining why the original step was too large.

## Rules

1. Never delete tests. Reverts target *production-code* edits only.
2. The revert is itself a TDD action: it requires a passing run to confirm green is restored.
3. After reverting, decompose the goal further before retrying. The previous attempt failed because the target was too coarse.

---
name: superctx:sync
description: Use when the user wants to set up, check, repair, or report the SuperCtx state for this repository. Consolidated command for global context convergence.
---

# SuperCtx Sync

Converge this repository into the correct SuperCtx state. `/superctx:sync` is the global setup, check, repair, and report command.

It checks the health of registered shims, initializes candidate repos, repairs missing or broken shims when safe, and reports healthy, repaired, unresolved, and warning states.

## Before Running (Consent Boundary)

1. **Direct User Invocation**: If the user explicitly typed `/superctx:sync` or asked you to sync/repair/setup the repo, you have consent. Announce the action:
   > Using SuperCtx to synchronize and verify project context.
2. **Agent-Initiated Flow**: If you detect a setup opportunity (no `.ctx/` folder but candidate files exist) or shim issues during a task, you **MUST** obtain explicit natural-language user consent before running the command. Use this consent prompt for setup:
   > Using SuperCtx, I can set up one shared context hub for this repo.
   >
   > This will:
   > - create `.ctx/SUPERCTX.md`
   > - back up the original instruction files under `.ctx/sources/`
   > - replace the live instruction files with generated shims pointing to the hub
   >
   > Proceed?

Do not run `/superctx:sync` or make any mutations until you have explicit consent.

## Run

```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}/scripts" python3 -m superctx sync
```

## Then report to the user

Present the output from the command:
- On the **healthy** path (exit 0), confirm concisely that all shims are healthy:
  > All SuperCtx context links are healthy.
- On **initialization** (exit 0), confirm the initialized files, hub location, and any backups.
- On **repair** (exit 0), list the repaired shims.
- On **legacy or inspection warning/stops** (exit 1), explain the warning and explain what needs to be inspected. Do not attempt automatic repair.

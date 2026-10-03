---
name: aries_repair_sweep
description: Run the Aries repair workflow from the repo, then return a concise operational summary for cron delivery.
---

# Aries Repair Sweep

## Use when
Use this skill when asked to run the Aries nightly repair sweep on demand or from cron.

## Launcher entrypoint
The legacy `lobster`/`workflows/openclaw/repair.json` execution path has been removed.
Do **not** invoke legacy workflow files — this skill now runs the Hermes-native repair
path via the execution port.

## Required procedure
1. Call the Hermes execution provider via the standard execution port to run the repair pipeline.
2. If the execution returns an error or non-ok result, fail loudly with the root cause.
3. Return a concise operational summary only.
4. Do not send a separate message with the `message` tool when cron announce delivery is already enabled.

## Response format
Return only:
- `status:` success or failed
- `actions:` short bullet or one-line summary
- `errors:` `none` or the root cause
- `next_step:` `none` or the specific operator follow-up needed

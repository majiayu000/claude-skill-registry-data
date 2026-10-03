---
name: aries_integrations_sync
description: Run the Aries integrations sync workflow from the repo, then return a concise operational summary for cron delivery.
---

# Aries Integrations Sync

## Use when
Use this skill when asked to run the Aries integrations synchronization pipeline on demand or from cron.

## Launcher entrypoint
The legacy `lobster`/`workflows/openclaw/integrations-sync.json` execution path has been removed.
Do **not** invoke legacy workflow files — this skill now runs the Hermes-native integrations
sync path via the execution port.

## Required procedure
1. Call the Hermes execution provider via the standard execution port to run the integrations sync pipeline.
2. If the execution returns an error or non-ok result, fail loudly with the root cause.
3. Return a concise operational summary only.
4. Do not send a separate message with the `message` tool when cron announce delivery is already enabled.

## Response format
Return only:
- `status:` success or failed
- `actions:` short bullet or one-line summary
- `errors:` `none` or the root cause
- `next_step:` `none` or the specific operator follow-up needed

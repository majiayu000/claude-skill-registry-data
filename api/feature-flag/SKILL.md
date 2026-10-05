---
name: feature-flag
description: Add or evaluate a LaunchDarkly feature flag. Use when implementing a new feature behind a flag or checking flag status.
---

# Feature Flag

Manage LaunchDarkly feature flags.

## Adding a new flag

1. Define flag key: `SCREAMING_SNAKE_CASE` → `kebab-case` for LD
2. Add TypeScript constant to `shared/src/feature-flags.ts`
3. Wrap feature in `if (await ldClient.variation('flag-key', context, false))`
4. Document flag purpose and expected removal date

## Checking flag status

List all flags and whether they're enabled: use LD API or `/flags` admin endpoint.

Arguments: $ARGUMENTS — flag name or action (list/add/remove)

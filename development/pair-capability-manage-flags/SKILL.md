---
name: pair-capability-manage-flags
description: "Manages feature flag lifecycle: creation, activation, deactivation, and cleanup. Follows feature-flags guidelines. Idempotent: detects existing flags, shows current state, offers lifecycle actions rather than re-creating."
version: 0.4.1
author: Foomakers
---

# /pair-capability-manage-flags — Feature Flag Lifecycle Manager

Manage feature flags throughout their lifecycle: creation, activation, deactivation, and cleanup. Follows the [feature flags guidelines](../../../.pair/knowledge/guidelines/technical-standards/feature-flags.md) for flag types, implementation patterns, and cleanup strategies.

## Arguments

| Argument | Required | Description                                                                                     |
| -------- | -------- | ----------------------------------------------------------------------------------------------- |
| `$flag`  | No       | Flag name to manage. If omitted, scans for all flags and presents status.                       |
| `$action`| No       | Lifecycle action: `create`, `activate`, `deactivate`, `cleanup`, `status`. Default: `status`.   |

## Algorithm

### Step 1: Read Feature Flag Guidelines

1. **Act**: Read [feature-flags.md](../../../.pair/knowledge/guidelines/technical-standards/feature-flags.md) for:
   - Flag types (Release, Experiment, Ops, Permission)
   - Implementation patterns (boolean, percentage-based, conditional)
   - Lifecycle management and cleanup strategies
2. **Verify**: Guidelines loaded. If not found, use framework-agnostic defaults.

### Step 2: Detect Existing Flags

1. **Check**: Scan the codebase for feature flag patterns:
   - Flag configuration files (e.g., `feature-flags.json`, `flags.yml`, environment variables)
   - Flag SDK usage (e.g., `isEnabled('flag-name')`, `useFeatureFlag()`)
   - Flag service configuration (LaunchDarkly, Unleash, Split, or custom)
2. **Act**: Build a flag inventory with current state per flag:
   - Name, type, status (active/inactive/stale), creation date (if trackable)
   - Files referencing the flag
3. **Verify**: Inventory built.

### Step 3: Route by Action

#### Action: `status` (default)

1. **Act**: Present the flag inventory:

   > **Feature Flag Status:**
   >
   > | Flag | Type | Status | References | Age |
   > |------|------|--------|------------|-----|
   > | [name] | [type] | [active/inactive/stale] | [N files] | [days/weeks] |
   >
   > Stale flags (inactive > 30 days) should be cleaned up.

2. **Verify**: Status reported. No modifications.

#### Action: `create`

1. **Check**: Does `$flag` already exist?
2. **Skip**: If exists → show current state, offer lifecycle actions instead. Do not re-create.
3. **Act**: Ask developer for flag details:
   - Flag name (validate naming conventions from guidelines)
   - Flag type (Release, Experiment, Ops, Permission)
   - Default value (on/off)
   - Scope (global, per-user, percentage-based)
4. **Act**: Generate flag implementation:
   - Add flag to configuration
   - Create wrapper/utility for flag checks (following adopted patterns)
   - Add cleanup reminder comment with expected removal date
5. **Verify**: Flag created and accessible in code.

#### Action: `activate`

1. **Check**: Does `$flag` exist and is currently inactive?
2. **Skip**: If already active → confirm current state.
3. **Act**: Activate the flag (update configuration to enabled).
4. **Verify**: Flag is active.

#### Action: `deactivate`

1. **Check**: Does `$flag` exist and is currently active?
2. **Skip**: If already inactive → confirm current state.
3. **Act**: Deactivate the flag (update configuration to disabled).
4. **Verify**: Flag is inactive.

#### Action: `cleanup`

1. **Check**: Does `$flag` exist? Is it safe to remove (inactive, no active references in critical paths)?
2. **Act**: Present cleanup plan:

   > **Cleanup plan for `$flag`:**
   > - Remove flag from configuration
   > - Remove flag checks from [N files]
   > - Keep the winning code path (flag-on or flag-off behavior)
   >
   > Proceed with cleanup?

3. **Act**: If developer confirms:
   - Remove flag from configuration
   - Remove flag conditionals, keeping the appropriate code path
   - Remove unused imports/utilities related to the flag
4. **Verify**: Flag fully removed. No orphaned references.

## Output Format

```text
FLAG MANAGEMENT COMPLETE:
├── Flag:    [$flag | inventory scan]
├── Action:  [status | create | activate | deactivate | cleanup]
├── Status:  [active | inactive | removed | inventory shown]
├── Files:   [N files modified | 0 (status only)]
└── Result:  [Complete | Confirmed existing | Cleaned up]
```

## Composition Interface

When composed by `/pair-process-implement`:

- **Input**: `/pair-process-implement` may invoke `/pair-capability-manage-flags` with `$action=create` when a task requires feature-flagged code.
- **Output**: Returns flag creation summary. `/pair-process-implement` continues with the flag available.

When invoked **independently**:

- Full interactive flow. Developer manages flags through the lifecycle.

## Graceful Degradation

- If [feature-flags.md](../../../.pair/knowledge/guidelines/technical-standards/feature-flags.md) is not found, provide framework-agnostic patterns: simple boolean flags with environment variables.
- If no feature flag tool is configured, use code-level flags (constants, config files) rather than a flag service.
- If no existing flags are found in the codebase, report empty inventory and offer to create the first flag.
- If cleanup would break active code paths, warn and require explicit developer confirmation.

## Notes

- This skill **modifies files** — it creates, activates, deactivates, and removes feature flag code and configuration.
- **Idempotent**: invoking `create` on an existing flag shows its current state instead of re-creating. Invoking `activate` on an active flag confirms the state. Invoking `cleanup` always requires explicit confirmation.
- **Stale flag detection**: flags inactive for more than 30 days are flagged as stale. Cleanup is recommended but not forced.
- Flag naming conventions should follow the project's adopted coding standards (e.g., `SCREAMING_SNAKE_CASE` for env vars, `camelCase` for code constants).
- Cleanup is the most critical lifecycle phase — leftover flags create technical debt. The `status` action helps identify cleanup candidates.

---
name: check-pr-errors
description: Check logs for errors and warnings in a specific PR. Use when debugging PR issues, investigating failed code reviews, or checking for errors in a pull request.
argument-hint: "<prNumber> <orgId> [--days=N] [--limit=N] [--all] [--legacy] [--env=PATH]"
---

# Check PR Errors

Check logs for errors and warnings in a specific PR.

## Usage

Run the check-pr-errors CLI script with the provided arguments:

```bash
npx ts-node scripts/check-pr-errors.cli.ts $ARGUMENTS
```

## Arguments

- `prNumber` (required): The PR number to check
- `orgId` (required): The organization ID

## Options

- `--days=N`: Number of days to search back (default: 7)
- `--limit=N`: Max number of logs to return (default: 100)
- `--all`: Show all log levels (debug, info, warn, error). Default: only error + warn
- `--legacy`: Also search in legacy collection (observability_logs)
- `--env=PATH`: Path to .env file (e.g., `--env=.env.prod`)

## Examples

```bash
# Check errors for PR #723 in production
/check-pr-errors 723 97442318-9d2a-496b-a0d2-b45fb --env=.env.prod

# Check all logs (not just errors) for PR #701
/check-pr-errors 701 97442318-9d2a-496b-a0d2-b45fb --all --env=.env.prod

# Check with more logs and legacy collection
/check-pr-errors 701 97442318-9d2a-496b-a0d2-b45fb --limit=500 --legacy --env=.env.prod
```

## What it checks

1. **Log errors**: Searches `observability_logs_ts` (and optionally `observability_logs`) for:
   - Logs with level `error` or `warn`
   - Logs with `attributes.error` present
   - Logs with messages containing error-related keywords

2. **Telemetry errors**: Checks `observability_telemetry` for failed operations related to the PR

## Output

The script outputs:
- List of errors/warnings with timestamps, components, and messages
- Stack traces when available
- Failed telemetry operations
- Summary of findings

## How to Respond
- Find the root cause of any errors.
- Look for anomalies.
- Pay close attention to skipped reviews.
- Determine the final status (success, error, or skipped). Keep using the command with `--limit=XX` if needed.


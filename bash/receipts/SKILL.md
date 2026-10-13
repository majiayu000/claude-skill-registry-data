---
name: receipts
description: Run and verify the daily receipt-to-Drive pipeline locally. Scans Gmail for purchase emails, uploads to Google Drive, and emails the configured accounting address.
user_invocable: true
arguments:
  - name: action
    description: "What to do: run (default), verify, dry-run, or backfill YYYY-MM-DD"
    required: false
    default: run
---

# /receipts — Receipt Pipeline

Run the receipt-to-Drive sync pipeline locally and verify results.

## Actions

### `run` (default)
Execute the receipt pipeline for yesterday's purchases.

### `dry-run`
Validate config and secrets without processing any emails.

### `verify`
Check the last run's results — query Gmail for the notification email sent to the accounting address and confirm it was delivered.

### `backfill YYYY-MM-DD`
Run the pipeline for a specific date (useful for catching missed days).

## Implementation

### Step 1: Parse the action

Parse the user's argument to determine which action to take. Default to `run` if no argument.

For `backfill`, extract the date argument (e.g., `backfill 2026-03-05`).

### Step 2: Execute

#### For `run`, `dry-run`, and `backfill`:

Run the shell script which pulls secrets from Vault and executes the pipeline:

```bash
# Normal run (yesterday)
$OUTWORKOS_ROOT/scripts/run-receipts.sh

# Dry run
$OUTWORKOS_ROOT/scripts/run-receipts.sh --dry-run

# Backfill specific date
$OUTWORKOS_ROOT/scripts/run-receipts.sh --date 2026-03-05
```

After the script completes, parse the JSON log output and report:
- Number of receipts scanned, uploaded, skipped, failed
- Drive folder URL (if receipts were uploaded)
- Whether the notification email was sent

#### For `verify`:

Look up the accounting email address from `user_profiles.accounting_email` or `outworkos.config.yaml`, then use Google Workspace Gmail search to find the most recent "Daily Receipts" notification:

1. Search Gmail for: `to:{ACCOUNTING_EMAIL} subject:"Daily Receipts" from:{USER_EMAIL}` (limit to last 7 days)
2. Read the most recent match
3. Report:
   - Date of last receipt email
   - Whether receipts were found or it was a "no receipts" confirmation
   - Drive folder link (if included)
   - Any gaps in daily coverage (missing dates in the last 7 days)

### Step 3: Report

Provide a concise summary:

**Run/Backfill success:**
> Receipt sync complete for {date}: {N} receipts uploaded to Drive.
> Notification sent to {ACCOUNTING_EMAIL}.
> Drive folder: {url}

**Dry-run success:**
> Config valid. All 4 Vault secrets loaded successfully. Pipeline ready.

**Verify result:**
> Last receipt email: {date} — {N} receipts ({vendor list})
> Coverage: {dates covered} | Gaps: {any missing dates}

**Failure:**
> Receipt sync failed: {error details}
> Suggested fix: {actionable suggestion}

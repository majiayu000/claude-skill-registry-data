---
name: audit-flush
description: Inspect and flush staged audit-trail entries to the remote trail repository. Use when the user asks to "flush audit trail", "show what's pending in audit trail", "dry-run audit flush", "retry audit pending", or when diagnosing why a previous auto-flush was skipped (secret hit, push failure, manual mode).
license: MIT
allowed-tools: Bash, Read
---

# audit-flush

Manual counterpart to the Stop hook. Same logic, invoked on demand.

## When to use

- The user asks to inspect staged trail entries before they auto-flush.
- The user wants to retry entries that moved to `$CCAUDIT_PENDING_DIR` after an earlier failure (secret hit or push error).
- Auto-flush is disabled (`CCAUDIT_MANUAL=1`) and entries must be flushed explicitly.
- The user needs a written record that "<user> inspected and approved this flush at time X" — running `/audit-flush` leaves a trace (the commit author and timestamp) that an unattended Stop hook cannot.

## Flags

| Flag | Behavior |
|------|----------|
| *(none)* | Same flow as `hooks/auto-flush.sh`: scan, secret-check, push, clear staging. |
| `--dry-run` | List what would be flushed, exit without touching anything. |
| `--force` | Include `$CCAUDIT_PENDING_DIR` contents in addition to staging; retry everything. |

## Procedure

Follow `skills/audit-flush/procedure.md` step by step. Do not invent additional safety checks — the hook and this skill must stay behavior-identical, so divergence creates undefined state.

## What this skill does NOT do

- It does not modify trail entries. Entries are append-only once written to staging.
- It does not delete from the remote trail repository. If a bad entry was pushed, the correction is a new entry referring to the bad one by hash — never a rewrite.
- It does not reconfigure the remote. `CCAUDIT_TRAIL_REPO` is read-only from this skill's perspective.

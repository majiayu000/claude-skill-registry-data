---
name: progress-summary-sync
description: Sync the Progress Summary counts in PROGRESS.md with the canonical Phase/TODO/Subtask sections; use after adding or updating TODOs/subtasks when the summary becomes stale.
---

# Progress Summary Sync

## Overview

Update the Progress Summary block in PROGRESS.md so its counts match the canonical Phase/TODO/Subtask sections.

## Quick start

- Update in place:
  - `python3 scripts/sync_progress_summary.py --path /path/to/PROGRESS.md`
- Check only (no changes):
  - `python3 scripts/sync_progress_summary.py --path /path/to/PROGRESS.md --check`

## Workflow

1. Run the script with `--check` to see if the summary is out of date.
2. Run without `--check` to update PROGRESS.md in place (atomic write).
3. Review the diff to confirm counts and status mapping.

## Script behavior

- Parses phase sections using the `PHASE <n>:` headings.
- Counts TODO blocks and SUB task checkboxes; reads TODO status from the `**Status**:` line in each TODO block.
- Rewrites only the Progress Summary block (the section titled "Progress Summary" up to the next header).
- Leaves the canonical plan and plan-manager JSON untouched.

## Resources

### scripts/

- `sync_progress_summary.py`: Recompute and rewrite the Progress Summary counts.

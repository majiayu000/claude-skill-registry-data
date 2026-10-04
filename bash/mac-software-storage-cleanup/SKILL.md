---
name: mac-software-storage-cleanup
description: Use when auditing macOS app storage, cleaning priority caches, or recommending reclaimable disk space.
---

# Mac Software Storage Cleanup

## Overview

Audit installed software and storage usage on macOS, produce prioritized cleanup recommendations, and execute low-risk cleanup only after confirmation. The skill separates app inventory, cache cleanup, simulator data, and medium-risk application data so destructive actions remain explicit and reversible where possible.

## When to Use

Use this skill when the user:
- Wants to inspect software installed under `/Applications`, `~/Applications`, Homebrew Formula, or Homebrew Cask
- Wants storage usage ranked by size across apps and common cache locations
- Wants to clean low-risk paths such as `~/Library/Caches` and `~/Library/Developer/CoreSimulator`
- Wants reclaim recommendations with low-risk and medium-risk cleanup separated clearly

## Do not use

Do not use this skill when:
- The user wants to uninstall one specific app instead of doing storage governance
- The user asks to delete application data directly without explicit confirmation
- The environment is not macOS or the target paths do not apply

## Instructions

1. Run `scripts/report_sizes.sh` first to inventory install sources and major storage consumers.
2. Classify cleanup candidates by priority:
   - Priority 1: caches and simulator data, generally low risk.
   - Priority 2: application data directories, report only and never delete by default.
   - Priority 3: low-yield small caches or logs.
3. Reports must show category totals, counts, and Top N largest entries.
4. To inspect priority-2 candidates, run `scripts/list_priority2_candidates.sh [target_dir] [TopN]`.
5. Only after explicit user confirmation, run `scripts/cleanup_priority1.sh` or an equivalent low-risk cleanup action.
6. After cleanup, recompute usage and show a `before -> after -> reclaimed` summary.

## Workflow

```text
Inventory install sources and storage usage
  -> identify high-value cleanup targets
  -> present prioritized recommendations
  -> wait for user confirmation
  -> run low-risk cleanup
  -> verify reclaimed space
```

## Run commands

```bash
bash scripts/report_sizes.sh
bash scripts/list_priority2_candidates.sh ~/Library/Application\\ Support 20
bash scripts/cleanup_priority1.sh
```

## Output requirements

- Show counts and total size for each path category
- List Top N largest consumers so the user can decide quickly
- Every cleanup action must include before-and-after comparison
- Do not delete priority-2 directories without explicit user approval

## Boundaries

- Do not use destructive git commands
- Do not delete unconfirmed application data
- If a script fails, fall back to read-only inspection or the smallest safe cleanup scope

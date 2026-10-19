---
name: dev-disk-report
description: Read-only scan of the home folder for space left behind by development work, rendered as a treemap page that builds a cleanup script from ticked items. Explicit invocation only.
disable-model-invocation: true
---

# Dev disk report

You are a **surveyor**: you measure and report; the user decides and runs the cleanup. Your whole footprint is `~/disk-report/`. Everything else on disk is read through sizes and metadata only (`du`, `stat`, directory names, and tools' own status commands like `docker system df` and `git worktree list`), never through file contents, and nothing is removed.

## 1. Scan

```bash
python3 <skill-dir>/scripts/scan.py            # --min-mb 50 is the default threshold
```

The script is the single source of truth for the run: it reads `~/disk-report/sizes.csv` first, measures, writes `~/disk-report/report.html`, then appends every listed item's size to `sizes.csv`. Done when it prints the `report:` line.

It stays inside the scan boundary by construction: it enters no permission-prompting or private folder (Desktop, Documents, Downloads, Pictures/Photos, Movies, Music, iCloud, Trash, `~/Library` beyond Caches, Application Support and Developer), stays on the home volume, and follows no symlinks. Folders macOS refuses silently come back as `SKIPPED … (protected by macOS)`. If a permission prompt still appears, add the folder's name to `PRUNE_TOP` or `SWEEP_SKIP` in `scan.py` and re-run.

## 2. Open and report

Run `open ~/disk-report/report.html`. Then tell the user, from the script's stdout:

- free space, and the totals for **safe to remove** and **let me review first**;
- every `GREW` line, biggest jump first, or that this was the first run;
- the `NOTE` lines (Docker in use vs reclaimable) and the `SKIPPED` lines, so they know what went unmeasured.

The page is the decision surface. Ticked items become `cleanup.sh` through **Generate cleanup script**: each runs the tool's own clean command, and items with no clean command appear as manual steps that never execute. The user downloads and runs it; your turn ends at the report.

## Changing what gets classified

All classification lives in `scan.py`, so a new tool is a one-place edit:

- `catalog()`: fixed locations, each with a title, kind, consequence, and either a clean command or manual instructions. `entry()` rejects an item with neither, which keeps raw `rm` out of the script.
- `runtime_items()`: installed Node (nvm, minus the default), Python (pyenv), and Rust (rustup, minus the default) versions, one item each with its uninstall command.
- `ARTIFACTS`: per-project build output, recognised by a marker (`node_modules` beside `package.json`). Inside a git repo the command is `git clean -fdX -- <dir>`, which removes only git-ignored files.
- Worktrees come from `git worktree list` on every repo found; `git worktree remove` refuses dirty ones.
- `SWEEP_ROOTS`: big children of `~/.cache`, `~/.local/share`, `~/Library/Caches`, `~/Library/Application Support`, plus top-level `~/.dirs`, that nothing above claims are listed as unrecognised. Give a recurring one a catalog entry.
- `REVIEW_KINDS`: kinds forced into **let me review first**. Sessions, models, Docker, runtimes, device state, worktrees, and unrecognised data stay there; `entry()` asserts it.

`sizes.csv` columns (`scanned_at,id,group,kind,kib`) are the growth history: an item's `id` must stay stable across runs, and changing the columns orphans every earlier scan.

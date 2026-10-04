---
name: vault-janitor
description: Scan a folder tree for accumulated junk (dependency folders, build caches, stray backups, log files, OS litter, duplicate copies) and produce a sized, grouped cleanup report. Report-only by default; it deletes nothing until you approve a specific list, and prefers moving to an archive over hard deletion. Use when the user says "clean up this folder", "what is taking all the space", "find the junk", or "vault cleanup".
---

# Vault Janitor

You find the junk that working folders accumulate: the `node_modules` inside an abandoned experiment, the `_backup_final_v2` nobody remembers making, the 400 MB of logs. You report it with sizes and let the human decide. You delete nothing on your own.

This skill exists because of a real cleanup: a personal vault that had quietly grown to 325,000 files, of which roughly 290,000 were dependency folders, build caches, and nested backups. The scan is the easy part; the discipline is in what happens after, which is why the report comes first and the deleting comes last, if at all.

## Step 1: Scan (read-only)

Take a target folder (default: current directory). Walk it and classify what you find into groups:

| Group | Patterns |
|---|---|
| Dependency folders | `node_modules`, `venv`, `.venv`, `env`, `vendor`, `site-packages` |
| Build caches | `__pycache__`, `.cache`, `dist`, `build`, `.next`, `.parcel-cache`, `*.pyc` |
| Backup litter | folders/files matching `*backup*`, `*_old`, `*_bk`, `* copy`, `*final_v*`, dated duplicates of the same name, `.zip`/`.rar` siblings of an existing folder |
| Logs and temp | `*.log`, `*.tmp`, `*.err.log`, `*.out.log`, crash dumps |
| OS litter | `Thumbs.db`, `.DS_Store`, `desktop.ini` |
| Heavyweights | any single file over 100 MB that fits no group above |

Measure each group: file count and total size. Note the largest individual offenders.

Things that are NEVER junk, regardless of pattern: anything inside a `.git` directory that belongs to a live repo, `.env` files, anything the user's notes or README mark as deliberate, and any folder whose name suggests the user chose to keep it ("dont_delete", "keep", "archive" with a date and intent).

## Step 2: Report

Produce `cleanup-report.md` in the target folder:

1. **Headline numbers**: total files, total size, what percentage the junk groups represent.
2. **Per group**: count, size, and the top 10 paths by size.
3. **Judgment calls**: items that match a junk pattern but might be deliberate (a `backup` folder with recent edits, a zip with no sibling folder). These get a "verify before touching" flag, not a recommendation.
4. **Recommended actions**, most space per least risk first. Dependency folders and caches lead (regenerable by definition); ambiguous backups come last.

## Step 3: Clean (only with an approved list)

Never act on the whole report. The flow is:

1. The user names which groups or paths to clean.
2. Prefer moving to a dated archive folder (or the system recycle bin) over hard deletion. State where things went.
3. Hard-delete only if the user explicitly chooses it, and confirm the exact path list once before running.
4. After cleaning, re-report the headline numbers so the result is visible.

## Rules

- Report-only by default. No file is moved or deleted in a scan.
- Never touch live `.git` repositories, `.env` files, or anything flagged "verify before touching" without the user resolving the flag.
- One folder tree per run. No "clean the whole drive" sweeps.
- If something looks like the only copy of user-created work (documents, designs, photos), it is not junk no matter where it sits. Flag it, never recommend deletion.
- OneDrive and other sync folders: warn that deletions sync to the cloud and other devices before cleaning anything inside one.

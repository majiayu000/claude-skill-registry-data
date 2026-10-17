---
name: workspace-storage-cleaner
description: Audits and purges stale artifacts, nested .git clones in brain session directories, oversized task logs, and temporary files across Antigravity Brain and development workspaces.
---

# Workspace & Brain Storage Cleaner

## Overview

As agent sessions execute, various systems create local storage bloat:
1. **Antigravity Brain**: Subagents or tasks that clone Git repos directly into conversation artifact folders leave behind multi-megabyte `.git` object stores; long-running processes generate multi-megabyte `task-*.log` files.
2. **Project Workspaces**: Stale temporary files (`null`, `*.tmp`, `vault-sync.log`, legacy dream logs) accumulate over time.

This skill provides an automated audit and cleanup tool to safely reclaim disk space without touching active source code, committed files, or active session memory.

---

## Capabilities

1. **Brain Audit & Purge**:
   - Locates nested `.git` folders in inactive conversation directories (`~/.gemini/antigravity/brain/*`).
   - Identifies oversized background task logs (> 2 MB) from completed sessions.
   - Protects the currently running conversation session.
2. **Workspace Audit & Purge**:
   - Removes stray root artifacts (`null`, `vault-sync.log`).
   - Removes redundant installer executables and zip archives.
   - Cleans legacy `.ijfw/logs/` older than 14 days.

---

## Usage

### 1. Audit / Dry-Run (Read-Only)

```bash
python C:\dev\skills\workspace-storage-cleaner\scripts\clean-storage.py
```

### 2. Execute Cleanup

```bash
python C:\dev\skills\workspace-storage-cleaner\scripts\clean-storage.py --apply
```

### Parameters

- `--brain-root`: Custom path to Antigravity brain (defaults to `~/.gemini/antigravity/brain`).
- `--workspace-root`: Path to target workspace (defaults to `C:\dev`).
- `--current-cid`: Active conversation ID to exempt from cleanup.
- `--apply`: When provided, executes deletions; otherwise runs in read-only audit mode.

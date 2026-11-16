---
name: "pre-compact-backup"
description: "Back up conversation transcript before context compaction. Use when: PreCompact hook fires, user asks to save session state, or before long tasks where context loss would be costly. Creates timestamped backup in logs/transcript_backups/. Inspired by: disler/claude-code-hooks-mastery pre_compact pattern."
---

# Pre-Compact Backup Skill

## When to trigger

- PreCompact hook fires (automatic)
- "save session before compact", "lưu transcript"
- "backup context", "sao lưu phiên làm việc"
- Before starting a very long multi-step task

## What to do

### Step 1 — Identify transcript location

Check for `.claude/state/` or default Claude Code transcript paths.

### Step 2 — Create backup

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="logs/transcript_backups"
mkdir -p "$BACKUP_DIR"
# Copy current transcript if accessible
cp .claude/transcript.jsonl "$BACKUP_DIR/transcript_${TIMESTAMP}.jsonl" 2>/dev/null || true
```

### Step 3 — Tag the backup

Write a short metadata file alongside:
```json
{
  "timestamp": "YYYY-MM-DDThh:mm:ssZ",
  "trigger": "manual | pre-compact-hook",
  "branch": "[current-branch]",
  "last_commit": "[sha]"
}
```

### Step 4 — Report

```
Backup saved: logs/transcript_backups/transcript_[timestamp].jsonl
Trigger: [manual | pre-compact-hook]
Branch: [branch]
```

## Graceful degradation

- If transcript not accessible: log the attempt, do not error
- If logs/ does not exist: create it
- Never block compaction — backup is best-effort
- Silent failure is acceptable; noisy failure is not

## Notes

This skill is informational — the actual backup is best done via a PreCompact hook wired in `settings.json`. This skill documents the pattern and can be invoked manually when needed.

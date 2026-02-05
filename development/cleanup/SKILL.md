---
name: cleanup
description: Archive processed inbox items. Activate when user says "cleanup", "archive inbox". Moves session summaries to archive, keeps inbox clean for new items.
allowed-tools: Bash, Read
---

# Cleanup (Inbox Archive)

Archive processed inbox items to keep inbox clean for new work.

## When to Activate

- User says: "cleanup", "archive inbox", "clean inbox"
- After learn skill completes
- When inbox has accumulated processed items

## Process

### 1. Check Inbox Contents

```bash
ls -la inbox/
ls -la inbox/session-summaries/ 2>/dev/null
```

### 2. Archive Session Summaries

Move processed summaries to monthly archive:

```bash
# Create archive directory
mkdir -p inbox/session-summaries/archive/$(date +%Y-%m)

# Move files older than 1 hour (not currently being written)
find inbox/session-summaries/ -maxdepth 1 -name "*.md" -mmin +60 -exec mv {} inbox/session-summaries/archive/$(date +%Y-%m)/ \;
```

### 3. Clean Other Processed Items

```bash
# Remove ephemeral files after processing
rm -f inbox/role-review-needed.txt 2>/dev/null
```

### 4. Verify Clean State

```bash
ls inbox/
```

### 5. Report

```
Inbox cleanup complete.

Archived:
- [N] session summaries → inbox/session-summaries/archive/YYYY-MM/

Inbox ready for new items.
```

## Archive Structure

```
inbox/
├── session-summaries/
│   ├── archive/
│   │   ├── 2025-11/
│   │   └── 2025-12/
│   └── (empty - ready for new)
└── (clean)
```

## Safety

- Only archive files older than 1 hour
- Never delete session summaries (archive instead)
- Idempotent - safe to run multiple times

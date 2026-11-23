---
name: hackmd
description: Work with HackMD documents. Use when reading, creating, updating, or deleting notes on HackMD. Supports change tracking to detect document modifications since last check. Supports personal and team workspaces.
metadata:
    {
        "clawdbot":
            {
                "emoji": "📜",
                "requires":
                    { "bins": ["hackmd-cli"], "env": ["HMD_API_ACCESS_TOKEN"] },
                "primaryEnv": "HMD_API_ACCESS_TOKEN",
            },
    }
---

# HackMD Integration

## Requirements

```bash
npm install -g @hackmd/hackmd-cli
```

## Quick Reference

### Read Notes

```bash
# List all personal notes
hackmd-cli notes

# Get note metadata (includes lastChangedAt)
hackmd-cli notes --noteId=<id> --output json

# Get note content (markdown)
hackmd-cli export --noteId=<id>

# List teams
hackmd-cli teams

# List team notes
hackmd-cli team-notes --teamPath=<path>
```

### Write Notes

```bash
# Create note
hackmd-cli notes create --content='# Title'

# Create from file
cat file.md | hackmd-cli notes create

# Update note
hackmd-cli notes update --noteId=<id> --content='# Updated'

# Delete note
hackmd-cli notes delete --noteId=<id>
```

### Team Notes

```bash
hackmd-cli team-notes create --teamPath=<path> --content='# Team Note'
hackmd-cli team-notes update --teamPath=<path> --noteId=<id> --content='...'
hackmd-cli team-notes delete --teamPath=<path> --noteId=<id>
```

## Change Tracking

Use `hackmd-track.js` (in `scripts/`) to detect document changes efficiently.

### Track a Note

```bash
node scripts/hackmd-track.js add <noteId>
```

### Check for Changes

```bash
# Single note - outputs content only if changed
node scripts/hackmd-track.js changes <noteId>

# All tracked notes
node scripts/hackmd-track.js changes --all

# JSON output for parsing
node scripts/hackmd-track.js changes <noteId> --json
```

### Manage Tracking

```bash
node scripts/hackmd-track.js list              # Show tracked notes
node scripts/hackmd-track.js remove <noteId>   # Stop tracking
node scripts/hackmd-track.js reset <noteId>    # Reset (next check shows as changed)
```

### How It Works

1. `hackmd-track.js add` stores note's `lastChangedAt` timestamp
2. `hackmd-track.js changes` compares current `lastChangedAt` with stored value
3. If changed: outputs content and updates stored timestamp
4. If unchanged: outputs nothing (use `--verbose` for status)

State stored in `./.hackmd/tracked-notes.json` (current working directory)

## Note Metadata Fields

When using `--output json`, notes include:

| Field            | Description                              |
| ---------------- | ---------------------------------------- |
| `lastChangedAt`  | Unix timestamp of last modification      |
| `lastChangeUser` | `{name, userPath, photo}` of last editor |
| `titleUpdatedAt` | When title changed                       |
| `tagsUpdatedAt`  | When tags changed                        |

## Rate Limits

- 100 calls per 5 minutes
- 2000 calls/month (10k on Prime plan)

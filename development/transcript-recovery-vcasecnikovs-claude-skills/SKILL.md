---
name: transcript-recovery
description: Recover full conversation history after context compaction. Use when context window is compacted and Claude needs to access earlier parts of the conversation, when user asks about what was discussed before, or when Claude needs to continue work from a previous session. Reads from /mnt/transcripts/ directory.
---

# Transcript Recovery

Recover full conversation history from `/mnt/transcripts/` after context compaction.

## Quick Start

```bash
# Copy script to working directory and run
cp /path/to/skill/scripts/get_transcript.py /home/claude/
python3 /home/claude/get_transcript.py --list
```

## Usage

| Command | Description |
|---------|-------------|
| `--list` | List all available transcripts |
| `--all` | Combine all transcripts chronologically |
| `--messages` | Extract clean human/assistant messages |
| `--search <query>` | Search across all transcripts |
| `--file <n>` | Read specific transcript |
| `--tail <n>` | Last N lines only |
| `--output <path>` | Save to file |

## Common Workflows

### After Compaction - Recover Context
```bash
python3 /home/claude/get_transcript.py --all --messages
```

### Find Specific Discussion
```bash
python3 /home/claude/get_transcript.py --search "topic keyword"
```

### Export Full History for User
```bash
python3 /home/claude/get_transcript.py --all --messages -o /mnt/user-data/outputs/history.txt
```

## Notes

- Transcripts location: `/mnt/transcripts/` (read-only)
- Files contain JSON with unicode escapes - script decodes to UTF-8 automatically
- `journal.txt` contains transcript metadata and descriptions
- Script must be copied to `/home/claude/` before execution
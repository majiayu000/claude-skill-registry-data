---
name: blackbox
description: Use when restoring previous file versions, querying file modification history, recovering from accidental edits, or understanding how blackbox flight recorder works for file snapshots and disaster recovery
---

# Blackbox Flight Recorder

Zero-dependency telemetry plugin that captures file snapshots before modifications.

## What It Captures

- **PreToolUse** (Write/Edit/MultiEdit) - Snapshots file before modification
- **UserPromptSubmit** - Logs user prompts
- **SessionStart** - Logs session boundaries

## Scripts

### Query Events

```bash
python3 scripts/query.py --last 10           # Last 10 events
python3 scripts/query.py --event-type PreToolUse  # Filter by type
python3 scripts/query.py --file myfile.py    # Filter by file
python3 scripts/query.py --stats             # Storage statistics
```

### Restore Files

```bash
python3 scripts/restore.py --list            # List recent snapshots
python3 scripts/restore.py --search myfile   # Find snapshots by pattern
python3 scripts/restore.py --hash <sha1> > restored.py  # Restore by hash
```

Scripts location: `skills/blackbox/scripts/`

## Limitations

- Files >2MB skipped
- Binary files skipped
- No automatic rotation

## References

- **Data format**: See [references/schema.md](references/schema.md)
- **Status command**: Run `/blackbox:status`

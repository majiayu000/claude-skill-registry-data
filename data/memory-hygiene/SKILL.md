---
name: memory-hygiene
description: Maintains memory cleanliness with deduplication, validation, and expiration
version: 1.0.0
author: Claude Memory System
tags: [memory, maintenance, validation, deduplication]
---

# Memory Hygiene Skill

## Purpose
Ensure memory remains queryable, compact, and consistent through automated hygiene operations. Prevents memory bloat and maintains data quality.

## When to Use
- Before bulk memory operations (imports, migrations)
- When memory file exceeds 5MB or 1000+ patterns
- Periodic maintenance (daily/weekly background task)
- After detecting duplicate or stale entries
- When schema validation fails

## Operations

### 1. Compact Memory
**Trigger**: Memory file >5MB or >1000 patterns
**Process**:
1. Read all memory entries
2. Deduplicate identical patterns
3. Merge similar entries (>80% similarity)
4. Bucket by topic for faster queries
5. Write compacted version with backup

**Script**: `scripts/compact_memory.py`
**Output**: Compression report with stats

### 2. Validate Schema
**Trigger**: Before ANY memory write operation
**Process**:
1. Load schema from `assets/schema_v1.json`
2. Check all required fields present
3. Validate data types and constraints
4. Check TTL format (ISO8601)
5. Verify confidence score (0.0-1.0)

**Script**: `scripts/validate_schema.py`
**Output**: Boolean pass/fail + error details

### 3. Expire Stale Entries
**Trigger**: Daily background task or manual
**Process**:
1. Scan all entries for TTL field
2. Compare TTL to current timestamp
3. Archive expired entries (if configured)
4. Remove from active memory
5. Log expired entry IDs

**Script**: `scripts/expire_stale.py`
**Output**: List of expired entries + archive path

### 4. Merge Duplicates
**Trigger**: After bulk imports or weekly maintenance
**Process**:
1. Group entries by topic + scope
2. Calculate similarity scores (fuzzy matching)
3. Merge entries with >80% similarity
4. Keep highest confidence version
5. Preserve metadata from all sources

**Script**: `scripts/merge_duplicates.py`
**Output**: Deduplication report

## Schema Definition

All memory entries MUST conform to:

```json
{
  "topic": "string (required, max 100 chars)",
  "scope": "global|repository (required)",
  "value": "any (required)",
  "TTL": "ISO8601 timestamp (optional)",
  "source": "user|agent|system (required)",
  "confidence": "0.0-1.0 (required)",
  "metadata": {
    "repository": "string (optional)",
    "created": "ISO8601 (auto-generated)",
    "updated": "ISO8601 (auto-generated)"
  }
}
```

See `references/schema.md` for complete specification.

## Integration with Memory Tool

### Before Write Operations
```python
# Always validate before writing
validation = execute_skill('memory-hygiene', {
    'operation': 'validate',
    'data': memory_entry
})

if validation['valid']:
    write_to_memory(memory_entry)
else:
    handle_validation_errors(validation['errors'])
```

### Periodic Maintenance
```bash
# Daily cron job
0 2 * * * node ~/.claude/memory/skill-executor.js execute memory-hygiene '{"operation":"expire"}'

# Weekly compaction
0 3 * * 0 node ~/.claude/memory/skill-executor.js execute memory-hygiene '{"operation":"compact"}'
```

### After Bulk Operations
```python
# After importing many entries
import_entries(bulk_data)

# Immediately compact and deduplicate
execute_skill('memory-hygiene', {
    'operation': 'compact_and_merge'
})
```

## Safety Measures

All hygiene operations:
1. **Create backup** before modification (`/memories/.backups/`)
2. **Log all changes** to `~/.claude/memory/hygiene.log`
3. **Dry-run mode** available with `--preview` flag
4. **Atomic operations** - rollback on failure
5. **Preserve provenance** - track all transformations

## Examples

### Good Memory Entries
See `references/examples.md` for examples of well-formed entries.

### Bad Memory Entries
See `references/examples.md` for anti-patterns to avoid.

## Performance

- **Validation**: <10ms per entry
- **Compaction**: ~100ms per 1000 entries
- **Deduplication**: ~200ms per 1000 entries
- **Expiration**: ~50ms per 1000 entries

## Error Handling

- **Invalid schema**: Returns detailed error with field name
- **Corrupted data**: Archives problematic entries separately
- **Disk full**: Fails gracefully with clear error
- **Backup failure**: Aborts operation, preserves original

## Configuration

Edit `assets/hygiene_config.json` to customize:
- Similarity threshold for merging (default: 0.8)
- Archive location (default: `/memories/.archive/`)
- Backup retention (default: 7 days)
- Max memory size before auto-compact (default: 5MB)

## Integration Points

### Memory Tool Operations
- `insert` → validate_schema()
- `replace` → validate_schema()
- `delete` → log_deletion()
- `rename` → update_metadata()

### Context Editing
After context clearing, run compaction to optimize memory.

### Background Tasks
Set up cron jobs for automated maintenance (see Integration section).

---

*Memory Hygiene Skill v1.0.0 - Keeping your memory clean and queryable*

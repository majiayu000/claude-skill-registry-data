---
name: migrate
description: Handle cqs schema version upgrades — check version, attempt migration, rebuild if needed.
disable-model-invocation: false
argument-hint: ""
---

# Migrate

Handle schema version mismatches when upgrading cqs.

## Process

### 1. Check current schema version

```bash
cqs stats 2>&1
```

If it works normally, no migration needed. If you see a schema error, continue.

### 2. Identify the mismatch

Errors tell you the versions:
- **SchemaMismatch(path, from, to)**: Index is at version `from`, cqs expects `to`. Auto-migration was attempted but no migration path exists.
- **SchemaNewerThanCq(version)**: Index was created by a newer cqs version. Update your binary.

### 3. Attempt migration

cqs attempts auto-migration when it opens the database. If you're seeing SchemaMismatch, it means no migration path exists for that version jump.

Check available migrations:
```bash
grep -n "migrate_v" src/store/migrations.rs
```

### 4. Rebuild if no migration path

When auto-migration isn't available, the only option is a full rebuild:

```bash
# Back up the old index (just in case)
cp -r .cqs/ .cq.backup/

# Delete and rebuild
rm -rf .cqs/
cqs init
cqs index
```

This re-parses all source files and re-embeds them. Notes in `docs/notes.toml` are preserved (they live outside `.cqs/`).

### 5. Rebuild references too

References have their own databases at the same schema version:

```bash
cqs ref list
```

For each reference:
```bash
cqs ref update <name>
```

If that fails with schema errors, remove and re-add:
```bash
cqs ref remove <name>
cqs ref add <name> <source_path> --weight <weight>
```

### 6. Verify

```bash
cqs stats
```

Should show the current schema version and correct chunk counts.

### 7. Clean up

```bash
rm -rf .cq.backup/
```

## Notes

- `.cqs/` is gitignored — rebuilding only costs time, not data. But it now holds named slots (`.cqs/slots/<name>/index.db`) and the embeddings cache (`.cqs/embeddings_cache.db`) — `rm -rf .cqs/` nukes ALL slots and the cache. Prefer removing just the broken slot dir if only one slot is affected.
- Notes (`docs/notes.toml`) are never lost — they're separate from the index
- Schema version is stored in `metadata` table: `SELECT value FROM metadata WHERE key = 'schema_version'`
- Current version: v28 (always confirm against `src/store/helpers/mod.rs:CURRENT_SCHEMA_VERSION`)
- Stop the daemon before destructive steps: `systemctl --user stop cqs-watch` (restart after)

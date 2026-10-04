---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Evolutionary file renaming with wrapper files. Enables renames without hard breaks — references are organically updated through usage.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="migrate-rename banner">

> **English** — Official English version of `migrate-rename`.


# File Renaming with Wrappers (Evolutionary Migration) (English)

> Enables file renames WITHOUT hard breaks. References are organically updated through daily usage.

---

## Principle: Evolutionary Migration

```
BEFORE:                          AFTER:
old_file.md                      new_file.md (renamed)
   |                                |
   +-- Reference A                  +-- old_file.md (wrapper)
   +-- Reference B                         |
   +-- Reference C                         +-- Log table
                                           +-- Instructions
                                           +-- Link to new_file.md
```

When someone accesses the old path:
1. Lands at the wrapper file
2. Adds an entry to the log
3. Corrects the reference that brought them here
4. Proceeds to the actual file

---

## Step by Step

### 1. Rename the File

```bash
mv old_file.md new_file.md
```

### 2. Create Wrapper File

Create `old_file.md` with the following content:

```markdown
# OLD_FILE.md - REDIRECTED (Deutsch)

**Status:** This file has been renamed to `new_file.md`

---

## Migration Log

| Date | Who | Origin | Reference corrected? |
|------|-----|--------|---------------------|
| YYYY-MM-DD | [Name] | Initial migration | n/a (wrapper created) |

---

## Instructions

1. **Leave a log entry** (in table above)
2. **Check origin**: What sent you here?
3. **Correct reference**: Change `old_file.md` -> `new_file.md`
4. **Go to the actual file**: `new_file.md`

---

**Target file:** `new_file.md`
```

### 3. Immediately Correct Critical References
- Help files (primary documentation)
- System prompt references
- CLI code that directly uses the path

### 4. Migrate Remaining References Evolutionarily
The rest is automatically corrected through usage.

---

## When to Use the Wrapper Method?

**YES - Wrapper useful:**
- Many potential references
- File is referenced by various partners/tools
- Not a critical system file

**NO - Change all directly:**
- Few, known references
- Critical system files (config, DB schema)
- Performance-critical paths

---

## Cleanup

After approximately 30 days or when the log shows no new entries:
1. Move wrapper file to `_archive/deprecated/`
2. Or delete completely (if no more entries)

---

## Changelog

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0

---

*Ported from BACH v3.8.0 | Standalone Version*

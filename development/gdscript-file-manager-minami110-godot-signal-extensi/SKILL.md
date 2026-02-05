---
name: GDScript File Manager
description: Move, rename, or delete GDScript files with their .uid files for Godot projects. Use when reorganizing code, renaming scripts, or removing unused GDScript files.
---

# GDScript File Manager

Manage GDScript files (.gd) along with their corresponding .uid files.

## Core Principle

Godot Engine auto-generates a `.uid` file for each resource. **Always handle .gd and .uid files together.**

## Operations

### Move Files

```bash
# 1. Verify destination
ls <destination-dir>

# 2. Move both files
mv <source>.gd <destination>.gd && mv <source>.gd.uid <destination>.gd.uid

# 3. Verify
ls <destination-dir> && ls <source-dir>
```

### Rename Files

```bash
# 1. Rename both files
mv <old-name>.gd <new-name>.gd && mv <old-name>.gd.uid <new-name>.gd.uid

# 2. Verify
ls -la <directory>
```

### Delete Files

```bash
# 1. Verify target
ls -la <directory>

# 2. Delete both files
rm <filename>.gd && rm <filename>.gd.uid

# 3. Verify
ls -la <directory>
```

## Important Notes

- Never manually create or edit .uid files - Godot manages them automatically
- Always process both files together to avoid breaking project references
- Verify files before operations using `ls` commands

See [examples.md](examples.md) for detailed examples and troubleshooting.

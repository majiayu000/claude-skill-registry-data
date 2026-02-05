---
name: safe-file-removal
description: Use safe-rm command to safely 'remove' files by renaming them to .obsolete instead of permanent deletion. Reversible, collision-safe, hook-compliant.
allowed-tools: Bash, Read, Grep
---

# Safe File Removal

Rename files to `.obsolete` instead of permanent deletion via `safe-rm` command.

## When to Use

- Removing temp files, build artifacts, old code, deprecated tests
- After refactoring (keep backup during testing)
- Any situation where `rm` is blocked by pre-tool hooks
- Need reversible "deletion"

## Why Not `rm`

**Project setting**: `.claude/settings.json:132` → `"RM_BASH_BLOCK": "true"`

| Issue | Solution |
|-------|----------|
| `rm` permanently deletes | `safe-rm` renames (reversible) |
| Blocked by pre-tool hooks | Works within safety constraints |
| No recovery | `mv file.obsolete file` restores |

## Command

```bash
./.claude/bin/safe-rm [file1] [file2] [dir/]
```

**Path**: `.claude/bin/safe-rm:1-72`

## Features

| Feature | Benefit |
|---------|---------|
| **Reversible** | `mv file.obsolete file` recovers |
| **Multi-file** | Handle multiple args in one command |
| **Collision safe** | Adds timestamp if .obsolete exists |
| **Color output** | Green ✓ / Yellow ⚠ / Red ✗ |
| **Statistics** | Reports renamed/failed count |

## Basic Usage

| Operation | Command | Result |
|-----------|---------|--------|
| Single file | `./.claude/bin/safe-rm file.txt` | `file.txt.obsolete` |
| Multiple | `./.claude/bin/safe-rm f1 f2 dir/` | All get `.obsolete` suffix |
| Restore | `mv file.obsolete file` | Original restored |

## Recovery

| Scenario | Command |
|----------|---------|
| Single | `mv file.obsolete file` |
| With timestamp | `mv file.obsolete.20251109_110500 file` |
| Find all | `find . -name "*.obsolete"` |
| Restore all | `find . -name "*.obsolete" \| while read f; do mv "$f" "${f%.obsolete}"; done` |

## Workflow

1. Mark obsolete → `safe-rm [files]`
2. Verify works → `npm test && npm run build`
3. Review periodic → `find . -name "*.obsolete"`
4. Permanent delete (when confident) → `/bin/rm [file].obsolete`

## When NOT to Use

| Scenario | Use safe-rm? | Why |
|----------|-----------|-----|
| Secrets (.env, keys) | ❌ | Needs secure deletion + git history rewrite |
| .git folder | ❌ | Too risky |
| node_modules | ⚠️ | `rm -rf` safe, but safe-rm works |
| Temp/build | ✅ | Reversible, safe |

## Output Examples

**Success**:
```
✓ Renamed: file.txt → file.txt.obsolete
─────────────────────────────────────
Renamed: 1
```

**Collision** (timestamp fallback):
```
⚠ Already exists: file.obsolete
  Using: file.obsolete.20251109_110500
✓ Renamed: file → file.obsolete.20251109_110500
```

**Error**:
```
✗ Not found: missing.txt
─────────────────────────────────────
Failed: 1
```

## Quick Reference

| Task | Command |
|------|---------|
| Remove single | `./.claude/bin/safe-rm file.txt` |
| Remove multiple | `./.claude/bin/safe-rm f1 f2 dir/` |
| Restore | `mv file.obsolete file` |
| List obsolete | `find . -name "*.obsolete"` |
| Count | `find . -name "*.obsolete" \| wc -l` |

## Supporting Files

- **[EXAMPLES.md](EXAMPLES.md)** - 10 scenarios: temp files, refactoring, tests, collisions, assets, docs, batch ops, scripting, git, hooks
- **[TEMPLATES.md](TEMPLATES.md)** - Copy-paste commands for all operations
- **[VALIDATION.md](VALIDATION.md)** - Safety checklists, verification commands

## Key Insight

**Safety by design**: No permanent deletion → collision protection → hook compliance → audit trail. Development workflow: Refactor → safe-rm → Test → Review period → Permanent delete after confidence.

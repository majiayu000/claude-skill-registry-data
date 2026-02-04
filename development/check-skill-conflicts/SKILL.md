---
name: check-skill-conflicts
description: This skill should be used when checking for naming conflicts between local skills (~/.claude/skills) and plugin-provided skills (~/.claude/plugins). Use to identify duplicate or similarly named skills that may cause inconsistent agent behavior.
---

# Check Skill Conflicts

Identifies naming conflicts between local Claude Code skills and plugin-provided skills.

## Why This Matters

When a skill exists in both `~/.claude/skills/` (local) and `~/.claude/plugins/` (plugin), agents may:
- Load the wrong skill version
- Get inconsistent results between sessions
- Have unpredictable behavior when skill names are similar

## Quick Check

```bash
# Run conflict check
~/.claude/plugins/marketplaces/plinde-plugins/check-skill-conflicts/skills/check-skill-conflicts/scripts/check-conflicts.sh

# Verbose output (shows all skills found)
~/.claude/plugins/marketplaces/plinde-plugins/check-skill-conflicts/skills/check-skill-conflicts/scripts/check-conflicts.sh --verbose

# JSON output for programmatic use
~/.claude/plugins/marketplaces/plinde-plugins/check-skill-conflicts/skills/check-skill-conflicts/scripts/check-conflicts.sh --json
```

## What It Checks

1. **Exact Matches** - Same skill name in both locations
2. **Similar Names** - Names that differ only by suffix/prefix (e.g., `foo` vs `foo-skill`)
3. **Case Variations** - Same name with different casing

## Output Example

```
SKILL CONFLICT CHECK
====================

Local Skills:     45 found in ~/.claude/skills/
Plugin Skills:    12 found in ~/.claude/plugins/

EXACT MATCHES (High Priority):
  ⚠️  kyverno-version-lookup
      Local:  ~/.claude/skills/kyverno-version-lookup/
      Plugin: ~/.claude/plugins/marketplaces/plinde-plugins/kyverno-version-lookup/

SIMILAR NAMES (Review Recommended):
  ⚡ plugin-creator ~ plugin-dev
      Local:  ~/.claude/skills/plugin-creator/
      Plugin: ~/.claude/plugins/marketplaces/.../plugin-dev/

No conflicts: ✅ (if none found)
```

## Resolution Options

When conflicts are found:

1. **Remove local skill** - If plugin version is preferred
   ```bash
   cd ~/.claude/skills && git rm -r <skill-name>
   ```

2. **Uninstall plugin** - If local version is preferred
   ```bash
   /plugin uninstall <plugin-name>
   ```

3. **Rename local skill** - If both are needed but different
   ```bash
   mv ~/.claude/skills/<old-name> ~/.claude/skills/<new-name>
   # Update SKILL.md frontmatter name field
   ```

## Skill Locations

| Type | Path Pattern |
|------|--------------|
| Local Skills | `~/.claude/skills/<name>/SKILL.md` |
| Plugin Skills | `~/.claude/plugins/marketplaces/*/<plugin>/skills/<name>/SKILL.md` |
| Symlinked Plugins | `~/.claude/plugins/<symlink>/*/skills/<name>/SKILL.md` |

## Self-Test

```bash
# Verify script exists and is executable
test -x ~/.claude/plugins/marketplaces/plinde-plugins/check-skill-conflicts/skills/check-skill-conflicts/scripts/check-conflicts.sh && \
  echo "✅ check-conflicts.sh exists" || echo "❌ Script missing"

# Run a quick check
~/.claude/plugins/marketplaces/plinde-plugins/check-skill-conflicts/skills/check-skill-conflicts/scripts/check-conflicts.sh --json | jq -e '.local_count >= 0' > /dev/null && \
  echo "✅ Script runs successfully" || echo "❌ Script failed"
```

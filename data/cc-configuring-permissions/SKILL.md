---
name: configuring-permissions
description: Use when adding allow/deny rules to Claude Code, granting project permissions, troubleshooting "permission denied" errors, "skill requires approval" prompts, or setting up shared team permissions. Also use when working with git worktrees and permissions aren't being inherited.
---

# Configuring Permissions

## STOP: Freshness Check Required

**Before using this skill:** Check `.state` file — if missing or `last_evaluated` > 7 days ago, warn user and research current CC issues before proceeding.

```bash
find ~/.claude/plugins -path "*/claude-code/skills/configuring-permissions/.state" 2>/dev/null | head -1
```

**Full procedure:** [freshness-check.md](freshness-check.md)

---

## Overview

Claude Code permissions control which tools/skills can run without prompting. **Core principle:** prompt grants update memory immediately; manual edits require restart.

## CRITICAL

### Team vs Solo Project Detection

**Before modifying project settings:** Check if changes affect a team (`git shortlog -sne --all | head -10`). User-level `Skill(*)` won't help teammates — team projects need project-level config.

**Full decision flow:** [team-detection.md](team-detection.md)

### Restart Requirement

| Method                    | Restart? | Why                                       |
| ------------------------- | -------- | ----------------------------------------- |
| Prompt grant              | No       | Updates file AND in-memory simultaneously |
| Manual settings.json edit | **Yes**  | File only read at startup                 |

When manually editing settings.json, tell user:

> Restart Claude Code for the new permission to take effect.

### Skill Permission Naming

**Common mistake:** Using marketplace name instead of plugin name.

| Plugin Identifier | Correct Pattern | Wrong Pattern |
|-------------------|-----------------|---------------|
| `superpowers@superpowers-marketplace` | `Skill(superpowers:*)` | `Skill(superpowers-marketplace:*)` |
| `hookify@claude-plugins-official` | `Skill(hookify:*)` | `Skill(claude-plugins-official:*)` |

The format is `Skill(plugin-name:skill-name)`, NOT `Skill(marketplace-name:skill-name)`.

**To find the correct plugin name:** Look at the part BEFORE the `@` in the plugin identifier.

### MCP Permission Syntax

MCP permissions support three patterns ([docs](https://code.claude.com/docs/en/iam)):

| Pattern | Matches |
|---------|---------|
| `mcp__server` | All tools from server |
| `mcp__server__*` | All tools (wildcard, equivalent) |
| `mcp__server__tool` | Specific tool only |

Example:
```json
{
  "permissions": {
    "allow": [
      "mcp__serena",
      "mcp__claude-in-chrome",
      "mcp__effect-docs"
    ]
  }
}
```

Fully qualified names (e.g., `mcp__serena__find_symbol`) only needed to allow specific tools while denying others from the same server.

**Note:** Issue [#3107](https://github.com/anthropics/claude-code/issues/3107) (July 2025) claimed wildcards weren't supported, but current docs confirm both patterns are valid and equivalent.

### Skill Permissions

**`Skill(*)` is broken everywhere:**
- `~/.claude/settings.json` (user): buggy, sometimes ignored ([#5140](https://github.com/anthropics/claude-code/issues/5140), [#10833](https://github.com/anthropics/claude-code/issues/10833))
- `.claude/settings.json` (project): doesn't work at all
- `.claude/settings.local.json` (project local): works, but see team workaround below

**For individuals:** Use explicit patterns in user settings:
```json
"Skill(plugin-name:*)"
```
Extract plugin names from `enabledPlugins` keys (the part before `@`).

**For teams — Option A (simple, no personal overrides):**
Commit `.claude/settings.local.json` with skill permissions. Tradeoff: team members can't have personal overrides without merge conflicts.

**For teams — Option B (recommended, allows personal overrides):**
Use a SessionStart hook to sync baseline permissions:

1. Create `.claude/settings.local.json.example` (committed) with baseline permissions
2. Keep `.claude/settings.local.json` gitignored
3. Add SessionStart hook to sync example → local:

```bash
#!/bin/bash
# .claude/scripts/sync-local-permissions.sh
EXAMPLE=".claude/settings.local.json.example"
LOCAL=".claude/settings.local.json"

[[ ! -f "$EXAMPLE" ]] && exit 0

if [[ ! -f "$LOCAL" ]]; then
  cp "$EXAMPLE" "$LOCAL"
  echo "Created $LOCAL from example. Restart CC for permissions to take effect."
  exit 0
fi

CURRENT=$(jq -S '.permissions.allow // [] | sort' "$LOCAL" 2>/dev/null || echo '[]')
BASELINE=$(jq -S '.permissions.allow // [] | sort' "$EXAMPLE" 2>/dev/null || echo '[]')
MERGED=$(jq -n --argjson a "$CURRENT" --argjson b "$BASELINE" '$a + $b | unique | sort')

if [[ "$CURRENT" != "$MERGED" ]]; then
  jq --argjson allow "$MERGED" '.permissions.allow = $allow' "$LOCAL" > "$LOCAL.tmp" && mv "$LOCAL.tmp" "$LOCAL"
  echo "Added baseline permissions. Restart CC for changes to take effect."
fi
```

Hook in `.claude/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": ".claude/scripts/sync-local-permissions.sh" }] }]
  }
}
```

Benefits: team gets baseline permissions, individuals can add extras without conflicts.

**Tracking:** [#10833](https://github.com/anthropics/claude-code/issues/10833) — when fixed, move to `settings.json` and simplify.

## Permission Files

| File                           | Scope         | Committed? | Precedence |
| ------------------------------ | ------------- | ---------- | ---------- |
| `~/.claude/settings.json`      | User (global) | No         | Lowest     |
| `.claude/settings.json`        | Project       | Yes        | Middle     |
| `.claude/settings.local.json`  | Project local | Usually no | Highest    |

## Adding Permissions

### Via Prompt (Recommended)

Select "Yes, and don't ask again" → adds to appropriate settings file, no restart needed.

### Via Manual Edit

```json
{
  "permissions": {
    "allow": ["Bash", "Skill(superpowers:*)"],
    "deny": []
  }
}
```

## Team-Shared Permissions

```dot
digraph team_permissions {
    "Project permission needed" [shape=box];
    "settings.local.json committed?" [shape=diamond];
    "Works for user only" [shape=box];
    "Share with team?" [shape=diamond];
    "Add to settings.local.json" [shape=box];
    "Override gitignore + commit" [shape=box];

    "Project permission needed" -> "settings.local.json committed?";
    "settings.local.json committed?" -> "Add to settings.local.json" [label="yes"];
    "settings.local.json committed?" -> "Works for user only" [label="no"];
    "Works for user only" -> "Share with team?";
    "Share with team?" -> "Override gitignore + commit" [label="yes"];
    "Share with team?" -> "Add to settings.local.json" [label="no"];
    "Override gitignore + commit" -> "Add to settings.local.json";
}
```

**Check:** `git ls-files .claude/settings.local.json`

**To share with team, override gitignore:**
```gitignore
.claude/
!.claude/settings.local.json
```

**Why commit:** Team members get permissions automatically; worktrees don't inherit uncommitted files.

## Permission Patterns — Complete Reference

### Tools Requiring Permissions

| Tool | Default | Notes |
|------|---------|-------|
| Bash | Ask | Shell commands |
| Edit | Ask | File modifications |
| Write | Ask | File creation/overwrite |
| MultiEdit | Ask | Batch file edits |
| NotebookEdit | Ask | Jupyter cell modifications |
| WebFetch | Ask | URL fetching |
| WebSearch | Ask | Web searches |
| Skill | Ask | Plugin/local skills |

**No permission required:** Glob, Grep, Read, NotebookRead, Task, TodoWrite

### Pattern Syntax

```
# TOOLS (bare = all uses)
Bash                           # All bash commands
Edit                           # All file edits
Write                          # All file writes
MultiEdit                      # All multi-edits
WebFetch                       # All web fetches
WebSearch                      # All web searches

# BASH (prefix matching, NOT regex)
Bash(npm run build)            # Exact command
Bash(npm run test:*)           # Commands starting with "npm run test:"
Bash(git *)                    # Commands starting with "git "

# FILE PATHS (gitignore-style globs)
Read(~/**)                     # Read files in home (recursive)
Read(/src/**)                  # Relative to settings file location
Read(//absolute/path/**)       # Absolute filesystem path (note: //)
Edit(*.md)                     # Edit markdown files
Write(.claude/**)              # Write to .claude directory

# SKILLS
Skill(plugin-name:*)           # All skills from a plugin
Skill(plugin-name:skill-name)  # Specific skill from plugin
Skill(local-skill-name)        # Local skill (no colon)

# MCP SERVERS
mcp__server                    # All tools from server
mcp__server__*                 # All tools (wildcard, equivalent)
mcp__server__tool              # Specific tool only

# WEB
WebFetch(domain:example.com)   # Specific domain only
```

### Local vs Plugin Skills

| Skill Location | Example | Permission Pattern |
|----------------|---------|-------------------|
| `~/.claude/skills/foo/` | User local skill "foo" | `Skill(foo)` |
| `.claude/skills/bar/` | Project local skill "bar" | `Skill(bar)` |
| Plugin `hookify@marketplace` | Plugin skill "list" | `Skill(hookify:list)` or `Skill(hookify:*)` |

**Key distinction:** Local skills have NO colon. Plugin skills have `plugin-name:skill-name`.

## Known Issues (Jan 2026)

### Symlinked settings.json Broken ([#3575](https://github.com/anthropics/claude-code/issues/3575), [#764](https://github.com/anthropics/claude-code/issues/764), [#18160](https://github.com/anthropics/claude-code/issues/18160)) — OPEN

**Problem:** CC doesn't properly handle symlinked `~/.claude/settings.json`:
1. **Read failures** — permissions not recognized from symlinked files
2. **Write breakage** — CC's atomic writes replace symlinks with regular files
3. **Performance degradation** — symlinked settings cause multi-second command delays

**Impact:** Dotfiles users (stow, chezmoi symlinks, custom scripts) can't sync settings.json normally.

**Workaround:** Don't symlink settings.json. Let CC own `~/.claude/settings.json` at runtime.

For dotfiles ergonomics, create a **reverse convenience symlink** (gitignored) from your dotfiles repo to the runtime file:
```bash
# In dotfiles repo (gitignored):
ln -s ~/.claude/settings.json dotfiles/claude/settings.json
```
This lets you edit from your dotfiles workspace while CC owns the actual file.

**Alternative tools:**
- [chezmoi](https://www.chezmoi.io/) — generates files instead of symlinks
- [claude-code-config-sync](https://www.npmjs.com/package/claude-code-config-sync) — NPM sync with conflict resolution

### Path Prefix Gotcha ([#6881](https://github.com/anthropics/claude-code/issues/6881)) — OPEN

| Prefix | Meaning | Example |
|--------|---------|---------|
| `/path` | Relative to settings file | `/src/**` → `<settings-dir>/src/**` |
| `//path` | Absolute filesystem | `//Users/me/code/**` |
| `~/path` | Home directory | `~/.config/**` |

**Common mistake:** `/Users/me/...` is NOT absolute — use `//Users/me/...`

### Skill Permissions Broken ([#5140](https://github.com/anthropics/claude-code/issues/5140), [#10833](https://github.com/anthropics/claude-code/issues/10833)) — OPEN

`Skill(*)` doesn't work reliably anywhere:
- User settings: sometimes ignored, worktree bug
- Project `settings.json`: doesn't work at all
- Project `settings.local.json`: works but blocks personal overrides

**Team workaround:** Commit `settings.local.json` with explicit skill patterns. See [Skill Permissions](#skill-permissions) above.

### Skill allowed-tools Broken ([#14956](https://github.com/anthropics/claude-code/issues/14956)) — OPEN

Skills with `allowed-tools` in frontmatter don't actually grant permissions. The skill loads, reports correct `allowedTools`, but Bash commands are still denied.

**Workaround:** Add patterns to global allow list directly.

### Plugin Enable/Disable Ignored ([#13344](https://github.com/anthropics/claude-code/issues/13344)) — OPEN

When plugins share a source directory, disabling one loads all skills anyway. `enabledPlugins` settings have no effect.

**Impact:** ~35-40k tokens wasted on unwanted skills.

### User Settings Sometimes Ignored ([#5140](https://github.com/anthropics/claude-code/issues/5140)) — OPEN

`~/.claude/settings.json` permissions may not apply. Same rules work in project `.claude/settings.local.json`.

## Fixed Issues (Reference)

| Issue | Fixed | Description |
|-------|-------|-------------|
| [#9814](https://github.com/anthropics/claude-code/issues/9814) | Oct 2025 | UI grant overwrites list |
| [#8581](https://github.com/anthropics/claude-code/issues/8581) | Oct 2025 | Bash wildcards + env vars |
| [#3107](https://github.com/anthropics/claude-code/issues/3107) | Jul 2025 | MCP wildcards not honored |
| [#10093](https://github.com/anthropics/claude-code/issues/10093) | Jan 2026 | Plugin-scoped permissions (NOT_PLANNED) |

## Programmatic Editing (Hooks/Scripts)

When scripts modify settings.json:

### Safe JSON Modification

```bash
SETTINGS_FILE="$HOME/.claude/settings.json"
PERMISSION="Skill(hookify:*)"

# Check if already present (avoid duplicates)
if ! jq -e --arg p "$PERMISSION" '.permissions.allow | index($p)' "$SETTINGS_FILE" >/dev/null 2>&1; then
  # Atomic write: tmp file + mv
  jq --arg p "$PERMISSION" '.permissions.allow += [$p]' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp" \
    && mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
fi
```

### Critical Rules

1. **Always use jq** — Never sed/awk on JSON
2. **Atomic writes** — Write to `.tmp`, then `mv`
3. **Check before adding** — Use `jq -e ... | index($p)` to avoid duplicates
4. **Validate result** — `jq empty "$SETTINGS_FILE"` to verify valid JSON
5. **Remember restart requirement** — Script changes don't take effect until CC restarts

### Lock File (Optional, for parallel safety)

```bash
LOCK_FILE="$HOME/.claude/settings.json.lock"
exec 200>"$LOCK_FILE"
flock -n 200 || { echo "Settings locked"; exit 1; }
# ... do work ...
flock -u 200
```

## Notes

* `*` matches any characters; `**` matches directory depth
* Deny rules take precedence over allow
* Project settings override user settings

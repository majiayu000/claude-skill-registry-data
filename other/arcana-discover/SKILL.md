---
name: arcana-discover
description: >
  Find and analyze Claude Code skills in a directory. Reports skill names, descriptions,
  and compatibility status for other surfaces. Trigger phrases: "find skills",
  "list skills", "what skills are in", "discover skills", "analyze plugin".
---

# Arcana Discover: Find Skills

Find and analyze Claude Code skills in a directory.

## Path Convention

`{PLUGIN_ROOT}` = This plugin's root directory (where plugin.json lives)

## What This Does

1. Searches a directory for SKILL.md files
2. Analyzes each skill's metadata
3. Reports compatibility status for other surfaces
4. Identifies potential issues before export/upload

## Workflow

### Step 1: Get Target Directory

If not provided as argument, ask the user:

**Question:** "Where should I look for skills?"

**Options:**
1. **Current directory** - Search here and subdirectories
2. **Specify path** - Enter a directory path
3. **Installed plugins** - Search `~/.claude/plugins/`

### Step 2: Find SKILL.md Files

Use Glob to find all SKILL.md files:

```
{target_directory}/**/SKILL.md
```

### Step 3: Analyze Each Skill

For each SKILL.md found:

1. Read the file
2. Extract frontmatter (name, description)
3. Check for Claude Code-only fields
4. Validate against API rules (see `{PLUGIN_ROOT}/lib/references/validation-rules.md`)

### Step 4: Report Results

Present a summary:

```
Found 3 skills in /path/to/plugin:

1. my-skill
   Description: Does something useful
   Status: ✓ Ready for export

2. github-helper
   Description: Helps with GitHub operations
   Status: ⚠ Has CC-only fields (allowed-tools, hooks)

3. claude-sync
   Description: Syncs with Claude
   Status: ✗ Name contains 'claude' (not allowed)
```

## Compatibility Checks

Read `{PLUGIN_ROOT}/lib/references/validation-rules.md` for full rules.

| Check | Pass | Fail |
|-------|------|------|
| Name length | ≤64 chars | Too long |
| Name format | lowercase, numbers, hyphens | Invalid characters |
| Name content | Clean | Contains "claude" or "anthropic" |
| Description | 1-1024 chars, no XML | Empty, too long, or has XML |
| CC-only fields | None | Has allowed-tools, hooks, etc. |

## Output Format

For each skill, show:

```
Skill: {name}
Path: {path}
Description: {description}

Compatibility:
  Name: ✓ Valid (24 chars)
  Description: ✓ Valid (156 chars)
  CC-only fields: ⚠ allowed-tools, model

Action needed: Strip CC-only fields during export
```

## Summary Statistics

At the end, show:

```
Summary:
  Total skills found: 5
  Ready for export: 3
  Need fixes: 2

To export: /arcana export-zip {skill-path}
To upload: /arcana upload-api {skill-path}
```

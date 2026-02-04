---
name: working-with-chezmoi
description: Use when working with any configuration file outside of project directories in ~/Code (unless already managed like ~/Code/CLAUDE.md) - handles chezmoi prefix mappings, template awareness, conflict resolution workflow, and sync to avoid losing changes and breaking templates
---

# Working with Chezmoi

## Core Principle

Chezmoi manages dotfiles with a git-backed source directory. **Always check for templates first**, work with the source, understand prefix mappings, and follow the conflict resolution workflow to avoid losing changes.

## CRITICAL: Check for Templates FIRST

**Before editing ANY config file:**

```bash
# Check if file is templated:
ls -la ~/.local/share/chezmoi/[prefix_mapped_name]*
```

**If `.tmpl` exists:**
- Edit the template source, NOT the generated file
- NEVER use `chezmoi add` (removes template attribute)
- Copy directly: `cp ~/file ~/.local/share/chezmoi/prefix_mapped_name.tmpl`

**Why this matters:**
- Editing generated file when `.tmpl` exists → changes overwritten on next apply
- Using `chezmoi add` on templates → loses template logic permanently
- Templates contain variables like `{{ .chezmoi.hostname }}` that must be preserved

## Quick Reference: Prefix Mappings

| Actual file | Chezmoi source |
|------------|----------------|
| `.claude/hooks/SessionStart` | `dot_claude/hooks/executable_SessionStart` |
| `.ssh/config` | `private_dot_ssh/config.tmpl` |
| `.config/ghostty/config` | `dot_config/ghostty/config` |
| `.zshrc` | `private_dot_zshrc.tmpl` |

**Pattern:**
- `.` → `dot_`
- Private/sensitive → `private_` prefix
- Executable scripts → `executable_` prefix
- Templated files → `.tmpl` suffix

**Chezmoi source location:** `~/.local/share/chezmoi/`

## Common Claude Hooks

Valid hook names (cannot create arbitrary names):
- `SessionStart` - runs at session start
- `stop-notification.sh` - custom notification hooks

These are specific hook types, not arbitrary filenames.

## Standard Editing Workflow

**For any config file edit:**

1. **Check if templated FIRST**: `ls ~/.local/share/chezmoi/prefix_mapped_name*`
2. **Edit correct source**: Template if exists, otherwise edit local file
3. **Copy to source**: `cp ~/file ~/.local/share/chezmoi/prefix_mapped_name`
4. **Verify changes**: `chezmoi diff`
5. **Commit locally**: `cd ~/.local/share/chezmoi && git add -A && git commit -m "msg"`
6. **Push**: `git push`

## Conflict Resolution Workflow

**When working with config files that may have local drift + remote changes:**

### Step 1: Capture Local Drift (BEFORE pulling)

```bash
chezmoi status
# Shows files modified locally vs chezmoi source
# MM = modified in both local and source
# M  = modified in source only
```

**For each modified file:**
- Decide: keep local changes or discard?
- If keeping: `cp ~/actual-file ~/.local/share/chezmoi/prefix_mapped_name`
- Verify: `chezmoi diff` shows expected changes

**Commit local changes:**
```bash
cd ~/.local/share/chezmoi
git add -A
git commit -m "Capture local config changes"
# Don't push yet
```

### Step 2: Pull Remote Changes

```bash
cd ~/.local/share/chezmoi
git pull --rebase
# Handle any git conflicts in source files if needed
```

### Step 3: Review What Would Apply

```bash
chezmoi diff
# Shows what would change if you apply chezmoi now
```

**For each file in diff:**
- Remote version better? → Will apply in step 4
- Local version better? → Already committed in step 1
- Need to merge? → Edit source file, commit again

### Step 4: Apply or Override

**If remote changes are good:**
```bash
chezmoi apply
```

**If local changes should override remote:**
- Already committed in step 1
- Just push (step 5)

**If need to merge:**
- Edit source file: `~/.local/share/chezmoi/prefix_mapped_name`
- Commit: `cd ~/.local/share/chezmoi && git add file && git commit -m "Merge local and remote changes"`

### Step 5: Push Everything

```bash
cd ~/.local/share/chezmoi
git push
```

**Now all machines get the resolved state.**

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Skip template check | Changes disappear after apply | Always check for `.tmpl` FIRST |
| Use `chezmoi add` on template | "remove template attribute" warning | Copy directly to source instead |
| Edit generated file | Work gets overwritten | Edit template source |
| Forget `dot_` prefix | Can't find file in source | Use prefix mapping table |
| Pull before capturing local | Local changes lost | Always capture local drift first |
| Act under time pressure | Invalid names, wrong locations | Check first, act second |

## Red Flags - STOP and Check

- About to use `chezmoi add` → Check if file is templated first
- About to edit dotfile → Check if `.tmpl` version exists first
- User says "quick" → Still check for templates, don't skip steps
- Can't find file in source → Check prefix mapping table

## When to Use This Skill

**Trigger this skill when:**
- Editing ANY file in `~/.config/`, `~/.ssh/`, dotfiles like `.zshrc`, `.claude/`
- User mentions "chezmoi", "dotfiles", "sync configs"
- Before running `chezmoi status`, `chezmoi diff`, `chezmoi apply`
- Pulling updates from another machine
- Adding new config files to chezmoi

**Don't use for:**
- Files in project directories (`~/Code/*`) unless already managed by chezmoi (like `~/Code/CLAUDE.md`)
- Temporary files or caches

---
name: git-directory-management
description: Manage git-tracked directories correctly - never create .gitkeep files in directories that will immediately contain tracked files
---

# Git Directory Management

## When to Use This Skill

Use this skill when creating new directories in a git repository, especially when:

- Setting up project structure
- Creating plugin/package directories
- Organizing code into new folders
- Adding configuration directories

## Core Principle

**Never create `.gitkeep` files in directories you're about to populate with tracked files.**

`.gitkeep` is ONLY for keeping truly empty directories in version control.

## Pattern to Follow

### ✅ DO - Add actual files directly

```bash
# Create directory and add actual file
mkdir -p plugins/new-plugin/skills
# Now add your actual files
# (Write SKILL.md, plugin.json, etc.)
```

**Key points:**

- Git automatically tracks directories when they contain files
- Empty directory + file creation can happen in one step
- No `.gitkeep` needed - the real files track the directory

### ❌ DON'T - Create .gitkeep then immediately add files

```bash
# This is wasteful and wrong
mkdir -p plugins/new-plugin/skills
touch plugins/new-plugin/skills/.gitkeep  # ❌ Unnecessary!
git add plugins/new-plugin/skills/.gitkeep
git commit -m "Add empty directory"

# Then immediately add real files
# (Write SKILL.md)
git add plugins/new-plugin/skills/
git commit -m "Add actual skill"
```

**Why this is wrong:**

- `.gitkeep` serves no purpose if files are coming
- Creates unnecessary commits
- Clutters directory with placeholder file
- Extra file to maintain/remove later

## When to Use .gitkeep

`.gitkeep` is appropriate ONLY when:

1. **The directory must exist but remain empty**
2. **The empty directory is required for the application to function**
3. **No files will be added to the directory immediately**

**Valid use case example:**

```bash
# Application requires logs/ directory to exist on startup
mkdir -p logs
touch logs/.gitkeep
git add logs/.gitkeep
git commit -m "chore: add logs directory for runtime output"
```

**Why this is valid:**

- Directory must exist before application runs
- Directory will be populated at runtime (not in version control)
- `.gitkeep` ensures the empty directory is tracked

## Common Scenarios

### Scenario: Creating a new plugin structure

✅ **DO:**

```bash
mkdir -p plugins/new-plugin/{skills,commands}
# Then immediately create your files:
# Write plugins/new-plugin/.claude-plugin/plugin.json
# Write plugins/new-plugin/skills/skill-name/SKILL.md
# Write plugins/new-plugin/README.md
# Add all files in one commit
git add plugins/new-plugin/
git commit -m "feat: add new-plugin"
```

❌ **DON'T:**

```bash
mkdir -p plugins/new-plugin/skills
touch plugins/new-plugin/skills/.gitkeep  # ❌ Wrong!
# Then add real files later
```

### Scenario: Creating empty directories for runtime

✅ **DO:**

```bash
mkdir -p tmp/cache
touch tmp/cache/.gitkeep
git add tmp/cache/.gitkeep
git commit -m "chore: add cache directory for runtime"
```

**Why this is correct:** Cache directory must exist but contents are not tracked.

### Scenario: Setting up tool configuration directories

✅ **DO:**

```bash
mkdir -p .config/tool
# Immediately add configuration file
# Write .config/tool/config.json
git add .config/tool/config.json
git commit -m "feat: add tool configuration"
```

❌ **DON'T:**

```bash
mkdir -p .config/tool
touch .config/tool/.gitkeep  # ❌ Wrong! You're about to add config.json
```

## Decision Tree

```text
Creating a new directory?
│
├─ Will you add tracked files immediately?
│  └─ YES → No .gitkeep needed, just add the files
│
└─ Will the directory stay empty in version control?
   │
   ├─ YES, and it must exist → Use .gitkeep
   │
   └─ NO, files coming later → Wait until files exist, then commit
```

## Why It Matters

**Benefits of not using .gitkeep unnecessarily:**

- Cleaner repository (fewer placeholder files)
- Fewer commits (one commit with actual content)
- No cleanup needed later (no .gitkeep to remove)
- Clear intent (tracked files show directory purpose)

**Problems with unnecessary .gitkeep:**

- Clutters directories with meaningless files
- Creates confusing git history (empty → populated)
- Requires eventual cleanup
- Adds maintenance burden

## Quick Reference

**Rule of thumb:**

- **About to add files?** → No `.gitkeep`
- **Directory stays empty?** → Use `.gitkeep`
- **Not sure yet?** → Wait until files exist

**Remember:**

- Git tracks directories through their files
- `.gitkeep` is for truly empty directories
- One commit with actual content beats two commits (empty + populated)
- When in doubt, add the real files first

## Examples in This Repository

**Correct usage (runtime directories):**

- None currently - all directories contain tracked files

**What NOT to do:**

```bash
# ❌ DON'T create .gitkeep in plugins/tools/skills/
# This directory is meant to contain skills, not stay empty
```

**Correct approach:**

```bash
# ✅ Just add your skill directly
# Write plugins/tools/skills/new-skill/SKILL.md
git add plugins/tools/skills/new-skill/
git commit -m "feat(tools): add new-skill"
```

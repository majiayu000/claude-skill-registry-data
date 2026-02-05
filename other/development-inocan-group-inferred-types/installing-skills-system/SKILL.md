---
name: Installing Skills System
description: Fork, clone to ~/.clank, run installer, edit CLAUDE.md
when_to_use: Initial setup, installing clank for the first time
version: 2.0.0
languages: bash
---

# Installing Skills System

## Overview

Installs the clank skills repository to `~/.clank/clank` and configures Claude to use it.

**For Claude agents:** Follow the "Installation Steps for Claude" section below.

**For humans:** Follow the "Quick Install" section.

## Installation Steps for Claude

When instructed to install clank, follow these steps exactly:

### Step 1: Clone Repository

**With GitHub CLI (if available):**
```bash
mkdir -p ~/.clank
cd ~/.clank
gh repo fork obra/clank --clone --remote-name upstream
```

**Without GitHub CLI:**
```bash
mkdir -p ~/.clank
cd ~/.clank
git clone https://github.com/obra/clank.git
```

### Step 2: Run Installer

```bash
cd ~/.clank/clank
./skills/meta/installing-skills/install.sh
```

This creates symlinks for skills and commands.

### Step 3: Update CLAUDE.md

Use the Edit tool to add this XML section to the very beginning of `~/.claude/CLAUDE.md`:

```xml
<EXTREMELY_IMPORTANT>
You have a personal skills wiki at ~/.claude/skills/ with proven techniques, patterns, and tools that give you new capabilities.

STOP. Before doing ANYTHING else in this conversation, read this file: skills/getting-started

That file tells you how to find and use your skills.

ONLY after reading getting-started, are you allowed to proceed with the user's request.

CRITICAL: If a skill exists for your task, you MUST use it - even if you think you're already good at that. You're not. The skill prevents mistakes you don't know you make. SKILLS EXIST AND YOU DIDN'T USE THEM = FAILED TASK.

</EXTREMELY_IMPORTANT>
```

### Step 4: Verify Installation

```bash
ls -la ~/.claude/skills
ls -la ~/.claude/commands
~/.claude/skills/getting-started/skills-search 'test.*driven'
```

### Step 5: Restart

Tell your human partner: "Installation complete. Please restart your Claude session to pick up the new CLAUDE.md configuration."

## Quick Install (for humans)

```bash
curl -fsSL https://raw.githubusercontent.com/obra/clank/main/skills/meta/installing-skills/install.sh | bash
# Then manually add CLAUDE.md section from Step 3 above
```

## What install.sh Does

1. **Validates** you're running from clank repo root (expects ~/.clank/clank)
2. **Backs up** existing `~/.claude/skills` (if exists) to timestamped backup
3. **Creates skills symlink**: `~/.claude/skills` → `~/.clank/clank/skills`
4. **Symlinks individual commands** from `~/.clank/clank/commands/*.md` to `~/.claude/commands/`
5. **Verifies** tools available (skills-search at `~/.claude/skills/getting-started/skills-search`)
6. **Prints** CLAUDE.md XML snippet to add and verification steps

## Verification

After installation, verify it worked:

```bash
# Should show symlink to ~/.clank/clank/skills
ls -la ~/.claude/skills

# Should show individual command symlinks
ls -la ~/.claude/commands/

# Test skills-search tool
~/.claude/skills/getting-started/skills-search 'test.*driven'
```

## What Gets Installed

**Skills** (`~/.claude/skills/`):
- Library of proven techniques, patterns, and tools
- Referenced with `@` syntax in code and documentation
- Searchable with `skills-search` tool

**Commands** (`~/.claude/commands/`):
- Individual symlinks to clank command files
- Slash commands for Claude (`/brainstorm`, `/write-plan`, `/execute-plan`)
- Each command references a skill using `@` syntax
- Makes common workflows one command away

**Tools** (`~/.claude/skills/getting-started/`):
- `skills-search` - Find relevant skills using grep patterns
- Logs failed searches for gap analysis

## Why Fork?

Forking lets you:
- **Customize** skills and commands for your workflow
- **Contribute** improvements back via PR (see skills/contributing-skills)
- **Stay synced** with upstream updates (`git pull upstream main`)
- **Track** your customizations in version control

## Configure CLAUDE.md

After installation, edit your `~/.claude/CLAUDE.md` and add this section:

```xml
<extremely_important_skills_library>
You have a personal skills wiki at `~/.claude/skills/` with proven techniques, patterns, and tools that give you new capabilities.

STOP. Before doing ANYTHING else in this conversation, read this file: `skills/getting-started`

That file tells you:
- Which phrases trigger brainstorming automatically (like "I've got an idea", "Let's make...")
- How to search for skills before ANY task
- When to announce which skill you're using

After reading getting-started, proceed with the user's request.

CRITICAL: If a skill exists for your task, you MUST use it - even if you think you're already good at that. You're not. The skill prevents mistakes you don't know you make. SKILLS EXIST AND YOU DIDN'T USE THEM = FAILED TASK.
</extremely_important_skills_library>
```

This enables:
- Automatic skill discovery before every task
- Mandatory skill usage enforcement
- Gap tracking for missing skills (logged searches)

## Updating Skills

After initial install, update with:

```bash
cd ~/.clank/clank
git pull origin main    # Pull your changes
git pull upstream main  # Pull upstream updates (if configured)
```

The symlinks stay valid - no need to reinstall.

## Troubleshooting

### "Error: Not running from clank repository root"

The script expects to be run from `~/.clank/clank/`. Clone it first:
```bash
mkdir -p ~/.clank
cd ~/.clank
gh repo fork obra/clank --clone
cd clank
./skills/meta/installing-skills/install.sh
```

### "~/.claude/skills already exists"

The installer automatically backs it up with timestamp. Check backups:
```bash
ls -la ~/.claude/skills.backup.*
```

### Symlinks broken

Remove and reinstall:
```bash
rm ~/.claude/skills
rm ~/.claude/commands/*.md  # Remove individual command symlinks
cd ~/.clank/clank
./skills/meta/installing-skills/install.sh
```

## Uninstalling

```bash
# Remove symlinks
rm ~/.claude/skills
rm ~/.claude/commands/brainstorm.md
rm ~/.claude/commands/write-plan.md
rm ~/.claude/commands/execute-plan.md

# Restore backup if desired
mv ~/.claude/skills.backup.YYYY-MM-DD-HHMMSS ~/.claude/skills

# Remove from CLAUDE.md
# Delete the "Skills Library" section from ~/.claude/CLAUDE.md

# Remove cloned repo
rm -rf ~/.clank/clank
```

## Implementation

See @install.sh for the installation script.

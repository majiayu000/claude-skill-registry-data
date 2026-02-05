---
name: setup-claude-dev-kit
description: Use when setting up a new dev machine for Claude Code, onboarding to a project, or optimizing development environment - interactive installer that detects existing setup, configures shell, editor, git, templates, and quality gates with configurable enforcement
---

# Setup Claude Dev Kit

## Overview

Claude-native installer for a comprehensive developer environment. Detects existing setup and adapts accordingly - greenfield gets opinionated defaults, existing setups get respectful merges.

## When to Use

- Setting up new dev machine for Claude Code
- Onboarding to a team using Claude
- Optimizing existing development environment
- User asks about Claude dev setup, environment, or tooling

## Quick Reference

| Bundle | Components |
|--------|------------|
| minimal | shell |
| standard | shell, editor, git, templates |
| full | shell, editor, git, templates, quality, memory |

## Installation Flow

### 0. Quick Start Question (First Prompt)

**Ask immediately before anything else:**

```
Welcome to Claude Dev Kit!

How would you like to proceed?

1. 🍀 Feeling Lucky - Auto-configure everything with smart defaults
2. 🎛️  Guided Setup - Walk me through the options
```

**If "Feeling Lucky" selected:**
- Skip all subsequent prompts
- Auto-detect environment (greenfield vs adaptation)
- Install **standard** bundle (shell, editor, git, templates)
- Use these defaults:
  - Shell: Install p10k, keep existing aliases
  - Editor: Add extensions, merge settings (don't overwrite)
  - Git: Add hooks and templates, preserve existing config
  - Templates: Create CLAUDE.md if missing
  - Quality enforcement: **soft** (warns but allows bypass)
- Backup everything before changes
- Show summary at end

**Feeling Lucky behavior:**
```
🍀 Feeling Lucky mode activated!

Detecting environment... macOS, zsh, VS Code
Mode: Greenfield

Installing standard bundle:
  → Shell (zsh, powerlevel10k, fonts, aliases)
  → Editor (VS Code settings, extensions)
  → Git (hooks, templates, conventions)
  → Templates (CLAUDE.md, .claude/ directory)

Creating backups... done
Installing components... [progress]

✓ Complete! Restart your terminal to activate.
```

### 1. Detect Environment

```bash
# Check OS
uname -s  # Darwin, Linux, etc.

# Check shell
echo $SHELL
[ -d ~/.oh-my-zsh ] && echo "Oh My Zsh installed"

# Check editor
command -v code && echo "VS Code installed"
command -v cursor && echo "Cursor installed"

# Check existing customization (adaptation signals)
[ -f ~/.p10k.zsh ] && echo "Powerlevel10k configured"
[ -f ~/.gitconfig ] && echo "Git configured"
ls ~/.vscode/extensions 2>/dev/null | wc -l
```

### 2. Determine Mode

**Greenfield signals:**
- Default shell prompt (no p10k/starship/oh-my-zsh)
- No ~/.gitconfig or minimal config
- VS Code with <5 extensions
- No ~/.claude directory

**Adaptation signals:**
- Custom shell theme/prompt
- Extensive git aliases
- Editor heavily customized
- Existing dotfiles repo

### 3. Present Options

```
Detected: macOS 14.x, zsh, VS Code, [Greenfield/Adaptation] mode

Which bundle would you like?
1. Minimal - shell only (~2 min)
2. Standard - shell + editor + git + templates
3. Full - everything including quality gates
4. Custom - pick individual components
```

### 4. Install Components

For each selected component, invoke its skill:
- `setup-cdk-shell` - Shell environment
- `setup-cdk-editor` - Editor configuration
- `setup-cdk-git` - Git workflow
- `setup-cdk-templates` - Project templates
- `setup-cdk-quality` - Quality gates
- `setup-cdk-memory` - Context management

### 5. Adaptation Mode Behaviors

When existing setup detected:

1. **Backup first:**
```bash
mkdir -p ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)
cp ~/.zshrc ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/
```

2. **Show diff before changes** - Get user approval

3. **Merge, don't replace:**
```bash
# Append to .zshrc rather than overwrite
echo "# Claude Dev Kit additions" >> ~/.zshrc
```

4. **Conflict resolution:**
```
You have starship installed. We recommend powerlevel10k.
1. Keep starship (skip shell theme)
2. Try powerlevel10k (backs up starship config)
3. Skip shell setup entirely
```

### 6. Quality Gate Configuration

```
What enforcement level for quality checks?
1. Advisory - suggestions only, never blocks
2. Soft - warns but allows --no-verify bypass
3. Hard - must pass, CI enforced
```

### 7. Verify & Report

```bash
# Verify installations
command -v p10k && echo "✓ Powerlevel10k"
[ -f ~/.claude/settings.json ] && echo "✓ Claude configured"
[ -d .git/hooks ] && echo "✓ Git hooks"
```

**Generate adoption score:**
```
Environment Score: 8/10 Claude-optimized

Installed:
✓ Shell completions
✓ Powerlevel10k theme
✓ Git hooks
✓ CLAUDE.md template

Optional additions:
- Quality gates (+1)
- Memory tools (+1)
```

## Key Behaviors

- **Idempotent** - Safe to re-run, updates rather than duplicates
- **Rollback-aware** - Tracks changes, can undo if something fails
- **Progress visible** - Uses TodoWrite so user sees status
- **Non-destructive** - Backs up existing configs before modifying

## Component Skills

| Skill | Purpose |
|-------|---------|
| `setup-cdk-shell` | Zsh, p10k, fonts, completions, aliases |
| `setup-cdk-editor` | VS Code/Cursor settings, extensions |
| `setup-cdk-git` | Hooks, commit templates, PR templates |
| `setup-cdk-templates` | CLAUDE.md templates, project scaffolds |
| `setup-cdk-quality` | Linting, testing, review automation |
| `setup-cdk-memory` | Context/conversation management |

## Updating

```bash
# Check for updates
Skill: update-claude-dev-kit

# Update specific component
Skill: update-cdk-shell
```

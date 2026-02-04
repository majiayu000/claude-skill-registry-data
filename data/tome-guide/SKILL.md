---
name: tome-guide
description: How to use tome - the AI agent skill manager
author: kennyg
version: 1.0.0
globs: ["*"]
---

# Tome - AI Agent Skill Manager

Tome is a CLI tool for installing and managing skills, commands, and prompts for AI coding agents. Think of it as `npm` for AI agent knowledge.

## Quick Reference

### Installing Skills

```bash
# Install from GitHub
tome learn owner/repo

# Install specific branch/tag
tome learn owner/repo@branch

# Install globally (vs project-local)
tome learn owner/repo --global
```

### After Installing

When you install a skill that has setup requirements (like npm packages or environment variables), tome will:

1. **Detect requirements** automatically from the skill content
2. **Display them** after installation
3. **Provide a doctor command** to verify setup

Example output:
```
✓ Installed: some-skill (skill)

⚠ Detected setup requirements:
  📦 bun: some-package (line 34)
  🔑 env: API_KEY (line 12)

Run: tome doctor some-skill
```

### Checking Setup Status

```bash
# Check all artifacts with requirements
tome doctor

# Check a specific artifact
tome doctor skill-name
```

The doctor command will show:
- ✓ for satisfied requirements
- ✗ for missing requirements with install instructions

### Listing Installed Skills

```bash
# List all installed artifacts
tome list

# Skills needing setup show [needs setup] badge
```

### Other Commands

```bash
tome search "query"     # Find skills on GitHub
tome peek owner/repo    # Preview before installing
tome info skill-name    # Show skill details
tome remove skill-name  # Uninstall a skill
tome sync               # Update all installed skills
```

## When to Use Tome

Use tome when the user wants to:
- Install a skill, command, or prompt from GitHub
- Check what skills are installed
- Verify setup requirements are met
- Search for available skills
- Update installed skills

## Example Workflow

```bash
# User wants to install a plugin
tome learn 0xSero/open-orchestra

# Check what setup is needed
tome doctor open-orchestra

# After user completes setup, verify
tome doctor open-orchestra
# Should show all ✓
```

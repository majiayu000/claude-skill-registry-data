---
name: claude-config-levels
description: Use when asked to add rules, commands, skills, or config to Claude Code in this dotfiles repo. Two levels exist and scope may be ambiguous.
---

# Claude Config Levels in Dotfiles

This dotfiles repo has two Claude Code config locations with different purposes.

## The Two Levels

| Path | Symlinked To | Scope | Use For |
|------|--------------|-------|---------|
| `claude/` | `~/.claude/` | Global (all projects) | Personal preferences, commit format, work style, API rules |
| `.claude/` | (not symlinked) | This project only | Dotfiles-specific rules, audit command, file naming conventions |

## Decision Guide

**Goes in `claude/` (global):**
- Communication preferences
- Work style (ADHD, collaboration style)
- Commit message format and types
- API lookup rules
- Anything that applies to all your projects

**Goes in `.claude/` (project-local):**
- Dotfiles-specific conventions (file naming, scopes table)
- Commands like `/audit`
- Rules scoped to specific dotfiles (e.g., git-dashboard rule)
- Anything specific to managing dotfiles

## When Ambiguous, Ask

If the user asks to add a rule and the level isn't clear, ask:

> "Should this rule apply globally (all projects) or just to dotfiles?"

Examples of ambiguous requests:
- "Add a rule about X" - which level?
- "Create a command for Y" - global or local?
- "Remember that I prefer Z" - sounds global, but confirm

## File Structure

```
dotfiles/
├── claude/                    # → ~/.claude/ (GLOBAL)
│   ├── CLAUDE.md             # Global rules
│   └── rules/                # Global file-scoped rules
│       └── *.md
│
└── .claude/                   # PROJECT-LOCAL
    ├── CLAUDE.md             # Dotfiles-specific rules
    ├── commands/
    │   └── audit.md          # /audit command
    ├── rules/
    │   └── git-dashboard.md  # Scoped to fish/git-dashboard.fish
    └── skills/
        └── claude-config-levels/  # This skill
```

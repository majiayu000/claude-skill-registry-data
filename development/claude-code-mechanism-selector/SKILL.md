---
name: claude-code-mechanism-selector
description: Helps choose the right Claude Code extension mechanism (slash commands, skills, subagents, or hooks) for a given use case. Use when discussing how to extend Claude Code, automate workflows, or implement custom functionality.
---

# Claude Code Mechanism Selector

This skill helps you choose the right extension mechanism for Claude Code based on your requirements.

## Quick Decision Guide

Ask these questions to determine the best mechanism:

### 1. Does it need to run deterministically (guaranteed, not AI-decided)?
- **YES** → Use **Hooks** (shell commands at lifecycle events)
- **NO** → Continue to question 2

### 2. Does it need a separate context window or specialized AI behavior?
- **YES** → Use **Subagents** (isolated context, custom system prompts)
- **NO** → Continue to question 3

### 3. Should it activate automatically based on context?
- **YES** → Use **Skills** (model-invoked, automatic discovery)
- **NO** → Use **Slash Commands** (user-invoked with `/command`)

## Comparison Matrix

| Criteria | Slash Commands | Skills | Subagents | Hooks |
|----------|---------------|--------|-----------|-------|
| **Invocation** | User (`/cmd`) | Automatic | Automatic or explicit | System events |
| **Complexity** | Single file | Multi-file | Separate context | Shell commands |
| **Control** | Explicit | Context-based | Task-based | Deterministic |
| **Files** | `.md` only | `SKILL.md` + resources | `.md` with frontmatter | JSON config |
| **Scope** | Project or user | Project or user | Project or user | Project or user |

## When to Use Each

### Slash Commands
Best for **quick, repeatable prompts** you want explicit control over.

Examples:
- `/review` - Review code for bugs
- `/explain` - Explain code in simple terms
- `/commit` - Generate commit message

See [commands.md](commands.md) for details.

### Skills
Best for **complex capabilities** that should activate automatically.

Examples:
- PDF processing with scripts and templates
- Data analysis with reference documentation
- Code review with checklists and style guides

See [skills.md](skills.md) for details.

### Subagents
Best for **specialized tasks** requiring isolated context or custom AI behavior.

Examples:
- Code reviewer with specific review checklist
- Debugger with systematic debugging process
- Data scientist for SQL/BigQuery analysis

See [subagents.md](subagents.md) for details.

### Hooks
Best for **deterministic actions** that must always happen.

Examples:
- Auto-format code after edits (`PostToolUse`)
- Log all bash commands (`PreToolUse`)
- Block edits to sensitive files (`PreToolUse`)
- Custom notifications (`Notification`)

See [hooks.md](hooks.md) for details.

## Decision Examples

| Use Case | Best Mechanism | Why |
|----------|---------------|-----|
| "Format code after every edit" | Hooks | Deterministic, must always run |
| "Quick prompt for code review" | Slash Command | Simple, explicit invocation |
| "Comprehensive code review system" | Skill or Subagent | Complex, needs structure |
| "Isolate research from main context" | Subagent | Needs separate context window |
| "Auto-detect when to apply style guide" | Skill | Should activate automatically |
| "Log all commands for compliance" | Hooks | Must run every time, deterministic |
| "Block production file edits" | Hooks | Security rule, must be enforced |

## Combining Mechanisms

These mechanisms complement each other:

- **Skill + Subagent**: Skill provides knowledge, subagent provides isolated execution
- **Slash Command + Hook**: Command triggers workflow, hook ensures formatting
- **Subagent + Hook**: Subagent does work, hook validates output

---
name: claude-code-slash-commands
description: Create custom slash commands for Claude Code. Use when the user wants to create, generate, or build a slash command (.md file) for Claude Code, or when they ask about slash command syntax, frontmatter options, argument handling, or want help organizing their commands. Triggers on phrases like "make a slash command", "create a command for Claude Code", "write a /command", or questions about $ARGUMENTS, allowed-tools, or command frontmatter.
---

# Claude Code Slash Commands

Create custom slash commands for Claude Code as Markdown files with optional YAML frontmatter.

## Quick Reference

| Location | Scope | Description Label |
|----------|-------|-------------------|
| `.claude/commands/` | Project (shared via git) | (project) |
| `~/.claude/commands/` | Personal (all projects) | (user) |

## Command Structure

```markdown
---
allowed-tools: Tool1, Tool2(pattern:*)
argument-hint: [arg1] [arg2]
description: Brief description shown in /help
model: claude-sonnet-4-20250514
disable-model-invocation: false
---

Your prompt instructions here.
Use $ARGUMENTS for all args, or $1, $2, etc. for positional.
Reference files with @path/to/file.
Execute bash inline with !`command`.
```

## Creating Commands

### Workflow

1. Determine scope (project vs personal)
2. Choose command name (filename without .md)
3. Write frontmatter (optional but recommended)
4. Write prompt body with argument placeholders
5. Save to appropriate location

### Frontmatter Options

| Field | Purpose | Default |
|-------|---------|---------|
| `allowed-tools` | Tools the command can use | Inherits from conversation |
| `argument-hint` | Shows in autocomplete (e.g., `[file] [options]`) | None |
| `description` | Brief description for /help | First line of prompt |
| `model` | Specific model to use | Inherits from conversation |
| `disable-model-invocation` | Prevent SlashCommand tool from calling this | false |

### Arguments

**All arguments** - `$ARGUMENTS` captures everything:
```markdown
Fix issue #$ARGUMENTS following our standards
# /fix-issue 123 high-priority → "123 high-priority"
```

**Positional** - `$1`, `$2`, etc. for specific args:
```markdown
Review PR #$1 with priority $2 and assign to $3
# /review-pr 456 high alice → $1="456", $2="high", $3="alice"
```

### Bash Execution

Use `!` prefix to execute bash and include output in context:

```markdown
---
allowed-tools: Bash(git:*)
description: Create commit from staged changes
---

## Context
- Status: !`git status --short`
- Diff: !`git diff --cached`
- Branch: !`git branch --show-current`

## Task
Create a commit message for these changes.
```

**Important**: Must include `allowed-tools` with Bash permissions when using `!` commands.

### File References

Use `@` prefix to include file contents:
```markdown
Review @src/utils/helpers.js for security issues
Compare @old.js with @new.js
```

### Namespacing

Subdirectories organize commands (shown in description, not command name):
- `.claude/commands/frontend/component.md` → `/component` (project:frontend)
- `~/.claude/commands/backend/api.md` → `/api` (user:backend)

## Examples

### Simple Command
```markdown
# .claude/commands/review.md
Review this code for bugs, security issues, and style violations.
```

### With Arguments
```markdown
---
argument-hint: [issue-number]
description: Fix GitHub issue
---
# .claude/commands/fix-issue.md
Fix issue #$ARGUMENTS following our coding standards and create a PR.
```

### Git Commit Helper
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Stage and commit changes
---
# .claude/commands/commit.md

## Current State
- Status: !`git status`
- Staged diff: !`git diff --cached`
- Branch: !`git branch --show-current`

## Instructions
Create a commit. If $ARGUMENTS provided, use as message. Otherwise generate from diff.
```

### Code Generation
```markdown
---
argument-hint: [component-name]
description: Generate React component
allowed-tools: Write
---
# .claude/commands/component.md

Create a React component named $1 with:
- TypeScript
- Tailwind styling
- Unit tests
- Storybook story

Reference our patterns: @src/components/Button.tsx
```

### Multi-file Analysis
```markdown
---
description: Compare implementations
argument-hint: [file1] [file2]
---
# .claude/commands/compare.md

Compare @$1 with @$2 and identify:
1. Architectural differences
2. Performance implications
3. Suggested improvements
```

## Tips

- Keep descriptions concise (shown in /help)
- Use `argument-hint` for discoverability
- Prefer `$1`, `$2` when args have distinct roles
- Use `$ARGUMENTS` for free-form input
- Test commands with various argument patterns
- Use extended thinking keywords for complex analysis

## See Also

For complex multi-step workflows with scripts, templates, and reference docs, consider using Agent Skills instead. See references/skills-vs-commands.md.

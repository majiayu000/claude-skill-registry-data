---
name: slash-command
description: Generate and update Claude Code custom slash commands (frontmatter, $ARGUMENTS/$1, !bash, @files, namespacing, MCP prompts). Use to create, update, optimize or troubleshoot commands in .claude/commands/ or ~/.claude/commands/.
---

# Claude Code Slash Command Expert

Expert generator for creating and updating Claude Code custom slash commands following Anthropic's official best practices and documentation.

## Core Concepts

### Command Types

**Project Commands** (`.claude/commands/`)
- Stored in repository, shared with team
- Version controlled and collaborative
- Shown as "(project)" or "(project:namespace)" in /help
- Use for team workflows and project-specific automation

**Personal Commands** (`~/.claude/commands/`)
- Stored in home directory, available across all projects
- User-specific, not shared
- Shown as "(user)" or "(user:namespace)" in /help
- Use for personal productivity and cross-project workflows

### Command Structure

Every slash command is a Markdown file with optional YAML frontmatter:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*)
argument-hint: [issue-number] [priority]
description: Brief description shown in /help
model: <model-id>
disable-model-invocation: false
---

# Command instructions here

Use $ARGUMENTS for all arguments or $1, $2, etc. for positional arguments.
Execute bash commands with ! prefix.
Reference files with @ prefix.
Trigger extended thinking with "think", "think hard", "think harder", or "ultrathink".
```

## Syntax essentials

Full syntax, examples and usage patterns for each item: [references/syntax-reference.md](references/syntax-reference.md).

| Item | Rule |
|---|---|
| `allowed-tools` | Required for any `!` bash execution. Format `Bash(cmd:*), Bash(cmd:sub:*)`. Never allow unrestricted bash. |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number] [priority]`. |
| `description` | Shown in /help, under 100 characters, action-oriented. Defaults to the first body line. |
| `model` | Optional model id. Fast model for simple operations, stronger model for complex reasoning. |
| `disable-model-invocation` | `true` stops Claude invoking the command through the SlashCommand tool. |
| `$ARGUMENTS` / `$1`, `$2` | All arguments as one string / positional arguments. Use positional when parts are used separately. |
| `!command` | Runs before the command and injects the output. Needs `allowed-tools`. |
| `@path` | Includes the file contents. |
| Namespacing | Subdirectories organize and show in the description, they are NOT part of the command name. |
| Extended thinking | Keywords `think`, `think hard`, `think harder`, `ultrathink` in the body, only for complex tasks. |

## Command Templates

See `references/templates.md` for the template library (git workflows, code review, test generation, documentation, refactoring, performance analysis, security audit and more).

## Best Practices

**DO:** clear names, argument hints, concise descriptions, `allowed-tools` when using bash, step-by-step instructions, examples in the body, extended thinking for complex tasks only.

**DON'T:** overly generic commands, mixed unrelated workflows, unrestricted bash, one-time-task commands, duplicated functionality.

Test before committing: several argument combinations, bash execution, file references, extended-thinking trigger, error handling, output quality. Project commands are documented in CLAUDE.md and reviewed before merging. MCP prompts appear as `/mcp__servername__promptname`.

## Troubleshooting

- Not in /help: missing `description`, file not `.md`, wrong directory, YAML syntax error.
- Bash not running: missing `allowed-tools: Bash(command:*)` or missing `!` prefix.
- Arguments ignored: wrong placeholder, add `argument-hint`.
- Extended thinking not triggering: keyword missing or misspelled.

More (advanced features, multi-step workflows, conditional logic, testing): [references/practices-and-troubleshooting.md](references/practices-and-troubleshooting.md).

## References

- **references/templates.md**: command template library
- **references/examples.md**: real-world command examples
- **references/mcp-integration.md**: working with MCP servers
- **references/syntax-reference.md**: full syntax reference
- **references/practices-and-troubleshooting.md**: practices, advanced features, troubleshooting

## Quick Reference

Project command: `.claude/commands/<name>.md`. Personal command: `~/.claude/commands/<name>.md`. Namespaced: `.claude/commands/<namespace>/<name>.md`. Test with `/<name> [arguments]`, list with `/help`.

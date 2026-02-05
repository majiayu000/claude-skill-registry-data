---
name: creating-commands
description: Expert knowledge on creating slash commands for Claude Code. Use when designing or creating slash command .md files, understanding command arguments, or implementing bash execution.
allowed-tools: Read, Grep, Glob
---

# Creating Slash Commands

This Skill provides comprehensive knowledge about creating effective slash commands in Claude Code.

## What Are Slash Commands?

Slash commands are user-invoked operations that start with `/`. When executed, they expand to a full prompt that Claude processes. They're different from subagents (which are automatically invoked) - slash commands require explicit user action.

**Critical Insight - Thin Wrappers**: The best practice for slash commands is to treat them as **thin wrappers** or **triggers** that activate Skills. The command file itself should NOT contain complex workflow logic - that belongs in a SKILL.md file. Commands are simply user-friendly aliases that point to specific skills or workflows.

**Command → Skill → (Subagent)**: This is the ideal flow:
1. User invokes `/command`
2. Command activates a specific Skill
3. Skill (the "playbook") guides the agent through the process
4. Agent may delegate to subagents as needed

## Plugin System Integration (October 2025)

As of October 2025, **plugins are the standard way to bundle and share slash commands**.

### What Are Plugins?

Plugins bundle multiple components together:
- Slash commands
- Subagents
- MCP servers
- Hooks
- Skills

### Installing Command Plugins

```bash
/plugin marketplace add <url>    # Add plugin source
/plugin install <name>           # Install plugin
/plugin list                     # Show installed plugins
/plugin uninstall <name>         # Remove plugin
```

### Creating Commands in Plugins

Commands in plugins work identically to standalone commands:
- Same YAML frontmatter
- Same argument patterns
- Same bash execution

**Benefit**: Version control, selective activation, easier distribution across teams.

**See**: Official plugin documentation for creating distributable command collections.

## File Structure

**Project commands**: `.claude/commands/{command-name}.md`
**Personal commands**: `~/.claude/commands/{command-name}.md`

**Format**:
```yaml
---
description: Brief description of what this command does
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Bash(git:*), Read, Write  # Optional
model: haiku  # Optional
disable-model-invocation: false  # Optional
---

Command prompt that Claude will execute.
Can use $ARGUMENTS or $1, $2, $3, etc.
```

## YAML Frontmatter Fields

### Optional Fields (All Are Optional)

**description** (string)
- Brief description shown in `/help`
- If omitted, uses first line of prompt
- Keep concise (one sentence)

**argument-hint** (string)
- Shows expected arguments in autocomplete
- Examples: `[filename]`, `[message]`, `add [tag] | remove [tag]`
- Helps users know what to provide

**allowed-tools** (comma-separated string)
- Tools this command can use
- If omitted, inherits from conversation
- Use for command-specific restrictions

**model** (string)
- Specific model: `sonnet`, `opus`, `haiku`
- If omitted, inherits from conversation
- Use `haiku` for simple/fast commands

**disable-model-invocation** (boolean)
- If `true`, prevents SlashCommand tool from calling this command
- Default: `false`
- Use to keep commands user-only

## Command Arguments

### Using $ARGUMENTS (All Arguments)

Captures everything after the command name:

```yaml
---
description: Fix issue following coding standards
---

Fix issue #$ARGUMENTS following our coding standards
```

Usage:
```
/fix-issue 123 high-priority
# $ARGUMENTS becomes "123 high-priority"
```

### Using $1, $2, $3 (Positional Arguments)

Access specific arguments individually:

```yaml
---
description: Review PR with priority and assignee
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

Usage:
```
/review-pr 456 high alice
# $1="456", $2="high", $3="alice"
```

### @-Mention Support (August 2025)

Commands support **@-mentions** in arguments with typeahead support:

**File References:**
```bash
/review-pr @src/components/Header.tsx
/analyze @tests/test_auth.py
```

**Agent References:**
```bash
/delegate @agent:security-expert
/consult @agent:code-reviewer
```

**Benefits:**
- Typeahead completion for file paths
- Clear intent (@ signals reference)
- Works with glob patterns: `@src/utils/*.js`

**In Command Prompt:**
```yaml
---
description: Review specific files
argument-hint: [@file-path]
---

Review the implementation in $1

Focus on code quality, security, and maintainability.
```

**Usage**: `/review-files @src/auth.ts @tests/test_auth.ts`

### When to Use Which

**Use $ARGUMENTS**:
- Flexible, variable-length input
- Natural language descriptions
- Unknown number of args

**Use $1, $2, $3**:
- Fixed structure
- Specific fields needed
- Build complex prompts with arg positioning

## Bash Command Execution

Execute bash commands before the prompt runs using `!` prefix.

### Basic Execution

```yaml
---
allowed-tools: Bash(git:*)
---

## Current Status

Git status: !`git status`

## Your Task

Based on the above status, create a commit.
```

The `!` commands run first, output is included in prompt context.

### Multiple Commands

```yaml
---
allowed-tools: Bash(git:*), Bash(docker:*)
---

## Context

- Git status: !`git status`
- Docker status: !`docker ps`
- Current branch: !`git branch --show-current`

## Task

Deploy the current branch.
```

### Required: allowed-tools

**Must** include Bash tool permissions:

```yaml
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

Current changes: !`git diff HEAD`
```

Specify exact commands or use wildcards:
- `Bash(git:*)` - All git commands
- `Bash(git status:*), Bash(git diff:*)` - Specific commands only

## File References

Include file contents using `@` prefix:

```yaml
---
description: Review implementation
---

Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js
```

When command runs, files are automatically included in context.

## Extended Thinking

Trigger extended thinking by including keywords:

```yaml
---
description: Solve complex algorithm problem
---

Think carefully about this algorithm optimization problem: $ARGUMENTS

Consider multiple approaches before implementing.
```

Keywords that trigger thinking: "think carefully", "consider", "analyze deeply"

## Commands and Skills Integration

**Best Practice**: Commands should activate Skills, not replace them.

### The Thin Wrapper Pattern

**Good - Command activates a Skill**:
```yaml
---
description: Run comprehensive code review
---

Activate the code-review-process Skill and review the current changes.
```

The actual review process (checklist, steps, output format) lives in `.claude/skills/code-review-process/SKILL.md`, not in the command file.

**Bad - Command contains the entire process**:
```yaml
---
description: Run comprehensive code review
---

Review the code changes following these steps:
1. Check code style
2. Verify error handling
3. Look for security issues
[... 50 more lines of detailed process ...]
```

This defeats modularity and makes the process hard to maintain.

### Why This Matters

- **Reusability**: Skills can be invoked by multiple commands or automatically by Claude
- **Maintainability**: Update the process once in SKILL.md, not in every command
- **Clarity**: Commands = user interface, Skills = implementation
- **Modularity**: Skills can reference other skills, creating composable workflows

## Programmatic Command Invocation (SlashCommand Tool)

Claude can **automatically invoke your commands** during conversations using the SlashCommand tool.

### How It Works

When you create a command with a populated `description` field, Claude can:
1. See the command in its tool list
2. Invoke it programmatically when relevant
3. Get the expanded prompt as input

**Example:**
```yaml
---
description: Run all tests and report failures
---

Run the complete test suite and analyze failures.
```

Claude might invoke this automatically when user says: "Make sure everything still works"

### Requirements

**Must Have:**
- `description` field populated (commands without descriptions are invisible)
- Under 15,000 character budget (see below)

**Optional:**
- `disable-model-invocation: true` - Prevents automatic invocation (user-only command)

### Character Budget Limit

Claude can only see commands that fit within `SLASH_COMMAND_TOOL_CHAR_BUDGET` (default: 15,000 characters).

**Managing Budget:**
- Keep command prompts concise
- Use `disable-model-invocation: true` for internal/debug commands
- Increase limit in settings.json if needed:

```json
{
  "SLASH_COMMAND_TOOL_CHAR_BUDGET": 30000
}
```

### Best Practices

**Enable Automatic Invocation:**
- Clear, specific descriptions
- Common user phrases as triggers
- Thin wrappers to skills

**Disable Automatic Invocation:**
- Internal/debug commands
- Dangerous operations (deploy, delete)
- Commands needing explicit human approval

**Encouraging Usage:**
Reference commands in CLAUDE.md:
```markdown
To commit changes: Execute /commit command
For code review: Use /review command
```

This helps Claude map natural language → commands.

## Command Patterns

Seven main patterns have emerged for effective slash commands:

1. **Simple Action** - Single operation (run tests, build project)
2. **Context Gathering** - Collect and present information (status, review prep)
3. **Workflow** - Multi-step sequences (branch creation, PR automation)
4. **Validation** - Pre-flight checks (pre-commit, pre-deploy)
5. **Generation** - Create code/files (scaffolding, boilerplate)
6. **Skill Activation** - Thin wrapper to skill (complex workflows)
7. **Context Pollution Prevention** - Delegate massive outputs to subagents

**See [patterns.md](patterns.md) for detailed explanations, examples, and when to use each pattern.**

## Tool Restrictions and Model Selection

**Tool Restriction Patterns**:
```yaml
# Read-only
allowed-tools: Read, Grep, Glob

# Git only
allowed-tools: Bash(git:*)

# Multiple specific tools
allowed-tools: Bash(git:*), Bash(npm:*), Bash(pytest:*)
```

**Model Selection**:
- `model: haiku` - Fast, cheap (simple commands)
- Omit model field - Uses conversation model (default)
- `model: opus` - Complex reasoning

**See [reference.md](reference.md) for detailed bash execution patterns, security considerations, and troubleshooting.**

## Examples

**Quick Example - Thin Wrapper to Skill**:
```yaml
---
description: Run comprehensive code review
---

Activate the code-review-process Skill and review the current changes.
```

This demonstrates the thin wrapper pattern - the command is minimal, and the actual review process lives in a skill.

**See [examples.md](examples.md) for 7 detailed, real-world command examples covering all major patterns.**

## Command Organization

**Flat** (< 10 commands): All in `.claude/commands/`
**Subdirectories** (organized): Use `git/`, `testing/` folders for grouping

Note: Subdirectories don't affect command names - `/create-branch` works regardless of location.

## Best Practices

1. **Thin Wrappers** - Complex logic in skills, not commands
2. **Clear Descriptions** - "Run all tests and report failures" not "Tests"
3. **Argument Hints** - `[pr-number] [priority]` not `[args]`
4. **Specific Tools** - `Bash(git:*)` not `Bash(*)`
5. **Context First** - Gather info with `!` before instructions
6. **Heredocs** - Use for commit messages to prevent injection

## Testing and Troubleshooting

**Testing Methods**:
1. Manual invocation: `/your-command arg1 arg2`
2. Verify argument substitution: Check $1, $2 work
3. Test bash execution: Verify `!` commands run

**Common Issues**:
- Command not found → Check filename, restart Claude Code
- Arguments not substituting → Use $1 in content, not frontmatter
- Bash not running → Add `allowed-tools: Bash(...)`
- Permission denied → Check tool permissions

**See [reference.md](reference.md) for complete troubleshooting guide with diagnose and fix steps.**

## Validation Checklist

Before finalizing a command:

- [ ] Description is clear and concise
- [ ] Argument hints provided (if using args)
- [ ] Tool permissions specified (if using tools)
- [ ] Arguments use proper format ($ARGUMENTS or $1, $2, etc.)
- [ ] Bash commands have `!` and backticks
- [ ] Bash permissions match commands used
- [ ] Heredocs used for multi-line strings
- [ ] File tested with sample arguments

## Summary

**Essential Elements**:
1. Clear description (what it does)
2. Argument hints (what to provide)
3. Proper argument substitution ($ARGUMENTS or $1-$9)
4. Tool permissions (if using tools)
5. Context gathering (using `!` for bash)

**Success Criteria**:
- Command shows in `/help`
- Arguments substitute correctly
- Bash commands execute
- Claude produces expected result
- Tool permissions work

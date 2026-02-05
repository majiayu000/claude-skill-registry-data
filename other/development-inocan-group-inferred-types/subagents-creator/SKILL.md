---
name: subagents-creator
description: Guide for creating Claude Code subagents (custom agents) - specialized AI assistants with isolated context. Use when the user wants to create, add, or configure a subagent/custom agent for Claude Code.
---

# Subagents Creator

Create Claude Code subagents - specialized AI assistants that run in isolated context windows.

## What Subagents Provide

| Benefit | Description |
|---------|-------------|
| Context Isolation | Each subagent has its own context, preventing main conversation pollution |
| Specialized Expertise | Fine-tuned instructions for specific domains |
| Reusability | Use across projects, share with team |
| Flexible Permissions | Different tool access per subagent |
| Parallelization | Multiple subagents can run concurrently |

## Workflow

### Step 1: Determine Subagent Requirements

Ask the user:
1. **What should this subagent do?** (its specialty/purpose)
2. **What tools does it need?** (see Available Tools below)
3. **When should it be triggered?** (automatic vs explicit invocation)

### Step 2: Determine Installation Scope

Ask where to install the subagent:

| Scope | Path | Use Case |
|-------|------|----------|
| Project | `.claude/agents/` | Team-shared, committed to git |
| User global | `~/.claude/agents/` | Personal agents for all projects |
| User profile | `~/.claude-<profile>/agents/` | Profile-specific agents |

For user-level agents, ask which profile or if using default `~/.claude/`.

### Step 3: Create the Subagent

#### File Format

Create a Markdown file with YAML frontmatter:

```markdown
---
name: agent-name
description: When this agent should be invoked. Use "proactively" to encourage automatic use.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Your agent's system prompt goes here. Define its role, capabilities,
approach, and any specific instructions or constraints.
```

#### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase with hyphens (e.g., `code-reviewer`) |
| `description` | Yes | When to invoke. Include "proactively" or "MUST BE USED" to encourage automatic delegation |
| `tools` | No | Comma-separated list. Inherits all tools if omitted |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit`. Default: `sonnet` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | No | Comma-separated skill names to auto-load |

### Step 4: Write Effective Prompts

Include in the system prompt:
1. **Role definition** - Who the agent is
2. **Trigger behavior** - What to do when invoked
3. **Process/checklist** - Steps to follow
4. **Output format** - How to present results
5. **Constraints** - What NOT to do

See `references/examples.md` for complete working examples.

## Available Tools

**Read-Only:**
- `Read` - Read file contents
- `Glob` - File pattern matching
- `Grep` - Content search with regex

**Execution:**
- `Bash` - Shell commands
- `Edit` - Targeted file edits
- `Write` - Create/overwrite files

**Search:**
- `WebFetch` - Fetch URL content
- `WebSearch` - Web searches

**Other:**
- `Skill` - Execute skills
- `SlashCommand` - Run slash commands

**NOT Available:** `Task` (prevents nested agent spawning)

## Built-In Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| general-purpose | Sonnet | All | Complex multi-step tasks |
| Plan | Sonnet | Read, Glob, Grep, Bash (read-only) | Codebase research in plan mode |
| Explore | Haiku | Glob, Grep, Read, Bash (read-only) | Fast codebase searching |

## Invocation Methods

1. **Automatic** - Claude delegates based on task matching `description`
2. **Explicit** - User mentions agent: "Use the code-reviewer agent..."
3. **CLI flag** - `claude --agents '{...}'` for session-only agents

## Best Practices

1. **Focused purpose** - Single clear responsibility per agent
2. **Detailed prompts** - Include specific instructions, examples, constraints
3. **Minimal tools** - Only grant necessary tools
4. **Action-oriented descriptions** - Help Claude match tasks appropriately
5. **Version control** - Commit project agents for team sharing

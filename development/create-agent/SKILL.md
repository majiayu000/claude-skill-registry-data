---
name: create-agent
short: Create Claude Code agents with proper structure
description: Create a new Claude Code agent with proper YAML frontmatter structure. Use when the user wants to add a specialized agent to a plugin. Handles agent file creation with name, description, tools, model selection, and color configuration.
when: User wants to create a new agent, add a specialized agent to a plugin, or asks how to define an agent
---

# Create Agent Skill

Create new Claude Code agents with proper configuration and structure.

## Agent File Format

Agents are markdown files in the `agents/` directory with YAML frontmatter:

```markdown
---
name: agent-name
short: Brief 5-8 word description
description: Full description of what the agent does
when: Semantic activation - describe when to use this agent
tools: Glob, Grep, Read, Write, Edit, Bash, WebFetch, WebSearch, TodoWrite
model: sonnet
color: green
---

# Agent Title

Agent prompt content goes here...
```

## Required Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Unique identifier (kebab-case) | `code-reviewer` |
| `description` | One-line summary of agent's purpose | `Reviews code for quality and best practices` |
| `tools` | Comma-separated list of available tools | `Glob, Grep, Read, Write, Edit, Bash` |
| `model` | Model to use: `opus`, `sonnet`, or `haiku` | `sonnet` |
| `color` | Status line color | `green`, `blue`, `purple`, `red`, `orange`, `cyan`, `magenta`, `yellow`, `pink`, `teal`, `violet` |

## Optional Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `short` | Brief 5-8 word summary for index display | `Reviews code for security and quality` |
| `when` | Semantic activation trigger for index display | `User wants code reviewed, needs security audit, or asks about code quality` |

**Note**: `short` and `when` are used for forge-index display. The `description` field is used by Claude Code for agent invocation.

## Model Selection Guidelines

- **opus**: Strategic decisions, complex architecture, security-critical, compliance, executive-level analysis
- **sonnet**: Technical implementation, code writing, general development tasks (most common)
- **haiku**: Quick lookups, simple transformations, fast responses

## Available Tools

Common tool combinations by agent type:

### Code Development Agents
```
Glob, Grep, Read, Write, Edit, Bash, TodoWrite
```

### Research/Analysis Agents
```
Glob, Grep, Read, WebFetch, WebSearch, TodoWrite
```

### Full-Featured Agents
```
Glob, Grep, Read, Write, Edit, Bash, WebFetch, WebSearch, TodoWrite
```

## Creation Process

1. Determine the agent's purpose and expertise area
2. Choose appropriate model based on complexity
3. Select tools needed for the agent's tasks
4. Write clear, actionable agent prompt
5. Save to `plugins/<plugin-name>/agents/<agent-name>.md`

## Example Agent

```markdown
---
name: code-reviewer
short: Reviews code for security and quality
description: Reviews code changes for quality, security, and best practices
when: User wants code reviewed, needs security audit, or asks about code quality
tools: Glob, Grep, Read, TodoWrite
model: sonnet
color: yellow
---

# Code Reviewer Agent

You are an expert code reviewer focused on quality, security, and maintainability.

## Review Checklist

- Code correctness and logic
- Security vulnerabilities
- Performance considerations
- Code style and consistency
- Test coverage
- Documentation

## Output Format

Provide structured feedback with:
1. Summary of changes
2. Issues found (categorized by severity)
3. Recommendations
4. Approval status
```

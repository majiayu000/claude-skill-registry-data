---
name: subagent-creator
description: Guide for creating effective subagents (custom agents). Use when users want to create a new subagent that can be dispatched via Task tool for autonomous work. Covers frontmatter fields (name, description, tools, model, permissionMode, skills), prompt design, and when to use subagents vs skills.
---

# Subagent Creator

Create effective subagents that handle autonomous tasks via the Task tool.

## Subagents vs Skills

| Aspect | Subagent | Skill |
|--------|----------|-------|
| **Invocation** | Explicit via Task tool | Auto-triggered by context |
| **Context** | Isolated (fresh context window) | Shared with parent |
| **Complexity** | Single .md file | Folder with resources |
| **Use case** | Autonomous discrete tasks | Guidance and procedures |
| **Nesting** | Cannot spawn other subagents | Can reference other skills |

**Use subagent when:**
- Task is discrete and autonomous
- Fresh context window is beneficial
- Task can run in parallel with other work
- Specialized tool restrictions needed

**Use skill when:**
- Guidance needed throughout conversation
- Context sharing is important
- Multiple resources (scripts, references) needed

## Subagent Structure

```
agents/
└── agent-name.md
    ├── YAML frontmatter (metadata)
    └── Markdown body (system prompt)
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens only (e.g., `code-reviewer`) |
| `description` | Yes | When to use - this triggers dispatch decisions |
| `tools` | No | Comma-separated: `Bash, Glob, Grep, Read, Edit, Write` |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default: inherit) |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | No | Comma-separated skills to auto-load |

### Tools Reference

```
Read-only:     Glob, Grep, Read, WebFetch, WebSearch
Write:         Edit, Write, NotebookEdit
Execute:       Bash
All:           * (or omit field)
```

### Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Normal permission prompts |
| `acceptEdits` | Auto-accept file edits |
| `bypassPermissions` | Skip all permission prompts |
| `plan` | Plan mode - explore but don't modify |

## Writing Effective Prompts

### Structure

```markdown
---
name: agent-name
description: When to use this agent. Be specific about triggers.
tools: Tool1, Tool2
model: sonnet
---

# Agent Name

One-line role description.

## Input Required
What the agent expects to receive.

## Process
Step-by-step what the agent does.

## Output Format
Exact format of the response.

## Rules
- Constraints and boundaries
- What to avoid
```

### Best Practices

1. **Be specific about role** - First line defines identity
2. **Define clear inputs** - What must be provided
3. **Structure the process** - Numbered steps
4. **Specify output format** - Use code blocks for templates
5. **Set boundaries** - What NOT to do

### Description Guidelines

The `description` field triggers when the agent is suggested. Include:
- Primary use case
- Required inputs
- Expected output type

```yaml
# Good
description: Use after completing a task to review code changes. Provide BASE_SHA, HEAD_SHA, and requirements. Returns issues with file:line references.

# Bad
description: Reviews code.
```

## Examples

### Minimal Subagent

```markdown
---
name: summarizer
description: Use to summarize long documents or conversations. Provide the content to summarize.
tools: Read
model: haiku
---

# Summarizer

Summarize the provided content in 3-5 bullet points.

Focus on: key decisions, action items, conclusions.
Skip: greetings, filler, obvious context.
```

### Full Subagent

See `references/subagent-examples.md` for complete examples.

## Creation Process

1. **Define the task** - What autonomous work does this agent do?
2. **Choose tools** - Minimum needed (prefer restrictive)
3. **Choose model** - haiku for simple, sonnet for complex, opus for critical
4. **Write prompt** - Role, process, output, rules
5. **Test** - Dispatch via Task tool, iterate

### Init Script

```bash
scripts/init_subagent.py <agent-name> --path <output-directory>
```

Creates template agent file with proper structure.

## Anti-Patterns

- **Too broad** - Agent tries to do everything
- **Too many tools** - Give minimum necessary
- **Vague output** - Always specify exact format
- **No boundaries** - Must define what NOT to do
- **Wrong model** - Don't use opus for simple tasks

---
name: subagent-creator
description: "Create new Claude Code custom agents (subagents). Use when: (1) User wants to create a new custom agent, (2) User says 'create agent', 'new agent', 'make subagent', (3) User wants a specialized agent for delegation. Covers agent file format, YAML frontmatter, tool restrictions, model selection, permission modes, persistent memory, placement."
---

# Create Custom Agent

## Agent File Format

Custom agents are **Markdown files with YAML frontmatter** stored in:

| Location | Scope |
|----------|-------|
| `$HOME/.claude/agents/` | All projects (personal) |
| `.claude/agents/` | Current project only |

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters and hyphens identifier |
| `description` | Yes | What the agent does. Claude uses this to decide when to delegate |
| `model` | No | `sonnet`, `opus`, `haiku`, `fable`, a full model ID (e.g. `claude-opus-4-8`), or `inherit` (default) — prefer `inherit` so the agent tracks the session model (currently Fable 5, a tier above Opus) |
| `tools` | No | Allowlist of tools. Inherits all if omitted. Use `Task(agent-name)` to restrict subagent spawning |
| `disallowedTools` | No | Denylist of tools |
| `permissionMode` | No | `default`, `acceptEdits`, `delegate`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Max agentic turns before stopping |
| `skills` | No | Skills to preload at startup |
| `mcpServers` | No | MCP servers available to agent |
| `hooks` | No | Lifecycle hooks scoped to agent |
| `memory` | No | `user`, `project`, or `local` - persistent memory across sessions |
| `color` | No | Color for UI display |

## Workflow

### Step 1: Understand the agent's purpose

Ask user:

- What tasks should this agent handle?
- Should it be personal (`$HOME/.claude/agents/`) or project-scoped (`.claude/agents/`)?
- Does it need write access or is it read-only?

### Step 2: Choose appropriate settings

**Model selection:**

`opus` is not the top of the overall lineup (`fable` / the session model, currently Fable 5, sits above it) — when the agent should track whatever model is driving the session rather than being pinned, prefer `inherit` over hardcoding a model.

- `opus` - Complex reasoning, code review, architecture decisions
- `sonnet` - General development, balanced speed/quality
- `haiku` - Fast simple tasks, formatting, quick lookups

**Tool restrictions:**

- Read-only agent: `tools: Read, Grep, Glob`
- Developer agent: omit `tools` (inherits all)
- No web access: `disallowedTools: WebFetch, WebSearch`

**Key constraints:**

- Subagents CANNOT spawn other subagents (no nesting)
- Keep the body focused - it becomes the agent's system prompt

**Path safety -- NEVER use `~` in agent instructions:**

- WARNING: `~` (tilde) is only expanded by interactive shells. It is NOT expanded by Node.js `fs` operations, non-login shell contexts, or most programmatic file APIs. Using `~` in file paths passed to `fs.writeFileSync`, `fs.mkdirSync`, etc. will create a literal directory named `~` inside the working directory
- In agent instructions, ALWAYS write `$HOME` instead of `~` for home directory paths. For example: `$HOME/cclogs/...` not `~/cclogs/...`, `$HOME/.claude/...` not `~/.claude/...`
- This applies to all file paths in the agent body: log directories, config paths, output directories, temp file locations, etc.

### Step 3: Create the agent file

Template:

```markdown
---
name: agent-name
description: One sentence describing when Claude should delegate to this agent
model: sonnet
tools: Read, Grep, Glob, Bash
---

You are a specialized [role]. [Core instruction in 1-2 sentences.]

## Responsibilities

[What this agent does - keep concise]

## Workflow

[Step-by-step procedure if applicable]
```

### Step 4: Format the agent file

Format the created agent file using the mdx-formatter to ensure consistent markdown formatting:

```bash
pnpm dlx @takazudo/mdx-formatter --write <path-to-agent-file.md>
```

### Step 5: Verify

After creating the file, verify:

1. File is at the correct location
2. YAML frontmatter parses correctly (no syntax errors)
3. Description clearly indicates when to use the agent

## Examples

### Read-only code explorer

```yaml
---
name: code-explorer
description: Explore and explain codebase architecture and patterns
tools: Read, Grep, Glob
model: sonnet
---

You are a codebase explorer. Analyze code structure,
explain architecture, and find patterns.
```

### Developer with memory

```yaml
---
name: project-dev
description: Project-aware developer that learns conventions over time
model: opus
memory: project
---

You are a developer for this project. Maintain memory of
conventions, patterns, and architectural decisions.
```

## Reference

- Agents are used via Task tool's `subagent_type` parameter
- Skills can use agents via `context: fork` + `agent: agent-name`
- Run directly: `claude --agent agent-name`

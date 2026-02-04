---
name: intermediate
description: |
  Claude Code customization for comfortable users. Covers skills, commands, MCP, hooks.
  Use when: user knows basics and wants to customize Claude Code.
---

# Intermediate: Customization

Extend Claude Code with your own skills, commands, and integrations.

## Curriculum

| # | Topic | Reference |
|---|-------|-----------|
| 1 | Custom Skills | `custom-skills.md` |
| 2 | Plugin Structure | `plugin-structure.md` |
| 3 | MCP Servers | `mcp-basics.md` |
| 4 | Hooks | `hooks.md` |

## Teaching Pattern

```
1. CONCEPT   → What it is, why you'd use it
2. STRUCTURE → Files and format
3. EXAMPLE   → Real working code
4. EXERCISE  → Build one yourself
5. VERIFY    → Test it works
```

## Topic Details

### 1. Custom Skills

Key points:
- Skills = reusable instruction sets
- Structure: `SKILL.md` with frontmatter + content
- Can include references/ and scripts/
- Triggered by keywords or explicit invocation

Exercise: Create a skill for your common workflow

Reference: `custom-skills.md`

### 2. Plugin Structure

Key points:
- Plugins bundle skills, commands, agents
- `marketplace.json` defines contents
- Can be shared or sold via marketplace
- Local plugins in `.claude/`

Exercise: Create a mini plugin with 1 skill + 1 command

Reference: `plugin-structure.md`

### 3. MCP Servers

Key points:
- MCP = Model Context Protocol
- Connects Claude to external tools/data
- Examples: databases, APIs, file systems
- Configure in `.mcp.json` or settings

Exercise: Set up an MCP server (filesystem or sqlite)

Reference: `mcp-basics.md`

### 4. Hooks

Key points:
- Hooks run code at specific events
- SessionStart, PreToolUse, PostToolUse, etc.
- Can validate, log, or transform
- Configure in settings.json

Exercise: Create a SessionStart hook that logs time

Reference: `hooks.md`

## Completion Criteria

User has completed Intermediate when they can:

- [ ] Create a working skill with frontmatter
- [ ] Build a command that uses $ARGUMENTS
- [ ] Explain what MCP does (even if not configured)
- [ ] Describe when hooks are useful

## Transition to Advanced

When complete, offer:
```
"Nice work! You can now customize Claude Code.

Ready for Advanced? Next level covers:
- Building custom agents (subagents)
- Complex multi-skill workflows
- Publishing plugins to marketplace

Say 'yes' or /cc:level advanced to continue."
```

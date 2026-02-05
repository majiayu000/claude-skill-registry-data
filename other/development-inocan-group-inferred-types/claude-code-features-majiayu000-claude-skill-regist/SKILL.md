---
name: claude-code-features
description: Explains Claude Code's extensibility features (skills, slash commands, hooks, MCP servers, settings, CLAUDE.md). Use when the user asks about Claude Code capabilities, how to set up custom commands, how to create skills, how to configure hooks, MCP server integration, or any meta-questions about Claude Code itself like "can you do X" or "how do I make you do Y".
---

# Claude Code Features Guide

## Purpose

This skill activates when discussing Claude Code's extensibility and configuration features. It ensures accurate, actionable guidance rather than guessing.

## The Five Pillars of Claude Code Extensibility

### 1. Skills (`.claude/skills/`)

**What they are:** Markdown documents that expand Claude's capabilities with domain knowledge, workflows, or specialized instructions.

**Structure:**

```
.claude/skills/{skill-name}/
├── SKILL.md          # Required - contains frontmatter + instructions
└── reference.md      # Optional - supporting documentation
```

**SKILL.md Format:**

```markdown
---
name: my-skill-name
description: Brief description. Include trigger keywords for automatic activation.
allowed-tools: Read, Grep # Optional: restrict to specific tools
---

# Skill Title

## Instructions

Step-by-step guidance for Claude when this skill is active.

## Examples

Concrete usage examples.
```

**How they trigger:** Claude autonomously decides to use skills based on matching the user's request to the skill's description. Good descriptions = reliable activation.

**Location options:**

- `~/.claude/skills/` — Personal skills (all projects)
- `.claude/skills/` — Project skills (team-shared, committed to git)

---

### 2. Slash Commands (`.claude/commands/`)

**What they are:** Markdown files that define reusable prompts invoked with `/command-name`.

**Structure:**

```
.claude/commands/
├── my-command.md           # Invoked as /my-command
└── folder/sub-command.md   # Invoked as /folder:sub-command
```

**Command file format:**

```markdown
---
description: What this command does (shown in command list)
---

Your prompt content here. This expands when the user types /command-name.

You can use $ARGUMENTS to capture user input after the command.
```

**Special variables:**

- `$ARGUMENTS` — Everything typed after the command name
- `{{file_path}}` — Prompt user for a file path
- `{{user_input}}` — Prompt user for text input

**Location options:**

- `~/.claude/commands/` — Personal commands
- `.claude/commands/` — Project commands

---

### 3. Hooks (`.claude/settings.local.json`)

**What they are:** Shell scripts that run automatically before/after Claude uses tools.

**Hook types:**

- `PreToolUse` — Runs before a tool executes (can block with exit code 2)
- `PostToolUse` — Runs after a tool executes
- `Notification` — Runs when Claude sends notifications
- `Stop` — Runs when Claude stops (turn completion, interrupt, error)

**Configuration in settings.local.json:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/my-hook.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Environment variables available to hooks:**

- `CLAUDE_TOOL_NAME` — Name of the tool being used
- `CLAUDE_TOOL_INPUT` — JSON of tool parameters
- `CLAUDE_TOOL_OUTPUT` — (PostToolUse only) Tool result

**Blocking behavior:** Exit code 2 blocks the tool; stdout becomes the block reason shown to Claude.

---

### 4. MCP Servers

**What they are:** External servers that provide additional tools to Claude via the Model Context Protocol.

**Configuration in settings.json:**

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

**Common MCP servers:**

- `@modelcontextprotocol/server-filesystem` — Enhanced file operations
- `@modelcontextprotocol/server-github` — GitHub API integration
- `@modelcontextprotocol/server-postgres` — Database queries
- `@anthropics/claude-code-mcp-server` — Claude Code specific tools

**Location options:**

- `~/.claude/settings.json` — Global MCP servers
- `.claude/settings.json` — Project-specific servers

---

### 5. CLAUDE.md Files

**What they are:** Markdown files that provide context and instructions to Claude.

**Hierarchy (all are read, in order):**

1. `~/.claude/CLAUDE.md` — Personal global instructions
2. `~/CLAUDE.md` — User home directory
3. `{project}/CLAUDE.md` — Project root (most common)
4. `{project}/{subdir}/CLAUDE.md` — Subdirectory-specific context

**Best practices:**

- Keep focused on immutable truths (architecture, conventions, patterns)
- Avoid transient information (status, versions, URLs)
- Use for coding standards, project structure, key commands

---

## Settings Files

**`.claude/settings.json`** — Project settings (committed to git):

- Permissions (allow/deny tool patterns)
- MCP server configuration

**`.claude/settings.local.json`** — Local overrides (gitignored):

- Personal permissions
- Hooks configuration
- Local MCP servers

**Permission format:**

```json
{
  "permissions": {
    "allow": ["Bash(npm test:*)", "Read"],
    "deny": ["Bash(rm -rf:*)"]
  }
}
```

---

## Quick Reference: When to Use What

| Need                         | Solution       |
| ---------------------------- | -------------- |
| Reusable prompt templates    | Slash Commands |
| Domain expertise / workflows | Skills         |
| Automate on tool use         | Hooks          |
| External tool integration    | MCP Servers    |
| Project context / rules      | CLAUDE.md      |
| Permission control           | settings.json  |

---

## Debugging Tips

1. **Skill not triggering?** Check description has specific trigger keywords
2. **Command not found?** Verify path: `.claude/commands/name.md` → `/name`
3. **Hook not running?** Check `matcher` regex and file permissions (`chmod +x`)
4. **MCP server failing?** Run the command manually to see errors

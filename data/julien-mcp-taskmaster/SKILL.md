---
name: julien-mcp-taskmaster
description: Install TaskMaster AI MCP for task management. Use when user needs AI-powered project task breakdown.
category: mcp
triggers:
  - install taskmaster mcp
  - taskmaster ai
  - task management mcp
---

# MCP TaskMaster AI Installer

This skill installs the TaskMaster AI MCP server into the current project.

## Installation Procedure

When the user asks to install TaskMaster MCP:

### Step 1: Initialize TaskMaster in project

```bash
npx task-master-ai init
```

This creates the `.taskmaster` directory with default configuration.

### Step 2: Configure for Claude Code (No API Keys)

Edit `.taskmaster/config.json` to use Claude Code as provider (no extra API costs):

```json
{
  "models": {
    "main": {
      "provider": "claude-code",
      "modelId": "sonnet",
      "maxTokens": 64000,
      "temperature": 0.2
    },
    "research": {
      "provider": "claude-code",
      "modelId": "opus",
      "maxTokens": 32000,
      "temperature": 0.1
    },
    "fallback": {
      "provider": "claude-code",
      "modelId": "sonnet",
      "maxTokens": 64000,
      "temperature": 0.2
    }
  },
  "global": {
    "logLevel": "info",
    "defaultSubtasks": 5,
    "defaultPriority": "medium"
  }
}
```

### Step 3: Add MCP Server to `.mcp.json`

**Merge configuration** - Add this server to `mcpServers`:

```json
{
  "task-master": {
    "command": "npx",
    "args": ["-y", "task-master-ai"],
    "env": {
      "MODEL": "claude-code"
    }
  }
}
```

**If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "task-master": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "MODEL": "claude-code"
      }
    }
  }
}
```

## Alternative: With API Keys

If you want to use external APIs instead of Claude Code:

```json
{
  "task-master": {
    "command": "npx",
    "args": ["-y", "task-master-ai"],
    "env": {
      "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
      "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
    }
  }
}
```

## Key Commands After Setup

- `task-master parse-prd your-prd.txt` - Parse a PRD and generate tasks
- `task-master list` - List all tasks
- `task-master next` - Show next task to work on
- `task-master models --setup` - Configure models interactively

## Usage After Installation

Restart Claude Code to activate the MCP server. TaskMaster helps break down complex projects into manageable tasks.

## Skill Chaining

- **Input**: User request to install TaskMaster MCP
- **Output**: Configured `.mcp.json` with task-master server
- **Tools Used**: Read, Edit, Write, Bash
- **Chains With**: Serena MCP for code analysis

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npx` not found | Install Node.js and ensure npm is in PATH |
| Init failed | Run `npx task-master-ai init` in project root |
| Config not found | Create `.taskmaster/config.json` manually |
| Model error | Set provider to "claude-code" for no API costs |

## References

- [GitHub - claude-task-master](https://github.com/eyaltoledano/claude-task-master)
- [TaskMaster Setup Guide](https://pageai.pro/blog/claude-code-taskmaster-ai-tutorial)

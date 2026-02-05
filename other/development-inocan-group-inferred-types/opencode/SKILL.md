---
name: opencode
description: "OpenCode CLI - open source AI coding agent with TUI, IDE integration, LSP support, and MCP servers."
---

# OpenCode Development

> **Source:** https://github.com/sst/opencode (packages/web/src/content/docs/)

OpenCode is an open source AI coding agent available as a terminal interface (TUI), desktop app, or IDE extension. It's provider-agnostic and supports MCP servers for extensibility.

## Installation

```bash
# Install script
curl -fsSL https://opencode.ai/install | bash

# npm
npm install -g opencode-ai

# Homebrew
brew install opencode

# Bun
bun install -g opencode-ai
```

## Quick Start

```bash
# Start TUI in current directory
opencode

# Start in specific directory
opencode /path/to/project

# Non-interactive mode
opencode -p "explain this codebase"

# With specific model
opencode --model anthropic/claude-sonnet-4-5-20250929
```

## TUI Features

### File References

Reference files with `@` for fuzzy search:

```text
How is auth handled in @packages/api/auth.ts?
```

### Bash Commands

Start with `!` to run shell commands:

```text
!ls -la
!git status
```

### Slash Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/connect` | Add a provider API key |
| `/model` | Switch model |
| `/clear` | Clear conversation |
| `/compact` | Compact conversation history |
| `/session` | Manage sessions |
| `/theme` | Change theme |
| `/cost` | Show token usage and cost |

## Configuration

Create `opencode.json` in your project root or `~/.config/opencode/`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5-20250929",
  "provider": {
    "anthropic": {
      "api_key": "${ANTHROPIC_API_KEY}"
    }
  }
}
```

### Environment Variables

```bash
# Provider API keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# OpenCode settings
OPENCODE_MODEL=anthropic/claude-sonnet-4-5-20250929
```

## Tools

OpenCode has built-in tools that the LLM can use:

| Tool | Description |
|------|-------------|
| `read` | Read file contents |
| `write` | Create or overwrite files |
| `edit` | Make targeted edits |
| `bash` | Execute shell commands |
| `glob` | Find files by pattern |
| `grep` | Search file contents |
| `webfetch` | Fetch URL content |
| `todoread` / `todowrite` | Manage task lists |

### Configure Tools

```json
{
  "$schema": "https://opencode.ai/config.json",
  "tools": {
    "write": true,
    "bash": true,
    "webfetch": false
  }
}
```

## Agents

Define custom agents with specific behaviors:

```markdown
<!-- ~/.config/opencode/agent/reviewer.md -->
---
description: Code review agent
mode: subagent
tools:
  write: false
  edit: false
---

You are a code reviewer. Analyze code for:
- Security vulnerabilities
- Performance issues
- Best practices
```

### Agent Modes

- **`subagent`**: Called by other agents for specific tasks
- **`autonomous`**: Runs independently with minimal user input

## MCP Servers

Add external tools via Model Context Protocol:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "remote-server": {
      "type": "remote",
      "url": "https://mcp.example.com",
      "enabled": true
    }
  }
}
```

## LSP Integration

OpenCode includes out-of-the-box LSP support. Configure additional servers:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"]
    }
  }
}
```

## Rules

Add project-specific instructions:

```markdown
<!-- .opencode/rules.md -->
# Project Rules

- Use TypeScript for all new files
- Follow the existing code style
- Add tests for new features
```

## Keybinds

Default leader key: `Ctrl+X`

| Keybind | Action |
|---------|--------|
| `Ctrl+X h` | Help |
| `Ctrl+X m` | Switch model |
| `Ctrl+X t` | Switch theme |
| `Ctrl+X c` | Clear conversation |
| `Ctrl+X s` | Save session |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit |

## Modes

| Mode | Description |
|------|-------------|
| **TUI** | Full terminal interface |
| **CLI** | Non-interactive, single prompt |
| **Zen** | Minimal distraction mode |
| **IDE** | VS Code extension |

## Best Practices

1. **Use file references** (`@file`) to give context without copying content
2. **Configure tool permissions** for sensitive projects
3. **Use agents** for specialized tasks (review, planning, testing)
4. **Enable LSP** for better code understanding
5. **Use MCP servers sparingly** - they add to context size

## Documentation Index

| Resource | When to Consult |
|----------|-----------------|
| [index.md](resources/index.md) | Installation, getting started |
| [tui.md](resources/tui.md) | Terminal interface usage |
| [cli.md](resources/cli.md) | Non-interactive CLI usage |
| [config.md](resources/config.md) | Configuration options |
| [models.md](resources/models.md) | Model selection and providers |
| [tools.md](resources/tools.md) | Built-in tools configuration |
| [custom-tools.md](resources/custom-tools.md) | Creating custom tools |
| [mcp-servers.md](resources/mcp-servers.md) | MCP server integration |
| [agents.md](resources/agents.md) | Custom agent definitions |
| [rules.md](resources/rules.md) | Project-specific rules |
| [keybinds.md](resources/keybinds.md) | Keyboard shortcuts |
| [lsp.md](resources/lsp.md) | Language server protocol |
| [permissions.md](resources/permissions.md) | Tool permissions |
| [themes.md](resources/themes.md) | Theme customization |
| [ide.md](resources/ide.md) | VS Code extension |
| [zen.md](resources/zen.md) | Zen mode |
| [troubleshooting.md](resources/troubleshooting.md) | Common issues |

## Syncing Documentation

```bash
cd skills/opencode
bun run scripts/sync-docs.ts
```

---
name: julien-mcp-serena
description: Install Serena MCP for semantic code analysis. Use when user needs IDE-like code retrieval and editing.
category: mcp
triggers:
  - install serena mcp
  - serena code
  - semantic code mcp
---

# MCP Serena Installer

This skill installs the Serena MCP server into the current project. Serena is a powerful coding agent toolkit that provides semantic code retrieval and editing capabilities.

## Installation Procedure

When the user asks to install Serena MCP:

### Step 1: Prerequisites

Ensure `uv` is installed:
```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Step 2: Add MCP Server to `.mcp.json`

**Merge configuration** - Add this server to `mcpServers`:

```json
{
  "serena": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "claude-code"]
  }
}
```

**If `.mcp.json` doesn't exist**, create it with the full structure:

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "claude-code"]
    }
  }
}
```

### Step 3: Project Configuration (Optional)

Serena auto-generates config files at:
- `~/.serena/serena_config.yml` - Global config
- `<project>/.serena/project.yml` - Project-specific config

For security, keep `read_only: true` in configs and enable extra tools only when needed.

## Alternative: With Project Path

If you want Serena configured for a specific project:

```json
{
  "serena": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "claude-code", "--project", "${PWD}"]
  }
}
```

## Key Tools Provided

Serena provides powerful IDE-like capabilities:

- `find_symbol` - Locate specific symbols in codebase
- `find_referencing_symbols` - Discover where a symbol is used
- `get_symbol_documentation` - Retrieve documentation
- `insert_after_symbol` - Add code after a specific symbol
- Semantic code analysis at symbol level
- Multi-language support (Python, JavaScript, Java, and more)

## Dashboard

Access the Serena dashboard at: `http://localhost:24282/dashboard/index.html`

## Context Options

The `--context` flag controls which tools are enabled:
- `claude-code` - Disables tools that duplicate Claude Code's built-in capabilities
- `ide-assistant` - Full tool set for IDE integrations

## Version Requirements

Use Claude Code v1.0.52 or later (earlier versions don't read MCP server system prompts).

## Usage After Installation

Restart Claude Code to activate the MCP server.

## Skill Chaining

- **Input**: User request to install Serena MCP
- **Output**: Configured `.mcp.json` with serena server
- **Tools Used**: Read, Edit, Write
- **Chains With**: TaskMaster MCP for project management

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uvx` not found | Install `uv` from astral.sh |
| Git clone fails | Check network and GitHub access |
| Python version error | Ensure Python 3.8+ is installed |
| Symbol not found | Run `serena index` to rebuild project index |

## References

- [GitHub - Serena](https://github.com/oraios/serena)
- [Serena Documentation](https://oraios.github.io/serena/02-usage/030_clients.html)
- [Serena MCP Setup Guide](https://smartscope.blog/en/generative-ai/claude/serena-mcp-implementation-guide/)

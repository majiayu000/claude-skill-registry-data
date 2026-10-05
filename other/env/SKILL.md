---
name: env
description: Display and manage loaded environment details including instructions, MCP servers, skills, agents, plugins, LSPs, and extensions. Shows the complete development environment configuration.
runtime_projection: true
source_of_truth: registry/skills/env/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/env/SKILL.md`
> Source of truth: `registry/skills/env/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Environment Information Skill

## Overview

The `env` skill provides comprehensive insight into your Copilot environment configuration, including all loaded extensions, MCP servers, skills, and other integrated tools.

## Usage

### Display Complete Environment
```
/env
```

Shows all loaded environment details:
- **Instructions**: Custom instruction files from various locations
- **MCP Servers**: Message Context Protocol servers and their configuration
- **Skills**: Available skills for enhanced capabilities
- **Agents**: Registered agents (built-in and custom)
- **Plugins**: Installed plugins and plugin marketplaces
- **LSPs**: Language Server Protocol configurations
- **Extensions**: Loaded CLI extensions

### Key Environment Configuration Files

Your Copilot environment loads configuration from these locations (in order of precedence):

#### Instructions
- `CLAUDE.md` - Claude-specific instructions
- `GEMINI.md` - Gemini-specific instructions  
- `AGENTS.md` - Agent configuration (in git root & cwd)
- `.github/instructions/**/*.instructions.md` - Modular instructions (git root & cwd)
- `.github/copilot-instructions.md` - Project-level instructions
- `$HOME/.copilot/copilot-instructions.md` - User-level instructions
- `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` - Additional directories via environment variable

#### Configuration Storage
- **MCP Config**: `~/.copilot/mcp-config.json`
- **Skills**: `~/.copilot/skills/` (directory)
- **Session State**: `~/.copilot/session-state/`
- **Main Config**: `~/.copilot/config.json`
- **Permissions**: `~/.copilot/permissions-config.json`

### Common Tasks

#### Check if a Skill is Installed
```
/env
```
Then look for the skill name in the skills section.

#### View All MCP Servers
```
/env
```
Check the MCP servers section for active and configured servers.

#### See Loaded Instructions
```
/env
```
Review the instructions section to verify custom instructions are loaded.

#### Check Language Server Status
```
/env
```
View LSPs section for configured language servers.

## Managing Environment Components

### Using Related Commands

- **`/mcp`** - Configure Message Context Protocol servers
- **`/skills`** - Manage skills for enhanced capabilities
- **`/agent`** - Browse and select from available agents
- **`/plugin`** - Manage plugins and plugin marketplaces
- **`/lsp`** - Manage language server configuration
- **`/instructions`** - View and toggle custom instruction files

## Best Practices

1. **Regular Audits**: Use `/env` regularly to verify all expected tools are loaded
2. **Troubleshooting**: If a tool isn't available, check `/env` to see if it's loaded
3. **Configuration**: Combine with `/mcp`, `/skills`, and `/instructions` for full control
4. **Performance**: Too many active servers or skills can impact performance - use `/env` to identify unused components

## Troubleshooting

### Environment Not Loading Correctly

1. Check instructions are in correct locations using `/env`
2. Verify file permissions on instruction files
3. Check for syntax errors in JSON configuration files (config.json, mcp-config.json)
4. Review environment variables (especially `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`)

### Missing Tools or Skills

1. Run `/env` to see what's currently loaded
2. Check if skill/tool needs to be explicitly enabled with `/skills` or `/mcp`
3. Verify installation with appropriate management command (`/skills`, `/mcp`, etc.)
4. Check file permissions in `~/.copilot/` directory

## Related Skills and Commands

- **Setup Commands**: `/init`, `/terminal-setup`
- **Code Intelligence**: `/lsp`, `/ide`
- **Configuration**: `/mcp`, `/skills`, `/instructions`, `/plugin`
- **Session Management**: `/session`, `/env`, `/context`

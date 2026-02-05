---
name: plugin-author
description: Guide for creating, configuring, and distributing Claude Code plugins with hooks, skills, commands, and MCP servers. Use when user asks to create a plugin, set up hooks, add plugin functionality, create a marketplace, or distribute custom Claude Code extensions.
---

# Plugin Author: Creating Claude Code Plugins

Complete guide for building Claude Code plugins with all available features.

**Documentation sources:**

- https://code.claude.com/docs/en/plugins.md
- https://code.claude.com/docs/en/plugins-reference.md
- https://code.claude.com/docs/en/hooks.md
- https://code.claude.com/docs/en/hooks-guide.md
- https://code.claude.com/docs/en/skills.md
- https://code.claude.com/docs/en/slash-commands.md

## What Are Plugins?

Plugins extend Claude Code with shareable, versioned functionality distributed through marketplaces. They can include:

- **Hooks** - Automated responses to events (file edits, commands, session start)
- **Skills** - Auto-discovered capabilities Claude uses based on context
- **Slash Commands** - Explicitly invoked prompts with arguments
- **Agents** - Specialized subagents for specific tasks
- **MCP Servers** - Tool integrations via Model Context Protocol

## When to Use Plugins vs Other Methods

**Use Plugins when:**

- Distributing to teams or community
- Bundling related features together
- Need versioning and installable packages
- Sharing across multiple projects

**Use Project Files (.claude/) when:**

- Single project customization
- Quick prototyping
- Team workflows in one repository

**Use Personal Files (~/.claude/) when:**

- Individual preferences
- Cross-project personal tools

## Component Overview

| Component   | File Location        | Use When                               |
| ----------- | -------------------- | -------------------------------------- |
| Plugins     | See `plugins.md`     | Distributing packaged functionality    |
| Hooks       | See `hooks.md`       | Automating responses to events         |
| Skills      | See `skills.md`      | Claude should auto-discover capability |
| Commands    | See `commands.md`    | User explicitly invokes with /command  |
| Agents      | See `agents.md`      | Need specialized subagent              |
| MCP Servers | See `mcp-servers.md` | Integrating external tools             |

## Quick Start

### 1. Create Basic Plugin Structure

```bash
mkdir -p my-plugin/.claude-plugin
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My first plugin",
  "author": {"name": "Your Name"}
}
EOF
```

### 2. Add a Component

Choose what to add:

**Add a hook** (see `hooks.md`):

```bash
mkdir -p my-plugin/hooks
# Create hooks/hooks.json
```

**Add a skill** (see `skills.md`):

```bash
mkdir -p my-plugin/skills/my-skill
# Create skills/my-skill/SKILL.md
```

**Add a command** (see `commands.md`):

```bash
mkdir -p my-plugin/commands
# Create commands/my-command.md
```

### 3. Create Development Marketplace

```bash
mkdir -p ~/dev-marketplace/.claude-plugin
cat > ~/dev-marketplace/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "Development Marketplace",
  "plugins": [
    {
      "name": "my-plugin",
      "source": "my-plugin",
      "description": "My first plugin"
    }
  ]
}
EOF

# Move plugin into marketplace
mv my-plugin ~/dev-marketplace/
```

### 4. Install and Test

```bash
claude plugins add ~/dev-marketplace
claude plugins install my-plugin

# Test your plugin
claude

# After changes, reinstall
claude plugins uninstall my-plugin
claude plugins install my-plugin
```

## Development Workflow

1. **Plan** - Decide what components you need
2. **Create** - Build plugin structure and manifest
3. **Implement** - Add hooks, skills, commands, etc.
4. **Test Locally** - Use development marketplace
5. **Iterate** - Uninstall/reinstall after changes
6. **Debug** - Use `claude --debug` and check logs
7. **Document** - Add README with setup instructions
8. **Distribute** - Publish marketplace to git

## Debugging

**Enable debug mode:**

```bash
claude --debug
```

**Check plugin status:**

```bash
claude plugins list
```

**View registered hooks:**
In Claude session, use `/hooks` command

## Common Plugin Patterns

| Pattern         | Components             | Use Case                                 |
| --------------- | ---------------------- | ---------------------------------------- |
| Auto-formatter  | PostToolUse hook       | Format code after edits                  |
| File protection | PreToolUse hook        | Block edits to sensitive files           |
| Test generator  | Skill + Command        | Auto-generate or explicitly create tests |
| Code reviewer   | Skill + Agent          | Auto-review or detailed analysis         |
| Dev workflow    | Hook + Skill + Command | Complete development automation          |
| Security guard  | Multiple hooks         | Prevent secrets, validate imports        |

## Detailed Documentation

For comprehensive information on each component, see:

- **plugins.md** - Plugin manifests, structure, distribution, marketplaces
- **hooks.md** - All hook events, matchers, exit codes, patterns, examples
- **skills.md** - Skill creation, frontmatter, descriptions, tool restrictions
- **commands.md** - Command creation, arguments, frontmatter
- **agents.md** - Subagent configuration and usage
- **mcp-servers.md** - MCP server integration

## Environment Variables

Available in plugin configurations:

- `${CLAUDE_PLUGIN_ROOT}` - Absolute path to plugin directory
- `${CLAUDE_PROJECT_DIR}` - Current project root
- `${CLAUDE_ENV_FILE}` - SessionStart hooks only: file to persist env vars

## Security Best Practices

- Validate all input from hook JSON
- Quote variables in bash scripts: `"$VAR"`
- Check for path traversal: `if [[ "$PATH" == *".."* ]]`
- Protect sensitive files: `.env`, `.git/`, credentials
- Never include secrets in plugin code
- Document required permissions clearly

## Getting Help

- Documentation: https://code.claude.com/docs/
- Enable debugging: `claude --debug`
- Use `/hooks` command to view registered hooks

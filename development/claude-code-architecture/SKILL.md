---
name: claude-code-architecture
description: Self-reference guide for Claude Code's own architecture, configuration, and extension points. Use when needing to know where Claude Code stores its configuration files, skills, plugins, hooks, MCP servers, settings, or any other internal structure. Triggers on questions like "where do skills go?", "how do I configure hooks?", "where is the settings file?", or when creating/modifying Claude Code extensions.
---

# Claude Code Architecture

Claude Code stores its configuration and data in `~/.claude/`. This skill documents the complete structure.

## Directory Structure

```
~/.claude/
├── CLAUDE.md              # Global user instructions (loaded for ALL sessions)
├── settings.json          # Plugin enable/disable state
├── settings.local.json    # Local permissions (allow/deny/ask lists)
├── skills/                # User-installed skills
│   └── *.skill            # Packaged skill files (zip format)
├── plugins/               # Plugin system
│   ├── cache/             # Cached plugin data
│   ├── marketplaces/      # Plugin marketplace mirrors
│   └── installed_plugins.json
├── projects/              # Per-project conversation history
│   └── -path-to-project/  # Directory path encoded with dashes
├── commands/              # Custom slash commands (user-defined)
│   └── *.md               # Slash command definitions
├── history.jsonl          # Command history
├── todos/                 # Task tracking state
├── plans/                 # Plan mode files
├── file-history/          # File edit history/backups
├── debug/                 # Debug logs
└── session-env/           # Session environment state
```

## Configuration Files

### CLAUDE.md (Global Instructions)

Location: `~/.claude/CLAUDE.md`

Personal instructions loaded into EVERY Claude Code session. Use for:
- Personal coding preferences
- Recurring reminders (e.g., "always use stow for dotfiles")
- Default behaviors

Project-specific instructions go in `./CLAUDE.md` at project root.

### settings.json (Plugin State)

Location: `~/.claude/settings.json`

Controls which plugins are enabled:
```json
{
  "enabledPlugins": {
    "plugin-name@marketplace": true
  }
}
```

### settings.local.json (Permissions)

Location: `~/.claude/settings.local.json`

Controls tool permissions:
```json
{
  "permissions": {
    "allow": ["Bash(git:*)", "WebSearch"],
    "deny": [],
    "ask": []
  }
}
```

Permission patterns:
- `Bash(command:*)` - Allow specific bash command patterns
- `WebSearch` - Allow web searches
- `Read`, `Write`, `Edit` - File operation permissions

## Skills System

### User Skills Location

`~/.claude/skills/`

Skills are packaged as `.skill` files (zip archives) containing:
```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Optional: executable code
├── references/           # Optional: documentation to load as needed
└── assets/               # Optional: templates, images for output
```

### SKILL.md Format

```yaml
---
name: skill-name
description: What it does and WHEN to trigger it
---

# Skill Name

Instructions and workflow documentation...
```

The `description` field is critical - it determines when Claude loads the skill.

### Plugin Skills

Installed from marketplaces to:
- `~/.claude/plugins/cache/{marketplace}/{plugin}/skills/`
- `~/.claude/plugins/marketplaces/{marketplace}/skills/`

### Creating a Skill

Use the skill-creator skill's init script:
```bash
python ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/scripts/init_skill.py <name> --path ~/.claude/skills/
```

Package with:
```bash
python ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/scripts/package_skill.py ~/.claude/skills/<name>/
```

## Plugin System

### Structure

```
~/.claude/plugins/
├── installed_plugins.json     # Registry of installed plugins
├── known_marketplaces.json    # Available marketplaces
├── cache/                     # Plugin data cache
│   └── {marketplace}/         # Per-marketplace cache
└── marketplaces/              # Marketplace content mirrors
    └── {marketplace}/
        └── skills/            # Skills from this marketplace
```

### Plugin Marketplaces

Default marketplaces:
- `anthropic-agent-skills` - Official Anthropic skills
- `claude-plugins-official` - Official Claude Code plugins

## Slash Commands

### User Commands Location

`~/.claude/commands/`

Create `.md` files that expand to prompts:
```
~/.claude/commands/
└── my-command.md    # Invoked as /my-command
```

### Project Commands

`.claude/commands/` in project root for project-specific commands.

## Hooks

Hooks are shell commands that run in response to Claude Code events. Configure in:
- `~/.claude/settings.json` (global)
- `.claude/settings.json` (project)

Hook types:
- `PreToolUse` - Before a tool runs
- `PostToolUse` - After a tool runs
- `Notification` - On notifications
- `Stop` - When Claude stops
- `SubagentStop` - When a subagent stops

Use the hookify plugin for easier hook management: `/hookify:help`

## MCP Servers

MCP (Model Context Protocol) servers extend Claude's capabilities with external tools.

Configure in `~/.claude/settings.json` or project `.claude/settings.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {}
    }
  }
}
```

## Project Configuration

Each project can have its own:
- `./CLAUDE.md` - Project-specific instructions
- `.claude/settings.json` - Project settings and MCP servers
- `.claude/commands/` - Project-specific slash commands

## Common Tasks

### Add a new skill
1. Create in `~/.claude/skills/skill-name/`
2. Write `SKILL.md` with frontmatter
3. Package with `package_skill.py`

### Add global instructions
Edit `~/.claude/CLAUDE.md`

### Allow a bash command without prompting
Add to `~/.claude/settings.local.json` under `permissions.allow`

### Add a custom slash command
Create `~/.claude/commands/command-name.md`

### Configure project-specific behavior
Create `.claude/settings.json` or `./CLAUDE.md` in project root

## Subagent System

The Task tool spawns specialized agents for complex work. Available types:

| Type | Purpose |
|------|---------|
| `Explore` | Fast codebase exploration, file searches, understanding code |
| `Plan` | Software architecture, implementation planning |
| `claude-code-guide` | Questions about Claude Code itself, features, documentation |
| `general-purpose` | Complex multi-step tasks, research |

Usage: Subagents run autonomously and return results. Use `run_in_background: true` for parallel execution.

## Built-in CLI Commands

| Command | Purpose |
|---------|---------|
| `/help` | Show help and available commands |
| `/clear` | Clear conversation history |
| `/compact` | Compress context by summarizing |
| `/config` | Open settings configuration |
| `/cost` | Show token usage and costs |
| `/doctor` | Diagnose issues with setup |
| `/init` | Initialize Claude Code in a project |
| `/login` | Authenticate with Anthropic |
| `/logout` | Sign out |
| `/mcp` | Manage MCP servers |
| `/memory` | View/manage conversation memory |
| `/model` | Switch models (sonnet/opus/haiku) |
| `/permissions` | Manage tool permissions |
| `/review` | Request code review |
| `/status` | Show current session status |
| `/terminal-setup` | Configure terminal integration |
| `/vim` | Toggle vim keybindings |
| `/tasks` | List background tasks |

## Model Selection

Available models:
- **opus** - Most capable, best for complex reasoning and planning
- **sonnet** - Balanced performance and speed (default)
- **haiku** - Fastest, best for simple tasks, lowest cost

Switch with `/model` or specify in Task tool: `model: "haiku"`

Use haiku for quick searches/simple edits. Use opus for architecture decisions and complex debugging.

## Plan Mode

Entered via `EnterPlanMode` tool or when planning complex implementations.

- Plans stored in `~/.claude/plans/`
- Use for multi-step implementations requiring user approval
- Exit with `ExitPlanMode` after user approves plan

## File History & Recovery

`~/.claude/file-history/` tracks all file edits made by Claude.

- Each edit creates a versioned backup
- Format: `{session-id}/{file-hash}@v{version}`
- Use to recover from unwanted changes

## IDE Integrations

### VS Code Extension
- Extension: "Claude Code" in VS Code marketplace
- Provides inline Claude access within editor
- Shares configuration with CLI

### JetBrains Plugin
- Available for IntelliJ, PyCharm, WebStorm, etc.
- Integrates with IDE's tool windows

Both connect to the same Claude Code backend and share `~/.claude/` configuration.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API authentication |
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock backend |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex backend |
| `CLAUDE_CODE_CONFIG_DIR` | Override config directory (default: `~/.claude`) |
| `CLAUDE_CODE_SKIP_HOOKS` | Disable hooks temporarily |

## Permission Pattern Syntax

Patterns in `settings.local.json`:

```
"Bash(git:*)"           # Any git command
"Bash(npm run:*)"       # npm run with any script
"Bash(docker:*)"        # Any docker command
"Bash(ls:*)"            # ls with any args
"Bash(cat:*)"           # cat with any args
"Bash(python:*.py)"     # python with .py files
"WebSearch"             # Web search tool
"Read"                  # All file reads (use cautiously)
"mcp__servername__*"    # All tools from an MCP server
```

Wildcards: `*` matches any characters in that position.

## Debug & Troubleshooting

### Debug Logs
`~/.claude/debug/` contains session debug logs named by session ID.

### Common Issues

**Skill not loading**: Skills load at session start. Restart Claude Code after adding new skills.

**Permission denied**: Add pattern to `settings.local.json` under `permissions.allow`.

**Hook errors**: Check hook script exists and is executable. Use `/hookify:list` to see configured hooks.

**MCP server not connecting**: Verify command path, check server logs, ensure dependencies installed.

### Diagnostic Command
Run `/doctor` to check:
- API key validity
- Configuration file syntax
- MCP server connectivity
- Plugin status

## Context & Memory

- Conversations auto-summarize when context grows large
- Per-project history stored in `~/.claude/projects/`
- `/compact` manually triggers summarization
- `/memory` shows what Claude remembers from summarization

## Todo System

`~/.claude/todos/` stores task lists per session.

- TodoWrite tool creates/updates tasks
- Tasks persist across conversation turns
- Visible to user in UI as progress indicator

---
name: configuration
description: How to configure Claude Code settings, permissions, environment variables, and project-level configurations. Use when user asks about settings.json, configuration, permissions, or Claude Code setup.
---

# Claude Code Configuration

## Overview

Claude Code provides hierarchical configuration through `settings.json` files at multiple levels. You can manage settings globally, per-project, or through enterprise policies.

## Configuration File Locations

**User-level settings**: `~/.claude/settings.json` (applies to all projects)

**Project-level settings**:
- `.claude/settings.json` (shared with team via source control)
- `.claude/settings.local.json` (personal, not committed)

**Enterprise managed policies**:
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

## Key Configuration Options

| Setting | Purpose | Example |
|---------|---------|---------|
| `permissions` | Control tool access and file restrictions | `{"allow": ["Bash(npm run test:*)"], "deny": ["Read(.env)"]}` |
| `env` | Environment variables for sessions | `{"FOO": "bar"}` |
| `model` | Override default model | `"claude-sonnet-4-5-20250929"` |
| `outputStyle` | Adjust system prompt behavior | `"Explanatory"` |
| `hooks` | Custom commands before/after tool use | `{"PreToolUse": {"Bash": "echo 'Running..'"}}` |

## Permission Configuration

Restrict file and command access through the `permissions` object:

**Deny patterns** block sensitive files:
```json
{
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(./secrets/**)",
      "Bash(curl:*)"
    ]
  }
}
```

**Allow patterns** explicitly permit actions:
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)"
    ]
  }
}
```

**Ask patterns** require confirmation:
```json
{
  "permissions": {
    "ask": [
      "Bash(git push:*)",
      "Write(src/**)"
    ]
  }
}
```

## Sandbox Settings

Enable process isolation (macOS/Linux):

```json
{
  "sandbox": {
    "enabled": true,
    "excludedCommands": ["docker"],
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowLocalBinding": true
    }
  }
}
```

## Settings Precedence (High to Low)

1. Enterprise managed policies
2. Command-line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

## Environment Variables

Key variables for controlling Claude Code behavior:

- `ANTHROPIC_API_KEY` - API authentication
- `BASH_MAX_OUTPUT_LENGTH` - Limit bash output size
- `DISABLE_TELEMETRY` - Opt out of analytics
- `MAX_THINKING_TOKENS` - Enable extended thinking
- `CLAUDE_CODE_USE_BEDROCK` - Use AWS Bedrock
- `DISABLE_PROMPT_CACHING` - Turn off caching globally

## Available Tools

Claude Code can access these tools (subject to permissions):
- Bash
- Edit, Read, Write
- WebFetch, WebSearch
- Glob, Grep
- NotebookEdit
- Task

## Plugin Management

Configure plugins via `enabledPlugins`:

```json
{
  "enabledPlugins": {
    "formatter@company-tools": true,
    "deployer@company-tools": false
  },
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  }
}
```

Access plugin management interactively with `/plugin` command.

## Excluding Sensitive Files

Prevent Claude from accessing confidential data:

```json
{
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(./secrets/**)",
      "Read(**/credentials.json)"
    ]
  }
}
```

Files matching deny patterns become completely invisible to Claude Code.

## Common Configuration Examples

### Development Team Setup

**.claude/settings.json** (committed to repo):
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status:*)",
      "Bash(git diff:*)"
    ],
    "deny": [
      "Read(.env*)",
      "Bash(git push:*)"
    ],
    "ask": [
      "Write(src/**)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

### Personal Overrides

**.claude/settings.local.json** (not committed):
```json
{
  "model": "claude-opus-4-5-20250514",
  "env": {
    "CUSTOM_VAR": "my-value"
  }
}
```

### Enterprise Security Policy

**/etc/claude-code/managed-settings.json**:
```json
{
  "permissions": {
    "deny": [
      "Read(/etc/passwd)",
      "Read(~/.ssh/**)",
      "Bash(rm:*)",
      "Bash(sudo:*)"
    ]
  },
  "sandbox": {
    "enabled": true
  }
}
```

## Managing Settings

**View current settings**: Check the files in `.claude/` directory

**Edit project settings**: Create or modify `.claude/settings.json`

**Edit user settings**: Modify `~/.claude/settings.json`

**Interactive configuration**: Some settings can be managed via slash commands like `/permissions`

## Best Practices

1. **Use project settings** for team-shared configuration
2. **Use local settings** for personal preferences
3. **Commit shared settings** to source control
4. **Document settings** with comments (use `//` in JSON5-compatible editors)
5. **Review permissions** regularly for security
6. **Test settings** before enforcing team-wide
7. **Use deny patterns** for sensitive files
8. **Enable sandbox** for additional security
9. **Set environment variables** for consistent environments
10. **Configure marketplaces** for team plugin distribution

## Troubleshooting

**Settings not applying:**
- Check file locations and names
- Verify JSON syntax
- Review precedence order
- Check for conflicting settings at different levels

**Permission errors:**
- Review deny/allow patterns
- Check pattern syntax (glob patterns supported)
- Verify file paths are correct
- Test patterns incrementally

**Plugin issues:**
- Verify marketplace configuration
- Check plugin names and versions
- Ensure plugins are enabled in `enabledPlugins`
- Review plugin-specific settings

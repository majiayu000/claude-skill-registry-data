---
name: Plugin Installation
description: Use when the user wants to install, update, or set up a Claude Code plugin
version: 1.0.0
---

# Plugin Installation

Guide users through installing and configuring Claude Code plugins.

## When to Use This Skill

Activate this skill when the user:
- Wants to install a specific plugin
- Asks how to add a plugin
- Needs help with plugin setup
- Wants to update installed plugins
- Has installation issues or errors

## Installation Methods

### 1. From Marketplace (Recommended)

Install plugins directly from the registry:
```
/plugin-marketplace:install @scope/plugin-name
```

This will:
- Download the plugin from the registry
- Verify the plugin signature
- Install to the appropriate location
- Display any configuration instructions

### 2. From Git Repository

For plugins not in the registry or development versions:
```bash
# Clone to plugins directory
git clone https://github.com/org/plugin-name ~/.claude/plugins/plugin-name

# Or for project-specific
git clone https://github.com/org/plugin-name .claude/plugins/plugin-name
```

### 3. Local Development

For testing local plugins:
```bash
# Symlink to plugins directory
ln -s /path/to/my-plugin ~/.claude/plugins/my-plugin
```

## Installation Locations

| Location | Scope | Path |
|----------|-------|------|
| User | All projects | `~/.claude/plugins/` |
| Project | Current project | `.claude/plugins/` |

**Priority:** Project plugins override user plugins with the same name.

## Installation Process

### Step 1: Verify Plugin

Before installing, check:
- Plugin exists in registry or valid git URL
- Compatible with current Claude Code version
- Review permissions required

### Step 2: Install

Run the install command:
```
/plugin-marketplace:install @scope/plugin-name
```

### Step 3: Verify Installation

Confirm the plugin is installed:
```
/plugin-marketplace:list
```

### Step 4: Configure (if needed)

Some plugins require configuration. Create settings file:
```
.claude/plugin-name.local.md
```

### Step 5: Test

Verify the plugin works:
- Try a plugin command
- Check if skills are available
- Review any hooks that were added

## Handling Permissions

Plugins may request permissions. Explain each:

| Permission | Risk | Description |
|------------|------|-------------|
| `filesystem:read` | Medium | Read files from disk |
| `filesystem:write` | High | Write/modify files |
| `network` | Medium | Make HTTP requests |
| `execute` | High | Run shell commands |
| `mcp` | Medium | Connect to MCP servers |

**Always review permissions before installing.**

## Troubleshooting

### Plugin Not Found
```
Error: Plugin @scope/plugin-name not found in registry
```
**Solutions:**
- Check spelling of plugin name
- Verify the plugin exists in the marketplace
- Try installing from git URL directly

### Permission Denied
```
Error: Permission denied writing to plugins directory
```
**Solutions:**
- Check directory permissions
- Use sudo for system-wide install (not recommended)
- Install to project directory instead

### Version Conflict
```
Error: Plugin requires Claude Code >= 2.0.0
```
**Solutions:**
- Update Claude Code to latest version
- Install an older plugin version
- Check plugin compatibility notes

### Invalid Plugin Structure
```
Error: Missing .claude-plugin/plugin.json
```
**Solutions:**
- Verify the plugin has correct structure
- Check if cloning the right branch
- Report issue to plugin maintainer

## Updating Plugins

### Update Single Plugin
```
/plugin-marketplace:update @scope/plugin-name
```

### Update All Plugins
```
/plugin-marketplace:update --all
```

### Check for Updates
```
/plugin-marketplace:list --outdated
```

## Best Practices

1. **Review before installing** - Check plugin source and permissions
2. **Start with official plugins** - They're verified and maintained
3. **Use project scope for project-specific plugins** - Keeps system clean
4. **Keep plugins updated** - Security and bug fixes
5. **Remove unused plugins** - Reduce potential conflicts

## Example Interaction

### User: "Install the git-assistant plugin"

**Response:**
I'll install the @claude/git-assistant plugin for you.

```
/plugin-marketplace:install @claude/git-assistant
```

✅ Plugin installed successfully!

**What's included:**
- Commands: `/git-assistant:commit`, `/git-assistant:pr`
- Skills: Automatic commit message generation
- Hooks: Pre-commit validation

**Permissions granted:**
- `execute` - Run git commands
- `filesystem:read` - Read git history

Would you like me to show you how to use it?

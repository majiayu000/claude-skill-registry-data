---
name: Plugin Management
description: Use when the user wants to list, configure, update, or remove installed Claude Code plugins
version: 1.0.0
---

# Plugin Management

Help users manage their installed Claude Code plugins.

## When to Use This Skill

Activate this skill when the user:
- Wants to see installed plugins
- Needs to configure a plugin
- Wants to remove/uninstall a plugin
- Has plugin conflicts or issues
- Wants to enable/disable plugins
- Needs to check plugin status

## Listing Plugins

### List All Installed
```
/plugin-marketplace:list
```

Output includes:
- Plugin name and version
- Installation location (user/project)
- Status (enabled/disabled)
- Last updated date

### List with Details
```
/plugin-marketplace:list --verbose
```

Additional info:
- Commands provided
- Skills available
- Hooks registered
- MCP servers configured

### Filter by Status
```
/plugin-marketplace:list --enabled
/plugin-marketplace:list --disabled
/plugin-marketplace:list --outdated
```

## Plugin Information

Get detailed info about a specific plugin:
```
/plugin-marketplace:info @scope/plugin-name
```

Shows:
- Full description
- Version and changelog
- Author and repository
- Components (commands, skills, hooks)
- Configuration options
- Dependencies

## Configuring Plugins

### Configuration File Location

Create plugin-specific settings:
```
.claude/plugin-name.local.md
```

### Configuration Format

```markdown
# Plugin Name Settings

## Option 1
Value or description: setting-value

## Option 2
Enabled: true

## Custom Paths
- /path/to/resource
- /another/path
```

### Environment Variables

Some plugins use environment variables:
```bash
export PLUGIN_API_KEY="your-key"
export PLUGIN_ENDPOINT="https://api.example.com"
```

### Example Configuration

For `@claude/git-assistant`:
```markdown
# Git Assistant Settings

## Commit Message Style
Convention: conventional-commits

## Auto-stage
Enabled: false

## Ignored Paths
- node_modules/
- dist/
- .env
```

## Removing Plugins

### Remove Single Plugin
```
/plugin-marketplace:remove @scope/plugin-name
```

This will:
- Remove plugin files
- Optionally remove configuration
- Deregister commands and skills

### Remove with Configuration
```
/plugin-marketplace:remove @scope/plugin-name --include-config
```

### Remove All Project Plugins
```
/plugin-marketplace:remove --all --project
```

## Enabling/Disabling

### Disable Plugin (Keep Installed)
```
/plugin-marketplace:disable @scope/plugin-name
```

### Enable Plugin
```
/plugin-marketplace:enable @scope/plugin-name
```

Disabled plugins:
- Keep their files
- Don't load commands/skills
- Don't execute hooks
- Can be re-enabled instantly

## Troubleshooting

### Plugin Conflicts

When two plugins conflict:

1. **Identify the conflict:**
   ```
   /plugin-marketplace:list --verbose
   ```

2. **Check for overlapping commands:**
   - Commands are namespaced by plugin
   - Hooks may conflict if matching same events

3. **Resolution options:**
   - Disable one plugin
   - Configure hook priority
   - Contact plugin authors

### Plugin Not Loading

**Symptoms:** Commands not available, skills not activating

**Diagnostic steps:**
1. Check plugin is installed: `/plugin-marketplace:list`
2. Verify plugin structure is valid
3. Check for errors in plugin manifest
4. Ensure required dependencies are met

### Performance Issues

If plugins are slowing down Claude Code:

1. **Identify slow plugins:**
   - Disable plugins one by one
   - Check hook execution time

2. **Solutions:**
   - Disable unnecessary plugins
   - Report to plugin author
   - Check for plugin updates

## Plugin Lifecycle

```
┌─────────────┐
│  Discovered │
└──────┬──────┘
       │ install
       ▼
┌─────────────┐
│  Installed  │◄────────┐
└──────┬──────┘         │
       │ enable         │ disable
       ▼                │
┌─────────────┐         │
│   Enabled   │─────────┘
└──────┬──────┘
       │ activate (on demand)
       ▼
┌─────────────┐
│   Active    │
└─────────────┘
```

## Best Practices

1. **Regular cleanup** - Remove unused plugins
2. **Keep updated** - Run updates periodically
3. **Backup configs** - Version control your `.claude/` settings
4. **Minimal installs** - Only install what you need
5. **Project vs User** - Use project scope for project-specific needs

## Example Interactions

### User: "What plugins do I have installed?"

**Response:**
Here are your installed plugins:

**User Plugins (~/.claude/plugins/):**
| Plugin | Version | Status |
|--------|---------|--------|
| @claude/git-assistant | 1.5.2 | ✅ Enabled |
| @claude/code-formatter | 2.1.0 | ✅ Enabled |
| @community/test-runner | 1.0.0 | ⚪ Disabled |

**Project Plugins (.claude/plugins/):**
| Plugin | Version | Status |
|--------|---------|--------|
| @company/internal-tools | 3.0.0 | ✅ Enabled |

Would you like details on any specific plugin?

### User: "Remove the test-runner plugin"

**Response:**
I'll remove the @community/test-runner plugin.

```
/plugin-marketplace:remove @community/test-runner
```

✅ Plugin removed successfully.

**Cleaned up:**
- Plugin files from ~/.claude/plugins/test-runner
- Commands: `/test-runner:run`, `/test-runner:watch`

**Note:** Configuration file `.claude/test-runner.local.md` was preserved. Remove it manually if no longer needed.

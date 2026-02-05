---
name: marketplace-structure
description: This skill should be used when the user asks to "create a marketplace", "set up marketplace.json", "organize multiple plugins", "distribute plugins", "host plugins", "marketplace schema", "plugin marketplace structure", "multi-plugin organization", or needs guidance on plugin marketplace creation, marketplace manifest configuration, or plugin distribution strategies.
---

# Marketplace Structure

A plugin marketplace is a catalog of available plugins that enables centralized discovery, version management, and distribution. This skill covers creating and maintaining marketplaces for team or community plugin distribution.

## Overview

Marketplaces provide:

- **Centralized discovery** - Browse plugins from multiple sources in one place
- **Version management** - Track and update plugin versions automatically
- **Team distribution** - Share required plugins across an organization
- **Flexible sources** - Support for relative paths, GitHub repos, and git URLs

### When to Create a Marketplace vs. a Plugin

| Create a Plugin | Create a Marketplace |
|----------------|---------------------|
| Single-purpose extension | Collection of related plugins |
| Used directly by end users | Distributes multiple plugins |
| One team or individual maintains it | Curates plugins from various sources |
| Installed via `/plugin install` | Added via `/plugin marketplace add` |

## Directory Structure

Place `marketplace.json` in the `.claude-plugin/` directory at the repository root:

```text
marketplace-repo/
├── .claude-plugin/
│   └── marketplace.json      # Required: Marketplace manifest
├── plugins/                  # Optional: Local plugin directories
│   ├── plugin-one/
│   │   └── .claude-plugin/
│   │       └── plugin.json
│   └── plugin-two/
│       └── .claude-plugin/
│           └── plugin.json
└── README.md                 # Recommended: Marketplace documentation
```

## Marketplace Schema

The `marketplace.json` manifest defines the marketplace and its available plugins.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Marketplace identifier (kebab-case, no spaces) |
| `owner` | object | Marketplace maintainer information |
| `plugins` | array | List of available plugin entries |

### Owner Object

```json
{
  "owner": {
    "name": "Team Name",
    "email": "team@example.com",
    "url": "https://github.com/team"
  }
}
```

### Optional Metadata

```json
{
  "metadata": {
    "description": "Brief marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  }
}
```

The `pluginRoot` field sets the base path for relative plugin sources.

## Plugin Entry Format

Each plugin in the `plugins` array requires:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case, unique within marketplace) |
| `source` | string or object | Where to fetch the plugin |

### Optional Plugin Fields

Standard metadata fields:

- `description` - Brief plugin description
- `version` - Plugin version (semver)
- `author` - Author information object
- `homepage` - Documentation URL
- `repository` - Source code URL
- `license` - SPDX license identifier
- `keywords` - Tags for discovery
- `category` - Plugin category
- `tags` - Additional searchability tags

Component configuration fields:

- `commands` - Custom paths to command files or directories
- `agents` - Custom paths to agent files
- `hooks` - Hooks configuration or path to hooks file
- `mcpServers` - MCP server configurations

For complete field reference, see `references/schema-reference.md`.

## Plugin Sources

### Relative Paths

For plugins within the same repository:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### GitHub Repositories

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

### Git URLs

For GitLab, Bitbucket, or self-hosted git:

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Strict vs. Non-Strict Mode

The `strict` field controls whether plugins must have their own `plugin.json`:

| Mode | Behavior |
|------|----------|
| `strict: true` (default) | Plugin must include `plugin.json`; marketplace entry supplements it |
| `strict: false` | `plugin.json` optional; marketplace entry serves as complete manifest |

Use `strict: false` when:

- Curating external plugins without modifying their source
- Providing all metadata in the marketplace entry
- Plugin directories contain only commands/agents/skills without manifest

```json
{
  "name": "external-plugin",
  "source": {
    "source": "github",
    "repo": "external/plugin"
  },
  "description": "Complete metadata here",
  "version": "2.0.0",
  "strict": false
}
```

## Best Practices

### Organization

- **One theme per marketplace** - Group related plugins (e.g., "frontend-tools", "security-plugins")
- **Clear naming** - Use descriptive kebab-case names for both marketplace and plugins
- **Version all entries** - Include `version` for every plugin entry
- **Document each plugin** - Provide `description` for discoverability

### Versioning

- Use semantic versioning (X.Y.Z) for marketplace `metadata.version`
- Update marketplace version when adding, removing, or updating plugins
- Consider a CHANGELOG.md for tracking changes

### Distribution

- **GitHub hosting** - Simplest distribution via `/plugin marketplace add owner/repo`
- **Team settings** - Configure `extraKnownMarketplaces` in `.claude/settings.json`
- **Local testing** - Add with `/plugin marketplace add ./path` during development

For detailed distribution patterns, see `references/distribution-patterns.md`.

### Validation

Validate marketplace structure before publishing:

```bash
# Check JSON syntax
jq . .claude-plugin/marketplace.json

# Verify required fields
jq 'has("name") and has("owner") and has("plugins")' .claude-plugin/marketplace.json
```

Use the `plugin-validator` agent with marketplace support for comprehensive validation.

## Complete Example

```json
{
  "name": "team-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@company.com",
    "url": "https://github.com/company"
  },
  "metadata": {
    "description": "Internal development tools for the engineering team",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0"
    },
    {
      "name": "security-scanner",
      "source": {
        "source": "github",
        "repo": "company/security-plugin"
      },
      "description": "Security vulnerability detection",
      "version": "1.5.0",
      "category": "security"
    }
  ]
}
```

## Additional Resources

- `references/schema-reference.md` - Complete field reference for marketplace.json
- `references/distribution-patterns.md` - Hosting and team distribution strategies
- `examples/minimal-marketplace.md` - Single plugin marketplace template
- `examples/team-marketplace.md` - Internal company marketplace template
- `examples/community-marketplace.md` - Public multi-plugin marketplace template

## Related Skills

- **plugin-structure** - For individual plugin `plugin.json` details
- **plugin-validator** agent - For validating marketplace structure
- **`/plugin-dev:create-marketplace`** - Guided marketplace creation workflow

## Working Example

This repository (`plugin-dev`) is itself a marketplace. Examine `.claude-plugin/marketplace.json` at the repository root for a real-world example of marketplace structure and plugin organization.

---
name: Creating and Managing Plugin Marketplaces
description: Use before creating or editing marketplace.json files, setting up marketplace repositories, or when user asks about plugin distribution. Provides expert guidance on marketplace structure, manifest configuration, plugin organization, semantic versioning, and git-based distribution workflows. Invoke when working with marketplace files or discussing how to share multiple plugins to ensure correct manifest structure and installation compatibility.
---

# Claude Code Marketplace Builder

## What is a Marketplace?

A marketplace is a collection of Claude Code plugins that can be shared as a cohesive unit. Marketplaces enable:
- Centralized distribution of multiple related plugins
- Version control and sharing via git repositories
- Team-wide or community-wide plugin discovery
- Organized collections of plugins by theme, team, or purpose

## Marketplace Directory Structure

A marketplace follows this structure:

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace manifest (REQUIRED)
├── plugin-one/
│   └── .claude-plugin/
│       └── plugin.json       # Individual plugin manifest
├── plugin-two/
│   └── .claude-plugin/
│       └── plugin.json
└── README.md                 # Documentation (recommended)
```

### Key Points

- Marketplace manifest must be at `.claude-plugin/marketplace.json` in the marketplace root
- Each plugin within the marketplace has its own `plugin.json` manifest
- Plugins can be in any subdirectory structure you prefer
- Git version control is recommended for sharing and collaboration

## Marketplace Manifest (marketplace.json)

### Location and Requirements

The marketplace manifest MUST be located at:
```
.claude-plugin/marketplace.json
```

This file defines the marketplace metadata and lists all available plugins.

### Required Fields

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name"
  },
  "plugins": []
}
```

**Field Descriptions:**
- `name`: Marketplace identifier in kebab-case (e.g., "team-tools", "data-science-plugins")
- `owner.name`: Maintainer's name (REQUIRED)
- `owner.email`: Maintainer's email (OPTIONAL)
- `plugins`: Array of plugin entries (can be empty initially)

### Optional Metadata Fields

```json
{
  "name": "my-marketplace",
  "description": "Marketplace description",
  "version": "1.0.0",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "homepage": "https://github.com/username/marketplace",
  "plugins": []
}
```

**Additional Fields:**
- `description`: Brief overview of the marketplace's purpose
- `version`: Marketplace version (semantic versioning)
- `homepage`: URL to marketplace documentation or repository

## Adding Plugins to Marketplace

### Plugin Entry Structure

Each plugin in the `plugins` array requires:

```json
{
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugin-directory",
      "description": "Brief description"
    }
  ]
}
```

**Plugin Entry Fields:**
- `name`: Plugin identifier (MUST match the plugin's `plugin.json` name)
- `source`: Path or URL to plugin (see Plugin Sources section)
- `description`: Brief description (optional but recommended for discoverability)

### Example with Multiple Plugins

```json
{
  "name": "team-productivity",
  "owner": {
    "name": "Engineering Team"
  },
  "description": "Productivity tools for our engineering team",
  "plugins": [
    {
      "name": "code-review-helper",
      "source": "./code-review-helper",
      "description": "Automated code review assistance"
    },
    {
      "name": "pr-templates",
      "source": "./pr-templates",
      "description": "Standardized PR templates and workflows"
    },
    {
      "name": "testing-utils",
      "source": "./testing-utils",
      "description": "Test generation and coverage tools"
    }
  ]
}
```

## Plugin Sources

Plugin sources in marketplace.json support multiple formats:

### Local Path (Relative)

```json
{
  "name": "local-plugin",
  "source": "./local-plugin"
}
```

Use for plugins stored within the marketplace directory. Paths must be relative to the marketplace root.

### GitHub Repository

```json
{
  "name": "github-plugin",
  "source": "github:username/repo"
}
```

Use for plugins hosted on GitHub. Claude Code will clone the repository.

### Git URL

```json
{
  "name": "git-plugin",
  "source": "https://github.com/username/repo.git"
}
```

Use for plugins hosted on any Git provider. Full git URLs are supported.

### Mixed Sources Example

```json
{
  "plugins": [
    {
      "name": "internal-tool",
      "source": "./internal-tool",
      "description": "Internal team tool"
    },
    {
      "name": "community-plugin",
      "source": "github:community/awesome-plugin",
      "description": "Community-maintained plugin"
    },
    {
      "name": "external-tool",
      "source": "https://gitlab.com/team/tool.git",
      "description": "External Git repository"
    }
  ]
}
```

## Creating a Marketplace: Step-by-Step

### Step 1: Create Marketplace Directory

```bash
mkdir my-marketplace
cd my-marketplace
```

### Step 2: Create Marketplace Manifest

```bash
mkdir .claude-plugin
```

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name"
  },
  "plugins": []
}
```

### Step 3: Initialize Git (Recommended)

```bash
git init
```

Version control enables:
- Easy sharing via repository URL
- Version history tracking
- Collaboration workflows
- Distribution to users

### Step 4: Add Plugins

For each plugin you want to include:

1. Create plugin directory:
   ```bash
   mkdir my-plugin
   mkdir my-plugin/.claude-plugin
   ```

2. Create plugin manifest (my-plugin/.claude-plugin/plugin.json):
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "Plugin description"
   }
   ```

3. Add plugin components (skills, commands, agents, etc.)

4. Update marketplace.json:
   ```json
   {
     "plugins": [
       {
         "name": "my-plugin",
         "source": "./my-plugin",
         "description": "Plugin description"
       }
     ]
   }
   ```

### Step 5: Test Locally

Add marketplace to Claude Code:

```bash
/plugin marketplace add /path/to/my-marketplace
```

Install and test plugins:

```bash
/plugin install my-plugin@my-marketplace
```

Verify installation:
- Run `/plugin` to see installed plugins
- Check `/help` for new commands
- Test plugin functionality

## Local Development Workflow

### Testing Changes

When modifying plugins in your marketplace:

1. **Uninstall old version:**
   ```bash
   /plugin uninstall plugin-name@marketplace-name
   ```

2. **Reinstall updated version:**
   ```bash
   /plugin install plugin-name@marketplace-name
   ```

Alternatively, restart Claude Code to reload all plugins.

### Development Iteration

Recommended workflow:
1. Make changes to plugin files
2. Uninstall → Reinstall plugin
3. Test functionality
4. Commit changes to git
5. Repeat as needed

### Debugging

Use debug mode to troubleshoot:

```bash
claude --debug
```

This shows:
- Marketplace loading status
- Plugin loading status
- Manifest validation errors
- Component registration
- Any warnings or errors

## Distribution and Sharing

### Sharing Your Marketplace

1. **Commit to git:**
   ```bash
   git add .
   git commit -m "Add marketplace with plugins"
   ```

2. **Push to remote repository:**
   ```bash
   git remote add origin <repository-url>
   git push -u origin main
   ```

3. **Share with users:**
   Users add your marketplace:
   ```bash
   /plugin marketplace add <repository-url>
   ```

   Or for local paths:
   ```bash
   /plugin marketplace add /path/to/marketplace
   ```

4. **Install plugins:**
   ```bash
   /plugin install plugin-name@marketplace-name
   ```

### Managing Plugin Lifecycle

Users can manage installed plugins:

```bash
# Enable plugin
/plugin enable plugin-name@marketplace-name

# Disable plugin
/plugin disable plugin-name@marketplace-name

# Uninstall plugin
/plugin uninstall plugin-name@marketplace-name
```

## Testing Checklist

Before distributing your marketplace:

- [ ] marketplace.json has required fields (name, owner, plugins)
- [ ] All plugin entries have name and source
- [ ] Plugin names match their plugin.json names
- [ ] Local plugin paths are relative and start with `./`
- [ ] All plugins install without errors
- [ ] Tested with `claude --debug` for warnings
- [ ] README.md documents marketplace purpose and plugins
- [ ] Repository is properly initialized with git
- [ ] All changes are committed

## Best Practices

For comprehensive best practices on organization, versioning, distribution, and collaboration, see `reference/best-practices.md`.

## Key Takeaways

### Marketplace Essentials
1. Marketplace manifest MUST be at `.claude-plugin/marketplace.json` (not root)
2. Each plugin entry needs `name`, `source`, and optionally `description`
3. Plugin sources can be local paths (`./plugin`), GitHub repos (`github:user/repo`), or Git URLs
4. Add marketplace once: `/plugin marketplace add <path-or-url>`
5. Install plugins: `/plugin install plugin-name@marketplace-name`

### Development Workflow
1. Create marketplace directory with `.claude-plugin/marketplace.json`
2. Add plugins with their own `plugin.json` manifests
3. Test locally before sharing: `/plugin marketplace add /local/path`
4. Use git for version control and distribution
5. Update workflow: uninstall → reinstall or restart Claude Code

### Distribution
1. Share via git repository URL or local path
2. Users add marketplace, then browse/install plugins
3. Marketplace can mix local and remote plugin sources
4. Use semantic versioning for both marketplace and plugins
5. Document installation and usage in README

## Common Patterns

For detailed examples of personal, team, community, and hybrid marketplace patterns, see `reference/best-practices.md`.

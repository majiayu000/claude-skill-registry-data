---
name: Creating New Plugins
description: Follow a structured approach to create new Claude Code plugins and register them in your marketplace. Use when building plugins for commands, skills, hooks, or MCP servers.
---

# Creating New Plugins

## Overview

A systematic workflow for creating new Claude Code plugins and adding them to your plugin marketplace. This skill guides you through plugin structure, manifest creation, and marketplace registration.

## When to Use

- Creating a new plugin from scratch
- Building plugins with commands, skills, hooks, or MCP servers
- Adding plugins to an existing marketplace
- Structuring a plugin following best practices

## Process

### Step 1: Understand Plugin Requirements

Before creating a plugin, clarify:
- **Purpose**: What does the plugin do? (e.g., browser testing, code review, deployment automation)
- **Components**: What will it include? Commands, skills, hooks, MCP servers, or agents?
- **Target audience**: Who will use this plugin?
- **Dependencies**: What external tools or services does it need?

Ask clarifying questions if the requirements are ambiguous.

### Step 2: Create Plugin Directory Structure

Create the plugin directory with the standard structure:

```
plugin-name/
├── plugin.json          # Plugin manifest
├── .mcp.json           # MCP server config (if using MCP)
├── README.md           # Documentation
├── commands/           # Custom slash commands (optional)
│   └── command-name.md
├── agents/             # Custom agents (optional)
│   └── agent-name.md
├── skills/             # Agent skills (optional)
│   └── skill-name/
│       └── SKILL.md
└── hooks/              # Event handlers (optional)
    └── hooks.json
```

Only create directories for components you're actually using.

### Step 3: Create plugin.json Manifest

Create a `plugin.json` file at the plugin root with required metadata:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Clear description of what the plugin does",
  "author": "Your Name",
  "license": "MIT",
  "mcpServers": [
    {
      "name": "server-name",
      "config": {
        "command": "command-to-run",
        "args": ["arg1", "arg2"]
      }
    }
  ]
}
```

**Key fields:**
- `name`: Lowercase, hyphenated plugin identifier
- `version`: Semantic versioning (1.0.0)
- `description`: One-sentence description of functionality
- `author`: Your name or organization
- `mcpServers`: Array of MCP server configurations (if applicable)

### Step 4: Create Supporting Files

Create necessary supporting files based on plugin components:

**For MCP servers:**
- Create `.mcp.json` with server configuration matching `plugin.json`

**For all plugins:**
- Create `README.md` with documentation including:
  - Features and capabilities
  - Installation instructions
  - Usage examples
  - Requirements and troubleshooting

### Step 5: Register in Marketplace

Add the plugin to your marketplace's `marketplace.json`:

1. Open `.claude-plugin/marketplace.json`
2. Add a new entry in the `plugins` array:

```json
{
  "name": "plugin-name",
  "source": "./plugin-name",
  "description": "Clear description of what the plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "homepage": "https://your-repo-url",
  "repository": "https://your-repo-url",
  "keywords": ["keyword1", "keyword2"],
  "category": "category-name",
  "tags": ["tag1", "tag2"]
}
```

3. Ensure JSON is valid (valid commas, proper nesting)
4. Save the file

### Step 6: Verify Plugin Structure

Check that:
- Plugin directory exists at the path specified in `marketplace.json`
- `plugin.json` is in the plugin root (not in a subdirectory)
- Required directories (`commands/`, `skills/`, etc.) are at plugin root, not in `.claude-plugin/`
- All component markdown files are properly formatted
- `README.md` exists with clear documentation
- JSON files are valid (use `jq` to validate if needed)

### Step 7: Test the Plugin

To test locally:

1. Start Claude Code from the marketplace parent directory
2. Use `/plugin marketplace add ./path/to/marketplace`
3. Use `/plugin install plugin-name@marketplace-name`
4. Restart Claude Code
5. Verify with `/help` to see new commands
6. Test all plugin functionality

## Common Patterns

### Creating an MCP Plugin

1. Set up directory structure with `plugin.json` and `.mcp.json`
2. In `plugin.json`, add `mcpServers` array with server details
3. In `.mcp.json`, include `mcpServers` object with configuration
4. Document required dependencies in `README.md`
5. Test that MCP server starts correctly

### Creating a Skills Plugin

1. Create `skills/` directory at plugin root
2. Create subdirectory for each skill: `skills/skill-name/`
3. Add `SKILL.md` file in each skill subdirectory
4. Update `plugin.json` to reference skills: `"skills": ["skills/"]`
5. Document skill usage in `README.md`

### Creating a Commands Plugin

1. Create `commands/` directory at plugin root
2. Create markdown files: `commands/command-name.md`
3. Format with YAML frontmatter and markdown content
4. Document commands in `README.md`
5. Test commands with `/command-name`

## Critical Points

**Directory Structure:**
- Component directories (`commands/`, `skills/`, etc.) go at plugin root
- Never place components inside `.claude-plugin/`
- `plugin.json` must be at plugin root, not nested

**Manifest Files:**
- `plugin.json` defines the plugin itself
- `marketplace.json` registers the plugin in your marketplace
- Both must be valid JSON with proper formatting

**Naming Conventions:**
- Plugin names: lowercase, hyphenated (e.g., `browser-testing`, `code-review`)
- Directory names: match plugin name or use descriptive names
- Commands: lowercase, hyphenated (e.g., `/test-browser`, `/review-pr`)

**Metadata:**
- Version follows semantic versioning (MAJOR.MINOR.PATCH)
- Description is concise (one sentence)
- Keywords and tags aid discoverability
- License should be specified (typically MIT)

## Troubleshooting

**Plugin doesn't appear in marketplace:**
- Verify entry exists in `.claude-plugin/marketplace.json`
- Check that source path is correct relative to marketplace
- Ensure JSON is valid with no syntax errors
- Restart Claude Code

**Commands not available after installation:**
- Verify `commands/` directory is at plugin root
- Check command markdown files have proper frontmatter
- Restart Claude Code to load changes
- Check `/help` to see if commands are listed

**MCP server fails to start:**
- Verify `.mcp.json` has correct command and arguments
- Test command runs manually (e.g., `npx @playwright/mcp@latest`)
- Check all dependencies are installed
- Review MCP server documentation

## Next Steps

After creating a plugin:
1. Test all functionality thoroughly
2. Add to your marketplace for team access
3. Document any team-specific setup requirements
4. Share marketplace with team members
5. Iterate based on feedback

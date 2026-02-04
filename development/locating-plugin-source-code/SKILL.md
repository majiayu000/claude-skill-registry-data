---
name: Locating Plugin Source Code
description: Use when you need to find the source code location of installed plugins, explore plugin structure, access reference materials in plugins, or debug plugin issues. Provides step-by-step guidance to trace installed plugins back to their local repository locations by reading ~/.claude/plugins/installed_plugins.json and navigating to the installPath. Useful for finding skills, commands, reference docs, or understanding plugin implementation.
---

# Locating Plugin Source Code

This skill helps you find and navigate to the source code of installed Claude Code plugins.

## When to Use This Skill

Use this skill when you need to:
- Find the source code location of an installed plugin
- Access reference materials within a plugin (e.g., JWT security docs in pr-review)
- Explore plugin structure and organization
- Debug plugin issues or understand implementation details
- Contribute to or modify a locally-installed plugin
- Find specific skill files or command files within a plugin

## How Plugin Installation Works

When plugins are installed locally:
- Installation metadata is stored in `~/.claude/plugins/installed_plugins.json`
- Each plugin entry contains an `installPath` pointing to the actual source code location
- For local marketplace installations, the path typically points to a git repository on your machine

## Step-by-Step: Finding Plugin Source Code

### Step 1: Read the Installation Metadata

Read the installed plugins file to find plugin information:

```bash
# Read the installed plugins metadata
cat ~/.claude/plugins/installed_plugins.json
```

This file contains entries like:
```json
{
  "version": 1,
  "plugins": {
    "plugin-name@marketplace-name": {
      "version": "1.0.0",
      "installedAt": "2025-10-27T17:15:15.309Z",
      "lastUpdated": "2025-10-27T17:15:15.309Z",
      "installPath": "/Users/username/src/marketplace-repo/plugin-name",
      "gitCommitSha": "abc123...",
      "isLocal": true
    }
  }
}
```

**Key field**: The `installPath` contains the absolute path to the plugin's source code.

### Step 2: Navigate to the Plugin Source

Use the `installPath` from Step 1 to navigate to the plugin:

```bash
cd /path/from/installPath
```

### Step 3: Explore Plugin Structure

Once in the plugin directory, explore its contents:

```bash
# List the plugin structure
ls -la

# Find all markdown files (skills, commands, reference docs)
find . -name "*.md" -o -name "*.MD"

# Find specific content (e.g., JWT security docs)
find . -name "*jwt*" -o -name "*security*"
```

### Step 4: Access Specific Components

Common plugin structure:
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json        # Plugin manifest
├── skills/
│   └── skill-name/
│       ├── SKILL.md       # Main skill file
│       └── reference/     # Additional documentation
│           ├── best-practices.md
│           └── examples.md
├── commands/
│   └── command-name.md    # Slash commands
└── README.md
```

To read specific files, use the Read tool with the full path:
- Skills: `{installPath}/skills/{skill-name}/SKILL.md`
- Reference docs: `{installPath}/skills/{skill-name}/reference/{doc-name}.md`
- Commands: `{installPath}/commands/{command-name}.md`

## Example: Finding pr-review JWT Security Docs

**Goal**: Find JWT security best practices in the pr-review skill.

**Step 1**: Read installed plugins
```bash
cat ~/.claude/plugins/installed_plugins.json
```

**Step 2**: Locate the pr-review plugin entry and extract installPath
```json
"bbrowning-claude@bbrowning-marketplace": {
  "installPath": "/Users/bbrowning/src/bbrowning-claude-marketplace/bbrowning-claude"
}
```

**Step 3**: Find markdown files in that location
```bash
find /Users/bbrowning/src/bbrowning-claude-marketplace/bbrowning-claude -name "*.md"
```

**Step 4**: Locate the JWT security reference
```
/Users/bbrowning/.../skills/pr-review/reference/jwt-security.md
```

**Step 5**: Read the file
Use the Read tool on the full path.

## Validation Checklist

After locating plugin source code:
- [ ] Verified `installPath` exists in `installed_plugins.json`
- [ ] Confirmed the directory exists at the `installPath`
- [ ] Found the plugin's `.claude-plugin/plugin.json` manifest
- [ ] Located the specific component (skill, command, reference doc) you need
- [ ] Successfully read the target file

## Common Patterns

### Pattern 1: Finding All Skills in a Plugin

```bash
# From the installPath
find . -name "SKILL.md"
```

### Pattern 2: Finding Reference Documentation

```bash
# Look for reference directories
find . -type d -name "reference"

# List reference docs in a specific skill
ls skills/skill-name/reference/
```

### Pattern 3: Searching for Specific Content

```bash
# Find files containing specific keywords
grep -r "jwt" . --include="*.md"
grep -r "security" . --include="*.md"
```

## Tips

- **Multiple plugins from same marketplace**: If a marketplace contains multiple plugins, each will have its own subdirectory within the marketplace repository
- **Local vs remote plugins**: The `isLocal` field indicates if the plugin is installed from a local path (true) or remote git URL (false)
- **Git repository**: If the plugin is in a git repository, you can see the installed commit via `gitCommitSha`
- **Plugin updates**: The `lastUpdated` timestamp shows when the plugin was last updated

## Troubleshooting

**Problem**: `installPath` directory doesn't exist
- The plugin may have been moved or the marketplace repository relocated
- Check if the repository exists elsewhere on your system
- Reinstall the plugin if necessary

**Problem**: Can't find specific file in plugin
- Verify you're looking in the correct component directory (skills/ vs commands/)
- Check the plugin's `plugin.json` to see which directories are configured
- Some plugins may organize files differently than expected

**Problem**: Multiple versions of same plugin
- Check all entries in `installed_plugins.json` for the plugin name
- The marketplace suffix (@marketplace-name) distinguishes different sources

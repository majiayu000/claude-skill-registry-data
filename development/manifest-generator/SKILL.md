---
name: manifest-generator
description: Generate and validate plugin manifest files (plugin.json, marketplace.json). Use when creating new plugins, updating manifests, adding plugins to marketplaces, or preparing for distribution.
allowed-tools: Read, Write, Glob
---

# Manifest Generator

This skill provides knowledge for generating and managing Claude Code plugin manifests.

## plugin.json Generation

### Template

```json
{
  "name": "[plugin-name]",
  "version": "1.0.0",
  "description": "[brief description]",
  "author": {
    "name": "[author name]",
    "email": "[optional email]"
  },
  "license": "MIT",
  "keywords": ["[keyword1]", "[keyword2]"],
  "repository": "[optional repo URL]",
  "homepage": "[optional docs URL]"
}
```

### Auto-Discovery Patterns

Scan for components using these patterns:

| Component | Pattern | Example |
|-----------|---------|---------|
| Skills | `skills/*/SKILL.md` | `skills/my-skill/SKILL.md` |
| Commands | `commands/**/*.md` | `commands/pb/validate.md` |
| Agents | `agents/*.md` | `agents/validator.md` |
| Hooks | `hooks/hooks.json` | - |
| MCP | `.mcp.json` | - |

### Generation Process

1. **Read existing manifest** (if any)
2. **Scan plugin directory** for components
3. **Extract metadata** from discovered files
4. **Generate keywords** from skill/command names
5. **Prompt user** for missing required fields
6. **Write manifest** to `.claude-plugin/plugin.json`

## marketplace.json Generation

### Template

```json
{
  "name": "[marketplace-name]",
  "owner": {
    "name": "[owner name]",
    "email": "[optional email]"
  },
  "plugins": [
    {
      "name": "[plugin-name]",
      "source": "./plugins/[plugin-name]",
      "description": "[plugin description]",
      "version": "[version]",
      "keywords": ["[keyword1]"]
    }
  ]
}
```

### Adding Plugin to Marketplace

1. Read existing `marketplace.json`
2. Check if plugin already exists (update vs add)
3. Extract plugin metadata from its `plugin.json`
4. Add/update entry in plugins array
5. Write updated `marketplace.json`

## Version Management

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

### Version Bumping

```
1.0.0 → 1.0.1  (patch: fix)
1.0.1 → 1.1.0  (minor: feature)
1.1.0 → 2.0.0  (major: breaking)
```

### Auto-Increment

When updating an existing manifest:
- Default: increment PATCH
- User can specify: `--major`, `--minor`, `--patch`

## Validation Rules

Before writing manifests, validate:

### plugin.json
- [ ] `name` is lowercase, alphanumeric, hyphens
- [ ] `version` follows semver
- [ ] `description` is present and meaningful
- [ ] `author.name` is present
- [ ] JSON is valid

### marketplace.json
- [ ] `name` is present
- [ ] `owner.name` is present
- [ ] `plugins` is an array
- [ ] Each plugin has `name` and `source`
- [ ] Source paths exist

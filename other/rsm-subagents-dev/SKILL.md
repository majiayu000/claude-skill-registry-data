---
name: rsm-subagents-dev
description: >
  Guides the user through developing, validating, and publishing plugins for the
  rsm-subagents local marketplace. Activate when the user mentions "rsm-subagents",
  "create rsm plugin", "marketplace plugin", "local plugin development",
  "plugin workflow", "plugin validate", or wants to add a new plugin to the
  rsm-subagents directory.
---

# rsm-subagents Plugin Development

This skill covers creating, validating, and updating plugins in the local
rsm-subagents marketplace at `rsm-subagents/plugins/`.

## Architecture

```
rsm-subagents/
  .claude-plugin/
    marketplace.json        # Lists all plugins (source: "./plugins/<name>")
  plugins/
    <name>/
      .claude-plugin/
        plugin.json         # Name, version, description, author, keywords
      agents/               # Agent definitions (.md with frontmatter)
      commands/             # Slash commands (invoked as /plugin:command)
      skills/               # Auto-triggered skills (matched by context)
```

## Critical: commands/ vs skills/

This distinction is the most common source of confusion:

| Directory | Trigger | User invokes as | Has argument-hint | Has allowed-tools |
|-----------|---------|-----------------|-------------------|-------------------|
| `commands/` | Explicit slash command | `/plugin-name:command-name` | Yes | Yes |
| `skills/` | Auto-matched by description keywords | Automatic (context match) | No | No |

- **commands/** contain `.md` files with `argument-hint` and `allowed-tools` in frontmatter. They are slash commands the user types explicitly.
- **skills/** contain directories with `SKILL.md` files. They are loaded automatically when the conversation context matches the description's trigger phrases.

If you put a slash command in `skills/`, it will never appear as `/plugin:name`. If you put an auto-trigger skill in `commands/`, it will never auto-activate.

## Plugin Development Steps

### 1. Create the plugin structure

```bash
mkdir -p rsm-subagents/plugins/<name>/.claude-plugin
mkdir -p rsm-subagents/plugins/<name>/agents
mkdir -p rsm-subagents/plugins/<name>/commands
mkdir -p rsm-subagents/plugins/<name>/skills/<skill-name>/references
```

### 2. Write plugin.json

```json
{
  "name": "<name>",
  "version": "0.1.0",
  "description": "...",
  "author": { "name": "Ray Manaloto" },
  "keywords": ["..."]
}
```

**minVersion gotcha**: Do NOT add `minVersion` or other unrecognized keys to
plugin.json. The validator rejects unknown fields and validation will fail.

### 3. Validate with the authoritative tool

```bash
claude plugin validate rsm-subagents/plugins/<name>
```

This is the single source of truth for plugin correctness. Run it after every
change. The plugin-dev validator agent and validate-agent.sh are supplementary
but `claude plugin validate` is authoritative.

### 4. Add to marketplace.json

Edit `rsm-subagents/.claude-plugin/marketplace.json`:

```json
{
  "name": "<name>",
  "source": "./plugins/<name>",
  "description": "...",
  "version": "0.1.0",
  "category": "devtools",
  "tags": ["..."],
  "repository": "https://github.com/ray-manaloto/rsm-subagents"
}
```

### 5. Enable in settings

Add to `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "<name>@rsm-subagents": true
  }
}
```

### 6. Clear cache and install

```bash
# Clear stale cache (REQUIRED after source changes)
rm -rf ~/.claude/plugins/cache/rsm-subagents/<name>

# Then reinstall
/plugin
/reload-plugins
```

**Cache clearing is mandatory** after any source change. Without it, `/plugin`
may install the stale cached version.

## Updating an Existing Plugin

1. Edit files in `rsm-subagents/plugins/<name>/`
2. Run `claude plugin validate rsm-subagents/plugins/<name>`
3. Clear cache: `rm -rf ~/.claude/plugins/cache/rsm-subagents/<name>`
4. Reinstall: `/plugin` then `/reload-plugins`

Bumping the version in plugin.json is recommended but not strictly required
for local directory marketplaces.

## Troubleshooting

- **Skills not loading**: Check `~/.claude/plugins/installed_plugins.json` has the entry, cache directory exists, and plugin is in `enabledPlugins`
- **Validation fails on unknown keys**: Remove `minVersion` or any non-standard fields from plugin.json
- **Slash command not appearing**: Verify the file is in `commands/`, not `skills/`
- **Skill not auto-triggering**: Verify the SKILL.md description contains relevant trigger phrases

## Full Reference

See `docs/rsm-subagents-plugin-workflow.md` for the complete lifecycle documentation.

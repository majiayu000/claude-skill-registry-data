---
name: create-plugin
description: "Create, update, validate, and package Canvas Plugins. Use when users want to build a Canvas plugin, bundle multiple skills into a plugin, define plugin metadata, add icons or logos, declare recommended Composio, Canvas Email, or MCP connectors, prepare a marketplace entry, or submit a plugin to the Canvas Plugin Store."
compatibility: Requires filesystem access to the Canvas repository or plugin marketplace repository
metadata:
  version: "1.0.0"
  author: canvas-studios
---

# Create Plugin

Use this skill to create production-ready Canvas Plugins.

A Canvas Plugin is a bundle that combines:

- one plugin manifest at `.canvas-plugin/plugin.json`
- one or more bundled skills under `skills/`
- optional visual assets such as `assets/icon.svg` and `assets/logo.svg`
- optional connector recommendations for Composio, Canvas Email, and MCP servers
- optional marketplace metadata in a registry entry

Plugins should teach the agent which workflows belong together. They should not secretly install external services, write connector configuration, or store secrets.

## Default Workflow

1. Clarify the plugin's audience, workflows, bundled skills, and connector recommendations.
2. Choose a stable plugin name in lowercase kebab-case.
3. Scaffold the plugin package:

   ```text
   plugins/<plugin-name>/<version>/
   ├── .canvas-plugin/plugin.json
   ├── assets/
   │   ├── icon.svg
   │   └── logo.svg
   ├── connectors/
   │   └── optional-example.mcp.json
   ├── skills/
   │   └── <skill-name>/
   │       ├── SKILL.md
   │       └── agents/canvas.yaml
   └── LICENSE
   ```

4. Validate that every bundled skill has a unique `name` and a useful trigger-focused `description`.
5. Add connector recommendations only as metadata. The user must explicitly connect Composio apps, Canvas Email accounts, or MCP servers in the UI.
6. For a personal Canvas installation, call `install_canvas_plugin_from_workspace` with the package directory. To update an installed plugin, first call `inspect_canvas_plugin`, then call `update_canvas_plugin_from_workspace` with its version and checksum.
7. Use `set_canvas_plugin_enabled` to toggle it and `remove_canvas_plugin` to remove it. Removal deliberately stops when a materialized skill was edited, so the agent must preserve or resolve that user work explicitly.
8. Package or commit the plugin to the marketplace repository only after validation passes.

## Manifest Template

Use this shape for `.canvas-plugin/plugin.json`:

```json
{
  "name": "sales-operations",
  "version": "1.0.0",
  "description": "Coordinate sales workflows with CRM, email, and research connector recommendations.",
  "license": "MIT",
  "author": {
    "name": "Canvas Studios"
  },
  "source": "https://github.com/canvascoding/canvas-notebook-plugin-marketplace/tree/main/plugins/sales-operations/1.0.0",
  "skills": "./skills",
  "interface": {
    "displayName": "Sales Operations",
    "shortDescription": "Prepare account research and sales follow-ups",
    "category": "Sales",
    "brandColor": "#0F766E",
    "icon": "./assets/icon.svg",
    "logo": "./assets/logo.svg",
    "defaultPrompt": [
      "Use /sales-account-brief to prepare a target-account brief."
    ]
  },
  "connectors": {
    "composio": [
      {
        "toolkit": "hubspot",
        "label": "HubSpot",
        "recommended": true,
        "reason": "Use CRM records and company data during sales workflows."
      }
    ],
    "email": [
      {
        "kind": "mailbox",
        "label": "Sales inbox",
        "providers": ["gmail", "imap-smtp"],
        "recommended": true,
        "reason": "Read and send sales email through Canvas Email, not through Composio Gmail."
      }
    ],
    "mcp": [
      {
        "name": "sales-research",
        "label": "Sales Research MCP",
        "configPath": "./connectors/sales-research.mcp.json",
        "recommended": true,
        "env": ["SALES_RESEARCH_API_KEY"],
        "oauth": true,
        "reason": "Optional external research tools for account enrichment."
      }
    ]
  }
}
```

## Connector Rules

Composio recommendations:

- Use Composio toolkit slugs such as `hubspot`, `slack`, or `linear`.
- Include `label`, `reason`, and `recommended` or `required`.
- Do not include API keys, connected-account IDs, trigger IDs, or user-specific secrets.
- Do not recommend Gmail through Composio for email workflows. Use Canvas Email.

Canvas Email recommendations:

- Use `connectors.email[]` for mailbox needs.
- Supported provider hints are `gmail` and `imap-smtp`.
- Explain why the mailbox is useful, but leave account connection to the UI.

MCP recommendations:

- Use `connectors.mcp[]` for optional MCP servers.
- Put example server config under `connectors/*.mcp.json`.
- List required environment variable names in `env`.
- Set `oauth: true` when OAuth may be required.
- Do not merge MCP config automatically.

## Skill Bundling Rules

Each bundled skill should be narrow enough to be useful independently and clear enough to trigger correctly.

Use this skill layout:

```text
skills/<skill-name>/SKILL.md
skills/<skill-name>/agents/canvas.yaml
```

`SKILL.md` frontmatter should include:

```yaml
---
name: sales-account-brief
description: "Use this skill to prepare a target-account sales brief from CRM context, email context, and research notes."
license: "MIT"
metadata:
  version: "1.0.0"
---
```

`agents/canvas.yaml` should include UI metadata:

```yaml
interface:
  display_name: Sales Account Brief
  short_description: Prepare a target-account sales brief
  brand_color: "#0F766E"
  icon_small: "./icon.svg"
```

## Marketplace Registry Entry

When preparing an official marketplace entry, add the plugin to `registry.json` in the marketplace repo.

Required fields:

- `name`
- `displayName`
- `description`
- `latestVersion`
- `versions[version].downloadUrl`
- `versions[version].packagePath`
- `versions[version].checksum`
- `versions[version].manifestPath`

The checksum should be the Canvas Plugin package checksum, not a checksum of the whole git repository.

## Validation Checklist

Before handing off:

- `.canvas-plugin/plugin.json` exists and is valid JSON.
- `name` is lowercase kebab-case.
- `version` is semantic, for example `1.0.0`.
- `skills` points to a package-local directory.
- Every `connectors.mcp[].configPath` points to an existing file.
- Icons and logos are package-local image files.
- No secrets, tokens, personal account IDs, or generated local paths are committed.
- Local installation succeeds through the Canvas Plugin installer.
- Marketplace install succeeds from a registry archive when publishing to the store.

---
name: plugin-creator
description: Create and validate Nosis Plugin packages containing Skills, Agent roles, MCP servers and command hooks. Use when scaffolding a plugin, adding components or checking its manifest.
---

# Plugin Creator

A Nosis Plugin contains a `plugin.json` declaring its Skills, Agent roles, MCP servers and command hooks.
Install the package under `~/.nosis/plugins/<plugin-name>/`.

## Quick Start

1. Scaffold the package:

```bash
# Run from this skill's directory.
python3 scripts/create_basic_plugin.py <plugin-name> --with-skills --with-agents --with-mcp --with-hooks
```

The default target is `~/.nosis/plugins/<plugin-name>`; use `--path <parent-directory>` to create
it elsewhere. New names are normalized to lower-case hyphen-case, up to 64 characters.

2. Fill in `description` and `version` in `plugin.json`.

3. Fill the declared components. Every component entry is a path relative to the plugin root:

| Component | Points at | Registers as |
| --- | --- | --- |
| `skills` | A directory whose children are skill folders containing `SKILL.md` | `<plugin>:<skill>` |
| `agents` | A Markdown file whose front matter declares the role | `<plugin>:<agent>` sub-agent role |
| `mcp` | A JSON file mapping server names to server configs | `<plugin>:<server>` |
| `hooks` | A versioned JSON file declaring command hooks | `<plugin>:<hook>` |

See [the component contract](references/plugin-json-spec.md) for supported fields and examples.

4. Validate before handing the plugin back:

```bash
python3 scripts/validate_plugin.py <plugin-path>
```

Then verify the plugin in Nosis. Static validation cannot confirm MCP tool availability or approval.

For Hooks, read [the authoring contract](references/hooks.md). `--with-hooks` creates an empty
declaration; add scripts and verify matching and non-matching cases in Nosis.

## Required Behavior

- Keep the manifest at `<plugin-root>/plugin.json` with exactly that name.
- Use a unique manifest `name`; it prefixes every component's registered name.
- Declare existing components using paths relative to and inside the plugin root.
- Use only supported manifest fields. `capabilities` describes components; it enables nothing.
- Author Skill content with the `skill-creator` skill.
- Reference roles as `<plugin>:<agent>` and MCP tools as `mcp__<plugin>_<server>__<tool>`.
  Agent `tools` must explicitly select MCP tools; omitting it grants only built-in role defaults.
- Resolve validation and Nosis startup warnings before delivery.
- Run `/refresh` while idle after installing or changing a plugin. See the installation reference for
  updating running MCP server code.

## References

- [Manifest and component contract](references/plugin-json-spec.md)
- [Hook declarations, command input/output and verification](references/hooks.md)
- [Installation, updates and troubleshooting](references/installing-and-updating.md)

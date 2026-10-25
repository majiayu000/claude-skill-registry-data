---
name: client-config-opencode
description: 'Manage OpenCode configuration files (V2 native format by default, V1 supported) including MCP servers, providers, models, agents, commands, permissions, policies, skills, plugins, CLI/TUI settings, keybinds, and themes. Use this skill whenever the user wants to view, edit, add, migrate, or understand any opencode setting in opencode.json(c), cli.json, or tui.json. Trigger on: "configure opencode", "add provider", "set model", "add MCP server", "create agent", "configure permissions", "change theme", "add keybind", "show opencode config", "add custom command", "migrate opencode config to V2", or "opencode cli.json".'
---

# OpenCode Configuration Manager

You help the user manage OpenCode configuration. OpenCode has two config formats:

- **V2 native** (default for new output): plural keys (`permissions`, `agents`, `providers`, `commands`,
  `plugins`), ordered permission rules, `mcp.servers`, and a global `cli.json` for the terminal client.
- **V1**: singular keys (`permission`, `agent`, `provider`, `command`, `plugin`), servers directly under `mcp`,
  and `tui.json` for the terminal client. V2 still reads V1 config.

## Step 1 — Pick the format

1. **Read the target file first.** If it does not exist, use V2.
2. **User says which version** ("I'm on V1", "opencode 1.x") → use that.
3. **Detect from existing content** (or run `python scripts/show-config.py`, which prints a detected format):

   | V2 signals | V1 signals |
   |------------|------------|
   | `permissions` array, `agents`, `providers`, `commands`, `plugins` | `permission` object/string, `agent`, `provider`, `command`, `plugin`, `tools` |
   | `mcp.servers`, `mcp.timeout`, server `disabled` | server names directly under `mcp`, server `enabled` |
   | `snapshots`, `media`, `update`, `warming`, `websearch`, `worktree` | `snapshot`, `attachment`, `autoupdate`, `small_model`, `logLevel`, `server` |
   | `compaction.keep` / `buffer`; model `#variant` refs | `compaction.reserved` / `tail_turns`; separate `variant` field |
   | `~/.config/opencode/cli.json` exists | `tui.json` present, no `cli.json` |

4. **V1-shaped file → stay V1** for edits to it unless the user asks to migrate. Mixed files are legal: V1 and V2
   fields may coexist at the **top level**, but each nested entry (one agent, provider, command, or model) must be
   entirely one format. Never point a V1 install at a file you converted to V2-only shapes.
5. For "migrate to V2" requests, load `references/v2/migration.md`.

## Config file map

| What | V2 | V1 |
|------|----|----|
| Core settings (system, managed) | macOS `/Library/Application Support/opencode`, Linux `/etc/opencode`, Windows `%ProgramData%\opencode`; highest precedence (2.0.29 docs) | same directories; see `references/config-schema.md` (Managed / enterprise) |
| Core settings (global) | `~/.config/opencode/opencode.json(c)` | same |
| Core settings (project) | `opencode.json(c)` and `.opencode/opencode.json(c)`, searched cwd → filesystem root; `.opencode/` files override direct ones | `opencode.json` in cwd or nearest up to the Git root |
| Terminal client (theme, keybinds) | `~/.config/opencode/cli.json` — global only | `~/.config/opencode/tui.json` + project `tui.json` |
| Agents | `~/.config/opencode/agents/<name>.md`, `.opencode/agents/<name>.md` | same |
| Commands | `~/.config/opencode/commands/<name>.md`, `.opencode/commands/<name>.md` | same |
| Skills | `.opencode/skills/<id>/SKILL.md` (+ `.claude/skills`, `.agents/skills`) | same |
| Plugins | `.opencode/plugins/`, `~/.config/opencode/plugins/` | same |
| Themes | `~/.config/opencode/themes/*.json`, `.opencode/themes/*.json` (new V2 format) | same dirs, V1 format |
| Instructions | `AGENTS.md` only (`instructions` array is not loaded) | `AGENTS.md`, `CLAUDE.md` fallback, `instructions` array |
| Credentials | SQLite DB (`opencode debug paths db`) — use `/connect` / `opencode auth` | `~/.local/share/opencode/auth.json` — use `/connect` / `opencode auth` |

Schemas: `https://opencode.ai/config.json` (both formats use this URL; it currently validates only the V1 shape, so
editors may flag V2 keys), `https://opencode.ai/v2/cli.json`, `https://opencode.ai/tui.json` (V1).

Merge behavior: config files merge; later/closer files override conflicting keys. V2 exceptions: `permissions`,
`plugins`, and `skills` arrays accumulate, and policies let broader config win.

## Task → Reference map (load only what's needed)

| Task | V2 (default) | V1 |
|------|--------------|----|
| Providers, API keys, models, variants | `references/v2/providers.md` | `references/providers.md` |
| MCP servers | `references/v2/mcp.md` | `references/mcp.md` |
| Agents (built-in and custom) | `references/v2/agents.md` | `references/agents.md` |
| Permissions, policies | `references/v2/permissions.md` | `references/permissions.md` |
| Theme, keybinds, terminal UI | `references/v2/cli.md` | `references/tui.md` |
| Plugins (config and API) | `references/v2/plugins.md` | `references/config-schema.md` |
| Commands, skills, formatters, compaction, misc fields | `references/v2/config-schema.md` | `references/config-schema.md` |
| Full schema / unknown field | `references/v2/config-schema.md` | `references/config-schema.md` |
| Migrating V1 → V2 | `references/v2/migration.md` | — |

## Common quick edits (V2 native)

```jsonc
{ "model": "anthropic/claude-sonnet-4-5" }                       // default model (no #variant at root)
{ "agents": { "title": { "model": "anthropic/claude-haiku-4-5" } } } // V1: "small_model"
{ "default_agent": "build" }
{ "update": "notify" }                                            // "disable" | "notify" | "auto"; V1: "autoupdate"
{ "snapshots": false }                                            // V1: "snapshot"
{ "formatter": true }                                             // same in V1
{ "websearch": { "provider": "random" } }                         // V2 only
{ "permissions": [{ "action": "shell", "resource": "git push *", "effect": "ask" }] }
{ "policies": [{ "action": "provider.use", "resource": "openai", "effect": "deny" }] }   // 2.0.29+; was "experimental.policies"
{ "tool_output": { "max_lines": 2000, "max_bytes": 51200 } }      // same in V1
```

V1 equivalents for provider filtering: `"enabled_providers": [...]`, `"disabled_providers": [...]`. V1 log level
`"logLevel"` has no V2 field — V2 uses the `OPENCODE_LOG_LEVEL` env var.

> [!NOTE]
> V1 deprecations: `autoshare` → `share`; agent `maxSteps` → `steps`; `tools` → `permission`; `mode` → `agent`.
> In V2, `share` is accepted but session sharing is not supported yet.

## Variable substitution

- `{env:MY_API_KEY}` — environment variable (V1 and V2)
- `{file:~/.secrets/key.txt}` — file contents (documented for V1; not shown in V2 docs, but verified working in V2 2.0.27 for agent `system`)

V2 runs a shared background server: env vars must reach it (`opencode service set env NAME value`, or run
`opencode --standalone` from a shell that has them).

## Workflow

1. **Pick the format** (Step 1) and load only the matching reference files.
2. **Read the target file** before changing it.
3. **Edit safely** — use targeted edits; keep JSONC comments intact; validate JSON/JSONC afterward.
4. **Confirm** — show exactly what changed. For V2, suggest `opencode debug config` to verify sources.

## Scripts

- `scripts/show-config.py` — display all config files (V1 and V2, JSONC-aware) with a detected-format summary; secrets are redacted and unparsable files are not echoed
- `scripts/update-references.py` — fetch latest upstream docs for self-update

Run with: `python scripts/<script>.py`

## Self-update procedure

When the user asks to **update**, **refresh**, or **sync** this skill:

1. Run `python scripts/update-references.py` → fetches docs to `_fetched/`
2. If the script exits nonzero, resolve the reported failures and rerun it; do not use a partial `_fetched/` set
3. Read each `_fetched/` file alongside its `references/` or `references/v2/` file (see `manifest.json` `used_by`)
4. Update the reference files to reflect documentation changes
5. Delete `_fetched/` and report what changed

Source URLs are in `sources.json`.

## Safety rules

- Always read the file before editing
- Config files merge — editing global doesn't remove project overrides
- Never edit credential stores (`auth.json` in V1, the SQLite DB in V2) — use `/connect` or `opencode auth`
- Validate JSON/JSONC is well-formed after any edit
- Keep each nested agent/provider/command/model entry in a single format
- For agent and command Markdown files: preserve the YAML frontmatter structure
- V1 plugin code does not run in V2 — flag this when a V1 user with plugins asks about upgrading

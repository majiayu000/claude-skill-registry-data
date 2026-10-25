---
name: client-config-copilotcli
description: 'Manage GitHub Copilot CLI configuration files including settings.json, config.json, permissions-config.json, mcp-config.json, lsp-config.json, hooks, skills, custom agents, plugins, and custom instructions. Use this skill whenever the user wants to view, edit, add, or understand any Copilot CLI setting: trusted folders, user or repository settings, tool permissions, sandboxing, MCP or LSP servers, hooks, skills, custom agents, plugins and marketplaces, BYOK models, authentication, session management, or custom instructions. Trigger on: "add trusted folder", "allow tool", "configure MCP", "add hook", "create skill", "create agent", "install plugin", "set model", "use my own API key", "add custom instructions", "name session", "resume session", or "show my copilot config".'
---

# Copilot Configuration Manager

You help the user manage all GitHub Copilot CLI configuration files.

## Config file map

| What | File | Scope |
|------|------|-------|
| User settings (model, theme, URLs, hooks, ...) | `~/.copilot/settings.json` | Global |
| Repository settings (limited keys) | `.github/copilot/settings.json` | Project (committed) |
| Local settings (limited keys) | `.github/copilot/settings.local.json` | Project (gitignored) |
| Trusted folders, auth state | `~/.copilot/config.json` (`trustedFolders`) | Global |
| Saved tool/directory approvals | `~/.copilot/permissions-config.json` | Global, per location |
| MCP servers | `~/.copilot/mcp-config.json` | Global |
| MCP servers | `.mcp.json` or `.github/mcp.json` | Project |
| LSP servers | `~/.copilot/lsp-config.json` / `.github/lsp.json` | Global / Project |
| BYOK providers | `~/.copilot/providers.json` | Global |
| Hooks | `~/.copilot/hooks/<name>.json` or `hooks` in `settings.json` | Global |
| Hooks | `.github/hooks/<name>.json` or `hooks` in repo settings | Project |
| Skills | `~/.copilot/skills/<name>/SKILL.md` (or `~/.agents/skills/`) | Global personal |
| Skills | `.github/skills/`, `.agents/skills/`, `.claude/skills/` | Project |
| Custom agents | `~/.copilot/agents/<name>.agent.md` | Global personal |
| Custom agents | `.github/agents/` or `.claude/agents/` | Project |
| Plugins | `~/.copilot/installed-plugins/` (manage via `copilot plugin`) | Global |
| Custom instructions | `~/.copilot/copilot-instructions.md`, `~/.copilot/instructions/**/*.instructions.md` | Global personal |
| Custom instructions | `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Project |
| Path-specific instructions | `.github/instructions/**/*.instructions.md` | Project (`applyTo` glob) |
| Model allowlist | `.github/allowed_models.txt` | Project |

**Config directory override**: set `COPILOT_HOME` to replace `~/.copilot` entirely
(`--config-dir` is deprecated). User preferences belong in `settings.json`; user-setting keys left
in `config.json` are ignored, and `config.json` keeps only internal state such as trusted folders.

## Workflow

1. **Identify the task** → use the task-to-reference map below to load only what you need
2. **Read the target file first** before making any changes
3. **Edit safely** → use the Edit tool for targeted changes; validate JSON after editing
4. **Confirm** → show the user exactly what changed

## Task → Reference map (load only what's needed)

| Task | Reference file |
|------|----------------|
| `settings.json` keys (user, repo, local), config directory layout | `references/config-schema.md` |
| Trusted folders, `config.json` | `references/config-schema.md` §config.json |
| Environment variables | `references/config-schema.md` §Environment variables |
| OpenTelemetry export, managed `telemetry` | `references/config-schema.md` §OpenTelemetry monitoring |
| Authentication, tokens | `references/config-schema.md` §Auth |
| BYOK models / custom providers, model selection | `references/config-schema.md` §BYOK, §Model usage |
| Tool/path/URL permissions, `permissions-config.json`, sandbox, plan-mode and shell safety checks | `references/permissions.md` |
| CLI flags, slash commands, supported model IDs, sessions (`--name`, `--resume`), debug logs | `references/cli-commands.md` |
| MCP servers, LSP servers | `references/mcp.md` |
| Hooks, including agent-scoped hooks in custom agent frontmatter | `references/hooks.md` |
| Skills | `references/skills.md` |
| Custom agents, subagents, plugins, marketplaces | `references/agents-plugins.md` |
| Custom instructions | `references/instructions.md` |

## Common quick operations (no reference needed)

```bash
# Trust a folder permanently: add its path to "trustedFolders" in ~/.copilot/config.json

# Change a setting (inside a session)
/settings                     # editor; /settings KEY VALUE sets inline
/settings show model

# Read or change a setting from the terminal (user file by default; --repo / --local available)
copilot config theme
copilot config footer.showQuota off
copilot config --list

# Check auth
/user show                    # inside a session; copilot login to sign in

# MCP servers
copilot mcp list              # terminal; /mcp list inside a session

# Skills
copilot skill list            # terminal; /skills list inside a session

# Model
/model                        # inside a session; or copilot --model=auto

# Permissions for this session
copilot --allow-tool='shell(git:*)' --deny-tool='shell(git push)'
/allow-all                    # alias for /permissions allow-all

# Sandbox shell commands (macOS, Linux, Windows)
copilot --sandbox             # this session only; /sandbox enable saves the setting

# Offline mode (BYOK only, no GitHub contact)
export COPILOT_OFFLINE=true

# Name and resume sessions
copilot --name my-feature-work
copilot --resume=my-feature-work
/session delete [ID]          # or /session delete-all

# Prevent system sleep during long sessions
/keep-alive on                # on | off | busy | DURATION

# Remote control
/remote on
/remote off

# What's loaded right now (instructions, MCP, skills, agents, hooks, plugins)
/env
```

## Scripts

- `scripts/show-config.py` — display all config files with annotations
- `scripts/update-references.py` — fetch latest upstream docs

Run with: `python scripts/<script>.py`

## Self-update procedure

When the user asks to **update**, **refresh**, or **sync** this skill:

1. Run `python scripts/update-references.py --all` → fetches each configured reference source to `_fetched/`
2. If the script exits nonzero, resolve the reported failures and rerun it; do not use a partial `_fetched/` set as source material
3. Read each `_fetched/` file alongside its corresponding `references/` file
4. Update `references/` files to reflect documentation changes
5. Delete `_fetched/` and report what changed

Source URLs are in `sources.json`.

## Safety rules

- Always read the file before editing
- Never remove `trustedFolders` entries without confirming with the user
- Hooks and skills live in project directories — confirm scope (global vs project) before creating
- Don't edit `permissions-config.json` while a Copilot CLI session is running
- JSON files: validate well-formed after any edit (`settings.json` also accepts JSONC comments)
- Hook, instruction, and custom-agent changes apply only after restarting (or resuming) the CLI; skills, MCP, and LSP can use `/skills reload`, `/mcp reload`, `/lsp reload`
- Markdown files: preserve frontmatter structure

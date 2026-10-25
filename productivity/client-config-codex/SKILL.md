---
name: client-config-codex
description: 'Manage OpenAI Codex CLI configuration files including config.toml, project .codex/config.toml, profiles, model providers, sandbox and approval settings, permission profiles, rules files, MCP servers, hooks, skills, plugins, custom agents, AGENTS.md instructions, and requirements.toml. Use this skill whenever the user wants to view, edit, add, or understand any Codex setting: trusted projects, approval policy, sandbox mode, network access, allow-listing commands, MCP servers, hooks, skills, plugins and marketplaces, model or reasoning effort, custom model providers, authentication, sessions, or AGENTS.md. Trigger on: "configure codex", "codex config.toml", "trust this project in codex", "codex approval policy", "codex sandbox", "add MCP server to codex", "codex hook", "codex rules", "codex profile", "codex plugin", "set codex model", "codex AGENTS.md", or "show my codex config".'
---

# OpenAI Codex Configuration Manager

You help the user manage all OpenAI Codex CLI configuration files.

> [!IMPORTANT]
> Codex changes quickly and much of what you remember about it is out of date. Answer
> from the reference files in this skill, not from memory. Where a reference and the
> installed CLI disagree, trust `codex --help` and `codex features list`, and tell the user.

References were last verified against **Codex CLI 0.163.0** (released 2026-10-15).

## Config file map

`CODEX_HOME` defaults to `~/.codex`. Setting the `CODEX_HOME` environment variable moves
every path below that starts with `~/.codex`.

| What | File | Scope |
|------|------|-------|
| User config (model, sandbox, approvals, MCP, plugins, hooks, features, providers, project trust) | `~/.codex/config.toml` | Global |
| Profile files (overlay on user config, selected with `--profile`/`-p`) | `~/.codex/<name>.config.toml` | Global |
| Project config (project-allowed keys only, see `references/config-schema.md` §Precedence; applied only when the project is trusted) | `<repo>/.codex/config.toml` | Project |
| System config | `/etc/codex/config.toml` (Unix), `%ProgramData%\OpenAI\Codex\config.toml` (Windows) | Machine |
| Admin-enforced requirements | `/etc/codex/requirements.toml` (Unix), `%ProgramData%\OpenAI\Codex\requirements.toml` (Windows) | Machine, users cannot override |
| Credentials | `~/.codex/auth.json` or the OS keyring | Global, **never read or print** |
| Hooks | `~/.codex/hooks.json`, `<repo>/.codex/hooks.json`, or `[hooks]` in `config.toml` | Global / Project |
| Rules (command allow/prompt/forbid) | `~/.codex/rules/*.rules`, `<repo>/.codex/rules/*.rules` | Global / Project |
| MCP servers | `[mcp_servers.<name>]` in `config.toml` (manage with `codex mcp`) | Global / Project |
| Skills | `<repo>/.agents/skills/`, `~/.agents/skills/`, `/etc/codex/skills/` | Project / Global / Machine |
| Custom agents | `~/.codex/agents/*.toml`, `<repo>/.codex/agents/*.toml` | Global / Project |
| Plugins and marketplaces | `[plugins."<name>@<marketplace>"]`, `[marketplaces.<name>]` in `config.toml` (manage with `codex plugin`) | Global |
| Global instructions | `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md` | Global |
| Project instructions | `AGENTS.md`, `AGENTS.override.md` from repo root down to the working directory | Project |

Codex config is **TOML**, not JSON. JSON appears only in `hooks.json`, plugin files (`.codex-plugin/plugin.json`, a plugin's `.mcp.json`, `.agents/plugins/marketplace.json`), and `auth.json`, which is credential state that you never inspect or edit.

## Workflow

1. **Identify the task** → use the task-to-reference map below to load only what you need
2. **Read the target file first** before making any changes
3. **Edit safely** → use the Edit tool for targeted changes; check that the TOML still parses after editing
4. **Confirm** → show the user exactly what changed, and say whether a Codex restart is needed

## Task → Reference map (load only what's needed)

| Task | Reference file |
|------|----------------|
| `config.toml` keys, layers and precedence, profiles, config directory layout | `references/config-schema.md` |
| Trusted projects (`[projects."<path>"]`) | `references/config-schema.md` §Projects and trust |
| Model, reasoning effort, custom providers, Azure, Bedrock, local/OSS models | `references/config-schema.md` §Model providers |
| Feature flags (`[features]`) | `references/config-schema.md` §Features |
| Environment variables, authentication, `codex login` | `references/config-schema.md` §Environment variables, §Auth |
| Managed configuration, `requirements.toml` | `references/config-schema.md` §Managed configuration |
| Browser Use, Computer Use, in-app browser, and desktop-app network requirements | `references/config-schema.md` §Browser Use and Computer Use requirements |
| Memories (`[memories]`) | `references/config-schema.md` §Memories |
| App (connector) defaults and per-app tool policy (`[apps]`) | `references/config-schema.md` §Apps |
| Sandbox mode, approval policy, network access, permission profiles, rules files, auto-review | `references/permissions.md` |
| CLI subcommands and flags, `-c` overrides, sessions (`resume`, `fork`), slash commands | `references/cli-commands.md` |
| MCP servers | `references/mcp.md` |
| Hooks | `references/hooks.md` |
| Skills | `references/skills.md` |
| Plugins, marketplaces, `[agents]` table, subagent overview | `references/agents-plugins.md` |
| Writing a custom agent TOML file | the `agent-creator-codex` skill |
| `AGENTS.md`, `AGENTS.override.md`, instruction discovery | `references/instructions.md` |

## Common quick operations (no reference needed)

```bash
# Override one setting for a single run (value is parsed as TOML)
codex -c model="gpt-6.1-sol" -c model_reasoning_effort="high"

# What features exist and their state
codex features list

# Diagnose install, config, auth, and runtime health
codex doctor

# MCP servers
codex mcp list

# Plugins
codex plugin --help

# Resume or fork a session
codex resume --last
codex fork --last

# Run with an explicit sandbox and approval policy for this run
codex --sandbox read-only --ask-for-approval on-request

# Sandbox a command the way Codex would
codex sandbox --help
```

Trust a project: add a table to `~/.codex/config.toml`.

```toml
[projects."/absolute/path/to/repo"]
trust_level = "trusted"
```

Project-level `.codex/` config, hooks, rules, and agents load **only for trusted projects**.
A project-scope file that appears to do nothing is usually an untrusted project.

## Scripts

- `scripts/show-config.py` — display all config files with annotations (secrets redacted)
- `scripts/update-references.py` — fetch latest upstream docs

Run with: `python scripts/<script>.py` (`show-config.py` needs Python 3.11+).

## Self-update procedure

When the user asks to **update**, **refresh**, or **sync** this skill:

1. Run `python scripts/update-references.py --all` → fetches each configured reference source into a staging directory (`.agent-output/client-config-codex/_fetched/` at the repo root when the skill is in a git checkout, otherwise `_fetched/` in the skill folder; the script prints the path)
2. If the script exits nonzero, resolve the reported failures and rerun it; the script discards what that run staged, so never use a partial set as source material
3. Read each staged file alongside its corresponding `references/` file, and read the staged `llms-index.md` for new upstream pages that `sources.json` does not cover yet
4. Check every command, flag, and feature you are about to write against the installed CLI (`codex --help`, `codex <subcommand> --help`, `codex features list`)
5. Update `references/` files to reflect documentation changes
6. Delete the staging directory and report what changed

Source URLs are in `sources.json`.

## Safety rules

- Always read the file before editing
- **Never read, print, or edit `auth.json`**, and never put a credential literal in `config.toml`, `hooks.json`, or a rules file — reference an environment variable instead
- Never mark a project `trusted` without confirming with the user; trust lets that repository's config, hooks, and rules run
- Never set `sandbox_mode = "danger-full-access"` or `approval_policy = "never"` (or their CLI equivalents) without explicit user confirmation, and say what it removes
- Hooks run arbitrary commands: show the user the exact command before adding one, and confirm scope (global vs project)
- `requirements.toml` and `/etc/codex/` are admin-owned; do not edit them, and explain that they override user config
- Confirm scope (global vs project) before creating hooks, rules, skills, or agents
- TOML: keep top-level keys **above** the first `[table]` header, or the key lands inside that table
- Config, hook, rule, and agent changes apply to **new** sessions; tell the user to restart Codex
- Markdown files (`SKILL.md`, `AGENTS.md`): preserve frontmatter structure

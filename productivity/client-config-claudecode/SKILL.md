---
name: client-config-claudecode
description: 'Manage and maintain Claude Code configuration files and settings. Use this skill whenever the user wants to view, edit, add, remove, or understand any Claude Code settings — permissions, hooks, MCP servers, environment variables, model settings, sandbox, auto mode, or any other configuration field. Trigger on: "add permission", "allow tool", "deny tool", "configure hook", "add MCP server", "change model", "update settings", "show my settings", "what settings do I have", or "set default mode".'
---

# Claude Code Configuration Manager

You help the user manage `~/.claude/settings.json` — their user-level Claude Code configuration that applies across all projects.

## Settings file locations (scope precedence: highest → lowest)

| Scope | File | Shared? |
|-------|------|---------|
| Managed (macOS) | `/Library/Application Support/ClaudeCode/managed-settings.json` (+ `managed-settings.d/*.json`) | IT-deployed |
| Managed (Linux/WSL) | `/etc/claude-code/managed-settings.json` (+ `managed-settings.d/*.json`) | IT-deployed |
| Managed (Windows) | `C:\Program Files\ClaudeCode\managed-settings.json` (+ `managed-settings.d\*.json`) | IT-deployed |
| Managed (other) | MDM profile / `HKLM` registry, or server-managed settings from the claude.ai console | IT-deployed |
| Command line | `--settings <file-or-json>`, `--model`, `--permission-mode`, … | One session |
| Local project | `.claude/settings.local.json` (at the git repo root) | No (gitignored) |
| Project | `.claude/settings.json` | Yes (git) |
| **User** | **`~/.claude/settings.json`** (or `$CLAUDE_CONFIG_DIR/settings.json`) | No |

Array settings such as `permissions.allow` merge across files; scalars take the highest-precedence value. Some keys are *user or managed* only (ignored in project/local files) — e.g. `autoMode`, `modelPicker`, `vimInsertModeRemaps`; `permissions.defaultMode` values `auto` and `bypassPermissions` are also ignored in project/local files. See `references/settings-schema.md` §Settings files and precedence.

**This skill focuses on the User scope**: `~/.claude/settings.json`

## Workflow

1. **Read current settings first** — always read `~/.claude/settings.json` before making changes
2. **Identify the task** — use the task-to-reference map below to load only what you need
3. **Edit safely** — use the Edit tool for targeted changes; validate JSON after editing
4. **Confirm** — show the user the diff of what changed

## Task → Reference map (load only what's needed)

| Task | Reference file to read |
|------|------------------------|
| Add/remove allow, deny, ask rules | `references/permissions.md` |
| Configure hooks (PreToolUse, PostToolUse, PreModelSwitch, etc.) | `references/hooks.md` |
| Add/configure MCP servers | `references/mcp.md` |
| Model, effort (`effortLevel`/`modelSettings`/`maxEffortLevel`), thinking, output style, prompt cache | `references/settings-schema.md` §Model |
| Sandbox filesystem/network isolation | `references/settings-schema.md` §Sandbox |
| Auto mode classifier | `references/settings-schema.md` §AutoMode |
| Status line, theme, time format, UI toggles | `references/settings-schema.md` §UI |
| Memory, compaction, workflows, update channel | `references/settings-schema.md` §Memory |
| Plugins & skills (enable/disable, marketplaces, sync) | `references/settings-schema.md` §Plugins |
| Subagent files, cross-session messaging | `references/settings-schema.md` §Subagents |
| Environment variables, auth helpers, notifications | `references/settings-schema.md` §Environment |
| Attribution, worktrees, enterprise/managed keys | `references/settings-schema.md` §Attribution / §Worktree / §Misc |
| Deprecated or removed keys | `references/settings-schema.md` §Deprecated |
| Unknown / full schema lookup | `references/settings-schema.md` |

## Common quick edits (no reference needed)

```jsonc
// Auto-updates channel
{ "autoUpdatesChannel": "stable" }          // or "latest" (default)

// Default permission mode
{ "permissions": { "defaultMode": "acceptEdits" } }
// valid: "default" (alias "manual") | "acceptEdits" | "plan" | "auto" | "dontAsk" | "bypassPermissions"
// "auto" and "bypassPermissions" only take effect from user/managed/--settings, not project/local
// Unset: terminal and VS Code sessions start in "auto" from v2.1.283 (details: references/permissions.md)

// Response language
{ "language": "spanish" }

// Effort level — default for models with no saved level
{ "effortLevel": "high" }  // "low" | "medium" | "high" | "xhigh"
// /effort (v2.1.251+) saves per model instead; Opus 5.5+ ignore effortLevel in user settings:
{ "modelSettings": { "claude-sonnet-4-6": { "effortLevel": "high" } } }

// Show thinking summaries
{ "showThinkingSummaries": true }

// Voice dictation (voiceEnabled is deprecated); autoSubmit applies in "hold" mode only
{ "voice": { "enabled": true, "mode": "hold", "autoSubmit": true } }

// Disable all hooks (emergency)
{ "disableAllHooks": true }

// Make a policy hook fail closed: a hook that can't start, times out, or exits with a
// code other than 0 or 2 blocks the action (v2.1.295+; command and http hooks only)
{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/check.js"], "onFailure": "block" }
```

## Scripts

For complex operations, use the helper scripts in `scripts/`:

- `scripts/show-settings.py [--json] [--settings PATH]` — pretty-print current settings across scopes (read-only)
- `scripts/validate-settings.py [path]` — validate JSON structure, flag bad values, unknown/deprecated keys, and user-or-managed keys and `env` variables Claude Code ignores placed in project files (read-only)
- `scripts/update-references.py` — fetch latest upstream docs (used during self-update)

Run with: `python scripts/<script>.py` from the skill directory, or with absolute paths.

## Self-update procedure

When the user asks you to **update**, **refresh**, or **sync** this skill with the latest Claude Code documentation, follow these steps:

1. **Fetch** — run `python scripts/update-references.py --all` (requires network access). This fetches each configured reference URL (plus its `additional_urls`) in `assets/sources.json` and saves raw content to `_fetched/`. Also scan `https://code.claude.com/docs/llms.txt` for new pages that belong in `sources.json`.

2. **Confirm success** — if the script exits nonzero, resolve the reported failures and rerun it. Do not use a partial `_fetched/` set as source material.

3. **Diff** — for each file in `_fetched/`, read it alongside the corresponding file in `references/`. Identify: new fields, removed fields, changed valid values, new examples, behavioral changes.

4. **Update** — rewrite each `references/*.md` file to reflect what changed. Preserve the existing structure and token-efficient style; add/remove/correct only what differs from the source.

5. **Sync scripts** — update the known keys, enums, hook events, and deprecated-key lists in `scripts/validate-settings.py` (and field notes in `scripts/show-settings.py`) to match, then run `python scripts/validate-settings.py <sample-file>` against a scratch sample, not the user's live settings.

6. **Clean up** — delete the `_fetched/` directory.

7. **Record the version** — note the Claude Code release the refresh was checked against (`claude --version`, or `npm view @anthropic-ai/claude-code version`) in `README.md` and `CHANGELOG.md`, and label any claim that only a changelog entry supports, not the docs.

8. **Report** — tell the user what changed (new keys added, deprecated fields, etc.).

### Source URLs (for manual lookup)

See `assets/sources.json` for the full manifest. Key URLs:

| Reference file | Source URL |
|----------------|-----------|
| `references/settings-schema.md` | `https://code.claude.com/docs/en/settings-reference.md` (+ `settings.md`, `managed-settings.md`, `sub-agents.md`) |
| `references/permissions.md` | `https://code.claude.com/docs/en/permissions.md` (+ `permission-modes.md`, `skills.md`) |
| `references/hooks.md` | `https://code.claude.com/docs/en/hooks.md` |
| `references/mcp.md` | `https://code.claude.com/docs/en/mcp.md` (+ `managed-mcp.md`) |
| Doc index | `https://code.claude.com/docs/llms.txt` |

## Safety rules

- Always read the file before editing
- Never remove fields you don't recognize without asking
- Keep a mental diff — tell the user exactly what changed
- If the file doesn't exist yet, create it with `{ "$schema": "https://json.schemastore.org/claude-code-settings.json" }` as the base
- Validate JSON is well-formed after any edit

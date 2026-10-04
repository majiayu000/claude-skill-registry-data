---
name: warp-ai-setup
description: Configure Warp terminal to share Claude Code's MCP servers and AI rules via File-based MCP + AGENTS.md. One-time UI toggles plus file sync. Use when onboarding Warp or after a Warp update resets settings.
---

# Warp AI Setup

Warp supports MCP servers and AI rules but has no file-based global config — it mixes UI settings with file detection. This skill documents the exact toggles and files so our Claude tooling propagates to Warp AI.

## One-time UI toggles

1. **Settings → AI → MCP Servers → "File-based MCP Servers"** — enable
   - Effect: Warp reads `~/.claude.json` (Claude Code format) and any project-root `.mcp.json`
2. **Settings → AI → Agents** — verify default agent is set (otherwise `/agent` commands fail)
3. **Warp Drive → Personal → Rules → Global** — optional: paste core identity rules (UI-only; no file mirror). Keep short; detailed rules live in project `AGENTS.md`.

## File-based rules (per-project)

Warp auto-detects any of these at project root:
- `AGENTS.md` (Warp-preferred)
- `WARP.md` (legacy)
- Symlinks to `CLAUDE.md`, `.cursorrules`, `.clinerules`, `.github/copilot-instructions.md`

Fast setup in a repo:
```bash
ln -s CLAUDE.md AGENTS.md   # if you have a Claude-native file
# or
cp ~/.claude/CLAUDE.md ./AGENTS.md
```

## MCP servers

After enabling the toggle above, Warp reads `~/.claude.json` which the `sync-ai-tools` skill keeps up to date. To add a new server:
1. Add to `~/.cursor/mcp.json` (source of truth)
2. Run `bash ~/.claude/skills/sync-ai-tools/sync.sh`
3. Restart Warp (or it may auto-reload)

## What Warp does NOT support

- No file-based skill system (Warp has no equivalent to Claude's `~/.claude/skills/`)
- No file-based global rules (must use UI)
- No `PreToolUse`/`PostToolUse` hooks

## Fallbacks

- For "skill-like" extension, use **MCP servers** (agents call MCP tools).
- For "rules-like" persistence, use **project AGENTS.md** (commit to repo) or **Warp Drive Rules** (personal).
- For workflows, continue using `~/.warp/workflows/*.yaml`.

## Verify

```bash
# Check Warp can read Claude's MCP set
jq '.mcpServers | keys' ~/.claude.json
```

Should list: fetch, filesystem, playwright, context7, memory, github, sequential-thinking.

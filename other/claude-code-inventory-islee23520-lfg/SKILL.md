---
name: claude-code-inventory
description: >
  Read Claude Code plugins, skills, project auto-memory, and the durable
  Grok↔Claude message bridge. Use when the user asks what Claude plugins/skills
  are installed, to inspect Claude MEMORY.md / project memory, or to send/read
  messages between Grok/lfg and Claude Code (mailbox or live `claude -p` ask).
  Triggers: claude plugins, claude skills, claude memory, Claude Code inventory,
  read claude skill, marketplace plugins, message claude, talk to claude,
  claude bridge, lfg claude ask.
---

# Claude Code Inventory

Inspect **Claude Code** plugins and skills on disk. Prefer the lfg CLI over ad-hoc `find`/`cat` so secrets in `settings.json` env are never printed.

## Commands

```bash
# Summary: skills + plugins + marketplaces
node dist/lfg.js --json claude inventory
# or after global install:
lfg --json claude inventory
lfg claude inventory

# Skills / plugins
lfg --json claude skills
lfg claude skill <name> --body
lfg --json claude plugins

# Project auto-memory (~/.claude/projects/*/memory)
lfg --json claude memory list
lfg claude memory read <name>

# Bridge Grok ↔ Claude (durable mailbox)
lfg claude message send "Hello from Grok — please review X"
lfg claude message list --box to-claude --pending
lfg claude message send --to lfg "Reply from Claude side"
lfg claude ask "One-shot question"              # spawns claude -p if installed
lfg claude ask "Note only" --bridge-only        # mailbox only, no CLI
lfg claude status
```

Flags:

| Flag | Meaning |
|------|---------|
| `--with-marketplace-skills` | Also scan `skills/` inside marketplace plugin trees (can be large) |
| `--no-marketplace` | Skip marketplace plugin scan |
| `--no-agents-skills` | Skip `~/.agents/skills` |

Env overrides:

| Env | Meaning |
|-----|---------|
| `CLAUDE_HOME` / `CLAUDE_CONFIG_DIR` | Claude config root (default `~/.claude`) |

## Stores scanned

| Source | Path |
|--------|------|
| User skills | `~/.claude/skills/*/SKILL.md` |
| Project skills | `<cwd>/.claude/skills/*/SKILL.md` |
| Shared agent skills | `~/.agents/skills/*/SKILL.md` |
| Installed registry | `~/.claude/plugins/installed_plugins.json` |
| Marketplaces | `~/.claude/plugins/known_marketplaces.json` → install trees |
| Plugin manifests | `*/.claude-plugin/plugin.json` or `plugin.json` |
| Settings (metadata only) | `~/.claude/settings.json` — **env values never emitted** |
| Project memory | `~/.claude/projects/<encoded-cwd>/memory/*.md` (+ `MEMORY.md` index) |
| Bridge mailbox | `~/.claude/lfg-bridge/messages/*.json` |

## Workflow

1. Prefer `lfg --json claude status` for a one-shot overview.
2. Skills/plugins: `lfg claude skill|plugin <name>`.
3. Memory: `lfg claude memory list` then `memory read <name>`.
4. Cross-agent chat: write with `message send`, poll with `message list --pending`, optional live `ask`.
5. Bridge protocol details: `references/bridge.md`.
6. Do **not** print API keys/tokens from Claude settings — inventory redacts env values.

## Related

- Session transcripts: `coding-agent-sessions` + `references/claude.md`.
- Bridge protocol: `references/bridge.md`.

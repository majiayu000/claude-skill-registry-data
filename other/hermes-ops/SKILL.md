---
name: hermes-ops
description: "Hermes instance ops: gateway, Discord, profiles, pets."
version: 1.0.0
author: Vesper (curator umbrella)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, ops, gateway, troubleshooting, profiles, identity, petdex, mascots]
    category: devops
    related_skills: [hermes-agent, self-management, session-recall]
---

# Hermes Instance Ops — this install's operational playbooks

Upstream Hermes *framework* knowledge lives in the bundled `hermes-agent` skill
(CLI, config keys, contributing). **This** skill is the counterpart for operating
*this* instance: the failures, rebuilds, and subsystem quirks we actually hit
here, kept as verbatim case files so the next session doesn't re-derive them.

**Trigger:** the bot's messaging misbehaves, a gateway fights itself, a profile
needs to be stood up as a new being, or a Hermes display extra (mascots) needs
fixing.

## Playbooks

### 1. Gateway / messaging troubleshooting → `references/gateway-troubleshooting.md`

Use when messaging is wrong in ways `/new` does NOT fix: DM system-message spam
(tool bubbles, credit notices, memory notices, empty posts), "I can see your
thinking", typing ghosts, gateway churn ("Another gateway instance is already
running", "Gateway (re)started N times in 120s"), or lock fights.

Core principle to state first: `/new` resets the **session**, not **config** or
**processes** — persistent weirdness is `display.*` or a duplicated gateway
process. Heredocs of the fix commands are in the reference.

Case files (verbatim session forensics):
`references/2026-08-20-dm-noise-and-gateway-war.md`,
`references/restart-war-20260820.md`,
`references/2026-09-01-lumi-ghost-forensics.md`,
`references/2026-09-03-lumi-unfreeze-fix.md`,
`references/context-compression-diagnostics.md`,
`references/multi-profile-operations.md`.
Scripts: `scripts/gateway-forensics.sh`, `scripts/gw-lumi-vesper-fix.sh`,
`scripts/discord_create_channel.py`.

### 2. Profile identity bootstrap → `references/profile-identity-bootstrap.md`

Standing up a NEW Hermes profile as a *distinct being* (not a clone of an
existing one), and adopting another AI's openly-shared lorebook frameworks with
correct attribution. Covers the inherited-memory audit, depersonalizing an
adopted framework, SOUL/MEMORY/USER voice-carry, and the lorebook loading
mechanism.

Triggers: "make a new profile for <name>", "give Vesper their own identity",
"adopt <X>'s frameworks", "clone these files but make them mine".

Support files: `references/declone-workflow.md`,
`references/depersonalize-open-framework.md`,
`references/framework-adaptation.md`,
`references/lorebook-audit-adapt-existing.md`,
`references/lorebook-loading-mechanism.md`,
`references/lorebook-refresh-workflow.md`,
`references/shapes-login-flow.md`,
`templates/ingest-lorebooks-openrouter.py`.

### 3. Petdex mascots → `references/petdex-mascots.md`

Install / select / scale / customize the animated pet spritesheets, and debug
rendering across CLI, TUI, desktop app, and SSH sessions (graphics-capable
terminal requirements, config, filesystem issues). Spritesheet spec:
`references/spritesheet-format.md`.

### 4. Discord server management & moderation → `references/discord-server-management.md`

Using and **extending** Hermes' built-in Discord REST tool (`tools/discord_tool.py`)
for server management and moderation: the 15 existing actions, how core/admin
actions split across the `discord` and `discord_admin` toolsets, the
action-dispatch extension pattern (`_ACTIONS` / `_ACTION_MANIFEST` /
`_REQUIRED_PARAMS` / `_ACTION_403_HINT`), and the RedBot coexistence topology.

Triggers: "moderate Discord", "kick/ban/timeout members", "extend discord
tools", "add moderation actions". Raw endpoint reference:
`references/moderation-api-endpoints.md`; helper script:
`scripts/discord_leave_guild.py`.

## Notes

Absorbed the former standalone skills `hermes-gateway-troubleshooting`,
`profile-identity-bootstrap`, `pet-management`, and `discord-server-management`; their full bodies and support
files live under `references/`, `scripts/`, and `templates/` above.

Sibling umbrellas: `self-management` (my autonomy infra: crons, flags, backups,
host updates), `session-recall` (session DB forensics), `vector-memory-setup`
(Qdrant memory), `local-inference` (local model/voice providers).

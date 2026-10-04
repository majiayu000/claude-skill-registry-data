---
name: hermes-agent_KM
description: >-
  Configure, troubleshoot, update, or extend Hermes Agent itself. Use this before
  answering questions about Hermes CLI commands, profiles, config, models,
  providers, tools, skills, gateways, Telegram/Discord surfaces, plugins, cron,
  memory, updates, or local Mac Studio Hermes operations.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
    - claude-hermes
    - immigration-project
  hermes:
    command_priority: 410
---
# Hermes Agent

Use this as the compact Hermes-specific router. It exists because the upstream Hermes prompt expects a `hermes-agent` skill, while Kosta's live setup also has local Skillshare skills that are more specific and more current for this Mac Studio.

## First move

For current commands, flags, provider settings, plugin behavior, gateway behavior, or config keys, inspect the live machine or current docs before answering. Do not invent Hermes syntax from memory.

Use these local entry points first:

```bash
hermes --help
hermes config --help
hermes tools --help
hermes skills --help
hermes gateway --help
hermes --profile gpt config path
hermes --profile default config path
```

For source-level work, the active repo is:

```text
~/.hermes/hermes-agent
```

For durable local prompt/state work, use:

```text
~/.config/hermes-state
~/.hermes/shared
```

## Route to the sharper skill

After loading this skill, immediately load the more specific Hermes skill if the task matches:

- Updates / Skillshare distribution / local customizations: `hermes-maintenance-and-distribution`
- Gateway, Telegram, Discord, API server, compact HUD, restarts: `hermes-gateway-operations` or `hermes-gateway-local-ops`
- Telegram bot behavior specifically: `hermes__telegram-gateway`
- Profile display/tool-progress settings: `hermes__profile-gateway-display-settings`
- Prompt stack, memory, mem0, SOUL/HERMES/USER files: `hermes-prompt-state-and-memory`
- Provider/media/image/voice configuration: `hermes-provider-media-configuration`
- Smart update workflow: `hermes__update-smart`
- Skillshare syncing/allowlists: `skillshare`
- Skill improvement/evolution: `hermes__hermes-self-evolve-skills` for Hermes-native runs, `agentic__self-evolve-skills` only for explicit Claude Code/Sonnet/Opus lanes, and `hermes__skill-lifecycle-automation` for lifecycle automation

If several apply, pick the one closest to the user's requested action and keep the rest out of context unless needed.

## Mac Studio safety defaults

This Mac Studio runs the active Telegram/Discord gateway and cron host. If the current conversation is arriving through Telegram/Discord/webhook/API gateway, do not restart that same gateway inline unless Kosta explicitly asked and the restart path is detached/safe. From a local Terminal/SSH/tmux session, service restarts are allowed when appropriate.

Never paste fragile `launchctl` snippets with standalone `$(id -u)`. Use copy-paste-safe blocks with `uid=$(id -u)` assigned first, then `user/$uid/...` or `gui/$uid/...` after discovering the actual domain.

Use 1Password service-account access for secrets when available; do not ask Kosta for credentials before checking the `CLI` vault.

## Gateway pitfall: BlueBubbles mixed media/text

If Kosta reports iMessage/BlueBubbles image + text messages splitting or follow-up text getting treated as “added to next tool call,” inspect both inbound batching and outbound send coalescing. Image/photo/attachment webhooks must enter the same stagger window as text webhooks; media should not dispatch immediately while text waits. Reproduce with an image followed quickly by text, then run the BlueBubbles gateway tests before claiming the fix. Source/test anchors: `gateway/platforms/bluebubbles.py`, `gateway/platforms/base.py`, and `tests/gateway/test_bluebubbles.py`.

## Verification

Before claiming a Hermes change is fixed, verify the actual surface affected:

- Config change: read back `hermes --profile <profile> config path` and the relevant config value.
- Skill distribution: run `skillshare sync --json`, verify target files under `~/.hermes/skills` and `~/.hermes/profiles/gpt/skills`, then load the skill with `skill_view`.
- Gateway/menu behavior: verify slash-command registration or `telegram_menu_commands()` from the live repo; restart/refresh only through a safe path.
- Code change: run the smallest relevant test or import/compile check, then inspect git diff.

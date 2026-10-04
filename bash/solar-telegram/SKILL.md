---
name: solar-telegram
description: >
  Operate Telegram transport for the Solar runtime: the bridge, the outbound
  alert path and their setup. Not published to any IDE — the agent-facing verb
  is the gated MCP tool `solar_telegram_send`, and this skill is what the
  runtime and the operator use behind it.
sync: false
---

# Solar Telegram

## Purpose

Provide one reusable skill for Telegram transport in Solar:
- inbound/outbound conversation bridge (Telegram -> local -> Telegram),
- direct outbound alerts (local -> Telegram),
- setup and validation of the visible configuration.

## Not synced to clients (required)

`sync: false` keeps this skill out of every client catalog — Codex, Claude,
Cursor and Gemini read one index, and it is not in it. The reason is not
tidiness: an agent that can read these scripts and a token in the same tree can
send without passing any gate. The verb moved to `solar_telegram_send` in
`solar-mcp`, which uses native client confirmation when supported, or a trusted operator
approval. The runtime manages the identifier, bound to workspace and exact
arguments, expiring and reserved before execution. See
`core/skills/solar-mcp/references/approvals.md` for the trust boundary.

Do not re-add it to the sync. If a client still shows it, its copy under
`.cursor/skills/` (or the symlink under `.claude/`, `.codex/`, `.gemini/`) is
stale: `solar client sync` removes it.

## Scope

- Keep transport logic reusable in `core/`.
- The bot token is an **installation secret**: it lives in the process store
  (`<app data>/Solar/secrets/installation.env`, 0600) and never in `.env`, which
  the IDE indexes. `send_telegram.sh` takes it from the environment and will not
  open the store itself; the runtime that calls it does.
- Visible configuration (chat id, parse mode, preview) stays in root `.env`.
- Keep deterministic operations inside this skill `scripts/`.

## Required MCP

None

## Validation commands

```bash
# Where the token must live (prints the path; never a value)
python3 core/skills/solar-paths/scripts/solar_secrets.py status

# Full setup runbook (recommended)
bash core/skills/solar-telegram/scripts/setup_telegram.sh --ping --test-message "Solar Telegram OK"

# Non-interactive setup check
bash core/skills/solar-telegram/scripts/setup_telegram.sh --non-interactive

# Sync core changes to local clients
solar client sync
```

## Required environment variables

- `TELEGRAM_BOT_TOKEN` — installation secret, process store only. Never `.env`.
- `TELEGRAM_CHAT_ID` (default target chat for alerts) — root `.env`.

Optional:
- `TELEGRAM_PARSE_MODE` (default: `Markdown`). `none` omits `parse_mode` and sends plain text: use it for text Solar does not control (task titles, paths), where a stray `_` or `*` makes Telegram reject the message with HTTP 400. Task notifications always send plain text.
- `TELEGRAM_DISABLE_PREVIEW` (default: `true`)

## Laptop runtime note (optional, bridge mode)

- `alerts` mode does not require a long-running local endpoint.
- `bridge` mode may depend on long-running local runtime services.
- If bridge runtime is hosted on a laptop, host sleep can interrupt message flow.
- This is a host operations concern, not a mandatory dependency of this skill.

## Environment block format (required)

- Write the *visible* Telegram variables in one compact skill-scoped block in
  root `.env`. The token is not one of them and must not appear there.
- Start block with header comment: `# [solar-telegram] required environment`.
- Keep block contiguous with no blank lines inside.
- Preserve existing values unless explicit overwrite is requested.

## Workflow

1. Confirm target mode: `bridge` or `alerts`.
2. Execute `setup_telegram.sh` as the default procedure from the agent (do not ask the user to run shell commands).
3. If the chat id is missing, ask for it and run setup with `--chat-id`. If the
   token is missing, say where it goes and let Louis write it: setup refuses
   `--token`, because a secret passed through argv lands in shell history and a
   secret written to `.env` lands in the IDE's index.
4. For bridge mode, use `references/telegram-transport-patterns.md` as the routing contract.
5. If skill files changed, run `solar client sync`.

## Output format

- Selected mode (`bridge` or `alerts`)
- Required environment keys
- Commands executed
- Result and next action

## References

- `references/telegram-transport-patterns.md`

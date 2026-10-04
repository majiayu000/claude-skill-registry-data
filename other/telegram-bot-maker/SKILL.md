---
name: telegram-bot-maker
description: Build and operate Telegram bots with BotFather, HTTPS webhooks, n8n workflows, and SCBE connector automation. Use when users ask to create, wire, debug, or harden Telegram bot pipelines.
---

# Telegram Bot Maker

## Overview

Use this skill to move from bot token to working Telegram automation quickly:
- BotFather token + webhook configuration.
- n8n workflow setup for inbound/outbound bot behavior.
- SCBE connector registration and health checks.
- Basic hardening and troubleshooting.

## Trigger Conditions

Use this skill when users ask to:
- Create a Telegram bot.
- Set or fix Telegram webhook URLs.
- Connect Telegram to n8n workflows.
- Add Telegram into SCBE connector matrix, watchdog, or fleet bootstrap.
- Troubleshoot errors like `https is required`, `404`, `chat not found`, `unauthorized`.

## Required Inputs

- `TELEGRAM_BOT_TOKEN` (or `SCBE_TELEGRAM_BOT_TOKEN`)
- Public HTTPS webhook URL
- Optional `TELEGRAM_CHAT_ID` (numeric) for send tests
- n8n endpoint details when routing to n8n
- SCBE base URLs for connector registration (`/mobile/connectors`)

## Workflow

### 1) Validate public endpoint first

Run URL checks before setting webhook:

```powershell
curl.exe -I https://<your-host>/<webhook-path>
```

If endpoint is not reachable, do not proceed with BotFather webhook setup.

### 2) Set/get/delete webhook using bundled script

Use:
- `scripts/telegram_webhook_ops.ps1`

Examples:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/telegram_webhook_ops.ps1 -Action set -WebhookUrl "https://<your-host>/webhook/<path>"
powershell -ExecutionPolicy Bypass -File scripts/telegram_webhook_ops.ps1 -Action get
powershell -ExecutionPolicy Bypass -File scripts/telegram_webhook_ops.ps1 -Action test -ChatId "<numeric_chat_id>" -Message "SCBE test ping"
```

### 3) Build n8n Telegram workflow

Start from `references/n8n_telegram_rag_blueprint.md`:
- Convert generic triggers to Telegram Trigger + Telegram send nodes.
- Keep embeddings/vector operations aligned between insert/retrieve.
- Replace in-memory vector store with persistent storage for production.

### 4) Wire Telegram into SCBE

In `SCBE-AETHERMOORE`:

```powershell
python scripts/connector_health_check.py --checks telegram --telegram-chat-id $env:TELEGRAM_CHAT_ID --output artifacts/connector_health/telegram_health.json
powershell -ExecutionPolicy Bypass -File scripts/system/register_connector_profiles.ps1 -Profile free -BaseUrl http://127.0.0.1:8000 -N8nBaseUrl http://127.0.0.1:5680 -ReplaceExisting
```

### 5) Hardening defaults

- Use numeric Telegram user/chat IDs for allowlists and tests.
- Keep bot token in environment or CI secret store only.
- Require HTTPS endpoints only.
- Prefer group mention gating when deploying to group chats.

## References

- `references/n8n_telegram_rag_blueprint.md`

## Scripts

- `scripts/telegram_webhook_ops.ps1`

## Output Contract

When completing a bot setup, return:
- `webhook_url`
- `webhook_state` (`set`/`missing`/`error`)
- `n8n_workflow_status`
- `scbe_connector_status`
- `next_command`

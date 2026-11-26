---
name: hermes-gateway-messaging
description: Set up Hermes gateway messaging with security lockdown.
version: 0.1.0
author: Charles Ponti, Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, gateway, messaging, telegram, whatsapp, imessage, security]
    related_skills: []
---

# Hermes Gateway Messaging Setup

Connect Hermes to a messaging platform so you can chat with it away from the machine, with the blast radius contained.

## When to Use

- User wants to talk to Hermes from a phone or another device.
- Setting up Telegram, WhatsApp, or iMessage (BlueBubbles) as a gateway surface.
- Locking down a bot so it cannot run arbitrary tools remotely.

Don't use for: local-only chat (CLI/desktop), or a full app uninstall.

## Platform choice

| Platform                 | Number needed            | Privacy                | Setup cost                        |
| ------------------------ | ------------------------ | ---------------------- | --------------------------------- |
| iMessage (BlueBubbles)   | existing Apple ID        | E2E                    | manual install + Apple ID sign-in |
| WhatsApp (linked device) | existing WhatsApp number | E2E-ish (Meta servers) | QR scan                           |
| Telegram (bot)           | none (bot token)         | not E2E for bots       | BotFather + token                 |

Prefer iMessage for privacy; Telegram for simplest setup; WhatsApp when the user already lives in WhatsApp.

## Procedure

1. Pick the platform and complete its pairing:
   - WhatsApp: `hermes whatsapp` (QR scan in your own terminal).
   - Telegram: create a bot via @BotFather, then `hermes gateway setup` and paste the token.
   - iMessage: install BlueBubbles Server, sign in with Apple ID, set `BLUEBUBBLES_SERVER_URL` and `BLUEBUBBLES_PASSWORD` in `<agent-home>/.env` (`<agent-home>` = your agent runtime's home dir), then `hermes gateway setup`.
2. Restrict allowed senders to your own user ID/number/address only.
3. Lock down the toolset: use the `safe` toolset for the gateway surface; keep `approvals.mode: smart` or `manual`.
4. Keep `security.redact_secrets: true` (default).
5. Install + start the gateway:
   ```
   hermes gateway install
   hermes gateway start
   hermes gateway status
   ```
6. Test by messaging the bot from the allowed account; verify it replies and that destructive commands still prompt.

## Pitfalls

- `hermes whatsapp` prints a QR code and needs a real TTY; run it in your own terminal, not through an agent subprocess.
- BlueBubbles' Homebrew cask is disabled by Gatekeeper; download the server from bluebubbles.app and install manually, then sign in with your Apple ID.
- A messaging bot inherits the agent's full tool access (shell, files, web). Restrict the toolset and keep approvals on; never expose `terminal`/`computer_use` remotely unless needed.
- Telegram bot messages are not end-to-end encrypted; treat them as readable by Telegram. Don't send secrets.
- The bot token is a credential; store in `<agent-home>/.env`, rotate via BotFather if leaked.
- WhatsApp requires your phone occasionally online; BlueBubbles requires the Mac running and logged in.
- Gateway settings are read at process start; restart the gateway after config changes.
- Prompt injection over a messaging surface is real; keep toolset minimal and approvals on.

## Verification

- `hermes gateway status` shows running.
- A message from the allowed account gets a reply.
- A destructive command request prompts for approval (or is denied).
- `df`/logs show no unexpected tool execution.

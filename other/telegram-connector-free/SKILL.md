---
name: telegram-connector-free
description: Telegram Connector (Free). Basic Telegram bot actions and webhooks for small projects.
version: 3.0.0
author: AgentBoost Open Source
enterprise: false
category: Communications
---

### System Instructions
You are equipped with the `telegram-connector-free` deterministic tool. This tool enables basic message dispersal and command handling via the Telegram Bot API. It supports simple webhook triggers and automated replies for lightweight operational notifications.

### Execution Protocol
Invoke the Telegram engine by passing strictly formatted JSON:

```json
{
  "chat_id": "@operational_log_channel",
  "message_text": "System Alert: Server Uptime Guardian heartbeat detected.",
  "parse_mode": "Markdown",
  "disable_notification": false
}
```

Outputs
- Message delivery status and Telegram API result.
- Simple webhook trigger identification.
- Basic automated command reply logs.
- Channel notification confirmation.

---
name: slack-notify
description: Send messages to Slack channels via webhook or API
activation_keywords: [slack, message, channel, notify, notification, webhook]
execution_mode: server
---

# Slack Notify Skill

Provides Slack messaging operations:
- Send messages to Slack channels
- Post via incoming webhook
- Format messages with blocks

Use `builtin_slack_notify` tool with fields:
- `operation`: one of "send", "webhook"
- `channel`: Slack channel name or ID
- `message`: Message text (supports Slack markdown)
- `webhook_url`: Incoming webhook URL (for webhook operation)

Note: Requires Slack webhook URL or bot token.

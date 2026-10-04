---
name: alert-sender
description: Send alert notifications via configured channels (lark, dingtalk, wecom)
activation_keywords: [alert, notify, notification, send alert, lark, dingtalk, wecom, webhook]
---

# Alert Sender Skill

Provides alert notification capabilities:
- Send alerts to Lark (Feishu) via webhook
- Send alerts to DingTalk via webhook
- Send alerts to WeCom via webhook
- Format alerts with title, content, and severity level

Use `builtin_alert_sender` tool with fields:
- `channel`: notification channel (lark, dingtalk, wecom)
- `webhook_url`: the webhook URL for the target channel
- `title`: alert title
- `content`: alert content (supports markdown)
- `level`: (optional) severity level: info, warning, critical (default: info)
- `at_users`: (optional) comma-separated user IDs to mention

---
name: slack-lite
description: Slack Lite (Free). Lightweight Slack automation for notifications and quick replies.
version: 3.0.0
author: AgentBoost Open Source
enterprise: false
category: Marketing
---

### System Instructions
You are equipped with the `slack-lite` deterministic tool. This tool handles lightweight Slack workspace interactions, including posting messages to specific channels and processing slash command triggers. It is optimized for operational notifications and high-speed team updates.

### Execution Protocol
Invoke the Slack engine by passing strictly formatted JSON:

```json
{
  "channel_name": "#operations-alerts",
  "text_content": "Operational Pulse: 15 specialized agents confirmed READY.",
  "as_user": false,
  "icon_emoji": ":robot_face:"
}
```

Outputs
- Slack channel delivery verification.
- Slash command handler execution status.
- Webhook trigger identification and logs.
- Lightweight team notification confirmation.

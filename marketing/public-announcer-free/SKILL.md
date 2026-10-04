---
name: public-announcer-free
description: Public Announcer (Free). Post public announcements across channels.
version: 3.0.0
author: AgentBoost Open Source
enterprise: false
category: Marketing
---

### System Instructions
You are equipped with the `public-announcer-free` deterministic tool. This tool enables one-click broadcasting of public statements across configured social and internal channels. It supports scheduled posting and basic engagement tracking for community and market updates.

### Execution Protocol
Invoke the announcer engine by passing strictly formatted JSON:

```json
{
  "announcement_text": "AgentBoost Autonomous Workstation v0.1.0 now live with 50+ agents.",
  "target_channels": ["Global_Community_Feed", "Internal_Announcements"],
  "schedule_timestamp": "2026-10-15T09:00:00Z",
  "track_basic_engagement": true
}
```

Outputs
- One-click broadcast execution and status.
- Scheduled post calendar entries.
- Basic engagement and reach analytics summaries.
- Multi-channel distribution verification logs.

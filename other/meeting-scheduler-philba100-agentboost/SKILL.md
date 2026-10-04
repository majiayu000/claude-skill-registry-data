---
name: meeting-scheduler
description: Calendar sync, proposals, and reminders. Orchestrates multi-timezone calendar alignment for global teams.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Operations & HR
---

### System Instructions
You are equipped with the `meeting-scheduler` deterministic tool. This tool synchronizes events across Google and Outlook calendars, identifies multi-timezone availability windows, and automates multi-stage meeting agendas and reminders.

### Execution Protocol
Invoke the scheduling engine by passing strictly formatted JSON:

```json
{
  "attendees": ["ceo@agentboost.com", "partner@institutional.vc"],
  "duration_mins": 60,
  "timezone": "America/New_York",
  "agenda_topic": "Strategic Q4 Capital Review",
  "auto_reminder_sequence": true
}
```

Outputs
- Multi-timezone availability window identification log.
- Automated meeting invite and agenda distribution status.
- Calendar synchronization and conflict resolution report.
- Reminder and follow-up communication logs.

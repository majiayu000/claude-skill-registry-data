---
name: calendar-sync-free
description: Calendar Sync (Free). Two-way calendar syncing for personal use.
version: 3.0.0
author: AgentBoost Open Source
enterprise: false
category: Operations & HR
---

### System Instructions
You are equipped with the `calendar-sync-free` deterministic tool. This tool performs two-way event synchronization between personal calendar accounts. It identifies basic schedule conflicts and handles timezone adjustments for individual operational planning.

### Execution Protocol
Invoke the sync engine by passing strictly formatted JSON:

```json
{
  "source_calendar": "personal_gmail",
  "target_calendar": "work_outlook",
  "sync_window_days": 14,
  "handle_timezones": true,
  "detect_conflicts": true
}
```

Outputs
- Two-way event synchronization audit log.
- Basic conflict detection and warning identification.
- Timezone adjustment verification results.
- Personal schedule alignment confirmation.

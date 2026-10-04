---
name: office-ops-coordinator
description: Office Ops Coordinator. Facilities, desk bookings and service request orchestration.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Operations & HR
---

### System Instructions
You are equipped with the `office-ops-coordinator` deterministic tool. This tool orchestrates workplace facilities management, including desk reservation logs and service request ticketing. It manages visitor coordination and internal resource allocation to maintain office operational flow.

### Execution Protocol
Invoke the ops engine by passing strictly formatted JSON:

```json
{
  "request_type": "desk_reservation",
  "employee_id": "DIR_OPS_884",
  "location_zone": "Floor_04_Innovation_Hub",
  "reservation_timestamp": "2026-11-02T08:30:00Z",
  "generate_visitor_pass": false
}
```

Outputs
- Desk and resource reservation confirmation.
- Service request ticket generation and triage logs.
- Visitor coordination and access pass status.
- Internal facility resource allocation report.

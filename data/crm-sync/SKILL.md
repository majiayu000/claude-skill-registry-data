---
name: crm-sync
description: Universal CRM integration hub. Orchestrates seamless data flow between Salesforce, HubSpot, and internal databases.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Operations & HR
---

### System Instructions
You are equipped with the `crm-sync` deterministic tool. This tool manages the synchronization of leads, accounts, and opportunities across multi-vendor CRM systems. It performs automated conflict resolution and maintains comprehensive operational audit logs.

### Execution Protocol
Invoke the CRM engine by passing strictly formatted JSON:

```json
{
  "source_system": "HubSpot",
  "target_system": "Salesforce_Enterprise",
  "sync_direction": "bi_directional",
  "object_type": "opportunity_pipeline",
  "perform_conflict_resolution": true
}
```

Outputs
- Multi-vendor CRM data synchronization status.
- Automated record conflict resolution audit log.
- Lead and account lifecycle consistency report.
- Real-time pipeline state mapping and validation.

---
name: crm-sync
description: Universal CRM integration hub. Syncs leads, meetings, deals, and activities across Salesforce, HubSpot, Pipedrive, and custom systems. Real-time data synchronization with conflict resolution.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

### System Instructions
You are equipped with the `crm-sync` skill for enterprise CRM integration. This tool manages real-time data synchronization across multiple CRM systems with built-in conflict resolution and audit trails.

**CRITICAL:** Never overwrite existing data without verification. Always maintain data integrity. Log all sync operations for compliance.

### Execution Protocol
Call the `run_js` tool with strictly formatted JSON:

```json
{
  "action": "sync_lead",
  "crm_systems": ["salesforce", "hubspot"],
  "lead_data": {
    "email": "john@acme.com",
    "first_name": "John",
    "last_name": "Smith",
    "company_name": "Acme Corp",
    "title": "VP Sales",
    "phone": "+1-555-0100",
    "qualification_score": 85,
    "lead_source": "agent_qualified",
    "deal_stage": "discovery",
    "estimated_value": 150000,
    "next_action": "demo_scheduled"
  },
  "sync_target_fields": ["email", "name", "company", "lead_score", "opportunity_value"],
  "conflict_resolution": "agent_priority",
  "create_if_missing": true,
  "update_if_exists": true,
  "log_activity": true
}
```

### Outputs
The skill delivers:
- **Sync Status:** Success/failure per CRM
- **Records Updated:** Count per system
- **Conflicts Resolved:** How conflicts were handled
- **Activity Log:** Complete audit trail
- **Error Report:** Any sync failures with reasons
- **Next Sync Scheduled:** When next sync occurs

### Alternative Actions
- `sync_deal`: Update opportunity records
- `sync_meeting`: Log calendar events
- `sync_activity`: Create CRM tasks/activities
- `sync_all`: Full data synchronization
- `create_contact`: New contact with enrollment

### Example Tool Call
```javascript
run_js(data='{"action": "sync_deal", "crm_systems": ["salesforce", "pipedrive"], "deal_data": {"deal_id": "DEAL-2026-0847", "deal_name": "Acme Corp Enterprise", "company_email": "john@acme.com", "deal_value": 185000, "deal_stage": "negotiation", "close_date": "2026-05-15", "probability": 75, "next_milestone": "contract_review", "notes": "Negotiation in progress, awaiting margin approval"}, "sync_target_fields": ["deal_value", "stage", "close_date", "probability"], "conflict_resolution": "agent_priority", "update_if_exists": true, "log_activity": true}')
```

### Supported CRM Systems
- **Salesforce**: Full API integration
- **HubSpot**: Native connector
- **Pipedrive**: REST API
- **Custom Systems**: Webhook integration

### Integration Points
- **Lead Qualifier:** Sync scores and recommendations
- **Meeting Scheduler:** Log meeting records
- **Negotiation Engine:** Track deal progress
- **Bidding Engine:** Store quote history
- **Email Orchestrator:** Log campaign sends
- **Analytics Hub:** Sync conversion data

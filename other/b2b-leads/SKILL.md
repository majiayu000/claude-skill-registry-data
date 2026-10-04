---
name: b2b-leads
description: LeadScraper Pro. Extract verified decision-maker contact data from any company domain.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Sales
---

### System Instructions
You are equipped with the `b2b-leads` deterministic tool. This tool scrapes public corporate registries and professional networks to extract verified decision-maker emails and direct-dial phone numbers. It maintains a 98% email verification rate and supports direct export to Salesforce and HubSpot.

### Execution Protocol
Invoke the lead engine by passing strictly formatted JSON:

```json
{
  "target_domain": "institutional-global.com",
  "target_roles": ["CFO", "Director_of_Procurement", "Legal_Counsel"],
  "verification_level": "strict_98_percent",
  "export_destination": "Salesforce_Enterprise"
}
```

Outputs
- List of verified decision-maker contact records.
- Email verification and deliverability scorecards.
- Direct-dial phone numbers and professional profile links.
- Automated CRM export and synchronization status.

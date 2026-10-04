---
name: b2b-lead-gen
description: Enterprise-grade tool to scrape, enrich, and verify B2B contact data (emails, phone numbers, LinkedIn profiles) for specific domains and roles. Auto-qualifies leads and triggers nurture sequences.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

### System Instructions
You are equipped with the `b2b-lead-gen` tool. To execute this skill, you MUST call the `run_js` tool passing a strictly formatted JSON string into the `data` parameter. 

Do not hallucinate parameters. Only use the keys defined in the schema below.

### JSON Schema Requirement
```json
{
  "type": "object",
  "properties": {
    "company_domain": {
      "type": "string",
      "description": "The root domain of the target company (e.g., 'microsoft.com'). Do not include 'https://' or 'www'."
    },
    "role": {
      "type": "string",
      "description": "The job title or department of the decision maker (e.g., 'Marketing Director', 'CEO', 'IT Procurement')."
    }
  },
  "required": ["company_domain", "role"]
}

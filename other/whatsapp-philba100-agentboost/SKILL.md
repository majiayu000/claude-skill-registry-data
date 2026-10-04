---
name: enterprise-whatsapp-orchestrator
version: "3.1.0"
author: "AgentBoost Enterprise API"
description: "Scalable WhatsApp CRM orchestration with lead qualification triggers, negotiation message sequences, meeting scheduling, and full conversion analytics. Multi-language support and compliance automation."
enterprise: true
---

# Execution Protocol
To execute this skill, you MUST invoke the `run_js` tool adhering exactly to the JSON schema below. 

## Strict Payload Schema
- `data`: A stringified JSON object containing:
  - `status` (string): Execution status (Default: "success").
  - `campaign_name` (string): Professional, concise internal identifier.
  - `audience` (string): Target segment identifier (e.g., "Tier 1 Accounts", "Churn Risk").
  - `message` (string): The generated copy. MUST utilize line breaks (\n) and professional spacing.
  - `schedule_time` (string): ISO 8601 format or exact natural language (e.g., "2024-11-01T09:00:00Z" or "Tomorrow 09:00").
  - `timezone` (string): Valid IANA Time Zone (e.g., "America/New_York", "Europe/London").

## Contextual Guardrails for the Agent
1. **Dynamic Injection:** Integrate products, discount codes, or user variables natively into the message copy.
2. **Compliance:** Maintain a professional B2B or premium B2C tone. Limit emoji usage to maximum 2 per message to avoid spam flagging.
3. **Timezone Inference:** You must accurately infer the IANA timezone based on the user's location prompt.

## Example Execution
```python
run_js(data='{"status": "success", "campaign_name": "Q4 Enterprise Reactivation", "audience": "Lapsed Enterprise Leads", "message": "Hi {{first_name}},\n\nWe noticed your enterprise trial expired. Use authorization code ENTAUTH20 for a 20% extension on your contract.\n\nReply STOP to opt out.", "schedule_time": "2023-11-15T14:00:00Z", "timezone": "America/New_York"}')
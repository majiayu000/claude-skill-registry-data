---
name: whatsapp
description: WhatsApp CRM Pro. Scalable CRM orchestration and high-conversion automation for enterprise communication.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Marketing
---

### System Instructions
You are equipped with the `whatsapp` deterministic tool. This tool manages scalable WhatsApp Business API orchestration. It utilizes liquid-template personalization for high-conversion outreach and maintains real-time webhook integration for response triage.

### Execution Protocol
Invoke the messaging engine by passing strictly formatted JSON:

```json
{
  "campaign_id": "RE-ENGAGE_Q4",
  "recipient_batch_id": "Lapsed_Enterprise_Clients",
  "template_id": "promo_personalized_institutional",
  "enable_webhook_triage": true,
  "liquid_variables": { "last_interaction": "90_days" }
}
```

Outputs
- High-deliverability messaging routing status.
- Liquid-template personalization and preview log.
- Real-time response webhook triage and priority alert.
- Campaign conversion and engagement analytics report.

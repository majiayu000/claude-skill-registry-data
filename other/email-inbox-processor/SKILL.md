---
name: email-inbox-processor
description: Commercial Communications & RFQ Choreographer. Coordinates high-volume operational inbox streams, executing multi-stage commercial parsing of critical legal or procurement documentation.
version: 3.0.0
author: AgentBoost Quantitative Trading Fleet
enterprise: true
category: Communications
---

### System Instructions
You are equipped with the `email-inbox-processor` autonomous agent. This agent executes heuristic operational urgency triage and priority-based corporate routing. It extracts binding requests for proposal (RFQs), invoices, and notices from inbound email streams to orchestrate executive action.

### Execution Protocol
Invoke the communications engine by passing strictly formatted JSON:

```json
{
  "email_thread_id": "thread_12345",
  "parsing_strategy": "multi_stage_commercial_extraction",
  "target_categories": ["RFQ", "Dispute_Notice", "Contract_Amendment"],
  "generate_draft_reply": true
}
```

Outputs
- Document classification and urgency score.
- Structured data extraction (dates, amounts, parties).
- High-stakes stakeholder alignment communication drafts.
- Automated escalation routing directives.

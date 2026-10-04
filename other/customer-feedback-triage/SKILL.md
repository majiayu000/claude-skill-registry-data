---
name: customer-feedback-triage
description: Triage customer feedback into themes, urgency, draft responses, and escalation notes.
risk: medium
required_tools:
  - file.read
  - memory.search
  - memory.propose
suggested_subagent: business-operator
business_domain: customer-support
cadence: daily, weekly
approval_required_for:
  - memory.propose
  - file.write_safe
  - app.action_proposed
---

# Customer Feedback Triage

Use this skill when the user wants to review comments, complaints, or customer messages.

Rules:
- Treat customer names, phone numbers, addresses, order details, and complaints as sensitive business data.
- Draft replies locally; do not send messages.
- Escalate safety, refund, legal, or public reputation issues to the user.

---
name: stripe-invoicer
description: Create Stripe invoices with deal tracking, payment status monitoring, late payment alerts, and revenue recognition reporting. Auto-sync with CRM and analytics.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

Instructions:
To run this skill, you MUST call the run_js tool with this parameter:
- data: A JSON string with the keys "client_email", "amount" (integer), and "description".

CRITICAL: If the user doesn't provide a specific amount, make a logical guess based on the work described (e.g., "Web design" -> $1500).

Example tool call: run_js(data='{"client_email": "client@example.com", "amount": 500, "description": "Logo Design Services"}')
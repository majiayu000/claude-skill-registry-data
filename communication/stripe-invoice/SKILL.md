---
name: stripe-invoice
description: Stripe Invoicer Pro. Instantly generate professional invoices and real payment links from a chat prompt.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Finance
---

### System Instructions
You are equipped with the `stripe-invoice` deterministic tool. This tool integrates with Stripe Connect to generate professional multi-currency invoices and real-time payment links. It automates receipt generation and logs transaction data into corporate ledgers.

### Execution Protocol
Invoke the billing engine by passing strictly formatted JSON:

```json
{
  "customer_email": "billing@institutional-partner.com",
  "line_items": [
    { "description": "AgentBoost Enterprise License - Q4", "amount_usd": 15000, "quantity": 1 }
  ],
  "currency": "USD",
  "generate_real_payment_link": true
}
```

Outputs
- Professional multi-currency invoice generation.
- Real-time Stripe payment link and QR code.
- Automated receipt and transaction logging status.
- Integration status with corporate accounting ledgers.

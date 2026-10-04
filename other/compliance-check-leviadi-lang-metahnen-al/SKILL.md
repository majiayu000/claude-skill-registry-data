---
name: compliance-check
description: Use whenever output to customers, prompts, or tool behavior might touch financial advice, regulation, or sensitive data. Enforces the spec's compliance rules — what is/isn't allowed.
---

# Compliance Check skill

## When to invoke

- Reviewing any customer-facing text (WhatsApp/email/CRM)
- Designing or modifying system prompts
- Adding new tools that could produce financial advice
- Reviewing escalation logic

## Hard rules (non-negotiable, from spec)

1. **Never** fabricate numbers (returns, balances, fees, tax rates)
2. **Never** quote a specific regulation/section without citing source
3. **Never** give a specific investment recommendation
4. **Never** discuss a customer's case with a different customer
5. Personalized financial advice requires explicit human licensee approval — Claude prepares draft, advisor approves

## Escalation triggers (auto-route to human)

- Regulatory question ("האם מותר לי...", "מה החוק אומר")
- Customer crisis (anger, threat, complaint to regulator, "אני אתבע")
- Compliance doubt (uncertain whether response is allowed)
- Missing critical data (advisor name, customer_id, process stage)
- Personal advice request ("מה הכי כדאי לי?", "תגיד לי איזה מסלול")
- API failure that affects a customer's process

## Review checklist for any prompt change

- [ ] Does the prompt instruct to refuse fabrication?
- [ ] Does it list escalation triggers explicitly?
- [ ] Does it require Hebrew output for customer-facing channels?
- [ ] Does it forbid quoting unverified figures?
- [ ] Is there a clear "when in doubt, escalate" rule?

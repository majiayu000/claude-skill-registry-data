---
name: ticket-triage
description: Classify and prioritize customer support tickets. Use when Codex is asked to triage support requests, assign severity, identify customer impact, summarize ticket facts, route ownership, detect missing information, or prepare next support actions.
license: MIT
---

# Ticket Triage

## Core Workflow

1. Separate customer facts from assumptions, guesses, and internal notes.
2. Identify customer goal, product area, account or plan context, impact,
   urgency, sentiment, and requested outcome.
3. Classify the ticket by type: how-to, bug, billing, access, data, incident,
   security, feature request, cancellation, renewal, or feedback.
4. Assign severity using the supplied support policy or escalation rules. If no
   policy is available, label severity as provisional and explain why.
5. Identify missing information needed to resolve or route the ticket.
6. Recommend owner, next action, and whether a reply draft, escalation pack, or
   KB draft is appropriate.

## Safety Rules

- Do not promise refunds, SLAs, incident status, fixes, timelines, or policy
  exceptions.
- Do not recommend account, billing, entitlement, or data changes without
  approval.
- Do not ask customers to send passwords, secrets, tokens, full payment data,
  or unredacted sensitive logs.
- Escalate security, privacy, legal, payment, data-loss, production outage, and
  high-value customer risks.

## Deliverable Shape

For ticket triage, provide:

- Customer issue summary
- Ticket type and product area
- Impact, urgency, and sentiment
- Severity with rationale
- Known facts and missing information
- Recommended owner
- Next action
- Escalation or reply-drafting notes

## References

- Read `references/ticket-triage-checklist.md` when triaging a support request
  or creating a support queue review.

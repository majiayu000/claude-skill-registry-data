---
name: escalation-pack
description: Prepare support escalation handoffs. Use when Codex is asked to escalate a customer issue, summarize severity and impact, package reproduction evidence, create an engineering handoff, prepare a billing/security/legal escalation, or request an internal decision.
license: MIT
---

# Escalation Pack

## Core Workflow

1. Identify why escalation is needed and what decision or action is requested.
2. Summarize the customer impact, severity, affected product area, environment,
   timeline, and current status.
3. Collect evidence: reproduction steps, observed results, expected results,
   redacted logs, sanitized screenshots, account context, related tickets, and
   prior attempts.
4. State what support has already tried and what remains unknown.
5. Route to the correct owner using escalation rules when available.
6. Draft a concise internal handoff and a separate customer update if requested.

## Safety Rules

- Do not expose internal escalation notes to the customer unless rewritten for
  customer-facing use.
- Do not assign severity as final when policy evidence is missing.
- Do not promise a fix, credit, refund, workaround, or timeline without owner
  approval.
- Do not include secrets, tokens, passwords, full payment data, or unnecessary
  customer personal data in escalation notes.
- Escalate immediately for security, privacy, data loss, broad outage, payment,
  legal, or executive-account risk.

## Deliverable Shape

For escalations, provide:

- Escalation reason
- Severity and customer impact
- Requested owner and decision
- Evidence package
- Steps already tried
- Unknowns and blockers
- Suggested internal handoff
- Optional customer update draft

## References

- Read `references/escalation-pack-checklist.md` when preparing support,
  engineering, billing, security, legal, or leadership escalations.

---
name: ops-ticket-intake-and-triage
description: Turn messy campaign requests into actionable programmatic operations tickets with required fields, severity, SLA, owner, evidence, acceptance criteria, and rejection rules for unclear asks. Use for Jira, Asana, Monday, spreadsheet queues, launch requests, trafficking requests, reporting asks, and client service tickets.
---

# Ops ticket intake and triage

A programmatic desk fails when requests enter as vague sentences: "launch this", "fix spend",
"update creative", "pull a report". This skill converts requests into operational tickets that
can be accepted, rejected, prioritized, assigned, and audited.

The assistant helps operators enforce intake quality. It does not approve work, change live
campaigns, or bypass the desk's priority model.

## When to use this skill

- A user asks to triage programmatic tickets or clean up a queue.
- A request is missing platform, campaign, budget, flight, creative, targeting, tags, or owner.
- A launch, trafficking, reporting, creative, taxonomy, billing, or optimization ask needs an
  SLA and acceptance criteria.
- The team wants a standard ticket template across Jira, Asana, Monday, Sheets, or email.

## Required fields

Reject or return the ticket if a required field is missing and cannot be inferred from an
attached source of truth.

| Field | Why it matters |
| --- | --- |
| Request type | Launch, edit, optimization, reporting, creative, tag, access, support, billing |
| Advertiser and platform | Prevents cross-account mistakes |
| Campaign, order, line item, ad group, or placement IDs | Names alone are not enough |
| Requested change | The exact thing being asked |
| Business reason | Why this matters and what outcome is expected |
| Deadline and time zone | Prevents false urgency and missed launches |
| Owner and approver | Makes the next decision explicit |
| Evidence or source | Brief, IO, platform export, screenshot, report, spec, or client email |
| Acceptance criteria | What must be true for the ticket to be done |
| Risk flags | Spend, brand safety, regulated category, consent, billing, legal, client-visible |

## Severity model

| Severity | Definition | Default response |
| --- | --- | --- |
| Sev 1 | Live spend, brand, or legal risk active now | Acknowledge immediately, contain first |
| Sev 2 | Material delivery, launch, tracking, or client deadline risk | Same business day owner and plan |
| Sev 3 | Routine edit, QA, report, creative, or access request | Standard SLA |
| Sev 4 | Nice-to-have cleanup, analysis, or future planning | Backlog or scheduled |

Severity is based on risk and time sensitivity, not on who asked loudest.

## Core process

1. **Normalize the ask.** Rewrite the request into a single clear action: "Add Creative A to
   Line Items 123, 124, and 125 in DV360 for Advertiser X by July 7, 2026, pending creative
   approval." If the action cannot be written, the ticket is not ready.
2. **Validate required fields.** Check the ticket against the required field table. Do not
   accept a live-change request without platform, advertiser, IDs, deadline, source, and
   acceptance criteria.
3. **Assign category and severity.** Category routes the ticket to the right owner. Severity
   sets the response clock. A launch blocker due today is not a routine ticket.
4. **Check approval requirements.** Use `approval-and-escalation-governance` for budget,
   bidding, brand-safety, targeting expansion, access, or client-facing changes.
5. **Attach the evidence package.** Store the source artifact that proves the request is real:
   client email, signed IO, media plan, tag sheet, export, screenshot, or report.
6. **Set acceptance criteria.** Done is not "updated". Done is "line items 123 to 125 have the
   approved creative assigned, creative preview passes, click URL works, and the launch QA row
   is updated."
7. **Route or return.** Route accepted tickets to the owner. Return unclear tickets with the
   exact missing fields, not a vague "need more info".

## Routing rules

| Ticket type | Primary owner | Supporting skill |
| --- | --- | --- |
| Launch or preflight | programmatic-ops-lead | `cross-platform-launch-qa` |
| Bulk edit | account-operations-specialist | `bulk-change-governance-and-rollback` |
| Creative add or swap | ad-ops-trafficker | `creative-review-and-approval-queue` |
| Conversion or tag issue | measurement-and-tagging-engineer | `tag-and-pixel-governance` |
| Delivery or pacing issue | optimization-specialist | Platform troubleshooting skill |
| Support case | programmatic-ops-lead | `platform-support-escalation` |
| Access or permission | account-operations-specialist | `platform-access-and-permissions-governance` |
| Billing or close | measurement-analyst | `programmatic-month-end-close` |

## Intake template

```text
Ticket title:
Request type:
Advertiser:
Platform:
Campaign/order/line/ad group IDs:
Requested change:
Business reason:
Deadline and time zone:
Owner:
Approver:
Source evidence:
Risk flags:
Acceptance criteria:
```

## Return-to-requester message

```text
I cannot accept this ticket yet. Please add:
- Platform and advertiser
- Exact entity IDs
- Requested change
- Deadline with time zone
- Source evidence
- Acceptance criteria

Once those are attached, I can triage severity, owner, approval path, and next action.
```

## Common pitfalls

- Accepting names instead of IDs. Names can duplicate and drift.
- Letting "urgent" replace severity. Urgency must tie to spend, launch, brand, legal, or client
  deadline risk.
- Finishing tickets without evidence. If the desk cannot prove the state changed, the ticket is
  not closed.
- Hiding approvals inside comments. Approval needs an explicit approver, timestamp, and scope.

## Related artifacts

- `templates/ops/ticket-intake-template.md`
- `programmatic-ops-control-center`
- `approval-and-escalation-governance`
- `change-management-and-incident-response`

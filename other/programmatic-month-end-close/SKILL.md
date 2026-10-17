---
name: programmatic-month-end-close
description: Run month-end close for programmatic media, including delivery and spend reconciliation, ad server versus DSP discrepancies, platform invoices, make-goods, accruals, billing codes, taxonomy checks, client evidence packs, and sign-off. Use when the user asks for billing close, invoice reconciliation, delivery close, accruals, make-goods, or finance handoff.
---

# Programmatic month-end close

Month-end close is where campaign operations becomes finance evidence. The desk needs to prove
what delivered, what spent, what should be billed, what differs across systems, and what needs
a make-good or accrual. This skill gives the close process.

Use `discrepancy-and-reconciliation` for the measurement and ad server discrepancy method. Use
this skill to run the full close calendar and handoff.

## When to use this skill

- Month-end or campaign-end delivery needs to be closed.
- Platform spend, ad server delivery, client reporting, and invoices do not match.
- A finance team needs billing evidence, accruals, make-good notes, or PO mapping.
- A client asks for final delivery, overdelivery, underdelivery, or discrepancy explanation.
- A platform invoice or credit needs review.

## Close package

| Component | Required evidence |
| --- | --- |
| Delivery export | Platform and ad server delivery by campaign, line, placement, date |
| Spend export | Media spend, fees where available, currency, tax or billing basis |
| Conversion export | If billed or judged on outcomes, the agreed conversion source |
| Discrepancy log | Difference by source, tolerance, root cause, action |
| Invoice or billing file | Platform invoice, DSP spend file, publisher invoice, or finance export |
| Taxonomy and PO map | Campaign code, cost center, PO, advertiser, market |
| Make-good or credit | Reason, amount, owner, approval, expected timing |
| Accrual | Amount, rationale, source, finance owner |
| Sign-off | Ops, account, finance, and client owner where required |

## Close calendar

| Window | Work |
| --- | --- |
| Last 3 business days | Check pacing risk, taxonomy, PO mapping, invoice setup, and known discrepancies |
| Day 1 to 2 after close | Pull delivery, spend, conversion, and ad server exports |
| Day 2 to 4 | Reconcile platform, ad server, analytics, and invoice numbers |
| Day 4 to 5 | Resolve exceptions, document credits, prepare finance handoff |
| By client deadline | Send approved close pack or billing backup |

Adjust the dates to the client and finance calendar, but do not remove the pre-close check.

## Core process

1. **Freeze the close scope.** Define the month, clients, advertisers, platforms, campaigns,
   currencies, time zones, and billing basis. Write whether the client bills on DSP spend,
   ad-server impressions, publisher invoices, or another source.
2. **Pull source exports.** Pull platform delivery, ad server delivery, spend, conversion,
   invoice, and dashboard extracts using the same date range and time zone where possible.
3. **Validate taxonomy and billing keys.** Campaign code, cost center, PO, market, advertiser,
   and platform keys must join. Missing keys are close blockers.
4. **Reconcile delivery and spend.** Compare platform vs ad server, platform vs invoice,
   dashboard vs source, and currency conversions where applicable. Use tolerance bands from
   `discrepancy-and-reconciliation`.
5. **Classify exceptions.** For each exception, mark timing lag, known discrepancy, invalid
   traffic, make-good, credit, setup error, missing invoice, platform issue, or data fault.
6. **Size financial impact.** Convert exceptions into dollars, impressions, conversions, or
   credit amount. Finance needs numbers, not adjectives.
7. **Collect approvals.** Ops confirms delivery evidence, measurement confirms numbers, account
   confirms client framing, finance confirms billing treatment.
8. **Archive the close pack.** Store exports, reconciliation file, exception log, invoices,
   approvals, and client copy in the approved location.

## Exception log template

```text
Month-end exception
Client:
Advertiser:
Platform:
Campaign:
Source A:
Source B:
Metric:
Difference:
Tolerance:
Root cause:
Financial impact:
Action:
Owner:
Due:
Approval:
```

## Decision rules

- Do not send a client final delivery number that does not state its source.
- Do not mix time zones inside one close pack without documenting it.
- Do not net discrepancies away without keeping the line-level evidence.
- Treat missing taxonomy or PO mapping as a close blocker, not an admin cleanup.
- If a platform invoice disagrees materially with source delivery, hold the billing line until
  the exception is classified and approved.

## Common pitfalls

- Waiting until the first of the month to discover a missing PO or invalid taxonomy.
- Reconciling dashboard numbers instead of source exports.
- Forgetting currency, fees, tax, or time-zone differences.
- Treating a make-good as a note instead of an approved finance action.
- Losing the support case or incident evidence that explains an invoice exception.

## Related artifacts

- `templates/ops/month-end-close-checklist.md`
- `discrepancy-and-reconciliation`
- `cross-platform-conversion-reconciliation`
- `marketing-analytics-warehouse-and-dashboards`
- `platform-support-escalation`
- `month-end-close` loop

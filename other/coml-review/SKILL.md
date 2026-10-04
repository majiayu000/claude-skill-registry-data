---
name: coml-review
version: 1.0.0
description: Triage an incoming commercial document, route it to the right review skill, run a first-pass red-flag scan, and produce a consolidated verdict.
author: matrixx0070
tags: [commercial-legal, triage, routing, review, escalation]
capabilities: []
---

## When to use

Use this as the front door when a contract arrives and you are not sure which review path it needs, or when a bundle of documents (MSA + order form + DPA) needs to be sorted and reviewed together. It classifies, dispatches, and rolls up.

**Not for:** deep single-type analysis once you know the type — go straight to coml-nda-review, coml-saas-msa-review, or coml-vendor-agreement-review. Setting up the playbook first is coml-cold-start-interview.

## Method

1. Identify document type: NDA, SaaS/MSA, vendor/services, or a proposal/order form. If the bundle mixes types, list each and its dependencies.
2. Run a first-pass red-flag scan across all documents: uncapped liability, IP shifts, data/privacy terms, auto-renewal, missing exit — anything on the escalation gate.
3. Route each document to the matching review skill; note which incorporate others by reference so nothing is reviewed in isolation.
4. **Escalation gate:** if the red-flag scan hits any gate item, flag it now (coml-escalation-flagger) so counsel starts in parallel with the detailed review.
5. Consolidate the sub-verdicts into one recommendation and a prioritized issues list.

## Example

Bundle: mutual NDA + SaaS MSA + order form. Type map: NDA → coml-nda-review; MSA → coml-saas-msa-review; order form incorporates MSA, review together. Red-flag scan: MSA has uncapped breach liability against you (escalate now). Consolidated verdict: NEGOTIATE — one blocker (liability), two fallback deviations (auto-renew, price cap). Counsel engaged on liability while redlines drafted.

## Pitfalls

- Reviewing an order form without pulling the MSA it incorporates.
- Sending everything to counsel indiscriminately instead of triaging first — or the reverse, missing a gate item.
- Producing per-document verdicts with no single recommendation for the decision-maker.
- Losing track of which document controls when terms conflict across the bundle.

## Output format

```
REVIEW TRIAGE — <counterparty> | docs: <count> | date
Type map:
  - <doc> → <route> (incorporates: <refs>)
Red-flag scan: <gate hits or clean>
Sub-verdicts: <doc → SIGN/NEGOTIATE/REJECT>
Consolidated verdict: <one recommendation>
Priority issues: <ranked list>
Escalated to counsel: <items or none>
```

## Reference

**Attorney-escalation gate** — route to counsel before agreeing, never decide alone, on: uncapped or one-sided liability, IP assignment or ownership shifts, indemnity you would owe for the vendor's own product, data-breach or privacy obligations, non-standard governing law or mandatory arbitration, anything a business owner cannot reverse, or any deal above your signing authority.

### NDA clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Term | 2-3 yr (trade secrets survive longer) | up to 5 yr | perpetual on ordinary CI |
| Mutuality | mutual | one-way when we only disclose | one-way binding us as recipient |
| CI definition | marked or reasonably identifiable | all disclosed | "anything discussed", no carve-outs |
| Carve-outs | public / independently developed / rightfully received / compelled | narrowed set | none |
| Residuals | none | narrow, memory-only | broad reuse license |
| Remedies / law | mutual injunctive, our or neutral law | neutral law, no bond | one-sided + liquidated damages |

### SaaS / MSA clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Liability cap | 12 mo fees | 24 mo fees | uncapped for us / their cap ≤3 mo |
| Cap carve-outs | IP, confidentiality, data breach | + willful misconduct | breach uncapped against us only |
| Indemnity | mutual IP; vendor covers data breach | mutual | we indemnify their product |
| Data | customer owns; export on exit | customer owns | vendor licenses or resells data |
| Security / SLA | SOC 2 + 99.9% + credits | 99.5% | no SLA, no security terms |
| Auto-renew | opt-in, 30-day notice | 60-day notice | evergreen, 90-day, uncapped uplift |
| Price increase | CPI or ≤5% | ≤7% | uncapped at renewal |

### Vendor / services clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Payment | net-30 / net-45 | net-15 | full prepay, no milestones |
| IP in deliverables | work-for-hire to us | perpetual license to us | vendor retains |
| Insurance | ≥$1M GL + cyber | $500K | none |
| Termination | for cause + convenience, 30-day | for cause only | locked full term, no exit |
| Audit / compliance | annual audit right | on cause | none |

### Renewal-notice tracking
| Field | Capture |
|---|---|
| Effective / expiry date | contract dates |
| Notice window | e.g. 60 days pre-expiry |
| Notice deadline | expiry − window (put on the calendar) |
| Auto-renew | yes/no + renewal term |
| Reminders | 90 / 60 / 30-day pings to the owner |

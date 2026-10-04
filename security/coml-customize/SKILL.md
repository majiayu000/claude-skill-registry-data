---
name: coml-customize
version: 1.0.0
description: Adapt the commercial-legal playbook and its standard / fallback / walk-away positions to a company's risk tolerance, industry, and signing authority, and version the result.
author: matrixx0070
tags: [commercial-legal, playbook, customization, positions, versioning]
capabilities: []
---

## When to use

Use this to turn the generic reference positions into your company's own playbook, or to update it when risk tolerance, industry, or authority tiers change. Every review skill measures deviations against these positions, so this is what makes their verdicts fit your organization.

**Not for:** the initial capture from a blank slate (use coml-cold-start-interview), or applying the playbook to a specific contract (the review skills).

## Method

1. Start from the current positions — the cold-start stub or the last playbook version.
2. Walk each row of the three reference tables and adjust the standard, fallback, and walk-away to fit. Record the rationale for every change so future reviewers understand the intent.
3. Layer industry overrides where needed — regulated data, government contracting, or high-IP work often demand stricter defaults on data, security, and IP.
4. Set signing-authority thresholds so the playbook knows when a term is auto-approvable versus escalation-only.
5. **Escalation gate:** never soften a gate term (uncapped liability, IP shift, data/privacy, non-standard law) into auto-approvable without counsel sign-off; those stay routed to a human.
6. Version the playbook (date + version number) and note what changed so amendment history and audits stay clean.

## Example

Fintech customizing the base playbook: tighten SaaS data to "customer owns + no sub-processor without notice + data residency" (rationale: regulated data); raise vendor insurance floor to $2M with cyber (rationale: PII exposure); keep liability cap at 12 months but move any uncapped-breach ask to counsel-only. Signing authority: <$10K auto if all standard; anything with a data term is escalation-only. Versioned v2, 2026-07-11, with a change note per row.

## Pitfalls

- Changing positions with no rationale, so reviewers cannot tell intent from accident.
- Softening a gate term into auto-approvable and quietly removing the counsel check.
- Ignoring industry-specific requirements that override the generic defaults.
- Not versioning, so it is impossible to tell which playbook a past review used.

## Output format

```
PLAYBOOK — <company> | version <n> | <date>
Changes from prior version:
  - <table.row>: <old → new> — rationale: <...>
Industry overrides: <items>
Signing authority: <threshold → auto | escalation-only>
Counsel-only terms (never auto): <gate items>
Change note: <summary>
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

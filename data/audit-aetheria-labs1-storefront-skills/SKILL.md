---
name: audit
description: Read-only conversion audit of a whole storefront page. Scores above-the-fold, offer strength, proof, copy, design, mobile and funnel data against the build rules and returns ranked fixes. Never edits; hand approved fixes to /optimize.
---

# Audit a Page

Produce an evidence-based CRO report for one live or draft page. This skill
changes nothing: no page writes, no generation, no publishing.

## References

| Reference | Read when |
|---|---|
| `references/page-types/_index.md`, then the type file | always |
| `references/evidence-led-cro.md`, `references/consumer-behavior-cro.md` | always |
| `references/design-rules.md` | always |
| `references/offers/offer-strategy.md`, `references/offers/offer-stacking.md`, `references/offers/offer-ledger.md` | always |
| `references/proof/proof-ledger.md` | always |
| `references/copy/headline-and-cta-rules.md`, `references/anti-patterns/cro-anti-patterns.md`, `references/anti-patterns/mobile-anti-patterns.md` | always |
| the matching section of `references/industry-cro.md` | when the vertical is known |

## Gather

1. Resolve the page: `lexsis_pages.find`, `lexsis_pages.get`,
   `lexsis_pages.inspect`, `lexsis_pages.source`.
2. Read `lexsis_analytics.page`, `lexsis_analytics.page_funnel`,
   `lexsis_analytics.page_attribution` and `lexsis_analytics.timeseries`. If
   data is missing or thin, say so; do not invent findings from it.
   For product and collection templates, also read
   `lexsis_analytics.resource_funnel`, `lexsis_analytics.resource_attribution`,
   `lexsis_analytics.resource_orders`, `lexsis_analytics.resource_views` and
   `lexsis_analytics.resource_vitals`.
3. Open the page in the host browser at 390 and 1280. Screenshot the first
   screen before any scroll.
4. `lexsis_assets.view` on hero and offer images; `lexsis_catalog.get` and
   `lexsis_catalog.reviews` for claimed products and proof.
5. If `work/storefront/setup.md` exists, read it for rules and personas. Its
   absence limits the report but does not stop it.

## Score

### Above the fold, at 390 and 1280

Pass or fail each, with the screenshot as evidence:

| # | Check |
|---|---|
| F1 | What it is and who it is for is clear within five seconds |
| F2 | The headline states the outcome and matches the ad or link that sent traffic |
| F3 | The hero image shows the product or its result |
| F4 | Price, or the offer, is visible on a PDP or offer page |
| F5 | The primary CTA is visible, high contrast, and states the action |
| F6 | Rating and review count sit near the title, when real reviews exist |
| F7 | One risk reducer is visible: returns, guarantee, or delivery date |
| F8 | Shipping cost or threshold is stated or one tap away |
| F9 | Nothing competes with the CTA: pop-ups, stacked bars, a second offer |
| F10 | Largest image is not lazy-loaded and appears quickly |

### Whole page

| Area | Rule source |
|---|---|
| Page type contract | `<type>.md` checklist |
| Offer | value score and OS rules in `offer-stacking.md`, offer-ledger |
| Proof | proof-ledger |
| Copy | headline and CTA rules |
| Design | design-rules N1-N14, A1-A12 |
| Mobile | mobile-anti-patterns |
| CRO tells | cro-anti-patterns |
| Funnel | biggest drop-off, device and source split |

Give each area 0 to 100 and one overall score. Unverified claims and
compliance problems are blocking, whatever the score.

## Report

```markdown
# Audit: <page> (version <n>, <date>)

## Summary
Overall: <score> | Blocking: <n> | Biggest opportunity: <one line>

## Above the fold
| Check | 390 | 1280 | Evidence |

## Scorecard
| Area | Score | Key finding | Rule |

## Offer
Value score, current stack, missing stack items, margin unknowns.

## Ranked fixes
| # | Fix | Evidence | Impact H/M/L | Effort H/M/L | Test or ship |

## Not assessed
<missing data>
```

Rank by evidence, impact, and effort. Do not promise a lift percentage. Mark
ideas without page evidence as hypotheses, and send uncertain ones to
`/ab-test`.

Write the report to `work/storefront/audits/<page-id>-v<version>.md`.

## Return

Return the report path, overall score, blocking count, the top three fixes, and
the state `AUDIT_READY`. To apply fixes, the user runs `/optimize`.

---
name: local-seo
description: Local SEO dominance system for UK service businesses. FAIL/PASS enforcement. GBP + area pages + reviews.
---

# Local SEO Skill

## Primary Objective

**Dominate local pack + service area organic results.**

## Scope

| ✅ Supported | ❌ Out of Scope |
|-------------|----------------|
| Single-location UK business | Multi-branch franchises |
| Service-area business | E-commerce / SaaS |

## Skill Output

```yaml
local_seo:
  primary_money_page: "/services/house-removals"
  nap_record: {...}
  services_canonical: [...]
  area_weights: {...}
  keyword_ownership: {...}
  state: PASS | WARN | FAIL
  blocking_issues: []
```

## Primary Money Page

**One page gets priority.** All local SEO decisions strengthen this first.

```yaml
primary_money_page: "/services/house-removals"
```

Links, reviews, GBP focus → this page first.

## Services Canonical List

**Single source of truth.** Must match everywhere.

```yaml
services_canonical:
  - "House Removals"
  - "Office Removals"
  - "Packing Service"
```

**Rule:** If not in this list → not on GBP, not on website, not in schema.

## Area Revenue Weights

`area_weights: { bristol: 1.0, bath: 0.7, gloucester: 0.4, weston: 0.2 }`

Low-weight areas get fewer links, less review focus.

## Keyword Ownership

**1 keyword = 1 page. Hard lock.**

| Keyword | Page |
|---------|------|
| "house removals bristol" | `/` |
| "removals bath" | `/areas/bath` |
| "office removals bristol" | `/services/office-removals` |

**FAIL if:** Same keyword in H1 on multiple pages.

## NAP Standard

`[Business Name] / [Street Address] / [City], [Postcode] / [+44 Phone]`

**Identical on:** website footer, GBP, all citations. **FAIL if mismatch.**

## GBP ↔ Website Parity

Services, Address, Phone must match exactly: GBP = Website = Schema. **FAIL if mismatch.**

## GBP Primary Category Lock

```yaml
gbp_primary_category: "House removal service"  # LOCKED
```

**Primary category cannot change.** Keyword-chasing category changes = FAIL.

## GBP → Area Page Mapping

```yaml
gbp_area_mapping:
  bath: "/areas/bath"
  gloucester: "/areas/gloucester"
```

**Every GBP service area must have matching website page.** Mismatch = FAIL.

## Review Velocity

| Metric | Requirement |
|--------|-------------|
| Minimum total | 10 |
| Per 30 days | 1+ |
| Max gap | 30 days |
| Response rate | 100% |

**FAIL if:** Gap >30 days OR 0 reviews OR unresponded.

## Local Proof Density

**Min 2 per area page.** Types: review snippet, street name, postcode, landmark.

**FAIL if:** Area page has <2 local proofs.

## Area Page Minimums

| Requirement | Threshold |
|-------------|-----------|
| Words | 600+ |
| Unique | 30%+ |
| Proofs | 2+ |

## GBP Posts

Weekly rotation: job → offer → review → team. Mix ranking posts (jobs, service) with conversion (offers, CTAs).

## SERP Feature Targets

| Page | Targets |
|------|---------|
| Homepage | local_pack, review_stars |
| Service | faq_rich, review_stars |
| Area | local_pack, faq_rich |

## Citation Limits

Tier 1 (all): GBP, Bing, Apple, Yell → Tier 2 (max 5): Industry specific → **STOP.**

## Geo-Modifier Cap

| Location | Max |
|----------|-----|
| H1 | 1 |
| H2+H3 total | 2 |
| Body per 500w | 2 |

**Over = spam risk → WARN.**

## FAIL States (Deploy Blocked)

| Condition | State |
|-----------|-------|
| No GBP claimed | ❌ |
| NAP inconsistent | ❌ |
| GBP ≠ Website services | ❌ |
| GBP primary category changed | ❌ |
| GBP area ≠ website area page | ❌ |
| No LocalBusiness schema | ❌ |
| 0 reviews | ❌ |
| Review gap >30 days | ❌ |
| Area page <600w / <30% unique / <2 proofs | ❌ |
| Photos without geo-tag | ❌ |
| Phone not clickable (mobile) | ❌ |
| Same keyword in H1 on 2+ pages | ❌ |

## WARN States (Deploy Allowed, Flagged)

| Condition |
|-----------|
| <10 total reviews |
| No GBP post in 7 days |
| Missing Tier 1 citation |
| No FAQ schema |
| Geo-modifier over cap |

## Health State

```yaml
local_seo_state: PASS | WARN | FAIL
blocking_issues: []
```

## Deployment Gate

```yaml
deployment_gate:
  block_on_fail: true
  warn_on_warn: true
```

**FAIL → production deploy blocked. No exceptions.**

## References

- [gbp-checklist.md](references/gbp-checklist.md)
- [area-page-template.md](references/area-page-template.md)
- [citations-uk.md](references/citations-uk.md)
- [review-templates.md](references/review-templates.md)
- [competitive-edge.md](references/competitive-edge.md) — 32 advanced tactics

## Definition of Done

- [ ] primary_money_page + services_canonical + keyword_ownership defined
- [ ] NAP identical everywhere, GBP verified
- [ ] 10+ reviews, no 30-day gap, all responded
- [ ] Area pages: 600w / 30% unique / 2 proofs
- [ ] Tier 1 citations complete
- [ ] local_seo_state = PASS

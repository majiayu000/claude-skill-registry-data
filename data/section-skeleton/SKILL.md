---
name: section-skeleton
description: Generates Astro component skeleton with slots. Stateless, deterministic. No content.
---

# Section Skeleton Skill

## Purpose

Outputs Astro component skeleton with named slots. Structure only.

## Input

```yaml
section_type: hero | trust-strip | problem | solution | benefits | how-it-works | social-proof | faq | final-cta | footer | pricing | gallery
variant: default | compact | expanded
page_type: landing | service | service-area | article | calculator | thank-you
```

## Output

```yaml
skeleton: "<section>...</section>"
slots: [headline, body, cta-primary]
slot_semantics: { headline: h2_primary }
skeleton_verdict: PASS | WARN | FAIL
```

## Page-Type Compatibility

| Section | Allowed | Forbidden |
|---------|---------|-----------|
| hero | landing, service, service-area | - |
| problem | landing | service-area, article |
| solution | landing | article, thank-you |
| pricing | service, landing | article, thank-you |
| gallery | service, landing | calculator |
| calculator-widget | calculator, landing | article |
| local-reviews | service-area | landing |
| upsell | thank-you | landing, service |

**Forbidden combination → STOP.**

## Section Order Constraints

| Section | Rule |
|---------|------|
| hero | must_be_first |
| footer | must_be_last |
| final-cta | before footer only |
| trust-strip | after hero only |

**Order violation → FAIL.**

## Slot Cardinality

| Slot | Min | Max |
|------|-----|-----|
| headline | 1 | 1 |
| subheadline | 0 | 1 |
| body | 0 | 1 |
| cta-primary | 0 | 1 |
| cta-secondary | 0 | 1 |
| image | 0 | 1 |
| items | 0 | ∞ |
| cards | 0 | ∞ |

**Max exceeded → FAIL. Required missing → FAIL.**

## Slot Semantic Roles

| Slot | SEO Role |
|------|----------|
| headline | h2_primary_keyword |
| subheadline | semantic_support |
| body | topical_depth |
| items | long_tail (FAQ) |

**Cross-reference:** `heading-tree` skill uses this.

## Variant Behaviour

### default
All slots available.

### compact
```yaml
forbidden_slots: [subheadline, cta-secondary, image]
```

### expanded
```yaml
required_slots: [image, subheadline]
```

**Variant violation → WARN.**

## Accessibility Requirements

| Slot | A11y Rule |
|------|-----------|
| image | alt required |
| faq items | aria-expanded |
| cta-* | aria-label if icon-only |

**A11y missing → WARN.**

## Slot Naming Convention

| Slot | Content Type |
|------|--------------|
| headline | H2 element |
| subheadline | Paragraph |
| body | Multiple paragraphs |
| cta-primary | Primary Button |
| cta-secondary | Secondary Button |
| cta-phone | Phone link |
| image | Picture component |
| items | Repeated list items |
| cards | Repeated card components |

## Skeleton Verdict

```yaml
skeleton_verdict: PASS | WARN | FAIL
issues: []
```

| Condition | Verdict |
|-----------|---------|
| Forbidden page-type | FAIL |
| Order violation | FAIL |
| Required slot missing | FAIL |
| Max cardinality exceeded | FAIL |
| Variant slot violation | WARN |
| A11y missing | WARN |
| All rules pass | PASS |

## FAIL States

| Condition |
|-----------|
| Section on forbidden page-type |
| hero not first |
| footer not last |
| Required slot missing (headline) |
| Slot count > max |

## WARN States

| Condition |
|-----------|
| Compact variant with forbidden slot |
| Image without alt |
| Icon button without aria-label |

## Non-goals

- Does NOT write content
- Does NOT style beyond structure
- Does NOT include interactivity
- Does NOT generate child components

## References

- [skeletons.md](references/skeletons.md) — Full Astro skeleton code

## Definition of Done

- [ ] section_type valid for page_type
- [ ] Order constraints satisfied
- [ ] Required slots present
- [ ] Cardinality rules pass
- [ ] Variant rules pass
- [ ] A11y requirements met
- [ ] skeleton_verdict = PASS

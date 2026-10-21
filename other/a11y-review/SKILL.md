---
name: a11y-review
description: Audit accessibility with automated and manual evidence. Triggers on "accessibility", "无障碍".
---

# Accessibility Review

## When to use

- Audit accessibility with automated and manual evidence.

**Not for:** frontend-design for redesign; e2e-testing for general journeys.

## Steps

1. Agree target and flows; consult current authoritative criteria rather than a frozen subset.

2. Run applicable tools and manual keyboard, focus, semantic, contrast and error checks.

3. Exercise assistive technology when available and disclose unavailable coverage; automation does not establish full conformance.

4. Document reproduction, impact and remedies at the approved path, retest fixes and leave acceptance to the human.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/a11y-report.md` when durable findings are requested.

## Verify

- Findings identify real controls and criteria; automated, manual and unavailable checks are distinguished.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/wcag-checklist.md](references/wcag-checklist.md) — WCAG 2.2 AA criterion-by-criterion checklist mapped to axe-core rules, with the manual checks automated tools miss

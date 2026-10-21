---
name: research
description: Investigate a question using verifiable sources and comparable criteria. Triggers on "deep research", "调研报告".
---

# Research

## When to use

- Investigate a question using verifiable sources and comparable criteria.

**Not for:** design-research for visuals; spec for requirements.

## Steps

1. Agree the question, decision, coverage and output path; choose general, market or tech-selection mode.

2. Read primary documentation and relevant real repository files. Record source, commit and implementation evidence; report unavailable community sources.

3. Compare candidates on the same requirements. Separate facts, inference and uncertainty; failed searches do not prove absence.

4. Lead with usefulness, applicability and recommendation, then evidence and limits. Explain what additional evidence could change the decision.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/research/YYYY-MM-DD-<slug>.md`, `docs/research/market.md` or `docs/research/competitor.md`; prefer its existing owner.

## Verify

- Claims trace to retrieved evidence; candidates share criteria and missing coverage is explicit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [product-principles.md](../../../references/product-principles.md) — product discipline (the real competitor is the current workaround). Linked by market + tech-selection modes.
- [references/report-spine.md](references/report-spine.md) — reader-first organization, evidence, diagram selection and human review.
- [references/general-mode.md](references/general-mode.md) — question framing, primary sources and bounded synthesis.
- [references/market-mode.md](references/market-mode.md) — problem, alternatives, sizing and distribution evidence with selection-bias limits.
- [references/tech-selection-mode.md](references/tech-selection-mode.md) — actual constraints, implementation evidence and comparable selection criteria.
- [references/web-tool-fallback.md](references/web-tool-fallback.md) — when a fetch tool is blocked or quota-exhausted: tiered fallback by quota dependency (GitHub → indexed docs → scrape → discovery), orthogonal to page-level retries.
- [references/pressure-scenarios.md](references/pressure-scenarios.md) — behavioral scenarios for certainty, access gaps, popularity and report bloat.

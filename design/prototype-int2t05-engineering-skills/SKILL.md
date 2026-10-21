---
name: prototype
description: Build a bounded disposable experiment to resolve a specific uncertainty. Triggers on "prototype", "原型".
---

# Prototype

## When to use

- Build a bounded disposable experiment to resolve a specific uncertainty.

**Not for:** implement for production work.

## Steps

1. State one uncertainty, observable criterion and effort bound; choose the simplest runnable form.

2. Implement only what exercises it; label simulated behavior and synthetic data.

3. Run and inspect the experiment against its criterion.

4. Report conclusions in conversation or an approved findings path; retain or remove the prototype according to its actual use.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/design/prototype-findings.md` when conclusions need persistence.

## Verify

- The experiment was run and narrows its question; simulated behavior is not presented as real integration.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [design-principles.md](../../../references/design-principles.md) — design discipline (hierarchy before decoration, design every state, recognize rather than recall).
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/logic.md](references/logic.md) — single-shareable-HTML logic prototype: pure module, free-play + guided walkthroughs
- [references/ui.md](references/ui.md) — toggleable UI variants: sub-shape A (existing page) vs B (throwaway route), floating switcher

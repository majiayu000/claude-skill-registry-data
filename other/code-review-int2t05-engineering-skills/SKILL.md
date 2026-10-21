---
name: code-review
description: Review a scoped change for correctness, coverage and material risk. Triggers on "review this", "代码审查".
---

# Code Review

## When to use

- Review a scoped change for correctness, coverage and material risk.

**Not for:** debugging for reproduction; purity-audit for residue.

## Steps

1. Choose pre-merge, in-flight, evidence-gate or receiving mode and inspect actual diff, contracts, callers and checks; review is read-only unless fixes were requested.

2. Trace consequential state, permission, error and regression paths; evaluate requirement coverage separately from code quality.

3. Recheck material findings against source and a concrete failing scenario; seek independent review only when authorized and justified.

4. Report high-confidence findings with severity, location, evidence and remedy; persistent tracking needs an approved path, not speculative code TODOs.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/TODO.md` only for agreed durable tracking; otherwise conversation.

## Verify

- Material findings have checked scenarios and evidence; reviewed, fixed and verified states remain distinct.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [clean-code.md](../../../references/clean-code.md) — naming, functions, smells.
- [mermaid-diagrams.md](../../../references/mermaid-diagrams.md) — diagram structure when reviewing architecture.
- [references/review-modes.md](references/review-modes.md) — the three non-default modes in full: in-flight adversarial doubt, evidence-gate verification, receiving review feedback.
- [references/tech-debt-register.md](references/tech-debt-register.md) — upgrade TODO.md to a prioritized register: interest/principal/risk/effort, paydown cadence, accepted-debt decisions.

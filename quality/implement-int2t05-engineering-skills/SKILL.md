---
name: implement
description: Implement an agreed change in verifiable steps. Triggers on "implement", "实现".
---

# Implement

## When to use

- Implement an agreed change in verifiable steps.

**Not for:** spec for unresolved behavior; architecture for consequential design.

## Steps

1. Inspect relevant contracts, code, user changes and actual commands; small unambiguous changes use an inline scope and checks.

2. Choose complete behavior slices or incremental mechanical steps. Use test-first at meaningful boundaries; configuration and generated artifacts use relevant validators.

3. Make the smallest correct change, verify unfamiliar APIs against current official docs and run affected checks after changed behavior.

4. Review the diff and failure paths; use independent review only when authorized and justified, otherwise self-review.

5. Complete relevant final checks, correct regressions and synchronize affected approved documents; report evidence and leave commits to explicit requests.

## Verify

- Acceptance behavior and relevant checks pass; diff is scoped, user work preserved and no commit or push inferred.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [clean-code.md](../../../references/clean-code.md) — code-quality bar for the implementation.
- [references/source-verification.md](references/source-verification.md) — source hierarchy, citation rules, retrieval safety.
- [references/doubt-cycle.md](references/doubt-cycle.md) — the five-step doubt cycle and cross-model escalation.
- [references/lightweight-changes.md](references/lightweight-changes.md) — small edits, renames, scaffolding that don't need a spec

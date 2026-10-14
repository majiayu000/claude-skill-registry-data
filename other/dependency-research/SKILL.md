---
name: dependency-research
description: "Research before guessing: official docs first, then repo, changelog, examples, RFCs. Never treat memory as docs."
---

# dependency-research

Need it? Prove it. Then pin it, license-check it, and own its updates.

## Activate when

- Considering a new dependency, evaluating alternatives, or checking compatibility/version behavior.

## Do NOT activate for

- Version-pinned API lookups (see research/documentation-search).

## Procedure

1. Justify: existing capability → framework-native → stdlib → existing dep → new dep. "Do we need a dependency at all?" first.
2. Evaluate candidates: maintenance (releases, bus factor), security history, license compatibility, bundle/runtime cost, API quality, type support, docs, version compatibility with the pinned stack.
3. Check supply chain: advisory history, maintainer trust, dependency-confusion risk; record the decision rationale.
4. Install pinned (lockfile updated), minimal scope; add a removal path note.
5. Verify: build + tests green, license check recorded, `audit` clean or findings triaged.

## References
- Related: `../../research/dependency-evaluation/`, `../../security/secrets-supply-chain/`.

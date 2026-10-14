---
name: plan-mode-audit
description: Judge an artifact against a named standard. Use when reviewing code, a document, or a design against a policy, style guide, security requirement, or set of invariants.
license: MIT
---

# Audit

Verify asks whether we did what we said. Audit asks whether the thing is good, consistent, and safe regardless of intent.

1. Name the artifact and the standard it will be judged against — a policy, a style guide, a security requirement, a performance budget, or a set of invariants. If no standard exists, say so and propose one before judging.
2. Enumerate the properties the standard requires. For each, inspect the artifact directly and record the evidence: file, line, or observation.
3. Report each property as met, violated, or unverifiable, with the specific evidence. Distinguish a violation of the standard from a violation of your preference.
4. For each violation, state the consequence and the smallest change that would resolve it. Rank by severity.

An audit judges against the standard you named, not against a better design. If the standard itself is wrong, say so separately.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.

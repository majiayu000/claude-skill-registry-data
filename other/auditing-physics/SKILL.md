---
name: auditing-physics
description: >-
  Checks science files for cross-layer contradictions, inconsistent equations,
  broken derivation chains, and violations of the universe's foundational axiom.
  Use when promoting drafts to canon, after writing new science content, after
  restructuring, or when user says "audit the science", "physics audit", "check
  for contradictions", "does this break anything", "verify the science", or
  "cross-layer check". Does NOT check frontmatter or writing standards — use
  /auditing-canon for that.
model: opus
effort: max
---

# Auditing Physics

Check science files for cross-layer consistency against the universe's
foundational rules.

## Prerequisites

Read CLAUDE.md for the universe's foundational axiom and locked rules.
If the project has reference files in `references/`, read those instead
of the full science backend.

## Chain of Draft Mode

Compress each reasoning step to ≤5 words. Mark conclusions with ####.

```
Axiom check. Signal exchange present. #### PASS.
Layer dependency. Upstream rule holds. #### PASS.
Equation check. Variable collision found. #### VIOLATION.
```

## Checks

For each file:

1. **Foundational Axiom Compliance** — does the mechanism reduce to the
   universe's core principle?
2. **Cross-Layer Consistency** — claims don't contradict upstream science
3. **Equation Consistency** — variables, constants, and formulas don't collide
4. **Derivation Chains** — each claim traces to a specific upstream principle

## Output

- **CONTRADICTION** — two files disagree on a rule
- **BROKEN-REF** — cross-reference to nonexistent file
- **COLLISION** — duplicate constants or numbering
- **DRIFT** — terminology inconsistency
- **GAP** — missing section that downstream files depend on

Do NOT fix anything. Report only.

## Out of Scope

Does NOT check frontmatter, naming, or writing standards (use /auditing-canon).
Does NOT verify a single term across the repo (use /cross-checking).
Does NOT write new content (use /writing-science).

---
name: source-evaluation
description: "Source evaluation: classify FACT/INFERENCE/ASSUMPTION/RECOMMENDATION/UNKNOWN. Evidence before confidence; cross-check community vs authority."
---

# source-evaluation

Label everything you believe: FACT, INFERENCE, ASSUMPTION, RECOMMENDATION, UNKNOWN. Never promote upward without new evidence.

## Activate when

- Any research output feeds an implementation decision; conflicting sources; uncertain claims.

## Do NOT activate for

- Direct official-doc lookups with clear answers (still cite, but no ceremony).

## Inspection

Collect the claim, its source, the source's level (L1–L8 per documentation-search), and any corroboration or contradiction.

## Decision rules

- FACT: verified in official docs/tests for the installed version, or reproduced locally. INFERENCE: logically derived from facts (show the chain). ASSUMPTION: unverified but necessary (mark owner + expiry). RECOMMENDATION: judgment call (show trade-offs). UNKNOWN: insufficient evidence — triggers more research, never implementation.
- Official sources beat community 1:1; community needs either official corroboration or local reproduction to promote.
- Two agreeing low-level sources ≠ one high-level source. Count levels, not links.

## Procedure

1. Classify each load-bearing claim before coding.
2. Resolve conflicts via the docs-vs-observed reconciliation (see documentation-search); record the outcome.
3. ASSUMPTIONs get explicit owners and re-check points; UNKNOWNs block the dependent decision.
4. Verify: decision record complete (see documentation-search templates), no UNKNOWN feeding code, assumptions tracked.

## Failure modes

- Snippet-as-fact; version-mismatched facts; silent promotion of assumptions; cherry-picked corroboration; "everyone does it" as evidence.

## Escalation

Ambiguous officials → source fallback chain in documentation-search; high-stakes calls → ask the user with options and evidence.

## References

- Related: `../../research/documentation-search/`, `../technology-evaluation/`.

---
name: candidate-mainline-ranker
description: Rank the most valuable research mainline directions across a professor candidate set by weighted occurrence statistics. Use when Codex has multiple professor direction maps or candidate records and needs to prioritize which current mainline directions to read first, especially for HKUST(GZ) RA/advisor scouting. Counts each direction across the primary and extended candidate pools, gives extra weight to each professor's rank-1 current mainline, adjusts for candidate priority/pool/confidence/evidence coverage, and outputs a transparent direction priority table with caveats.
---

# Candidate Mainline Ranker

Rank current mainline directions across a candidate professor set. This skill runs after one or more `professor-direction-mapper` outputs exist. It answers: "Which shared directions are most worth reading first because they recur as current mainlines across the candidate pool?"

It does not decide whether any single professor is a fit. It aggregates direction signals across candidates.

## Inputs

Preferred:

- A JSON file following `references/input-schema.md`.

Accepted:

- A directory of direction maps, if Codex can extract the same fields.
- A Markdown candidate table, if directions and ranks are explicit enough.
- Manual records pasted by the user.

Required per professor:

- Professor/lab name.
- Pool: `primary`, `extended`, or `historical`.
- Current mainline directions with order/rank.

Recommended per direction:

- Normalized direction label.
- Raw direction text.
- Rank within that professor's current mainlines.
- Confidence: high / medium / low.
- Evidence status: complete / sampled / weak / stale.
- Source direction-map path or URL.

## Default Weights

Use transparent additive/multiplicative scoring:

- Base occurrence: `1.0`.
- Rank-1 current mainline bonus: `+0.75`.
- Rank-2 current mainline bonus: `+0.35`.
- Rank-3+ current mainline bonus: `+0.0`.
- Pool multiplier:
  - primary: `1.0`
  - extended: `0.6`
  - historical-only: `0.25`
- Candidate priority multiplier:
  - P1: `1.0`
  - P2: `0.8`
  - P3: `0.6`
  - E1: `0.6`
  - E2: `0.45`
  - E3: `0.3`
  - unknown: `0.5`
- Confidence multiplier:
  - high: `1.0`
  - medium: `0.75`
  - low: `0.45`
- Evidence status multiplier:
  - complete: `1.0`
  - sampled: `0.8`
  - weak: `0.55`
  - stale: `0.35`
  - unknown: `0.7`

Formula per professor-direction record:

```text
score = (base_occurrence + rank_bonus) * pool_multiplier * priority_multiplier * confidence_multiplier * evidence_multiplier
```

The default formula is a decision aid, not a truth machine. If the user gives a different weighting policy, use that policy and state it.

## Workflow

1. Collect direction records.
   - Prefer current mainlines from `professor-direction-mapper` outputs.
   - Include extended candidates if requested; label them as lower-priority evidence through pool/priority multipliers.
   - Exclude historical mainlines unless the user asks for historical influence analysis.

2. Normalize direction labels.
   - Merge obvious aliases, such as `RAG`, `retrieval-augmented generation`, and `LLM retrieval`.
   - Keep a raw-label list for audit.
   - Do not over-merge broad fields. For example, `LLM agents`, `RAG`, and `LLM reasoning` may be adjacent but should remain separate unless evidence shows they are the same reading direction.

3. Score directions.
   - Use `scripts/rank_mainlines.py` when a JSON input is available.
   - Otherwise calculate manually using the default weights and show the scoring table.
   - Report both weighted score and raw professor count.

4. Interpret the ranking.
   - Prioritize directions that have high weighted score, multiple professors, and evidence from primary candidates.
   - Flag directions dominated by one professor, one extended candidate, weak evidence, or aliasing uncertainty.
   - Recommend the first 1-3 directions to read and explain why.

5. Return a durable output.
   - Use `references/output-template.md`.
   - Include scoring policy, ranked table, raw records, caveats, and recommended next reading actions.

## Guardrails

- Do not rank historical mainlines as current priorities unless explicitly requested.
- Do not let a broad umbrella label swallow distinct reading directions.
- Do not hide that a direction is driven by only one professor.
- Do not treat the highest weighted direction as automatically the best personal fit.
- Do not compare directions without showing the weighting policy.
- Do not count a direction twice for the same professor unless the direction appears as two genuinely distinct current mainlines.

## Resources

- `scripts/rank_mainlines.py`: score a JSON input and emit Markdown plus optional JSON.
- `references/input-schema.md`: input JSON schema and example.
- `references/output-template.md`: recommended human-readable report structure.

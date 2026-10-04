---
name: principle-promotion
description: "Promote high-value, evidence-backed claims into operational principles (principles-v1) that drive subagent behaviour, mapping each to profile rules / skills / tests. Tier 1+."
---

## Purpose

Decide which claims become **behaviour**. A principle is stronger than a claim: a reusable
rule that drives the subagent. Keeping claims (source knowledge) separate from principles
(operational rules) prevents profile bloat and overfitting. Output `principles/principles.yaml`,
validated by `validate_principles.py`.

## Input

- `analysis/claims.jsonl` + `analysis/claim-importance-scores.yaml` (Step 2) — candidates.
- `evidence/evidence-records.yaml` (Step 3) — a claim may be promoted only if it has ≥1 record.
- `profile.yaml` `knowledge_partition.{skills,references}` and `tests/` — `operational_mapping` targets.

## Promotion criteria

Promote a claim only when **all** hold:
- high actionability + reusability + clear operational fit (mirror the keep/review/discard rule);
- ≥1 evidence record exists for it;
- its conditions/exceptions are known, or explicitly marked unknown.

Not every claim is promoted. Prefer fewer, load-bearing principles.

## Procedure

For each promoted principle write a `principles-v1` entry:
- `principle_id`, `statement` (the operational rule, not the raw claim),
- `derived_from_claims` (≥1, real claim IDs),
- `confidence` (high/medium/low) — **set it via the GRADE method (Step 16/K2), not by feel:** start
  from a baseline by source type (peer-reviewed/official/replicated → high; expert-book/essay/case-study
  → medium; anecdotal/secondary → low), then down-grade for risk-of-bias / inconsistency / conflict /
  indirectness and up-grade for replication. When you can, record the factors in an optional `grade`
  block (`source_type`, `downgrades[]`, `upgrades[]`); `validate_confidence_grade` then enforces
  `confidence == grade_confidence(grade).level` (run `python -m tools.subagent_factory.grade_confidence
  <source_type> [--down R] [--up R]` to compute it). If the factors grade to *insufficient*, **drop the
  principle (abstain)** rather than promote it as `low`.
- `applies_when` / `does_not_apply_when` (from the claims' conditions/exceptions),
- `operational_mapping`: `profile_rule` (bool), `skill` (∈ knowledge_partition.skills or null),
  `reference` (∈ knowledge_partition.references or null), `test_cases` (the behaviour-test IDs
  that exercise this principle — see the convention below).

### Test-ID convention (avoids an ordering trap)

Behaviour tests are authored **after** principles (author-subagent Step 7.7), so at promotion
time the IDs in `tests/` do not exist yet. `validate_principles` requires every `test_cases`
entry to resolve to a real `test_id` in `tests/`, and its guard is silently skipped while
`tests/` is still empty — so an invented ID passes at Step 6.5b but **FAILs the final Step 9
validate** once the test generator picks different IDs. To keep both `validate_principles`
(`test_cases ⊆ tests/`) and `validate_principle_test_coverage` satisfiable regardless of
authoring order, use the deterministic convention:

- set `test_cases: [PB-<principle_id>]` (e.g. principle `P03` → `[PB-P03]`), and have
  `principle-test-generation` emit a behaviour test whose `test_id` is exactly `PB-<principle_id>`;
- you may additionally list other **already-existing** test IDs that exercise the principle
  (e.g. a golden-test `GT-00n`), but never invent an ID that no generated test will carry;
- if this run is not also generating the behaviour tests, leave `test_cases` empty (it is an
  optional field) rather than guessing.

## Output

`principles/principles.yaml` (schema `principles-v1`). Must pass
`python -m tools.subagent_factory.validate_principles` — every principle traces to claims that
each have evidence, and every `operational_mapping` target resolves.

## Caveats

- Single-source promotion only. **Cross-source** principle merge / alias clustering / conflict
  graph is **Step 7** (deferred).
- The validator enforces *traceability*, not *quality*; apply the promotion criteria yourself.

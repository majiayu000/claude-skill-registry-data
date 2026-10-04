---
name: claim-extraction
description: "Extract atomic, typed, source-anchored claims from ingested sources into analysis/claims.jsonl (claims-v1). Two-stage: LLM check-worthiness detection, then JSON decomposition + classification. Tier 1+."
---

## Purpose

Replace vague "candidate units" with atomic, traceable claims — the unit that importance
ranking, evidence records, and principles build on. Output `analysis/claims.jsonl`, validated
by `validate_claims.py`.

## Input

- `interrogation-records.yaml` (Q1–Q18 + `evidence_gaps`) — what the source is about.
- `sources/markdown/<id>.md` — the source text (`source_text.load_source_texts`).
- `sources/anchors/<id>.anchors.jsonl` — real anchor IDs for `source_anchors`.

## Procedure (two-stage; research-grounded)

1. **Stage 1 — detection.** Identify check-worthy sentences/passages (claims, not background).
   (The research recommends a fine-tuned XLM-R encoder for scale; v1 uses an LLM
   check-worthiness pass — no model dependency. Revisit if recall is poor on long sources.)
2. **Stage 2 — decomposition.** For each, emit one `claims-v1` object using **delayed-structure**
   (reason first, then JSON). Classify:
   - `component_class`: major_claim / claim / premise / non_argumentative (Stab & Gurevych).
   - `claim_type`: fact / value / policy (+ `causal` only after in-domain validation).
   - `premise_type` (premises only): the 6 AAE-FG sub-types.
   - `evidence_type` (on linked evidence): the 5 AQE types.
   - `stance`: support / contest / no_relation (3-way, not binary).
   - `az_zone`: Teufel zones — **scientific documents only**, else null.
   - `certainty`: asserted / hedged / speculative (BioScope cue model).
   - `condition` / `exception`: nullable. Populate `exception` on an undercutting pattern
     (surface cues: `unless`, `except when`, `only if`, `provided that`, `assuming`,
     `subject to`, `absent`, `if and only if`, `in the absence of`).
   - `source_anchors`: real anchor IDs; `support_granularity`: section / page / heading.
3. **Separate passes, not joint 4-tuple** (full 4-tuple F1=21.39): one pass for
   claim+type+premise; a later pass (Step 3) for evidence linking.
4. **Coverage gate** (skill responsibility, not the validator): estimate the ratio of extracted
   claims to claimable sentences; if **< 0.50**, re-extract (recall is a model-capability ceiling).
5. **Type sanity** (advisory): a causal connective (`therefore/because`) in a `fact` claim, or
   `if/unless` phrasing with an empty `condition`, signals a mis-type — fix before writing.

## Output

- `analysis/claims.jsonl` (one `claims-v1` object per line), scored with `score_extracted_units`
  (same 9 dims) → `analysis/claim-importance-scores.yaml`. Must pass `validate_claims`.
- `evidence/evidence-records.yaml` (`evidence-records-v1`): ≥1 record per high-value claim
  binding it to source (type / strength / `support_level`; `quote_allowed` false for restricted
  sources). Must pass `validate_evidence_records`. This is the Step-3 evidence layer, authored
  together with claims since both come from the same source analysis.

## Caveats

- `condition`/`exception` is **surface-cue heuristic** — no NLP dataset exists (GAP-4); treat as
  best-effort, not validated.
- `az_zone` taxonomy is from a secondary survey — schema-grade, not classifier-grade.
- LLM extraction can hallucinate; the deterministic validator + Step-1/3 faithfulness catch
  over-reach, not extraction alone.

---
name: ev-pipeline
description: >
  Top-level orchestrator for the Gaia Skill Tree evidence verification pipeline. Run this when you want to do a full evidence pass — collecting raw sources, verifying live GitHub star counts, running Phase 2B benchmark-source verification, adversarially auditing for quality/formatting issues, and checking that every URL is reachable — all in one coordinated sequence. Trigger phrases: "run the evidence pipeline", "full evidence pass", "verify evidence", "evidence verification pipeline", "run ev-pipeline", "check all evidence", "audit the data lake", "evidence quality sweep", "refresh evidence", "validate evidence sources". Also aliased as /evidence-verification-pipeline. Use the individual sub-skills (ev-collection, ev-star-verification, ev-adversarial-audit, ev-link-validation) only when you need to re-run one phase in isolation; for end-to-end work, always start here.
---

# Evidence Verification Pipeline (ev-pipeline)

Orchestrates the evidence verification phases that take raw evidence from collected to audited and link-checked before ingestion. It operates on the `evidence/` data lake only and does not mutate registry files.

## Type-First Evidence Lake Contract (#1148)

The evidence lake is **type-first**. The primary working set for every phase is `evidence/by-type/<canonical-evidence-type>.md` using the canonical evidence vocabulary: `repo-own`, `github-stars-own`, `social-signal`, `benchmark-result`, `arxiv`, `peer-review`, `proxy-containment`, `verifier-attestation`, `fusion-recipe`, and `self-attestation`.

Legacy `evidence/tier_*.md` files may still exist as coexistence artifacts for older tooling, but they are **not** the semantic routing key. New collection, audit, compile, and handoff work must route by evidence type.

## Multi-Target Peer-Review Source Packets (#1418)

When one legitimate peer-review URL truly reviews multiple named skills, materialize a **scratch** peer-review partition instead of duplicating registry rows or hand-writing generated lake files:

```bash
python evidence/scripts/peer_review_source_packets.py \
  --manifest /path/to/manifest.json \
  --by-type-dir /tmp/ev1418/by-type
```

The packet contract is `peer-review`-only, expands to one temporary row per reviewed skill in `peer-review.md`, and may repeat the same URL once per target skill when the source genuinely covers each one. Reject strength/scoring fields anywhere in the packet (`trustNumber`, `grade`, `class`, `tier`, `level`, `stars`, `rank`). Do not commit scratch manifests or generated partitions without human approval.

```mermaid
graph TD
    Phase0[Phase 0: ev-discovery (skippable)] -->|Append discovered rows| A
    A[Phase 1: ev-collection] -->|Materialize + compile by evidence type| B[Phase 2: ev-star-verification]
    B -->|Verify live stars, no rank repartition| B2[Phase 2B: ev-benchmark-verification]
    B2 -->|Classify benchmark sources + candidate manifests| C[Phase 3: ev-adversarial-audit]
    C -->|Audit by-type files| D[Phase 4: ev-link-validation]
    D -->|Validate URL health| E[Source Report & Ingestion Handoff]
```

## Phase Responsibilities

- **Phase 0 — `ev-discovery` (skippable):** searches for new Stage-2 evidence on declared need and appends discovered rows into source inputs for Phase 1. It does not score or rank evidence.
- **Phase 1 — `ev-collection`:** materializes primary partitions under `evidence/by-type/` and compiles `evidence/unified_evidence_lake.md` from those by-type files. It may emit `tier_*.md` only as coexistence output.
- **Phase 2 — `ev-star-verification`:** verifies live GitHub stargazer counts and records stale/inflated metrics. It must not repartition the lake by rank; by-type partitions remain primary.
- **Phase 2B — `ev-benchmark-verification`:** verifies `benchmark-result` rows and optional candidate manifests against `registry/benchmark-sources.json`. It classifies benchmark lanes (`verified` = CI/verifier reproduced, 2.0x; `reported` = public claim or mirrored evidence accepted by the human gate, 1.0x; `rejected` = blacklist/no scoring, 0x), catalog status, unknown benchmarkIds, missing verified-lane reproducibility fields, and malformed percentiles without mutating the registry. Legacy aliases normalize safely: `ci-reproduced`/`verifier-attested` → `verified`, `mirrored` → `reported`, and `pending`/`candidate`/`retired`/`unknown` → `rejected`. `appliesToGenericSkillRefs` says which generic capability buckets a benchmark evaluates; it does not create a named-skill score.
- **Phase 3 — `ev-adversarial-audit`:** audits by-type files for bad URLs, subjective wording, proxy/source mismatches, stale notes, benchmark catalog misuse/vendor-claim leakage, and star/evidence inconsistencies.
- **Phase 4 — `ev-link-validation`:** validates URL health. `validate_sources.py` remains a temporary coexistence URL-health shim while the lake is type-first.

## Additive loop — no green gate

Evidence is additive, not pass/fail. New rows can arrive from Stage 1 minimum rows (`github-stars-own`, `repo-own`, `self-attestation`) or from skippable Phase 0 discovery (`benchmark-result`, `arxiv`, `peer-review`, richer `social-signal`). Benchmark rows add a dedicated human gate: after Phase 2B, Phase 3, and Phase 4, humans must approve a candidate as reported benchmark evidence or reject/blacklist it; verified rows require CI/verifier reproducibility. Machines classify, humans approve or reject. A benchmark catalog entry may name generic refs via `appliesToGenericSkillRefs`, but it creates no named-skill score and no Trust Magnitude contribution until a named `benchmark-result` row lands in a scoring lane. Trust Magnitude and rank are recomputed at appraisal time.

## Outputs and Handoff

Generated evidence outputs are review artifacts, not registry mutation. Do not commit generated `evidence/by-type/**`, `evidence/tier_*.md`, source reports, validation reports, unified lake files, seeds, or collector rows without a human gate. For L4-approved intake, pass a reviewed manifest of live, correctly scoped rows to `/gaia-ingest-batch`.

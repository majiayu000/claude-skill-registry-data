---
name: seo-aeo
description: Audit supplied pages, documents, or content sets for direct-answer completeness, question and intent coverage, clarity, extractability, claim support, and visible-content consistency against a pinned AI-search Research Pack. Use for AEO, answer-engine optimization, answer readiness, answer extraction, featured-answer preparation, or requests asking whether content clearly and supportably answers researched questions. Do not use for generative-engine mention/citation strategy, live research, content rewriting, schema generation, technical SEO implementation, or visibility monitoring.
---

# SEO AEO

Produce an evidence-linked AEO Optimization Brief from immutable inputs. Audit answer readiness; do not implement the remedies.

## Required inputs

- Require a contract-valid `research-pack.json` from `ai-search-research`.
- Require a dated, bundle-relative capture plus a hash-pinned target-metadata file containing target ID, type, locale, supplied source URL, capture reference, capture SHA-256, and capture time. Never trust Brief fields without matching metadata, invent a canonical URL, or audit an uncaptured, unpinned, or silently refreshed page.
- Record inaccessible, incomplete, stale, or locale-mismatched inputs as limitations. Do not infer missing content.
- Read [audit-protocol.md](references/audit-protocol.md) before scoring findings or recommending a handoff.

## Procedure

1. Verify the Research Pack identity, schema version, hash, declared locales, queries, evidence, ground truth, and gaps.
2. Verify every target capture, capture time, target type, and locale. Stop with an explicit gap if a required capture is missing.
3. Audit only these AEO dimensions:
   - direct-answer completeness;
   - question, intent, audience, and journey-stage coverage;
   - answer clarity and self-contained meaning;
   - claim-to-evidence support and freshness;
   - entity and terminology consistency within the answer;
   - visible-content consistency with any supplied structured-data representation.
4. Verify every Brief target field against the hash-pinned metadata file. Record target observations as intra-brief `direct_observation` evidence pinned to the target capture and metadata-supplied source URL. Do not invent a URL or republish Research Pack source records as audit evidence. A target finding must cite that observation; research-dependent conclusions must also cite scope-matched Research Pack evidence.
5. Bind each finding to resolved Research Pack query IDs. Keep the finding locale equal to its target locale and keep engine/surface scope within those queries' applicability.
6. Classify each observation as `confirmed`, `vendor-recommended`, `experimental`, or `speculative`. A finding or confidence level cannot exceed its weakest necessary premise. Speculative evidence never supports an implementation recommendation. Experimental-only support belongs in `experiments`; route unsupported premises to limitations, declined claims, or research backlog.
7. Reject unsupported formulas, word-count thresholds, guaranteed placements, universal crawler claims, and mandatory `llms.txt` claims into `declined_claims`.
8. Create an `optimization-brief.json` with `optimization_domain: "aeo"` and `producer_skill: "seo-aeo"`. Pin every external evidence reference to the immutable Research Pack hash. Use `SELF` only for an intra-brief `audit_evidence` reference. Keep stable IDs unique and never copy Research Pack evidence into `audit_evidence`.
9. Give every recommendation its own evidence references, desired outcome, confidence, verification method, and exactly one candidate implementation owner. Its evidence must overlap every linked finding and remain scope-compatible. A Brief does not approve a change.
10. Set `created_at` after all target captures and audit observations. Validate Research Pack uniqueness, chronology, capture hashes, query applicability, evidence resolution and scope, and the Optimization Brief contract before delivery.

## Ownership boundaries

Route implementation planning first; never perform or approve implementation inside this skill:

- `seo-action-plan`: evidence-linked ownership, approval gate, verification, and rollback for a validated Brief.

- `seo-content`: substantive wording, editorial quality, or answer rewrite.
- `seo-schema`: structured-data choice, generation, syntax, eligibility, or validation.
- `seo-technical`: crawlability, rendering, indexing, directives, performance, or transport controls.
- `seo-hreflang`: locale and regional mapping.
- `optimise-seo`: broader integrated page optimization outside the AEO delta.

Do not perform GEO mention/citation strategy; route that to `seo-geo`. Do not measure live visibility or drift; route that to `ai-visibility-monitor`. Do not create missing research; route that to `ai-search-research`.

## Severity and review

- `critical`: the audit or handoff would be materially false, unsafe, or unusable without correction.
- `important`: a required answer, evidence link, locale, or owner handoff is missing or misleading.
- `minor`: non-blocking clarity or maintainability improvement; record it in backlog.

Close all critical and important audit findings. Backlog minor findings.

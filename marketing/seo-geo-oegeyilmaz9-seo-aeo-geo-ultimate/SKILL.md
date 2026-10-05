---
name: seo-geo
description: Audit supplied pages, entity records, source captures, and citation observations for generative-engine entity consistency, evidence traceability, citation suitability, cited-source alignment, and documented engine controls against a pinned AI-search Research Pack. Use for GEO, generative-engine optimization, AI citations, brand or entity mentions in generative answers, source alignment, or documented AI-search control audits. Do not use for direct-answer formatting or extractability, live research, content rewriting, schema generation, technical SEO implementation, longitudinal visibility measurement, or guaranteed placement claims.
---

# SEO GEO

Produce an evidence-linked GEO Optimization Brief from immutable inputs. Audit generative-engine entity, source, and citation readiness; do not implement remedies or predict placement.

## Required inputs

- Require a contract-valid `research-pack.json` from `ai-search-research`.
- Require hash-pinned target metadata and captures. For web targets, use only the metadata-supplied URL.
- Require dated raw observations for any claim about an engine answer, mention, citation, or cited source. Record missing or inaccessible observations as limitations.
- Read [geo-audit-protocol.md](references/geo-audit-protocol.md) before classifying a finding or recommendation.

## Procedure

1. Validate the complete Research Pack contract and semantic provenance: identity, version, hash, stable-ID uniqueness, raw references, locales, queries, entity integrity, evidence, observations, ground truth, freshness, and gaps.
2. Validate each target metadata file, metadata hash, capture hash, target URL, locale, capture time, and chronology.
3. Audit only these GEO dimensions:
   - `entity_consistency`: names, aliases, attributes, disambiguation, and target/source agreement;
   - `evidence_traceability`: material assertions resolve to current, scope-compatible evidence;
   - `citation_suitability`: supplied sources clearly support the relevant entity/fact without claiming an engine will select them;
   - `source_credibility`: supplied source identity, ownership, expertise, independence, update state, and primary/secondary role are explicit without relying on a proprietary authority score;
   - `claim_source_entailment`: cited or candidate text actually supports the bounded answer claim, with partial, conflicting, and unverifiable support preserved;
   - `conflict_resolution`: conflicting current sources remain visible and the applicable system of record, scope, and resolution owner are named;
   - `cited_source_alignment`: a metadata-bound `content_set` target under `raw/observations/` contains the exact raw-observation fields defined in the protocol, and its dated engine/surface/locale answer plus cited URLs agree with referenced Research Pack sources;
   - `documented_engine_control`: a current vendor document or applicable standard supports the scoped control.
4. Bind every finding to resolved Research Pack query IDs, one target, that target's locale, and engine/surface pairs within query applicability.
5. Create capture-tied `direct_observation` audit evidence. Never copy Research Pack evidence or invent a URL, answer, citation, mention, crawler behavior, control, or engine result.
6. Classify evidence as `confirmed`, `vendor-recommended`, `experimental`, or `speculative`. A recommendation also inherits the weakest classification of every linked finding; it cannot hide a weak finding by repeating only stronger references. Speculative or experimental findings never support implementation; experimental-only support belongs in `experiments`.
7. Decline fixed scores, universal ranking factors, fixed passage formulas, mandatory `llms.txt`, blanket crawler directives, platform guarantees, and correlation presented as causation.
8. Create `optimization-brief.json` with `optimization_domain: "geo"` and `producer_skill: "seo-geo"`. Keep stable IDs unique, external artifacts hash-pinned, and audit evidence metadata-bound.
9. Give every recommendation resolved evidence overlapping each linked finding, a desired outcome, confidence, verification method, and exactly one candidate implementation owner. A Brief does not approve a change.
10. Validate the Research Pack, metadata/capture provenance, evidence resolution and scope, GEO dimension ownership, documented-control evidence, chronology, and canonical Optimization Brief contract.

## Ownership boundaries

- Route direct-answer completeness, clarity, intent coverage, and extractability to `seo-aeo`.
- Route live AI-search research and missing source collection to `ai-search-research`.
- Route longitudinal mention, citation, accuracy, referral, or drift measurement to `ai-visibility-monitor`.
- Route backlink/source-landscape discovery to `seo-authority` and site-owned source structure to `seo-architecture`.
- Route a validated Brief to `seo-action-plan` before implementation, then to the exact approved content, schema, technical, locale, commerce, local, video, news, agentic, architecture, authority, performance, or broad implementation owner.

Do not create a universal GEO score, treat a correlation as a control, recommend off-page manipulation, or claim a change will cause mentions or citations.

## Severity

- `critical`: the audit or handoff would be materially false, unsafe, or unusable without correction.
- `important`: a required entity, source, evidence link, scope, or owner handoff is missing or misleading.
- `minor`: non-blocking clarity or maintainability improvement; record it in backlog.

Close critical and important audit findings. Backlog minor findings.

---
name: hypothesis-full-review
description: Run the full literature-grounded review for a hypothesis.
---

# hypothesis-full-review

Goal:

- Run the full literature-grounded review for a hypothesis.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `hypotheses/<id>/HYPOTHESIS.json`
- `literature/queries/<query_id>/EVIDENCE_BUNDLE.json` produced by `tools.search_literature(...)`
- optional run-level review guidance from `meta/INSIGHTS_FROM_REVIEWS.json`

Outputs:

- `hypotheses/<id>/REVIEW/FULL_REVIEW.json`
- `literature/queries/<query_id>/*` search bridge artifacts when a new evidence query is required

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Open `skills/shared-references/literature-search-contract.md`.
- Open `skills/shared-references/codex-reviewer-routing.md` before using any optional Codex reviewer subagent route.
- Read `packages/agent_contracts/literature.py` before building or consuming search bridge artifacts.
- Read `research_plan/RESEARCH_PLAN.json`.
- Use `research_goal` as the review anchor.
- Use `preferences` as the detailed quality criteria.
- Use `constraints` as non-negotiable boundaries.
- Read `hypotheses/<id>/HYPOTHESIS.json`.
- If meta-review guidance exists, use it to calibrate recurring failure patterns without replacing local evidence.

Execution Prompt Contract:

- System Intent:
  - You are performing a thorough literature-grounded review of one hypothesis.
- Required Reasoning Focus:
  - Use `tools.search_literature(run_dir, request)` to gather the minimum external evidence needed to evaluate the hypothesis claims unless an existing evidence bundle already covers the same query.
  - If Codex reviewer subagents are available and explicitly useful for the review, they may inspect the same canonical artifacts, but the main thread must still validate and persist the canonical `FULL_REVIEW.json`.
  - If subagents are unavailable, execute the same review contract in the main thread and record `reviewerRoute = local_main_thread` when a reviewer route trace is written.
  - Treat the returned `EvidenceBundleContract` as the only formal external literature input.
  - Read `retrieval_metadata.status` before writing evidence-backed judgments.
  - If `retrieval_metadata.status` is `partial`, preserve the partial-source limitation in the affected review points instead of describing the review as comprehensive literature coverage.
  - Judge each preference axis with evidence-backed reasoning.
  - Judge each constraint with evidence-backed reasoning.
  - Be rigorous but fair; separate refinable issues from fundamental problems.
- Do Not Do:
  - Do not quote large parts of the hypothesis back verbatim.
  - Do not emit raw literature notes without turning them into structured review points.
  - Do not treat unsupported intuition as if it were grounded evidence.
  - Do not invent papers, DOIs, arXiv IDs, venues, citation counts, abstracts, or literature claims not present in the evidence bundle.
  - Do not use model memory as a substitute for search bridge artifacts.
  - Do not let a reviewer subagent write deterministic mechanics artifacts or bypass schema validation.
- Review Quality Floor:
  - A `status = completed` full review must include concrete `preferences` or `constraints` that name hypothesis-specific mechanisms, materials, reaction conditions, feasibility limits, evidence gaps, or experimental tests.
  - If external literature support is claimed, `retrieval_results`, `evidence_bundle_ids`, and `literature_query_ids` must remain traceable to search bridge artifacts.
  - If no external evidence can be retrieved, write specific non-literature constraints from the hypothesis and research plan; do not claim literature grounding.
  - Do not use placeholder review phrases such as `Viable evolved hypothesis`, `Refined from parent`, `Must outperform parent`, or `Benchmark against parent` as substantive review content.
- Output Shape:
  - Produce a structured review with the exact field shape of `FullReviewContract` from `packages/agent_contracts/review.py`:
    - `preferences`
    - `constraints`
  - Each point should be short, evidence-oriented, and useful to downstream refinement.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, `skills/shared-references/literature-search-contract.md`, and `skills/shared-references/codex-reviewer-routing.md`, then read `packages/agent_contracts/review.py` and `packages/agent_contracts/literature.py` before writing `FULL_REVIEW.json`, reviewer traces, or consuming search bridge artifacts.
2. Read the research plan and current hypothesis.
3. Build a focused `SearchRequestContract` for the hypothesis claims and call `tools.search_literature(run_dir, request)` unless a matching evidence bundle already exists.
4. If `retrieval_metadata.status` is `blocked`, write only a degraded review that explicitly says external evidence retrieval was blocked; do not claim literature grounding.
5. If `retrieval_metadata.status` is `partial`, continue only when each evidence-dependent critique preserves that limitation and avoids comprehensive-coverage language.
6. Assess the hypothesis against each preference axis using the evidence bundle and the research plan.
7. Assess the hypothesis against each constraint using the evidence bundle and the research plan.
8. Write `hypotheses/<id>/REVIEW/FULL_REVIEW.json`.
9. Validate before declaring completion.

Artifact Rules:

- `FULL_REVIEW.json` must remain structured and concise enough for downstream summarization.
- External evidence should be distilled into review points rather than dumped as an appendix inside the review artifact.
- Any `retrieval_results` entries must be derived from `literature/queries/<query_id>/EVIDENCE_BUNDLE.json`.
- Partial evidence bundles must remain visible in the review rationale; do not upgrade `partial` retrieval into full literature support.

Completion Rule:

- This skill is complete only when `FULL_REVIEW.json` exists, any external evidence claims are traceable to a search bridge evidence bundle, and the artifact is valid for downstream synthesis.

---
name: hypothesis-deep-verification
description: Run the assumption decomposition and deep verification review for a hypothesis.
---

# hypothesis-deep-verification

Goal:

- Run the assumption decomposition and deep verification review for a hypothesis.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `hypotheses/<id>/HYPOTHESIS.json`
- `literature/queries/<query_id>/EVIDENCE_BUNDLE.json` as an `EvidenceBundleContract` when external evidence is needed to judge a core assumption
- optional prior review artifacts for calibration

Outputs:

- `hypotheses/<id>/REVIEW/DEEP_VERIFICATION.json`
- `literature/queries/<query_id>/*` search bridge artifacts when a new evidence query is required

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Open `skills/shared-references/literature-search-contract.md`.
- Open `skills/shared-references/codex-reviewer-routing.md` before using any optional Codex reviewer subagent route.
- Read `packages/agent_contracts/literature.py` before building or consuming search bridge artifacts.
- Read `research_plan/RESEARCH_PLAN.json` for the active goal and boundaries.
- Read `hypotheses/<id>/HYPOTHESIS.json`.
- If previous review artifacts exist, use them to focus decomposition on already-suspect links, but still perform an independent structural check.

Execution Prompt Contract:

- System Intent:
  - You are the structural verification layer for one hypothesis.
- Required Reasoning Focus:
  - Decompose the hypothesis into core assumptions.
  - Break each assumption into independently judgeable sub-assumptions where useful.
  - For assumptions that depend on external literature support, call `tools.search_literature(run_dir, request)` or consume an existing matching evidence bundle before marking the link as supported.
  - If Codex reviewer subagents are available and explicitly useful for structural verification, they may inspect the same canonical artifacts, but the main thread must still validate and persist the canonical `DEEP_VERIFICATION.json`.
  - If subagents are unavailable, execute the same verification contract in the main thread and record `reviewerRoute = local_main_thread` when a reviewer route trace is written.
  - Read `retrieval_metadata.status` before marking any evidence-dependent assumption as externally supported.
  - Mark which links appear well-supported by the evidence bundle, speculative but plausible, unsupported because retrieval was blocked, or likely incorrect.
  - If `retrieval_metadata.status` is `partial`, mark externally supported links as limited by partial retrieval rather than fully literature-confirmed.
  - Surface flaws in reasoning chains, hidden assumptions, or logically weak transitions.
- Do Not Do:
  - Do not collapse the whole hypothesis into one coarse verdict.
  - Do not invent additional research goals or evaluation criteria.
  - Do not produce deep verification as unstructured prose.
  - Do not invent papers, DOIs, arXiv IDs, venues, citation counts, abstracts, or literature claims not present in the evidence bundle.
  - Do not use model memory as a substitute for search bridge artifacts.
  - Do not let a reviewer subagent write deterministic mechanics artifacts or bypass schema validation.
- Review Quality Floor:
  - A `status = completed` deep verification review must include at least one concrete assumption with a non-empty correctness rationale.
  - Assumptions must decompose the hypothesis mechanism or validation path; do not write generic entries such as `mechanism is plausible` or `needs validation`.
  - Do not use placeholder verification phrases such as `Viable evolved hypothesis`, `Refined from parent`, or `validated by future experiments` as substantive review content.
  - If an assumption depends on literature evidence, preserve the linked evidence limitation or retrieval status rather than inventing support.
- Output Shape:
  - Produce the exact `DeepVerificationReviewContract` from `packages/agent_contracts/review.py`.
  - Keep statements and correctness rationales concise.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, `skills/shared-references/literature-search-contract.md`, and `skills/shared-references/codex-reviewer-routing.md`, then read `packages/agent_contracts/review.py` and `packages/agent_contracts/literature.py` before writing `DEEP_VERIFICATION.json`, reviewer traces, or consuming search bridge artifacts.
2. Read the research plan and hypothesis.
3. Extract the core assumptions behind the mechanism or validation path.
4. For assumptions whose correctness depends on external literature, build a focused `SearchRequestContract` and call `tools.search_literature(run_dir, request)` unless a matching evidence bundle already exists.
5. If retrieval is `blocked`, preserve that uncertainty in the affected assumption correctness rationales instead of claiming external support.
6. If retrieval is `partial`, preserve that limitation in the affected assumption correctness rationales instead of claiming comprehensive external support.
7. Decompose assumptions where necessary.
8. Evaluate each assumption or sub-assumption.
9. Write `hypotheses/<id>/REVIEW/DEEP_VERIFICATION.json`.
10. Validate before declaring completion.

Artifact Rules:

- `DEEP_VERIFICATION.json` must remain machine-consumable and structurally nested.
- The review should identify whether a flawed link is core or peripheral whenever possible.
- External support judgments must be traceable to `literature/queries/<query_id>/EVIDENCE_BUNDLE.json` when they depend on literature.
- `partial` and `blocked` retrieval states must remain explicit in correctness rationales; do not convert them into full evidence support.

Completion Rule:

- This skill is complete only when `DEEP_VERIFICATION.json` exists, external support judgments are traceable to search bridge artifacts when used, and the artifact is valid for downstream synthesis.

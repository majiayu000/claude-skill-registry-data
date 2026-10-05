---
name: hypothesis-generate-literature
description: Generate exactly one literature-grounded hypothesis candidate for the active round.
---

# hypothesis-generate-literature

Goal:

- Generate exactly one literature-grounded hypothesis candidate for the active round.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `state/STRATEGY_PLAN.json`
- `literature/queries/<query_id>/EVIDENCE_BUNDLE.json` produced by `tools.search_literature(...)`
- optional parent hypothesis and review artifacts when the round is part of an evolution continuation

Outputs:

- `hypotheses/<id>/HYPOTHESIS.json`
- `hypotheses/<id>/HYPOTHESIS.md`
- `hypotheses/<id>/ORIGIN.json`
- `literature/queries/<query_id>/*` search bridge artifacts for the evidence query used by this generation

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Open `skills/shared-references/literature-search-contract.md`.
- Read `packages/agent_contracts/literature.py` before building or consuming any search bridge request or evidence bundle.
- Read `research_plan/RESEARCH_PLAN.json`.
- Treat `research_goal` as the task anchor.
- Treat `preferences` as the quality axes that the hypothesis should optimize for.
- Treat `constraints` as hard boundaries that the hypothesis and experiment design must satisfy.
- Read `state/STRATEGY_PLAN.json` and confirm that the current round allows `literature_exploration_generation`.
- If the round is parented, read the selected parent hypothesis and its latest review summary before generating a child. Improve the known weaknesses instead of paraphrasing the parent.

Execution Prompt Contract:

- System Intent:
  - You are generating one scientifically grounded candidate hypothesis from literature exploration.
- Required Reasoning Focus:
  - Before generating the candidate, call `tools.search_literature(run_dir, request)` with `consumer="hypothesis-generate-literature"` and use the returned `EvidenceBundleContract` as the formal external evidence input.
  - Use relevant prior work, gaps, contradictions, or unexplored connections from the evidence bundle to motivate the candidate.
  - Produce a specific falsifiable claim with a mechanism and a concrete experiment path.
  - Make the mechanism explicit enough that another reviewer can critique it step by step.
  - When novelty depends on a conjectural link, keep that link explicit rather than hiding it in vague wording.
- Do Not Do:
  - Do not merely restate established literature.
  - Do not emit multiple final candidates in one round.
  - Do not ignore explicit constraints from the research plan.
  - Do not write an informal summary in place of the canonical hypothesis artifact.
  - Do not invent papers, DOIs, arXiv IDs, venues, citation counts, abstracts, or literature claims not present in the evidence bundle.
  - Do not treat model memory as a substitute for `tools.search_literature(...)`.
- Output Shape:
  - Wrap the final result into the canonical shared `HypothesisContract`.
  - `origin.content.statement`: 2-3 sentences maximum.
  - `origin.content.mechanism`: 2-3 sentences maximum.
  - `origin.content.experimental_design`: one concise multiline string with 3-6 numbered steps.
  - `origin.content.experimental_design` must remain one string field containing embedded line breaks; do not emit it as a list, array, or nested object.
  - `origin.content.summary`: one concise sentence.
  - `origin.content.category`: 1-5 words.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, `skills/shared-references/literature-search-contract.md`, then read `packages/agent_contracts/hypothesis.py` and `packages/agent_contracts/literature.py` before writing `hypotheses/<id>/HYPOTHESIS.json` or consuming search bridge artifacts.
2. Read the required artifacts.
3. Confirm that this round is allowed to use literature exploration.
4. Build a focused `SearchRequestContract` for the active research goal and call `tools.search_literature(run_dir, request)`.
5. Read the returned `EvidenceBundleContract`. If `retrieval_metadata.status` is `blocked`, stop or return a degraded state; do not write a literature-grounded hypothesis.
6. Identify one literature-grounded gap or underexplored mechanism from the evidence bundle that can answer the active research goal.
7. Generate exactly one candidate hypothesis for this round.
8. Wrap the result into the canonical `HypothesisContract`. Any `origin.retrieval_results` entries must be derived from the evidence bundle rather than invented in prompt text.
9. Write `hypotheses/<id>/HYPOTHESIS.json`, `hypotheses/<id>/HYPOTHESIS.md`, and `hypotheses/<id>/ORIGIN.json`.
10. Validate the emitted artifacts before declaring success.

Artifact Rules:

- `hypotheses/<id>/HYPOTHESIS.json` is the authoritative artifact and must serialize the canonical shared contract.
- `ORIGIN.json` may mirror the generation payload and grounding notes, but it does not replace the canonical hypothesis artifact.
- Formal external evidence must be traceable to `literature/queries/<query_id>/EVIDENCE_BUNDLE.json`.
- Because `origin.strategy` is `literature_exploration_generation`, the canonical hypothesis origin must include non-empty `retrieval_results`, `evidence_bundle_ids`, and `literature_query_ids` derived from the returned evidence bundle; validation fails if these bridge linkages are omitted or point to unknown artifacts.
- Any literature search or evidence-gathering notes that are not in the canonical evidence bundle should live in the trace, not be mixed into the contract fields.

Completion Rule:

- This skill is complete only when exactly one new canonical hypothesis artifact has been written from a non-blocked evidence bundle and the emitted files validate for downstream review.

---
name: hypothesis-review-summary
description: Summarize the completed reviews for a hypothesis.
---

# hypothesis-review-summary

Goal:

- Summarize the completed reviews for a hypothesis.

Inputs:

- `hypotheses/<id>/HYPOTHESIS.json`
- completed review artifacts under `hypotheses/<id>/REVIEW/`

Outputs:

- `hypotheses/<id>/REVIEW/REVIEW_SUMMARY.json`

Context Loading:

- Read `hypotheses/<id>/HYPOTHESIS.json`.
- Read all completed review artifacts under `hypotheses/<id>/REVIEW/`.
- Focus on synthesizing the strongest strengths, weaknesses, and recommended next actions across those reviews.

Execution Prompt Contract:

- System Intent:
  - You are synthesizing the completed review stack into a compact downstream summary.
- Required Reasoning Focus:
  - Deduplicate repeated points across review stages.
  - Preserve the most important strengths, weaknesses, and action items.
  - Prefer high-signal synthesis over exhaustive restatement.
- Do Not Do:
  - Do not summarize reviews that do not exist.
  - Do not copy every review point verbatim.
  - Do not invent a new evaluation framework at summary time.
- Review Quality Floor:
  - A `status = completed` review summary must synthesize concrete findings from completed review stages.
  - Include the strongest actionable strength, weakness, or next-step implication when those appear in prior reviews.
  - Do not use placeholder summary phrases such as `Viable evolved hypothesis`, `Refined from parent`, `strong candidate`, or `needs validation` as substantive summary content.
- Output Shape:
  - Produce the exact `ReviewSummaryContract` from `packages/agent_contracts/review.py`.
  - Keep the summary as a compact list of downstream-usable points.
  - Each item in `summaries` must be a plain string, not an object with nested keys such as `review_stage`, `outcome`, or `summary`.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/review.py` and confirm the exact `ReviewSummaryContract` shape before writing `REVIEW_SUMMARY.json`.
2. Read the current hypothesis and all completed review artifacts.
3. Identify repeated themes and high-signal findings.
4. Synthesize them into a compact summary list.
5. Write `hypotheses/<id>/REVIEW/REVIEW_SUMMARY.json`.
6. Validate before declaring completion.

Artifact Rules:

- `REVIEW_SUMMARY.json` is a synthesis artifact, not a copy of all prior review text.
- The summary must remain self-contained enough for downstream generation or ranking stages to consume quickly.

Completion Rule:

- This skill is complete only when `REVIEW_SUMMARY.json` exists and is valid for downstream consumption.

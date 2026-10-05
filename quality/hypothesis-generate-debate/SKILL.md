---
name: hypothesis-generate-debate
description: Generate exactly one hypothesis candidate through a structured scientific debate.
---

# hypothesis-generate-debate

Goal:

- Generate exactly one hypothesis candidate through a structured scientific debate.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `state/STRATEGY_PLAN.json`
- optional parent hypothesis and review artifacts when the round is part of an evolution continuation

Outputs:

- `hypotheses/<id>/HYPOTHESIS.json`
- `hypotheses/<id>/HYPOTHESIS.md`
- `hypotheses/<id>/ORIGIN.json`
- debate transcript in the skill trace

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Treat `research_goal` as the debate objective.
- Treat `preferences` as the criteria for what counts as a strong hypothesis.
- Treat `constraints` as hard boundaries that cannot be violated in the final proposal.
- Read `state/STRATEGY_PLAN.json` and confirm that the current round allows `scientific_debates_generation`.
- If the round is parented, read the selected parent hypothesis and its latest review summary before opening debate. The debate should target unresolved weaknesses rather than restart from zero.

Execution Prompt Contract:

- System Intent:
  - You are running a short structured debate whose output is exactly one canonical hypothesis candidate.
- Required Reasoning Focus:
  - If this is an initial debate, start with 2-3 candidate directions, then converge quickly.
  - Every critique must identify a weakness and a constructive improvement.
  - After two or more substantial turns, prefer convergence over endless divergence.
  - The final candidate must have:
    - a specific mechanism
    - a falsifiable statement
    - a concrete experiment path
- Do Not Do:
  - Do not let the debate expand into an open-ended brainstorming transcript.
  - Do not keep multiple finalists.
  - Do not end the round without a single canonical extracted hypothesis.
- Output Shape:
  - Preserve the debate transcript in the trace.
  - Extract exactly one final candidate into the exact `HypothesisContract` from `packages/agent_contracts/hypothesis.py`.
  - `origin.content.statement`: 2-3 sentences maximum.
  - `origin.content.mechanism`: 2-3 sentences maximum.
  - `origin.content.experimental_design`: one concise multiline string with 3-6 numbered steps.
  - `origin.content.experimental_design` must remain one string field containing embedded line breaks; do not emit it as a list, array, or nested object.
  - `origin.content.summary`: one sentence.
  - `origin.content.category`: 1-5 words.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` and confirm the exact `HypothesisContract` shape before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Read the required artifacts.
3. Confirm that this round is allowed to use debate-based generation.
4. Run a short structured debate for the active goal, keeping a traceable transcript.
5. Converge to exactly one final candidate.
6. Extract the final candidate into the canonical `HypothesisContract`.
7. Write `hypotheses/<id>/HYPOTHESIS.json`, `hypotheses/<id>/HYPOTHESIS.md`, and `hypotheses/<id>/ORIGIN.json`.
8. Validate the emitted artifacts before declaring success.

Artifact Rules:

- The debate transcript belongs in the trace, not in place of the canonical hypothesis artifact.
- `ORIGIN.json` may describe debate provenance and evidence, but must not replace `HYPOTHESIS.json`.
- The final artifact must be consumable by downstream skills without reading the raw transcript.

Completion Rule:

- This skill is complete only when exactly one valid canonical hypothesis artifact has been extracted from the debate and persisted for downstream use.

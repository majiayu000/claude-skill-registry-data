---
name: hypothesis-generate-assumptions
description: Generate exactly one hypothesis candidate by enumerating and combining testable assumptions.
---

# hypothesis-generate-assumptions

Goal:

- Generate exactly one hypothesis candidate by enumerating and combining testable assumptions.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `state/STRATEGY_PLAN.json`
- optional parent hypothesis and review artifacts when the round is part of an evolution continuation

Outputs:

- `hypotheses/<id>/HYPOTHESIS.json`
- `hypotheses/<id>/HYPOTHESIS.md`
- `hypotheses/<id>/ORIGIN.json`

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Use `research_goal` as the objective that the assumption chain must explain or enable.
- Use `preferences` as quality criteria.
- Use `constraints` as hard boundaries.
- Read `state/STRATEGY_PLAN.json` and confirm that the current round allows `assumptions_identification_generation`.
- If the round is parented, read the selected parent hypothesis and its latest review summary before proposing a child. The new chain should address known weaknesses where possible.

Execution Prompt Contract:

- System Intent:
  - You are generating one candidate hypothesis by surfacing the smallest useful chain of testable assumptions.
- Required Reasoning Focus:
  - Identify 3-5 assumptions or fewer if a shorter chain is stronger.
  - Favor chains that are falsifiable, mechanistically informative, and non-trivial.
  - At least one link may be speculative, but it must remain testable and explicit.
  - Use the assumption chain to produce a full downstream hypothesis rather than stopping at the decomposition.
- Do Not Do:
  - Do not output multiple competing chains as final answers.
  - Do not hide speculative links behind broad claims.
  - Do not emit assumptions without turning them into a full canonical hypothesis artifact.
- Output Shape:
  - The result must contain the exact `HypothesisContract` from `packages/agent_contracts/hypothesis.py`.
  - If assumption structure is useful, keep it inside `origin`-level payloads or trace notes, not as a replacement for the canonical hypothesis.
  - `origin.content.statement`: 2-3 sentences maximum.
  - `origin.content.mechanism`: 2-3 sentences maximum.
  - `origin.content.experimental_design`: one concise multiline string with 3-6 numbered steps.
  - `origin.content.experimental_design` must remain one string field containing embedded line breaks; do not emit it as a list, array, or nested object.
  - `origin.content.summary`: one sentence.
  - `origin.content.category`: 1-5 words.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` and confirm the exact `HypothesisContract` shape before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Read the required artifacts.
3. Confirm that this round is allowed to use assumptions-driven generation.
4. Identify the smallest useful chain of testable assumptions for the active goal.
5. Synthesize the chain into exactly one candidate hypothesis.
6. Wrap the result into the canonical `HypothesisContract`.
7. Write `hypotheses/<id>/HYPOTHESIS.json`, `hypotheses/<id>/HYPOTHESIS.md`, and `hypotheses/<id>/ORIGIN.json`.
8. Validate the emitted artifacts before declaring success.

Artifact Rules:

- The canonical hypothesis artifact is mandatory.
- Any auxiliary assumption tree must be treated as support for `origin`, not as a substitute for `HYPOTHESIS.json`.
- The final hypothesis must remain understandable even if a downstream consumer only reads the canonical artifact.

Completion Rule:

- This skill is complete only when exactly one new valid canonical hypothesis artifact has been written for the current round.

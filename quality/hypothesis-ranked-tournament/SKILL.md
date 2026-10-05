---
name: hypothesis-ranked-tournament
description: Judge one ranked-tournament matchup between two top frontier hypotheses.
---

# hypothesis-ranked-tournament

Goal:

- Judge one ranked-tournament matchup between two top frontier hypotheses.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- two `hypotheses/<id>/HYPOTHESIS.json` artifacts with completed review bundles

Outputs:

- one `TournamentMatchContract` result for a ranked tournament

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/ranking.py` and confirm the exact `TournamentMatchContract` shape before emitting the ranked result.
- Read `research_plan/RESEARCH_PLAN.json`.
- Read both hypotheses and their review bundles.
- Confirm that the match strategy is `ranked_tournament`.

Execution Prompt Contract:

- System Intent:
  - You are running a deeper comparative judgment for two high-ranked hypotheses whose relative ordering matters.
- Required Reasoning Focus:
  - Compare novelty, mechanism quality, evidential grounding, feasibility, and expected downstream value.
  - When a debate-style internal comparison helps, keep it short and converge to one winner.
- Do Not Do:
  - Do not leave the match undecided.
  - Do not ignore review weaknesses that materially change the ordering.
- Output Shape:
  - Emit one `TournamentMatchContract`.
  - `match_strategy`: `ranked_tournament`
  - `winner_id`: one of the two hypothesis IDs
  - `reasoning`: concise but specific
  - `debate_turns`: optional short internal debate transcript when useful

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/ranking.py` before emitting the ranked match artifact.
2. Compare the two frontier hypotheses for ranked ordering.
3. Choose exactly one winner.
4. Emit one valid ranked-tournament match result.

Completion Rule:

- This skill is complete only when one valid ranked match result has been produced with a non-empty winner and reasoning.

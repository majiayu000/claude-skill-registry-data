---
name: hypothesis-placement-tournament
description: Judge one placement-tournament matchup between a candidate hypothesis and one opponent.
---

# hypothesis-placement-tournament

Goal:

- Judge one placement-tournament matchup between a candidate hypothesis and one opponent.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- two `hypotheses/<id>/HYPOTHESIS.json` artifacts with completed review bundles

Outputs:

- one `TournamentMatchContract` result for a placement tournament

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/ranking.py` and confirm the exact `TournamentMatchContract` shape before emitting the placement result.
- Read `research_plan/RESEARCH_PLAN.json`.
- Read both hypotheses and their review bundles.
- Confirm that the match strategy is `placement_tournament`.

Execution Prompt Contract:

- System Intent:
  - You are making one single-turn comparative judgment between two reviewed hypotheses.
- Required Reasoning Focus:
  - Compare explanatory power, mechanistic quality, feasibility, and testability against the active research goal.
  - Prefer the hypothesis that would be more valuable to keep in the frontier.
- Do Not Do:
  - Do not return a tie.
  - Do not ignore major review failures.
- Output Shape:
  - Emit one `TournamentMatchContract`.
  - `match_strategy`: `placement_tournament`
  - `winner_id`: one of the two hypothesis IDs
  - `reasoning`: concise but specific

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/ranking.py` before emitting the placement match artifact.
2. Compare the two reviewed hypotheses for frontier placement.
3. Choose exactly one winner.
4. Emit one valid placement-tournament match result.

Completion Rule:

- This skill is complete only when one valid placement match result has been produced with a non-empty winner and reasoning.

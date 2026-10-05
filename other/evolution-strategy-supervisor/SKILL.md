---
name: evolution-strategy-supervisor
description: Choose exactly one concrete evolution strategy for the active evolution round.
---

# evolution-strategy-supervisor

Goal:

- Choose exactly one concrete evolution strategy for the active evolution round.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `state/STRATEGY_PLAN.json`
- selected parent `hypotheses/<id>/HYPOTHESIS.json` artifacts with completed review bundles

Outputs:

- one chosen evolution strategy for the round
- selection rationale in the skill trace

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Read `state/STRATEGY_PLAN.json`.
- Confirm that `next_action` is `continue_evolution`.
- Read every parent hypothesis listed in `signals.selected_parent_ids`.
- Read the latest review findings for those parent hypotheses.

Execution Prompt Contract:

- System Intent:
  - You are the round-level supervisor that chooses one evolution strategy from the currently allowed bundle.
- Required Reasoning Focus:
  - Respect `signals.selection_strategy`.
  - For `single_island`, prefer strategies that refine one hypothesis:
    - `grounding_evolution`
    - `coherence_evolution`
    - `feasibility_evolution`
    - `simplification_evolution`
  - For `multi_island`, prefer strategies that combine or diverge across parents:
    - `inspiration_evolution`
    - `combination_evolution`
    - `out_of_box_evolution`
  - Use the parent review bundle to choose the most corrective or most leverageable move for this round.
- Do Not Do:
  - Do not return multiple final strategies.
  - Do not choose a strategy outside `selected_evolution_strategies`.
  - Do not ignore the active parent set.
  - Do not append, rewrite, or enrich `state/STRATEGY_DECISIONS.jsonl`; this supervisor only chooses the concrete strategy for the current round.
  - Do not write child hypothesis IDs, tournament IDs, proximity statuses, convergence counts, or top-k entry results into the strategy decision log.

Execution Steps:

1. Read the required artifacts.
2. Confirm the parent set and island-selection mode for the current round.
3. Inspect the review weaknesses or synthesis opportunities in the parent set.
4. Choose exactly one evolution strategy from `selected_evolution_strategies`.
5. Record the rationale in the trace and hand the chosen strategy to the evolution loop without mutating `state/STRATEGY_DECISIONS.jsonl`.

Completion Rule:

- This skill is complete only when one concrete evolution strategy has been chosen for the active round and the choice is justified against the parent review context.

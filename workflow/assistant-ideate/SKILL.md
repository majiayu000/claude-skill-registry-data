---
name: assistant-ideate
description: "Generate and rank options. Use light mode for quick improvement scans and deep mode for explicit brainstorm requests or broad exploration."
---

# Idea Generation

Mode-aware ideation that turns vague opportunities into proportionally ranked options.

Core principle: **Match ideation depth to the decision.**

## Contracts

| Contract | File | Purpose |
|---|---|---|
| **Input** | `contracts/input.yaml` | Seed, mode, goal, and constraints |
| **Output** | `contracts/output.yaml` | Mode-appropriate ranking, next step or decision packet |
| **Phase Gates** | `contracts/phase-gates.yaml` | Light and deep pipeline gates |

Contract v2 makes the former deep-only ranking, refinement, and decision
artifacts conditional; deep mode preserves those v1 artifacts, while light mode
uses `quick_ranking` and `recommended_next_step`.

**Rules:**
- Infer light mode unless the user explicitly asks for broad/deep exploration
- Light mode produces 3-5 options and a quick ranking without a full scoring matrix
- Deep mode produces 8-15 ideas, full scoring, and at least 3 refined candidates
- Never present a single option — ideation means choices
- Constraints from input are respected throughout all phases
- Deep DECIDE output includes `decision_point` and `decision_options`; capture `user_decision` only after an actual user choice

## Required References

Before running the pipeline, load and apply `references/ideation-pipeline.md`.
Light mode uses only that compact selector. Deep mode additionally loads
`references/deep-ideation.md`; load it only for deep mode.

## Goal

Generate several useful options at the least costly depth that supports the user's decision.

## Success Criteria

- The response states whether it used light or deep mode.
- Light mode returns 3-5 options, a quick ranking, trade-offs, and one recommended next step.
- Deep mode generates at least 8 ideas before full scoring and refines at least the top 3.
- Neither mode fabricates a user choice or presents one unexamined option.

## Constraints

- Do not force deep-mode ceremony onto a quick improvement or "what else" request.
- Do not collapse to one recommendation before generating multiple options.
- Ask only when missing goals or constraints would materially change the idea space or ranking.
- Respect explicit constraints throughout scoring and refinement.
- Respect prior attempts; do not re-propose rejected approaches unchanged.
- Include a wild or unconventional idea in deep mode.

## Modes

### Light mode

Use for quick improvement scans, "what else" questions, or a small set of
alternatives. Run UNDERSTAND → DIVERGE → CONVERGE → DECIDE with 3-5 options,
a qualitative quick ranking, trade-offs, first steps, and one recommended next
step. Do not build a five-criterion score table unless the user asks.

### Deep mode

Use when the user explicitly asks to brainstorm, explore broadly, generate many
ideas, or compare a wide solution space. Run the full pipeline with 8-15 ideas,
five-criterion weighted scoring, at least 3 refined candidates, and a decision
packet.

## Pipeline

```text
Light: UNDERSTAND -> DIVERGE (3-5) -> CONVERGE (quick rank) -> DECIDE (next step)
Deep:  UNDERSTAND -> DIVERGE (8-15) -> CONVERGE (weighted) -> REFINE -> DECIDE
```

## Output

Return:
- Both modes: `ideation_mode`, problem statement, and multiple ideas.
- Light: `quick_ranking` and `recommended_next_step`.
- Deep: `ranked_ideas`, `refined_candidates`, `decision_point`, and `decision_options`.
- `user_decision` only after the user explicitly chooses.

## Stop Rules

- Stop and ask when the goal or hard constraints are too ambiguous to generate useful options.
- In light mode, stop after the ranked options and recommended next step; do not force a follow-up decision.
- In deep mode, stop after the decision point and options unless the user already chose or asked for implementation.
- Do not enter implementation; hand selected candidates to `assistant-workflow` when build work starts.

## Integration with Workflow

When an idea is selected:
1. Decompose into testable criteria (using `assistant-workflow`'s idea-to-action pipeline)
2. Hand off to workflow for implementation
3. Save the outcome only when the user asks or it contains a concrete durable lesson

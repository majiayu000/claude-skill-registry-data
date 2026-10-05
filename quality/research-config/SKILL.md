---
name: research-config
description: Generate a `ResearchPlan` from `input.md` or equivalent raw research input.
---

# research-config

Goal:

- Generate a `ResearchPlan` from `input.md` or equivalent raw research input.

Inputs:

- `input.md` or equivalent raw research brief text
- optional `state/START_REQUEST.json`
- optional `RUN_POLICY.yaml`

Outputs:

- `research_plan/RESEARCH_PLAN.json`
- `research_plan/RESEARCH_PLAN.md`

Context Loading:

- Read `input.md` first. Treat it as the canonical user brief for the run.
- If `state/START_REQUEST.json` exists, use it only as auxiliary context for how the run was started. Do not let it override the actual brief text in `input.md`.
- If `RUN_POLICY.yaml` exists, use it only as supporting context for expected run style or emphasis. Do not copy policy values into the research goal unless the brief implies them.
- Extract three things from the research input:
  - the primary `research_goal`
  - `preferences` that define what a strong hypothesis should optimize for
  - `constraints` that all downstream hypotheses must satisfy

Execution Prompt Contract:

- System Intent:
  - You are the run's research-plan structuring layer.
  - Your job is to convert raw user research input into a concise, stable `ResearchPlanContract`.
- Required Reasoning Focus:
  - Extract the main scientific objective faithfully when it is explicit.
  - If the goal is underspecified, synthesize the shortest accurate formulation that preserves the user's intent.
  - Derive `preferences` as evaluation criteria for hypothesis quality.
  - Derive `constraints` as hard boundaries for downstream generation and review.
  - If `preferences` or `constraints` are not explicit, infer only reasonable defaults from the research domain and stated goal.
- Do Not Do:
  - Do not invent specific scientific facts that are not present or reasonably implied.
  - Do not turn broad domain assumptions into narrow claims unless the brief clearly supports them.
  - Do not emit verbose analysis or chain-of-thought style discussion.
  - Do not exceed five preferences or five constraints.
- Output Shape:
  - Produce a canonical `ResearchPlanContract`.
  - `research_goal` must be a single natural-language string, ideally no more than three sentences.
  - Each `preferences` and `constraints` item must be short, specific, and directly useful to downstream skills.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/research_plan.py` before writing `research_plan/RESEARCH_PLAN.json`.
2. Read `input.md`.
3. If present, read `state/START_REQUEST.json` and `RUN_POLICY.yaml` as contextual hints only.
4. Identify the main research objective.
5. Extract or infer up to five `preferences`.
6. Extract or infer up to five `constraints`.
7. Write the canonical `research_plan/RESEARCH_PLAN.json`.
8. Write the companion `research_plan/RESEARCH_PLAN.md`.
9. Run validation before declaring the skill complete.

Artifact Rules:

- `research_plan/RESEARCH_PLAN.json` must validate against the canonical shared `ResearchPlanContract`.
- `research_plan/RESEARCH_PLAN.md` must remain a human-readable rendering of the same plan, not a divergent summary.
- The JSON artifact is authoritative; the Markdown file is a companion view.

Completion Rule:

- This skill is complete only when `research_plan/RESEARCH_PLAN.json` and `research_plan/RESEARCH_PLAN.md` both exist and the JSON artifact is valid for downstream consumption.

---
name: team-ai-model
description: "Orchestrates an AI model project end to end: benchmark first, AI build, interpretation, audit, MLOps and release."
---
<!-- Generated from .claude/skills/team-ai-model/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /team-ai-model — Team AI Model

**Category:** Team Orchestration · **Primary agent:** `deep-learning-architect`

Orchestrates an AI model project end to end: benchmark first, AI build, interpretation, audit, MLOps and release.

Arguments: whatever the user wrote after the command name.

## Purpose
Orchestrate an AI model project end to end with a benchmark-first discipline: define the problem and the traditional benchmark, build and compare AI candidates, interpret what they learned, audit them independently, and put the approved model into monitored production. The output is an AI model whose added value over the benchmark is demonstrated and whose risks are controlled.

**Use it when** a forecasting, classification, solution or policy-learning task justifies a full AI project.

**Do not use it when** a single build skill is enough (`/build-deep-forecaster`, `/build-causal-ml`, `/build-neural-solver`, `/build-drl-policy`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Approved model-brief
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `deep-learning-architect` — primary agent; coordinates the work and integrates results
- `time-series-deep-learning-specialist` — Builds deep sequence and foundation-model forecasters
- `deep-reinforcement-learning-specialist` — Applies deep reinforcement learning to policy problems
- `neural-solver-specialist` — Solves high-dimensional economic models with neural networks
- `interpretable-ml-specialist` — Makes AI models explainable
- `mlops-engineer` — Engineers MLOps for models
- `ai-ethics-fairness-specialist` — Reviews AI ethics and fairness
- `llm-red-team-specialist` — Red-teams LLM systems

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Workflow
1. Phase 1: define problem, data splits, metrics and the traditional benchmark; user approves
2. Phase 2: build the benchmark, then AI candidates (parallel across architectures); log experiments
3. Phase 3: interpretable-ml-specialist explains and probes; neural-solver or DRL specialists extend if relevant
4. Phase 4: AI audit (ethics, red-team, leakage) by independent validators
5. Phase 5: mlops-engineer registers, deploys and sets monitoring; model-risk-governance-specialist recommends release or block
   - Register the model as a lego brick where it feeds a macro set (`/lego-map`)

## Checkpoints with the user
- End of Phase 1: approve problem, splits and benchmark
- End of Phase 2: decide whether candidates beat the benchmark enough to continue
- End of Phase 4: review audit findings

## Common pitfalls
- AI candidates built before the benchmark
- Auditors who built the model
- Deployment without monitoring

## Output
`models/ai/<name>/`

The project folder holds benchmark and candidate code, experiment logs, interpretation results, the audit report, registry entries and the monitoring plan.

## Gate / verdict
- Benchmark-first protocol followed; audit not FAIL
- Added value over the benchmark is shown with significance tests

## Suggested next steps
- `/model-release`

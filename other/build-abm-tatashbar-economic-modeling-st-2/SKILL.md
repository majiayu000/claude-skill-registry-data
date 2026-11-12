---
name: build-abm
description: "Builds an agent-based model with ODD documentation, calibration, validation and experiment design."
argument-hint: "[model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /build-abm — Build ABM

**Category:** Build · **Primary agent:** `agent-based-modeling-specialist`

Builds an agent-based model with ODD documentation, calibration, validation and experiment design.

Arguments: `$ARGUMENTS`

## Purpose
Build an agent-based model whose aggregate behavior emerges from heterogeneous, boundedly rational agents interacting in markets and networks, documented well enough that someone else can rebuild it and calibrated tightly enough that its results are more than illustrations. The output is a reviewed, reproducible simulation model with a validation record, not a single striking simulation run.

**Use it when** heterogeneity, interaction, networks, disequilibrium or learning drive the question: financial contagion, housing booms, firm dynamics, distributional dynamics, or policy experiments where behavioral responses differ from rational-expectations benchmarks.

**Do not use it when** a representative-agent or heterogeneous-agent equilibrium model answers the question (`/build-dsge`, `/build-hank`), or when accounting consistency of sectoral balances is the main concern without agent heterogeneity (`/build-sfc`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Approved model-spec with agent rules
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `agent-based-modeling-specialist` — primary agent; coordinates the work and integrates results
- `simulation-based-inference-specialist` — Estimates complex models with neural simulation-based inference
- `hpc-gpu-engineer` — Engineers high-performance computing

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Agent types | households, firms, banks, government, foreign sector; number of each | Mechanisms available; runtime |
| Behavioral rules | fixed heuristics, adaptive learning, reinforcement learning, LLM-informed rules | Realism versus discipline; calibration burden |
| Market protocols | decentralized matching, search, posted prices, order books | Price formation and frictions |
| Accounting | full stock–flow consistency or partial | Credibility of aggregate dynamics |
| Calibration method | moment matching, indirect inference, simulation-based inference | Identification and uncertainty |
| Scale | hundreds to millions of agents | Statistical stability versus compute |

## Workflow
1. Document the model with the ODD protocol before coding
   - Overview (purpose, entities, state variables, scales, process scheduling), Design concepts (emergence, adaptation, learning, interaction, stochasticity, observation) and Details (initialization, input data, submodels)
   - State each behavioral rule with its evidence or rationale
2. Implement with explicit random-seed management and unit tests for agent rules
   - One generator per stochastic process; seeds recorded in every output
   - Unit tests for each rule and for stock–flow consistency at the aggregate
3. Calibrate by indirect inference or SBI; check stylized facts
   - Targets: business-cycle moments, firm-size and income distributions, fat tails, volatility clustering, as relevant to the question
   - Report fit to targeted and untargeted moments
4. Design experiments and run with enough replications for stable estimates
   - Determine replications from the convergence of Monte Carlo averages; report confidence bands
   - Use common random numbers across policy variants
5. Report sensitivity to parameters and seeds
   - Global sensitivity analysis on behavioral parameters; key-driver ranking
6. Register the model as a lego set (`/lego-map`): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After the ODD document: confirm agents, rules and protocols before coding
- After calibration: confirm targets and fit are adequate for the question
- Before policy experiments: confirm the experiment design and replications

## Common pitfalls
- Behavioral parameters tuned freely until the model delivers the expected result
- Results from a handful of runs
- Accounting leaks that create or destroy money or assets
- Undocumented code that reviewers cannot follow

## Output
`models/abm/<name>/ (+ model.lego.json)`

The folder holds the ODD document, code, unit tests, calibration scripts and results, experiment scripts with seeds, the sensitivity report and the lego manifest. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- ODD complete
- Stylized-facts validation and seed-robustness reported
- Lego manifest passes `python tools/lego.py check`
- Aggregate stock–flow consistency is verified by tests
- Confidence bands come from enough replications to be stable

## Suggested next steps
- `/validate-model`
- `/policy-simulation`
- `/lego-map`

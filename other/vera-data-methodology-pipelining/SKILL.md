---
name: vera-data-methodology-pipelining
description: >-
  End-to-end statistics methodology research pipeline. From research direction
  to publication-ready manuscript with novel estimators, theoretical proofs,
  simulation studies, and real data applications. Use when user says
  "methodology pipeline", "develop new method", "research pipeline",
  "full pipeline", "run everything", or wants the complete methodology
  research workflow. Human-in-the-loop by design: the skill standardizes
  implementation and draft generation, while the human owns research taste,
  novelty judgment, and final sign-off.
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Task, spawn_agent, send_input, wait_agent, mcp__codex__codex, mcp__codex__codex-reply
---

# Statistics Methodology Research Pipeline

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Configuration Defaults](#configuration-defaults)
- [Why These Defaults](#why-these-defaults)
- [Runtime Capability Detection (mandatory at pipeline start)](#runtime-capability-detection-mandatory-at-pipeline-start)
- [Method Status](#method-status)
- [Open-Source Boundary](#open-source-boundary)
- [Operating Constraints](#operating-constraints)
- [Constants](#constants)
- [Tool Usage](#tool-usage)
- [Agent Communication](#agent-communication)
- [Pipeline Overview](#pipeline-overview)
- [Stage 1: Research Direction Intake](#stage-1-research-direction-intake)
- [Stage 2: Idea Discovery](#stage-2-idea-discovery)
- [GATE 1: Idea Selection (Human Checkpoint)](#gate-1-idea-selection-human-checkpoint)
- [Stage 3: Implementation](#stage-3-implementation)
- [Stage 4: Run Experiments](#stage-4-run-experiments)
- [Stage 5: External or Self Review](#stage-5-external-review-via-codex-mcp)
- [Stage 6: Paper Writing](#stage-6-paper-writing)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Output Structure](#output-structure)
- [State Persistence](#state-persistence)
- [Error Recovery](#error-recovery)


Open-source skill.

You are a methodology research copilot. You take a research direction and develop a novel statistical method end-to-end: idea discovery, theoretical proofs, simulation studies, external review, and manuscript production. The skill handles the codifiable research mechanics; the human owns idea taste, threshold-setting, and final acceptance of claims.

You do NOT submit manuscripts. You do NOT claim proofs are verified — all proofs are sketches requiring human verification. You do NOT upload user data to external services. You do NOT make claims of optimality without rigorous proof. All outputs are drafts. The pipeline produces a DRAFT — human review is always the final step.

Read `config/default.json` for pipeline settings.

## Scope Boundary

Use this skill when:
- The goal is statistics methodology research: a new estimator, inferential procedure, proof-backed asymptotic result, or simulation-backed methodological comparison.
- A draft-grade research pipeline is acceptable and a human will verify proofs, novelty, and publication claims.

Do not use this skill when:
- The main need is an applied analysis of one fixed dataset rather than a methodological contribution.
- Formal proof checking, theorem verification, or acceptance-quality novelty judgment must happen without human review.
- The available compute budget cannot support even pilot simulations plus at least one substantive validation step.

## Configuration Defaults

Pipeline constants live in `config/default.json`. Key knobs:

- `AUTO_PROCEED`, `GATE1_TIMEOUT` — unattended draft-mode behavior at Gate 1
- `MAX_REVIEW_ROUNDS`, `REVIEWER_MODEL` — Stage 5 review loop settings
- `MAX_TOTAL_CPU_HOURS`, `PILOT_REPLICATIONS` — pilot-simulation budget for idea triage
- `simulation-standards` and `implementation-tracks` references — normative requirements for Monte Carlo reporting, reproducibility, and track ownership

To override: create `config/local.json` or pass flags via `argument-hint`.

## Why These Defaults

- `PILOT_REPLICATIONS = 500` is intentionally a pilot budget: enough to falsify obviously weak ideas, not enough to overstate precision before the main simulation stage.
- `MAX_TOTAL_CPU_HOURS = 4` keeps the open-source workflow honest about finite compute and forces scope reduction when a proposal is too expensive to validate responsibly.
- `reference/specs/simulation-standards.md` is normative for this skill: Monte Carlo SEs, seeds, and reproducible simulation settings are part of the method contract, not optional polish.

## Runtime Capability Detection (mandatory at pipeline start)

The methodology pipeline can only run on runtimes that expose EITHER a parallel
SubAgent surface (Stage 3) OR the Main Agent with enough budget to run tracks
sequentially. Detect capabilities once at Stage 1 and bind for the whole run.

**Parallel-worker surface (Stage 3 tracks).** Bind `DISPATCH_MODE` to the first
option that resolves, in this priority order:

- `Agent` (Claude Code / Claude Agent SDK) — dispatch multiple independent
  SubAgents by emitting multiple `Agent` tool calls in a single response.
- `Task` (alternate Claude Code surface) — same semantics as `Agent`.
- `spawn_agent` + `send_input` + `wait_agent` (Codex / agent SDKs with a
  lifecycle-based worker surface) — use only when runtime policy and user
  authorization permit subagents; spawn each independent track, send its
  prompt, wait, collect results.
- **Sequential fallback** — if NO parallel-worker tool is available, run the
  independent Stage 3 tracks sequentially in the main agent loop. Slower but
  functionally equivalent. Log `dispatch_mode="sequential"` in
  `PIPELINE_STATE.json` and proceed. NEVER abort.

**External-review surface (Stage 5 review loop).** Bind `REVIEW_MODE`:

- `REVIEW_MODE = "external"` — an external reviewer bridge responded
  successfully; use the review loop described in `workflow/step05-review.md`.
- `REVIEW_MODE = "self"` — no external reviewer bridge is available. Use the self-review fallback
  embedded at the end of `workflow/step05-review.md` (same rubric + artifact
  contract as the external path, just with the Main Agent playing reviewer
  under a strict critique rubric + per-round improvement cap).

The pipeline NEVER aborts because a specific tool name is missing — every
stage has a degraded-but-complete path. Log chosen modes in `RESEARCH_LOG.md`.

## Method Status

| Status | Methods / Guarantees |
|---|---|
| Implemented workflow guarantees | Literature-grounded idea discovery, proof-sketch generation, pilot simulations, full simulation studies, real-data application drafting, manuscript drafting |
| Implemented quality controls | Runtime detection for parallel tracks, sequential fallback, Codex-MCP review fallback, Monte Carlo SE reporting, reproducibility logging, and explicit proof-verification handoff to the human |
| Human-verification required | Proof correctness, novelty judgment, asymptotic claim acceptance, and final manuscript approval |

## Open-Source Boundary

- This skill package is the open, reusable workflow layer.
- It does NOT encode a paid service, subscription tier, or private idea feed.
- If someone builds a paid offering around it, the paid value should come from human judgment: idea selection, novelty filtering, reviewer strategy, and domain-specific oversight.
- The point of the skill is to standardize what can be standardized so the human can spend energy on what cannot.

## Operating Constraints

- Gate 1 is the primary human checkpoint, but additional human review is required whenever novelty, proofs, or publication claims remain uncertain
- Stage 1 may ask for clarification if the research direction is too broad
- Proofs generated by AI MUST be verified by the author
- Include all random seeds and package versions for reproducibility
- Always report Monte Carlo SEs alongside simulation results
- Do NOT submit the paper — always leave final submission to the human

## Constants

- AUTO_PROCEED = true — Only for unattended draft generation; do not bypass required human review in interactive use
- GATE1_TIMEOUT = 10 — Seconds to wait at Gate 1 before logging a default draft choice in unattended runs
- MAX_REVIEW_ROUNDS = 4 — External review iterations through the configured reviewer bridge
- REVIEWER_MODEL = gpt-5.4 — External reviewer model
- MAX_TOTAL_CPU_HOURS = 4 — Limit for pilot simulations during idea discovery
- PILOT_REPLICATIONS = 500 — Replications for pilot sims

## Tool Usage

This skill is runtime-agnostic. Use the local platform's equivalent tools while
preserving the same files, state, and checkpoints. See the repository-level
`PLATFORM-COMPATIBILITY.md` when available for the Claude Code / Codex mapping.

- **Parallel workers**: Dispatch independent implementation tracks only when
  the runtime and user permissions allow it. Claude Code can use `Agent`/`Task`;
  Codex can use `spawn_agent` only when subagents are explicitly authorized.
  Otherwise, use the sequential fallback.
- **Shell/script execution**: Run R/Python simulations, monitor processes,
  compile LaTeX, and perform file operations.
- **File reading/editing**: Load workflow steps and create simulation code,
  proof sketches, output files, and state files.
- **File search**: Locate result files, artifacts, and references.
- **Web/literature lookup**: Discover literature and retrieve specific papers
  or web resources when the runtime provides web tools.
- **External reviewer bridge**: Stage 5 can use `mcp__codex__codex` /
  `mcp__codex__codex-reply` or another configured reviewer bridge. If no bridge
  is available, use the self-review fallback.

## Agent Communication

- At each stage start: print `=== Stage N: [Name] ===`
- At each stage end: print completion status + key metrics
- At Gate 1: present top ideas as numbered list with scores, wait for selection
- Progress: one summary line per completed track or sub-skill
- Errors: state what failed, what was skipped, and impact on pipeline
- Write all execution details to RESEARCH_LOG.md, not to chat
- Tone: direct, technical, no hedging
- For overnight runs: log stage transitions to PIPELINE_STATE.json for resume

## Pipeline Overview

```
Stage 1: Intake ──→ Stage 2: Idea Discovery
                          │
                    ══ GATE 1 ══  (Human selects idea)
                          │
                    Stage 3: Implementation
                     ┌─────┼─────┐
                    Sims  Proofs  Data   (parallel tracks)
                     └─────┼─────┘
                          │
                    Stage 4: Run Experiments
                          │
                    Stage 5: External/Self Review
                          │
                    Stage 6: Paper Writing (LaTeX + PDF)
                          │
                    paper/main.pdf + RESEARCH_LOG.md
```

## Stage 1: Research Direction Intake

Execute `workflow/step01-intake.md`.

Collect research direction, assess existing knowledge, set scope.
- Research direction from $ARGUMENTS
- Scan local files (papers/, literature/, proofs/) for existing work
- Identify computational environment (R/Python)
- Set up project structure

Output: `PIPELINE_STATE.json` with research context.

---

## Stage 2: Idea Discovery

Execute `workflow/step02-discover.md`.

Full idea discovery pipeline using absorbed sub-skills:
1. Read and execute `reference/patterns/literature-reviewing.md` with context: "$ARGUMENTS" — Literature survey
2. Read and execute `reference/patterns/idea-creating.md` with context: "$ARGUMENTS" — Brainstorm + pilot simulations
3. Read and execute `reference/patterns/novelty-checking.md` — Verify novelty of top ideas
4. Read and execute `reference/patterns/research-reviewing.md` — External critical review

Output: `IDEA_DISCOVERY_REPORT.md` with ranked ideas, novelty scores, reviewer feedback.

---

## GATE 1: Idea Selection (Human Checkpoint)

Present top 3 ideas and ask user to select.
- If AUTO_PROCEED=true: in unattended draft mode, wait GATE1_TIMEOUT seconds, then log #1 ranked as the draft default
- If AUTO_PROCEED=false: wait indefinitely for user response

This is the primary human decision point. Stage 1 may also ask for clarification
if the research direction is too broad (< 5 words). Downstream stages can draft
artifacts automatically, but novelty claims, proof acceptance, and submission-level
framing still belong to the human.

---

## Stage 3: Implementation

Execute `workflow/step03-implement.md`.

Three parallel implementation tracks (see `reference/specs/implementation-tracks.md`):

**Track A — Simulation Code** (SubAgent):
- Data-generating process functions
- Proposed estimator/method implementation
- Competing method implementations
- Evaluation metrics (bias, MSE, coverage, power)
- Parallel execution setup, random seeds

**Track B — Proof Sketches** (SubAgent):
- Key theorem/lemma statements
- Proof outlines and strategies
- Technical conditions and assumptions (numbered: A1, A2, ...)
- Regularity conditions

**Track C — Real Data Preparation** (SubAgent, if applicable):
- Data loading and preprocessing
- Analysis script applying proposed method
- Sensitivity analysis plan
- Comparison with competing methods on real data

Tracks A, B, C run in parallel. Track C is optional (skip if purely theoretical).

Output: `simulation/`, `proofs/`, `real_data/` directories.

---

## Stage 4: Run Experiments

Execute `workflow/step04-experiment.md`.

Deploy and manage simulations using absorbed sub-skills:
1. Read and execute `reference/patterns/experiment-running.md` — Deploy simulation code (local or remote)
2. Read and execute `reference/patterns/experiment-monitoring.md` — Track progress
3. Read and execute `reference/patterns/results-analyzing.md` — Interpret results with Monte Carlo SEs

Simulations include:
- Coverage probability studies (B ≥ 1000)
- Size and power comparisons across sample sizes
- Robustness checks under model misspecification
- Convergence rate verification

Output: `results/` directory with `.rds`/`.csv`/`.json` files + `RESULTS_ANALYSIS.md`.

---

## Stage 5: External or Self Review

Execute `workflow/step05-review.md`.

```
Read and execute reference/patterns/review-looping.md with context: "$ARGUMENTS"
```

Up to MAX_REVIEW_ROUNDS rounds of external review:
- Senior statistics reviewer simulation (JASA/Annals/Biometrika level)
- Evaluates: theoretical rigor, methodological contribution, simulation design, real data analysis, presentation
- Each round: review → parse → implement fixes (proof corrections, new simulations, reframing) → re-review
- Fixes may trigger additional simulations (launched and monitored inline)

**STOP**: Score ≥ 6/10 AND verdict "ready"/"almost", or max rounds reached.

Output: `AUTO_REVIEW.md` + `REVIEW_STATE.json`.

---

## Stage 6: Paper Writing

Execute `workflow/step06-paper.md`.

Full paper pipeline using absorbed sub-skills:
```
Read and execute reference/patterns/paper-writing.md with context: "$ARGUMENTS"
```

This chains:
1. Read and execute `reference/patterns/paper-planning.md` — Section outline + claims-evidence matrix
2. Read and execute `reference/patterns/figure-creating.md` — Publication-quality figures from simulation results
3. Read and execute `reference/patterns/manuscript-writing.md` — LaTeX manuscript (venue-specific)
4. Read and execute `reference/patterns/paper-compiling.md` — Compile to PDF
5. Read and execute `reference/patterns/paper-improving.md` — 2 rounds of writing polish

Output: `paper/main.pdf` + complete `paper/` directory.

---

## Minimal Smoke Test

- Smoke-test prompt: "Use `vera-data-methodology-pipelining` to prototype a small coverage-study methodology project with `PILOT_REPLICATIONS=100`, one baseline comparator, one proof sketch, and one draft application example."
- Expected pass condition: the pipeline produces `IDEA_DISCOVERY_REPORT.md`, `PIPELINE_STATE.json`, runnable artifacts under `simulation/` and `proofs/`, a small `results/` directory with Monte Carlo summaries, and a draft `paper/` directory without claiming theorem verification.

## Output Structure

All paths are relative to the **project root**. Sub-skills (auto-review-loop,
run-experiment, analyze-results, idea-discovery, paper-writing) write to root-level
locations — this pipeline follows those conventions, not an output/ subdirectory.

```
[project root]
├── PIPELINE_STATE.json        ← Pipeline state persistence
├── IDEA_DISCOVERY_REPORT.md   ← Ranked ideas with novelty scores (Stage 2)
├── IDEA_REPORT.md             ← Raw idea brainstorm output (idea-creator)
├── RESULTS_ANALYSIS.md        ← Simulation results interpretation (analyze-results)
├── AUTO_REVIEW.md             ← External review loop log (auto-review-loop)
├── REVIEW_STATE.json          ← Review loop state (auto-review-loop)
├── PAPER_PLAN.md              ← Claims-evidence matrix (paper-plan)
├── RESEARCH_LOG.md            ← Full pipeline execution trace (Stage 6)
│
├── simulation/
│   └── simulation_code.R or .py   ← DGP + estimators + metrics
│
├── proofs/                    ← Top-level, NOT under simulation/
│   ├── THEOREM_1.tex          ← Theorem statements + proof sketches
│   ├── PROOF_OUTLINE.md       ← Overall proof strategy
│   └── ASSUMPTIONS.md         ← Numbered conditions (A1, A2, ...)
│
├── real_data/                 ← Top-level, NOT under simulation/
│   ├── data_load.R or .py
│   ├── analysis_script.R or .py
│   └── sensitivity_analysis.R or .py
│
├── results/
│   ├── sim_results.rds or .pkl    ← Raw simulation output
│   └── comparison_table.csv       ← Method comparison table
│
├── logs/                      ← Top-level (run-experiment convention)
│   └── sim_*.log              ← Simulation progress logs
│
└── paper/
    ├── main.tex               ← LaTeX master document
    ├── main.pdf               ← Compiled PDF
    ├── sections/*.tex         ← LaTeX sections
    ├── figures/*.pdf          ← Publication figures
    └── references.bib         ← Bibliography
```

## State Persistence

After each stage, update `PIPELINE_STATE.json` (project root):
```json
{
  "stage": 3,
  "status": "in_progress",
  "research_direction": "...",
  "selected_idea": "...",
  "implementation_tracks": {
    "simulation": "completed",
    "proofs": "in_progress",
    "real_data": "completed"
  },
  "timestamp": "2026-04-05T14:00:00"
}
```

On resume: read state from project root, skip completed stages, continue from last checkpoint.
Stale threshold: 24 hours.

## Error Recovery

- If a pilot simulation fails in Stage 2: continue with other ideas, flag the failure
- If an implementation track fails in Stage 3: continue other tracks, note gap
- If main simulation fails in Stage 4: diagnose, attempt auto-fix, re-run (up to 3 retries)
- If no external reviewer bridge is available in Stage 5: fall back to self-review
- If LaTeX compilation fails in Stage 6: auto-fix up to 3 iterations

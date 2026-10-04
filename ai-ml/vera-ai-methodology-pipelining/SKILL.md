---
name: vera-ai-methodology-pipelining
description: >-
  End-to-end AI/ML methodology research pipeline. From research direction
  to publication-ready manuscript with novel architectures, training strategies,
  or evaluation methods. Includes idea discovery, implementation (model code,
  ablation studies, benchmark experiments), external review through the configured reviewer bridge,
  and paper writing (LaTeX + PDF). Use when user says "methodology pipeline",
  "develop new method", "research pipeline", "full pipeline", "run everything",
  or wants the complete autonomous AI/ML methodology research workflow.
  Designed for overnight autonomous execution.
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Task, spawn_agent, send_input, wait_agent, mcp__codex__codex, mcp__codex__codex-reply
---

# AI/ML Methodology Research Pipeline

## Table of Contents

- [Positioning](#positioning)
- [Scope Boundary](#scope-boundary)
- [Configuration Defaults](#configuration-defaults)
- [Why These Defaults](#why-these-defaults)
- [Operating Constraints](#operating-constraints)
- [Method Status](#method-status)
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


Open-source skill. This pipeline demonstrates end-to-end autonomous ML
research — what the machine can automate. Human judgment remains essential
at Gate 1 (idea selection), final manuscript review, and submission decisions.

## Positioning

- This skill is the free/open workflow layer. It shows what can be standardized,
  automated, and safely exposed as a reusable research pipeline.
- This skill does NOT hard-code a paid tier, subscription, cohort, or VIP offer
  into the workflow itself. Those commercial layers live above the skill, not
  inside it.
- General business pattern: publish the reusable workflow openly, then charge
  for the human judgment layer around it.
- Typical paid layers above this skill are idea/radar subscriptions, cohort or
  community access, custom review, and high-stakes strategy decisions.
- In a broader human-machine collaboration model, the paid value is typically in
  the human judgment layer: research direction selection, idea radar, novelty
  filtering, reviewer strategy, and final go/no-go decisions.
- Read this skill as an example of "the machine-doable part." The remaining
  value sits in the human decisions that cannot be fully reduced to a workflow.
- This framing is vertical-agnostic: the same free-skill / paid-judgment split
  can support research, education, consulting, or professional training.

You are an autonomous methodology research agent. You take a research direction and develop a novel AI/ML method end-to-end: idea discovery, implementation, benchmark experiments, external review, and manuscript production.

You do NOT submit manuscripts. You do NOT claim SOTA without rigorous benchmarking. You do NOT upload user data to external services. All outputs are drafts. The pipeline produces a DRAFT — human review is always the final step.

Read `config/default.json` for pipeline settings.

## Scope Boundary

Use this skill when:
- The goal is ML methodology research: new architectures, training procedures, or evaluation methods that need baselines, ablations, and benchmark reporting.
- A draft-grade research pipeline is acceptable and human review will remain in the loop.

Do not use this skill when:
- The main need is an applied analysis of one fixed dataset rather than a methodological contribution.
- Formal proof verification, production deployment, or leaderboard claims without human audit are required.
- The available compute budget cannot support even pilot benchmarking.

## Configuration Defaults

Pipeline constants live in `config/default.json`. Key knobs:

- `AUTO_PROCEED` (true), `GATE1_TIMEOUT` (10) — Gate 1 auto-proceed behavior (unattended mode only)
- `MAX_REVIEW_ROUNDS` (4), `REVIEWER_MODEL` — Stage 7 review settings
- `MAX_TOTAL_GPU_HOURS` (4), `PILOT_EPOCHS` (3) — compute budget for idea-discovery pilots
- `benchmark.{datasets, metrics, baselines}` — Stage 4 experiment matrix
- `seeds.{ablation, benchmark}` — reproducibility seeds
- `pytorch_version`, `cuda_version` — pinned runtime versions

To override: create `config/local.json` or pass flags via `argument-hint`.

## Why These Defaults

- `PILOT_EPOCHS = 3` is deliberately small: the idea-discovery stage is for falsifying weak ideas cheaply, not for producing publishable benchmark numbers.
- `MAX_TOTAL_GPU_HOURS = 4` keeps the open-source workflow honest about compute budgets and forces early scope reduction when a method is too expensive to validate responsibly.
- The benchmark references in `reference/specs/experiment-standards.md` are normative for this skill: same seeds, same splits, same compute budget, and no test-set tuning for the proposed method or its baselines.

## Operating Constraints

- Gate 1 is the primary human checkpoint — rest proceeds autonomously
- Stage 1 may ask for clarification if the research direction is too broad
- All experiments must include random seeds and package versions for reproducibility
- Always report confidence intervals alongside benchmark results
- Do NOT submit the paper — always leave final submission to the human

## Method Status

| Status | Methods / Guarantees |
|---|---|
| Implemented workflow guarantees | Literature-grounded idea discovery, multi-baseline benchmarking, ablations, hyperparameter sensitivity, benchmark reporting, LaTeX paper drafting |
| Implemented quality controls | Multi-seed reporting, paired/bootstrap significance guidance, same-protocol baselines, sequential runtime fallback, self-review fallback when no external reviewer bridge is available |
| Human-verification required | Novelty judgment, SOTA claims, go/no-go publication decisions, final manuscript approval |

## Constants

- AUTO_PROCEED = true — Auto-select top-ranked idea at Gate 1 if no user input
- GATE1_TIMEOUT = 10 — Seconds to wait at Gate 1 before auto-proceeding
- MAX_REVIEW_ROUNDS = 4 — External review iterations through the configured reviewer bridge
- REVIEWER_MODEL = gpt-5.4 — External reviewer model
- MAX_TOTAL_GPU_HOURS = 4 — Limit for pilot experiments during idea discovery
- PILOT_EPOCHS = 3 — Quick training runs for idea validation

## Tool Usage

This skill is runtime-agnostic. Use the local platform's equivalent tools while
preserving the same files, state, and checkpoints. See the repository-level
`PLATFORM-COMPATIBILITY.md` when available for the Claude Code / Codex mapping.

**Required capabilities** (the pipeline cannot run without these):
- **File reading**: Load workflow steps and reference files before executing them
- **File editing**: Create model code, experiment configs, output files, update state
- **Shell/script execution**: Run Python training scripts, monitor processes, compile LaTeX, file operations
- **File search**: Search results files, locate artifacts, verify file existence
- **Web/literature lookup**: Literature discovery and paper retrieval during Stage 2

**Parallel-worker surface** (runtime-dependent; pipeline auto-detects):
Stage 3 launches parallel implementation tracks (Track A: model code,
Track B: baselines, Track C: data prep) using whatever parallel-worker
tool the runtime exposes and the user's permissions allow. Detect it at
Stage 3 start and bind `DISPATCH_MODE` to one of the following, in priority
order:
- `Agent` (Claude Code / Claude Agent SDK) — dispatch multiple independent
  SubAgents in a single response by emitting multiple `Agent` tool calls.
- `Task` (alternate Claude Code surface) — same semantics as `Agent`.
- `spawn_agent` + `send_input` + `wait_agent` (Codex / agent SDKs that
  expose a lifecycle-based worker surface) — use only when the runtime policy
  and user authorization permit subagents; spawn each independent track, send
  its prompt, collect results before Stage 4.
- **Sequential fallback** — if NO parallel-worker tool is available, run
  the three implementation tracks sequentially (Track A, then B, then C)
  in the main agent loop. This is slower but functionally equivalent;
  log `dispatch_mode="sequential"` in `PIPELINE_STATE.json` and proceed.

The pipeline NEVER aborts because a specific parallel-worker tool name
is missing — the sequential fallback guarantees completion.

**Optional tools** (graceful fallback if missing):
- **External reviewer bridge**: Optional assistant for Stage 2 idea discovery
  and Stage 5 review. The preferred bridge is `mcp__codex__codex` /
  `mcp__codex__codex-reply`, but another configured reviewer bridge can be used
  if it accepts the same prompt context. If no bridge is available, Stage 2
  falls back to local brainstorming / search-only novelty verification /
  self-critical review, and Stage 5 falls back to self-review. The pipeline
  never aborts because an external reviewer bridge is missing.

## Agent Communication

- At each stage start: print `=== Stage N: [Name] ===`
- At each stage end: print completion status + key metrics
- At Gate 1: present top ideas as numbered list with scores, wait for selection
- Progress: one summary line per completed track
- Errors: state what failed, what was skipped, and impact on pipeline
- Write all execution details to RESEARCH_LOG.md, not to chat
- Tone: direct, technical, no hedging

## Pipeline Overview

```
Stage 1: Intake ──→ Stage 2: Idea Discovery
                          │
                    ══ GATE 1 ══  (Human selects idea)
                          │
                    Stage 3: Implementation
                     ┌─────┼─────┐
                    Code  Baselines  Data   (parallel tracks)
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

Collect research direction, assess existing knowledge, set scope.
- Research direction from $ARGUMENTS
- Scan local files for existing work
- Identify computational environment (GPU availability, frameworks)
- Set up project structure

Output: `PIPELINE_STATE.json` with research context.

---

## Stage 2: Idea Discovery

Full idea discovery pipeline:
1. Literature survey (recent arXiv, conference papers)
2. Brainstorm + pilot experiments (quick feasibility checks)
3. Verify novelty of top ideas
4. External critical review of ideas

Output: `IDEA_DISCOVERY_REPORT.md` with ranked ideas, novelty scores, reviewer feedback.

---

## GATE 1: Idea Selection (Human Checkpoint)

Present top 3 ideas and ask user to select.
- If AUTO_PROCEED=true: wait GATE1_TIMEOUT seconds, then auto-select #1
- If AUTO_PROCEED=false: wait indefinitely

---

## Stage 3: Implementation

Three parallel implementation tracks:

**Track A — Model Code** (SubAgent):
- Proposed architecture/method implementation (PyTorch)
- Training loop with early stopping, learning rate scheduling
- Evaluation metrics (F1, AUC, accuracy with bootstrapped CIs)
- Random seeds for reproducibility

**Track B — Baseline Implementations** (SubAgent):
- Competing method implementations (or loading pre-trained)
- Same evaluation protocol as Track A
- Ensure fair comparison (same data splits, preprocessing)

**Track C — Data Preparation** (SubAgent, if applicable):
- Dataset loading and preprocessing
- Train/val/test splits with reproducible seeds
- Data augmentation pipeline
- Benchmark dataset integration

Tracks A, B, C run in parallel.

Output: `models/`, `baselines/`, `data/` directories.

---

## Stage 4: Run Experiments

Deploy and manage experiments:
1. Main benchmark experiments (proposed vs baselines)
2. Ablation studies (component contribution analysis)
3. Hyperparameter sensitivity analysis
4. Robustness checks (different seeds, data perturbations)

Results include:
- Performance comparison tables with bootstrapped CIs
- Ablation tables showing component contributions
- Training curves (loss, metrics over epochs)
- Statistical significance tests (paired bootstrap)

Output: `results/` directory + `RESULTS_ANALYSIS.md`.

---

## Stage 5: External or Self Review

Up to MAX_REVIEW_ROUNDS rounds of external review:
- Senior ML reviewer simulation (NeurIPS/ICML/ACL level)
- Evaluates: methodological contribution, experimental design, baselines, presentation
- Each round: review → parse → implement fixes → re-review

**STOP**: Score ≥ 6/10 AND verdict "ready"/"almost", or max rounds reached.

Output: `AUTO_REVIEW.md` + `REVIEW_STATE.json`.

---

## Stage 6: Paper Writing

Full paper pipeline:
1. Section outline + claims-evidence matrix
2. Publication-quality figures from experiment results
3. LaTeX manuscript (venue-specific: NeurIPS, ICML, ACL, EMNLP)
4. Compile to PDF
5. 2 rounds of writing polish

Output: `paper/main.pdf` + complete `paper/` directory.

## Minimal Smoke Test

- Smoke-test prompt: "Use `vera-ai-methodology-pipelining` to explore a tiny CIFAR-10 or AG News pilot, with `PILOT_EPOCHS=2`, at least two baselines, one ablation, and the standard draft artifacts."
- Expected pass condition: the pipeline produces `IDEA_DISCOVERY_REPORT.md`, `PIPELINE_STATE.json`, runnable code under `models/` and `baselines/`, a small `results/` directory, and a draft `PAPER_PLAN.md` without claiming SOTA.

---

## Output Structure

```
[project root]
├── PIPELINE_STATE.json
├── IDEA_DISCOVERY_REPORT.md
├── RESULTS_ANALYSIS.md
├── AUTO_REVIEW.md
├── REVIEW_STATE.json
├── PAPER_PLAN.md
├── RESEARCH_LOG.md
│
├── models/
│   ├── proposed_model.py
│   └── training_script.py
│
├── baselines/
│   ├── baseline_1.py
│   └── baseline_2.py
│
├── data/
│   ├── data_loader.py
│   └── preprocessing.py
│
├── results/
│   ├── benchmark_results.csv
│   ├── ablation_results.csv
│   └── training_curves.json
│
└── paper/
    ├── main.tex
    ├── main.pdf
    ├── sections/*.tex
    ├── figures/*.pdf
    └── references.bib
```

## State Persistence

After each stage, update `PIPELINE_STATE.json`:
```json
{
  "stage": 3,
  "status": "in_progress",
  "research_direction": "...",
  "selected_idea": "...",
  "implementation_tracks": {
    "model_code": "completed",
    "baselines": "in_progress",
    "data_prep": "completed"
  },
  "timestamp": "2026-04-05T14:00:00"
}
```

On resume: read state, skip completed stages, continue from last checkpoint.

## Error Recovery

- If a pilot experiment fails in Stage 2: continue with other ideas, flag the failure
- If an implementation track fails in Stage 3: continue other tracks, note gap
- If main experiment fails in Stage 4: diagnose, attempt auto-fix, re-run (up to 3 retries)
- If no external reviewer bridge is available in Stage 5: automatically fall back to self-review (see `workflow/step05-review.md` section 5.6). The pipeline never aborts because an external reviewer bridge is missing.
- If LaTeX compilation fails in Stage 6: auto-fix up to 3 iterations

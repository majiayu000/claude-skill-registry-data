---
name: vera-data-application-pipelining
description: >-
  End-to-end applied statistical research pipeline. Takes a research question
  and dataset, runs literature review, statistical analysis with parallel method
  tracks, and produces a complete manuscript (Markdown + LaTeX/PDF). Use when
  user says "application pipeline", "applied analysis", "analyze my data and
  write paper", "end-to-end analysis", or wants to go from raw data to
  manuscript. Covers all outcome types: continuous, binary, ordinal, nominal,
  count, survival, repeated measures, time series, multivariate, DOE,
  meta-analysis, and SEM. Human-in-the-loop by design: the skill handles the
  standardized workflow, while the user owns study framing, high-stakes
  judgment, and final sign-off.
argument-hint: [research-question]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Task, spawn_agent, send_input, wait_agent, mcp__codex__codex, mcp__codex__codex-reply
---

# Applied Statistical Analysis Pipeline

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Open-Source Boundary](#open-source-boundary)
- [Method Status](#method-status)
- [Constants](#constants)
- [Tool Usage](#tool-usage)
- [Agent Communication](#agent-communication)
- [Pipeline Overview](#pipeline-overview)
- [Stage 1: Intake](#stage-1-intake)
- [Stage 2: Outcome Detection & Routing](#stage-2-outcome-detection-&-routing)
- [Stage 3: Quick Literature Scan](#stage-3-quick-literature-scan)
- [Stage 4: Parallel Execution](#stage-4-parallel-execution)
- [Stage 5: Assemble Markdown Manuscript](#stage-5-assemble-markdown-manuscript)
- [Stage 6: LaTeX Manuscript & PDF](#stage-6-latex-manuscript-&-pdf)
- [Stage 7: External or Self Review](#stage-7-external-or-self-review)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Output Structure](#output-structure)
- [State Persistence](#state-persistence)
- [Error Recovery](#error-recovery)


Open-source skill.

You are a statistical research copilot. You take a research question and dataset through a complete analysis pipeline: literature review, multi-method statistical analysis, and manuscript production. The machine handles the codifiable, repeatable parts of the workflow; the human owns study framing, threshold-setting, interpretation, and release decisions.

You do NOT interpret clinical or policy significance beyond what the data supports. You do NOT submit manuscripts. You do NOT make causal claims that exceed the study design. You do NOT upload user data to external services. All outputs are drafts requiring human review.

Read `config/default.json` for pipeline settings.

## Scope Boundary

Use this skill when:
- The goal is an applied statistical manuscript for one concrete dataset and research question.
- The outcome family is one of the routed open-source families listed in `reference/specs/skill-routing-table.md`.

Do not use this skill when:
- The goal is a new estimator, theorem, or simulation-first methodology paper; use `vera-data-methodology-pipelining` instead.
- The requested claim exceeds the study design (for example, causal language from purely observational data).
- The needed method family is not named in the routing table or requires a specialty workflow not shipped in this repository.

## Open-Source Boundary

- This repository documents the reusable, standardized workflow layer. It is intentionally open-source and reproducible.
- The skill does NOT implement a paid tier, subscription system, or idea-radar product inside the repo.
- If someone builds paid services around this stack, the paid value should come from human judgment: problem selection, study design decisions, reviewer strategy, and domain-specific review, not from the reusable mechanics encoded here.
- When the workflow reaches a decision that cannot be safely standardized, escalate to the human instead of pretending the skill can fully automate it.

## Method Status

| Status | Coverage |
|---|---|
| Implemented workflow guarantees | Outcome detection, routed testing/analyzing handoff, literature review, manuscript assembly, LaTeX/PDF drafting, and Stage 7 review through an external reviewer bridge when available, with self-review fallback otherwise |
| Routed open-source families | Continuous, binary, ordinal, nominal, count, survival, repeated, time series, multivariate, DOE, meta-analysis, SEM-CFA, full SEM, and longitudinal-change SEM |
| Human verification required | Outcome-routing edge cases, domain interpretation, causal framing, and final manuscript approval |

## Constants

- HUMAN_GATE_TIMEOUT = 30 — Seconds to wait before re-prompting or logging a default suggestion in unattended draft runs; do not bypass required human review in interactive use
- MAX_REVIEW_ROUNDS = 4 — External review iterations in Stage 7 when an external reviewer bridge is available
- MAX_PARALLEL_TRACKS = 4 — Maximum concurrent analysis method tracks
- REVIEWER_MODEL = gpt-5.4 — Default external reviewer model when the configured bridge supports model selection

## Tool Usage

This skill is runtime-agnostic. Use the local platform's equivalent tools while
preserving the same files, state, and checkpoints. See the repository-level
`PLATFORM-COMPATIBILITY.md` when available for the Claude Code / Codex mapping.

**Required capabilities** (the pipeline cannot run without these):
- **Shell/script execution**: Run R/Python scripts, file operations, LaTeX compilation, data inspection
- **File reading**: Load workflow steps and sub-skill reference files before executing them
- **File editing**: Create output files (manuscript, code, tables), update state files
- **File search**: Search data files, locate output artifacts, verify file existence
- **Web/literature lookup**: Literature discovery and paper retrieval during Stages 3–4

**Parallel-worker surface** (runtime-dependent; pipeline auto-detects):
Stage 4 launches parallel SubAgents using whatever parallel-worker tool the
runtime exposes and the user's permissions allow. Detect it at Stage 4 start
and bind `DISPATCH_MODE` to one of the following, in priority order:
- `Agent` (Claude Code / Claude Agent SDK) — dispatch multiple independent
  SubAgents in a single response by emitting multiple `Agent` tool calls.
- `Task` (alternate Claude Code surface) — same semantics as `Agent`.
- `spawn_agent` + `send_input` + `wait_agent` (Codex / agent SDKs with a
  lifecycle-based worker surface) — use only when the runtime policy and user
  authorization permit subagents; spawn each independent track, send its prompt,
  wait for completion, collect results before Stage 4.5 convergence.
- **Sequential fallback** — if NO parallel-worker tool is available, run the
  independent tracks sequentially (one after another) in the main agent loop.
  This is slower but functionally equivalent; log
  `dispatch_mode="sequential"` in `PIPELINE_STATE.json` and proceed.

The pipeline NEVER aborts because a specific parallel-worker tool name is
missing — the sequential fallback guarantees completion.

**Optional tools** (graceful fallback if missing):
- **External reviewer bridge**: Stage 7 can use `mcp__codex__codex` /
  `mcp__codex__codex-reply` when available, or another configured reviewer
  bridge with the same request/response contract. If no bridge is available,
  Stage 7 automatically falls back to the self-review procedure embedded in
  `workflow/step07-review.md`. The pipeline produces the same artifact set in
  either mode.

Prefer the platform's native file/search tools when available. In Codex, `rg`
and shell reads are acceptable; in Claude Code, prefer `Read`, `Grep`, and
`Glob` where available.

## Agent Communication

- At each stage start: print `=== Stage N: [Name] ===`
- At each stage end: print completion status + key metrics (e.g., "4 tracks completed, 22 references")
- At human gates: present options as a numbered list, wait for response
- When uncertainty is material, say what requires human judgment instead of silently defaulting
- Progress: one summary line per completed track, not verbose logs
- Errors: state what failed, what was skipped, and impact on manuscript
- Write all execution details to RESEARCH_LOG.md, not to chat
- Tone: direct, technical, no hedging

## Pipeline Overview

```
Stage 1: Intake → Stage 2: Detect → Stage 3: Quick Lit Scan
                                          │
                               ┌─── Stage 4: Parallel ───┐
                               │                          │
                          Stream A:                  Stream B:
                        Full Lit Review            Analysis Tracks
                               │              T1│T2│T3│T4 (parallel)
                               │                    │
                               │                   T5 (sequential)
                               │                    │
                               └─── Convergence ────┘
                                          │
                               Stage 5: Assemble Markdown
                                          │
                               Stage 6: LaTeX & PDF
                                          │
                               Stage 7: External/Self Review
                                          │
                               output/manuscript.md + paper/main.pdf
```

## Stage 1: Intake

Execute `workflow/step01-intake.md`.

Collect research question, load data, inspect structure, assign variable roles.
Output: structured input summary + data profile in `PIPELINE_STATE.json`.

---

## Stage 2: Outcome Detection & Routing

Execute `workflow/step02-detect.md`.

Auto-detect outcome type using 3-signal system (see `reference/rules/outcome-detection-rules.md`).
Route to appropriate analysis skill (see `reference/specs/skill-routing-table.md`).

**HUMAN GATE**: Confirm outcome type detection with user.
- HIGH confidence: present a default recommendation; only auto-advance in unattended draft mode
- MEDIUM/LOW confidence: ask user to confirm or correct

---

## Stage 3: Quick Literature Scan

Execute `workflow/step03-quicklit.md`.

Fast literature survey: how have others analyzed this type of data in this domain?
Produces analysis strategy document with method tracks informed by prior work.

---

## Stage 4: Parallel Execution

Execute `workflow/step04-parallel.md`.

Two concurrent streams:

**Stream A — Full Literature Review** (SubAgent):
- Deepens Stage 3 scan into comprehensive review
- Output: `output/literature_review.md` + references

**Stream B — Analysis Method Tracks** (parallel SubAgents):
- Decompose analysis into independent method tracks (see `reference/specs/method-tracks.md`)
- Independent tracks run in parallel (e.g., regression, trees, quantile regression)
- Dependent tracks run sequentially (e.g., subgroup analysis after primary tests)
- Each track produces: methods fragment, results fragment, code, tables, figures

**Convergence** (after all tracks complete):
- Build unified variable importance table (0-100 normalized)
- Synthesize cross-method insights
- Merge all track outputs into unified `output/` artifacts
- Apply output quality variation protocol from the analyzing skill's references

---

## Stage 5: Assemble Markdown Manuscript

Execute `workflow/step05-assemble.md`.

Stitch all outputs into `output/manuscript.md`:
1. Title (from research question)
2. Abstract (written last, 150-250 words)
3. Introduction (RQ + literature review + gap + contribution)
4. Data & Study Design (dataset description, variables, sample)
5. Statistical Methods (merged methods from all tracks)
6. Results (merged results, ordered by track)
7. Discussion (findings vs prior work, limitations, implications)
8. References (merged + deduplicated)

See `reference/templates/manuscript-template.md` and `reference/rules/assembly-rules.md`.

---

## Stage 6: LaTeX Manuscript & PDF

Execute `workflow/step06-latex.md`.

Convert Markdown manuscript to LaTeX using the paper-writing sub-skills:
1. Read and execute `reference/patterns/paper-planning.md` — Generate claims-evidence matrix from `output/manuscript.md`
2. Read and execute `reference/patterns/figure-creating.md` — Convert PNG figures to PDF vector graphics for LaTeX
3. Read and execute `reference/patterns/manuscript-writing.md` — Convert manuscript.md into LaTeX sections (`paper/sections/*.tex`)
4. Read and execute `reference/patterns/paper-compiling.md` — Compile to `paper/main.pdf`

Venue-specific formatting applied (JASA, Biometrika, Annals, etc. based on user's target).

Output: `paper/main.tex`, `paper/sections/*.tex`, `paper/figures/*.pdf`, `paper/main.pdf`

---

## Stage 7: External or Self Review

Execute `workflow/step07-review.md`.

```
Read and execute reference/patterns/review-looping.md with context: "$ARGUMENTS"
```

Up to MAX_REVIEW_ROUNDS rounds of external review through the configured
reviewer bridge, or the self-review fallback when no bridge is available:
- Senior statistics reviewer simulation (JASA/Annals/Biometrika level)
- Each round: review → parse score/verdict/action items → implement fixes → re-review
- Fixes applied to both Markdown and LaTeX manuscripts
- Recompile PDF after each round of fixes

**STOP**: Score ≥ 6/10 AND verdict contains "ready"/"almost", or max rounds reached.

Output: polished `output/manuscript.md` + `paper/main.pdf` + `output/RESEARCH_LOG.md`.

---

## Minimal Smoke Test

- Smoke-test prompt: "Use `vera-data-application-pipelining` on `mtcars`, with `mpg` as a continuous outcome and `am` or `cyl` as the main grouping variable. Produce the standard manuscript and paper artifacts."
- Expected pass condition: the pipeline routes to the continuous family, produces `output/manuscript.md`, `output/methods.md`, `output/results.md`, `output/track_outputs/`, `paper/main.tex`, and `paper/main.pdf`, and records the review mode chosen in Stage 7.

## Output Structure

```
output/
├── manuscript.md              ← Complete Markdown manuscript
├── methods.md                 ← Merged methods section
├── results.md                 ← Merged results section
├── tables/                    ← All tables (Markdown + CSV)
├── figures/                   ← All figures (PNG, 300 DPI)
├── references.bib             ← Merged bibliography
├── code.R                     ← Combined R code (style-varied)
├── code.py                    ← Combined Python code (style-varied)
├── literature_review.md       ← Full literature review
├── analysis_strategy.md       ← Method track plan (from Stage 3)
├── track_outputs/             ← Per-track raw outputs (dynamic, varies by outcome type)
│   ├── {track_id}/            ← One directory per track from analysis_strategy.md
│   ├── ...                    ← e.g., T1_primary/, T2_regression/, T3_trees/, T4_qr/
│   └── ...                    ← SEM-family track IDs vary by routed family; see reference/specs/method-tracks.md
├── RESEARCH_LOG.md            ← Pipeline execution trace
└── PIPELINE_STATE.json        ← Pipeline state persistence

[project root]
├── AUTO_REVIEW.md             ← Review loop log (auto-review-loop convention)
└── REVIEW_STATE.json          ← Review loop state (auto-review-loop convention)

paper/
├── main.tex                   ← LaTeX master document
├── main.pdf                   ← Compiled PDF
├── sections/                  ← LaTeX sections
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── data.tex
│   ├── methods.tex
│   ├── results.tex
│   ├── discussion.tex
│   └── appendix.tex
├── figures/                   ← PDF vector figures for LaTeX
├── tables/                    ← LaTeX tables (optional)
└── references.bib             ← Bibliography
```

## State Persistence

After each stage, update `PIPELINE_STATE.json`:
```json
{
  "stage": 4,
  "status": "in_progress",
  "research_question": "...",
  "outcome_type": "continuous",
  "method_tracks": ["T1_primary", "T2_regression", "T3_trees", "T4_qr"],
  "tracks_completed": ["T1_primary", "T2_regression"],
  "tracks_pending": ["T3_trees", "T4_qr"],
  "lit_review_status": "completed",
  "timestamp": "2026-04-05T10:30:00"
}
```

On resume: read `PIPELINE_STATE.json`, skip completed stages, continue from last checkpoint.
Stale threshold: 24 hours — if older, offer fresh start or resume.

## Error Recovery

- If a track fails: log error, continue other tracks, report gap in manuscript
- If lit review fails: proceed with analysis, note limited background in manuscript
- If assembly finds inconsistencies: flag in RESEARCH_LOG.md, attempt auto-fix in Stage 6

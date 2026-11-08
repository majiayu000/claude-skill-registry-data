---
name: optimize
description: 'Makes code, containers, builds or LLM hyperparameters faster, smaller or cheaper, keeping only changes a benchmark proves. Use when the user says "optimize", "make it faster" or "speed up the build". Not for tidying code (use polish).'
argument-hint: '[scope:branch|global|working] [type:code|container|llm_hyperparams|build_pipeline|system] <target + metric + goal>'
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(git worktree *), Bash(git apply *), Bash(git branch *), Bash(git for-each-ref *), Bash(git update-ref *), Bash(git gc *), Bash(mkdir *), Bash(date *), Bash(printf *), Bash(printenv MZ_DEV_PIPE_AUTO_APPROVE *), Bash(${CLAUDE_PLUGIN_ROOT}/shared/journal-artifact.sh *), Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch, WebSearch
---

# Performance Optimization Pipeline

## Overview

Orchestrates iterative, measurement-driven performance optimization of any optimizable system — source code, container images and services, LLM hyperparameters, build pipelines, or a composite of these. Each iteration measures, profiles the dominant bottleneck, forms falsifiable speedup hypotheses, generates candidate changes, and verifies each one by measurement — banking only a change a benchmark proves faster and a correctness check proves safe.

Two principles are structural, not advisory:

- **Measure first, always.** No optimization before a trustworthy baseline exists. Profiling precedes hypothesizing; hypothesizing precedes changing. Every speedup number originates from the measurement harness (`pipeline-measure-runner`) — never from model narration.
- **The model generates candidates; measurement decides.** LLMs reliably pick the wrong bottleneck and over-claim speedups. This pipeline uses the model as a candidate *generator* and a deterministic harness as the *evaluator*. A change that was not measured is not a speedup.

The skill is **domain-generic**. The methodology — the scientific loop — is identical across domains; only the measurement command, the profiling technique, and the change space differ. Those three live in a per-run **Optimization Contract** (`contract.md`); the pipeline itself carries zero domain-specific commands. Swap the contract and the same pipeline optimizes a container image instead of a function.

## When to Use

Making source code, container images and services, LLM hyperparameters, build pipelines, or composite `system` targets faster, smaller, or cheaper against a goal that a repeatable command can measure.

### When NOT to use

- Removing dead code, unused imports, or reducing cyclomatic complexity — use `polish` with a cleanup criterion. It makes code tidier; it does not measure speed.
- A correctness bug or a failing test — use `debug`.
- Making existing code meet quality criteria or pass tests — use `polish`.
- There is no measurable metric and none can be supplied — the skill hard-gates on a measurable goal and cannot run without one.
- Understanding how code works, with no change intent — use `explain`.

## Input

`$ARGUMENTS` — the optimization target, the metric, and the goal. Examples:

- `optimize make src/parser/tokenizer.py 2x faster, p95 under 120ms`
- `optimize type:container reduce the api image below 200MB`
- `optimize type:llm_hyperparams tune sampling params for lowest eval loss`
- `optimize type:system scope:branch cut orchestrator end-to-end latency below 400ms`

Modifiers:

- `scope:` — `branch` | `global` | `working`; bounds which files / artifacts a candidate change may touch.
- `type:` — `code` | `container` | `llm_hyperparams` | `build_pipeline` | `system` | `generic`; selects the contract auto-detect path. If omitted, it is inferred from the target in Phase 0.5.

If `$ARGUMENTS` is empty, or names no measurable metric, the Phase 0 Goal Declaration gate collects it before the run proceeds.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands.

- **Default** (no `scope:`): all project files / artifacts eligible for candidate changes.
- `scope:` controls **which files / artifacts a candidate may edit**. Profiling and measurement are never scope-bound — the profiler reads whatever it needs and the harness runs the whole `measure_command`. The contract's `scope` field records the resolved value; a candidate change that would cross it triggers the Phase 4.5 boundary pause.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

| Constant                       | Value                      | Bounds                                                          |
| ------------------------------ | -------------------------- | --------------------------------------------------------------- |
| `MAX_OPTIMIZE_ITERATIONS`      | 6                          | Phase 2→6 loop hard cap                                         |
| `CANDIDATE_COUNT`              | 4                          | parallel `pipeline-perf-candidate` agents per hypothesis        |
| `SIGNIFICANCE_THRESHOLD`       | 0.10                       | minimum measured improvement to keep a candidate                |
| `CV_CEILING`                   | 0.10                       | measurement-noise hard-block ceiling (coefficient of variation) |
| `MEASURE_REPS`                 | 10                         | default benchmark repetitions                                   |
| `MEASURE_WARMUP`               | 3                          | default warmup repetitions (discarded)                          |
| `DIMINISHING_RETURNS_WINDOW`   | 2                          | iterations of sub-threshold gain before stopping                |
| `MAX_CANDIDATE_REVIEW_RETRIES` | 2                          | retries when a candidate agent returns malformed output         |
| `TASK_DIR`                     | `<PROJECT_ROOT>/.mz/task/` | task-state root                                                 |

`MEASURE_REPS`, `MEASURE_WARMUP`, `CV_CEILING`, and `MAX_OPTIMIZE_ITERATIONS` seed the matching `contract.md` fields (`measure_reps`, `measure_warmup`, `noise_ceiling_cv`, `iteration_cap`). Once the contract is approved, the contract's values are authoritative for the run — the contract is the per-run source of truth.

`PLUGIN_ROOT` is `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| Phase | Goal                                   | Reference                           | Gate                     |
| ----- | -------------------------------------- | ----------------------------------- | ------------------------ |
| 0     | Setup + Goal Declaration               | inline below                        | Hard                     |
| 0.5   | Contract Approval                      | `phases/contract_approval.md`       | Approval                 |
| 1     | Baseline                               | `phases/baseline.md`                | Hard                     |
| 2     | Profile & Classify Bottleneck          | `phases/profile_and_hypothesize.md` | —                        |
| 3     | Hypothesis Generation & Prioritization | `phases/profile_and_hypothesize.md` | —                        |
| 3.5   | Backlog / Strategy Approval            | `phases/backlog_approval.md`        | Approval                 |
| 4     | Candidate Generation & Verification    | `phases/candidate_loop.md`          | autonomous (risk-tiered) |
| 4.5   | Mid-loop Boundary Pause                | `phases/loop_checkpoints.md`        | Conditional              |
| 4.7   | Manual Correctness Checkpoint          | `phases/loop_checkpoints.md`        | Conditional              |
| 5     | Validation & Results                   | `phases/validate_and_results.md`    | Approval                 |
| 6     | Termination Decision                   | `phases/terminate.md`               | loop-back / stop         |

The loop is Phase 2 → 3 → 3.5 → 4 → (4.5 / 4.7 as triggered) → 5 → 6; Phase 6 either loops back to Phase 2 (re-profile — the bottleneck has moved) or stops. Phases 0, 0.5, and 1 run exactly once. Read each phase file when you reach it — do not load all phase files upfront.

### Phase 0: Setup + Goal Declaration

**Hard gate** — the pipeline cannot proceed without a measurable goal.

1. **Resolve project root** — resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. **Parse input** — extract `scope:`, `type:`, and the free-text target + metric + goal from `$ARGUMENTS`.
1. **Resolve scope** — per `<PLUGIN_ROOT>/shared/scope-parameter.md`; keep the resolved file list for the state step below. No `scope:` → all project files / artifacts eligible.
1. **Task name** — `<YYYY_MM_DD>_optimize_<slug>`, where `<slug>` is a snake_case summary of the target (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. **Unattended check** — run `printenv MZ_DEV_PIPE_AUTO_APPROVE` once. The resume check below uses the result, and the state write records it as `unattended: true` or `unattended: false`.
1. **Resume check** (before creating the task directory): follow `<PLUGIN_ROOT>/shared/resume-protocol.md`, "On entry". A `complete`, `completed` or `aborted_by_user` file starts a `_vN`. A `pending`, `running`, `blocked` or `failed` file gets the resume gate. When the run is unattended or nobody can answer, report the path, `Status` and `what_remains`, and stop. A pre-existing `state.md` **without** a `skill_variant: methodology` key belongs to the task history of the old code-cleanup skill that once had this name, not this skill — do not resume into it; pick a fresh `_vN` name.
1. **Task dir & state** — create `<PROJECT_ROOT>/.mz/task/<task_name>/`, save the resolved file list to `<PROJECT_ROOT>/.mz/task/<task_name>/scope_files.txt`, and write `state.md` per `<PLUGIN_ROOT>/shared/state-schema.md`: first line must be `schema_version: 2`, then `Status`, `Phase`, `PhaseName`, `Started`, `Iteration` (0), `FilesWritten`, and the progress-ledger keys `phase_complete: false` and `what_remains: []`, plus skill-specific keys `skill_variant: methodology`, `unattended`, `Target`, `Metric`, `Goal`, `TargetType`, and an empty `## History` section (the persistent record of every hypothesis tried and its measured outcome — it survives context compaction and stops a failed transform from being retried).
1. **Task tracking** — TaskCreate per pipeline phase.

**Goal Declaration.** The pipeline cannot proceed without a *measurable* goal. A measurable goal has three parts: a **metric** (what is measured), a **unit**, and either a **target value** or an explicit **"best effort"** (optimize as far as the iteration cap allows).

- If any part is missing — e.g. "make it faster" with no metric and no unit — emit `BUDGET MISSING` and ask the user, via AskUserQuestion, for the missing parts. Never guess a metric or a target. Do not proceed.
- Once all three parts are present → emit `BUDGET DECLARED`, record `Metric` and `Goal` in `state.md`, and proceed to Phase 0.5.

The "budget" is the performance budget — the measurable goal the whole loop is held to.

### Phase 0.5: Contract Approval

Phase 0.5 is in `<SKILL_DIR>/phases/contract_approval.md`: the contract drafting steps, the contract template, the gate message template and the gate handling.

### Phase 3.5: Backlog / Strategy Approval

Phase 3.5 is in `<SKILL_DIR>/phases/backlog_approval.md`: the gate message template and the gate handling.

### Phase 4.5: Mid-loop Boundary Pause

Phase 4.5 is in `<SKILL_DIR>/phases/loop_checkpoints.md`, section "Phase 4.5: Mid-loop Boundary Pause".

### Phase 4.7: Manual Correctness Checkpoint

Phase 4.7 is in `<SKILL_DIR>/phases/loop_checkpoints.md`, section "Phase 4.7: Manual Correctness Checkpoint".

## Common Rationalizations

| Rationalization                                        | Rebuttal                                                                                       |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| "the speedup is obvious, skip the measurement"         | unmeasured is not a speedup — the harness reports the number, never the model                  |
| "CV is a little over the ceiling, close enough"        | a benchmark above the noise ceiling is a coin flip; hard-block and quiesce the host            |
| "the model said it's O(n) now, so it's faster"         | Big-O claims are UNVERIFIED until the harness measures wall-clock — algebra is not a benchmark |
| "optimize the hottest function first"                  | the hottest function is often not the highest-impact target — rank by Amdahl-bounded impact    |
| "all candidates missed the threshold, keep the best"   | a sub-threshold result is a `DEAD END`; banking it banks measurement noise as a "win"          |
| "skip the correctness check, it's just a speed change" | a faster wrong answer is still wrong — most unverified optimizations regress behavior          |

## Red Flags

- A speedup number reached the user that did not originate from a `pipeline-measure-runner` artifact.
- A candidate was banked without a green correctness gate (or, for `manual` contracts, without the Phase 4.7 checkpoint).
- A hypothesis was formed from intuition instead of a measured profile — Phase 2 was skipped or rushed.
- The run continued past a `BENCHMARK UNRELIABLE` baseline.
- A cross-module, out-of-scope, or out-of-`change_space` change was applied without the Phase 4.5 pause.
- The Phase 4.7 manual checkpoint was auto-approved or skipped.
- A "win" below `SIGNIFICANCE_THRESHOLD` was banked anyway.

## Verification

Output the final results block: the contract's metric and goal, the **measured** baseline and final values (each tagged harness-sourced, with its measurement-artifact path), the per-iteration measured gains, the cumulative speedup (geometric mean across iterations), the correctness status of every banked change, the iteration count, and the termination reason. Every number must trace to a `pipeline-measure-runner` artifact under `.mz/task/<task_name>/measurements/`. A results block carrying a number with no artifact path is invalid — do not emit it.

## References

- `${CLAUDE_SKILL_DIR}/references/optimization-toolkit.md`: the bottleneck taxonomy, transformation catalog, profiling principles, prioritization rules and anti-patterns. Grep it per section: Phase 2 reads the taxonomy and the profiling principles, Phase 3 reads the catalog and the prioritization rules. Do not load the whole file.

## Error Handling

- **No measurable goal** — Phase 0 emits `BUDGET MISSING`, asks, does not proceed.
- **`measure_command` emits no parseable scalar** — Phase 1 hard-blocks; ask the user to fix the command; never substitute a guessed number.
- **Noisy baseline** (`CV > noise_ceiling_cv`) — Phase 1 emits `BENCHMARK UNRELIABLE` and hard-blocks; the user quiesces the host or raises the ceiling (which returns through the Phase 0.5 gate).
- **Baseline already meets the target** — Phase 1 emits `ALREADY WITHIN BUDGET` and stops successfully.
- **A hypothesis yields no surviving candidate** — emit `DEAD END`, move to the next backlog item, diversify the transformation class.
- **A candidate agent returns malformed output** — retry up to `MAX_CANDIDATE_REVIEW_RETRIES`, then drop that candidate.
- **`pipeline-tooling-detector` cannot detect a command** — fall back to asking the user to supply each contract field.
- **An unfamiliar target domain** — Phase 2 dispatches `pipeline-researcher` with web research; the live profile remains the primary signal.
- **Every exit** — a Reject at any gate, a Phase 1 hard-block, `ALREADY WITHIN BUDGET`, or the Phase 6 stop — runs the leftover sweep in `phases/terminate.md` §6.5 before the final `Status` is written, so no candidate worktree, branch, or `refs/mz/optimize/<task_name>/` ref outlives the run.
- Always save state before spawning agents.

## State Management

After each phase and each loop iteration, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`: the current `Phase` / `PhaseName`, `Iteration`, the current best measured value, `FilesWritten`, and the `## History` buffer. The history buffer records every hypothesis tried, its assigned transformation class, and its measured outcome (banked win / `DEAD END` / `HYPOTHESIS UNVERIFIED`) — Phase 4 reads it so no failed transform is retried, and it is the only reliable cross-iteration memory after context compaction. The `skill_variant: methodology` key is set in Phase 0 and never mutates.

Maintain the progress ledger on every phase transition: set `phase_complete: false` on entering a phase and `true` only once its artifacts are written and its gates pass; refresh `what_remains` (outstanding work as plain strings) — it must be `[]` when `Status: complete`. Stamp `last_verified` whenever a correctness or validation gate passes clean. Reading a `schema_version: 1` or unversioned `state.md` upgrades it in place: add the ledger keys, set `schema_version: 2`, and log the upgrade. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`.

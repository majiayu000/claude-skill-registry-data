---
name: auto-research
description: Autonomous experiment/evaluate/iterate loop for code, prompts, skills, or workflows. Use when optimizing a measurable metric with repeated keep/discard decisions and resumable state.
version: 2
---

# Auto-Research

Goal
- Run bounded autonomous optimization loops with measurable metrics.
- Keep experiment state on disk so a fresh agent can resume exactly.
- Prefer simple changes that survive verification, not random mutation spam.

Use this when
- The user wants to optimize a measurable target: test speed, build time, bundle size, training loss, memory, prompt quality, workflow latency, etc.
- There is a clear benchmark command or evaluation harness.
- The work has a rollback path (git, branch, snapshot, or disposable environment).
- You want `autoresearch`-style keep/discard loops inside Hermes.

Do not use this when
- No primary metric exists.
- The benchmark cannot be run repeatedly.
- The task is destructive/high-risk and lacks approval.
- Success is mostly subjective and cannot be reduced to stable checks.

Core pattern
1. Separate infrastructure from domain knowledge.
   - Infrastructure: benchmark runner, result log, baseline compare, rollback, resume files.
   - Domain knowledge: what to optimize, which files matter, which changes are allowed, what side effects are forbidden.
2. Externalize state to files in the target repo/workdir.
3. Record the baseline on the current machine/runtime.
4. Make one targeted change.
5. Run the benchmark.
6. Keep the change only if the primary metric improves and checks pass.
7. Record what was learned, not just what changed.
8. Repeat within time, token, and budget caps.

Required inputs
- Goal
- Benchmark command
- Primary metric name, unit, and direction (`lower` or `higher`)
- Files in scope
- Off-limits files/areas
- Constraints (tests, types, no new deps, etc.)
- Iteration cap or stop condition

State files
- `autoresearch.md`
  - Human-readable session doc: objective, metrics, files in scope, constraints, dead ends, wins, current hypotheses.
- `autoresearch.sh`
  - Fast benchmark wrapper. Emits `METRIC name=value` lines.
- `autoresearch.jsonl`
  - Append-only machine-readable log.
- `autoresearch.checks.sh` (optional)
  - Correctness backpressure: tests, types, lint.
- `autoresearch.ideas.md` (optional)
  - Promising ideas you are not testing yet.

Why this layout
- `autoresearch.md` keeps reasoning durable.
- `autoresearch.jsonl` keeps metrics durable.
- A fresh agent can resume from these files plus git history.
- State survives context resets and agent restarts.

Recommended directory discipline
- Default: keep these files at repo root or task root.
- If the repo is large, keep them in a dedicated experiment subdir but make `autoresearch.sh` run from the real target cwd.
- If the repo may sit inside a larger monorepo, stage only in-scope files. Avoid blind `git add -A` unless the scope is truly the full repo.

Suggested `autoresearch.md` structure
```markdown
# Autoresearch: <goal>

## Objective
<What is being optimized and why it matters>

## Primary Metric
- `<metric_name>` (<unit>, lower/higher is better)

## Secondary Metrics
- <optional tradeoff metrics>

## How to Run
- `./autoresearch.sh`
- `./autoresearch.checks.sh` (if present)

## Files in Scope
- <file>: <why it matters>

## Off Limits
- <file/area>

## Constraints
- tests must pass
- no new dependencies
- no behavior regression

## What's Been Tried
- baseline: ...
- keep: ...
- discard: ...
- dead ends: ...
```

Suggested `autoresearch.sh`
- Start with `set -euo pipefail`.
- Do the fastest useful precheck first.
- Run the workload.
- Print structured lines:
  - `METRIC duration_ms=1234`
  - `METRIC accuracy=0.91`
- Keep stdout lean. Large logs poison context.
- For noisy benchmarks under ~5 seconds, run several times and report the median.
- Template: `templates/autoresearch.sh`

Suggested `autoresearch.checks.sh`
- Only create when correctness constraints matter.
- Keep output short; show errors, not happy-path spam.
- Checks do not redefine the primary metric. They gate `keep`.

`autoresearch.jsonl` schema
- First write a config/header row for each new segment:
```json
{"type":"config","name":"vitest-speed","metric_name":"duration_ms","metric_unit":"ms","direction":"lower","timestamp":1710000000}
```
- Then append one row per experiment:
```json
{"type":"result","commit":"abc1234","metric":912.4,"metrics":{"duration_ms":912.4},"status":"keep","description":"cache glob parsing","timestamp":1710000100,"confidence":2.4,"asi":{"why":"memoized file stat fanout"}}
```

Status meanings
- `keep`
  - Primary metric improved and checks passed.
- `discard`
  - Primary metric worsened or tied.
- `crash`
  - Benchmark failed or timed out.
- `checks_failed`
  - Benchmark passed, but correctness checks failed.

Loop rules
1. Baseline first.
   - Never trust baseline numbers from another machine, runtime, or model.
   - Promote a new baseline only after an attempt clearly beats the current best.
2. One targeted change per iteration.
   - If you change five things, you learn nothing.
   - Parameter sweeps or mutation batches are discovery probes, not true autoresearch, unless each attempt still has a single keep/discard decision against the current baseline.
3. Primary metric is king.
   - Secondary metrics are tradeoff monitors, not the main objective.
4. Simpler wins ties.
   - Equal metric + less code/complexity => keep.
5. Do not thrash.
   - If the same family of ideas keeps failing, switch angle.
6. Log discarded runs well.
   - Reverted code is gone. The surviving lesson is in `description` and `asi`.
   - For failed branches, save a short branch summary: wrong hypothesis, touched files/params, observed regression, and the next safer direction.
7. Crash small, move on.
   - Fix trivial crashes. Do not spend ten iterations rescuing a bad idea.
8. For stateful evaluators, isolate comparison runs.
   - If the benchmark or optimizer writes persistent state (learning weights, mutation history, calibration files, cached policies), do NOT compare candidates in one shared state dir unless the experiment explicitly wants cumulative learning.
   - Prefer one fresh state dir / workdir / artifact root per candidate when measuring which config is better.
   - Otherwise you can get false positives from baseline drift, cumulative promotions, or cross-run contamination.
   - If a batch unexpectedly shows many late-run improvements after earlier candidates were accepted, suspect state contamination before trusting the leaderboard.
9. Resume from files.
   - On restart, read `autoresearch.md`, `autoresearch.jsonl`, recent git log, and `autoresearch.ideas.md` if present.
9. Prefer explicit rollback/checkpoint boundaries.
   - Before risky edits or mutations, create a git/worktree/snapshot checkpoint.
   - After regression, revert to the last good baseline instead of stacking fixes on top of a bad attempt.

Confidence scoring
- After 3+ data points, estimate session noise with Median Absolute Deviation (MAD).
- Confidence = `abs(best_improvement) / MAD`.
- Interpretation:
  - `>= 2.0` : likely real
  - `1.0 - 2.0` : above noise but marginal
  - `< 1.0` : likely noise; rerun before trusting
- Use `scripts/analyze_autoresearch_jsonl.py` to summarize segments and compute confidence from `autoresearch.jsonl`.

Recommended execution flow
1. Create a dedicated branch if git is available.
2. Read the files in scope.
3. Write `autoresearch.md` and `autoresearch.sh`.
4. Run baseline.
5. Append baseline to `autoresearch.jsonl`.
6. For each iteration:
   - patch one idea
   - run `./autoresearch.sh`
   - run `./autoresearch.checks.sh` if present
   - compare to current best
   - `keep` via commit or snapshot if better
   - otherwise discard via reset/revert
   - append result row
   - update `autoresearch.md`
7. Stop when:
   - iteration cap reached
   - no credible improvements remain
   - confidence stays low and no idea survives re-run
   - user interrupts

Minimal benchmark discipline
- Fast benchmarks: run multiple repetitions and use median.
- Slow benchmarks: one run is fine.
- Prefer repo-local scripts over giant shell one-liners.
- Keep the benchmark deterministic where possible: fixed seeds, fixed sample count, warmed cache rules stated explicitly.

Branch/finalization discipline
- If the loop produced several good changes, split them into independent reviewable branches.
- Group only changes that do not overlap on files unless they are tightly coupled.
- If two kept changes touch the same file, consider one branch unless you can cleanly replay them independently.

Hermes-specific adaptation
- Hermes has no built-in `run_experiment` or `log_experiment` tool. Emulate them with:
  - `write_file` / `patch` for session files
  - `terminal` / `execute_code` for benchmark runs and metric extraction
  - git commands for keep/discard
- Prefer repo artifacts over chat-only notes.
- If the loop becomes large, keep the plan and findings on disk, then resume from those artifacts instead of re-explaining in chat.

## Useful outputs
- `autoresearch.jsonl`
- `autoresearch.md`
- `results.tsv` or `results.csv` if tabular browsing helps
- small final summary in repo docs or CHANGELOG when the project expects it

## Reusable lesson: mutation sweep is not autoresearch

A repeated failure pattern in experiment-heavy repos:
- users run `N` mutation specs in a batch
- each run has an evaluator/result surface
- but there is no baseline promotion, no keep/discard state, and no resumable ledger
- this looks like "autoresearch" but is really just mutation spam / probe sweep

If the codebase already has a mutation evaluator, the minimal autoresearch wrapper should add:
1. **session ledger**
   - one durable session id
   - objective, base factor/family, baseline mutation id, attempts_total, kept/discarded counts
2. **attempt ledger**
   - candidate spec
   - evaluation result
   - explicit decision: `keep` or `discard`
   - compact failed-branch summary
3. **baseline promotion**
   - accepted attempt becomes the new baseline inside the session
   - future attempts branch from the promoted baseline, not from chat memory
4. **resume semantics**
   - if resuming and no prior `keep` exists, continue from the latest attempted spec rather than resetting blindly to the initial spec
5. **branch summary discipline**
   - save high-signal lines only: `reason=...`, `failure_tags=...`, `next_focus=...`

Good smell:
- one atomic mutation per attempt
- objective score is compared to baseline every time
- session can be resumed from disk by a fresh agent

Bad smell:
- 10/100 mutations run in a row with no explicit keep/discard state
- accepted/rejected must be inferred later from logs
- process loss means the search state is lost or ambiguous
- repeated `no_superior_mutation_found` keeps generating same-family specs without changing cluster/family

## Diagnosing batch mutation sweep failures

When a batch of N mutation specs all regress, before re-running with different params, diagnose the failure pattern:

1. Check if params were actually consumed:
   - Look for `parameter_overrides` in the output JSON, not just the input spec
   - If output shows empty overrides but input spec had values, the engine may not be reflecting consumed params (cosmetic gap, not necessarily a real problem)
   - Verify via `apply_factor_mutation_spec` code path that `registry.set_parameter()` is called

2. Classify failure tags:
   - `best_factor_composite_regressed` = mutation made the target factor worse overall
   - `bridge_gap_too_small` = improvement exists but below acceptance threshold
   - `pre_bayes_gate_regressed` = upstream gating layer degraded
   - `no_superior_mutation_found` = no improvement found at all

3. Look for systematic patterns:
   - If even-numbered runs have extra failure tags (e.g. from `evaluate_expansion_preview=true`), that flag adds stricter gates — disable it for pure parameter sensitivity analysis
   - If score_delta approaches zero at certain param values (e.g. run 5 at -0.002), that's near the local optimum — do finer search around those values
   - If all deltas are negative and monotonically worsening in one direction, the sweep is moving away from the optimum — reverse direction or narrow range

4. Check baseline stability:
   - If `top_factor_names` ranking is identical across all baseline measurements, the baseline is stable
   - If `composite_score` and `factor_scores` are None/N/A, the engine doesn't expose fine-grained scores — rely on `score_delta` and `top_factor_names` ranking changes

5. Next steps after all-regress batch:
   - Find the least-negative delta run and do local search (±small steps) around its params
   - Try cluster jumps (different param families) instead of linear sweeps within one family
   - If the engine has built-in cluster presets, use those rather than hand-crafting param combinations

Operational lesson: long-running repo-native autoresearch commands
- If a user asks for a fixed large iteration count (for example 100 attempts), run the command, but monitor state files during execution instead of waiting blindly.
- If the process is still alive but no stdout appears, inspect stderr and the attempt ledger/state directory to distinguish "hung" from "slow but progressing".
- If runtime becomes unreasonable, stop only after preserving partial state and report the actual completed attempt count; do not imply the requested count completed.
- Prefer the command's official status surface first, but if it returns empty or stale while the attempt ledger clearly has data, summarize directly from the ledger and state that the status surface did not reflect the run.
- For mutation/autoresearch ledgers, compute: session_id, attempts_total, kept/discarded counts, decision_counts, failure_tag_counts, latest reason, latest cluster/family jump, cycle, next mutation hint, and whether families actually rotated.

## Status determination for long-running autoresearch sessions

When a session writes both a live snapshot (with `status` and `updated_at`) and a final summary artifact on completion, the status command must use correct priority ordering to avoid misclassifying completed or interrupted runs.

Verified priority order:
1. `final_summary_exists || snapshot.status == "completed"` → completed (highest priority)
2. `snapshot.status == "running" && updated_at stale (>threshold)` → interrupted
3. `snapshot.status == "running" && updated_at fresh` → running
4. else → unknown

Common bug: checking `snapshot.status == "running"` before checking `final_summary_exists` causes completed sessions to report as "running" when the snapshot status field wasn't updated (e.g. crash after writing final summary but before updating snapshot).

Staleness threshold: use the session's typical iteration duration × 3-5x as the threshold. For ict-engine factor autoresearch, 10 minutes works. For faster benchmarks, use shorter thresholds.

Test cases to cover:
- final_summary exists + stale running snapshot → completed (not interrupted)
- snapshot says completed + no final summary → completed
- stale running + no final → interrupted
- fresh running + no final → running
- no snapshot + no final → unknown

## ict-engine factor iteration prompt design

See also `references/ict-engine-options-proxy-factor-iteration.md` for a concrete options-proxy / IV-RV compression iteration pattern, including 3-month timeframe sweep gates and tree-handoff checks.

When the user asks for an optimized background factor iteration prompt after a failed sweep, follow this pattern:

### Diagnosing the failed sweep first

Before designing the next iteration, extract from the previous batch:
1. Which run had the least-negative `score_delta` → that's the local optimum center
2. Whether `evaluate_expansion_preview` was toggled across runs → if so, even/odd runs have different gate strictness, confounding parameter sensitivity
3. Whether the sweep was monotonic (linear param increase) → if so, it only covered one direction, too narrow
4. Whether `top_factor_names` ranking changed across runs → if stable, baseline is solid; if unstable, noise is high

### Three-phase iteration strategy

Phase 1 — Local search around the best run's params:
- Use Latin Hypercube sampling (not full grid) to cover the combinatorial space efficiently
- Pick 2-3 key parameters to vary, fix the rest at the best run's values
- Set `evaluate_expansion_preview: false` to isolate pure parameter sensitivity from gate effects
- Use `factor-research` with `--emit-mutation-evaluation` for single-shot eval per spec

Phase 2 — Cluster jump exploration:
- ict-engine has 4 built-in cluster presets: `displacement_fvg_cluster`, `mss_bos_cluster`, `premium_discount_ote_cluster`, `smt_cluster`
- Each cluster has characteristic parameter overrides (see `forced_cluster_jump_template` in main.rs)
- Use `factor-autoresearch --iterations 3 --max-cluster-fail-streak 2` per cluster
- Critical: each cluster must use its own `--state-dir` to avoid cross-contamination of mutation_runs, learning_state, and ensemble scorecards
- Seed specs should blend the best local params with the cluster's preset overrides, not start from scratch

Phase 3 — Cross-validation:
- Collect best spec from Phase 1 + best from each Phase 2 cluster
- Compare by `score_delta` and `promoted_to_baseline` status
- If all deltas are negative, the current baseline is likely near global optimum for this objective

### Seed spec construction pattern

```json
{
  "mutation_id": "cluster-{name}-001",
  "base_factor": "structure_ict",
  "hypothesis": "Cluster jump: {cluster_name} with {focus_description}",
  "parameter_overrides": {
    // Start from best local search params
    // Then overlay cluster-specific preset values
  },
  "direction_hints": {
    "cluster_jump": "{cluster_name}_cluster",
    "cluster_jump_cycle": "{cycle_number}",
    "available_clusters": "displacement_fvg_cluster|mss_bos_cluster|premium_discount_ote_cluster|smt_cluster"
  },
  "step_size_hints": {},
  "enabled_overrides": {},
  "evaluate_expansion_preview": false
}
```

Note: `smt_cluster` changes `base_factor` to `cross_market_smt` — the only cluster that switches the base factor.

### Parallel execution pattern

- Phase 1 (local search) and Phase 2 (cluster jumps) are independent — run them simultaneously
- Use Python `ProcessPoolExecutor(max_workers=4)` for both phases
- Each worker writes its own spec file, runs the binary, captures stdout, extracts the last JSON object
- Results append to a shared `results.json` with incremental writes after each completion
- Always `cargo build --release` first — debug builds are 3-5x slower per run

### Data path convention

ict-engine MTF data lives at:
```
~/Downloads/Tomac/ict-cleaned-mtf/cleaned-{tf}/nq.continuous-{tf}.json
```
where `{tf}` is `1m`, `5m`, `15m`, `1h`, `4h`, `1d`. The `--data` flag uses the 15m file.

Pitfalls
- No metric -> no autoresearch.
- Do not optimize against a flaky benchmark without repetition.
- Do not keep an improvement that breaks correctness checks.
- Do not overfit to one tiny test input.
- Do not let experiment scaffolding sprawl bigger than the thing being optimized.
- Do not trust improvements with confidence below the noise floor unless manually confirmed.
- Do not forget to log dead ends.

Verification checklist
- Baseline recorded on this machine
- Metric direction explicit
- Files in scope explicit
- Rollback path available
- Benchmark script reproducible
- Checks script present when required
- Every kept change beats baseline or current best on the primary metric
- Confidence reviewed for noisy benchmarks

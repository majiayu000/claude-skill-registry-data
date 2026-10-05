---
name: mk:benchmark
version: 1.0.0
preamble-tier: 3
description: Experimental/manual harness canary procedure. It records benchmark manifests and scores but does not provide a fully automated runner.
argument-hint: '[run | compare <a> <b>] [--full]'
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - Agent
source: local
keywords:
  - benchmark
  - canary-suite
  - trace-log
  - measure-harness
  - dead-weight-audit
  - ground-truth
when_to_use: Experimental/manual use when measuring harness changes against ground truth. NOT for production performance benchmarking.
user-invocable: true
owner: testing
criticality: medium
status: active
runtime: claude-code
---

# mk:benchmark — Experimental Harness Canary Suite

Measures harness performance against a small set of ground-truth tasks. Provides the empirical signal that the dead-weight audit (per `.claude/rules/dead-weight-audit-rules.md`) consumes to make load-bearing decisions about each harness component.

## When to Use

Activate when:
- User runs `/mk:benchmark run` (default = quick tier, 5 tasks, ≤$5)
- User runs `/mk:benchmark run --full` (quick tier + 1 heavy task, ≤$30)
- User runs `/mk:benchmark compare <run-id-a> <run-id-b>` (delta table)
- Before applying a harness change (baseline)
- After applying a harness change (verify delta)
- During the dead-weight audit playbook (component enable/disable cycles)

Skip when:
- The harness has been run end-to-end manually within the last hour (use that data instead)
- Budget cap is hit before the suite finishes (record partial result, alert)

## Hard Constraints

1. **Quick tier ≤$5 total cost.** Hard block if projected cost exceeds.
2. **Full tier ≤$30 total cost.** Hard block if projected cost exceeds.
3. **`--full` is opt-in.** The heavy task (`06-small-app-build`) requires explicit `--full` flag because it triggers `mk:autobuild` which can run for hours. Refuses to run without the flag.
4. **NOT a replacement for unit tests.** This is harness-level measurement only.
5. **Results recorded in trace-log.jsonl** as `event=benchmark_result` records, tagged with `benchmark_version` + `harness_version` + `model_version`.

## Subcommands

| Subcommand | Purpose | Tier | Cost cap |
|---|---|---|---|
| `run` | Execute the quick tier (5 tasks) and record scores | quick | $5 |
| `run --full` | Execute quick + heavy tier (6 tasks total) | full | $30 |
| `compare <a> <b>` | Show per-task delta between two prior runs | — | (free, reads cache) |

## Tier Layout

```
.claude/benchmarks/
├── README.md                                  ← how to use + add tasks
├── canary/
│   ├── quick/                                 ← default tier (5 tasks, ≤$5)
│   │   ├── 01-react-component-spec.md
│   │   ├── 02-api-endpoint-spec.md
│   │   ├── 03-bug-fix-spec.md
│   │   ├── 04-refactor-spec.md
│   │   └── 05-tdd-feature-spec.md
│   └── full/                                  ← --full only (1 task, ~$25)
│       └── 06-small-app-build-spec.md
└── results/                                   ← per-run JSON dumps
```

## Usage

### Run quick tier

```bash
/mk:benchmark run
```

Outputs:
- Per-task verdict + score
- Total cost + duration
- Run ID written to `.claude/benchmarks/results/{run-id}.json` AND trace-log.jsonl

### Run full tier

```bash
/mk:benchmark run --full
```

Same as quick, plus the heavy `06-small-app-build` task. Refuses to run without `--full` to prevent accidental cost burn.

### Compare two runs

```bash
/mk:benchmark compare 260408-1430 260408-1530
```

Outputs a delta table:

```
| Task | Run A score | Run B score | Δ |
|---|---|---|---|
| 01-react-component | 0.92 | 0.88 | -0.04 |
| 02-api-endpoint    | 0.85 | 0.91 | +0.06 |
| 03-bug-fix         | 1.00 | 1.00 |  0.00 |
| ... | ... | ... | ... |
| TOTAL              | 0.89 | 0.91 | +0.02 |
```

## Output Schema

Each benchmark run writes a JSON dump to `.claude/benchmarks/results/{run-id}.json`:

```json
{
  "run_id": "260408-1430-bench",
  "tier": "quick",
  "started": "2026-04-08T14:30:00Z",
  "ended": "2026-04-08T14:42:00Z",
  "harness_version": "3.0.0",
  "model": "claude-opus-4-6",
  "total_cost_usd": 4.20,
  "total_duration_seconds": 720,
  "tasks": [
    {
      "spec": "01-react-component-spec.md",
      "verdict": "PASS",
      "weighted_score": 0.92,
      "duration_seconds": 145,
      "cost_usd": 0.85,
      "rubric_preset": "frontend-app"
    },
    ...
  ],
  "summary": {
    "passed": 4,
    "warned": 1,
    "failed": 0,
    "average_score": 0.89
  }
}
```

## Audit Mode

`scripts/git-index-audit.sh` records a reproducible git tracked-state fingerprint as a
JSON artifact — independent of the canary benchmark loop. Use it to verify two checkouts
of a repo are identical, or to snapshot tracked state over time.

```bash
# single-repo snapshot
bash .claude/skills/benchmark/scripts/git-index-audit.sh [repo-path]
# comparison (adds local/remote-only counts + recursive diff status)
bash .claude/skills/benchmark/scripts/git-index-audit.sh <local> <remote>
```

**Artifact location:** `.claude/benchmarks/audits/{YYMMDD-HHMMSS}-audit.json` — a SIBLING
of `results/`, NOT inside it. `compare-runs.sh` prefix-globs `results/*.json` and assumes a
`tier` key; an audit artifact placed in `results/` would crash it. Every audit artifact
carries a top-level `"type": "audit"` discriminator. Override the output dir with
`MEOWKIT_AUDIT_OUT_DIR`.

**Artifact schema:** `type`, `run_id`, `ts`, `repo`, `tracked_file_count`,
`directory_count_excl_git`, `tracked_path_sha256`, `tracked_index_sha256`, `comparison`
(null in single-repo mode), `working_tree_clean`. A best-effort `audit_result` trace event
is appended via `append-trace.sh`.

**Index-hash definition (toolkit canonical):** `tracked_index_sha256 = sha256(sort(git
ls-files -s))`. The `-s` flag includes mode + blob hash + stage, so the index hash captures
tracked CONTENT, not just paths; `tracked_path_sha256 = sha256(sort(git ls-files))` captures
paths only. The source method did not specify an index-hash command — this definition is
the toolkit's, documented here and in the script header so future comparisons are reproducible.

## Gotchas

- **`run-canary.sh` is an orchestrator-driven runner for the model-in-loop canary.** It writes a manifest with `PENDING` tasks then prints orchestrator instructions. The script CANNOT itself invoke `mk:autobuild` per task because each invocation requires a fresh subagent context, which only an orchestrator agent can spawn — not a shell process. **The agent invoking this skill MUST follow the printed instructions to fill in each task's results.** Failure to do so leaves the manifest as a stub.
- **The cost cap is now enforced (not just recorded).** After each task the orchestrator appends a `{costUsd,…}` receipt to the run's `.ledger.jsonl` and runs `run-canary.sh check-cap <ledger> <cap>`; exit 2 means the cap was reached and the run STOPS. Thresholds follow `harness-rules.md` Rule 6 (warn at $30, halt at the effective cap; `--budget N` / `MEOWKIT_BUDGET_CAP` override the tier cap). This mirrors the TypeScript cost-ledger the deferred live backends inherit.
- **The cross-harness journey (J10) IS automated.** Its deterministic layer runs offline in CI via the TypeScript journey runner (`packages/mewkit/src/journey-validation`) — migration → target validation → route/artifact/denied-token/side-effect oracles — with no model calls. Only the model-in-loop (live) canary above still needs the orchestrator handoff.
- **Circular dependency with `mk:autobuild`.** This skill invokes `mk:autobuild` per task. If a harness bug is exactly what the dead-weight audit is trying to find, the audit can fail to even start. The manual fallback is documented in `.claude/rules/dead-weight-audit-rules.md` Rule 8 — run individual canary specs via `/mk:cook <spec.md>` and score by hand.
- **Don't treat 100% pass as "harness is perfect."** Canary tasks are intentionally simple. Real-world failures live in the long tail; canary catches regressions, not all bugs.
- **Don't skip `--full` for the dead-weight audit.** The audit needs the heavy task to detect issues that only manifest in real product builds.
- **Don't compare runs across different model versions** without noting it in the delta table — model upgrade is a confounding variable.
- **Don't auto-rerun on FAIL.** Investigate FAILs manually; rerun only after a code change.

## References

| File | Purpose |
|---|---|
| `scripts/run-canary.sh` | Emits a task manifest + a cost-ledger path; prints orchestrator instructions for the per-task harness runs. Does NOT invoke `mk:autobuild` directly (needs a fresh subagent context only the orchestrator can spawn). `run-canary.sh check-cap <ledger> <cap>` enforces the Rule 6 cost cap between tasks (exit 2 = halt). |
| `scripts/compare-runs.sh` | Reads two prior run JSONs, emits delta table |
| `../../benchmarks/README.md` | How to add new canary tasks |
| `../../benchmarks/canary/` | Spec files |
| `../../benchmarks/results/` | Per-run JSON dumps |
| `../../memory/trace-log.jsonl` | Append-only trace store (benchmark results land here too) |
| `../mk:autobuild/SKILL.md` | The harness skill that benchmark invokes per spec |
| `../mk:trace-analyze/SKILL.md` | The consumer of benchmark results for the dead-weight audit |

## Start

For run: `scripts/run-canary.sh [--full]`.
For compare: `scripts/compare-runs.sh <run-id-a> <run-id-b>`.

## Memory Write

After each completed benchmark run, append the baseline to `.meowkit/telemetry/cost-log.json` (top-level array). Create the file with `[]` if it does not exist.

```json
{"run_id": "{id}", "date": "{ISO-date}", "tier": "quick|full", "pass_rate": N, "avg_score": N, "total_cost_usd": N}
```

Use `mkdir -p .meowkit/telemetry` before the append. This persists baselines for `compare-runs.sh` and the dead-weight audit.

---
name: jobs-trace-analyzer
description: "Analyze benchmark jobs (Terminal-Bench, Harbor) in jobs/, inspect ATIF trajectory logs, tool call errors, prompt issues, timeout/circuit-breaker failures, and verifier results to identify harness bottlenecks in LibrAgent and generate evidence-based improvement plans. Trigger phrases: 'jobs 트레이스 분석', 'benchmark trace analysis', 'jobs 디렉토리 분석', '하네스 분석', '성적 감점 요인 분석', 'jobs-trace-analyzer'."
---

# Jobs Trace & Harness Bottleneck Analyzer

Analyze benchmark run trajectories stored under `jobs/<job_timestamp>/` to
pinpoint harness bottlenecks in **LibrAgent** (Builtin Tools, Prompts, Circuit
Breakers, Timeouts, Context Compaction) that degrade scores, and formulate
evidence-backed improvement plans.

**Scope:** tool sequences, observations, harness layers. **Don't care:**
model, serving engine. No harness contract broken → pattern and stop.

## Relationship to `harbor-harness-improvement-loop`

This skill is a **lighter inventory / categorization** pass over `jobs/<run>/`.

| Concern                                          | Use                                  |
| ------------------------------------------------ | ------------------------------------ |
| Quick pass-rate, failure buckets, tool frequency | **jobs-trace-analyzer** (this skill) |
| Evidence-backed BM → fix → rerun cycles          | **harbor-harness-improvement-loop**  |

Harbor’s analyzer is stricter: `verifier/reward.txt` as reward SSOT, ATIF-first
metrics, and explicit **heuristic ≠ verified failure**. Prefer that skill when
proposing product changes. Do not treat this script’s categories as causal proof.

## Workflow

### 1. Job Inventory & Automatic Trace Analysis

```bash
python .agents/skills/jobs-trace-analyzer/scripts/analyze_jobs_trace.py \
  jobs/<job_timestamp> \
  --output .libragent/work/trace-analysis/<job_timestamp>-analysis.md
```

Optional: `--verbose` prints per-task tool name lists.

The script reports:

- Total trials, pass rate (%), failed trial counts
- Failure categories (see below)
- Tool call frequency (ATIF-first when metadata trajectory is empty)
- `heuristic_error_observations` (keyword hits in ATIF observation text — **not**
  verified tool failures)

#### Failure categories

| Category                        | Meaning                                                                |
| ------------------------------- | ---------------------------------------------------------------------- |
| `SUCCESS`                       | Reward ≥ 1.0                                                           |
| `TIMEOUT_EXCEEDED`              | Exception type contains `Timeout`                                      |
| `NETWORK_API_ERROR`             | Connection / API network exception                                     |
| `TOOL_EXECUTION_ERROR`          | Structured tool `error` fields only (rare; not observation heuristics) |
| `INITIALIZATION_OR_EARLY_ABORT` | Zero turns                                                             |
| `AGENT_LOOP_OR_STUCK`           | ≥3 repeated adjacent identical tool calls (loop detected)              |
| `HIGH_TURN_COUNT`               | Turns > 30 without repeated-call evidence (inspect manually)           |
| `VERIFIER_FAILED_WRONG_STATE`   | Default failed bucket                                                  |

#### Tool extraction priority

1. `agent_result.metadata.trajectory` tool calls when present
2. Else ATIF `agent/trajectory.json` → `steps[].tool_calls[].function_name`
3. Else `metadata.tool_calls_count` (count only; names unavailable)

Reward prefers `verifier/reward.txt`, then `verifier_result.rewards.reward`.

---

### 2. Deep-Dive Trajectory Inspection (ATIF & Task Logs)

For each failed trial, inspect `jobs/<job_timestamp>/<task_name>/`:

1. **`result.json`**: rewards, `exception_info` / `exception.txt`, metadata turns
2. **`agent/trajectory.json` (ATIF)**: first divergence turn
3. **`verifier/reward.txt` & `trial.log`**: why verification failed

---

### 3. Harness Layer Mapping

> **Don't care (never diagnose, compare, or blame):** model, serving engine.
> In this harness project, tests evaluate the harness itself. If no harness
> contract (tool schema, handler, prompt assembly, circuit breaker, adapter)
> is broken, report the tool pattern and stop.

| Symptom                              | Primary Owning Layer               | Target Code                                                         |
| ------------------------------------ | ---------------------------------- | ------------------------------------------------------------------- |
| Tool parameter / schema error        | Builtin MCP tools                  | `src-tauri/src/mcp/builtin/`                                        |
| Repeated tool loop                   | Circuit breaker / natural recovery | `src-tauri/src/agent/llm/circuit_breaker.rs`, `natural_recovery.rs` |
| Timeout / unfinished                 | Timeout multipliers / shell        | `src-tauri/src/mcp/builtin/workspace/utils.rs`                      |
| Missing verification / premature end | Prompts                            | `src-tauri/src/agent/prompt/`                                       |
| Context loss / truncation            | Compaction                         | `src-tauri/src/agent/llm/completion/request/compact.rs`             |

---

### 4. Formulate Evidence-Based Improvement Plan

For each issue: symptom + trajectory evidence → root cause → smallest
intervention → verification (`pnpm refactor:validate`, `cargo test`, re-run
slice). Escalate to `harbor-harness-improvement-loop` for controlled BM cycles.

---

### 5. Report Output Location

Save reports under:

`.libragent/work/trace-analysis/<job_name>-analysis.md`

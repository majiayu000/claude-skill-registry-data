---
name: cortivex-agent-replay
version: 1.0.0
description: Records and replays agent execution traces for debugging, optimization, and regression analysis
category: debugging
tags: [replay, traces, debugging, optimization, time-travel, diff, execution-analysis]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [trace-recording, trace-replay, trace-diffing, time-travel-inspection, selective-replay, trace-analysis]
---

# Cortivex Agent Replay

You have access to an execution replay system that records every decision, tool call, and output an agent makes during a pipeline run, then lets you replay, diff, and analyze those traces. When a pipeline produces unexpected results, replay is how you find out why -- step through the agent's reasoning, compare two runs side-by-side, or re-execute the same trace with different models or inputs to isolate the cause.

## Overview

Agent replay operates on execution traces. A trace is a complete, ordered record of everything an agent did during a pipeline node execution: the input it received, every tool call it made (with arguments and responses), every intermediate reasoning step, every decision point, and the final output it produced. Traces are stored as structured JSON in `.cortivex/traces/` and can be replayed, diffed, or analyzed at any time after the original run.

Replay is not re-running the pipeline from scratch. Replay re-executes the agent's decision logic against the recorded inputs and tool responses, optionally substituting different models, prompts, or configurations to see how the output changes. This makes it fast (no actual file I/O or test execution) and deterministic (same inputs always available).

## When to Use

- A pipeline produced an incorrect or suboptimal result and you need to understand which agent decision led to it
- You want to compare how two different models handle the same task (swap claude-sonnet for claude-haiku and diff the outputs)
- A pipeline that previously worked has started producing worse results and you need to identify when the regression began
- You need to debug a specific node failure without re-running the entire pipeline
- You want to optimize agent prompts by replaying the same trace with modified system instructions and comparing outputs
- To feed execution data into the cortivex-learn system for pattern detection and insight generation

## When NOT to Use

- For live monitoring of running pipelines -- use `/cortivex status` instead
- As a substitute for unit tests -- replay validates agent behavior, not code correctness
- For traces older than 30 days unless explicitly archived -- traces are automatically pruned by default
- When the original trace was recorded against a codebase that has since changed substantially -- tool responses will no longer match reality

## How It Works

### Trace Structure

A trace captures the full execution timeline of a single agent within a single pipeline node. It contains metadata (run_id, node_id, model, timestamp, duration, cost), the input data from upstream nodes, an ordered array of steps, the final output, and aggregate metrics.

Each step has a type: `reasoning` (chain of thought), `tool_call` (tool name, arguments, response), `decision` (chosen action and alternatives considered), or `output` (final structured result). Steps include timestamps, duration, and token counts.

### Recording

Recording is automatic when enabled. Every pipeline run with `trace: true` in its config captures traces for all nodes. Traces are written to `.cortivex/traces/{run_id}/{node_id}.trace.json` as each node completes.

Recording adds minimal overhead (2-5% duration increase, no extra API calls) because it captures data the agent is already producing.

### Replay Modes

**Full Replay** re-executes the agent's decision logic from step 0 through the final output, using the recorded tool responses. The agent receives the same input and sees the same tool results, but makes fresh decisions. This reveals whether the agent's behavior is deterministic or whether it makes different choices on the same inputs.

**Selective Replay** re-executes only specific steps or step ranges. Use this to focus on a particular decision point without replaying the entire trace. You can start replay from any step and the system will inject the recorded state up to that point.

**Modified Replay** re-executes the trace with substitutions: a different model, different system prompt, different temperature, or different input data. The tool responses remain the same (from the recording), but the agent's reasoning and decisions may differ. This is the primary mechanism for A/B testing agent configurations.

## Pipeline Configuration

### Recording Traces in a Pipeline

```yaml
name: pr-review-traced
version: "1.0"
description: PR review with full execution tracing
trace: true                               # enable tracing for all nodes
trace_config:
  storage_path: .cortivex/traces/
  retention_days: 30
  capture_reasoning: true                  # include chain-of-thought
  capture_tool_responses: true             # include full tool output
  max_trace_size_mb: 50                    # cap per-trace file size
nodes:
  - id: security_scan
    type: SecurityScanner
    config:
      scan_depth: deep

  - id: code_review
    type: CodeReviewer
    depends_on: [security_scan]
    config:
      review_scope: changed_files

  - id: auto_fix
    type: AutoFixer
    depends_on: [code_review]
    config:
      fix_categories: [style, bugs]
```

### Replay and Diff Pipeline

```yaml
name: replay-comparison
version: "1.0"
description: Replay a trace with a different model and compare results
nodes:
  - id: replay_original
    type: ReplayAgent
    config:
      trace_id: "ctx-a1b2c3"
      node_id: "code_review"
      mode: full

  - id: replay_modified
    type: ReplayAgent
    config:
      trace_id: "ctx-a1b2c3"
      node_id: "code_review"
      mode: modified
      overrides:
        model: claude-haiku-4-20250414
        temperature: 0.2

  - id: diff_results
    type: ReplayAgent
    depends_on: [replay_original, replay_modified]
    config:
      action: diff
      left: replay_original
      right: replay_modified
      diff_format: structured
```

### Integration with Learning System

```yaml
name: replay-to-learn
version: "1.0"
description: Analyze replay data and feed insights to cortivex-learn
nodes:
  - id: analyze_traces
    type: ReplayAgent
    config:
      action: analyze
      trace_ids: ["ctx-a1b2c3", "ctx-d4e5f6", "ctx-g7h8i9"]
      analysis_type: failure-patterns

  - id: record_insights
    type: CustomAgent
    depends_on: [analyze_traces]
    config:
      system_prompt: |
        Take the trace analysis results and record actionable insights
        using cortivex_insights. Focus on patterns that appear across
        multiple traces: common failure points, model performance
        differences, and configuration optimizations.
```

## MCP Tool Reference

### Record a Trace

Recording is typically automatic via pipeline config, but can be started manually:

```
cortivex_replay({
  action: "record",
  run_id: "ctx-a1b2c3",
  node_id: "code_review",
  config: {
    capture_reasoning: true,
    capture_tool_responses: true,
    max_steps: 500
  }
})
```

**Response:**

```json
{
  "trace_id": "trace-7f3a",
  "status": "recording",
  "run_id": "ctx-a1b2c3",
  "node_id": "code_review",
  "started_at": "2025-01-15T09:30:00Z",
  "storage_path": ".cortivex/traces/ctx-a1b2c3/code_review.trace.json"
}
```

### Replay a Trace

```
cortivex_replay({
  action: "replay",
  trace_id: "trace-7f3a",
  mode: "full",
  overrides: {
    model: "claude-haiku-4-20250414",
    temperature: 0.3,
    system_prompt_append: "\nFocus only on security-related issues."
  }
})
```

**Response:**

```json
{
  "replay_id": "replay-2c9d",
  "source_trace": "trace-7f3a",
  "overrides_applied": {
    "model": "claude-sonnet-4-20250514 -> claude-haiku-4-20250414",
    "temperature": "0.5 -> 0.3",
    "system_prompt": "appended 1 instruction"
  },
  "result": {
    "output_changed": true,
    "steps_total": 23,
    "steps_diverged_at": 8,
    "original_issues_found": 7,
    "replay_issues_found": 4,
    "matching_issues": 4,
    "missing_issues": 3,
    "cost": { "original": "$0.018", "replay": "$0.003" },
    "duration": { "original_ms": 48000, "replay_ms": 12000 }
  }
}
```

### Diff Two Runs

```
cortivex_replay({
  action: "diff",
  left: "trace-7f3a",
  right: "replay-2c9d",
  diff_format: "structured",
  include_step_comparison: true
})
```

**Response:**

```json
{
  "diff_id": "diff-5e1b",
  "left": { "id": "trace-7f3a", "model": "claude-sonnet-4-20250514", "cost": "$0.018" },
  "right": { "id": "replay-2c9d", "model": "claude-haiku-4-20250414", "cost": "$0.003" },
  "summary": {
    "output_similarity": 0.72,
    "steps_identical": 7, "steps_similar": 9, "steps_divergent": 7,
    "first_divergence_at_step": 8
  },
  "output_diff": {
    "only_in_left": [
      { "category": "naming", "file": "src/api/routes.ts" },
      { "category": "edge-cases", "file": "src/utils/parser.ts" },
      { "category": "dry", "file": "src/services/order.ts" }
    ],
    "only_in_right": [],
    "in_both": [
      { "category": "complexity", "file": "src/utils/parser.ts" },
      { "category": "error-handling", "file": "src/api/auth.ts" }
    ]
  },
  "step_comparison": [
    { "step": 8, "left": "Checked naming conventions", "right": "Skipped naming, focused on error handling", "reason": "Haiku prioritized higher-severity categories" }
  ]
}
```

### Inspect Trace at a Point in Time (Time-Travel)

```
cortivex_replay({
  action: "trace",
  trace_id: "trace-7f3a",
  step: 8,
  context_window: 3
})
```

**Response:**

```json
{
  "trace_id": "trace-7f3a",
  "position": { "step": 8, "of": 23 },
  "context": {
    "steps": [
      { "index": 5, "type": "tool_call", "tool": "file_read", "arguments": { "path": "src/utils/parser.ts" }, "response_summary": "245 lines, TypeScript, parseInput at line 23" },
      { "index": 6, "type": "reasoning", "content": "parseInput has cyclomatic complexity of 18, exceeding threshold of 15. Flagging.", "token_count": 87 },
      { "index": 7, "type": "tool_call", "tool": "file_read", "arguments": { "path": "src/api/routes.ts" }, "response_summary": "189 lines, 12 route handlers" },
      {
        "index": 8,
        "type": "decision",
        "content": "Decided to check naming conventions across all changed files",
        "alternatives_considered": [
          "Skip naming and focus on error handling (rejected: naming issues found in routes.ts)",
          "Check only files with complexity issues (rejected: too narrow)"
        ],
        "chosen_reason": "routes.ts uses mixedCase and snake_case inconsistently"
      }
    ]
  },
  "state_at_step_8": {
    "files_analyzed": 3, "findings_so_far": 2, "tokens_consumed": 4250, "cost_so_far": "$0.008"
  }
}
```

### Analyze Traces for Patterns

```
cortivex_replay({
  action: "analyze",
  trace_ids: ["trace-7f3a", "trace-9b2c", "trace-1d4e", "trace-3f6g"],
  analysis_type: "failure-patterns",
  min_occurrences: 2
})
```

**Response:**

```json
{
  "analysis_id": "analysis-8a3f",
  "traces_analyzed": 4,
  "total_steps_analyzed": 89,
  "patterns": [
    {
      "pattern": "timeout-before-completion",
      "occurrences": 3,
      "description": "Agent spent excessive tokens on early files, ran out of budget before completing scope",
      "root_cause": "No file prioritization -- processes in directory order instead of by change size",
      "recommendation": "Analyze files with most changes first, skip files under 10 lines changed"
    },
    {
      "pattern": "redundant-tool-calls",
      "occurrences": 4,
      "description": "Agent reads the same file multiple times within a single node execution",
      "root_cause": "Agent does not cache file contents between reasoning steps",
      "recommendation": "Instruct agent to reference previously read files instead of re-reading"
    }
  ],
  "optimization_opportunities": [
    {
      "type": "model_substitution",
      "evidence": "In 3/4 traces, initial scan steps produced identical results regardless of model",
      "suggestion": "Use Haiku for file scanning phase, Sonnet for deep analysis"
    }
  ]
}
```

### Export Traces

```
cortivex_replay({
  action: "export",
  trace_ids: ["trace-7f3a", "trace-9b2c"],
  format: "json",
  include_tool_responses: true
})
```

**Response:**

```json
{
  "exported": 2,
  "files": [".cortivex/exports/trace-7f3a.json", ".cortivex/exports/trace-9b2c.json"],
  "total_size": "2.4 MB"
}
```

## Node Reference

```yaml
- id: replay_agent
  type: ReplayAgent
  config:
    action: record                        # record | replay | diff | trace | analyze | export
    trace_id: null                        # trace to operate on (required for replay, diff, trace)
    run_id: null                          # pipeline run ID (required for record)
    node_id: null                         # specific node (required for record, optional for others)
    mode: full                            # full | selective | modified
    step_range: null                      # [start, end] for selective replay
    overrides:                            # substitutions for modified replay
      model: null                         # replacement model
      temperature: null                   # replacement temperature
      system_prompt_append: null          # text appended to system prompt
      system_prompt_replace: null         # full system prompt replacement
      input_override: null                # replacement input data
    diff_format: structured               # structured | markdown | side-by-side
    include_step_comparison: true         # show per-step divergence in diffs
    analysis_type: failure-patterns       # failure-patterns | cost-optimization | quality-comparison
    min_occurrences: 2                    # minimum pattern frequency for analysis
    context_window: 3                     # steps before/after for time-travel
    capture_reasoning: true               # include chain-of-thought in traces
    capture_tool_responses: true          # include full tool output in traces
    max_steps: 500                        # maximum steps per trace
    storage_path: .cortivex/traces/       # trace storage directory
    retention_days: 30                    # auto-prune traces older than this
    export_format: json                   # json | csv | parquet
```

## Quick Reference

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Start recording | `cortivex_replay({ action: "record", run_id, node_id })` | Begin capturing an execution trace |
| Full replay | `cortivex_replay({ action: "replay", trace_id, mode: "full" })` | Re-execute trace with original config |
| Modified replay | `cortivex_replay({ action: "replay", trace_id, overrides: {...} })` | Re-execute with different model/config |
| Selective replay | `cortivex_replay({ action: "replay", trace_id, step_range: [5, 15] })` | Replay only specific steps |
| Diff two runs | `cortivex_replay({ action: "diff", left, right })` | Compare outputs and decisions side-by-side |
| Time-travel | `cortivex_replay({ action: "trace", trace_id, step: N })` | Inspect state at any execution step |
| Analyze patterns | `cortivex_replay({ action: "analyze", trace_ids: [...] })` | Find failure patterns across traces |
| Export traces | `cortivex_replay({ action: "export", trace_ids: [...] })` | Export traces for external analysis |

## Best Practices

1. **Enable tracing on all pipelines by default.** The overhead is negligible (2-5% duration, no additional API cost), but the debugging value when something goes wrong is enormous. You cannot replay what you did not record.
2. **Use modified replay for model evaluation, not separate pipeline runs.** Replaying the same trace with a different model controls for input variance. Running separate pipelines on the same repo introduces variance from file changes between runs.
3. **Diff before and after prompt changes.** When you modify a node's system prompt, replay the last 3-5 traces with the new prompt and diff against originals. This shows the exact impact of your change across multiple real-world inputs.
4. **Use time-travel to understand decisions, not just outputs.** The output diff tells you what changed. Time-travel to the first divergence step tells you why it changed. Always inspect the divergence point.
5. **Feed analysis results into cortivex-learn.** Replay analysis identifies patterns (redundant tool calls, timeout issues, model underperformance) that the learning system can turn into applied optimizations for future runs.
6. **Prune traces intentionally.** The default 30-day retention keeps storage manageable. Archive important traces (regression baselines, failure investigations) before they are pruned.
7. **Use selective replay for targeted debugging.** When you know which step caused the problem (from time-travel inspection), replay only that step range instead of the full trace. This is faster and produces less noise.

## Reasoning Protocol

Before recording, replaying, or analyzing traces, reason through:

1. **What specific question am I trying to answer?** "Why did the code review miss the null pointer bug?" is actionable. "Let me replay everything and see what happens" is not. Define the question before choosing the replay mode.
2. **Is the trace still valid for this codebase version?** If the codebase has changed significantly since the trace was recorded, tool responses in the trace (file contents, test results) no longer reflect reality. Replaying against stale data produces misleading results. Check the trace timestamp against recent commits.
3. **Am I controlling for the right variable?** When diffing two replays, change only one variable at a time. Swapping both the model and the temperature simultaneously makes it impossible to attribute output differences to either change.
4. **Is this a pattern or a one-off?** Before optimizing based on a single trace analysis, verify the pattern appears across multiple traces. Use the `analyze` action with `min_occurrences: 3` or higher to filter out noise.
5. **Will replay data feed the learning system?** If the analysis reveals an actionable pattern (e.g., "Haiku produces equivalent results to Sonnet for this node type"), record it as a cortivex-learn insight. Replay findings that are not recorded are wasted knowledge.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Replaying without a specific question | Produces data without insight; wastes time reviewing irrelevant steps | Define what you are investigating before starting replay |
| Changing multiple variables in a modified replay | Cannot attribute output differences to any single change | Change one variable per replay: model OR temperature OR prompt, never all at once |
| Replaying stale traces against a changed codebase | Tool responses in the trace do not match current file contents; conclusions are invalid | Check trace timestamp vs last commit; re-record if codebase has changed substantially |
| Ignoring the first divergence step in diffs | Focusing on output differences without understanding root cause | Always time-travel to the step where divergence began and understand why |
| Recording traces only when something goes wrong | The "before" trace does not exist, making comparison impossible | Enable tracing by default on all pipelines; the overhead is minimal |
| Storing traces indefinitely without pruning | Storage grows unbounded; old traces become stale and misleading | Set retention_days and archive only traces needed for regression baselines |
| Using full replay when selective replay suffices | Replaying 500 steps when the issue is at step 47 wastes time | Use time-travel to identify the relevant steps, then selective-replay that range |

**WRONG:**
```yaml
# Replaying with everything changed at once
nodes:
  - id: replay_test
    type: ReplayAgent
    config:
      trace_id: "trace-7f3a"
      mode: modified
      overrides:
        model: claude-haiku-4-20250414       # changed
        temperature: 0.1                      # changed
        system_prompt_replace: |              # changed
          You are a strict code reviewer...
        input_override:                       # changed
          review_scope: full
      # Cannot determine which change caused the output difference
```

**RIGHT:**
```yaml
# Isolating one variable at a time
nodes:
  - id: replay_baseline
    type: ReplayAgent
    config:
      trace_id: "trace-7f3a"
      mode: full                             # original config

  - id: replay_model_swap
    type: ReplayAgent
    config:
      trace_id: "trace-7f3a"
      mode: modified
      overrides:
        model: claude-haiku-4-20250414       # only model changed

  - id: diff_model_impact
    type: ReplayAgent
    depends_on: [replay_baseline, replay_model_swap]
    config:
      action: diff
      left: replay_baseline
      right: replay_model_swap
      include_step_comparison: true          # see exactly where model choice matters
```

## Grounding Rules

- **Trace file is corrupted or missing steps:** Do not attempt to replay incomplete traces. Re-run the original pipeline with tracing enabled to capture a fresh trace. Partial replays against corrupted data produce unreliable results.
- **Replay produces identical output to original:** This means the agent's behavior is deterministic for this input. This is a useful finding -- it confirms the agent is consistent. If you expected different output (e.g., after a prompt change), verify that your override was actually applied by checking the replay response's `overrides_applied` field.
- **Analysis finds no patterns across traces:** Either the sample size is too small (increase trace count) or the failures are genuinely independent. Not every failure has a systemic pattern. Report that no pattern was found rather than forcing a conclusion.
- **Diff shows high divergence but both outputs are acceptable:** Different models may take different paths to equally valid results. High divergence is not inherently bad. Evaluate whether the lower-cost path produces acceptable quality, and if so, record a model substitution insight in cortivex-learn.
- **Unsure whether to archive or prune old traces:** If the trace was recorded against a codebase version that still exists as a release tag, archive it. If the trace predates a major refactor and the codebase has changed structurally, prune it -- replaying against an obsolete codebase state provides no value.

## Advanced Capabilities

### Variant Testing & Branching

Variant testing forks a recorded trace at a specific decision point and explores alternative execution paths. Each variant branches from identical recorded state, ensuring controlled comparison.

```json
{
  "method": "cortivex_replay_variant",
  "params": {
    "trace_id": "trace-7f3a",
    "branch_at_step": 8,
    "variants": [
      { "variant_id": "v-strict", "overrides": { "model": "claude-sonnet-4-20250514", "system_prompt_append": "\nReject complexity above 10." } },
      { "variant_id": "v-lenient", "overrides": { "model": "claude-haiku-4-20250414", "temperature": 0.7 } }
    ],
    "compare_outputs": true
  }
}
```

**Response:**

```json
{
  "variant_run_id": "vrun-4e8b",
  "source_trace": "trace-7f3a",
  "branch_point": 8,
  "variants": [
    { "variant_id": "v-strict", "steps_executed": 18, "issues_found": 11, "cost": "$0.014" },
    { "variant_id": "v-lenient", "steps_executed": 12, "issues_found": 5, "cost": "$0.002" }
  ],
  "comparison": { "overlap_issues": 5, "strict_only": 6, "lenient_only": 0 }
}
```

### Replay Session Management

Sessions group related replay operations into a managed workspace with shared configuration, retention policies, and tagging. They persist across invocations for incremental comparison building.

```yaml
replay_session:
  session_id: "session-regression-q1"
  description: "Q1 regression investigation for PR review pipeline"
  tags: [regression, pr-review, q1-2026]
  config:
    base_trace_ids: ["trace-7f3a", "trace-9b2c", "trace-1d4e"]
    default_overrides: { capture_reasoning: true, include_step_comparison: true }
    retention: { keep_days: 90, archive_on_expiry: true, max_variants_per_trace: 10 }
    comparison: { baseline_trace: "trace-7f3a", similarity_threshold: 0.85, auto_diff: true }
```

### Execution Comparison & Diff Analysis

The comparison API returns structured diff results conforming to a strict schema, enabling programmatic consumption by CI pipelines and dashboards.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ReplayComparisonResult",
  "type": "object",
  "required": ["comparison_id", "left", "right", "summary", "step_diffs"],
  "properties": {
    "comparison_id": { "type": "string", "pattern": "^cmp-[a-z0-9]{4,}$" },
    "left": { "type": "object", "properties": { "trace_id": { "type": "string" }, "model": { "type": "string" }, "total_steps": { "type": "integer" }, "cost_usd": { "type": "number" } } },
    "right": { "type": "object", "properties": { "trace_id": { "type": "string" }, "model": { "type": "string" }, "total_steps": { "type": "integer" }, "cost_usd": { "type": "number" } } },
    "summary": { "type": "object", "properties": { "output_similarity": { "type": "number", "minimum": 0, "maximum": 1 }, "first_divergence_step": { "type": "integer" }, "divergent_step_count": { "type": "integer" }, "cost_delta_usd": { "type": "number" } } },
    "step_diffs": { "type": "array", "items": { "type": "object", "properties": { "step_index": { "type": "integer" }, "left_action": { "type": "string" }, "right_action": { "type": "string" }, "divergence_type": { "type": "string", "enum": ["identical", "similar", "divergent", "missing"] } } } }
  }
}
```

### Time-Travel Debugging

The `cortivex_replay_seek` tool provides fine-grained navigation within a trace, supporting conditional breakpoints and state watches alongside step-level inspection.

```json
{
  "method": "cortivex_replay_seek",
  "params": {
    "trace_id": "trace-7f3a",
    "seek_to": { "step": 12 },
    "inspect": { "agent_state": true, "tool_call_history": true, "token_budget_remaining": true },
    "breakpoints": [
      { "condition": "step.type == 'decision' && step.alternatives_considered.length > 2" },
      { "condition": "state.tokens_consumed > state.token_budget * 0.8" }
    ],
    "watches": ["state.findings_count", "state.files_remaining"]
  }
}
```

**Response:**

```json
{
  "trace_id": "trace-7f3a",
  "position": { "step": 12, "of": 23 },
  "agent_state": { "files_analyzed": 5, "files_remaining": 3, "findings_count": 4, "tokens_consumed": 6800, "token_budget": 10000, "current_file": "src/services/order.ts" },
  "tool_call_history": [
    { "step": 1, "tool": "file_list", "duration_ms": 45 },
    { "step": 3, "tool": "file_read", "file": "src/api/routes.ts", "duration_ms": 120 },
    { "step": 5, "tool": "file_read", "file": "src/utils/parser.ts", "duration_ms": 98 },
    { "step": 9, "tool": "file_read", "file": "src/api/auth.ts", "duration_ms": 105 }
  ],
  "breakpoints_hit": [{ "step": 8, "condition": "alternatives_considered.length > 2", "value": 3 }],
  "watches": { "state.findings_count": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4], "state.files_remaining": [8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 3] }
}
```

### Regression Detection from Replays

Regression detection compares new trace outputs against established baselines using configurable rules with thresholds and severity levels. Violations are flagged with full diagnostic context.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RegressionRuleConfig",
  "type": "object",
  "required": ["rule_id", "baseline_trace", "assertions"],
  "properties": {
    "rule_id": { "type": "string", "pattern": "^reg-[a-z0-9-]+$" },
    "baseline_trace": { "type": "string" },
    "schedule": { "type": "string", "enum": ["on_commit", "daily", "weekly", "manual"] },
    "assertions": { "type": "array", "items": { "type": "object", "required": ["metric", "operator", "threshold", "severity"], "properties": {
      "metric": { "type": "string", "enum": ["output_similarity", "issues_found", "cost_usd", "duration_ms", "steps_total"] },
      "operator": { "type": "string", "enum": ["gte", "lte", "eq", "within_pct"] },
      "threshold": { "type": "number" }, "severity": { "type": "string", "enum": ["info", "warning", "critical"] }
    } } },
    "on_failure": { "type": "object", "properties": { "notify": { "type": "array", "items": { "type": "string" } }, "block_deploy": { "type": "boolean" }, "auto_bisect": { "type": "boolean" } } }
  }
}
```

A typical regression rule applied in practice:

```typescript
const prReviewRegression: RegressionRuleConfig = {
  rule_id: "reg-pr-review-quality",
  baseline_trace: "trace-7f3a",
  schedule: "on_commit",
  assertions: [
    { metric: "output_similarity", operator: "gte", threshold: 0.85, severity: "critical" },
    { metric: "issues_found", operator: "gte", threshold: 5, severity: "warning" },
    { metric: "cost_usd", operator: "lte", threshold: 0.05, severity: "info" }
  ],
  on_failure: { notify: ["slack:#agent-alerts"], block_deploy: true, auto_bisect: true }
};
```

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for agent replay operations, aligned with the OWASP Automated Security Testing (AST) risk taxonomy. Each subsection maps to a specific AST risk ID and provides enforceable configuration, validation schemas, and MCP tool integration examples.

### AST09: Trace Data Encryption at Rest

All persisted trace files contain agent reasoning chains, tool call arguments, and tool responses that may include source code, secrets, or sensitive business logic. Per **AST09** (Sensitive Data Exposure in Test Artifacts), traces must be encrypted at rest using AES-256-GCM.

```yaml
# .cortivex/security/trace-encryption.yaml
trace_encryption:
  enabled: true
  algorithm: AES-256-GCM
  key_derivation:
    method: PBKDF2-HMAC-SHA512
    iterations: 600000
    salt_length_bytes: 32
  key_management:
    provider: vault                      # vault | aws-kms | gcp-kms | local-keyring
    key_id: cortivex/trace-encryption-key
    rotation_interval_days: 90
    auto_rotate: true
  scope:
    encrypt_reasoning: true              # chain-of-thought steps
    encrypt_tool_responses: true         # full tool output payloads
    encrypt_metadata: false              # run_id, timestamps, cost (non-sensitive)
  storage:
    encrypted_extension: .trace.enc
    plaintext_traces_allowed: false      # reject writes of unencrypted traces
    migration:
      encrypt_existing: true             # encrypt pre-existing plaintext traces
      delete_plaintext_after: true       # remove originals after encryption
```

MCP tool call to verify encryption status of a trace (AST09 compliance check):

```
cortivex_replay({
  action: "inspect_security",
  trace_id: "trace-7f3a",
  checks: ["encryption_at_rest", "key_rotation_status"]
})
```

```json
{
  "trace_id": "trace-7f3a",
  "encryption": {
    "encrypted": true,
    "algorithm": "AES-256-GCM",
    "key_id": "cortivex/trace-encryption-key",
    "key_last_rotated": "2026-01-15T00:00:00Z",
    "ast_risk_id": "AST09",
    "compliant": true
  }
}
```

### Sensitive Data Redaction in Traces

Traces capture tool call arguments and responses verbatim, which may contain secrets, API keys, or PII. The redaction engine auto-strips sensitive values before they are written to disk, ensuring that even encrypted traces do not retain raw secrets. This control supplements AST09 by applying defense-in-depth.

```yaml
# .cortivex/security/trace-redaction.yaml
trace_redaction:
  enabled: true
  redaction_marker: "[REDACTED:{{category}}]"
  categories:
    secrets:
      patterns:
        - "(sk-[a-zA-Z0-9]{32,})"                    # OpenAI-style keys
        - "(ghp_[a-zA-Z0-9]{36})"                     # GitHub PATs
        - "(AKIA[0-9A-Z]{16})"                        # AWS access keys
        - "(?i)(bearer\\s+[a-zA-Z0-9\\-._~+/]+=*)"   # Bearer tokens
      action: replace
    api_keys:
      patterns:
        - "(?i)(api[_-]?key\\s*[:=]\\s*[\"']?)[^\"'\\s]+"
        - "(?i)(authorization\\s*[:=]\\s*[\"']?)[^\"'\\s]+"
      action: replace
    pii:
      patterns:
        - "(\\b[A-Z][a-z]+\\s[A-Z][a-z]+\\b)"        # full names (heuristic)
        - "(\\b\\d{3}-\\d{2}-\\d{4}\\b)"              # SSN format
        - "(\\b[\\w.+-]+@[\\w-]+\\.[\\w.-]+\\b)"      # email addresses
      action: hash_and_replace
      hash_algorithm: SHA-256
  enforcement:
    block_unredacted_write: true         # reject trace writes with detected secrets
    scan_on_export: true                 # re-scan before export (AST09 defense-in-depth)
    audit_log: true                      # log all redaction events
```

```typescript
interface TraceRedactionResult {
  trace_id: string;
  redactions_applied: number;
  categories_hit: Array<"secrets" | "api_keys" | "pii">;
  blocked: boolean;                      // true if block_unredacted_write triggered
  ast_risk_id: "AST09";
}
```

### Replay Authorization Controls

Modified replay can alter agent behavior by substituting models, prompts, or inputs. Per **AST09**, replays that change execution parameters require elevated permissions to prevent unauthorized experimentation with production traces.

```json
{
  "$schema": "https://cortivex.dev/schemas/replay-authorization/v1.json",
  "title": "ReplayAuthorizationPolicy",
  "type": "object",
  "required": ["policy_id", "rules"],
  "properties": {
    "policy_id": { "type": "string", "pattern": "^rpol-[a-z0-9-]+$" },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["replay_mode", "required_role", "ast_risk_id"],
        "properties": {
          "replay_mode": { "enum": ["full", "selective", "modified"] },
          "required_role": { "enum": ["viewer", "operator", "admin", "security-lead"] },
          "require_mfa": { "type": "boolean", "default": false },
          "require_approval": { "type": "boolean", "default": false },
          "approval_count": { "type": "integer", "minimum": 1 },
          "ast_risk_id": { "type": "string" }
        }
      }
    }
  }
}
```

```yaml
# Enforced replay authorization policy
replay_authorization:
  policy_id: rpol-production-traces
  rules:
    - replay_mode: full
      required_role: operator
      require_mfa: false
      ast_risk_id: AST09
    - replay_mode: selective
      required_role: operator
      require_mfa: false
      ast_risk_id: AST09
    - replay_mode: modified
      required_role: admin
      require_mfa: true
      require_approval: true
      approval_count: 1
      ast_risk_id: AST09
```

### Trace Export Controls

Exporting traces moves sensitive execution data outside the Cortivex security boundary. Per **AST09**, restricted traces (those containing redacted secrets or flagged PII) require explicit approval before export.

```yaml
# .cortivex/security/trace-export-controls.yaml
trace_export:
  default_policy: allow
  restricted_traces:
    policy: require_approval
    approval_roles: [security-lead, admin]
    approval_count: 1
    max_export_age_days: 30              # cannot export traces older than this
    ast_risk_id: AST09
  restrictions:
    - condition: "trace.redaction_count > 0"
      policy: require_approval
      reason: "Trace contained redacted sensitive data"
    - condition: "trace.classification == 'confidential'"
      policy: deny
      reason: "Confidential traces cannot be exported"
  audit:
    log_all_exports: true
    log_denied_exports: true
    include_requester_identity: true
```

```
cortivex_replay({
  action: "export",
  trace_ids: ["trace-7f3a"],
  format: "json",
  security: {
    approval_token: "appr-9c2d1e",
    requester: "eng-lead@example.com",
    justification: "Regression investigation for Q1 pipeline failure"
  }
})
```

```json
{
  "export_id": "exp-4f8a",
  "trace_ids": ["trace-7f3a"],
  "status": "approved",
  "approval_token": "appr-9c2d1e",
  "ast_risk_id": "AST09",
  "audit_entry": "Export approved by security-lead@example.com at 2026-03-24T10:15:00Z"
}
```

### Remote Attach Authentication Enforcement

Remote attach mode connects external debuggers to running or recorded replay sessions. Per **AST09**, token-only authentication is insufficient for remote attach because bearer tokens can be exfiltrated from logs or environment variables. All remote attach connections must use mTLS or OIDC.

```yaml
# .cortivex/security/remote-attach-auth.yaml
remote_attach_authentication:
  allowed_methods:
    - mtls
    - oidc
  explicitly_denied_methods:
    - token                               # AST09: bearer tokens are insufficient
    - basic                               # AST09: basic auth transmits credentials
  mtls_config:
    ca_bundle: /etc/cortivex/ca-chain.pem
    client_cert_required: true
    min_tls_version: "1.3"
    allowed_cipher_suites:
      - TLS_AES_256_GCM_SHA384
      - TLS_CHACHA20_POLY1305_SHA256
    certificate_revocation_check: true
    cert_expiry_warning_days: 30
  oidc_config:
    issuer: https://auth.example.com
    audience: cortivex-replay-remote
    required_claims:
      - sub
      - email
      - "cortivex:role"
    role_claim: "cortivex:role"
    min_required_role: operator
    token_max_age_seconds: 3600
  session_controls:
    max_session_duration_minutes: 60
    idle_timeout_minutes: 15
    max_concurrent_sessions: 3
    require_re_auth_for_write: true       # read-only sessions can attach; write requires re-auth
  audit:
    log_all_connections: true
    log_auth_failures: true
    alert_on_denied_method: true          # alert when token/basic auth is attempted
    ast_risk_id: AST09
```

```typescript
interface RemoteAttachSecurityCheck {
  connection_id: string;
  auth_method: "mtls" | "oidc";
  client_identity: string;
  role: string;
  tls_version: string;
  session_start: string;                 // ISO 8601
  session_max_expiry: string;            // ISO 8601
  read_only: boolean;
  ast_risk_id: "AST09";
  compliant: boolean;
  denied_reason?: string;                // populated when compliant is false
}
```

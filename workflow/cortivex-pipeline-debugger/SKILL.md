---
name: cortivex-pipeline-debugger
version: 1.0.0
description: Step-through debugging for Cortivex pipelines with breakpoints, inspection, replay, and execution tracing
category: debugging
tags: [debug, breakpoints, inspection, replay, trace, pipeline, troubleshooting]
author: Cortivex
requires: [cortivex MCP server, cortivex-pipeline]
capabilities: [breakpoint-management, node-inspection, input-replay, execution-tracing, watch-expressions]
---

# Cortivex Pipeline Debugger

You are a pipeline debugging agent that provides step-through debugging capabilities for Cortivex pipeline executions. You enable developers to set breakpoints on DAG nodes, inspect intermediate outputs flowing between nodes, replay failed nodes with modified inputs, and navigate forward and backward through the execution trace.

## Overview

Pipeline debugging solves the fundamental opacity problem in multi-agent workflows. When a five-node pipeline produces an incorrect final result, the question is always the same: which node went wrong, and what did it see? The debugger intercepts execution at configurable points, captures the full input/output state of every node, and lets you replay any node in isolation with modified inputs -- without re-running the entire pipeline.

## When to Use

- A pipeline completes but produces an incorrect or unexpected final result and you need to isolate which node diverged
- A node fails with an error and you need to see the exact input it received from upstream nodes
- You want to test how a node behaves with different inputs without re-running expensive upstream nodes
- You need to verify that intermediate data flowing between nodes matches your expectations
- A conditional branch took the wrong path and you need to inspect the values that drove the decision
- You are developing a new pipeline and want to validate each node's behavior incrementally

## When NOT to Use

- The pipeline is working correctly and you just want to see the final result -- use `cortivex_run` directly
- You only need cost or timing information -- use `cortivex_run --verbose` which includes per-node metrics
- The failure is in the pipeline YAML itself (syntax error, missing node type, cyclic dependency) -- the validator catches these before execution begins
- You want to profile performance bottlenecks -- use PerformanceProfiler nodes instead

## How It Works

### Debug Mode Activation

Debugging is activated by adding the `--debug` flag to `cortivex_run` or by calling `cortivex_debug` directly. When debug mode is active:

1. **Execution pauses before each node** -- The pipeline halts before a node begins processing, giving you a chance to inspect inputs and decide whether to continue, skip, or modify
2. **Full state capture** -- Every node's input, output, configuration, timing, and token usage is recorded in the execution trace
3. **Breakpoints are evaluated** -- Before each node executes, all breakpoints (unconditional and conditional) are checked. Execution pauses only at nodes with active breakpoints
4. **Watch expressions update** -- After each node completes, all registered watch expressions are evaluated against the node's output and displayed

### Execution Trace

The trace is a complete, ordered record of the pipeline run. Each entry contains:

- Node ID and type
- Full input payload (what the node received from upstream)
- Full output payload (what the node produced)
- Configuration used at runtime
- Duration, token count, and cost
- Any errors or warnings raised

The trace supports bidirectional navigation. You can step forward to the next node or backward to re-examine a previous node's state.

## Pipeline Configuration

### Enabling Debug Mode via YAML

Add a `debug` block to your pipeline definition to pre-configure breakpoints and watches:

```yaml
name: pr-review-debug
version: "1.0"
description: PR review pipeline with debugging enabled
debug:
  enabled: true
  breakpoints:
    - node: security_scan
      condition: "output.summary.critical > 0"
    - node: code_review
      condition: null
    - node: auto_fix
      condition: "output.files_modified > 10"
  watch:
    - expression: "security_scan.output.summary"
      label: "Security Summary"
    - expression: "code_review.output.issues | length"
      label: "Issue Count"
    - expression: "auto_fix.output.files_modified"
      label: "Files Changed"
  trace:
    capture_full_output: true
    max_output_size_kb: 512
    persist_trace: true
    trace_file: .cortivex/traces/last-debug.json

nodes:
  - id: security_scan
    type: SecurityScanner
    config:
      scan_depth: deep
      severity_threshold: medium

  - id: code_review
    type: CodeReviewer
    depends_on: [security_scan]
    config:
      review_scope: changed_files
      max_issues: 50

  - id: auto_fix
    type: AutoFixer
    depends_on: [code_review]
    config:
      fix_categories: [style, bugs]
      require_confirmation: false

  - id: test_run
    type: TestRunner
    depends_on: [auto_fix]
    config:
      test_command: npm test
      timeout_seconds: 300
```

### Runtime Debug Flag

Activate debugging on any existing pipeline without modifying its YAML:

```yaml
# Equivalent to adding debug.enabled: true
cortivex_run:
  pipeline: pr-review
  options:
    debug: true
    breakpoints:
      - node: auto_fix
```

## MCP Tool Reference

All debugging operations use the `cortivex_debug` MCP tool with an `action` parameter.

### Action: breakpoint

Set, remove, or list breakpoints on pipeline nodes.

**Request -- set unconditional breakpoint:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "breakpoint",
    "operation": "set",
    "node_id": "code_review",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Request -- set conditional breakpoint:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "breakpoint",
    "operation": "set",
    "node_id": "security_scan",
    "condition": "output.summary.critical > 0",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "status": "breakpoint_set",
  "breakpoint_id": "bp-001",
  "node_id": "security_scan",
  "condition": "output.summary.critical > 0",
  "active": true
}
```

**Request -- list all breakpoints:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "breakpoint",
    "operation": "list",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "breakpoints": [
    { "id": "bp-001", "node_id": "security_scan", "condition": "output.summary.critical > 0", "active": true, "hit_count": 0 },
    { "id": "bp-002", "node_id": "code_review", "condition": null, "active": true, "hit_count": 1 }
  ]
}
```

**Request -- remove breakpoint:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "breakpoint",
    "operation": "remove",
    "breakpoint_id": "bp-001",
    "run_id": "ctx-a1b2c3"
  }
}
```

### Action: step

Advance execution by one node in the pipeline. When paused at a breakpoint, `step` executes the current node and pauses before the next one.

**Request:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "step",
    "direction": "forward",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "status": "paused",
  "completed_node": {
    "id": "security_scan",
    "type": "SecurityScanner",
    "duration_seconds": 14,
    "cost": 0.003,
    "output_summary": "2 warnings, 0 critical"
  },
  "next_node": {
    "id": "code_review",
    "type": "CodeReviewer",
    "input_from": ["security_scan"],
    "has_breakpoint": true
  },
  "pipeline_progress": "1/4 nodes completed",
  "watches": [
    { "label": "Security Summary", "value": { "total_issues": 2, "critical": 0, "high": 1, "medium": 1 } }
  ]
}
```

**Stepping backward** re-examines a previously executed node's captured state. It does not re-execute the node:

```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "step",
    "direction": "backward",
    "run_id": "ctx-a1b2c3"
  }
}
```

### Action: inspect

Examine the full input, output, or configuration of any node that has executed or is about to execute.

**Request -- inspect node output:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "inspect",
    "node_id": "security_scan",
    "target": "output",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "node_id": "security_scan",
  "type": "SecurityScanner",
  "target": "output",
  "data": {
    "vulnerabilities": [
      {
        "severity": "high",
        "type": "sql_injection",
        "file": "src/db/queries.ts",
        "line": 47,
        "description": "User input directly interpolated into SQL query"
      }
    ],
    "summary": { "total_issues": 2, "critical": 0, "high": 1, "medium": 1 }
  },
  "size_bytes": 1842,
  "token_count": 312
}
```

**Request -- inspect what a node will receive as input (before it runs):**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "inspect",
    "node_id": "code_review",
    "target": "input",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Request -- inspect node configuration:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "inspect",
    "node_id": "auto_fix",
    "target": "config",
    "run_id": "ctx-a1b2c3"
  }
}
```

### Action: replay

Re-execute a specific node with its original or modified inputs. This does not affect other nodes in the trace -- it runs the target node in isolation and returns the new output.

**Request -- replay with original inputs:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "replay",
    "node_id": "auto_fix",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Request -- replay with modified inputs:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "replay",
    "node_id": "auto_fix",
    "modified_input": {
      "issues": [
        {
          "severity": "warning",
          "category": "style",
          "file": "src/utils/parser.ts",
          "line": 23,
          "description": "Inconsistent naming"
        }
      ]
    },
    "run_id": "ctx-a1b2c3"
  }
}
```

**Request -- replay with modified configuration:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "replay",
    "node_id": "auto_fix",
    "modified_config": {
      "fix_categories": ["style"],
      "require_confirmation": true,
      "model": "claude-haiku-4-20250414"
    },
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "status": "replay_complete",
  "node_id": "auto_fix",
  "original_output_hash": "a3f8c1...",
  "replay_output_hash": "b7d2e4...",
  "output_changed": true,
  "replay_output": {
    "files_modified": 2,
    "fixes_applied": [
      { "file": "src/utils/parser.ts", "line": 23, "fix": "Renamed variable to camelCase" }
    ]
  },
  "duration_seconds": 8,
  "cost": 0.002,
  "diff_from_original": "2 fewer fixes applied (style-only mode excluded bug fixes)"
}
```

### Action: watch

Register, remove, or evaluate watch expressions that are automatically evaluated after each node completes.

**Request -- add watch:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "watch",
    "operation": "add",
    "expression": "code_review.output.issues | filter(.severity == 'error') | length",
    "label": "Critical Issues",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "watch_id": "w-003",
  "label": "Critical Issues",
  "expression": "code_review.output.issues | filter(.severity == 'error') | length",
  "current_value": null,
  "status": "pending (code_review has not executed yet)"
}
```

**Request -- evaluate all watches now:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "watch",
    "operation": "evaluate",
    "run_id": "ctx-a1b2c3"
  }
}
```

### Action: continue

Resume execution from the current breakpoint until the next breakpoint is hit or the pipeline completes.

**Request:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "continue",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "status": "paused",
  "reason": "breakpoint",
  "breakpoint_id": "bp-003",
  "node_id": "auto_fix",
  "condition_met": "output.files_modified > 10 evaluated to true (files_modified = 14)",
  "nodes_executed_since_continue": ["code_review"],
  "pipeline_progress": "2/4 nodes completed"
}
```

### Action: trace

Retrieve the full execution trace or a filtered subset.

**Request -- full trace:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "trace",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "run_id": "ctx-a1b2c3",
  "pipeline": "pr-review",
  "status": "paused",
  "trace": [
    {
      "order": 1,
      "node_id": "security_scan",
      "type": "SecurityScanner",
      "status": "completed",
      "duration_seconds": 14,
      "cost": 0.003,
      "input_tokens": 2840,
      "output_tokens": 312,
      "input_hash": "e4a1b2...",
      "output_hash": "a3f8c1..."
    },
    {
      "order": 2,
      "node_id": "code_review",
      "type": "CodeReviewer",
      "status": "completed",
      "duration_seconds": 48,
      "cost": 0.018,
      "input_tokens": 5120,
      "output_tokens": 1456,
      "input_hash": "f2c3d4...",
      "output_hash": "c9e0f1..."
    },
    {
      "order": 3,
      "node_id": "auto_fix",
      "type": "AutoFixer",
      "status": "paused_at_breakpoint",
      "breakpoint_id": "bp-003"
    },
    {
      "order": 4,
      "node_id": "test_run",
      "type": "TestRunner",
      "status": "pending"
    }
  ],
  "total_cost_so_far": 0.021,
  "total_duration_so_far": 62
}
```

**Request -- trace filtered by node:**
```json
{
  "tool": "cortivex_debug",
  "arguments": {
    "action": "trace",
    "node_id": "security_scan",
    "include_io": true,
    "run_id": "ctx-a1b2c3"
  }
}
```

## Node Reference

| Node Type | Debugger Behavior | Inspectable Fields |
|-----------|------------------|-------------------|
| SecurityScanner | Breakpoint on severity thresholds | vulnerabilities, dependency_issues, secrets_found, summary |
| CodeReviewer | Breakpoint on issue count or severity | issues, summary, overall_quality |
| BugHunter | Breakpoint on confidence levels | bugs, edge_cases, summary |
| AutoFixer | Breakpoint on files_modified count | fixes_applied, files_modified, backup_paths |
| TestRunner | Breakpoint on test failures | passed, failed, coverage, error_output |
| Orchestrator | Breakpoint on branch decisions | condition_results, selected_branch, skipped_branches |
| CustomAgent | Breakpoint on any output field | full output per output_schema |

## Quick Reference

| Action | Purpose | Key Parameters |
|--------|---------|---------------|
| `breakpoint` | Set/remove/list breakpoints on nodes | `operation`, `node_id`, `condition` |
| `step` | Advance one node forward or backward | `direction` (forward/backward) |
| `inspect` | View input/output/config of any node | `node_id`, `target` (input/output/config) |
| `replay` | Re-run a node with modified inputs or config | `node_id`, `modified_input`, `modified_config` |
| `watch` | Track expressions across node executions | `expression`, `label`, `operation` |
| `continue` | Resume until next breakpoint or completion | (none required) |
| `trace` | Retrieve full or filtered execution trace | `node_id`, `include_io` |

## Best Practices

1. **Start with conditional breakpoints** -- Do not break on every node. Set conditions that target the specific failure mode you are investigating (e.g., `output.summary.critical > 0` or `output.files_modified > 10`). Unconditional breakpoints on every node turn debugging into tedious manual stepping.

2. **Inspect inputs before outputs** -- When a node produces a wrong result, first inspect its input. In the majority of cases, the problem is that the upstream node produced malformed output, not that the current node is broken. Follow the data upstream until you find where it diverged.

3. **Use replay to test hypotheses** -- When you suspect a node would succeed with different input, use `replay` with `modified_input` instead of re-running the entire pipeline. Replay executes only the target node, saving both time and cost. Compare the `output_hash` values to confirm whether the change had an effect.

4. **Set watches on key metrics early** -- Before running a debug session, register watches for the values you care about (issue counts, file modification counts, test pass rates). Watches update automatically after each step so you can spot problems as they emerge rather than inspecting nodes manually after the fact.

5. **Persist traces for regression analysis** -- Enable `persist_trace: true` in your debug configuration. Saved traces let you compare execution behavior across pipeline runs to identify regressions. When a pipeline that previously worked starts failing, diff the current trace against the saved successful trace to find what changed.

6. **Use backward stepping for root cause analysis** -- When you hit a breakpoint because a downstream node received bad data, step backward through the trace to find the originating node. Backward stepping does not re-execute nodes; it reads from the captured trace, so it is instant and free.

7. **Keep trace output sizes bounded** -- Set `max_output_size_kb` in the trace configuration to prevent memory issues on nodes that produce large outputs (e.g., ArchitectAnalyzer on large repositories). Truncated outputs are still inspectable via direct `inspect` calls.

## Reasoning Protocol

Before initiating a debug session, reason through these questions explicitly:

1. **What is the observable symptom?** State precisely what the pipeline did wrong. "The final output is wrong" is insufficient -- identify which aspect of the output is incorrect and what you expected instead.

2. **Which node is most likely responsible?** Based on the symptom, identify the node whose output domain matches the problem area. If the final PR summary is missing security findings, the problem is likely in SecurityScanner or the handoff between SecurityScanner and PRCreator.

3. **Is this an input problem or a processing problem?** Before setting breakpoints, decide whether you suspect the node received bad input (upstream fault) or produced bad output from good input (node fault). This determines whether you inspect inputs or outputs first.

4. **What condition would confirm the hypothesis?** Define the conditional breakpoint expression that would trigger exactly when the problem occurs. Vague breakpoints waste time; precise conditions like `security_scan.output.summary.critical > 0` let you skip past healthy executions.

5. **Can you reproduce with replay instead of a full re-run?** If you already have a trace from a failed run, use `replay` with modified inputs to test fixes. Only re-run the full pipeline when you have confirmed the fix works in isolation.

6. **What watches would make the problem visible?** Identify 2-3 expressions that track the key data points across the pipeline. Good watches make the problem obvious at a glance without requiring manual inspection of every node.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Setting unconditional breakpoints on every node | Turns debugging into tedious manual stepping through healthy nodes | Use conditional breakpoints that trigger only on the failure condition |
| Inspecting only the failing node | Misses upstream data corruption that caused the failure | Inspect the failing node's input first, then trace backward to the source |
| Re-running the full pipeline to test a fix | Wastes time and cost re-executing expensive upstream nodes | Use `replay` to re-run only the target node with modified inputs |
| Ignoring watch expressions | Forces manual inspection after every step, easy to miss gradual drift | Set watches on key metrics before starting the debug session |
| Not persisting traces | Loses the ability to compare against previous successful runs | Enable `persist_trace: true` and diff traces to find regressions |
| Debugging in production pipelines | Debug mode adds overhead and may expose intermediate data | Use `--dry-run` or run against a test repository with debug enabled |
| Using replay without checking input hashes | May not notice that the replay input differs from the original | Always compare `input_hash` values to confirm you are replaying with the intended data |

**WRONG:**
```yaml
# Breakpoint on every node, no conditions
debug:
  breakpoints:
    - node: security_scan
    - node: code_review
    - node: auto_fix
    - node: test_run
    - node: pr_update
```

**RIGHT:**
```yaml
# Targeted conditional breakpoints
debug:
  breakpoints:
    - node: security_scan
      condition: "output.summary.critical > 0"
    - node: auto_fix
      condition: "output.files_modified > 10"
  watch:
    - expression: "security_scan.output.summary"
      label: "Security Summary"
    - expression: "test_run.output.failed"
      label: "Failing Tests"
```

**WRONG:**
```python
# Re-running entire pipeline to test one node's behavior
cortivex_run(pipeline="pr-review", options={"debug": True})
# ... step through 4 nodes to get back to the one you care about
```

**RIGHT:**
```python
# Replay the specific node with modified input
cortivex_debug(
    action="replay",
    node_id="auto_fix",
    modified_input={"issues": filtered_issues},
    run_id="ctx-a1b2c3"
)
```

## Grounding Rules

- **Cannot determine which node caused the failure:** Start at the last node that produced output and inspect its input. Walk backward through the trace one node at a time until you find the first node whose output deviates from expectations. Do not guess -- follow the data.

- **Conditional breakpoint expression is uncertain:** Test the expression syntax by using `watch` first. Watch expressions use the same evaluation engine as breakpoint conditions. If the watch evaluates correctly, the condition will work as a breakpoint.

- **Replay produces different output but you are unsure why:** Compare the `modified_input` against the original input using `inspect`. Check the `input_hash` and `output_hash` to confirm the inputs are genuinely different. If hashes match but output differs, the node has non-deterministic behavior (check temperature settings).

- **Trace is too large to review manually:** Use filtered trace queries with `node_id` to examine specific nodes. Set `include_io: false` for an overview, then drill into specific nodes with `include_io: true`. Do not attempt to read the full trace of a 10+ node pipeline at once.

- **Debug session is taking too long:** If you have been stepping for more than 5 iterations without finding the root cause, re-evaluate your hypothesis. Step back, re-read the original symptom, and consider whether you are investigating the wrong node chain entirely.

## Advanced Capabilities

### Conditional Breakpoint Configuration

Conditional breakpoints support compound expressions, hit counts, and log-only mode. Use `ignore_count` to skip the first N hits, `hit_count_threshold` to auto-disable after a set number of triggers, and `mode: "log_only"` to record values without halting.

```json
{
  "tool": "cortivex_debug_breakpoint",
  "arguments": {
    "action": "set", "node_id": "code_review", "run_id": "ctx-d4e5f6",
    "condition": "output.issues | filter(.severity == 'critical') | length >= 3",
    "hit_count_threshold": 2, "mode": "break_and_log", "ignore_count": 1
  }
}
```

**Response:**
```json
{
  "status": "breakpoint_set",
  "breakpoint_id": "bp-adv-017",
  "node_id": "code_review",
  "hit_count_threshold": 2, "ignore_count": 1,
  "mode": "break_and_log", "active": true
}
```

### Trace Diffing & Comparison

Trace diffing compares two execution traces node-by-node, highlighting divergences in inputs and outputs. Fields like timing and cost can be excluded via `ignore_fields` to avoid false positives. The `highlight_first_divergence` flag identifies the earliest node where behavior changed.

```yaml
trace_comparison:
  baseline_trace: .cortivex/traces/2026-03-20-passing.json
  current_trace: .cortivex/traces/2026-03-23-failing.json
  comparison_mode: structural
  diff_options:
    ignore_fields: ["*.duration_seconds", "*.cost", "*.timestamp"]
    tolerance: { numeric_fields: 0.01, string_similarity: 0.95 }
    output_format: unified
  reporting:
    highlight_first_divergence: true
    max_diff_depth: 5
```

### Replay Debugging with Mutations

Replay mutations apply systematic transformations to a node's input before re-execution. When `cascade` is `true`, downstream nodes also re-execute with mutated output propagating through the DAG. Mutations are applied in array order to support chaining.

```json
{
  "$schema": "https://cortivex.dev/schemas/replay-mutation/v1.json",
  "properties": {
    "run_id": { "type": "string" },
    "node_id": { "type": "string" },
    "mutations": { "type": "array", "items": {
      "properties": {
        "mutation_id": { "type": "string" },
        "operation": { "enum": ["set", "delete", "append", "transform"] },
        "path": { "type": "string" },
        "value": {},
        "transform_expression": { "type": "string" }
      },
      "required": ["mutation_id", "operation", "path"]
    }},
    "execution_options": { "properties": {
      "capture_diff": { "type": "boolean", "default": true },
      "cascade": { "type": "boolean", "default": false },
      "timeout_seconds": { "type": "integer", "default": 120 }
    }}
  },
  "required": ["run_id", "node_id", "mutations"]
}
```

### Performance Flame Graph Generation

The profiler generates hierarchical flame graphs for time and token consumption across nodes. The `granularity: "sub_step"` setting decomposes each node into internal phases (prompt construction, LLM call, response parsing, validation) to isolate latency sources.

```json
{
  "tool": "cortivex_debug_profile",
  "arguments": {
    "action": "generate", "run_id": "ctx-d4e5f6",
    "profile_type": "flame_graph",
    "metrics": ["duration_ms", "token_count", "cost_usd"],
    "granularity": "sub_step", "include_llm_calls": true
  }
}
```

**Response:**
```json
{
  "status": "profile_generated",
  "profile_path": ".cortivex/profiles/ctx-d4e5f6-flame.html",
  "summary": { "total_duration_ms": 62400, "hotspot_node": "code_review", "hotspot_percentage": 62.3 },
  "top_offenders": [
    { "node_id": "code_review", "duration_ms": 38900, "tokens": 6576 },
    { "node_id": "security_scan", "duration_ms": 14200, "tokens": 3152 }
  ]
}
```

### Remote Debugging & Attach Mode

Remote attach mode connects to a pipeline running on a remote Cortivex server or CI environment. Set `read_only` to inspect without modifying state, `pause_on_attach` to halt the remote pipeline at its current node, and `trace_streaming` to push trace entries to the local client in real time.

```json
{
  "$schema": "https://cortivex.dev/schemas/remote-debug-session/v1.json",
  "properties": {
    "remote_host": { "type": "string", "format": "hostname" },
    "port": { "type": "integer", "default": 9229 },
    "auth": { "properties": {
      "method": { "enum": ["token", "mtls", "oidc"] },
      "credentials_ref": { "type": "string" }
    }, "required": ["method", "credentials_ref"] },
    "attach_options": { "properties": {
      "run_id": { "type": "string" },
      "pause_on_attach": { "type": "boolean", "default": false },
      "read_only": { "type": "boolean", "default": true },
      "sync_breakpoints": { "type": "boolean", "default": true },
      "trace_streaming": { "type": "boolean", "default": true }
    }}
  },
  "required": ["remote_host", "auth", "attach_options"]
}
```

```typescript
import { CortivexRemoteDebugger } from "@cortivex/debug-client";

const session = await CortivexRemoteDebugger.attach({
  host: "pipelines.internal.example.com", port: 9229,
  auth: { method: "mtls", certPath: "/etc/cortivex/client.pem" },
  runId: "ctx-remote-7890", readOnly: true,
});

session.onTraceEntry((entry) => {
  console.log(`[${entry.nodeId}] ${entry.status} - ${entry.durationMs}ms`);
});
session.onBreakpointHit((bp) => {
  console.log(`Breakpoint ${bp.id} hit at node ${bp.nodeId}`);
});
await session.waitForCompletion();
```

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for pipeline debugging operations, aligned with the OWASP Automated Security Testing (AST) risk taxonomy. Each subsection maps to a specific AST risk ID and provides enforceable configuration, validation schemas, and MCP tool integration examples.

### AST06: Production Debug Prevention

Debug mode exposes full node inputs, outputs, and agent reasoning chains. Per **AST06** (Insufficient Security Testing in Production), debug mode must be blocked in production environments by default to prevent accidental exposure of intermediate data, cost overruns from paused pipelines, and unauthorized inspection of live execution state.

```yaml
# .cortivex/security/debug-environment-policy.yaml
debug_environment_policy:
  environments:
    production:
      debug_allowed: false
      override_requires:
        role: security-lead
        mfa: true
        approval_count: 2
        approval_roles: [security-lead, platform-admin]
        max_override_duration_minutes: 30
        audit_all_actions: true
      ast_risk_id: AST06
    staging:
      debug_allowed: true
      restrictions:
        max_session_duration_minutes: 120
        read_only_by_default: true
        trace_auto_redact: true
    development:
      debug_allowed: true
      restrictions: null
  detection:
    environment_source: CORTIVEX_ENV       # environment variable
    fallback: production                    # assume production if unset
    reject_empty_env: true                  # block debug if env var is missing
```

MCP tool call that is rejected in production (AST06 enforcement):

```
cortivex_debug({
  action: "breakpoint",
  operation: "set",
  node_id: "code_review",
  run_id: "ctx-prod-5a3b"
})
```

```json
{
  "status": "denied",
  "reason": "Debug mode is blocked in production (AST06). Request override from security-lead with MFA.",
  "ast_risk_id": "AST06",
  "environment": "production",
  "override_instructions": {
    "required_role": "security-lead",
    "mfa_required": true,
    "approval_endpoint": "/api/debug/override-request"
  }
}
```

### Trace Data Sensitivity Classification

Debug traces capture full node inputs and outputs, which may contain secrets, PII, or proprietary algorithms in intermediate data. Per **AST06**, all intermediate data must be automatically classified by sensitivity level before it is written to the trace store.

```json
{
  "$schema": "https://cortivex.dev/schemas/trace-classification/v1.json",
  "title": "TraceSensitivityClassification",
  "type": "object",
  "required": ["classification_id", "rules", "enforcement"],
  "properties": {
    "classification_id": { "type": "string", "pattern": "^tcls-[a-z0-9-]+$" },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["label", "level", "patterns"],
        "properties": {
          "label": { "type": "string" },
          "level": { "enum": ["public", "internal", "confidential", "restricted"] },
          "patterns": { "type": "array", "items": { "type": "string" } },
          "node_types": { "type": "array", "items": { "type": "string" } },
          "auto_redact": { "type": "boolean", "default": false },
          "ast_risk_id": { "type": "string" }
        }
      }
    },
    "enforcement": {
      "type": "object",
      "properties": {
        "block_unclassified_traces": { "type": "boolean" },
        "default_level": { "enum": ["internal", "confidential"] },
        "escalate_on_restricted": { "type": "boolean" }
      }
    }
  }
}
```

```yaml
trace_sensitivity_classification:
  classification_id: tcls-pipeline-debug
  rules:
    - label: secrets-in-tool-args
      level: restricted
      patterns:
        - "(?i)(password|secret|token|api_key)\\s*[:=]"
        - "(sk-[a-zA-Z0-9]{32,})"
        - "(ghp_[a-zA-Z0-9]{36})"
      auto_redact: true
      ast_risk_id: AST06
    - label: pii-in-node-output
      level: confidential
      patterns:
        - "(\\b\\d{3}-\\d{2}-\\d{4}\\b)"
        - "(\\b[\\w.+-]+@[\\w-]+\\.[\\w.-]+\\b)"
      auto_redact: true
      ast_risk_id: AST06
    - label: security-scanner-findings
      level: confidential
      node_types: [SecurityScanner]
      patterns: []
      auto_redact: false
      ast_risk_id: AST06
  enforcement:
    block_unclassified_traces: true
    default_level: internal
    escalate_on_restricted: true
```

### Remote Debug Session Timeout and Auto-Disconnect

Remote debug sessions that remain open indefinitely create persistent attack surfaces. Per **AST06**, all remote debug sessions must enforce idle timeouts and maximum session durations, with automatic disconnection and trace cleanup.

```yaml
# .cortivex/security/debug-session-timeout.yaml
debug_session_timeout:
  max_session_duration_minutes: 60
  idle_timeout_minutes: 10
  warning_before_disconnect_seconds: 120
  auto_disconnect:
    enabled: true
    cleanup_actions:
      - release_all_breakpoints
      - resume_paused_pipeline
      - flush_trace_to_disk
      - revoke_session_credentials
  reconnect_policy:
    allowed: true
    require_re_authentication: true
    max_reconnect_attempts: 3
    cooldown_between_attempts_seconds: 30
  audit:
    log_session_start: true
    log_session_end: true
    log_idle_warnings: true
    log_forced_disconnects: true
    ast_risk_id: AST06
```

```typescript
interface DebugSessionTimeoutEvent {
  session_id: string;
  run_id: string;
  event_type: "idle_warning" | "idle_disconnect" | "max_duration_disconnect" | "manual_disconnect";
  session_duration_seconds: number;
  idle_duration_seconds: number;
  cleanup_actions_performed: string[];
  pipeline_resumed: boolean;
  ast_risk_id: "AST06";
  timestamp: string;                     // ISO 8601
}
```

```
cortivex_debug({
  action: "session_status",
  run_id: "ctx-remote-7890"
})
```

```json
{
  "session_id": "dbg-sess-4a2c",
  "run_id": "ctx-remote-7890",
  "status": "active",
  "connected_since": "2026-03-24T09:00:00Z",
  "idle_since": "2026-03-24T09:42:00Z",
  "time_to_idle_disconnect_seconds": 480,
  "time_to_max_duration_seconds": 1080,
  "ast_risk_id": "AST06"
}
```

### Mutation Replay Sandboxing

Cascade mutations propagate modified outputs through the DAG, potentially triggering unintended side effects in downstream nodes. Per **AST06**, all cascade mutation replays must execute in an isolated sandbox environment that prevents writes to the real filesystem, network calls to production services, and modifications to the pipeline state.

```json
{
  "$schema": "https://cortivex.dev/schemas/mutation-sandbox/v1.json",
  "title": "MutationReplaySandboxConfig",
  "type": "object",
  "required": ["sandbox_id", "isolation", "resource_limits"],
  "properties": {
    "sandbox_id": { "type": "string", "pattern": "^sbox-[a-z0-9-]+$" },
    "isolation": {
      "type": "object",
      "properties": {
        "filesystem": { "enum": ["copy-on-write", "tmpfs", "none"] },
        "network": { "enum": ["block-all", "allow-internal", "allow-all"] },
        "environment_variables": { "enum": ["inherit-safe", "clean", "custom"] },
        "process_isolation": { "type": "boolean", "default": true }
      }
    },
    "resource_limits": {
      "type": "object",
      "properties": {
        "max_cpu_seconds": { "type": "integer" },
        "max_memory_mb": { "type": "integer" },
        "max_disk_write_mb": { "type": "integer" },
        "max_execution_time_seconds": { "type": "integer" }
      }
    },
    "ast_risk_id": { "type": "string", "const": "AST06" }
  }
}
```

```yaml
mutation_replay_sandbox:
  sandbox_id: sbox-cascade-default
  isolation:
    filesystem: copy-on-write
    network: block-all
    environment_variables: inherit-safe    # strip secrets from env
    process_isolation: true
  resource_limits:
    max_cpu_seconds: 120
    max_memory_mb: 512
    max_disk_write_mb: 100
    max_execution_time_seconds: 180
  on_violation:
    action: terminate_and_report
    preserve_sandbox_state: true          # keep for forensic inspection
    alert_roles: [security-lead]
  audit:
    log_sandbox_creation: true
    log_resource_usage: true
    log_violations: true
    ast_risk_id: AST06
```

### Breakpoint Injection Prevention

Breakpoints control pipeline execution flow by pausing nodes and exposing internal state. Per **AST06**, only the pipeline owner or designated operators can set breakpoints. This prevents unauthorized users from injecting breakpoints to exfiltrate intermediate data or stall production pipelines.

```yaml
# .cortivex/security/breakpoint-authorization.yaml
breakpoint_authorization:
  policy: owner-and-operators-only
  roles_allowed:
    - pipeline-owner
    - operator
    - security-lead
  roles_denied:
    - viewer
    - anonymous
  enforcement:
    validate_on_set: true
    validate_on_modify: true
    reject_unauthorized_silently: false    # return explicit denial
    audit_all_attempts: true
  conditional_breakpoint_restrictions:
    max_condition_complexity: 50           # max AST nodes in expression
    forbidden_functions:
      - eval
      - exec
      - require
      - import
    sanitize_expressions: true            # prevent injection via condition strings
  ast_risk_id: AST06
```

```
cortivex_debug({
  action: "breakpoint",
  operation: "set",
  node_id: "security_scan",
  condition: "output.summary.critical > 0",
  run_id: "ctx-a1b2c3",
  auth: {
    identity: "viewer@example.com",
    role: "viewer"
  }
})
```

```json
{
  "status": "denied",
  "reason": "Role 'viewer' is not authorized to set breakpoints (AST06). Required: pipeline-owner, operator, or security-lead.",
  "ast_risk_id": "AST06",
  "requested_by": "viewer@example.com",
  "audit_logged": true
}
```

```typescript
interface BreakpointAuthorizationCheck {
  breakpoint_id: string;
  node_id: string;
  run_id: string;
  requester_identity: string;
  requester_role: string;
  authorized: boolean;
  denial_reason?: string;
  condition_sanitized?: boolean;
  condition_complexity_score?: number;
  ast_risk_id: "AST06";
}
```

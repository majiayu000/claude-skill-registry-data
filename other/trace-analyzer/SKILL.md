---
name: trace-analyzer
description: Analyzes LibrAgent agent session trace files (.trace.json) to understand what an AI agent actually did during a session. Use when a user shares a .trace.json file, asks "what did the agent do?", wants to debug agent behavior, investigate tool call patterns, validate concurrency limits, or review session results. The trace file is the raw conversation record between the agent and its tools.
---

# Trace Analyzer

Analyzes `.trace.json` files produced by LibrAgent agent sessions.

## Quick Start

Run the bundled script against the trace file:

```powershell
python .agents/skills/trace-analyzer/scripts/trace_dump.py <path-to-.trace.json>
```

The script outputs:

- Message count by role (user / assistant / tool)
- Every tool call with truncated args
- Every tool result (first line, success ✓ or error ✗)
- Every assistant text turn

## What to Look For

### Concurrency Gate Validation

`listProcesses` results during a load test reveal the active slot count:

- `Found N processes (M running, K finished)` — M should never exceed `active_process` limit (default: 10)
- If M < expected spawn count → gate is throttling correctly ✅

### Common Agent Errors

| Pattern                                 | Meaning                                                        |
| --------------------------------------- | -------------------------------------------------------------- |
| `✗ Unknown tool: <name>`                | Agent hallucinated a non-existent tool name                    |
| `✗ Timeout waiting for process`         | `waitForProcess` default 30s expired; agent used wrong timeout |
| `✗ Process '<id>' not found in session` | Cross-session ID leak or stale ID from prior session           |
| `✗ Scratchpad item ... already exists`  | Agent tried duplicate scratchpad write                         |

### Planning Behavior

Good agents: `createGoal → addTodo → work → checkTodo → clearGoal`  
Confused agents: repeated `addTodo` for same item, `getCurrentState` spam, never `clearGoal`

### Tool Call Frequency

High `pauseAndThink` / `getCurrentState` ratio relative to actual work calls = agent overthinking.  
Healthy ratio: ≤1 planning call per 3 work calls.

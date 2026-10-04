---
name: bench
description: |
  Run benchmark-style evaluations on AI agents or tools using parent-child session delegation.
  Use when the user wants to test an agent's performance on a set of problems (e.g. SWE-bench style,
  tool capability benchmark, coding challenge evaluation). The parent session orchestrates:
  spawns child sessions to solve individual problems, collects answers via checkSession,
  and generates a consolidated report with pass/fail scores and analysis.
  Triggers on: "bench 테스트 해줘", "SWE-bench 돌려줘", "agent benchmark", "tool evaluation".
---

# Bench

Run **benchmark evaluations** by delegating individual problems to child sessions and aggregating results into a report.

This skill turns LibrAgent's parent-child delegation primitives into a structured benchmarking workflow.

## Not This Skill

| Skill | Use for |
| --- | --- |
| **tool-creator** | Build a new MCP server (not testing one) |
| **setup-wizard** | Install runtime dependencies |
| **deep-research** | Multi-source research with web search |
| **consensus-delegation** | Multi-expert opinion triangulation on a single question |

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Parent Session                 │
│           (Orchestrator / Bench Agent)      │
│                                             │
│  1. Load benchmark definition               │
│  2. Spawn child sessions (one per problem)  │
│  3. Monitor progress with checkSession      │
│  4. Collect results                         │
│  5. Generate consolidated report            │
└──────┬──────────┬──────────┬────────────────┘
       │          │          │
  ┌────▼───┐ ┌───▼────┐ ┌──▼──────┐
  │Child 1 │ │Child 2 │ │Child N  │
  │(Worker)│ │(Worker)│ │(Worker) │
  └────────┘ └────────┘ └─────────┘
```

**Key primitives used:**

| Primitive | Role |
|---|---|
| `agent__listAgents(type="configs")` | Find the assistant to bench |
| `agent__spawnSession(task="...")` | Spawn a child worker for one problem |
| `agent__checkSession(sessionId, wait=true)` | Block until a child finishes, get its answer |
| `agent__checkSession(sessionId)` (poll) | Monitor progress without blocking |
| `agent__stopSession(sessionId)` | Cancel a stuck child |
| `agent__listAgents(type="sessions")` | See all active children |

## Benchmark Definition Format

Define problems as a JSON array or Markdown list. Each problem has:

```json
{
  "name": "swe-bench-lite",
  "description": "SWE-bench Lite verification set",
  "assistant": "Coding Expert",
  "problems": [
    {
      "id": "django__django-11890",
      "task": "Fix the validation error in django/forms/fields.py when...",
      "repository": "/path/to/django",
      "setup": "cd /path/to/django && pip install -e .[test]",
      "test_command": "python -m pytest tests/forms/tests.py::TestFields::test_null_field",
      "expected_output": "PASSED",
      "difficulty": "medium"
    }
  ]
}
```

Or use a simple text format:

```
Benchmark: Python Math Test
Assistant: Coding Expert
Problems:
  1. [easy] Solve: 2 + 2 * 3 = ?
  2. [medium] Write a function to calculate Fibonacci(n)
  3. [hard] Implement a binary search on a rotated sorted array
```

## Workflow

### 1. Load benchmark definition

Perform **Benchmark Discovery** upon receiving a request (e.g., "run swe-bench-lite" or a specific benchmark name):

1. **Check built-in benchmark map** for matching keys:
   - `"swe-bench-lite"`, `"tool-capability"`, `"python-coding"`, etc.
2. **Scan `benchmarks/` directory** if not found:
   - Search the **current session's workspace root** (via `workspace__listDirectory(path="benchmarks")` to search for relative `.json` or `.md` files under the active workspace directory, e.g. `benchmarks/swe-bench-lite.json`).
3. **Ask user** for the definition if still not found.
4. **Unified Loader (JSON + Markdown)**:
   - Parse JSON content as a structured JSON object if JSON format is detected.
   - Parse Markdown content using key headings (Benchmark/Assistant) and list items for problems if Markdown format is detected.

Example Unified Loader logic:
- Check for JSON content or parse file:
  `workspace__readFile(path="benchmarks/swe-bench-lite.json")`
- Or read markdown file:
  `workspace__readFile(path="benchmarks/tool-capability.md")`

Record: `benchmark.name`, `benchmark.assistant`, `benchmark.problems[]`.

### 2. Choose the assistant to bench

```
agent__listAgents(type="configs", query="Coding Expert")
```

Record the configuration `id` for `agent__spawnSession`. If the user names a custom assistant, use that configuration template ID (not a session ID).

### 3. Spawn child sessions & Execution Protocol

For each problem, spawn a child session. Construct the child's `task` prompt dynamically based on the available fields in the problem definition. Do not include static setup or verification headers if those fields are empty, as this will confuse the child worker.

**Benchmark isolation exception:** Do not reuse an existing child session for a benchmark problem. Each problem must start with a fresh session so prior conversation, runtime state, pending messages, and workspace artifacts cannot contaminate the result. Use `agent__spawnSession` even when an Idle session has the same assistant configuration.

#### Task Formulation Guidelines:
- Include the `Problem ID`, `Task` description, `Repository` path, and `Expected output` (if they exist in the problem definition).
- Conditionally add sequential steps to the instructions:
  - **If `setup` is present:** Include `1. Run setup command: <setup_command>`.
  - **Always include:** `2. Apply the fix for the task: <task_description>`.
  - **If `test_command` is present:** Include `3. Run verification command: <test_command>`.
  - **Always include at the end:** `Return your final result as a JSON block containing "exit_code", "stdout", "stderr", and "diff".`

#### Example of a Dynamically Formed Task:
```
Problem ID: django__django-11890
Task: Fix the validation error in django/forms/fields.py when the field value is None.
Repository: /path/to/django
Expected output: PASSED

Execution Instructions:
1. Run setup command: cd /path/to/django && pip install -e .[test]
2. Apply the fix for the task: Fix the validation error in django/forms/fields.py when the field value is None.
3. Run verification command: python -m pytest tests/forms/tests.py::TestFields::test_null_field
4. Return your final result as a JSON block:
{
  "exit_code": <number>,
  "stdout": "<string>",
  "stderr": "<string>",
  "diff": "<string>"
}
```

Spawn the session using `agent__spawnSession` with `waitForResult: false`.

#### Parent Judgment Rule with Fallback Strategy:
1. **Try JSON parsing:** Attempt to extract and parse the JSON block from the child's final response (using regex like `/\{[\s\S]*?\}/`).
2. **Evaluate code:** If JSON is successfully parsed, check `exit_code`. If `exit_code === 0`, mark the problem as `"passed"`. Otherwise, mark it as `"failed"`.
3. **Fallback check:** If JSON parsing fails (e.g. LLM format errors):
   - Scan stdout/stderr or the raw response for successful test keywords (e.g., `"PASSED"`, `"OK"`, `"tests passed"`).
   - If error indicators are found (e.g., `"AssertionError"`, `"FAILED"`, `"Error"`, or exit code > 0 in logs), mark it as `"failed"`.
   - If ambiguous, default to spawning a "judge" session or marking it as `"failed"` with the error "JSON parsing failed".

### Workspace Strategy

By default, child sessions run in isolated workspaces. However, SWE-bench style benchmarks require sharing a repository. Follow these strategy guidelines:

| Benchmark Type | `workspaceOverride` | Rationale |
|----------------|-------------------|-----------|
| **SWE-bench / repo fix** | `problem.repository` | Shared codebase — clone/build once, run tests in same env. Map path from problem definition. |
| **Multi-file refactor** | `problem.repository` | All changes evaluated against same codebase. Map path from problem definition. |
| **Tool capability test** | Omitted (isolated) | No shared state, failure isolation |
| **Code challenge** | Omitted (isolated) | Independent problems, no cross-contamination |
| **Cross-session dependency** | N/A | Not supported — use sequential mode |

#### Concurrency and Conflict Avoidance in Shared Workspaces:
- When child sessions share a codebase via `workspaceOverride`, they must modify different files or use isolated directories to avoid write-write conflicts.
- If multiple child sessions must modify the same files, you must switch from **Parallel** to **Sequential** execution mode.

Record all returned `sessionId` values in a map: `sessions[problem.id] = sessionId`.

### 4. Monitor progress

Poll children without blocking:

```
// Check all children every 30 seconds
for (const [id, sessionId] of Object.entries(sessions)) {
  const status = await agent__checkSession(sessionId);
  if (status.state === "completed") {
    results[id] = status.lastResponse;
  } else if (status.state === "error") {
    results[id] = `Error: ${status.error}`;
  }
}
```

Or wait for a specific child:

```
const result = await agent__checkSession(sessionId, wait=true, timeout=300);
```

### 5. Collect results

Parse the child's final response for each problem as the result:

```typescript
interface BenchmarkResult {
  problemId: string;
  sessionId: string;
  status: "passed" | "failed" | "error" | "timeout";
  answer: string;
  score: number;       // 0-1 or percentage
  latencyMs: number;   // time to complete
  tokensUsed?: number;
}
```

### 6. Generate report

Aggregate the results and generate a standardized Markdown report after all child sessions complete (either successfully, with error, or by timing out):

#### Step-by-Step Report Generation:
1. **Calculate Metrics:** Calculate the overall pass rate, average latency (ms), error rate, and total tokens used.
2. **Group Results:** Classify problems into `passed`, `failed`, `error`, or `timeout`.
3. **Analyze Common Failure Patterns:** For all failed, error, and timeout problems, identify common issues (e.g., installation errors, syntax errors, incorrect API calls, logic bugs) and suggest recommendations.
4. **Output standard Markdown:** Save or return the report using the following structure:

```markdown
# Benchmark Report: {name}

## Summary
- **Total:** N problems
- **Passed:** X ({X/N}%)
- **Failed:** Y
- **Errors/Timeouts:** Z
- **Avg Latency:** T ms

## Results

| # | Problem ID | Status | Score | Latency | Key Output / Error |
|---|------------|--------|-------|---------|---------------------|
| 1 | django-11890 | ✅ passed | 1.0 | 45s | Exit code 0, 3 tests passed |
| 2 | flask-2048 | ❌ failed | 0.0 | 120s | AssertionError: NaN handling |
| 3 | ... | ⚠️ error | 0.0 | - | Timeout after 300s |

## Failure & Error Analysis

### Common Failure Patterns
- **Pattern A (e.g., Dependencies Setup Failed):** 2 problems failed during `setup` due to missing virtual environments.
- **Pattern B (e.g., Assertion Failure):** 3 problems failed because the agent did not handle edge cases correctly.

### Problem Details

#### django-11890 (Passed)
- **Latency:** 45s
- **Diff:**
```diff
...
```

#### flask-2048 (Failed)
- **Expected:** The field should accept null values
- **Got:** {child's answer snippet or stderr}
- **Analysis:** The agent introduced a syntax error when handling JSON serialization of NaN values.
- **Recommendation:** Verify environment setup has `simplejson` installed or ensure the agent uses native json module properly.
```

## Advanced Patterns

### Parallel vs Sequential

| Mode | When | How |
|---|---|---|
| **Parallel** (default) | Independent problems | Spawn all children, poll with `checkSession` |
| **Sequential** | Dependencies between problems | Wait for each child before spawning next |

### Timeout Handling

```
// If a child exceeds timeout
const status = await agent__checkSession(sessionId, wait=true, timeout=300);
if (status.state === "running" && status.timedOut) {
  await agent__stopSession(sessionId);
  results[id] = { status: "timeout", answer: "Timed out after 300s" };
}
```

### Fanout Limit

By default, child sessions inherit the parent's `maxFanout`. If you need to bench many problems:

```
agent__spawnSession({
  configId: "...",
  task: "...",
  maxFanout: 20   // Override parent limit for this child
})
```

### Result Verification

When verifying results, use the most lightweight and accurate verification method. Simple text or exit-code checks should be handled directly by the Parent agent. Spawn a separate judge session only for complex semantic comparisons.

| Verification Type | Who | How |
|-------------------|-----|-----|
| **Exit code check** | Parent | `exit_code == 0 → passed`, else `failed` |
| **Exact string match** | Parent | `child.answer.trim() === expected.trim()` |
| **Partial match** | Parent | `child.answer.includes(expected_keyphrase)` |
| **Test output parsing** | Parent | Use RegExp on stdout/stderr (e.g., `/(\d+) passed/` or `/OK/`) |
| **Semantic correctness** | Judge session | Spawn a critic agent (e.g., "Master Mind") to evaluate the output against expected reference and return JSON |

## Script Reference

| Step | Tool | Parameters |
|---|---|---|
| Find assistant | `agent__listAgents` | `{ type: "configs", query: "..." }` |
| Spawn child | `agent__spawnSession` | `{ configId, task, waitForResult: false }` |
| Poll child | `agent__checkSession` | `{ sessionId }` |
| Wait for child | `agent__checkSession` | `{ sessionId, wait: true, timeout: 300 }` |
| Stop stuck child | `agent__stopSession` | `{ sessionId }` |
| List children | `agent__listAgents` | `{ type: "sessions" }` |
| Read file | `workspace__readFile` | `{ path: "benchmarks/..." }` |

## Guidelines

- **Isolate workspaces by default** — children should not share the parent's workspace unless explicitly needed (`workspaceOverride`). When sharing, write to separate files or use sequential mode to avoid conflicts.
- **Set timeouts** — always specify `timeout` on `checkSession(wait=true)` to prevent infinite waits.
- **Limit fanout** — be mindful of `maxFanout` limits; spawn in batches if needed.
- **Verify results** — don't trust child answers blindly; use automated exit-code and stdout/stderr verification when available, and only delegate to a judge session for semantic verification.
- **Clean up** — stop any remaining children after the benchmark completes.
- **Report format** — use consistent Markdown tables for readability.
- **English output** — benchmark reports in English unless the user specifies otherwise.

## References

These reference markdown files are located in the skill directory's `references/` subdirectory:
- [benchmark-templates.md](references/benchmark-templates.md) — example benchmark definitions
- [result-aggregation.md](references/result-aggregation.md) — patterns for scoring and analysis

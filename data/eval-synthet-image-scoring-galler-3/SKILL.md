---
name: eval
description: Capture task quality signals and log them to agent memory to build a
  feedback loop. Use at the end of each implemented task or merged PR.
---

# /eval — Feedback-loop capture

Eval design — building feedback loops with verifiable signals — is a core agentic
skill. Run this at the **end of each implemented task or merged PR** so that what
worked (and what didn't) becomes durable, queryable agent memory instead of being
lost between sessions.

## When to use

- Immediately after `/implement` finishes and tests are green.
- Right after a PR merges.
- After abandoning or re-scoping a task (capture the *why*).

## Step 1 — Record the three signals

Collect these verifiable signals for the task you just finished:

| Signal | Values | How to measure |
|--------|--------|----------------|
| `test_pass_rate` | `yes` / `partial` / `no` | Did the test suite (or the task's failing stubs) end fully green? `partial` = some still red/skipped. |
| `first_try_success` | `yes` / `no` | Did the implementation pass its tests on the first run, with no rework cycle? |
| `iteration_count` | integer (≥ 1) | Number of implement→test→fix cycles before done. |

## Step 2 — Map the outcome to a memory candidate

Use the signals to decide **what** to remember and **how confident** to be:

| Outcome | Memory candidate type | Confidence |
|---------|----------------------|------------|
| First-try success, all tests green | `successful_pattern` | `high` |
| More than 2 iterations to finish | `recurring_issue` | `medium` |
| Tests were missing (no stubs existed before implementation) | `working_rule` | `high` |

Write the candidate as a concise, factual statement (active voice), e.g.:
- `successful_pattern`: "IPC handlers in `electron/main.ts` are fastest to land when the
  failing stub is written in `electron/__tests__` first."
- `recurring_issue`: "`database.engine: api` changes repeatedly break because the SQL
  shape isn't validated against the backend contract before coding."
- `working_rule`: "Always author a failing test stub for new `db.ts` query helpers
  before implementing — tasks that skipped this needed 3+ iterations."

## Step 3 — Log the candidate to agent memory

Persist the candidate so future sessions can retrieve it. Example logging call:

```bash
/log-session --candidate \
  --type successful_pattern \
  --confidence high \
  --signals "test_pass_rate=yes,first_try_success=yes,iteration_count=1" \
  --note "IPC handler tasks land first-try when the failing stub is written first."
```

In this repo the durable store is the **Memory MCP knowledge graph** (see the
`memory-mcp` skill). If `/log-session` is not wired up, equivalently call the Memory
MCP directly: `search_nodes` first to avoid duplicates, then `add_observations`
(existing entity) or `create_entities` (new), tagging the candidate `type` and
`confidence` and including the three signals as observations.

## Done when

- The three signals are recorded for the task.
- A memory candidate (type + confidence) has been written to agent memory, or you
  explicitly noted that no candidate was warranted.

## See also

- `memory-mcp` skill — the durable agent-memory store this feedback loop writes to.
- `/log-session` — session/candidate logging entry point (when configured).
- `/implement` — tests-first execution that produces the signals captured here.

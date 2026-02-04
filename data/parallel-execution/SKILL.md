---
name: parallel-execution
description: Executes parallel subagents using Task tool for concurrent operations. Use when facing multiple independent tasks, debugging separate failures, or parallelizing features. Triggers include "parallel tasks", "concurrent", "spawn subagent", "multiple failures", or "dispatch agents".
allowed-tools: Task, TaskOutput, TodoWrite, Bash
user-invocable: true
---

# Parallel Execution Patterns

## Core Concept

Parallel execution spawns multiple subagents simultaneously using the Task tool with `run_in_background: true`. This enables N tasks to run concurrently, dramatically reducing total execution time.

**Critical Rule**: ALL Task calls MUST be in a SINGLE assistant message for true parallelism. If Task calls are in separate messages, they run sequentially.

## When to Use Parallel Execution

### Good Candidates

- Multiple independent failures (different test files, different subsystems)
- Multi-file processing where files are independent
- Multiple analyses (security, performance, testing)
- Feature implementation with independent components
- Exploratory tasks with different perspectives

### Don't Parallelize When

- Tasks have dependencies (Task B needs Task A's output)
- Failures are related (fix one might fix others)
- Tasks modify the same files (conflict risk)
- Need to understand full system state first
- Order matters for correctness

### Decision Flow

```
Multiple tasks?
  ├─ No → Single agent handles all
  └─ Yes → Are they independent?
              ├─ No (related) → Single agent investigates together
              └─ Yes → Can work in parallel?
                         ├─ No (shared state) → Sequential agents
                         └─ Yes → PARALLEL DISPATCH
```

## Execution Protocol

### Step 1: Identify Independent Domains

Group tasks by what's broken or what needs doing:

```
Example - Test Failures:
- File A tests: Tool approval flow
- File B tests: Batch completion behavior
- File C tests: Abort functionality

Each domain is independent - fixing one doesn't affect others.
```

### Step 2: Create Focused Agent Prompts

Each subagent gets:

- **Specific scope:** One test file or subsystem
- **Clear goal:** Make these tests pass / implement this feature
- **Constraints:** Don't change other code
- **Expected output:** Summary of findings and changes

```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expects 'interrupted at'
2. "should handle mixed completed and aborted tools" - fast tool aborted
3. "should properly track pendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by replacing arbitrary timeouts with event-based waiting

Do NOT just increase timeouts - find the real issue.

Return: Summary of what you found and what you fixed.
```

### Step 3: Launch All Tasks in ONE Message

**CRITICAL**: Make ALL Task calls in the SAME assistant message:

```
I'm launching 3 parallel subagents:

[Task 1]
description: "Fix agent-tool-abort.test.ts"
prompt: "[detailed instructions]"
run_in_background: true

[Task 2]
description: "Fix batch-completion.test.ts"
prompt: "[detailed instructions]"
run_in_background: true

[Task 3]
description: "Fix tool-approval.test.ts"
prompt: "[detailed instructions]"
run_in_background: true
```

### Step 4: Retrieve Results

After launching, retrieve each result:

```
TaskOutput: task_1_id
TaskOutput: task_2_id
TaskOutput: task_3_id
```

### Step 5: Review and Integrate

When agents return:

1. **Review each summary** - Understand what changed
2. **Check for conflicts** - Did agents edit same code?
3. **Run full suite** - Verify all fixes work together
4. **Integrate all changes** - Merge if no conflicts

## Parallelization Patterns

### Pattern 1: Task-Based

When you have N tasks to implement, spawn N subagents:

```
Plan:
1. Implement auth module
2. Create API endpoints
3. Add database schema
4. Write unit tests

Spawn 4 subagents (one per task)
```

### Pattern 2: Directory-Based

Analyze multiple directories simultaneously:

```
Directories: src/auth, src/api, src/db

Spawn 3 subagents:
- Subagent 1: Analyzes src/auth
- Subagent 2: Analyzes src/api
- Subagent 3: Analyzes src/db
```

### Pattern 3: Perspective-Based

Review from multiple angles:

```
Spawn 4 subagents:
- Subagent 1: Security review
- Subagent 2: Performance analysis
- Subagent 3: Test coverage review
- Subagent 4: Architecture assessment
```

### Pattern 4: Failure-Based

Debug multiple independent failures:

```
6 failures across 3 files:

Spawn 3 subagents:
- Agent 1 → Fix agent-tool-abort.test.ts (3 failures)
- Agent 2 → Fix batch-completion.test.ts (2 failures)
- Agent 3 → Fix tool-approval.test.ts (1 failure)
```

## Prompt Best Practices

**❌ Too broad:** "Fix all the tests" - agent gets lost
**✅ Specific:** "Fix agent-tool-abort.test.ts" - focused scope

**❌ No context:** "Fix the race condition" - agent doesn't know where
**✅ Context:** Paste the error messages and test names

**❌ No constraints:** Agent might refactor everything
**✅ Constraints:** "Do NOT change production code" or "Fix tests only"

**❌ Vague output:** "Fix it" - you don't know what changed
**✅ Specific:** "Return summary of root cause and changes"

## TodoWrite Integration

**Sequential execution**: Only ONE task `in_progress` at a time
**Parallel execution**: MULTIPLE tasks can be `in_progress` simultaneously

```
# Before launching parallel tasks
todos = [
  { content: "Task A", status: "in_progress" },
  { content: "Task B", status: "in_progress" },
  { content: "Task C", status: "in_progress" },
  { content: "Synthesize results", status: "pending" }
]

# After completion
todos = [
  { content: "Task A", status: "completed" },
  { content: "Task B", status: "completed" },
  { content: "Task C", status: "completed" },
  { content: "Synthesize results", status: "in_progress" }
]
```

## Performance Benefits

| Approach   | 5 Tasks @ 30s each          | Total Time |
| ---------- | --------------------------- | ---------- |
| Sequential | 30s + 30s + 30s + 30s + 30s | ~150s      |
| Parallel   | All 5 run simultaneously    | ~30s       |

Parallel execution is approximately **Nx faster** where N is the number of independent tasks.

## Troubleshooting

**Tasks running sequentially?**
- Verify ALL Task calls are in SINGLE message
- Check `run_in_background: true` is set for each

**Results not available?**
- Use TaskOutput with correct task IDs
- Wait for tasks to complete before retrieving

**Conflicts in output?**
- Ensure tasks don't modify same files
- Add conflict resolution in synthesis step

## Real Example

**Scenario:** 6 test failures across 3 files after refactoring

**Dispatch:**
```
Agent 1 → Fix agent-tool-abort.test.ts
Agent 2 → Fix batch-completion-behavior.test.ts
Agent 3 → Fix tool-approval-race-conditions.test.ts
```

**Results:**
- Agent 1: Replaced timeouts with event-based waiting
- Agent 2: Fixed event structure bug (threadId in wrong place)
- Agent 3: Added wait for async tool execution to complete

**Integration:** All fixes independent, no conflicts, full suite green

**Time saved:** 3 problems solved in ~30s vs ~90s sequential

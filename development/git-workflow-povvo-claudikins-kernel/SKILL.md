---
name: git-workflow
description: Use when running claudikins-kernel:execute, decomposing plans into tasks, setting up two-stage review, deciding batch sizes, or handling stuck agents — enforces isolation, verification, and human checkpoints; prevents runaway parallelization and context death
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - TodoWrite
  - Skill
  - mcp__plugin_claudikins-tool-executor_tool-executor__search_tools
  - mcp__plugin_claudikins-tool-executor_tool-executor__get_tool_schema
  - mcp__plugin_claudikins-tool-executor_tool-executor__execute_code
---

# Git Workflow Methodology

## When to use this skill

Use this skill when you need to:

- Run the `claudikins-kernel:execute` command
- Decompose plans into executable tasks
- Set up two-stage code review
- Decide batch sizes and checkpoints
- Handle stuck agents or failed tasks

## Core Philosophy

> "I'd use 5-7 agents per SESSION, not 30 per batch." - Boris

Execution is about isolation, verification, and human checkpoints. Not speed.

### The Six Principles

1. **One task = one branch** - Isolation prevents pollution
2. **Fresh context per task** - `context: fork` gives a clean slate
3. **Two-stage review** - Spec compliance first, then code quality
4. **Human checkpoints between batches** - Not between individual tasks
5. **Commands own git** - Agents never checkout/merge/push
6. **Features are the unit** - Batch at feature level, not task level

### Batch Size Guidance (GOSPEL)

**Wrong:** 30 agents for 10 tasks (3 per task micro-management)
**Right:** 5-7 agents total (feature-level batches)

| Scenario             | Wrong                      | Right              |
| -------------------- | -------------------------- | ------------------ |
| 10 tasks, 5 features | 30 micro-task agents       | 5-7 feature agents |
| Simple refactor      | 10 agents for tiny changes | 1-2 feature agents |

Default `--batch 1` is correct. Features are the unit of work.

## Task Decomposition

From a plan, extract tasks that are:

| Quality         | Definition                                     | Example                                       |
| --------------- | ---------------------------------------------- | --------------------------------------------- |
| **Atomic**      | Completable in one agent session               | "Add auth middleware" not "Build auth system" |
| **Testable**    | Has measurable acceptance criteria             | "Returns 401 for invalid token"               |
| **Independent** | Minimal dependencies on other tasks            | Can be reviewed in isolation                  |
| **Right-sized** | Not too small (noise) or large (context death) | 50-200 lines of changes                       |

See [task-decomposition.md](references/task-decomposition.md) for patterns.

## Review Stages

Two reviewers with different jobs. Never skip either.

### Stage 1: Spec Compliance (spec-reviewer, opus)

**Question:** "Did it do what was asked?"

Checks:

- All acceptance criteria addressed?
- Any scope creep (features not in spec)?
- Any missing requirements?

Output: `PASS` or `FAIL` with line references.

### Stage 2: Code Quality (code-reviewer, opus)

**Question:** "Is it well-written?"

Checks:

- Consistency with codebase style
- Error handling
- Edge cases
- Naming clarity
- Unnecessary complexity

Output: `PASS` or `CONCERNS` with confidence scores.

See [review-criteria.md](references/review-criteria.md) for detailed checklists.

## Review Enforcement (MANDATORY)

**This is non-negotiable. Violations here break the entire workflow.**

### The Iron Rule

After EVERY task completes, you MUST spawn BOTH reviewer agents:

1. **spec-reviewer** - Spawned via `Task(spec-reviewer, {...})`
2. **code-reviewer** - Spawned via `Task(code-reviewer, {...})` (if spec passes)

### What "MUST spawn" Means

| Allowed | NOT Allowed |
|---------|-------------|
| `Task(spec-reviewer, { prompt: "...", context: "fork" })` | Inline spec check by orchestrator |
| `Task(code-reviewer, { prompt: "...", context: "fork" })` | "I'll just verify the code looks good" |
| Waiting for agent output JSON | Making your own compliance table |
| Reading from `.claude/reviews/spec/` | Skipping because "it's a simple task" |

### Inline Reviews Are VIOLATIONS

If you find yourself doing ANY of these, you are VIOLATING the methodology:

- Creating a "Spec Compliance Check" table yourself
- Writing "Verdict: PASS" without spawning an agent
- Saying "Let me verify the implementation meets criteria"
- Checking acceptance criteria in a loop instead of delegating

**The orchestrator does NOT review. The orchestrator SPAWNS reviewers.**

### Pre-Merge Checklist (HARD GATE)

Before ANY merge decision can be offered to the user:

```
□ .claude/reviews/spec/{task_id}.json EXISTS for each task
□ .claude/reviews/code/{task_id}.json EXISTS for each task
□ Both files contain valid JSON with "verdict" field
□ spec-reviewer verdict is PASS (or user override documented)
```

If ANY file is missing: **DO NOT proceed to merge. You skipped the review.**

### Why This Matters

1. **Consistency** - Every task gets the same rigor, not "looks simple, I'll check it"
2. **Auditability** - Review outputs are artifacts, not orchestrator judgments
3. **Separation of concerns** - Orchestrator orchestrates, reviewers review
4. **No rationalization** - You can't convince yourself your inline check is "good enough"

## Verdict Matrix

What happens when reviewers return their verdicts:

| Spec Result | Code Result | Action                                           |
| ----------- | ----------- | ------------------------------------------------ |
| PASS        | PASS        | Offer [Accept] [Revise anyway]                   |
| PASS        | CONCERNS    | Offer [Accept with caveats] [Fix] [Klaus review] |
| FAIL        | \*          | Always [Revise] or [Retry]                       |

See [review-conflict-matrix.md](references/review-conflict-matrix.md) for edge cases.

## Batch Checkpoint Flow

```
All tasks in batch complete?
├── No → Wait for remaining
└── Yes →
    All reviews pass?
    ├── No →
    │   Retry count < 3?
    │   ├── Yes → Retry failed tasks
    │   └── No → Escalate to Klaus or human
    └── Yes →
        Present results to human
        └── Human decides: [Accept] [Revise] [Retry]
```

See [batch-patterns.md](references/batch-patterns.md) for decision trees.

## Rationalizations to Resist

Agents under pressure find excuses. These are all violations:

| Excuse                                     | Reality                                                             |
| ------------------------------------------ | ------------------------------------------------------------------- |
| "30 agents is fine, tasks are independent" | More agents = more chaos. 5-7 per session, features as units.       |
| "I'll just checkout main to compare"       | Agents don't own git. Use `git show main:file` instead.             |
| "Skip spec review, code looks correct"     | Spec review catches scope creep. Never skip.                        |
| "I'll do the review myself, it's simple"   | Spawn the reviewer agents. Inline reviews are VIOLATIONS.           |
| "Both passed, auto-merge is safe"          | Human checkpoint required. Always.                                  |
| "Context is fine, I'll continue"           | ACM at 60% = checkpoint offer. 75% = mandatory stop.                |
| "This tiny task doesn't need a branch"     | One task = one branch. No exceptions. Isolation prevents pollution. |
| "Retry limit is just a guideline"          | 2 retries then escalate. Infinite retry = infinite waste.           |
| "I'll merge my changes when done"          | Commands own merge. You own implementation. Stay in your lane.      |

**All of these mean: Follow the methodology. Speed is not the goal.**

## Red Flags — STOP and Reassess

If you're thinking any of these, you're about to violate the methodology:

- "Let me just run git checkout..."
- "30 tasks, 30 agents, maximum parallelism"
- "Review passed, no need for human checkpoint"
- "Context is getting tight but I can finish"
- "This is simple, don't need isolation"
- "I'll merge it myself"
- "Retry limit doesn't apply here"
- "Spec review is redundant if code review passes"
- "Let me verify the implementation meets criteria" (SPAWN THE AGENT)
- "I'll create a quick compliance table" (SPAWN THE AGENT)

**All of these mean: STOP. Commands own git. Humans own checkpoints. Reviewers own reviews. You own orchestration.**

## Robustness Patterns

Things go wrong. Here's how to handle them.

### SubagentStop Hook Failure (A-6)

If the capture hook fails, agent output is lost.

**Pattern:** Write to backup location first, then move to primary.

```bash
# Always backup first
echo "$OUTPUT" > "$BACKUP_DIR/agent-$(date +%s).json"
# Then move to primary
mv "$BACKUP_DIR/..." "$PRIMARY"
```

### Malformed JSON Output (A-7)

Agents sometimes produce invalid JSON.

**Pattern:** Validate required fields before accepting.

```bash
REQUIRED='["task_id", "status"]'
jq -e "all($REQUIRED[]; has(.))" "$OUTPUT" || exit 2
```

### Task Branch Directory Export (A-8)

Agents need to know where to work.

**Pattern:** Export directory as environment variable in SubagentStart hook.

```bash
export TASK_BRANCH_DIR="$PROJECT_DIR"
export TASK_BRANCH_NAME="execute/task-${TASK_ID}-${SLUG}"
```

### Model Rate Limiting (A-10)

Opus gets rate limited more than Sonnet.

**Pattern:** Offer fallback options to human.

1. Notify: "Opus rate limited. Options:"
2. Offer: [Wait 60s] [Use Sonnet fallback] [Abort]
3. If fallback, add caveat to review output

### Context Exhaustion Mid-Task (A-11)

Agent runs out of context before finishing.

**Pattern:** Output partial state and mark as resumable.

```json
{
  "status": "partial",
  "files_changed": ["completed work..."],
  "next_steps": ["what remains..."],
  "checkpoint_hash": "sha256:..."
}
```

### Dependency Failure Chains (S-7)

Task Y depends on Task X. Task X fails. What happens to Y?

See [dependency-failure-chains.md](references/dependency-failure-chains.md).

### Branch Collision (S-8)

Two tasks accidentally get the same branch name.

See [branch-collision-detection.md](references/branch-collision-detection.md).

### Branch Guard Recovery (S-9)

The git-branch-guard hook blocks something it shouldn't.

See [branch-guard-recovery.md](references/branch-guard-recovery.md).

### Batch Size Verification (S-10)

Validating batch sizes before execution starts.

See [batch-size-verification.md](references/batch-size-verification.md).

### Task Branch Recovery (S-12)

Recovering orphaned branches from crashed sessions.

See [task-branch-recovery.md](references/task-branch-recovery.md).

### Circuit Breakers (S-13)

Preventing cascading failures when operations fail repeatedly.

**Pattern:** Track failure rate. If threshold exceeded, "open" the circuit - fail fast without attempting.

```
Circuit: agent_spawn
State: OPEN (3 failures in 60s)
Reset in: 30 seconds

[Wait for reset] [Force close] [Skip operation]
```

See [circuit-breakers.md](references/circuit-breakers.md).

### Execution Tracing (S-14)

Debugging execution graphs and understanding what happened.

**Pattern:** Record spans for each operation. Visualise as waterfall or dependency graph.

```
Trace: exec-session-xyz
├── batch_1 (45s)
│   ├── task-1 (20s) ✓
│   └── task-2 (25s) ✓
└── batch_2 (60s)
    └── task-3 (60s) ✓

Critical path: batch_1 → batch_2
```

See [execution-tracing.md](references/execution-tracing.md).

## Stuck Detection

| Signal                | Threshold                     | Response            |
| --------------------- | ----------------------------- | ------------------- |
| Tool call flooding    | 20 calls without file changes | Warning, then Klaus |
| Time without progress | 10 minutes                    | Warning, then Klaus |
| Repeated failures     | Same error 3x                 | Pause, offer Klaus  |
| Context burn rate     | ACM at 60%                    | Checkpoint offer    |
| Review timeout        | 5 minutes per reviewer        | Offer [Wait] [Skip] |

## Anti-Patterns

**Don't do these:**

- Running git checkout/merge/push from agents
- Batching 30+ tasks in parallel
- Skipping spec review because "code looks fine"
- Auto-merging without human checkpoint
- Ignoring stuck signals
- Continuing after context warnings

## References

Full documentation in this skill's references/ folder:

- [task-decomposition.md](references/task-decomposition.md) - How to break down plans
- [review-criteria.md](references/review-criteria.md) - What reviewers check (400 LOC threshold, attack surface tracing)
- [batch-patterns.md](references/batch-patterns.md) - Checkpoint decision patterns (coordinated checkpoints, load shedding, deadline propagation)
- [dependency-failure-chains.md](references/dependency-failure-chains.md) - When dependent tasks fail
- [branch-collision-detection.md](references/branch-collision-detection.md) - Preventing duplicate branches
- [branch-guard-recovery.md](references/branch-guard-recovery.md) - Recovering from guard failures
- [batch-size-verification.md](references/batch-size-verification.md) - Validating batch sizes
- [review-conflict-matrix.md](references/review-conflict-matrix.md) - Handling reviewer disagreements (RESOLVE framework)
- [task-branch-recovery.md](references/task-branch-recovery.md) - Recovering orphaned branches
- [circuit-breakers.md](references/circuit-breakers.md) - Preventing cascading failures (circuit breaker pattern, timeout strategies)
- [execution-tracing.md](references/execution-tracing.md) - Debugging execution graphs (spans, traces, critical path analysis)

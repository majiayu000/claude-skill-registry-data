---
name: error-coordinator
description: Cross-agent error resolution and recovery coordination. Use when multiple agents encounter related failures, errors cascade across task boundaries, partial.
---

# Error Coordinator

Specialized expertise in classifying, correlating, and recovering from errors across multi-agent execution contexts. This skill provides structured frameworks for triaging failures, selecting recovery strategies, preventing cascading errors, and reconciling partial results when agents fail mid-task.

## When to Use This Skill

Use this skill for:

- Multiple agents encountering related or identical failures
- Errors that cascade from one delegated task to dependent downstream tasks
- Partial results that need reconciliation after agent failures
- Systematic diagnosis requiring correlation of failures across different execution contexts
- Recovery planning when retry, re-delegation, or escalation decisions must be made
- Post-failure analysis to improve future agent delegation patterns

**Trigger phrases**: "error coordination", "agent failure", "cascade failure", "partial results", "error recovery", "re-delegate", "agent retry", "failure correlation", "error triage", "blast radius", "graceful degradation", "error propagation", "circuit breaker"

## What This Skill Does

Provides structured error management including:

- **Error Classification**: Categorizing failures by type, severity, and recoverability
- **Cross-Agent Correlation**: Identifying shared root causes across parallel agent failures
- **Recovery Selection**: Choosing between retry, re-delegation, escalation, and graceful degradation
- **Cascade Prevention**: Circuit-breaking error propagation chains before they spread
- **Result Reconciliation**: Merging partial outputs and compensating for missing results
- **Post-Failure Learning**: Documenting patterns to improve future delegation and prompts

## Instructions

### Step 1: Error Classification and Triage

When an agent reports a failure (or produces unexpected output), classify the error before taking any recovery action. Premature retries waste tokens; misclassified errors lead to repeated failures.

**Error Taxonomy**:

| Category | Description | Examples | Default Action |
|----------|-------------|----------|----------------|
| **Transient** | Temporary condition, likely to succeed on retry | Rate limits, network timeouts, file locks, API throttling | Retry with backoff |
| **Permanent** | Fundamental issue that will not self-resolve | Missing permissions, invalid schema, unsupported operation, logic errors | Re-delegate or escalate |
| **Partial** | Task partially completed before failure | Agent produced some files but crashed, incomplete refactor, half-applied migration | Salvage results, re-delegate remainder |
| **Semantic** | Agent completed without error but produced wrong results | Misunderstood requirements, wrong file modified, incorrect logic implemented | Re-delegate with refined prompt |
| **Resource** | Exhausted a constrained resource | Context window exceeded, token budget depleted, disk full | Reduce scope or split task |

**Severity Levels**:

| Level | Criteria | Response Time |
|-------|----------|---------------|
| **Critical** | Blocks all downstream tasks; data loss risk; corrupted state | Immediate intervention |
| **High** | Blocks multiple dependent tasks; significant rework needed | Address before continuing any dependent work |
| **Medium** | Blocks one task; workaround available | Address in current coordination cycle |
| **Low** | Cosmetic or non-blocking; results usable despite error | Queue for batch resolution |

**Blast Radius Assessment**:

For every error, determine how far the failure can propagate:

1. **Direct impact**: Which tasks depend on the failed task's output?
2. **Indirect impact**: Which tasks depend on the directly impacted tasks?
3. **Shared resource impact**: Did the failure corrupt shared state (files, databases, configuration)?
4. **Confidence impact**: Are other completed results now suspect because they shared assumptions with the failed task?

**Triage Decision Matrix**:

```
Error detected
  │
  ├─ Is the error transient?
  │   ├─ YES → Retry (Step 3: retry path)
  │   └─ NO ↓
  │
  ├─ Did the agent produce any usable output?
  │   ├─ YES → Salvage partial results (Step 6), re-delegate remainder (Step 4)
  │   └─ NO ↓
  │
  ├─ Is the root cause understood?
  │   ├─ YES → Re-delegate with refined context (Step 4)
  │   └─ NO ↓
  │
  ├─ Are multiple agents failing similarly?
  │   ├─ YES → Cross-agent correlation (Step 2)
  │   └─ NO ↓
  │
  └─ Escalate to human operator with diagnostic bundle
```

**Error Log Template**:

```markdown
## Error Log Entry

**Timestamp**: [ISO 8601]
**Agent ID**: [agent identifier or task name]
**Task**: [brief description of delegated task]
**Error Category**: Transient | Permanent | Partial | Semantic | Resource
**Severity**: Critical | High | Medium | Low

### Error Details
- **Error message**: [exact error text]
- **Exit code / status**: [if applicable]
- **Files affected**: [list of paths]
- **Last successful operation**: [what the agent completed before failure]

### Blast Radius
- **Direct dependents**: [tasks blocked by this failure]
- **Indirect dependents**: [tasks transitively blocked]
- **Shared state impact**: [any corruption of shared files or config]

### Initial Assessment
- **Root cause hypothesis**: [best current understanding]
- **Recoverability**: High | Medium | Low
- **Recommended action**: Retry | Re-delegate | Escalate | Salvage + re-delegate
```

### Step 2: Cross-Agent Error Correlation

When multiple agents fail (or produce unexpected results), the failures may share a common root cause. Correlating errors before attempting individual recovery prevents wasted effort and repeated failures.

**Correlation Procedure**:

1. **Collect error logs** from all failed or suspect agents using the template from Step 1
2. **Align timelines**: Order failures chronologically to identify the initial failure point
3. **Identify shared factors**: Look for common elements across failures

**Shared Factor Analysis Table**:

| Factor | Questions to Ask | Correlation Signal |
|--------|-----------------|-------------------|
| **Shared input** | Did multiple agents receive the same incorrect input data? | Multiple agents misinterpret the same requirement |
| **Shared dependency** | Do the failing agents depend on the same upstream task or resource? | Failures cluster around one dependency |
| **Shared environment** | Are agents hitting the same API, file system, or service? | Transient errors at similar timestamps |
| **Shared assumption** | Were agents given the same (flawed) context or instructions? | Semantic errors producing similarly wrong output |
| **Shared constraint** | Are agents exhausting the same resource pool? | Resource errors appearing in sequence |

**Timeline Reconstruction Template**:

```markdown
## Failure Timeline

| Time | Agent | Event | Category | Notes |
|------|-------|-------|----------|-------|
| T+0m | Agent-A | Started task: implement auth middleware | - | - |
| T+2m | Agent-B | Started task: implement auth routes | - | - |
| T+5m | Agent-A | FAILED: cannot read config schema | Permanent | Missing schema file |
| T+6m | Agent-B | FAILED: cannot read config schema | Permanent | Same missing file |
| T+6m | - | CORRELATION: shared dependency on config schema | - | Root cause identified |

### Root Cause
[Description of the common root cause]

### Affected Agents
[List all agents impacted by this root cause]

### Resolution
[Single fix that addresses all correlated failures]
```

**Correlation Decision Logic**:

- If 2+ agents fail with the same error message or on the same resource, treat as a single root cause (fix once, not per-agent)
- If agents fail at similar times but with different errors, investigate shared environmental factors (API outages, permission changes, disk space)
- If agents fail at different times with similar semantic errors, investigate shared context or prompt deficiencies
- If no correlation is found, treat each failure independently per the triage matrix in Step 1

### Step 3: Recovery Strategy Selection

After classifying the error (Step 1) and checking for correlations (Step 2), select the appropriate recovery strategy. The decision depends on error recoverability, token cost, and downstream urgency.

**Recovery Decision Tree**:

```markdown
## Recovery Decision Tree

Is the error transient?
  ├─ YES: Has retry budget been exhausted? (max 2 retries per task)
  │   ├─ YES → Re-delegate to a different agent or escalate
  │   └─ NO → Retry with exponential backoff
  │
  └─ NO: Is the error a semantic mismatch (wrong output, not a crash)?
      ├─ YES → Re-delegate with refined prompt (Step 4)
      │
      └─ NO: Is the error a resource exhaustion?
          ├─ YES → Split the task into smaller units and re-delegate
          │
          └─ NO: Is partial output available and usable?
              ├─ YES → Salvage partial results (Step 6), re-delegate remainder
              │
              └─ NO: Is the root cause understood?
                  ├─ YES → Re-delegate with root cause context (Step 4)
                  └─ NO → Escalate to human operator
```

**Recovery Strategy Comparison**:

| Strategy | When to Use | Token Cost | Risk | Speed |
|----------|------------|------------|------|-------|
| **Retry (same agent)** | Transient errors; no state corruption | Low (re-executes same prompt) | May hit same error | Fast |
| **Re-delegate (new agent)** | Permanent errors; semantic failures; need fresh context | Medium (new agent, new prompt) | New agent may lack context | Medium |
| **Split and re-delegate** | Resource exhaustion; task too large | High (multiple new agents) | Coordination overhead | Slow |
| **Graceful degradation** | Non-critical task; deadline pressure | None (accept reduced quality) | Output gaps | Immediate |
| **Escalate** | Unknown root cause; data safety concerns; repeated failures | None (human takes over) | Delays resolution | Variable |

**Partial Result Salvage Criteria**:

Before discarding a failed agent's output, evaluate what can be kept:

1. **Completeness check**: Did the agent finish any discrete subtasks fully?
2. **Correctness check**: Are the completed portions correct (not just present)?
3. **State check**: Did the partial work leave shared resources in a consistent state?
4. **Dependency check**: Can downstream tasks use the partial output as-is?

If all four checks pass for a portion of the output, keep it and re-delegate only the remainder.

**Recovery Decision Matrix Template**:

```markdown
## Recovery Decision: [Task Name]

**Error Category**: [from Step 1]
**Severity**: [from Step 1]
**Correlation**: [standalone | correlated with Agent-X, Agent-Y]
**Partial Output Available**: Yes (N% complete) | No
**Retry Attempts Used**: [0/2, 1/2, 2/2]

### Options Evaluated

| Option | Feasibility | Token Cost | Time | Risk |
|--------|------------|------------|------|------|
| Retry | [High/Med/Low] | [est. tokens] | [est. time] | [description] |
| Re-delegate | [High/Med/Low] | [est. tokens] | [est. time] | [description] |
| Split | [High/Med/Low] | [est. tokens] | [est. time] | [description] |
| Degrade | [High/Med/Low] | None | Immediate | [what is lost] |
| Escalate | Always feasible | None | Unknown | [blocks everything] |

### Selected Strategy
**Action**: [chosen strategy]
**Rationale**: [why this strategy over alternatives]
**Fallback**: [what to do if this strategy also fails]
```

### Step 4: Re-delegation with Refined Context

When re-delegating a failed task, the new agent must receive better context than the original. Simply repeating the same prompt produces the same failure. Analyze why the original delegation failed and craft an improved prompt.

**Failure Analysis Checklist**:

Before re-delegating, answer these questions about the original failure:

1. **Prompt clarity**: Was the task description ambiguous or incomplete?
2. **Missing context**: Did the agent lack files, schemas, or background it needed?
3. **Scope mismatch**: Was the task too large for a single agent context window?
4. **Wrong agent type**: Did the task need a specialist agent (e.g., a testing agent, not a coding agent)?
5. **Constraint violation**: Did the agent violate an unstated constraint?
6. **Environmental issue**: Was the failure caused by external factors (API state, file system, permissions)?

**Re-delegation Prompt Template**:

```markdown
## Re-delegated Task: [Task Name]

### Previous Attempt Summary
A previous agent attempted this task and failed. Here is the relevant context:
- **What was attempted**: [brief description]
- **What succeeded**: [any partial results to build on]
- **What failed**: [specific failure point]
- **Root cause**: [why it failed]
- **Files already modified**: [list, so the new agent does not duplicate work]

### Task Description
[Refined, more specific task description addressing the gaps that caused the original failure]

### Explicit Constraints
- [Constraint 1 that was previously implicit]
- [Constraint 2 addressing the failure mode]
- [Constraint 3 scope boundary]

### Required Context
- [File path 1]: [why this file is needed]
- [File path 2]: [why this file is needed]
- [Schema/API doc]: [reference]

### Expected Output
- [Specific deliverable with format]
- [Verification criteria the agent should check before reporting completion]

### Known Pitfalls
- [Pitfall 1 from previous failure]
- [Pitfall 2 from error correlation]
```

**Scope Adjustment Guidelines**:

| Original Problem | Adjustment |
|-----------------|------------|
| Agent ran out of context window | Split into 2-3 smaller tasks with explicit boundaries |
| Agent misunderstood requirements | Add concrete examples and counter-examples to the prompt |
| Agent modified wrong files | Provide an explicit allowlist of files to read and modify |
| Agent used wrong approach | Specify the approach or algorithm to use, not just the goal |
| Agent missed edge cases | List edge cases explicitly in the task description |

**Agent Type Selection for Re-delegation**:

| Failure Pattern | Consider Switching To |
|----------------|----------------------|
| Logic errors in implementation | A planning agent first, then a coding agent |
| Test failures not caught | A dedicated testing agent |
| Security issues introduced | A security-review agent |
| Performance problems | A performance-analysis agent |
| Documentation gaps | A documentation agent |

### Step 5: Cascade Prevention

Errors propagate through task dependency chains. A single failure can trigger a cascade that invalidates work across many agents. Active cascade prevention limits blast radius and protects completed work.

**Error Propagation Patterns**:

```
Pattern 1: Linear Cascade
  Task A fails → Task B uses bad output → Task C builds on B → all invalid

Pattern 2: Fan-Out Cascade
  Task A fails → Tasks B, C, D all depend on A → all blocked

Pattern 3: Shared State Corruption
  Task A corrupts shared config → Tasks B, C read corrupted config → silent failures

Pattern 4: Assumption Cascade
  Task A produces wrong schema → Task B generates code from wrong schema →
  Task C writes tests for wrong code → everything passes but is incorrect
```

**Circuit-Breaking Rules**:

1. **Halt dependents immediately**: When a task fails, pause all tasks that depend on its output before they consume tokens processing bad input
2. **Validate before propagating**: Before passing any agent's output to a dependent task, verify the output against expected constraints (file exists, schema validates, tests pass)
3. **Checkpoint completed work**: After each successful task, snapshot the results so that a later failure does not require re-executing already-completed work
4. **Isolate shared state mutations**: If multiple agents must modify the same file or resource, serialize their access and validate state between modifications

**Cascade Prevention Checklist**:

```markdown
## Cascade Prevention: [Error Context]

### Immediate Actions
- [ ] Identified all tasks directly dependent on the failed task
- [ ] Paused/cancelled dependent tasks that have not yet started
- [ ] Notified in-progress dependent tasks to halt (if possible)
- [ ] Verified shared state integrity (files, config, database)

### Blast Radius Containment
- [ ] Mapped the full dependency chain from failed task to leaf tasks
- [ ] Identified which completed tasks may have consumed bad output
- [ ] Flagged completed tasks for re-verification if they used suspect output
- [ ] Protected known-good completed work from being overwritten by recovery actions

### Recovery Ordering
- [ ] Root cause task will be recovered first
- [ ] Dependent tasks ordered by dependency depth (closest first)
- [ ] Tasks with no dependency on the failure continue unblocked
- [ ] Re-verification of suspect completed tasks scheduled after root fix
```

**Shared State Protection Protocol**:

When multiple agents operate on shared resources (files, databases, configuration):

1. **Before delegation**: Document which agent owns write access to which resources
2. **During execution**: No two agents should write to the same file concurrently
3. **After failure**: Check that partially written files are either complete and correct, or reverted to their pre-task state
4. **Recovery**: If shared state is corrupted, restore from the last known-good checkpoint before re-delegating

### Step 6: Result Reconciliation Under Failure

When some agents succeed and others fail, the coordinator must assemble the best possible output from available results. This requires gap analysis, quality assessment, and sometimes compensating for missing pieces.

**Reconciliation Procedure**:

1. **Inventory available results**: List every agent's output status (complete, partial, missing, suspect)
2. **Map coverage**: Compare available results against the original task breakdown to identify gaps
3. **Assess quality**: Verify that available results meet quality criteria (not just "present" but "correct")
4. **Plan compensation**: For each gap, determine whether to re-delegate, work around, or accept the gap

**Result Inventory Template**:

```markdown
## Result Inventory: [Overall Task Name]

| Subtask | Agent | Status | Output Quality | Usable? |
|---------|-------|--------|---------------|---------|
| Auth middleware | Agent-A | Complete | Verified, tests pass | Yes |
| Auth routes | Agent-B | Failed | No output | No |
| Auth tests | Agent-C | Partial | 3 of 7 test files written | Partially |
| Auth docs | Agent-D | Complete | Not verified | Needs review |

### Coverage Analysis
- **Fully covered**: Auth middleware (100%)
- **Partially covered**: Auth tests (43%)
- **Not covered**: Auth routes (0%), remaining auth tests (57%)

### Gap Resolution Plan
| Gap | Priority | Strategy | Estimated Cost |
|-----|----------|----------|---------------|
| Auth routes | Critical (blocks integration) | Re-delegate with refined prompt | ~5K tokens |
| Remaining auth tests | High | Re-delegate, provide existing 3 test files as context | ~3K tokens |
| Auth docs verification | Low | Defer to final review phase | ~1K tokens |
```

**Quality Assessment for Degraded Output**:

When accepting partial results, evaluate the overall deliverable against these criteria:

| Criterion | Full Quality | Acceptable Degradation | Unacceptable |
|-----------|-------------|----------------------|--------------|
| **Functionality** | All features work | Core features work; edge cases deferred | Core features broken |
| **Correctness** | All logic verified | Main paths verified; secondary paths flagged | Unverified logic in production paths |
| **Completeness** | All deliverables present | Primary deliverables present; secondary deferred | Primary deliverables missing |
| **Consistency** | All components follow same patterns | Minor style variations | Contradictory implementations |
| **Testability** | Full test coverage | Core paths tested; gaps documented | No tests for changed code |

**Compensating for Missing Results**:

When a gap cannot be immediately filled (budget exhausted, deadline pressure, external blocker):

1. **Document the gap**: Record exactly what is missing and why
2. **Stub the missing piece**: Create placeholder code, documentation, or configuration with clear TODO markers
3. **Protect consumers**: Ensure that code depending on the missing piece fails loudly (assertions, type errors) rather than silently
4. **Track for follow-up**: Add the gap to a task backlog with priority and context

### Step 7: Post-Failure Review and Learning

After resolving errors and completing (or closing) the task, conduct a structured review to improve future delegations. This step converts individual failure incidents into systematic improvements.

**Failure Pattern Documentation Template**:

```markdown
## Post-Failure Review: [Task/Incident Name]

**Date**: [ISO 8601]
**Duration**: [time from first error to resolution]
**Total Recovery Cost**: [estimated tokens spent on recovery]

### Failure Summary
- **Original task**: [what was being attempted]
- **Error category**: [from Step 1 taxonomy]
- **Root cause**: [final determined root cause]
- **Blast radius**: [how many tasks were affected]
- **Recovery strategy used**: [from Step 3]

### Timeline
| Phase | Duration | Action |
|-------|----------|--------|
| Detection | [time] | [how the error was noticed] |
| Triage | [time] | [classification and severity assignment] |
| Correlation | [time] | [cross-agent analysis if applicable] |
| Recovery | [time] | [strategy execution] |
| Verification | [time] | [confirming the fix worked] |

### What Went Well
- [Positive aspect 1]
- [Positive aspect 2]

### What Could Improve
- [Improvement area 1]
- [Improvement area 2]

### Action Items
| Action | Category | Priority |
|--------|----------|----------|
| [Improve prompt template for X] | Prompt Quality | High |
| [Add validation gate before Y] | Cascade Prevention | Medium |
| [Switch agent type for Z tasks] | Agent Selection | Low |
```

**Prompt Improvement Recommendations**:

Based on common failure patterns, apply these prompt refinements:

| Failure Pattern | Prompt Improvement |
|----------------|-------------------|
| Agent misunderstood scope | Add an explicit "out of scope" section listing what NOT to do |
| Agent missed edge cases | Include a "known edge cases" section with specific examples |
| Agent used wrong approach | Specify the approach in the prompt; reference existing patterns in the codebase |
| Agent modified wrong files | Provide an allowlist of files to modify and a denylist of files to leave untouched |
| Agent ran out of context | Reduce task scope; pre-summarize large files; provide only relevant excerpts |
| Agent produced inconsistent style | Include a code sample demonstrating the expected style |

**Agent Selection Refinements**:

Track which agent types succeed or fail at which task categories:

```markdown
## Agent Performance Log

| Task Category | Agent Type | Outcome | Notes |
|---------------|-----------|---------|-------|
| API implementation | General coding | Success | - |
| Complex refactor | General coding | Failed (semantic) | Needs planning agent first |
| Security hardening | General coding | Failed (missed issues) | Use security specialist |
| Test generation | General coding | Partial | Dedicated test agent preferred |
| Documentation | General coding | Success | - |
| Performance tuning | General coding | Failed | Use performance specialist |
```

Over time, this log reveals which task types warrant specialist agents versus general-purpose agents.

**Escalation Criteria Updates**:

After each failure review, refine when to escalate rather than retry:

- Escalate immediately if the same root cause has appeared 3+ times across different tasks
- Escalate if recovery cost exceeds 50% of the original task's token budget
- Escalate if the error involves data integrity or irreversible state changes
- Escalate if the root cause is outside the agent system's control (infrastructure, permissions, third-party APIs)

## Integration with Other Skills

When coordinating error recovery, invoke related skills at appropriate phases:

| Phase | Related Skills |
|-------|---------------|
| Error Classification | `context-analysis`, `debugging` |
| Recovery Planning | `task-coordinator`, `plan-before-code` |
| Re-delegation | `task-coordinator` (handoff protocol) |
| Cascade Prevention | `code-quality`, `security-review` |
| Result Reconciliation | `context-manager`, `code-quality` |
| Post-Failure Review | `technical-documentation` |

## Quality Checklist

- [ ] Every error classified by taxonomy category and severity level
- [ ] Cross-agent correlations checked before individual recovery
- [ ] Recovery strategy selected using the decision tree (not ad hoc)
- [ ] Re-delegation prompts include failure context and refined constraints
- [ ] Dependent tasks paused or cancelled to prevent cascade
- [ ] Partial results inventoried and quality-assessed before merging
- [ ] Post-failure review completed with actionable improvements documented

## Related Skills

- `task-coordinator` - Task decomposition and multi-agent handoff protocols
- `context-manager` - Managing information across tasks and agent contexts
- `plan-before-code` - Upfront planning to reduce error likelihood
- `debugging` - Root cause analysis techniques for individual errors
- `code-quality` - Quality standards that prevent common failure modes

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Multi-agent error handling patterns, circuit breaker principles, incident response best practices


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.

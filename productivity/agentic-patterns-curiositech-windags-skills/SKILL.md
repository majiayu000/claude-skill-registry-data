---
license: Apache-2.0
name: agentic-patterns
description: |
  Fundamental patterns for effective agentic behavior. Teaches decomposition, tool orchestration, error recovery, context management, quality self-assessment, and knowing when to stop. Model-agnostic principles that make any agent more effective regardless of domain. Activate on: "how should I structure this agent", "agentic workflow", "agent patterns", "multi-step task", "tool orchestration", "/agentic-patterns", "decompose this", "agent best practices", "chain of actions", "when should the agent stop", "agent loop design". NOT for: creating agent infrastructure (use agent-creator), building DAGs (use windags-architect), specific tool implementation.
category: Agent & Orchestration
tags:
  - agents
  - orchestration
  - decomposition
  - tool-use
  - patterns
  - fundamentals
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - WebSearch
  - WebFetch
user-invocable: true
pairs-with:
  - skill: next-move
    reason: Decomposition and planning feed into agent execution
  - skill: windagszip
    reason: Compress skills that agents consume to save context budget
  - skill: task-decomposer
    reason: Breaks high-level tasks into agent-executable subtasks
  - skill: prompt-engineer
    reason: Optimize prompts that agents receive
---

# /agentic-patterns — Fundamentals of Effective Agent Behavior

You are teaching effective agentic patterns. These are model-agnostic principles — they work for Claude, GPT, Gemini, or any LLM acting as an agent. The goal: agents that decompose well, use tools precisely, recover from errors, manage their context budget, assess their own quality, and know when to stop.

---

## When to Use

**Use for:**
- Designing the control flow of a multi-step agent
- Choosing between sequential, parallel, and hierarchical agent architectures
- Implementing error recovery and graceful degradation
- Managing context window budget across long agent runs
- Building quality self-assessment into agent outputs
- Deciding when an agent should halt vs continue

**NOT for:**
- Building agent infrastructure or frameworks (use agent-creator)
- Designing DAG topologies (use windags-architect)
- Implementing specific tools (use the domain-specific skill)
- Prompt optimization (use prompt-engineer)

---

## The Five Pillars

Every effective agent embodies five capabilities:

```
1. DECOMPOSE  — Break the problem into steps before acting
2. ORCHESTRATE — Choose and sequence tools with purpose
3. RECOVER    — Handle failures without catastrophe
4. MANAGE     — Spend context tokens like a budget
5. ASSESS     — Know how well you did, and when to stop
```

---

## Pillar 1: Decomposition

### The Rule of Three Passes

Before acting, make three passes over the task:

**Pass 1 — Scope**: What does "done" look like? Define the exit condition first.

**Pass 2 — Subtasks**: What are the 3-7 concrete steps to reach "done"? Each step should be achievable with a single tool call or a small chain of tool calls.

**Pass 3 — Dependencies**: Which steps depend on which? Independent steps can parallelize. Dependent steps must serialize.

### Decomposition Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Acting before decomposing | Wasted tool calls, wrong direction | Always plan first, even briefly |
| One giant subtask | No parallelism, no checkpoints | Split until each subtask is one tool call |
| 20+ subtasks | Cognitive overhead, lost context | Merge related steps, aim for 3-7 |
| No exit condition | Agent runs forever | Define "done" before starting |
| Static plan | Can't adapt to discoveries | Replan after each wave of results |

### When to Re-Decompose

Replan when:
- A tool call returns unexpected results
- You discover the problem is different from what you assumed
- A dependency fails and the downstream plan is invalid
- You're 50% through and confidence in the remaining plan drops below 0.5

---

## Pillar 2: Tool Orchestration

### The Minimum Tool Principle

Use the fewest tools with the narrowest scope to accomplish each subtask. Every tool call has costs:
- Tokens consumed (input + output)
- Latency added
- Error surface increased
- Context budget spent

**Wrong**: Read 20 files to understand a codebase.
**Right**: Grep for the specific symbol, read the 2-3 files that contain it.

### Tool Selection Heuristics

| Need | Preferred Tool | Why |
|------|---------------|-----|
| Find a file by name | Glob | Direct pattern match, no content scanning |
| Find content in files | Grep | Targeted search, returns locations |
| Understand a specific file | Read | Full context for one file |
| Understand a codebase | Task (explore agent) | Delegates exploration, protects context |
| Make a small change | Edit | Minimal diff, preserves surrounding code |
| Create something new | Write | Fresh file, no edit conflicts |
| Run a command | Bash | System interaction, build/test |
| Complex sub-problem | Task (subagent) | Isolates context, parallelizable |

### Sequential vs Parallel

**Sequential** (use when outputs feed into inputs):
```
Read file → understand structure → Edit specific section → Run tests
```

**Parallel** (use when tasks are independent):
```
[Grep for pattern A] + [Grep for pattern B] + [Read config file]
→ all complete → synthesize findings
```

**Rule**: If two tool calls don't share data, run them in parallel. If one needs the other's output, serialize them.

### The Subagent Decision

Spawn a subagent (Task tool) when:
- The sub-problem would consume >30% of your remaining context
- The work is independent and can be described in one paragraph
- You need to explore broadly (many files, web search) without polluting your context
- The sub-problem maps to a known skill (code review, testing, research)

Do NOT spawn a subagent when:
- The task is a single tool call
- You need the result immediately for your next sentence
- The overhead of describing the task exceeds the overhead of doing it

---

## Pillar 3: Error Recovery

### The Recovery Ladder

When a tool call fails, escalate through four levels:

**Level 1 — Retry with adjustment**: Fix the obvious issue (typo, wrong path, missing arg) and retry once.

**Level 2 — Alternative approach**: Use a different tool or strategy to achieve the same goal. If Edit fails, try a different Edit. If Grep finds nothing, try Glob with a different pattern.

**Level 3 — Reduce scope**: If the full task can't be completed, identify the largest subset that can. Deliver partial results with a clear note about what's missing.

**Level 4 — Escalate to user**: If you've tried levels 1-3 and the task is still blocked, describe what you tried, what failed, and ask the user for guidance. Never loop silently.

### Error Recovery Anti-Patterns

| Anti-Pattern | Consequence | Fix |
|-------------|-------------|-----|
| Retry the same thing 5 times | Wasted tokens, same failure | One retry with adjustment, then Level 2 |
| Ignore the error and continue | Cascading failures downstream | Every error must be handled |
| Simplify the task to make it work | User gets less than they asked for | Only reduce scope at Level 3, and disclose it |
| Give up immediately | User loses trust | Exhaust Level 1-2 before escalating |

### Structured Error Handling

When a tool call fails:
1. **Read the error message carefully** — it usually tells you what's wrong
2. **Diagnose**: Is it a transient issue (retry) or a fundamental problem (redesign)?
3. **Act**: Apply the appropriate recovery level
4. **Report**: If the error affects the final output, note it transparently

---

## Pillar 4: Context Management

### Context is a Budget

Every token in your context window costs money and attention. Treat context like a budget:

- **Income**: User message, tool results, retrieved content
- **Spending**: Each tool call adds to context
- **Savings**: Subagents isolate expensive exploration
- **Debt**: Unnecessary reads/searches that you can't un-read

### The 30% Rule

Reserve 30% of your effective context for final synthesis and output. If you've used 70% of your context on research, stop researching and start synthesizing.

### Context-Efficient Patterns

| Pattern | How | Saves |
|---------|-----|-------|
| Targeted reads | Read specific line ranges, not whole files | 50-90% per file |
| Grep before read | Find the exact location, then read only that section | Avoids reading irrelevant files |
| Subagent delegation | Expensive exploration happens in isolated context | Protects main context |
| Summarize early | After a research phase, write a summary before continuing | Prevents re-reading |
| Batch tool calls | Run independent calls in parallel | Reduces round trips |

### What NOT to Load Into Context

- Entire files when you need 10 lines
- Build output or test logs beyond the relevant failure
- Files you've already read and understood
- Exploratory searches when you already know the answer

---

## Pillar 5: Quality Self-Assessment

### Confidence Calibration

After completing a task, assess your confidence on two axes:

**Completeness**: Did you address everything the user asked for?
- 1.0: Every aspect addressed with evidence
- 0.7: Main request addressed, some secondary aspects missing
- 0.4: Partial answer, significant gaps
- 0.1: Barely started

**Correctness**: How likely is your output to be right?
- 1.0: Verified by tests, cross-referenced, high certainty
- 0.7: Reasonable confidence but not verified
- 0.4: Best guess, significant uncertainty
- 0.1: Speculative

### When to Stop

Stop when ANY of these are true:
- The exit condition (from decomposition) is satisfied
- Your confidence that further work improves the output drops below 0.3
- You've consumed 70% of available context (the 30% rule)
- The user's question has been answered completely
- You're making changes that don't measurably improve the result

Continue when ALL of these are true:
- The exit condition is not yet met
- You have a clear next step with expected improvement
- You have sufficient context budget remaining
- Each iteration is producing measurable progress

### The "One More Thing" Trap

Resist the urge to add improvements the user didn't ask for. Every "one more thing" costs tokens, risks introducing bugs, and delays delivery. If you see an improvement opportunity, note it in your response — don't implement it unasked.

---

## Architecture Patterns

### Pattern 1: Scout-Then-Act

```
Phase 1 (Scout):   Read, Grep, Glob — understand the territory
Phase 2 (Plan):    Decompose based on what you found
Phase 3 (Act):     Edit, Write, Bash — execute the plan
Phase 4 (Verify):  Run tests, check results
```

Best for: Bug fixes, feature additions, refactoring. You need to understand before you change.

### Pattern 2: Parallel Fan-Out

```
Wave 0: [Research A] + [Research B] + [Research C]   ← parallel subagents
Wave 1: [Synthesize findings]                         ← single agent
Wave 2: [Implement based on synthesis]                ← single agent
```

Best for: Tasks requiring multiple independent information sources. Research tasks, competitive analysis, multi-file understanding.

### Pattern 3: Iterative Refinement

```
Loop:
  1. Produce draft output
  2. Evaluate against criteria
  3. If criteria met → done
  4. Identify largest gap
  5. Fix the gap → go to 1
Max iterations: 3-5
```

Best for: Creative tasks, code generation, content production. Each pass improves quality.

### Pattern 4: Staged Pipeline

```
Stage 1: Raw extraction (fast, broad)
Stage 2: Filtering (remove noise)
Stage 3: Enrichment (add detail to survivors)
Stage 4: Final synthesis
```

Best for: Data processing, research synthesis, skill compression. Each stage narrows the working set.

---

## Quality Checklist

Before considering an agentic task complete:

```
[ ] Exit condition defined before starting
[ ] Task decomposed into 3-7 concrete subtasks
[ ] Dependencies identified (what must serialize vs parallelize)
[ ] Each tool call has a clear purpose (no exploratory fishing)
[ ] Errors handled at the appropriate recovery level
[ ] Context budget tracked (not over 70% before synthesis)
[ ] Output addresses every part of the user's request
[ ] Confidence self-assessed on completeness and correctness
[ ] Improvements not requested by user noted but not implemented
[ ] Clear stopping point reached (exit condition met)
```

---

## The Meta-Pattern

All five pillars follow one meta-pattern: **think before acting, act with precision, assess after acting**.

```
THINK:  What am I trying to do? How will I know it's done?
ACT:    Use the minimum tools with maximum precision.
ASSESS: Did it work? What's my confidence? Should I continue?
```

Agents that skip THINK waste tokens exploring. Agents that skip ASSESS don't know when to stop. Agents that skip ACT just plan forever. All three, in that order, every cycle.

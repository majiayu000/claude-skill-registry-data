---
license: Apache-2.0
name: agentic-patterns
description: |
  Fundamental patterns for effective agentic behavior. Teaches decomposition, tool orchestration, error recovery, context management, quality self-assessment, and knowing when to stop. Model-agnostic principles that make any agent more effective regardless of domain. Activate on: "how should I structure this agent", "agentic workflow", "agent patterns", "multi-step task", "tool orchestration", "/agentic-patterns", "decompose this", "agent best practices", "chain of actions", "when should the agent stop", "agent loop design". NOT for: creating agent infrastructure (use agent-creator), building DAGs (use jury_rig-architect), specific tool implementation.
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
metadata:
  category: Agent & Orchestration
  tags:
    - agents
    - orchestration
    - decomposition
    - tool-use
    - patterns
    - fundamentals
  pairs-with:
    - skill: next-move
      reason: Decomposition and planning feed into agent execution
    - skill: jury_rigzip
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
- Designing DAG topologies (use jury_rig-architect)
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

Before acting, make scoped passes over the task as its risk and uncertainty require:

**Pass 1 — Scope**: What does "done" look like? Define the exit condition first.

**Pass 2 — Subtasks**: What concrete steps and dependency boundaries are needed to reach "done"? Each step should be achievable with a single tool call or a small chain of tool calls.

**Pass 3 — Dependencies**: Which steps depend on which? Independent steps can parallelize. Dependent steps must serialize.

### Decomposition Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Acting before decomposing | Wasted tool calls, wrong direction | Always plan first, even briefly |
| One giant subtask | No independent verification or ownership | Split at real effect or verification boundaries |
| Many subtasks | Cognitive overhead, lost context | Merge or split based on dependency and review cost |
| No exit condition | Agent runs forever | Define "done" before starting |
| Static plan | Can't adapt to discoveries | Replan after each wave of results |

### When to Re-Decompose

Replan when:
- A tool call returns unexpected results
- You discover the problem is different from what you assumed
- A dependency fails and the downstream plan is invalid
- A material dependency, observation, or risk changes the plan’s basis

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

**Sequential** work passes each result to the next action. **Parallel** work
collects independent results before synthesis. See
[`references/evidence-and-control-loop.md`](references/evidence-and-control-loop.md)
for rendered control-loop diagrams.

**Rule**: If two tool calls don't share data, run them in parallel. If one needs the other's output, serialize them.

### The Subagent Decision

Spawn a subagent (Task tool) when:
- The sub-problem has a bounded question whose exploration would otherwise crowd out integration
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

**Level 1 — Classify, then retry when justified**: A rejected read or an input-validation failure can often be retried after correction. Before repeating a write, determine whether it may already have taken effect; an ambiguous outcome requires reconciliation or target-enforced idempotency. A retry count is a task-specific budget, not a universal rule.

**Level 2 — Alternative approach**: Use a different tool or strategy to achieve the same goal. If Edit fails, try a different Edit. If Grep finds nothing, try Glob with a different pattern.

**Level 3 — Complete independent work**: If a dependency is blocked, finish the authorized parts that do not depend on it and retain a concrete handoff. Partial results do not change the requested exit condition or make the task complete.

**Level 4 — Request missing input or authority**: Name the actual blocker and evidence. Ask as soon as a required user decision is clear; do not perform unsafe retries merely to exhaust a ladder.

### Error Recovery Anti-Patterns

| Anti-Pattern | Consequence | Fix |
|-------------|-------------|-----|
| Repeat a failed call without new evidence | Duplicate effects or wasted work | Classify the outcome, then use a justified recovery step |
| Ignore the error and continue | Cascading failures downstream | Every error must be handled |
| Quietly reduce the requested task | User gets less than they asked for | Preserve the exit condition; report the exact blocked portion |
| Abandon a recoverable task | Useful authorized work remains | Continue concrete independent steps; escalate real dependencies |

### Structured Error Handling

When a tool call fails:
1. **Read the error message carefully** — it usually tells you what's wrong
2. **Diagnose**: Is the request known not to have executed, known applied, or uncertain? Separately classify transient versus structural failure.
3. **Act**: Apply the appropriate recovery level
4. **Report**: If the error affects the final output, note it transparently

---

### External effects: unknown is a state

A timeout after a local or remote write is neither success nor failure. Record
the intended effect, stable idempotency identity, authorization used, observed
receipt, and reconciliation query. Resume by re-grounding from the authoritative
external state; retry only with a target-enforced duplicate-suppression contract, or authoritative absence plus a mechanism preventing the earlier attempt from committing later. If the provider cannot answer, leave the effect
`unknown` and escalate rather than creating a second successor. Local workspace
rollback cannot undo remote effects. See `references/effect-reconciliation.md`.

---

## Pillar 4: Context Management

### Context is a Budget

Every token in your context window costs money and attention. Treat context like a budget:

- **Income**: User message, tool results, retrieved content
- **Spending**: Each tool call adds to context
- **Savings**: Subagents isolate expensive exploration
- **Debt**: Unnecessary reads/searches that you can't un-read

### Reserve room for synthesis

Reserve a task-specific synthesis budget. Stop research when another read is less valuable than integrating the evidence already obtained.

### Context-Efficient Patterns

| Pattern | How | Saves |
|---------|-----|-------|
| Targeted reads | Read specific line ranges, not whole files | Depends on the relevant fraction of the file |
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

### Evidence before self-ratings

Assess **completeness** against the requested deliverables and **correctness** against the available acceptance evidence. Record completed, missing, blocked and unverified items separately. Passing a named test is evidence for that test's scope, not probability 1 that an artifact is correct.

If an application genuinely needs numerical confidence, define the event being forecast and calibrate predictions against held-out labeled outcomes. A verbal self-rating or a convenient decimal is not automatically a probability. Keep task coverage, correctness forecasts and expected benefit of further work as different quantities.

### When to Stop

Finish when the requested exit condition and matching acceptance checks are satisfied. Pause dependent work when a required input or authority is missing, while continuing useful independent work. Use explicit time, cost or context limits where the task supplies them; report unmet deliverables when a real limit prevents completion.

Continue when the exit condition remains unmet and there is a concrete authorized next step that can resolve a material gap. Do not replace the user's completion requirement with an invented confidence threshold or stop because a turn is getting long.

### The "One More Thing" Trap

Resist the urge to add improvements the user didn't ask for. Every "one more thing" costs tokens, risks introducing bugs, and delays delivery. If you see an improvement opportunity, note it in your response — don't implement it unasked.

---

## Architecture Patterns

### Pattern 1: Scout-Then-Act

Scout, plan, act, and verify are distinct phases; findings may revise the plan
before an authorized effect.

Best for: Bug fixes, feature additions, refactoring. You need to understand before you change.

### Pattern 2: Parallel Fan-Out

Run independent research in one bounded wave, synthesize it, then decide
whether implementation is authorized.

Best for: Tasks requiring multiple independent information sources. Research tasks, competitive analysis, multi-file understanding.

Use fan-out only after a single-worker plan is written. Add workers when the
task has independently verifiable branches and the expected coordination cost is
bounded; serialize coupled edits and unresolved effect reconciliation.

### Pattern 3: Iterative Refinement

Produce a draft, evaluate it against stated criteria, repair the most material
gap, and stop when the task-specific exit condition or budget says to stop.

Best for: Creative tasks, code generation, content production. Each pass improves quality.

### Pattern 4: Staged Pipeline

The pipeline is extraction, filtering, enrichment, then synthesis. Its stage
count and stopping rule depend on the task and evidence budget.

Best for: Data processing, research synthesis, skill compression. Each stage narrows the working set.

---

## Quality Checklist

Before considering an agentic task complete:

```
[ ] Exit condition defined before starting
[ ] Task decomposed into concrete, independently checkable subtasks
[ ] Dependencies identified (what must serialize vs parallelize)
[ ] Each tool call has a clear purpose (no exploratory fishing)
[ ] Errors handled at the appropriate recovery level
[ ] Context budget tracked with a task-specific synthesis reserve
[ ] Output addresses every part of the user's request
[ ] Confidence self-assessed on completeness and correctness
[ ] Improvements not requested by user noted but not implemented
[ ] Clear stopping point reached (exit condition met)
```

---

## The Meta-Pattern

All five pillars follow one meta-pattern: **think before acting, act with precision, assess after acting**.

Think sets goal and evidence needs; act takes the narrowest authorized action;
assess checks the observed result and whether the exit condition is met.

Agents that skip THINK waste tokens exploring. Agents that skip ASSESS don't know when to stop. Agents that skip ACT just plan forever. All three, in that order, every cycle.

## Bundle navigation

[references index](references/INDEX.md).

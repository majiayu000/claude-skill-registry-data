---
name: analyze-agent-loop
description: Use when tracing turn loops, tool continuations, state transitions, or understanding how an AI agent or complex system actually processes requests through its execution cycle
---

## Announce at start: "Using codebase-analyzer to analyze the agent loop."

## Overview

Map the runtime execution spine: how does a request enter, get processed, and produce output? Identify the turn loop, state machine, and tool continuation patterns.

**Prerequisite:** Reads `docs/analysis/artifact-classification.md` (need to know core vs support).

## Process

1. Identify the main entry point and request handler
2. Trace the turn/request loop: input -> processing -> tool call -> response -> next turn
3. Map state transitions: idle -> active -> waiting -> responding -> idle
4. Find tool continuation patterns: when does the system call another tool after receiving output?
5. Identify termination conditions: when does the loop stop?
6. Find state persistence: what survives between turns?
7. Produce execution spine diagram

## State Machine Decomposition

Break the agent loop into discrete states and map every transition between them. The canonical state cycle is:

```
IDLE -> RECEIVING -> PROCESSING -> TOOL_CALL -> WAITING -> RESPONDING -> IDLE
```

For each state, identify:
- **Entry condition** -- what causes the system to enter this state?
- **Actions** -- what work happens while in this state?
- **Exit transitions** -- what are the possible next states, and what triggers each?
- **Error paths** -- what happens on failure within this state?

```
State Transitions:
  IDLE        --[new message]-->  RECEIVING
  RECEIVING   --[parsed]-->       PROCESSING
  PROCESSING  --[tool needed]-->  TOOL_CALL
  PROCESSING  --[text reply]-->   RESPONDING
  PROCESSING  --[error]-->        ERROR
  TOOL_CALL   --[dispatched]-->   WAITING
  WAITING     --[tool result]-->  PROCESSING (continuation)
  WAITING     --[timeout]-->      ERROR
  RESPONDING  --[sent]-->         IDLE
  ERROR       --[retry]-->        RECEIVING
  ERROR       --[fatal]-->        IDLE (terminal)
```

Look for states that are implicit rather than explicit -- code that behaves like a state machine without naming states is harder to debug. Identify any states not covered by the canonical cycle (e.g., RATE_LIMITED, CANCELLED, STREAMING).

## Turn Loop Tracing

Count turns, map tool continuations, and identify state transitions per turn. For each iteration of the loop, record:

- **Turn number** and entry state
- **Input type** (user message, tool result, system event)
- **Tools called** and their continuation chain (tool A result triggers tool B)
- **State transitions** within this turn
- **Accumulated context** -- what grows or changes between turns

```
Turn Trace Template:
  Turn N:
    Input: <what arrived>
    State: <state at entry>
    Action: <processing decision>
    Tool calls: <if any, with continuation depth>
    State transitions: <state1> -> <state2> -> ...
    Termination check: <condition evaluated, result>
```

**Termination analysis:** How many turns before the loop terminates? What conditions cause termination -- explicit stop, max-turns limit, completion signal, or unhandled error? What causes infinite loops (missing break conditions, tool results that always re-trigger the same path, state that never transitions to terminal)?

```
Loop termination audit:
  1. Count max-turns guard -- is it enforced? What is the limit?
  2. Check completion signal -- does the loop check for "done"?
  3. Find stall conditions -- states with no exit transition
  4. Identify replay loops -- same input producing same tool call repeatedly
  5. Verify error escape -- does every error path eventually terminate?
```

## The Iron Law

```
Prompt != behavior. The prompt says what to do; the code determines what CAN be done. Map both separately.
```

The system prompt defines intent. The runtime code defines capability. A gap between them is where bugs, hallucinations, and unexpected behaviors live. When analyzing an agent loop:

1. **Map the prompt's declared behavior** -- what does the system prompt claim the agent should do?
2. **Map the code's actual behavior** -- what execution paths, tool limits, and state transitions does the code enforce?
3. **Find the gaps** -- places where the prompt promises behavior the code cannot deliver, or the code allows behavior the prompt did not anticipate.

## Quick Reference

| Component | What To Find |
|-----------|-------------|
| Entry point | Main function, request handler, message listener |
| Turn loop | while/for loop processing messages, recursive call pattern |
| State machine | switch/if-else on state, state object transitions |
| Tool dispatch | function call mapping, tool registry lookup |
| Continuation | re-entry after tool output, message chaining |
| Termination | break condition, max turns, completion signal |
| Persistence | state saved between turns, conversation history |

## Trigger Signals

- **HIGH confidence**: Conditional tool availability in the loop -> `extract-tool-graph`
- **HIGH confidence**: State transitions gated by conditions -> `map-feature-gates`
- **MEDIUM confidence**: Complex multi-step processing -> refactoring candidate
- **LOW confidence**: Simple linear processing -> no deep dive needed

## Adversarial Lens

If the agent loop had a hidden behavior, where would it be? Check: error paths that trigger unexpected tool calls, state transitions that skip authorization checks, "fallback" behaviors that escalate capabilities. Hidden behaviors live in edge cases of the state machine.

## Red Flags

- Only tracing the happy path, missing error/retry branches
- Not identifying state persistence mechanisms
- Missing the tool dispatch/registration pattern

## Output Contract

Write `docs/analysis/agent-loop.md` using standard contract.
Include: execution spine diagram, state machine, turn loop flow, termination conditions.

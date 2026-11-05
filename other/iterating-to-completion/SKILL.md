---
name: iterating-to-completion
description: "Prevents premature exit and infinite loops. Three mechanisms: Completion Promises, Scratchpads, Loop Detection."
type: orchestrate
tier: core
trigger: "keep iterating, don't exit early, loop until done, completion signal, stuck detection"
---

## Purpose

This skill prevents two failure modes:
1. **Premature exit** — agent stops before success criteria are met
2. **Infinite loop** — agent spins endlessly with no progress

## Mechanism 1: Completion Promises

Every agent task has an explicit completion signal. The agent outputs this string ONLY when success criteria are truly met:

| Role | Signal | Meaning |
|---|---|---|
| Lead | `ARCHITECTURE_PLAN_COMPLETE` | Architecture JSON is complete and valid |
| Developer | `IMPLEMENTATION_COMPLETE` | Code compiles, lints pass, basic sanity checked |
| Reviewer | `REVIEW_COMPLETE` | Review report generated (approved or rejected) |
| Test Lead | `TEST_PLAN_COMPLETE` | Test plan JSON is complete |
| Tester | `ALL_TESTS_PASSING` | All tests pass, coverage met |

**Rule:** Never output the completion signal unless the criteria are truly met. The orchestrator blocks on this signal.

## Mechanism 2: Scratchpad Protocol

Maintain a scratchpad file at `.jonggrang/.ephemeral/scratchpad-{task_id}.md`:

```markdown
# Task: {task_id} — {title}
## Completed Steps
- [x] Step 1 — what was done
- [x] Step 2 — outcome

## Current Focus
- [ ] Step 3 — what you're working on now

## Failures & Learnings
- Attempt 2: Failed because X. Will try Y instead.

## Next Step
Clear description of what you do next iteration.
```

Update this EVERY iteration. If you're stuck, the scratchpad shows why.

## Mechanism 3: Loop Detection

The orchestrator reads your last 3 outputs. If similarity > 90%, you're stuck.

**Signs you're stuck:**
- Repeating the same command outputs
- The same error message appearing 3+ times
- Trying the same approach with minor variation

**When stuck:**
1. Write to scratchpad: "STUCK: [reason]"
2. Try a fundamentally different approach (not a variation)
3. If still stuck after 2 more tries, output `BLOCKED: [reason]` and stop

## Iteration Limit

Max 10 iterations per agent spawn. After 10:
1. Write current state to scratchpad
2. Output `ITERATION_LIMIT_REACHED: [what's left]`
3. Orchestrator will re-spawn you with fresh context and the scratchpad

## Integration with Hooks

The `feedback-loop.sh` / OpenCode `session.idle` hook enforces this:
- If dirty bit is set and you output a completion signal without going through reviewer/tester, the hook blocks your exit.
- You must demonstrate the full cycle: implement → review → test → signal.

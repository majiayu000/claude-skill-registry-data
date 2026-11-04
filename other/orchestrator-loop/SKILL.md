---
name: orchestrator-loop
description: "Orchestration pipeline for development tasks. The orchestrator delegates everything and never writes code directly."
---

# Orchestrator Loop

> The orchestrator DOES NOT WRITE CODE. This pipeline defines how the orchestrator delegates tasks.

## Pipeline

```
RESEARCH --> PLAN --> IMPLEMENT --> REVIEW --> REPORT
    |          |        |            |          |
 delegate   orchestr.  delegate    delegate   orchestr.
(bridge.sh) (approve)  (spawn)    (spawn)   (report)
```

## Step 1 -- RESEARCH (Gather Context)

- If context is already clear --> SKIP (e.g., user provided file paths and explicit instructions)
- If context is missing --> delegate via `bridge.sh --research "..."` or a research subagent
- Output: Summary of current state + relevant files + risks

## Step 2 -- PLAN (Design + Approval)

- **Large work** (multi-file, architectural decisions): invoke the `structured-brainstorming` skill --> get user approval
- **Small work** (single file, clear instructions): orchestrator writes a short summary --> get user approval
- **HARD-GATE**: No implementation without approval. Do not proceed to Step 3 until the user says "go".

## Step 3 -- IMPLEMENT (Delegate)

- Invoke the `subagent-execution` skill --> spawn subagents for each task
- The orchestrator only WATCHES: answers subagent questions, redirects if stuck
- The orchestrator DOES NOT WRITE: creating/editing files directly is forbidden
- Alternative for simple tasks: delegate via `bridge.sh --code "..."` to a coding subagent

## Step 4 -- REVIEW (Verify)

- Invoke the `verification-gate` skill
- Check: spec compliance + code quality + tests
- If it does not pass after 3 iterations --> escalate to the user; do NOT try to fix it yourself

## Step 5 -- REPORT (Present to User)

The orchestrator reports:
1. What was done (changed files + summary)
2. What was skipped and why
3. What requires human review
4. Known limitations, if any

---

## Shortcut Flow

Use the shortcut flow when ALL of the following are true:

- [x] Single file change
- [x] Less than 20 lines changed
- [x] Low risk (does not touch a working system)
- [x] Clear instructions (what to do is unambiguous)

**Shortcut pipeline:**
1. Orchestrator writes a short summary --> gets user approval
2. Delegates to a single coding subagent via `bridge.sh --code "..."`
3. Verifies the result (read file + run)
4. Reports

---

## Red Flags

| If the orchestrator is thinking... | Reality |
|---|---|
| "This is simple, I will do it myself" | NO. Simplicity does not change the rules. Delegate. |
| "Just one line" | Size does not matter. Writing directly is forbidden. |
| "Spawning a subagent is slow" | Doing it right > doing it fast. |
| "The pipeline is overkill" | Use the shortcut flow, but do NOT skip the pipeline. |
| "I already know the answer" | Knowing is not writing. Delegate. |

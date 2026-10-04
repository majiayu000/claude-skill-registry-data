---
name: fleet-stage-progression
description: How PM monitors and advances task stage progression — detecting stalled tasks, verifying methodology checks pass, coordinating PO gates. The bridge between methodology and dispatch.
---

# Stage Progression Oversight — PM's Methodology Bridge

Tasks don't advance themselves. The PO sets readiness. The methodology defines what each stage requires. But YOU monitor whether tasks are actually progressing — and when they stall, you act.

## The Stage Lifecycle

```
conversation (0-20) → analysis (20-50) → investigation (50-80) → reasoning (80-99) → work (99-100)
```

Each transition requires:
1. The current stage's work is done (artifact exists, criteria met)
2. PO reviewed and confirmed (readiness advanced)
3. Required contributions exist (for stories/epics entering reasoning/work)

Your job: monitor all three conditions for every active task.

## What to Check Each Heartbeat

### 1. Stalled Tasks

A task that hasn't changed stage or readiness in 2+ heartbeat cycles is stalling.

**How to detect:**
- Read your ASSIGNED TASKS section — check `task_readiness` and `task_stage`
- Compare to what you remember from last cycle (or check trail events)
- If readiness hasn't moved and no trail events → stalled

**Actions by cause:**

| Cause | How You Know | What to Do |
|-------|-------------|-----------|
| Agent waiting for PO | Artifact exists, readiness unchanged | Route to PO: `fleet_gate_request` or `fleet_chat(mention="human")` |
| Agent stuck on work | In-progress but no commits or progress reports | `fleet_chat("Status on task X?", mention=agent)` |
| Missing contribution | Task in reasoning, no required contribution | Call `pm_contribution_check(task_id)` → create missing contribution tasks |
| Unclear requirement | Agent asked questions, no PO response | Escalate: `fleet_escalate(title="PO input needed for task X")` |
| Agent offline | Agent in SLEEPING/OFFLINE state | Wait one cycle, then consider reassignment |

### 2. Ready to Advance

A task whose stage work is DONE but readiness hasn't been updated yet.

**Indicators:**
- Analysis stage: analysis_document artifact at 100% completeness → ready for investigation
- Investigation stage: investigation_document with options explored → ready for reasoning
- Reasoning stage: plan references verbatim, contributions received → ready for work
- Work stage: `fleet_task_complete` called → now in review (automatic)

**What you do:**
- Verify the artifact or deliverable exists
- Verify PO has seen it (check for PO comments or directive)
- If PO confirmed: advance readiness to next stage boundary
- If PO hasn't seen: route to PO with summary

### 3. Contribution Gates

Before any story/epic advances to work stage, contributions must be complete.

**The mandatory check:**
```
pm_contribution_check(task_id)
```

This returns:
- `all_received: true` → safe to advance to work
- `missing: ["design_input", "qa_test_definition"]` → create contribution tasks

**Never advance to work without this check.** The engineer needs contributions in their context.

### 4. The 90% Gate

When readiness reaches 90%, a PO gate fires:
- `fleet_gate_request(task_id, "readiness_90", summary)` → ntfy to PO
- PO approves → readiness goes to 99 → dispatched for work
- PO rejects → readiness stays or regresses → task needs revision

Package the gate with context: `pm_gate_route(task_id)` gathers plan status, contribution completeness, and readiness for the PO's decision.

## Stage-Specific Monitoring

### Conversation → Analysis (readiness 20)
- Agent has understood requirements? (check for task comments with questions answered)
- Verbatim requirement populated?
- If vague after 2 cycles → escalate to PO

### Analysis → Investigation (readiness 50)
- Analysis document exists with findings?
- PO reviewed findings?
- Implications for the task are clear?

### Investigation → Reasoning (readiness 80)
- Investigation document has multiple options explored?
- PO reviewed options?
- Enough information to make a decision?

### Reasoning → Work (readiness 99)
- Plan references verbatim requirement?
- All required contributions received? (`pm_contribution_check`)
- PO confirmed the plan?
- Gate approved?

## Common Anti-Patterns

1. **Readiness inflation** — PM sets readiness to 99 without contributions. Result: engineer works without design input, gets rejected.
2. **Stage skipping** — Task goes from conversation to work because "it's clear enough." Result: no analysis, no investigation, weak implementation.
3. **Stale advancement** — Task readiness was set 5 cycles ago but nobody's working on it. Result: context is stale when agent finally gets dispatched.
4. **PO bottleneck** — Multiple tasks waiting for PO review. Result: fleet stalls. Batch PO gates together and escalate proactively.

## The Dispatch Connection

When you advance readiness to 99%, the orchestrator's dispatch step picks it up:
1. Orchestrator reads task with `task_readiness >= 99` and `task_stage = work`
2. Budget check → storm check → doctor check → router selects model
3. Context refresh: writes task-context.md with stage instructions + contributions
4. Agent wakes and sees the task with FULL context

Your readiness advancement IS the dispatch trigger. Setting it correctly — with contributions verified, plan confirmed, PO gate approved — is what makes dispatch work.

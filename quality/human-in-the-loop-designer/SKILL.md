---
name: human-in-the-loop-designer
description: "Designs the human-in-the-loop (HITL) layer of an agent workflow - checkpoints, approval gates, escalation paths, and agent-to-human handoffs - with an interruption-cost budget and review-fatigue limits for each reviewer role. Use when mapping where a human must review an agent's work; designing escalation from an agent to a person; users are rubber-stamping approvals; or an agent workflow is stalling waiting for human input."
---

# Human-in-the-Loop Designer

> Every checkpoint costs attention. Spend it where human judgment actually changes the outcome.

## What this skill is

A workflow for placing and designing the moments where an agent pauses for a person: checkpoints, approval gates, escalations, and full handoffs. It treats human attention as a budgeted resource, sizes each touchpoint by its interruption cost and its error-catching value, and caps review load so approvals stay meaningful. Use it after autonomy levels are set (see `agent-autonomy-level-mapper`) to design how the human side of each gate actually works.

## What it solves

- Reviewers approving 50 items an hour without reading, so the gate catches nothing
- Agents that escalate everything, or nothing, because escalation triggers are undefined
- Handoffs where the human receives a task with no context and starts from zero
- Workflows that stall for hours because the approver is unavailable and there is no fallback
- Checkpoints placed at the end of a long run, after expensive or wrong work is already done

## When to invoke

- Designing a multi-step agent workflow with human review points
- Audit or compliance requires a human to sign off on agent output
- Approval rates are near 100 percent and reviewers report fatigue
- Customer-facing agents need a path to a human representative
- An agent run failed late and the team asks "why didn't we check earlier?"

## Phase 1: Map the workflow and the humans

Lay out the agent workflow as steps, then list each human role involved.

| Step | Agent action | Output | Downstream cost if wrong |
|-----:|--------------|--------|--------------------------|
| 1 | Gather requirements | Brief | Low (rework) |
| 2 | Generate plan | Plan | High (all later steps inherit errors) |

| Role | Availability | Expertise | Max reviews per day before quality drops |
|------|-------------|-----------|------------------------------------------|
| Requester | Synchronous, in session | Knows intent | 5-10 |
| Domain approver | Asynchronous, hours | Knows policy | 20-40 |

Capacity limits are estimates to validate in research; start conservative.

## Phase 2: Choose the touchpoint type

| Type | Purpose | Agent state | Human effort |
|------|---------|-------------|--------------|
| Checkpoint | Confirm direction before costly work | Paused, plan ready | Low: skim and confirm |
| Approval gate | Authorize a specific consequential action | Paused, action prepared | Medium: verify values |
| Escalation | Agent hit uncertainty or policy boundary | Paused or partial | Medium-high: decide |
| Handoff | Human takes ownership of the task | Stopped | High: complete the work |
| Notification | Inform after the fact | Continuing | Minimal: read |

Place checkpoints **after the step with the highest downstream cost**, usually the plan, not the final output. Catching a wrong plan is cheaper than reviewing a wrong deliverable.

## Phase 3: Score each candidate touchpoint

```
Touchpoint value = P(agent error at this step) x Cost of error x P(human catches it)
Interruption cost = Review time + Context-switch penalty + Wait time imposed on the workflow
Keep the touchpoint if value > interruption cost
```

Practical defaults:
- Context-switch penalty: 5-15 minutes for asynchronous reviewers pulled from other work; near zero if in session
- P(human catches it) drops sharply when the reviewer cannot see the evidence; if the gate shows only a summary, assume under 30 percent
- A touchpoint with high error cost but low catch probability needs a better review interface, not removal

## Phase 4: Set review-fatigue limits

Rubber-stamping is the main failure mode of human-in-the-loop systems. Define limits per role:

| Signal | Threshold | Response |
|--------|-----------|----------|
| Approval rate | Above 97 percent for 2 weeks | Gate is likely low value; consider promoting autonomy or sampling |
| Median review time | Under 3 seconds per item | Reviewer is not reading; redesign or reduce volume |
| Daily review volume | Above role capacity from Phase 1 | Batch, sample, or add reviewers |
| Edit rate at gate | Above 30 percent | Agent quality too low for this level; demote or fix upstream |

Volume controls:
- **Batching** - group similar low-risk items into one review with exceptions highlighted
- **Sampling** - review a random 10-20 percent when a gate is mostly confirmatory, plus 100 percent of flagged items
- **Exception-only review** - agent surfaces only items that fail a rule or fall below a confidence threshold

## Phase 5: Design escalation and handoff

Escalation triggers (define each explicitly):
- Confidence below the measured threshold for this action
- Policy or permission boundary reached
- Conflicting instructions or missing required data
- User expresses frustration or asks for a person
- Retry limit exceeded (for example, 2 failed attempts)

Every handoff package must include:

| Element | Content |
|---------|---------|
| Goal | What the user or requester wanted, in their words |
| Done so far | Steps completed with outputs and links |
| Blocker | Why the agent stopped, in one sentence |
| Suggested next step | Agent's best recommendation, labeled as such |
| Evidence | Sources, logs, and inputs the agent used |

Define fallback when the human is unavailable: wait with a stated expected time, route to a backup role, or safely park the task. Never let the agent proceed past a gate by timeout.

## Phase 6: Specify the touchpoint interface

For each kept touchpoint, write a one-row spec: trigger, who, channel (in-product, email, chat, queue), content shown, actions available, expected response time, and fallback. Tell the waiting user who is reviewing and when to expect an answer.

## Output

- Workflow map with human roles and review capacity
- Touchpoint inventory with type, value score, and interruption cost
- Review-fatigue thresholds and volume controls per role
- Escalation trigger list and handoff package template
- Touchpoint interface specs with fallbacks
- Instrumentation list (approval rate, review time, edit rate, wait time)

## Operating rules

**Always**
- Put the earliest checkpoint after the highest-leverage step
- Show the reviewer the evidence, not just the agent's conclusion
- Budget reviewer capacity and monitor approval rate and review time
- Include full context in every handoff so the human does not restart
- Tell the waiting user who is reviewing and the expected response time

**Never**
- Add a gate only to shift liability onto the reviewer
- Let an approval time out into automatic execution
- Escalate without stating why the agent stopped
- Treat a 99 percent approval rate as evidence the gate works
- Route every edge case to a human without a capacity plan

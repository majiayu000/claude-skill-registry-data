---
name: fleet-sprint-planning
description: How to plan sprints with capacity awareness, velocity history, and realistic commitment — the art of saying no to protect what you said yes to
user-invocable: false
---

# Sprint Planning

## The Core Tension

The PO wants everything. The sprint has finite capacity. Your job is to
create a realistic plan that DELIVERS, not a fantasy plan that impresses.

A sprint where 8 of 10 stories complete is better than a sprint where
6 of 15 complete. Predictability > ambition.

## Step 1: Calculate Capacity

### Agent Availability
Each agent has a heartbeat interval and a maximum parallel task capacity:

| Agent | Heartbeat | Capacity | Notes |
|-------|-----------|----------|-------|
| software-engineer | 65m | 1 task | Implementation is focused work |
| architect | 60m | 2 tasks | Design can overlap (review + new) |
| qa-engineer | 70m | 2 tasks | Predefinition + validation overlap |
| devsecops-expert | 55m | 1 task | Security review is deep |
| devops | 75m | 1 task | Infrastructure is sequential |
| technical-writer | 80m | 2 tasks | Documentation can overlap |
| ux-designer | 85m | 1 task | UX spec is deep thinking |

### Sprint Points Budget
- Sprint length in days x points-per-day-per-agent
- Conservative: 3 points/day for implementation agents
- Reduce by 20% for sprint overhead (standups, reviews, blockers)
- Reduce by contribution load (architect + QA + devsecops time
  on contribution tasks for OTHER agents' stories)

### Contribution Tax
For every story the engineer works on, architect/QA/devsecops each spend
time on contribution tasks. Budget this explicitly:

```
Story (5pts engineer) requires:
  + 2pts architect (design_input)
  + 1pt QA (test_definition)
  + 1pt devsecops (security_requirement)
  = 9pts total fleet capacity consumed
```

**A 5-point story costs 9 points of fleet capacity.** Plan for this.

## Step 2: Prioritize

Use the PO's priority ordering. Don't re-prioritize.

But within that ordering, sequence for dependency efficiency:
1. Foundation stories first (models, migrations, shared utilities)
2. Stories that unblock the most other stories
3. Stories with the most contribution requirements (start early
   so contributions have time to complete)
4. Independent stories last (can fill gaps)

## Step 3: Commit Realistically

### The Commitment Protocol
1. List all candidate stories by PO priority
2. Calculate total points
3. Compare against sprint capacity (with contribution tax)
4. Draw the line where capacity runs out
5. Everything below the line is backlog, not sprint

### Negotiation Signals
If the PO pushes for more:
- Show the math: "10 agents, 2-week sprint, 180 available points,
  stories total 220 points including contribution tax"
- Offer trades: "We can add story X if we move story Y to next sprint"
- Never commit to what can't be done — the PM's credibility is the
  fleet's credibility

## Step 4: Create the Sprint Board

For each committed story:
1. Set sprint assignment in Mission Control
2. Verify contribution tasks exist
3. Verify dependencies are ordered
4. Set initial stage and readiness

### Sprint Kickoff Checklist
- [ ] All stories have ALL fields set (type, stage, readiness, points, agent, verbatim, phase)
- [ ] Contribution tasks created for required roles
- [ ] Dependencies mapped and ordered
- [ ] Capacity math documented in board memory
- [ ] PO has approved the sprint commitment

## Velocity Tracking

After each sprint:
- Points committed vs. points completed
- Stories committed vs. stories completed
- Blocker count and duration
- Contribution completion rate

Use velocity to improve NEXT sprint's commitment. Three sprints of data
beats any estimation technique.

## Group Calls

| Call | When |
|------|------|
| `pm_sprint_standup(sprint_id)` | Every heartbeat — velocity, blockers, gaps |
| `pm_contribution_check(task_id)` | Before advancing to work stage |
| `pm_gate_route(task_id, "sprint_boundary")` | At sprint boundaries |

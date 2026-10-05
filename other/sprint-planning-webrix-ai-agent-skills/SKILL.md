---
name: sprint-planning
displayName: Sprint Planning
tagline: Automate sprint planning with capacity analysis, backlog prioritization, and workload balancing.
description: |
  Assists with sprint planning by analyzing team capacity, prioritizing the
  backlog based on impact and effort, and balancing workload across team members.
  Pulls data from Jira or Linear to recommend sprint scope, flag overcommitment,
  and generate sprint goals.
department:
  - Engineering
  - Project Management
use_cases:
  - Sprint Planning
  - Capacity Management
  - Backlog Prioritization
tools_required:
  - Jira MCP
  - Linear MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Plan Sprint 24 for the Platform team (6 engineers).
  Velocity: avg 42 story points. Focus: reliability improvements.
exampleOutput: |
  Sprint 24 Plan — Platform Team

  CAPACITY
  Team Size:       6 engineers (1 on PTO day 3-5)
  Available Days:  56 engineer-days
  Target Points:   40 (below velocity — PTO adjusted)

  RECOMMENDED SCOPE
  1. [P0] Fix connection pool exhaustion — 8pts — @alice
  2. [P0] Add circuit breaker to payment svc — 5pts — @bob
  3. [P1] Migrate cache to Redis cluster — 13pts — @carol, @dave
  4. [P1] Add latency alerts dashboard — 5pts — @eve
  5. [P2] Update dependency versions — 3pts — @frank
  6. [P2] Document failover procedures — 3pts — @alice

  TOTAL: 37 points (93% of target — safe buffer)
---

# Sprint Planning

Automate sprint planning with capacity analysis, backlog prioritization, and workload balancing.

**Integrations:** Jira, Linear

## When to Use

- The team is preparing for a new sprint and needs scope recommendations
- The user wants to balance workload across team members
- The user mentions "sprint planning", "capacity", or "backlog prioritization"

## Steps

### Step 1: Analyze Capacity

Calculate available engineer-days factoring in PTO and meetings.

### Step 2: Prioritize Backlog

Rank items by priority, dependencies, and sprint goals.

### Step 3: Assign and Balance

Distribute work across team members based on skills and availability.

## Output

Deliver:
- Sprint plan with recommended scope
- Capacity analysis and velocity comparison
- Workload distribution by team member

---
name: planning-innovation-cost-and-capacity
description: Use the Innovation cost tracking data and project list to estimate spend, capacity, and tradeoffs across CustomGPT.ai Labs projects.
---

# Planning Innovation Cost and Capacity

You help Felipe understand how Innovation time and budget are allocated, and
what tradeoffs are involved in starting, continuing, or stopping projects.

## When to Use

Use this skill when the user:

- Is planning Innovation work for the next month or quarter.
- Must decide whether to start a new project or extend an existing one.
- Needs to understand cost and capacity implications for leadership.

## Inputs

Expect:

- The cost tracking sheet with roles, hours per week, rates, and status.
- The current list of active projects and their owners.
- Any constraints (monthly budget caps, immovable deadlines, key launches).

## Core Tasks

1. **Capacity Snapshot**
   - Summarize total hours per role and total monthly cost.
   - Highlight roles that are constrained vs. those with slack.

2. **Project Allocation**
   - Estimate how much capacity each project consumes by role.
   - Identify over‑allocated contributors or unrealistic plans.

3. **Scenario Analysis**
   - Given a proposed new or changed project, estimate:
     - Incremental cost.
     - Which existing projects would likely slow down or pause.
   - Provide a small set of scenarios (e.g., “Option A, B, C”).

4. **Recommendations**
   - Suggest specific actions (kill, pause, or extend certain projects).
   - Suggest where additional resources would have the highest leverage.

## Output Format

Produce a Markdown report with:

- **Capacity Snapshot**
- **Cost Summary**
- **Project Allocation**
- **Scenarios & Tradeoffs**
- **Recommendations**

Use simple tables where helpful and make assumptions explicit.

## Guidelines

- Be conservative when data is incomplete; avoid false precision.
- Focus on **choices and tradeoffs**, not just raw numbers.
- Tie recommendations back to outcomes from `analyzing-innovation-portfolio`
  when available.

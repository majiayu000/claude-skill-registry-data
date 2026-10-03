---
name: capacity-planning
description: >
  Use when forecasting resource needs, evaluating if current capacity is sufficient
  for planned work, or sizing systems for expected load. This skill provides procedures
  for estimating, planning, and monitoring capacity to prevent resource shortages.
---

# Capacity Planning

## Overview
This skill defines how to forecast and plan for resource capacity. Proactive capacity planning prevents resource shortages, avoids emergency procurement, and ensures systems and teams can handle planned workloads.

## When to Use
- Before starting work that needs significant resources (compute, storage, personnel)
- When current resources are approaching capacity limits
- When planning new features expected to increase load
- Before committing to delivery timelines that depend on resource availability
- When evaluating cost estimates for new projects
- **Don't use when:** Resource needs are trivial and well within current capacity

## Core Procedures

### Step 1: Inventory Current Capacity
Document what you have:
- **Compute:** Available cores, memory, concurrent processing capacity
- **Storage:** Available disk, database space, file storage
- **Network:** Bandwidth, connection limits, API rate limits
- **Personnel:** Available agents, their skills, current workload
- **Budget:** Available budget for the planning period
- **Time:** Hours or sessions available before deadline

### Step 2: Estimate Requirements
For the planned work:
- What resources are needed? (compute, storage, personnel, time, budget)
- How much of each? (quantified estimates)
- When are they needed? (timing over planning period)
- What are the peak requirements? (maximum concurrent usage)
- What is the growth curve? (linear, exponential, seasonal)

### Step 3: Identify Capacity Gaps
For each resource:
```
CAPACITY GAP
============
Resource: [what resource]
Current capacity: [what you have]
Planned requirement: [what you need]
Gap: [deficit or surplus]
Timeline: [when the gap occurs]
Impact if gap not filled: [what happens]
```

### Step 4: Plan Responses
For each gap, choose a response:
- **Add Capacity:** Procure more resources (costs money, takes time)
- **Reduce Demand:** Scope down, phase delivery, defer features
- **Optimize Usage:** Get more from existing resources (efficiency gains)
- **Accept Risk:** Proceed knowing capacity may be insufficient (document risk)

### Step 5: Monitor and Adjust
- Track actual usage against projections
- Alert when usage approaches capacity threshold (80%)
- Re-estimate if requirements change
- Update plan quarterly or at major milestones

## Quality Checklist
- [ ] Current capacity documented with actual numbers
- [ ] Requirements estimated with reasoning
- [ ] Capacity gaps identified with impact analysis
- [ ] Response plan for each gap
- [ ] Monitoring thresholds set for key resources
- [ ] Plan reviewed and approved by stakeholders

## Error Handling
- **Error:** Capacity gap identified but no budget to add capacity
  **Response:** Reduce demand (scope down) or optimize usage; escalate if neither possible
- **Error:** Actual usage much higher than estimated
  **Response:** Re-estimate immediately, activate response plan for new gap, notify stakeholders
- **Error:** Capacity emergency (near exhaustion)
  **Response:** Add emergency capacity immediately, then investigate why planning failed

## Cross-Team Integration
**Related Skills:** risk-assessment, cost-optimization, status-reporting, incident-response
**Used By:** CEOs, Infrastructure agents (Orchestrator, Database, Compute), project managers, finance agents
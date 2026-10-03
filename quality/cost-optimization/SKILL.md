---
name: cost-optimization
description: >
  Use when evaluating costs or looking for ways to reduce expenses in your domain.
  This skill provides a framework for identifying, analyzing, and reducing costs
  across all operations, infrastructure, development, and business activities.
---

# Cost Optimization

## Overview
This skill defines how to identify and reduce costs without compromising quality or delivery. Every agent should periodically review costs in their domain and apply optimization principles.

## When to Use
- When reviewing resource usage or budget allocation
- When costs are higher than expected or trending upward
- When planning new initiatives (evaluate cost alternatives)
- When asked to reduce costs or improve efficiency
- Before provisioning new resources or tools
- **Don't use when:** Quality, security, or compliance would be compromised by cost reduction

## Core Procedures

### Step 1: Identify Cost Areas
Map where costs are being incurred:
- **Infrastructure:** Compute, storage, networking, licenses
- **Operations:** Processing time, API calls, data transfer
- **Development:** Tools, services, subscriptions
- **Time:** Duration of processes, rework, idle time
- **External:** Vendors, contractors, third-party services
- **Quality:** Bug fixing, rework, testing, support

### Step 2: Analyze Cost Drivers
For each cost area:
1. What is the current cost (amount per period)?
2. What drives the cost (usage, time, complexity, inefficiency)?
3. Is the cost necessary or a result of waste?
4. Is the cost fixed or variable?
5. Are there alternatives that cost less?

### Step 3: Identify Optimization Opportunities

**ELIMINATE:** Costs that provide no value
- Unused subscriptions, idle resources, redundant processes
- Automated reports nobody reads, redundant approvals

**REDUCE:** Costs that can be lowered
- Right-size infrastructure (not over-provisioning)
- Batch processing instead of real-time when possible
- Caching and reuse to reduce repeated computation
- Pre-emptible or spot instances for non-critical workloads
- Consolidate redundant tools and services

**OPTIMIZE:** Costs that can be made more efficient
- Automate manual processes
- Improve algorithms to reduce processing time
- Use more efficient data structures or approaches
- Schedule non-urgent work during off-peak hours

**TRANSFER:** Costs that can shift to lower-cost alternatives
- Open source alternatives to paid tools
- Build vs buy analysis
- Different vendor with better pricing
- Negotiate volume discounts

### Step 4: Evaluate Trade-offs
For each optimization opportunity:
- What is the potential savings?
- What is the effort to implement?
- Is there any impact on quality, security, or performance?
- **Only proceed if savings outweigh implementation cost AND no quality degradation**

### Step 5: Implement and Monitor
For each approved optimization:
```
COST OPTIMIZATION
=================
Cost area: [what costs are being addressed]
Current cost: [amount per period]
Expected savings: [amount or percentage]
Implementation: [what changes need to be made]
Risk: [impact on quality/security/performance]
Validation: [how to verify savings were achieved]
Timeline: [when to implement and review]
```

After implementation:
- Verify savings match projections
- Confirm no negative impact on quality
- Document lessons for future optimizations

## Quality Checklist
- [ ] All cost areas identified and analyzed
- [ ] Optimization opportunities prioritized by savings vs effort
- [ ] Trade-offs evaluated for each optimization
- [ ] Savings validated after implementation
- [ ] No negative impact on quality or security
- [ ] Optimization documented and shared

## Error Handling
- **Error:** Optimization causes quality degradation
  **Response:** Rollback immediately, document what went wrong, reassess approach
- **Error:** Projected savings not materializing
  **Response:** Investigate root cause, adjust projections, revise approach if needed
- **Error:** Optimization causes operational issues
  **Response:** Disable optimization, fix operational issue, retry with corrected approach

## Cross-Team Integration
**Related Skills:** risk-assessment, testing-strategy, capacity-planning, continuous-improvement
**Used By:** CEOs, infrastructure agents, project managers, finance agents, ALL agents in cost-conscious operations
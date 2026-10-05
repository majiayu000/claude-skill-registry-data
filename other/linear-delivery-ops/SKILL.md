---
name: linear-delivery-ops
description: "Trigger: Linear status, cycle, estimate, hours, blocker, weekly report. Operate NutrIA delivery tracking safely."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use for project-management and reporting tasks in Linear.

# Hard Rules
- Linear is the work-status source of truth.
- Estimate is complexity/capacity, not actual hours.
- Use a linked time tracker for actual hours.
- Read first. Do not reassign, reprioritize, close or change scope without human approval.

# Execution Steps
1. Query project, cycle, issues and statuses.
2. Reconcile linked PR/test evidence before reporting completion.
3. Report committed/completed, estimates, time-in-status, logged hours, blockers and owner.
4. Propose changes; wait for approval before mutations.

# Output Contract
Produce a compact decision-ready status report with source links.

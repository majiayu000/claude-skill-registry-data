---
name: finance-engineer
description: Plan, review, or reduce project, cloud, SaaS, API, deployment, and operations costs using FinOps guidance while preserving security and maintainability.
metadata:
  short-description: Minimize feasible project and cloud costs
---

# finance-engineer

## Purpose During Development

Use this skill when Codex and similar AI coding agents need to plan, review, or reduce the engineering cost of a project, deployment, tool choice, cloud service, API, or operational workflow.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being financed.

## When To Apply

- choosing paid tools, SaaS products, cloud services, AI APIs, databases, storage, queues, analytics, monitoring, or CI minutes
- estimating launch, prototype, staging, or production cost
- reviewing a project plan for FinOps risk, surprise bills, or over-provisioning
- finding the lowest-cost approach that remains feasible, secure, and maintainable

## What To Inspect

- deployment architecture, infrastructure files, service plans, API usage, expected traffic, storage, retention, and background jobs
- existing tools already paid for or already approved by the organization
- free tiers, quotas, rate limits, egress, build minutes, seats, regions, backups, logs, and observability retention
- cost controls such as budgets, alerts, caps, autoscaling limits, TTLs, cleanup jobs, and environment shutdowns
- security and operations requirements that cannot be sacrificed for cost

## Rules To Enforce

- minimize total recurring cost, not just the first invoice line
- prefer free, existing, or already-approved tools when they are secure and operationally sufficient
- avoid usage-based services without budgets, quotas, or alerting
- scale from actual demand, not imagined future traffic
- make cost tradeoffs explicit when reducing cost increases security, reliability, or maintenance risk
- require cleanup and shutdown plans for preview, staging, test, and demo resources

## Cost Review Checklist

- identify fixed monthly costs, variable usage costs, seat costs, storage, egress, logs, backups, and CI/build minutes
- estimate the smallest launch footprint and the first scale breakpoint
- define budgets, alerts, spend caps, quota limits, and ownership
- remove unused services, duplicate vendors, idle environments, and over-retained data
- document what can be upgraded later without re-architecting the project

## Common Anti-Patterns To Catch

- selecting enterprise services for prototype workloads
- leaving preview environments, test databases, or generated storage running indefinitely
- adding analytics, monitoring, or AI APIs without usage limits
- ignoring egress, log retention, backup, or seat pricing
- cutting costs by weakening security, backups, or basic operability

## Expected Output From The Agent

- cost model
- lowest feasible option
- cost risks and scale triggers
- budget and alert plan
- cleanup plan
- tradeoff notes
- verification plan

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Cost Model
- Cost Controls
- Tradeoffs
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Use this skill to keep the deployment plan as cheap as feasible without weakening security."

"Review this project architecture for FinOps risks and surprise cloud costs."

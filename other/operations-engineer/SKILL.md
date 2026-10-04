---
name: operations-engineer
description: Plan, implement, or review operational readiness, observability, reliability, recovery, runbooks, backups, support, and maintenance for projects.
metadata:
  short-description: Prepare projects for basic operations
---

# operations-engineer

## Purpose During Development

Use this skill when Codex and similar AI coding agents need to plan, implement, or review the operational readiness of a project.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being operated.

## When To Apply

- preparing a project for production, demos, handoff, support, or repeated use
- defining logs, metrics, alerts, backups, incident response, runbooks, or maintenance tasks
- reviewing reliability, recoverability, support burden, or operational ownership
- deciding how much operations work is enough for the simplest feasible launch

## What To Inspect

- deployment path, runtime model, data stores, background jobs, queues, storage, and external services
- existing observability, logging, monitoring, error reporting, backup, and support tools
- failure modes for startup, deploy, rollback, migration, secrets, data loss, rate limits, and dependencies
- ownership notes, runbooks, incident docs, support workflows, and on-call expectations
- cost and security constraints that affect operations

## Rules To Enforce

- define the minimum operational controls needed for the project’s actual risk
- prefer existing observability and support tools when they pass security review
- make failure modes and recovery actions explicit before launch
- keep runbooks short enough to use during stress
- avoid expensive monitoring, tracing, or incident systems before the project needs them
- coordinate with `deployment-engineer`, `security-engineer`, and `finance-engineer` for production-facing decisions

## Common Anti-Patterns To Catch

- launching without knowing how to detect failure
- logs that omit useful context or leak sensitive data
- backups that are configured but never restored in testing
- alerts that page on symptoms nobody can act on
- operational plans that require paid tooling for a low-risk prototype
- undocumented manual steps that only work on one machine

## Expected Output From The Agent

- operational readiness summary
- observability plan
- failure modes and recovery plan
- runbook expectations
- backup and data-retention notes
- support and maintenance ownership
- verification plan

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Operational Readiness
- Observability Plan
- Recovery Plan
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Use this skill to prepare this deployed project for basic production operations."

"Review this launch plan for logging, monitoring, backups, runbooks, and support risk."

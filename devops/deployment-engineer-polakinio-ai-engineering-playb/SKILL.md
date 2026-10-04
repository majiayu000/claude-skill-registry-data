---
name: deployment-engineer
description: Plan, implement, review, or troubleshoot deployment paths, hosting, CI/CD, release, rollback, environment, and production-readiness decisions for projects.
metadata:
  short-description: Plan simple, safe deployment paths
---

# deployment-engineer

## Purpose During Development

Use this skill when Codex and similar AI coding agents need to plan, implement, review, or troubleshoot deployment paths for a project.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being deployed.

## When To Apply

- choosing hosting, runtime, CI/CD, release, rollback, or environment strategy
- preparing a project for local preview, staging, production, or demos
- reviewing deployment configuration, infrastructure-as-code, containerization, build scripts, or environment variables
- reducing deployment complexity while preserving security and operational needs

## What To Inspect

- package managers, build scripts, lockfiles, runtime versions, and framework conventions
- existing deployment files, CI workflows, Dockerfiles, compose files, IaC, hosting config, and environment examples
- secrets handling, environment variables, domains, TLS, storage, database, queue, and background job needs
- repository guidance for security, operations, testing, and cost
- current production or staging assumptions if the repo already deploys

## Rules To Enforce

- choose the simplest deployment target that satisfies the project’s runtime and traffic needs
- prefer existing deployment tooling when it is already working and passes security review
- keep dev, preview, staging, and production differences explicit
- avoid introducing containers, orchestration, IaC, or multi-cloud complexity before the project needs it
- require rollback or recovery guidance for production-facing changes
- verify build commands and deployment assumptions before presenting them as done
- coordinate with `finance-engineer` before adopting paid or usage-based infrastructure

## Common Anti-Patterns To Catch

- deploying from undocumented local state
- hardcoding secrets, URLs, regions, tenants, or credentials
- adding Kubernetes, queues, or managed databases for a static or simple app
- missing health checks, migration order, rollback notes, or environment documentation
- ignoring cold starts, build limits, storage persistence, or regional constraints

## Expected Output From The Agent

- deployment target recommendation
- environment and secrets plan
- build and release steps
- rollback or recovery plan
- verification commands
- operational handoff notes
- cost-impact notes

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Deployment Path
- Environment And Secrets
- Rollback Plan
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Use this skill to deploy this project with the simplest feasible hosting setup."

"Review these deployment files for release, environment, rollback, and cost risk."

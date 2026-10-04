---
name: security-engineer
description: Plan or review project security, tool reuse, dependencies, services, integrations, permissions, secrets, supply-chain risk, and security scan requirements.
metadata:
  short-description: Review security and tool reuse decisions
---

# security-engineer

## Purpose During Development

Use this skill when Codex and similar AI coding agents need to plan or review security for a project, dependency, third-party tool, integration, deployment path, or operational workflow.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being secured.

## When To Apply

- selecting or reusing third-party tools, services, dependencies, plugins, packages, or SaaS integrations
- reviewing authentication, authorization, secrets, permissions, network exposure, data handling, or supply-chain risk
- preparing a project for deployment or external users
- deciding whether an existing tool is safe enough to reuse

## What To Inspect

- existing security guidance in `AGENTS.md`, `SECURITY.md`, policies, and deployment docs
- dependency manifests, lockfiles, plugins, CI workflows, container files, and infrastructure configuration
- data classification, auth model, permission boundaries, secrets storage, and external integrations
- security scan results from available package, dependency, container, IaC, or code scanning tools
- maintenance signals for proposed tools: provenance, update cadence, permissions, vulnerability history, and necessity

## Rules To Enforce

- run the most appropriate available security scan before approving a new or reused tool
- prefer existing tools only when they are necessary, maintained, least-privilege, and pass review
- reject tools that require broad secrets, excessive permissions, unclear provenance, or avoidable data exposure
- keep security controls explicit in deployment, operations, and implementation plans
- treat defaults, fallbacks, retries, and local development shortcuts as part of the security boundary
- document accepted residual risks and compensating controls

## Tool Reuse Review

- identify the specific job the tool performs
- check whether the repo already has a safer or simpler tool for that job
- inspect permissions, network access, secrets, data access, generated files, and CI effects
- run dependency or configuration scans available in the project
- decide: reuse, replace, sandbox, defer, or reject

## Common Anti-Patterns To Catch

- adding a tool before defining the security problem it solves
- accepting broad cloud, repository, or workspace permissions for convenience
- using stale packages or abandoned services for critical paths
- storing secrets in examples, client bundles, logs, screenshots, or generated docs
- assuming local-only scripts are safe when they touch real credentials or production data

## Expected Output From The Agent

- threat and trust-boundary summary
- tool security decision
- required scans and scan results
- permission and secrets plan
- residual risks
- required fixes or compensating controls
- security verification plan

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Tool Security Decision
- Security Scan Plan
- Permission And Secrets Plan
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Use this skill to decide whether we should reuse this deployment tool after a security scan."

"Review this project plan for auth, secrets, dependency, and deployment security risk."

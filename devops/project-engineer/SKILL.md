---
name: project-engineer
description: Turn a design, idea, sketch, brief, or product concept into the simplest feasible project plan spanning design, deployment, security, operations, finance, tool reuse, and verification.
metadata:
  short-description: Turn ideas into feasible project plans
---

# project-engineer

## Purpose During Development

Use this skill when Codex and similar AI coding agents need to turn a design, idea, sketch, brief, or product concept into a feasible project plan and implementation path.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being built.

## When To Apply

- new project planning from an idea, design, prototype, screenshot, or vague brief
- early implementation planning before repository structure, tooling, deployment, or cost model is clear
- requests that need coordination across design, application engineering, deployment, security, operations, and finance engineering
- project rescue work where the simplest feasible path needs to be recovered from an overbuilt plan

## What To Inspect

- the repository `AGENTS.md`, `PLAYBOOK.md`, and `skills/PLAYBOOK.md`
- existing source layout, package managers, CI, deployment files, infrastructure files, and environment examples
- product brief, design inputs, screenshots, diagrams, tickets, or user-provided constraints
- existing tools and services already present in the repo or organization
- security, operations, and budget constraints that affect launch feasibility

## Rules To Enforce

- start with the smallest project shape that can satisfy the real user workflow
- separate must-have launch scope from later polish, scale, and automation
- reuse existing tools when they already fit the need and pass security review
- avoid adding services, frameworks, queues, databases, or deployment layers before the project needs them
- make deployment, security, operations, and cost decisions explicit before implementation hardens around them
- keep design quality part of delivery, not a cosmetic final pass

## Role Handoff Model

- apply `product-designer` for user experience, visual direction, and non-generic design quality
- apply `security-engineer` before adopting third-party tools, services, dependencies, or external integrations
- apply `deployment-engineer` before choosing hosting, CI/CD, environment strategy, or release flow
- apply `operations-engineer` before defining observability, support, backup, incident, or runbook expectations
- apply `finance-engineer` before committing to paid services, cloud resources, usage-based APIs, or scale assumptions
- apply existing review skills from `skills/PLAYBOOK.md` when implementation touches architecture, safety, contracts, performance, LLM behavior, or tests

## Common Anti-Patterns To Catch

- turning an idea into a platform before there is a validated workflow
- choosing tools because they are fashionable rather than already present, simpler, safer, or cheaper
- postponing deployment until after implementation creates awkward infrastructure requirements
- treating security, operations, or cost as separate afterthoughts
- accepting a generic AI-looking interface when the product needs a believable, domain-specific design

## Expected Output From The Agent

- project brief and success criteria
- simplest feasible scope
- role-by-role engineering plan
- reuse-versus-build decisions
- deployment path
- security and operations guardrails
- cost controls
- implementation milestones
- verification plan

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Simplest Feasible Path
- Role Plan
- Tool Reuse And Security Scan
- Deployment Plan
- Cost Controls
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Use this skill to turn this app idea and screenshot into a buildable project with deployment, security, operations, and cost guidance."

"Plan the simplest feasible project from this design, reuse existing tools where safe, and give me a deployment path."

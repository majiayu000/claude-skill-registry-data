---
name: architecture-guardian
description: Review or plan changes that affect repository structure, layering, ownership, orchestration flow, or architectural boundaries.
metadata:
  short-description: Guard boundaries, ownership, and layering
---

# architecture-guardian

## Purpose During Development

Use this skill when Codex and similar AI coding agents are changing or reviewing repository structure, module boundaries, layering, ownership, or orchestration flow.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being reviewed.

## When To Apply

- feature work that adds a new module, service, package, or boundary
- refactors that move responsibilities between layers
- PRs that mix UI, orchestration, domain logic, persistence, or integration concerns
- changes that duplicate an existing architectural path instead of extending it

## What To Inspect

- the repository `AGENTS.md`
- architecture or design docs
- the main entrypoints touched by the change
- service, orchestration, persistence, and interface boundaries affected by the task
- tests that define or imply ownership boundaries

## Rules To Enforce

- responsibilities should remain explicit
- control flow should stay centralized where the repo expects it
- interfaces should stay narrower than implementations
- avoid parallel architectures for the same responsibility
- prefer extending existing seams over creating an unowned layer
- runtime code must not depend on agent-governance files

## Common Anti-Patterns To Catch

- CLI or UI layers absorbing business logic
- persistence details leaking into presentation layers
- orchestration duplicated across multiple modules
- new abstractions without a clear ownership problem they solve
- generic manager or engine layers that hide existing boundaries

## Expected Output From The Agent

- boundary analysis
- ownership risks
- affected modules
- refactor or implementation guidance
- regression risks
- suggested tests around behavior-preserving boundaries

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Areas
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Review this refactor for boundary drift and duplicated orchestration."

"Use this skill to plan a new feature without breaking the repository’s existing layer ownership."

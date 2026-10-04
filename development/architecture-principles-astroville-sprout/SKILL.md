---
name: architecture-principles
description: Shared software architecture principles focused on right-tool decisions, scale-readiness, and avoiding unnecessary distributed complexity.
compatibility: opencode
metadata:
  audience: architects
  purpose: reusable-guidance
---
## What I do

Provide shared architectural principles that can be loaded by agents when evaluating existing systems or designing new ones.

## Core stance

- Prefer the simplest design that credibly satisfies the requirements.
- Optimize for the right tool for the job and the right design for the job.
- Treat complexity as a cost that must justify itself.
- Favor maintainability, operability, debuggability, and team cognition.
- Preserve a credible path to scale without forcing distributed complexity too early.

## Scale-readiness without overengineering

- Do not build microservices or distributed systems by default.
- Do design systems so they can grow beyond one node when needed.
- Prefer stateless application nodes where practical.
- Prefer externalized durable state and shared coordination mechanisms.
- Design async work to be queue-friendly and idempotent.
- Avoid designs that require special singleton nodes unless they are truly necessary.
- Call out likely first bottlenecks and the incremental path to address them.

## Guardrails

- Recommend microservices only when scaling asymmetry, ownership boundaries, isolation requirements, or compliance pressures clearly justify them.
- Do not recommend rewrites without a realistic migration path.
- Do not add abstractions for hypothetical future flexibility.
- Do not recommend CQRS, event sourcing, plugin systems, or heavy orchestration unless the problem clearly demands them.
- Every recommendation should include operational implications and testing implications.

## When to use me

Use this skill when an agent needs consistent architectural judgment across brownfield analysis, greenfield design, or architecture review.

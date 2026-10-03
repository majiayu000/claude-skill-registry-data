---
name: agentic-prd
description: Create practical product requirements documents for agentic engineering projects, AI-assisted software builds, MVP experiments, vibe-coded prototypes, and production-ready applications. Use when drafting, refining, or reviewing PRDs that need to guide Codex or other coding agents through product intent, scope, architecture, UI design direction, visual styling, security, acceptance criteria, evaluation loops, and delivery plans.
---

# Agentic PRD

## Overview

Use this skill to turn a product idea into a PRD that an agentic engineering workflow can execute. Bias toward crisp product intent, small verifiable milestones, explicit safety constraints, and a build-measure-learn loop that can scale from MVP to production.

## Operating Principles

- Start with the smallest useful product loop, then specify how to harden it.
- Treat the PRD as an execution contract for human engineers and coding agents.
- Separate discovery risk, product risk, technical risk, security risk, and operational risk.
- Prefer concrete examples, user stories, state transitions, data contracts, design references, and acceptance tests over broad claims.
- Preserve creative "vibe coding" momentum during ideation, then force rigor before production scope.
- Write requirements so a coding agent can implement, test, and verify without guessing hidden intent.

## Workflow

1. Clarify the product goal, users, core job, non-goals, and target quality bar.
2. Choose a delivery mode: `mvp`, `production`, or `phased`.
3. Identify the agentic workflow: what the user delegates, what the agent plans, what the system verifies, and where humans approve.
4. Draft the PRD using `references/prd-template.md` when a full document is needed.
5. Add acceptance criteria with observable behavior, test strategy, and evaluation signals.
6. Add design inspiration, aesthetic direction, UI styling constraints, security, privacy, abuse, reliability, and deployment requirements before calling anything production-ready.
7. End with open questions, cut lines, sequencing, and a validation plan.

## Mode Guidance

Use `mvp` mode when speed and learning matter most:

- Keep the scope to one primary workflow and one sharp success metric.
- Allow manual operations, limited scale, and simple persistence if they reduce time to validation.
- Require guardrails for data loss, user harm, cost blowups, and irreversible actions.
- Define what must be learned before expanding scope.

Use `production` mode when the app handles real users, money, sensitive data, integrations, or business-critical workflows:

- Require threat modeling, authn/authz, audit logging, secrets handling, rate limits, backup/restore, observability, and incident paths.
- Specify data retention, privacy boundaries, compliance assumptions, and abuse cases.
- Include failure modes, rollback plans, load expectations, and operational ownership.
- Demand test coverage across unit, integration, end-to-end, security, accessibility, and regression surfaces as relevant.

Use `phased` mode when the user wants both:

- Split the PRD into prototype, private beta, public beta, and production readiness phases.
- Give each phase explicit entry criteria, exit criteria, and cut lines.
- Prevent MVP shortcuts from silently becoming production architecture.

## Agentic Engineering Requirements

For agent-driven builds, include:

- Task decomposition boundaries: which tasks can be delegated independently.
- Context package: repo, docs, APIs, designs, credentials assumptions, and constraints the agent needs.
- Verification loop: commands, tests, visual checks, security checks, and reviewer gates.
- Human checkpoints: decisions that require approval, especially data model changes, payments, auth, migrations, deletion, or external side effects.
- Recovery plan: how to inspect work, revert, retry, or narrow scope when the agent gets stuck.

## PRD Quality Bar

Before finalizing, check that the PRD:

- Names the user, problem, value, and non-goals.
- Defines the smallest coherent product loop.
- Makes requirements testable and unambiguous.
- States assumptions and unknowns without hiding risk.
- Includes UX expectations, design direction, data model needs, integrations, and error states.
- Separates MVP shortcuts from production requirements.
- Provides enough implementation context for a coding agent to start safely.

## Reference

Read `references/prd-template.md` when the user asks for a full PRD, a reusable PRD template, production-readiness details, or a structured agentic build plan.

---
name: laravel-specialist
description: Coordinate full Laravel feature work across models, APIs, auth, queues, Livewire, tests, and quality checks by routing to focused skills.
tags:
  - laravel
  - php
---

# Laravel Specialist

Layer: 3 (Implementation Orchestrator)

Use this skill for broad Laravel implementation, refactoring, review, or bug-fixing tasks that touch several parts of an application.

This skill assumes Layer 0-2 have already run. If you have not run `memory-management` preflight, `least-code`, and `using-laravel-standards` skill selection yet, do so before loading this skill.

## Workflow

1. Confirm the task shape and primary workflow boundary: HTTP, console, queue, scheduled task, Livewire, API, integration, or data migration.
2. Apply `least-code` minimization: reuse existing helpers, stdlib, native features, installed dependencies before writing new code.
3. Select the smallest focused skills for the task and load only their `SKILL.md`.
4. Apply existing project conventions before introducing new patterns.
5. Verify with the smallest meaningful tests and quality checks.

## Skill Routing

- New feature architecture: `architecture`, `actions-and-services`
- Controllers and routes: `controller-cleanup`, `routes-best-practices`
- Validation and authorization: `form-requests`, `policies-and-authorization`
- Models and queries: `eloquent-patterns`, `eloquent-relationships`
- API responses: `api-resources-and-pagination`, `api-surface-evolution`
- Database writes and consistency: `database-transactions`
- Database performance: `laravel-database-optimization`
- Queues, workers, and Horizon: `queues-and-jobs`
- Livewire implementation, architecture, and tests: `livewire-development`
- Security: `security`, `rate-limiting`, `request-forgery-protection`
- Tests and handoff: `testing`, `tdd-with-pest`, `quality-checks`

## Guardrails

- Keep controllers focused on HTTP orchestration.
- Put reusable workflows in Actions or Services only when they reduce real complexity.
- Use Eloquent relationships, scopes, casts, policies, resources, jobs, events, and framework fakes before custom infrastructure.
- Queue slow external calls, email, exports, imports, and other work that should not block the request.
- Never skip validation, authorization, transaction boundaries, or failure handling because a task is "small".
- Avoid raw SQL unless Eloquent or the query builder cannot express the needed shape clearly or efficiently.
- Keep secrets, client names, private URLs, and one-off business rules out of reusable guidance.

## Handoff

Report the files changed, checks run, and any checks that could not run. If the task touches data shape, include migration and rollback risk in the handoff.

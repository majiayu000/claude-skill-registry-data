---
name: brainstorming
description: Interactive design refinement tailored to Laravel projects; clarify domain, data, interfaces, testing, and quality gates while accounting for Sail/non‑Sail environments
tags:
  - laravel
  - php
---

# Brainstorming

Layer: 2-3 (Design + Implementation)

Use this skill when a Laravel task involves design refinement before implementation.

This skill assumes Layer 0-1 have already run. If you have not run `memory-management` preflight and `least-code` minimization yet, do so before loading this skill.

## Syarif Defaults

- Follow Laravel conventions before introducing custom abstractions.
- Prefer project-local patterns when they are explicit and tested.
- Keep controllers focused on HTTP orchestration.
- Put validation, authorization, transactions, side effects, and integrations at clear boundaries.
- Keep client names, credentials, internal URLs, provider secrets, and project-specific business rules out of reusable standards.
- Verify important behavior with the smallest meaningful tests and quality checks.

## Workflow

1. Confirm memory preflight and least-code minimization are active.
2. Detect the Laravel version, PHP version, runner, package manager, and existing project conventions.
3. Identify the smallest local skill set that overlaps this topic.
4. Design or review the change using Laravel-native APIs first.
5. Add abstractions only when they reduce real complexity or protect a meaningful boundary.
6. Run targeted tests and available quality checks before handoff.

## Checkpoints

- Authorization and validation boundaries are explicit.
- Query shape, transactions, queues, cache, files, and external calls are intentional when touched.
- User-facing behavior has feature, unit, browser, or integration tests at the right level.
- Logs and errors are useful without exposing secrets or unnecessary personal data.
- Documentation or proposals avoid importing source-project names or one-off business rules.

## Related Skills

- `using-laravel-standards` - entrypoint and skill selection
- `architecture` - layer decisions
- `testing` - test strategy
- `security` - security review

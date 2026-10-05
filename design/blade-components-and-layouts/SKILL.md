---
name: blade-components-and-layouts
description: Laravel guidance to compose UIs with Blade components, slots, and layouts; keep templates pure and testable
tags:
  - laravel
  - php
---

# Blade Components And Layouts

Use this skill when a Laravel task involves blade components and layouts.

When the app has multiple menus/pages, also use `module-per-menu`: keep one Blade view per page or page state, share layout/components, and avoid a single Blade file full of menu-condition blocks.

When the Blade work includes UI/UX design, frontend implementation, browser inspection, or backend contract alignment, also use `ui-agent-browser`. Keep this skill focused on template structure, component boundaries, slots, layouts, and rendering purity.

This skill is adapted to the personal Laravel standards in this repository. It maps the public `blade-components-and-layouts` topic from `jpcaparas/superpowers-laravel` into the local `blade-components-and-layouts` catalog without copying third-party skill body text.

## Syarif Defaults

- Follow Laravel conventions before introducing custom abstractions.
- Prefer project-local patterns when they are explicit and tested.
- Keep controllers focused on HTTP orchestration.
- Put validation, authorization, transactions, side effects, and integrations at clear boundaries.
- Keep client names, credentials, internal URLs, provider secrets, and project-specific business rules out of reusable standards.
- Verify important behavior with the smallest meaningful tests and quality checks.

## Workflow

1. Detect the Laravel version, PHP version, runner, package manager, and existing project conventions.
2. Identify the smallest local skill set that overlaps this topic.
3. Implement or review the change using Laravel-native APIs first.
4. Add abstractions only when they reduce real complexity or protect a meaningful boundary.
5. Run targeted tests and available quality checks before handoff.

## Checkpoints

- Authorization and validation boundaries are explicit.
- Query shape, transactions, queues, cache, files, and external calls are intentional when touched.
- User-facing behavior has feature, unit, browser, or integration tests at the right level.
- Logs and errors are useful without exposing secrets or unnecessary personal data.
- Documentation or proposals avoid importing source-project names or one-off business rules.

## Related Skills

- `using-laravel-standards`
- `architecture`
- `ui-agent-browser`
- `module-per-menu`
- `testing`
- `security`

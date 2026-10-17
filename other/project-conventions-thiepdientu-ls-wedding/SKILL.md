---
name: project-conventions
description: Defines project-wide engineering rules for Laravel 12 + Blade + MySQL applications. Use when creating, modifying, reviewing, testing, or refactoring project code.
---

# Project Conventions — Laravel 12 + Blade + MySQL

## Role
Act as a senior full-stack Laravel engineer. Optimize for correctness, maintainability, security, testability, performance, accessibility, and a clean user experience.

## Fixed baseline
- Laravel 12.x
- PHP version: inspect the project; do not assume
- MySQL: inspect actual version/config
- Blade server-rendered UI
- Vite: use the existing asset pipeline
- Tailwind/Alpine: use only if already installed or explicitly requested

## Non-negotiable rules
1. Inspect the repository before changing it.
2. Preserve working project conventions unless there is a concrete reason to change them.
3. Prefer Laravel-native features and existing dependencies.
4. Do not add packages merely for convenience.
5. Controllers stay thin; business workflows do not belong in Blade or bloated controllers.
6. Validate all user-controlled input server-side.
7. Enforce authorization server-side with middleware/policies/gates as appropriate.
8. Prefer Eloquent relationships and query builder parameterization.
9. Prevent N+1 queries and unbounded result sets.
10. Use database constraints for data integrity.
11. Never hard-code secrets or expose `.env` values.
12. Never silently weaken authentication, authorization, CSRF, validation, or security.
13. Never run destructive production database commands without explicit confirmation.
14. Do not invent APIs for packages; inspect `composer.json`/`package.json` and installed versions.
15. Do not assume Livewire, Inertia, Vue, React, or an admin package exists.
16. Important new behavior requires automated tests.
17. Before declaring completion, run relevant tests/checks and fix failures.
18. Make the smallest coherent change that satisfies the requirement.

## Preferred structure
Use Laravel conventions first:
- `app/Http/Controllers`
- `app/Http/Requests`
- `app/Models`
- `app/Policies`
- `app/Rules`
- `app/Services` or `app/Actions` only when a real boundary is useful
- `resources/views`
- `resources/css`
- `resources/js`
- `routes/web.php`
- `database/migrations`
- `database/factories`
- `database/seeders`
- `tests/Feature`
- `tests/Unit`

## Coding standards
- Type parameters and return values where practical.
- Prefer dependency injection.
- Prefer early returns for guard clauses.
- Use meaningful names.
- Keep methods cohesive.
- Avoid speculative abstractions.
- Avoid duplicate business rules.

## Change protocol
Before editing:
1. Inspect relevant files.
2. Trace the existing request/data flow.
3. Identify authorization and validation requirements.
4. Identify database and UI impact.
5. Choose the smallest safe implementation.

After editing:
1. Inspect the diff.
2. Run targeted tests.
3. Run relevant broader tests/build checks.
4. Check logs/errors.
5. For UI changes, verify browser behavior if browser tooling is available.
6. Report assumptions and unresolved risks honestly.

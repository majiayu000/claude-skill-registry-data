---
name: testing-debugging
description: Tests and debugs Laravel 12 + Blade + MySQL applications using PHPUnit/Pest, feature tests, HTTP tests, database tests, factories, logs, routes, and browser verification when available. Use before declaring a feature complete.
---

# Testing & Debugging

## Role
Act as a senior QA-minded Laravel engineer.

## Completion rule
Code is not complete until behavior has been verified.

## Test priority
1. Feature tests for user-visible HTTP workflows.
2. Unit tests for isolated business logic where valuable.
3. Database assertions for persistence/relationships.
4. Browser smoke tests when UI interaction matters and browser tooling is available.

## Typical CRUD matrix
- guest denied
- authenticated allowed
- unauthorized user denied
- valid create works
- invalid input returns validation errors
- update works
- delete works
- missing model returns 404
- database state is correct
- redirect/view is correct

## Database tests
Use `RefreshDatabase` when appropriate. Prefer factories. Do not rely on test execution order. Avoid slow full database truncation unless it is actually required.

## Debug workflow
1. Reproduce.
2. Capture the exact error.
3. Identify the first meaningful stack trace.
4. Inspect source/config/database state.
5. Form a hypothesis.
6. Make the smallest fix.
7. Add a regression test.
8. Run the targeted test.
9. Run broader tests when practical.

## Useful Laravel checks
Use only when relevant:
- `php artisan test`
- `php artisan route:list`
- `php artisan about`
- `php artisan migrate:status`
- `php artisan optimize:clear`
- `php artisan view:clear`
- `php artisan cache:clear`

Never use destructive reset commands against production.

## Browser/UI diagnostics
Check console errors, failed requests, HTTP status codes, CSRF errors, form validation, broken links, responsive behavior, and asset loading.

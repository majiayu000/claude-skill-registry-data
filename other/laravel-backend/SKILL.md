---
name: laravel-backend
description: Implements Laravel 12 backend features using routes, controllers, Form Requests, Eloquent, policies, services/actions, jobs, events, notifications, caching, files, sessions, and HTTP responses. Use for backend feature development.
---

# Laravel Backend Development

## Role
Act as a senior Laravel 12 backend developer.

## Implementation sequence
1. Read the requirement and acceptance criteria.
2. Inspect existing code and conventions.
3. Identify authentication/authorization.
4. Design validation.
5. Design persistence and relationships.
6. Implement business logic in the right layer.
7. Implement response/redirect behavior.
8. Add tests.
9. Run tests and inspect logs/errors.

## Validation
- Validate every user-controlled input server-side.
- Prefer Form Requests for substantial forms/endpoints.
- Normalize input deliberately.
- Never rely on client-side validation.

## Eloquent
- Define relationships explicitly.
- Use casts intentionally.
- Prevent mass-assignment vulnerabilities.
- Use scopes for recurring query constraints.
- Eager-load relationships used in loops.
- Paginate large datasets.
- Use `withCount`, `withExists`, aggregates, or selective columns where they materially improve queries.

## HTTP behavior
- Use correct status codes.
- Use named route redirects for web flows.
- Preserve validation errors and old input for Blade forms.
- Follow the project’s existing flash-message conventions.

## External services
- Isolate integrations.
- Set timeouts.
- Handle non-success responses.
- Never log secrets or tokens.
- Use safe retry strategies.
- Queue slow operations when appropriate.

## File uploads
- Validate type and size.
- Use Laravel Storage APIs.
- Generate safe paths/names.
- Store outside public web root unless public access is intentional.
- Never trust original filenames.

## Caching
- Cache only when there is a real performance reason.
- Use stable, scoped keys.
- Define invalidation rules.
- Never share user-specific data under a global cache key.

## Jobs
- Prefer idempotent jobs.
- Avoid serializing unnecessary objects.
- Design retries/failures intentionally.
- Be careful with jobs dispatched before database commit.

## Error handling
Do not swallow exceptions. Return safe user-facing errors while preserving useful server-side diagnostics without exposing secrets.

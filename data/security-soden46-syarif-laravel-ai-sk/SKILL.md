---
name: security
description: Run focused Laravel security checks for authorization, request forgery, rate limits, uploads, secrets, APIs, and configuration.
tags:
  - laravel
  - php
---

# Security

Run a focused security pass whenever work touches authentication, authorization, input handling, uploads, external integrations, payment-like flows, public APIs, or sensitive data.

## Access Control

Every route/action that reads or mutates protected data needs authorization.

Use:

- route middleware for coarse access boundaries;
- Policies for model actions;
- Gates for cross-cutting checks;
- Form Request `authorize()` for request-input-dependent checks.

Test both allowed and denied paths.

## Request Forgery And Rate Limits

Use CSRF protection for browser forms. Exclude webhooks only deliberately, and authenticate webhook requests through signatures, shared secrets, IP allowlists, or provider verification as appropriate.

Apply rate limits to abuse-prone routes such as login, password reset, public forms, file uploads, and expensive API endpoints.

## Input And Output Safety

Validate all request input at the boundary. Use query builder bindings or Eloquent instead of interpolated raw SQL.

Escape output in Blade. Be deliberate about HTML rendering.

For frontend stacks, expose only the props needed by the page. Do not send hidden sensitive data because it is "not displayed."

## Uploads And Files

Validate uploaded files for:

- required/optional state;
- MIME/type;
- extension if relevant;
- size;
- count;
- image dimensions when needed.

Store files through Laravel `Storage`. Do not trust original filenames for storage paths. Keep visibility explicit.

## Secrets And Logs

Keep credentials in environment/config, not database-backed admin settings or source files.

Do not log:

- tokens;
- signatures;
- passwords;
- card data;
- full provider payloads;
- unnecessary personally identifiable information.

Use structured logs with safe identifiers and sanitized summaries.

```php
Log::info('integration.gateway.create.completed', [
    'record_id' => $record->id,
    'reference' => $record->public_reference,
    'provider_status' => $response->status(),
]);
```

## API Security

For APIs:

- return consistent errors;
- hide stack traces;
- validate input;
- authorize every action;
- apply rate limits;
- avoid leaking internal IDs when public identifiers are needed;
- add compatibility tests for consumed response shapes.

## Dependency And Configuration Review

When dependency or deployment configuration changes are in scope:

- check for known advisories;
- remove unused packages;
- avoid exposing frontend env values that are not meant for browsers;
- verify production debug settings are safe.

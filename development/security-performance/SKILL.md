---
name: security-performance
description: Performs security and performance reviews for Laravel 12 + Blade + MySQL applications, covering authentication, authorization, validation, CSRF, XSS, uploads, secrets, queries, caching, queues, assets, and release readiness.
---

# Security & Performance

## Role
Act as a senior application-security and performance engineer specializing in Laravel 12, Blade, and MySQL.

## Security checklist

### Authentication
- Use established Laravel authentication.
- Never implement custom password hashing casually.
- Protect sessions and credentials.
- Never expose tokens/secrets to client code.

### Authorization
- Enforce permissions server-side.
- Use policies/gates/middleware appropriately.
- Never rely on hidden buttons or route obscurity.

### Input and output
- Validate user input.
- Prevent mass assignment issues.
- Use parameterized queries.
- Escape Blade output by default.
- Raw HTML must be intentional and trusted/sanitized.

### CSRF
Do not disable CSRF as a shortcut. Fix token/session/request integration correctly.

### Uploads
Validate size/type, store safely, prevent executable uploads, and do not trust original names.

### Secrets
Keep secrets in environment/config systems. Never commit `.env`, log secrets, or return them in responses.

### Rate limiting
Consider rate limits for login, password reset, OTP, public APIs, expensive endpoints, and abuse-prone actions.

## Performance checklist

### Database
- Identify N+1 queries.
- Add indexes based on query patterns.
- Avoid unbounded lists.
- Paginate large datasets.
- Avoid unnecessary columns and eager loads.

### Laravel
- Cache only measured/known expensive work.
- Queue slow asynchronous work.
- Avoid repeated configuration/database work.

### Blade/frontend
- Optimize images.
- Avoid unnecessary JavaScript.
- Use Vite correctly.
- Avoid rendering huge tables without pagination.

## Measurement
Prefer before/after evidence where possible: query count, response time, memory, payload size, and page-load metrics.

## Release gate
Before release, verify debug mode, secrets, authorization, validation, file uploads, CSRF, safe error pages, migrations, asset builds, tests, and sensitive logging.

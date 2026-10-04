---
model_tier: medium
name: security
description: "Use when applying security best practices — authentication, authorization, CSRF protection, input sanitization, rate limiting, or secure coding — stack-agnostic."
domain: quality
workspaces:
  - engineering
packs:
  - engineering-base
---

# security

## When to use

Use when implementing authentication, authorization, or any security-sensitive functionality.

Do NOT use when:

* Validation logic only — route to the project's validation carve-out ([`laravel-validation`](../laravel-validation/SKILL.md) for Laravel; otherwise the framework-native primitive — Zod / class-validator, Pydantic, struct-tag validators).
* Full security audit — route to [`security-audit`](../security-audit/SKILL.md).
* You need a pre-implementation threat model — route to [`threat-modeling`](../threat-modeling/SKILL.md).
* You need end-to-end authorization analysis — route to [`authz-review`](../authz-review/SKILL.md).

## Stack-specific carve-outs

The procedure below is stack-agnostic. For framework-specific primitives (Laravel Policies / Gates / FormRequests, Symfony voters, NestJS guards, Next.js middleware), defer to:

| Stack | Carve-out |
|---|---|
| Laravel | [`laravel`](../laravel/SKILL.md), [`laravel-validation`](../laravel-validation/SKILL.md), [`laravel-middleware`](../laravel-middleware/SKILL.md) |
| Symfony | [`symfony-workflow`](../symfony-workflow/SKILL.md) |
| Next.js / TS | [`nextjs-patterns`](../nextjs-patterns/SKILL.md) |

## Procedure: Implement security for a feature (stack-neutral)

### Step 0: Inspect

1. Read the project's auth doc (`agents/authentication.md`, `docs/auth.md`, or framework docs).
2. Read the project's authorization doc (gates / policies / voters / guards).
3. Locate existing authorization rules in the project's idiomatic location (Laravel `app/Policies/`, Symfony `src/Security/Voter/`, NestJS `*.guard.ts`).

### Step 1: Authentication

- Identify the auth mechanism in use (session, JWT, OAuth, API token) — read the framework's auth config (`config/auth.php`, `next-auth.config.ts`, Symfony `security.yaml`, FastAPI dependency).
- Check guard / strategy / provider configuration.
- Multi-tenant identification happens **after** authentication — see [`multi-tenancy`](../multi-tenancy/SKILL.md).

### Step 2: Authorization

1. Create / locate the authz rule in the framework's idiomatic primitive (Policy, voter, guard, middleware, route dependency).
2. Apply it at the request boundary (FormRequest `authorize()`, controller / route-handler dependency, middleware chain).
3. Cover non-model gates (cross-aggregate rules) — keep them centralised, not scattered across handlers.

### Step 3: Review for adversarial

For security-sensitive changes, run [`adversarial-review`](../adversarial-review/SKILL.md).
Focus on: attack surface, trusting user input, authorization gaps.

## Conventions

→ For PHP / Laravel specifics (auth helpers, mass assignment, Blade escaping, CSRF middleware): see guideline `docs/guidelines/php/security.md`.
→ For other stacks, follow the framework's hardening guide and the carve-outs above.

### Crypto, password storage, certificates — route, do not guess

This skill carries no cryptographic parameter, key size, work factor, cipher
suite, or TLS version floor: such a value is authoritative-looking long after it stops
being true. Take it from <https://cheatsheetseries.owasp.org/> at the moment you
need it — never from memory, never from this file. Rationale and reopening
condition: [ADR-238](../../../docs/decisions/ADR-238-security-content-routes-to-external-authority.md).

### Validate

- Verify all user input is validated at the boundary via the framework's primitive — never trust raw request data.
- Confirm an authorization check exists for every state-changing action.
- Check that no raw user input reaches SQL, HTML output, shell commands, or template renderers without escaping.
- Run the project's type-checker — must pass (catches type-safety issues that enable injection).

## Output format

1. Security-hardened code with auth, input validation at the boundary, and output encoding.
2. Authorization rule (Policy / voter / guard / middleware) co-located with the route.

## Gotcha

- Validation ensures format, not intent — don't trust input after validation alone.
- "Throw" vs "boolean" authz APIs behave differently (`Gate::authorize()` throws vs `Gate::allows()` returns bool in Laravel; `CanActivate` in NestJS throws; FastAPI dependencies throw `HTTPException`). Pick based on how the framework expects failure to surface.
- Rate-limit ALL public endpoints, not just login.
- Never log passwords, tokens, or API keys.

## Do NOT

- Do NOT bypass the framework's request-validation primitive inside handlers.
- Do NOT bulk-bind raw request payloads to ORM entities without an explicit allow-list (`$fillable` / `$guarded`, DTO mapping, Pydantic model).
- Do NOT store plaintext passwords or secrets in the database.
- Do NOT expose internal error details in production API responses.

## Auto-trigger keywords

- security
- authentication
- authorization
- CSRF
- XSS
- policy

---
name: security-audit
description: Inspect code and configuration for common security risks before deployment, after sensitive feature changes, before client demo, before handover, or before merging high-risk code. Use when Codex needs to review exposed secrets, environment configuration, authentication, authorization, RBAC, API validation, injection risks, unsafe file uploads, CORS, cookies, sessions, CSRF, error messages, sensitive data exposure, logging safety, frontend storage, dependency risks, rate limiting, webhooks, external integrations, admin actions, payment-related features, staff/user management, private files, addresses, tokens, reports, customer data, and production deployment safety.
---

# Security Audit

Use this skill when code must be reviewed from a security-risk perspective.

## Core Rule

Keep findings evidence-based, specific, severity-ranked, and actionable. Do not print real secrets, do not make broad security claims from a partial review, and do not treat frontend hiding as security.

## Workflow

1. Understand audit scope:
   - whole app or feature, frontend/backend/database/deployment scope, roles, sensitive data, APIs, uploads, integrations, environment, and recent changes reviewed
2. Check for exposed secrets:
   - source, config, tests, docs, Docker, CI/CD, frontend env vars, logs, debug output, `.env` files, keys, tokens, private keys, webhook secrets, and passwords
3. Check environment configuration:
   - `.env.example`, ignored real env files, production debug mode, production URLs, secure cookies, HTTPS, secret exposure to frontend bundles, and dev settings in production
4. Check authentication:
   - password hashing, safe login errors, token signing/verification, expiration, refresh token safety, logout revocation/cleanup, inactive/banned users, reset tokens, and verification flows
5. Check backend authorization and access control:
   - role checks, ownership, user/shop/branch/tenant/organization scope, ID guessing, privileged actions, role assignment abuse, and public registration privilege escalation
6. Check API input validation:
   - required fields, types, formats, enums, lengths, ranges, files, status transitions, pagination/search limits, request size, extra fields, and nested object validation
7. Check injection risks:
   - SQL/NoSQL, command, template, path traversal, unsafe dynamic queries, eval-like behavior, shell usage, unsafe HTML rendering, and unsafe redirects
8. Check file upload security when applicable:
   - type/size/content validation, randomized names, storage location, path traversal, private access controls, signed URLs, image processing, deletion policy, and error handling
9. Check CORS, cookies, sessions, CSRF, and cross-origin behavior.
10. Check error message and logging safety:
   - stack traces, database errors, secrets, tokens, internal paths, auth enumeration, full request bodies, and safe server-only logs
11. Check sensitive data exposure:
   - API responses, frontend state, exports, reports, cache, logs, local/session/mobile storage, tokens, hashes, reset tokens, addresses, payment data, admin notes, and private files
12. Check dependency and package risk where practical.
13. Check rate limiting and abuse protection:
   - login, registration, reset, OTP, upload, public forms, search, webhooks, payment callbacks, reports, AI endpoints, and email/SMS sending
14. Check webhook and external integration security:
   - signature verification, shared secrets, timestamp/replay protection, idempotency, retries, logging, and permission boundaries
15. Check admin and privileged actions:
   - role changes, refunds, payment status, exports, deletes, settings, audit logs, API keys, and destructive overrides
16. Assign severity:
   - Critical, High, Medium, Low, or Informational, with impact and deployment blocking status
17. Recommend specific fixes and security tests.
18. Provide deployment recommendation:
   - safe to deploy, safe with fixes, or do not deploy until issues are fixed
19. Summarize scope, findings, severity, affected files/areas, risks, fixes, checks, and follow-up actions.

Read `references/security-audit-checklist.md` for detailed security review categories, severity guidance, test recommendations, deployment recommendation rules, and the final report format.

## Non-Negotiable Rules

- Do not print real secrets in the report.
- Do not claim the app is secure after only a partial review.
- Do not ignore backend authorization.
- Do not treat frontend hiding as security.
- Do not ignore cross-user, cross-shop, cross-branch, or cross-tenant access risks.
- Do not ignore file upload risks.
- Do not ignore injection risks from user input.
- Do not ignore production configuration.
- Do not expose sensitive data in examples.
- Do not remove security controls for convenience.
- Do not suggest disabling validation, auth, or permission checks.
- Do not run destructive commands.
- Do not make broad security claims without evidence.
- Keep findings specific, actionable, and severity-ranked.

## Output Contract

When using this skill, provide:

1. Audit scope and overall risk assessment.
2. Severity-ranked findings summary.
3. Critical, high, medium, low, and informational findings as applicable.
4. Authentication review.
5. Authorization and access control review.
6. Input validation and injection review.
7. File upload review when applicable.
8. Data exposure, logging, frontend storage, and error message review.
9. Configuration, CORS, cookies/session, dependency, webhook, rate-limit, and admin action review as applicable.
10. Security tests or checks recommended.
11. Deployment recommendation.
12. Follow-up actions.

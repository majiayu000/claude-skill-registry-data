---
name: auth-flow-design
description: Design authentication and authorization flows for backend APIs and applications. Use when Codex is asked to plan login, sessions, tokens, roles, permissions, OAuth/OIDC, API keys, service accounts, tenant access, or auth-related error behavior.
license: MIT
---

# Auth Flow Design

## Core Workflow

1. Identify actors, clients, trust boundaries, data sensitivity, and existing
   identity provider or auth stack.
2. Separate authentication, authorization, session/token handling, and audit
   requirements.
3. Define flows for login, token issuance, refresh, logout/revocation, service
   access, permission checks, and failure behavior.
4. Specify where checks happen: gateway, middleware, service layer, database, or
   external provider.
5. Document abuse cases, least privilege, tenant isolation, and review gates.
6. Include tests and operational checks for auth regressions.

## Safety Rules

- Do not invent provider-specific behavior without checking current official
  docs when details matter.
- Do not recommend storing plaintext secrets, long-lived broad tokens, or
  client-trusted authorization decisions.
- Escalate auth flows involving payments, admin access, customer data,
  multi-tenant isolation, or regulated data.

## Deliverable Shape

For auth flow plans, provide:

- Actors and trust boundaries
- Authentication flow
- Authorization model
- Token/session lifecycle
- Permission checks and enforcement points
- Error behavior and audit events
- Abuse cases and mitigations
- Test plan and review gates

## References

- Read `references/auth-flow-design-checklist.md` when designing or reviewing
  backend auth flows.

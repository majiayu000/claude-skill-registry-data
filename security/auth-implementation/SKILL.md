---
name: auth-implementation
description: Implement authentication and authorization with supported mechanisms. Triggers on "implement auth", "实现认证".
---

# Auth Implementation

## When to use

- Implement authentication and authorization with supported mechanisms.

**Not for:** security-review for auditing existing security.

## Steps

1. Identify actors, trust boundaries, session lifecycle and provider; check current official guidance.

2. Implement the chosen flow, secure credential handling, expiration and revocation without custom cryptography.

3. Enforce server-side ownership and tenant authorization, including login, logout and session renewal behavior.

4. Test real allowed and denied paths, expiration, revocation and cross-user access in an isolated environment.

## Verify

- Tests cover authentication and object authorization; sessions use supported mechanisms and no secrets leak.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/token-patterns.md](references/token-patterns.md) — session-vs-token decision matrix, JWT structure, refresh-token rotation + reuse detection, revocation strategies
- [references/oauth-flows.md](references/oauth-flows.md) — Authorization Code + PKCE, Client Credentials, Implicit deprecation, Token Exchange (RFC 8693)

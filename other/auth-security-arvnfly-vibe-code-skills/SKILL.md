---
name: auth-security
description: "Authentication and authorization security, JWT lifecycle, OAuth 2.1 and OIDC flows, PKCE, and RBAC/ABAC access control."
---

# Authentication & Access Control Security Protocol

When implementing login, session tokens, identity providers, or role permissions, enforce these standards.

---

## 1. Token Lifecycles & Storage

1. **Short-Lived Access Tokens**:
   - Access tokens should expire in 10-15 minutes.
   - Refresh tokens should be long-lived (e.g. 7-30 days) and stored in HttpOnly; Secure; SameSite=Lax cookies, never in localStorage.
2. **Refresh Token Rotation**:
   - Invalidate the old refresh token immediately upon issuing a new pair.
   - If an invalidated refresh token is reused, revoke the entire token family immediately (indicates token theft).

---

## 2. OAuth 2.1 & PKCE

1. Always use Proof Key for Code Exchange (PKCE) for both public (SPA, mobile) and confidential clients.
2. Eliminate the deprecated OAuth 2.0 Implicit Flow.
3. Validate state and nonce parameters strictly to prevent CSRF authentication replay attacks.

---

## 3. RBAC & ABAC Enforcement

1. Perform authorization checks at the data service/controller boundary, never rely solely on frontend UI hiding.
2. Enforce tenancy boundaries: Every query must verify that the requesting user's organization matches the target resource.

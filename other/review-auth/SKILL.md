---
name: review-auth
description: >
  Audit authentication and authorization paths for common misconfigurations,
  bypass risks, and IDOR vulnerabilities. Use before shipping any
  auth-related change or during a security review. Trigger on "is this auth
  code secure", "check for IDOR vulnerabilities", "review my auth logic",
  "can users access data they shouldn't", or "audit our permission checks".
  This is the deep, dedicated auth audit — review-changes only flags auth
  issues in passing during a general review; use this skill when auth needs
  focused scrutiny.
---

# review-auth

## You are an authentication and authorization security reviewer. Your job is to find auth bypass risks, misconfigured guards, missing ownership checks, and insecure token handling. Be thorough and specific — vague "consider adding auth" notes are not useful.

## Step 1 — Map the auth infrastructure

Locate the core auth machinery:

- authentication middleware (JWT verification, session validation, API key checking)
- authorization guards, decorators, or middleware (role checks, permission checks, policy evaluators)
- the user/session extraction mechanism (how `req.user`, `ctx.user`, or equivalent is set)
- token issuance and validation logic (login, token refresh, logout, token revocation)

Search for:

```
isAuthenticated, requireAuth, @UseGuards, @Roles, authorize, checkPermission,
verifyToken, validateSession, currentUser, passport, jwt.verify, session.get
```

Read the core files to understand:

- what a "valid" authenticated request looks like
- how roles or permissions are represented (string enum, bitmask, RBAC, ABAC)
- how the auth layer passes identity information to handlers

**NestJS.** If the project uses NestJS (`@nestjs/core` in `package.json`), also apply the framework checks in [references/nestjs.md](references/nestjs.md), covering sign-in that reveals which accounts exist, guard metadata and order, claims versus database roles, long-lived connections and shared caches. A documented convention still wins over them.

---

## Step 2 — Audit route and handler coverage

Find all routes, controllers, handlers, and resolvers in the application.

For each one, determine:

- is it protected by the authentication middleware/guard?
- is it protected by an authorization check (role, permission, or ownership)?
- is the protection applied correctly (middleware order matters; a guard applied after a data fetch is too late)?

Build a list of:

- **Unprotected routes**: routes that serve sensitive data or perform mutations without authentication
- **Under-authorized routes**: routes that authenticate the user but do not check whether the user is _allowed_ to perform the operation
- **Incorrectly ordered middleware**: auth middleware applied after other middleware that exposes data

Flag any route that:

- exposes user data without verifying the caller owns that data
- performs a write or delete without verifying the caller has permission
- is missing auth in a group where all other routes are protected (likely accidental omission)

---

## Step 3 — Check for IDOR vulnerabilities

Insecure Direct Object Reference: the user can access any record by guessing or iterating an ID, even if it belongs to another user.

Look for handlers that:

- accept a resource ID as a path parameter or query parameter (e.g., `/orders/:id`, `/users/:userId/documents`)
- fetch the resource directly by that ID without checking ownership

Example vulnerable pattern:

```typescript
// Missing ownership check — any authenticated user can fetch any order
async getOrder(orderId: string, user: User) {
  return this.db.order.findUnique({ where: { id: orderId } });
}
```

Safe pattern:

```typescript
async getOrder(orderId: string, user: User) {
  const order = await this.db.order.findUnique({ where: { id: orderId } });
  if (!order || order.userId !== user.id) throw new ForbiddenException();
  return order;
}
```

Flag every handler that loads a resource by ID without a subsequent ownership or permission check.

---

## Step 4 — Review token validation logic

Inspect JWT or session token validation:

**JWT risks:**

- `algorithm: 'none'` accepted — allows tokens without a signature
- `algorithms` array not specified — allows algorithm confusion attacks
- `exp` claim not validated — tokens never expire
- `aud` (audience) or `iss` (issuer) not validated — tokens from other services accepted
- token stored in `localStorage` instead of `httpOnly` cookie (XSS exposure)
- no token revocation mechanism (logout does not invalidate the token)

**Session risks:**

- session secret is weak or hardcoded
- `secure` flag not set on session cookie in production
- `httpOnly` flag not set
- `sameSite` not set (CSRF exposure)
- session not invalidated on logout

**Refresh token risks:**

- refresh tokens not rotated on use
- refresh tokens not invalidated after account deletion or password change
- refresh tokens stored in a way that can be stolen (localStorage, non-httpOnly cookie)

---

## Step 5 — Check for common auth misconfigurations

**Wildcard roles:**

- any check like `if (user.role === 'admin' || true)` or overly broad conditions
- role hierarchies that grant more than intended

**Test/dev environment leakage:**

- auth middleware disabled by environment variable checked at runtime
- `NODE_ENV === 'test'` bypasses that could be triggered in production
- hardcoded test credentials or bypass tokens in non-test code

**Rate limiting:**

- login endpoints without brute-force protection
- token refresh endpoints without rate limiting
- password reset endpoints without rate limiting

**Privilege escalation:**

- endpoints that allow a user to change their own role
- user update endpoints that accept a `role` field without restricting who can set it

---

## Step 6 — Report findings

```text
Auth review findings
──────────────────────────────────────────────────

1. [high] <title> — `path/to/file:line`
   <what the vulnerability is>
   <the scenario in which it can be exploited>
   <concrete fix>

2. [medium] <title> — `path/to/file:line`
   <issue and scenario>
   <fix>

3. [low] <title> — `path/to/file:line`
   <issue and fix>

Unprotected routes
  <list routes that appear to be missing auth — may be intentional (public routes), confirm with the team>

Token configuration
  <JWT/session configuration summary with issues highlighted>

Summary
  <overall verdict: no critical issues / issues found that need addressing before shipping>
```

If a finding is uncertain (e.g., a route might be intentionally public), flag it as a question rather than a confirmed vulnerability.

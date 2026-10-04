---
name: auth-review
description: Perform a defensive review of authentication and authorization flows in an authorized codebase. Use for login, session, MFA, OAuth, password reset, cookie security, JWT validation, impersonation, privilege checks, and object-level access control.
---

# Auth Review

## Focus

- login and logout correctness
- session fixation and invalidation
- cookie flags and token storage
- reset, invite, recovery, and MFA flows
- server-side authorization and object-level checks
- impersonation, elevation, and admin escape hatches

## Review prompts

- Are checks enforced server-side on every sensitive action?
- Does auth depend on user-controlled headers, origins, or claims?
- Are session boundaries rotated after identity change?
- Can one user access another user's objects through predictable identifiers?

## Output

Use the Patchman findings format and call out auth assumptions explicitly.

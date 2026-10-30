---
name: broken-access-control
description: Detects missing ownership checks, broken role enforcement, and IDOR
  vulnerabilities that let users access other users' resources. Use when
  writing code that checks authorization, enforces resource ownership, handles
  IDOR (object-level authorization), processes server-side requests to
  external URLs, or implements access control middleware.
---

# Broken Access Control Security Check (A01:2025)

## What this checks

Protects against unauthorized resource access caused by missing ownership checks or
role enforcement. Exploitation leads to horizontal/vertical privilege escalation.
For SSRF (server-side request forgery), see the dedicated `ssrf` skill.

## Vulnerable patterns

- Resource lookup by caller-supplied identifier with no ownership predicate before the row is returned, mutated, or acted on
- Privileged or admin route mounted with no role check at the route/controller declaration
- Ownership check that runs after the resource has already been fetched and consumed by downstream logic
- Ownership failure that responds with a distinct "forbidden" status, leaking that the resource exists

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Every resource lookup by caller-supplied identifier is gated before the resource
   is returned, mutated, or acted on.** The gate binds the row to the authenticated
   caller — an ownership predicate for per-instance access, or a role predicate for
   role-scoped access. The check can live in a handler, interceptor, filter, annotation,
   decorator, or middleware — anywhere, as long as it runs before the data is used.
2. **Privileged routes enforce role membership through a reusable, centrally-declared
   mechanism** (middleware, filter chain, annotation, decorator, policy) attached at
   the route or controller declaration. Ad-hoc `if role != "admin"` checks inside
   handler bodies are brittle — they can be forgotten on a new route and they're
   invisible at a glance.
3. **Ownership failures return an indistinguishable "not found" response (HTTP 404).**
   Returning 403 leaks that the resource exists. Role-missing failures on a privileged
   route may still return 403 — the route itself is public knowledge, so only the
   *instance-level* check needs to hide behind 404.

Translate these principles to the audited file's language and framework. Use the
documented authorization or policy mechanism for that stack; do not invent ad-hoc
checks in handler bodies.

## Verification

Confirm these properties hold (language-agnostic):

- [ ] Every resource lookup by caller-supplied identifier is gated by an ownership or role predicate before the resource is returned, mutated, or acted on — regardless of whether the check lives in a handler, interceptor, filter, annotation, decorator, or middleware
- [ ] Privileged routes enforce role membership through a reusable, centrally-declared mechanism (middleware, filter chain, annotation, decorator, policy) attached at the route/controller declaration — not via ad-hoc `if` checks inside individual handler bodies
- [ ] Ownership (per-instance IDOR) failures return an indistinguishable "not found" response (e.g. HTTP 404) rather than a distinct "forbidden" response, to prevent resource enumeration. Role-missing failures on a privileged route may use 403 because the route itself is public knowledge

## References

- CWE-284 ([Improper Access Control](https://cwe.mitre.org/data/definitions/284.html))
- CWE-862 ([Missing Authorization](https://cwe.mitre.org/data/definitions/862.html))
- CWE-863 ([Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html))
- CWE-918 ([Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html))
- [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

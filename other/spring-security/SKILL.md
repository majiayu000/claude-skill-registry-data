---
name: spring-security
description: "Spring Security: authentication, method/URL authorization, CSRF/CORS/session/JWT/OAuth2, password storage, security testing. Use for securing Spring apps; pairs with frameworks/spring-boot."
---

# spring-security

Deny by default, permit explicitly, test as an attacker.

## Activate when

- Adding login, JWT/OAuth2 resource-server setup, method security, CSRF/CORS, session handling, or password storage to Spring apps.

## Do NOT activate for

- Non-Spring auth (see backend/authentication); general service structure (see frameworks/spring-boot).

## Procedure

1. Version: detect Spring Boot/Security generation from build files; research in https://docs.spring.io/spring-security/reference/ for THAT generation (configuration style changed across generations — never copy config across generations without checking).
2. Architecture: filter chain explicit; authorization rules most-specific-first with deny-by-default tail; method security (`@PreAuthorize`) for service boundaries, URL rules for coarse gates.
3. Authentication: form/oauth2Login for interactive, JWT validation for resource servers (issuer/audience/expiry enforced, JWKS cached); passwords with adaptive hashing (bcrypt/scrypt/argon2, work factor reviewed); sessions with fixation protection, concurrency limits, and logout invalidation.
4. CSRF/CORS: CSRF tokens for cookie/session flows (disabled only for stateless token APIs, deliberately); CORS allowlisted origins/methods/headers, never `*` with credentials.
5. Secrets/headers: credentials externalized; security headers enabled; error responses free of stack traces and user-enumeration oracles.
6. Testing: `@WithMockUser`/`@WithUserDetails` for slices plus at least one full-chain test per critical rule; cross-user access tests fail closed.
7. Verify: unauthenticated, low-privilege, and cross-tenant probes against every new endpoint; config diff reviewed line by line.

## Failure modes

- Permit-all ordering mistakes; CSRF disabled globally; JWT accepted without issuer/audience checks; method security enabled nowhere (annotation present, enforcement off).

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (spring-security, spring-boot, oauth, oidc).
- Related: `../spring-boot/`, `../../backend/authorization/`, `../../security/secure-baseline/`.

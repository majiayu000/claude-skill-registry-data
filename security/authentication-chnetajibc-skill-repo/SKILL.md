---
name: authentication
description: "Authentication: JWT/OAuth-OIDC/sessions/API keys, password storage, secrets, CSRF/CORS/cookies. Verify with evidence; server-side checks only."
---

# authentication

Prove identity server-side; store secrets like attackers read your repo — because they might.

## Activate when

- Adding login, tokens, sessions, API keys, password handling, or cookie/auth-header flows.

## Do NOT activate for

- Permission modeling (see authorization); Spring wiring (see frameworks/spring-security).

## Procedure

1. Mechanism per threat model: sessions (web, with fixation/CSRF handling), JWT (services/mobile, issuer/audience/expiry enforced), OAuth2/OIDC via provider (never hand-rolled), API keys with scopes + rotation.
2. Passwords: adaptive hashing (bcrypt/scrypt/argon2, reviewed cost), no custom crypto, enumeration-safe errors, rate-limited attempts.
3. Tokens: short lifetimes, refresh rotation with reuse detection, revocation path; cookies `HttpOnly`/`Secure`/`SameSite`, CORS allowlisted.
4. Secrets externalized (vault/env); none in code, logs, or error messages.
5. Verify: auth matrix (valid/expired/forged/absent) green, cross-checked against docs for the installed library versions.

## Failure modes

- JWT accepted without issuer/audience/expiry checks; sessions without fixation protection; passwords with fast hashes; CSRF disabled globally 'temporarily'; secrets in error responses or logs; clock-skew lockouts with no test.

## Escalation

- Spring wiring → frameworks/spring-security; protocol doubts → research/documentation-search for the installed library version.

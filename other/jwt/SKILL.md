---
name: JWT
slug: jwt
version: 1.0.1
description: Implement secure JWT authentication with proper validation, token lifecycle, and key management.
homepage: https://clawic.com/skills/jwt
metadata:
  clawdbot:
    emoji: 🔐
    os:
    - linux
    - darwin
    - win32
    displayName: JWT
---

## Quick Reference

| Topic | File |
|-------|------|
| Algorithm selection | `algorithms.md` |
| Token lifecycle | `lifecycle.md` |
| Validation checklist | `validation.md` |
| Common attacks | `attacks.md` |

## Security Fundamentals

- JWTs are signed, not encrypted—anyone can decode and read the payload; never store secrets in it
- Always verify signature before trusting claims—decode without verify is useless for auth
- The `alg: none` attack: reject tokens with algorithm "none"—some libraries accepted unsigned tokens
- Use strong secrets: HS256 needs 256+ bit key; short secrets are brute-forceable

## Algorithm Choice

- HS256 (HMAC): symmetric, same key signs and verifies—good for single service
- RS256 (RSA): asymmetric, private key signs, public verifies—good for distributed systems
- ES256 (ECDSA): smaller signatures than RSA, same security—preferred for size-sensitive cases
- Never let the token dictate algorithm—verify against expected algorithm server-side

## Required Claims

- `exp` (expiration): always set and verify—tokens without expiry live forever
- `iat` (issued at): when token was created—useful for invalidation policies
- `nbf` (not before): token not valid until this time—for scheduled access
- Clock skew: allow 30-60 seconds leeway when verifying time claims

## Audience & Issuer

- `iss` (issuer): who created the token—verify to prevent cross-service token theft
- `aud` (audience): intended recipient—API should reject tokens for other audiences
- `sub` (subject): who the token represents—typically user ID
- Token confusion attack: without aud/iss validation, token for Service A works on Service B

## Token Lifecycle

- Access tokens: short-lived (5-15 min)—limits damage if stolen
- Refresh tokens: longer-lived, stored securely—used only to get new access tokens
- Refresh token rotation: issue new refresh token on each use, invalidate old one
- Revocation is hard—JWTs are stateless; use short expiry + refresh, or maintain blacklist

## Storage

- httpOnly cookie: immune to XSS, but needs CSRF protection
- localStorage: vulnerable to XSS, but simpler for SPAs
- Memory only: most secure, but lost on page refresh
- Never store in URL parameters—visible in logs, history, referrer headers

## Validation Checklist

- Verify signature with correct algorithm (don't trust header's alg)
- Check `exp` is in future (with clock skew tolerance)
- Check `iat` is not unreasonably old (optional policy)
- Verify `iss` matches expected issuer
- Verify `aud` includes your service
- Check `nbf` if present

## Common Mistakes

- Storing sensitive data in payload—it's just base64, not encrypted
- Huge payloads—JWTs go in headers; many servers limit header size to 8KB
- No expiration—indefinite tokens are security nightmares
- Same secret across environments—dev tokens work in production
- Logging tokens—they're credentials; treat as passwords

## Key Rotation

- Use `kid` (key ID) claim to identify which key signed the token
- JWKS (JSON Web Key Set) endpoint for public key distribution
- Overlap period: accept old key while transitioning to new
- After rotation, old tokens still valid until they expire—plan accordingly

## Implementation

- Use established libraries—don't implement JWT parsing yourself
- Libraries: `jsonwebtoken` (Node), `PyJWT` (Python), `java-jwt` (Java), `golang-jwt` (Go)
- Middleware should reject invalid tokens early—before any business logic

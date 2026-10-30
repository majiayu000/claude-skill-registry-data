---
name: oauth-implementation
description: Detects weak JWT validation, loose redirect_uri matching, and missing state
  parameters in OAuth/OIDC flows. Use when writing OAuth2 or OpenID Connect
  flows, JWT validation logic, token endpoint handling, or redirect URI
  processing. Also invoke when implementing any code that parses or verifies
  JWTs.
---

# OAuth/OIDC Implementation Security (OWASP A07:2025)

## What this checks

Prevents authentication bypasses from weak JWT validation, open redirects from loose
`redirect_uri` matching, and CSRF from missing `state` parameters. These flaws allow
account takeover and session hijacking.

## Vulnerable patterns

- JWT decode call that accepts the `none` algorithm, or accepts an attacker-supplied algorithm header — enabling algorithm-confusion bypass.
- `redirect_uri` validated by prefix match, substring match, or regex — letting an attacker host a lookalike domain whose URL passes the check.
- JWT decode that omits audience (`aud`) validation — a token minted for a sibling service passes signature verification but should not be honored here.
- Tokens stored in browser web storage (e.g. `localStorage`) where any same-origin script can read them.
- OAuth authorization request sent with no `state` parameter, or with a `state` that is not bound to and verified against the initiating session.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language and
OAuth/JWT library — use the library's documented secure-by-default APIs rather
than mirroring an example from another stack.

1. **JWT verification pins algorithms to an explicit allowlist** that never
   includes `none` and never permits switching between symmetric and asymmetric
   families (the classic HS256/RS256 public-key-as-HMAC attack). For broader JWT
   handling guidance, see the `authentication-failures` skill.
2. **Redirect URIs match exactly against an allowlist set.** Prefix matching,
   substring matching, and regex matching all have known bypass classes —
   percent-encoded tricks, userinfo smuggling, lookalike subdomains. The only
   safe comparison is exact string equality against a set of registered URIs.
3. **Every JWT decode validates `aud` (audience) and required claims.** A token
   minted for a different service of the same issuer will pass signature
   verification; only the audience check catches the confused-deputy case.
   Require `exp`, `iat`, `sub` at minimum.
4. **State parameter ties the callback to the initiating session.** Generate a
   CSPRNG `state`, store it in the session before redirect, compare it on the
   callback. Without this the OAuth flow is CSRF-forgeable.
5. **Tokens live in a Secure, HttpOnly, SameSite cookie or in memory — not
   web storage.** Browser storage is readable by any same-origin script, so one
   XSS compromise exfiltrates every token.

## Verification

Confirm the response:

- [ ] Algorithm parameter is an explicit allowlist and never includes `none`
- [ ] `redirect_uri` is checked with exact-match equality against an allowlist set
- [ ] Audience is validated in every JWT decode call
- [ ] `state` parameter is generated, stored in session, and compared on callback
- [ ] Tokens are not stored in browser web storage

## References

- CWE-287 ([Improper Authentication](https://cwe.mitre.org/data/definitions/287.html))
- CWE-601 ([Open Redirect](https://cwe.mitre.org/data/definitions/601.html))
- CWE-346 ([Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html))
- [OWASP A07:2025 Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

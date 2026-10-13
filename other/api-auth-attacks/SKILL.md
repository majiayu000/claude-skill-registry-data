---
name: api-auth-attacks
description: >
  Break API authentication: token handling, key leakage, weak session/JWT, and no-auth
  endpoints. Load on REST/GraphQL APIs using API keys, Bearer tokens, HMAC signing, or basic
  auth. Signals: `Authorization` headers, api_key params, tokens in URLs, /v1 vs /v2 auth drift.
domain: api
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp_api: [API2:2023-Broken-Authentication]
cwe: [CWE-287, CWE-306]
tools: [burp, jwt_tool]
schema_version: 1
---

# API authentication attacks

## When it applies
An API authenticates requests via tokens/keys/sessions. Auth is the gate; weaknesses here open
everything behind it.

## Why it works
APIs sprawl (many endpoints, versions, clients) so authentication is applied inconsistently:
some routes forgot it, tokens are long-lived or weakly signed, keys leak client-side, and
error/timing differences enable enumeration and brute force.

## Method
1. **No-auth endpoints**: replay requests with the token removed; probe `/v1` vs `/v2`,
   `/internal`, `/debug`, and undocumented routes (Swagger/OpenAPI) for missing auth.
2. **Token weaknesses**: JWT issues (→ `web-auth-jwt`: alg confusion, weak secret, none); long/
   non-expiring tokens; predictable session ids; token accepted in URL (logged/leaked).
3. **Key leakage**: hunt keys in JS bundles, mobile apps, git (→ `code-review-secrets-detection`),
   and test their privilege/scope.
4. **Brute/enumeration**: username enumeration via login/reset differences; weak rate limits on
   login/OTP (→ `web-race-conditions` for OTP windows).
5. **Auth logic**: password reset token predictability/leak, 2FA bypass, "remember me" tokens.

## Gotchas
- Test every version and verb — the fix may exist only on the newest route.
- A leaked key must be *live and privileged* to matter — validate scope, don't over-collect.
- Rate-limit "bypass" via parallelism or header rotation is reportable on many programs.

## Verify success
Authenticated access without valid credentials (no-auth route, forged/replayed token, or a live
leaked key performing a privileged action).

## References
OWASP API Security Top 10 (API2); PortSwigger auth labs.

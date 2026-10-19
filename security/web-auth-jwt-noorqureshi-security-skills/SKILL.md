---
name: web-auth-jwt
description: >
  Attack JWT/session authentication. Load when auth uses a JWT (three base64url parts,
  header.payload.signature), Authorization: Bearer, or you see alg/kid/jku fields. Signals:
  eyJ... tokens, "alg":"none"/"HS256"/"RS256", kid header, JWKS endpoints, role/admin claims.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A07:2021-Auth-Failures]
owasp_api: [API2:2023-Broken-Authentication]
cwe: [CWE-347, CWE-287]
tools: [jwt_tool, hashcat, burp]
schema_version: 1
---

# JWT / token authentication attacks

## When it applies
The app authenticates with a JSON Web Token and trusts claims inside it (user id, role,
`isAdmin`). The win is forging a valid-looking token the server accepts.

## Why it works
JWTs are only as safe as their signature verification. Implementations routinely skip it,
confuse algorithms, or trust attacker-controlled key hints (`kid`, `jku`, `x5u`). If you can
make the server accept a signature you produced, you own every claim.

## Method
> **Payloads & full variation set:** [`cheatsheet.md`](cheatsheet.md) next to this file — work the set, not the first line.
1. **Decode & read claims**: `jwt_tool <token>` — look for `role`, `admin`, `sub`, weak `exp`.
2. **alg=none**: strip the signature and set header `{"alg":"none"}`; some libs accept it.
3. **Algorithm confusion RS256→HS256**: if the server verifies RS256 with the *public* key,
   re-sign HS256 using that public key as the HMAC secret — server verifies with the same key.
   `jwt_tool -X k -pk public.pem`.
4. **Weak HMAC secret**: crack HS256 offline — `hashcat -m 16500 token.txt rockyou.txt`; if it
   falls, mint any token.
5. **kid / jku / x5u abuse**: `kid` path traversal or SQLi to control the key file; `jku`/`x5u`
   pointing at *your* JWKS so the server fetches your public key and you sign with your private key.

## Gotchas
- Editing claims without re-signing fails unless verification is broken — confirm the vuln class first.
- `exp`/`nbf` may be enforced even when signature isn't — keep timestamps valid.
- Public key sourcing: grab it from `/.well-known/jwks.json`, a cert, or TLS if not published.

## Verify success
Server accepts a token you forged with elevated claims (e.g. admin panel loads, or an
authenticated endpoint returns another user's data with your minted `sub`).

## References
PortSwigger JWT labs; jwt_tool wiki; Auth0 "Critical vulnerabilities in JWT libraries".

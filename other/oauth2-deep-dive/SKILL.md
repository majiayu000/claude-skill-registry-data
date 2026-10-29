---
name: oauth2-deep-dive
description: Use when assessing OAuth 2.0 and OpenID Connect
  implementations on an authorized engagement. Covers flow selection,
  redirect URI validation, code and token theft, PKCE review, and
  common misconfigurations. Also use when a "login with" integration
  needs a thorough security review.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [oauth-attacks, auth-attacks, jwt-attacks, open-redirect]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

OAuth 2.0 delegates login to an identity provider, and every shortcut
in the flow becomes an account takeover: open redirect URIs, leaked
codes, missing state. This skill goes deeper than the oauth-attacks
overview: full flow analysis, redirect URI bypass techniques, PKCE
verification, and token handling review. Test with accounts you own
on systems you may assess.

## Quick Workflow

1. Map the flow: which grant type, which endpoints, and the exact
   redirect URIs registered.
2. Capture a full login in Burp and label every parameter.
3. Test redirect URI validation: bypasses via subdomains, paths, and
   fragments.
4. Test code theft and replay: can a code be used twice or by another
   client.
5. Verify PKCE: is it required, and is the verifier actually checked.
6. Review token storage and scope: where tokens live and what they
   allow.
7. Test state and nonce: CSRF on the login flow itself.
8. Document each bypass with the exact crafted URL.

## 1. Flow capture and redirect URI tests

```bash
# Capture the authorization request (start login in the browser via Burp)
# Example structure to label:
# response_type=code & client_id=... & redirect_uri=... & scope=... & state=...
echo "save the full authorize URL; every test mutates one parameter"
```

```bash
# Redirect URI bypass attempts (use your own test client registration)
BASE="https://idp.example/authorize?client_id=TEST&response_type=code"
for uri in \
  "https://app.example.evil.com" \
  "https://app.example/callback/../evil" \
  "https://app.example%2e evil.com" \
  "https://app.example/callback?next=evil.com" ; do
  echo "=== $uri"
  curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" \
    "$BASE&redirect_uri=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$uri")&state=x"
done
# A redirect to your attacker domain with a code = account takeover primitive
```

## 2. Code handling and PKCE

```bash
# Code replay: use the same code twice (second use must fail)
curl -s -X POST 'https://idp.example/token' \
  -d "grant_type=authorization_code&code=$CODE&redirect_uri=$REDIR&client_id=TEST" | head -c 200
echo "--- replay ---"
curl -s -X POST 'https://idp.example/token' \
  -d "grant_type=authorization_code&code=$CODE&redirect_uri=$REDIR&client_id=TEST" | head -c 200
```

```bash
# PKCE check: send a wrong verifier and see if the token still issues
# Generate: verifier=random, challenge=BASE64URL(SHA256(verifier))
python3 - << 'PY'
import secrets, hashlib, base64
v = secrets.token_urlsafe(32)
c = base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b"=").decode()
print("verifier:", v)
print("challenge:", c)
print("test: authorize with challenge, then redeem with a WRONG verifier")
PY
```

## 3. State, nonce, and token review

```bash
# State CSRF: drop or replay the state parameter
# If login completes with a missing or attacker chosen state, the flow
# is CSRF-able (login CSRF -> session fixation class issues)
echo "test: authorize with state=A, return with state=B; must be rejected"
```

```bash
# Token review: decode the id_token and access token
echo "$ID_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -m json.tool | head -30
# Check: aud matches your client, iss is the real IdP, exp is short,
# nonce matches the request
```

## Edge cases

- The IdP is a social provider you cannot reconfigure. Test the
  client's validation, since the IdP side is fixed.
- Mobile app flows use custom URI schemes. Test scheme hijacking
  only on your own test device.
- The flow uses response_mode=form_post. CSRF tests change shape;
  the code still must bind to state.
- PKCE is optional on this IdP. Recommend requiring it for all
  public clients.

## Escalation

- Redirect bypass found: prove code theft end to end with your test
  accounts, then stop; this is account takeover.
- Code replay works: check token binding and sender constrained
  tokens as the fix direction.
- Everything holds: review the less common angles (JWT request
  objects, pushed authorization requests) if in scope.

## Detection and defender view

Defenders see OAuth attacks as authorization requests with odd
redirect URIs, token redemptions from unexpected IPs, and replayed
codes. Detect with redirect URI allowlist alerts, code reuse
alerts, and token usage anomaly detection. The durable fix is strict
redirect URI matching, PKCE for public clients, single use codes
bound to the client, and short lived tokens.

## Key references

- RFC 6749 (OAuth 2.0) and RFC 7636 (PKCE).
- CWE-601 (URL Redirection to Untrusted Site): redirect URI bypass.
- CWE-287 (Improper Authentication): code and token flaws.
- OAuth Security Best Current Practice (IETF draft/RFC).

## See also

- `oauth-attacks`: Use it instead for exploit-focused coverage, including authorization code interception and replay and PKCE downgrade.

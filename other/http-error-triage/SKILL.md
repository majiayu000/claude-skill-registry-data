---
name: http-error-triage
description: Run before concluding anything from an HTTP error on a third-party API. Separates a real credential/entitlement problem from a CDN or WAF block, a wrong endpoint, or a client-signature ban. Use whenever an API returns 401/403/402/429 and you are about to say "the key is dead", "credits are exhausted", "the plan lacks access", or "we are rate limited".
---

# HTTP error triage

An HTTP error tells you a request failed. It usually does **not** tell you why.
Concluding "the key is dead" from a 403 is a guess wearing a number.

Born from a real incident (2026-07-30): a third-party contact-enrichment API
returned `403 error code: 1010` to every call for six days. It was read as "key
not entitled", "credits exhausted", "monthly quota reached". A 756-line browser
automation workaround was built on that belief, and a customer was nearly asked
to check a plan that was fine. The actual cause was a missing `User-Agent`, so
the CDN banned the client at the edge. One header fixed it: 200 OK, full data,
and the credit balance had been there the whole time.

## Run these three controls before you diagnose

**1. The invalid-credential control.** Send the same request with a deliberately
garbage credential, and again with none at all.

```python
for label, key in [("real", REAL_KEY), ("garbage", "0"*36), ("empty", "")]:
    ...  # same URL, same method, same headers
```

If all three return the **same** status and body, the error is not about your
credential. It carries zero information about entitlement, quota or validity.
Stop reasoning about the key.

**2. The nonsense-path control.** Request a path that certainly does not exist,
and the site root.

```
GET https://api.example.com/definitely-not-a-real-path-12345
GET https://api.example.com/
GET https://www.example.com/          # their marketing site
```

If the API error also comes back from the marketing site, you are being blocked
**in front of** the origin. Nothing about the API call will help.

**3. Read the response headers, not just the body.**

```python
except urllib.error.HTTPError as e:
    print(e.code, e.headers.get("server"), e.read()[:200])
```

`server: cloudflare` on an "auth" error is the giveaway. So are `cf-ray`,
`x-amzn-waf`, `akamai`. Those are infrastructure, not the API.

## Known signatures

| Symptom | Real cause | Fix |
|---|---|---|
| `403` + body `error code: 1010`, `server: cloudflare` | Cloudflare banned the client signature | Send a real browser `User-Agent` |
| Same error for every path incl. `/` | Edge/WAF block or IP ban | Change UA, then IP/proxy |
| `402` | Genuinely out of credits: the request **authenticated** | Top up; the key is fine |
| `429` right after a success | Real rate limit | Pace requests, add backoff |
| `400` with a field message | You reached the API and auth passed | Fix the payload; this is good news |

A `400` validation error is a **success signal** for triage: it proves auth was
accepted.

## Default headers for any server-side API call

Python's `urllib` sends `User-Agent: Python-urllib/3.x`, which many WAFs ban
outright. Always set:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
```

## Then measure cost before any sweep

Once it works, do not estimate spend. Read usage before and after one call, and
read the provider's own billing field in the response.

```python
before = usage(); result = call(); after = usage()
print("charged:", result.get("billing"), "| measured:", before - after)
```

## What to report

State what you tested and what remains unknown. "Both keys 403" is not a finding
if an empty key returns the same 403. Say instead: "403 is uninformative here, a
null credential returns it too; the cause is upstream of auth."

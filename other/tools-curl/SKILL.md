---
name: tools-curl
description: >
  Use curl as the ground-truth HTTP client during recon and verification — browser-impersonation
  headers for CDN/WAF 403s, --globoff for bracket params, Windows curl.exe quirks, SPA false-200
  traps. Load when bare tooling gets 403/blocked at a CDN edge, an API needs precise hand-crafted
  requests, or scanner output needs a clean manual repro. Signals: curl, 403 access-policy, CF-RAY,
  Cf-Mitigated, "bad range in position", --globoff, data-center UA blocked.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: info
tools: [curl]
schema_version: 1
---

# curl as ground truth

## When it applies
Any time you need to know what a server *actually* returns — no proxy magic, no scanner
interpretation — or when automated tooling is being blocked at a CDN/WAF edge and you suspect the
request shape, not the content, is the problem. Typical trigger: bare curl or a datacenter UA gets
`403` with a JSON `access-policy` body or a `CF-RAY` header, while the same endpoint works in a real
browser.

## Why it works
Edge protection (Cloudflare & friends) classifies clients by TLS/HTTP fingerprints and headers. A
request carrying a browser User-Agent plus plausible `Origin`/`Referer`/`Sec-Fetch-*` headers often
sails through where a naked `curl` gets challenged — and unlike a scanner, curl shows you the exact
bytes that came back.

## Method
1. **Baseline:** `curl -sS -D - -o /dev/null --max-time 15 https://target/` — `-D -` dumps response
   headers, `-o /dev/null` discards the body, `--max-time` keeps a hung endpoint from stalling you.
2. **On an edge 403, impersonate the browser** before concluding anything:
   ```bash
   curl -sS --max-time 15 \
     -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" \
     -H "Accept: application/json, text/plain, */*" \
     -H "Origin: https://app.example" \
     -H "Referer: https://app.example/" \
     -H "Sec-Fetch-Site: same-site" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Dest: empty" \
     "https://api.example/v1/health"
   ```
   Match `Origin`/`Referer` to the site's real front-end origin — that's usually what the policy
   keys on.
3. **Bracket/query params (prototype-pollution shapes) need `--globoff`:** curl treats `[]` as URL
   globs and dies with `curl: (3) bad range in position N`. Either:
   ```bash
   curl --globoff -sS "https://target/?__proto__%5Btest%5D=polluted"
   curl --globoff -sS -G "https://target/path" --data-urlencode "__proto__[test]=polluted"
   ```
4. **Read the response like a signal, not a verdict:**
   - `403` + JSON access-policy / `CF-RAY` → retry with browser headers (step 2).
   - Still `403` and HTML contains `Cf-Mitigated: challenge` → a real browser or an authenticated
     session is required; **do not** brute-force the edge.
   - SPA route that returns `200` with an identical body size for every path → front-end router,
     not a real API hit — don't log it as an endpoint.
5. **Feed curl requests to other tools:** once a request works, export/replay it exactly — save it
   for `sqlmap -r` (`tools-sqlmap`) or send it to Burp Repeater (`tools-burp-suite`) instead of
   re-deriving it.

## Gotchas
- **`curl -I` sends HEAD** — some apps 405 or behave differently on HEAD; for a real GET with
  headers shown, use `curl -s -o /dev/null -D -`.
- **Windows `curl.exe` vs the alias** — in PowerShell `curl` may be an alias for
  `Invoke-WebRequest`; call `curl.exe` explicitly, and remember `--globoff` for `[]`.
- **Windows `httpx` collision** — the `httpx` command may resolve to the Python httpx library CLI,
  not ProjectDiscovery's httpx; check `httpx -version` before piping recon output into it.
- **A working browser-header bypass is recon, not a bypass finding** — it means the edge admits
  browser-shaped traffic; record it and continue, don't report it.
- **Timeouts are part of the command** — always `--max-time`; a hung curl in an automated loop
  silently stalls the whole pipeline.

## Verify success
You have a reproducible, copy-pasteable request that returns the expected status/body through the
edge, saved verbatim in the engagement notes so any later tool (sqlmap, Repeater, a finding's
repro steps) uses the exact same bytes.

## References
curl manual (`--globoff`, `--data-urlencode`); Cloudflare edge behavior. Pipeline context:
`automation-recon-pipeline`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._

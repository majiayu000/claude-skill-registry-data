---
name: bb-pipeline
description: Full bug-bounty hunting pipeline for authorized programs (Intigriti/HackerOne/Bugcrowd). Use whenever the user wants to hunt bugs, start recon on a bounty target, "go hunt", test an in-scope program, go deeper on a target, or continue a previous hunt — even if they just paste a program description or scope list. Orchestrates passive recon (incl. Wayback CDX and VirusTotal pivots), JS recon, browser-pass for WAF-protected apps, authenticated endpoint testing, IDOR matrices, escalation with real-bug precedent, and reporting.
---

# Bug Bounty Pipeline

Run authorized-target hunting as a disciplined pipeline. Authorization context must exist (a bounty program with published scope). If the user names no program and no scope, ask for the program page/scope before any active work.

## Prime directives (read first)

1. **Scope is law.** Classify every host against the program's scope list before the first request. Out-of-scope hosts get logged in `recon/subdomains/out_of_scope_subs.txt` and are never touched — not even a HEAD request. Wildcards in scope (e.g. `*.cloud.target.com`) are in scope; similar-looking domains (`target.com` vs `target.net`) are not.
2. **Audit everything.** Create a workspace `recon/` with `audit.log`. Append one timestamped line per action batch: `date -u +%FT%TZ [PHASE] what was done`. Reports reference evidence files, never memory.
3. **Program rules beat thoroughness.** Read the program's rules: required headers (e.g. Intigriti requires `X-Intigriti: <username>` on every request), rate limits (default assumption ≤5 req/s), forbidden endpoints, known-issues/dupes list. If the user hasn't provided required identifiers, keep volume at manual pace (single-digit requests per endpoint, ≥1.2s apart) and tell them what's blocked on compliance.
4. **Evidence-based over brute force.** Blind path guessing wastes budget and trips WAFs. Build every wordlist from JS bundles, wayback CDX, and observed traffic. Blind fuzz only after evidence-based paths are exhausted, only if the user explicitly demands it, and then throttled with the required headers.
5. **Honest negatives.** A tested-and-rejected path is progress. Record it with the server's own error string as evidence (`403 "Cart unit does not belong to the current cart"` is proof of a working authz check). Never present an unverified finding as a bug.
6. **Rounds, not one pass.** If round 1 finds nothing, the answer is deeper recon (new sources, new pivots), not the same probes harder. Each round must add a source: wayback → VT pivots → vhost brute → JS deep-dive → authenticated.

## Pipeline phases

Run in order. Skip only phases the user explicitly excludes.

### Phase 0 — Workspace & scope
- `mkdir -p recon/{subdomains,js,ips,findings}`; start `audit.log`.
- Parse the program scope into: in-scope host patterns, out-of-scope patterns, known-issues (do not report), forbidden actions.
- Ask for (and record) researcher identifier for mandatory headers if the program requires one.

### Phase 1 — Passive subdomain recon (multi-source, escalate per round)
Use `scripts/passive_recon.sh <domain>` (bundled) — 8 passive sources in parallel: certspotter, crt.name, rapiddns, Wayback CDX (root + interesting wildcards), urlscan, ctl.shodan. Then:
- Dedupe + classify: `in_scope_subs.txt` / `out_of_scope_subs.txt`.
- DNS resolve; note non-CDN IPs (different infra = interesting).
- **Wayback CDX per interesting zone**: `web.archive.org/cdx/search/cdx?url=*.<host>/*&collapse=urlkey&output=text&fl=original&limit=15000` — yields historical hostnames + endpoint dictionaries + old params. Diff found hosts against current recon: everything new gets DNS + fingerprint. Old PHP-era endpoints (loginProcess.php, admin.php) prove nothing — verify live before caring.
- **VirusTotal pivots** (v2 API, ~4 req/min — pace ≥16s):
  - `vtapi/v2/ip-address/report?ip=<IP>` on the target's IPs — including **RFC1918 internal IPs** from passive DNS. Internal IPs routinely leak sibling hostnames via `resolutions` and `detected_urls` (one 10.x query once returned 350+ hostnames + forgotten vhosts).
  - `vtapi/v2/domain/report?domain=<host>` — `detected_urls` shows archived parameterized endpoints (tokens, IDs in query strings) and `domain_siblings`.
- **Wildcard-DNS zones**: if `*.foo.target.com` answers the same IP for any name, DNS is useless for discovery — brute **vhosts** by Host header instead and diff response signatures (a wildcard zone hid a live API behind `test.`/`demo.` labels). Extract the TLS cert SANs (`openssl s_client` + `x509 -text`) — wildcard certs confirm nothing, SANs with real names are leads.
- Fingerprint everything alive (status, server, title, redirect, first bytes) and sort: login-gated / IAP-gated / open apps / internal-only (10.x answering public DNS = topology leak, Low).

### Phase 2 — JS recon
Hand every JS bundle URL found in HTML/manifests/history/**wayback** to the **js-recon** skill (its `scripts/mine_js.py` does download + extraction in one pass). Deliverables: API path dictionary, GraphQL operation list, secret scan, internal-host inventory, microfrontend maps, per-environment config maps (prod/staging/QA URL sets leak the whole topology).

### Phase 2.5 — Browser pass (WAF-protected frontends)
When scripts get Cloudflare-challenged (403 "Just a moment"/"Attention Required") but the app matters:
- Launch Edge/Chrome with `--remote-debugging-port=9222 --user-data-dir=<fresh>`; drive it over the CDP websocket (`websocket.create_connection(ws_url, suppress_origin=True)` — required to pass the 403 origin check).
- **Timer throttling trap**: an occluded/minimized window freezes `setTimeout`, so async `Runtime.evaluate` hangs forever. Use sync evaluates + Python-side sleeps, or verify with a microtask test first.
- `Page.reload` can trigger the CF interstitial; in-page `location.reload()` usually passes it.
- Hook `XMLHttpRequest.prototype` (axios apps) AND `fetch` in-page to capture method/URL/headers/body + cloned responses — this recovers the real API contract behind any SPA.
- Synthetic `element.click()` works for most controls; real clicks need `Input.dispatchMouseEvent` at viewport coordinates from a **fresh** `getBoundingClientRect` in the same evaluate.

### Phase 3 — Authenticated testing
Real bug classes live behind login. Get sessions via the user's own accounts, in preference order:
1. **Cookie handoff**: user pastes `Cookie:` headers (Cookie-Editor export) per domain per account, labeled acct1/acct2.
2. **Burp ingestion**: user signs up through Burp, then either (a) enable the Burp REST API (`127.0.0.1:1337`, `/v0.1/proxy/history`) and hand me the key, or (b) "Save items" from HTTP history into the workspace — I parse sessions from the file.
3. **CDP login**: I drive the browser through the login flow myself (works for password forms; NOT for email-OTP flows where the code goes to the user's inbox — for those, the user must fetch the OTP or hand off the post-login cookies).
4. "Copy as cURL" blocks from DevTools — one per account.
Then: parse into jars; **identify each session first** via the app's session-status endpoint (`{"loggedIn":true}` or identity object) before any testing. Dead jar? Say so plainly and ask for a fresh paste. Never reuse a jar that failed identification.

### Phase 4 — IDOR/BOLA matrix
Use the **idor-runner** skill. Its script enforces the discipline that matters: positive control (owner succeeds) BEFORE cross-account attempts, mutation reverts, and JSON evidence logs. Report a negative only when the positive control succeeded or the server returned an explicit ownership error.

### Phase 5 — Escalation & chains (with real-bug precedent)
For each finding, try to chain to full impact (IDOR → PII exfil on own accounts; info leak → account enumeration → verify it's not on the known-issues list). Then **calibrate against the bb-disclosures corpus** (11,338 real paid reports):
- `python C:/Users/Admin/.agents/skills/bb-disclosures/scripts/query.py --q "<pattern>" --min-bounty 1000` — what did similar bugs pay, and what element did the expensive ones have that yours lacks? Close that delta or temper the claim.
- Re-check every candidate against the program's out-of-scope list before writing it up — most "bugs" on real programs are pre-declared known issues (redirects, missing headers, enumeration, rate limits).

### Phase 6 — Report
Use the **bb-report** skill. One `recon/findings/report.md`: every bug with Title/Summary/PoC/Impact/Remediation/CVSS, a TESTED-NEGATIVE section, and the artifact index. Update it incrementally every session, not at the end.

## Bug-class routing (use the matching skill per surface)

| Surface / user says | Skill |
|---|---|
| IDOR, BOLA, access control, auth bypass, JWT | **bb-authz** |
| Business logic, price/coupon/checkout/refund flows | **bb-bizlogic** |
| Race conditions, double redeem, concurrency | **bb-race** |
| SSRF, URL fetch, webhooks, cloud metadata | **bb-ssrf** |
| XSS, DOM sinks, postMessage | **bb-xss** (deep DOM source→sink work: **bb-domxss**) |
| Pre-hunt: understand/map the whole target from passive sources first | **target-intelligence** |
| OAuth/SSO login flows, redirect_uri, social login, MCP | **bb-oauth** |
| File uploads, public buckets, polyglots, serve-side rendering | **bb-upload** |
| CSRF, content-type defenses, state-changing actions cross-site | **bb-csrf** |
| GraphQL API | **bb-graphql** |
| RCE, command injection, SSTI, deserialization, upload-to-RCE | **bb-rce** |
| PII exposure, data leaks, oversharing, GDPR impact | **bb-pii** |
| SQL / NoSQL injection | **bb-sqli** |
| JS bundle mining | **js-recon** |
| Deep JS audit (10-section attack-surface + vuln mapping) | **js-audit** |
| Tech fingerprint → known-bug/CVE hunt per stack | **footprinting** |
| Escalate/chain a finding, "worth reporting?" | **bb-chains** |
| Real-bug precedent, bounty calibration, idea generation | **bb-disclosures** |
| Cross-account test execution | **idor-runner** |
| Write/format findings | **bb-report** |

## Session continuity
If a `recon/` workspace exists for the target, read `audit.log` tail + `findings/report.md` first and continue from the recorded state instead of re-running recon. Multi-program hunts: one directory per program under a shared `hunt/` root with a shared `audit.log`.

## Campaign playbooks (read before long hunts)
`references/hunt-playbooks.md` — program-selection discipline, narrow-vs-wide recon switching, asset discovery beyond crt.sh CN (Organization-field certs, ASN pivots, corporate-blog mining), parameter bruteforcing (x8/GAP), session-upgrade flow bugs, and hours-based goal setting. Distilled from three $7k–$20k documented campaigns.

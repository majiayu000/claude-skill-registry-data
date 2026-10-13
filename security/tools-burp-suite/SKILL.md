---
name: tools-burp-suite
description: >
  Drive Burp Suite for web/API testing — proxy history triage, Repeater, Intruder enumeration,
  Collaborator OOB, active scanning — manually or agent-driven through a Burp MCP extension on
  127.0.0.1:9876. Load for any HTTP-target deep testing: "burp", proxy history analysis, repeater
  replay, intruder brute/enum, collaborator payloads, DAST scan, CSRF PoC generation, token
  randomness analysis. Signals: port 8080 proxy, port 9876 MCP, burpsuite, BApp MCP Server.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
tools: [burp-suite, burp-mcp, collaborator, intruder, repeater]
schema_version: 1
---

# Burp Suite deep testing (GUI + MCP)

## When it applies
You're web/API testing an in-scope target (`tradecraft-scope-roe`; load `web-testing-checklist` or
`api-testing-checklist` as the coverage map) and need the core manual-testing platform: intercept,
modify/replay, targeted enumeration, OOB detection, or an active scan. Burp is name-dropped across
many skills as "send it to Repeater" — this one is how to *operate* it, including agent-driven
operation through an MCP extension so the AI can read proxy history and fire Intruder itself.

## Why it works
Every request the browser makes flows through Burp's proxy into a searchable history; Repeater gives
byte-exact replay, Intruder turns one request into a thousand enumerated variants, Collaborator
provides OOB callbacks that prove blind bugs, and the MCP extensions expose all of it as tools — so
an agent can triage hundreds of captured requests and only escalate the interesting ones.

## Method
1. **Set up agent access (MCP).** Burp must be running with an MCP extension loaded:
   - *Official*: Extensions → BApp Store → "MCP Server" (PortSwigger) → Enable (~20 core tools).
   - *Community full-coverage extensions* expose ~78 tools (full inventory:
     [`cheatsheet.md`](cheatsheet.md)) via an HTTP API on `127.0.0.1:9876` plus a stdio bridge for
     MCP clients. Health check: `curl http://127.0.0.1:9876/health`.
   - Never load cracked/repackaged Burp builds — official PortSwigger releases only (Community is
     fine but rate-limits Intruder hard).
2. **Triage proxy history first.** Browse the app through the proxy (login, exercise every feature),
   then work the history: filter by host/path, pull full request/response detail on candidates,
   regex-search history for secrets (`Authorization: Bearer`, `api_key`, JWT shapes). This turns
     "click around" into a coverage map for the checklist skills.
3. **Verify by replay (Repeater).** Modify one thing at a time and diff responses — auth headers
   removed, HTTP method swapped (GET→PUT/DELETE), IDs incremented for `web-idor`, extra JSON fields
   for `api-mass-assignment`, `X-Forwarded-For`/`X-Original-URL` for 403 bypasses, path case/traversal
   variants (`/Admin`→`/admin`, `..;/`).
4. **Enumerate with Intruder.** Numeric ranges (OTP/ID enum: `code=@@` from 000000–999999),
   wordlist attacks, cluster-bomb for multi-param cartesian products. Identify hits by
   *response-length difference* (e.g. `success when length ≠ <error length>`) or response time for
   blind injections. On Community, keep threads low — it throttles to ~1 req/s.
5. **Prove blind bugs with Collaborator.** Generate a payload, inject it into URL/webhook/redirect
   params, poll for DNS/HTTP interactions after a few seconds — a callback confirms SSRF/XXE/blind
   injection that no response diff ever would (`web-ssrf`).
6. **Active scan + targeted fuzzing.** Add the target to scope, crawl, then active-scan key requests;
   treat scanner output as *candidates* — every issue gets a manual Repeater confirmation
   (`reporting-triage-validation`) before it becomes a finding.
7. **Automate repetitive transforms** with HTTP handlers / match-and-replace: auto-attach auth
   headers, re-sign requests after reverse-engineering a client signature scheme
   (`web-client-side-signing-bypass`), or route through an upstream proxy pool for IP rotation.

## Gotchas
- **Extension won't load** — community MCP extensions are typically compiled for JDK 21+; check
  Burp's Java version first. Port 9876 already bound = another extension instance running.
- **Community Edition** throttles Intruder and has no active scanner — plan around it (small
  targeted lists, manual Repeater loops) or use Pro.
- **High thread counts DoS the target and trip WAFs** — cap threads, respect `roe.md` rate limits,
  and prefer `success_length_not`-style discrimination over reading every response.
- **History ≠ evidence** — a suspicious request in proxy history is a lead, not a finding; the
  finding is the Repeater replay that proves impact.
- **Encrypted/signed params** — don't fuzz ciphertext; extract or re-implement the transform first,
  then register it as an auto-handler so Intruder works on plaintext.
- **Scope discipline** — Burp will happily scan whatever you crawl; keep `add_to_scope` aligned with
  `scope.txt` and never point the active scanner out of scope.

## Verify success
Each candidate from history/scanner/Intruder either reproduces in Repeater with a visible impact
(diff, data, OOB callback) or is ruled out with the variation matrix worked (per House rules).
Confirmed issues are written up per the engagement's findings format with the exact replayed request
as proof.

## References
PortSwigger Web Security Academy & Burp docs; BApp Store "MCP Server". Tool-by-tool inventory and
per-scenario workflows: [`cheatsheet.md`](cheatsheet.md).

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._

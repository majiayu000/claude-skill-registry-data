---
name: bb-chains
description: Escalate and chain bug bounty findings to full impact, run the 8-question validation gate before reporting, calibrate against real paid disclosures, and kill weak findings fast with the always-rejected list. Use whenever the user says "escalate this", "chain it", "is this worth reporting", "this is only P4, make it bigger", "full impact", has a weak finding to strengthen, or is deciding whether to submit.
---

# Chains, Escalation & The Validation Gate

A finding's bounty is set by the END of the chain, not the start. Two jobs here: build the chain upward, and kill weak findings before they burn triage goodwill.

## The chaining matrix (A → B → C)

| Bug A (weak alone) | Hunt B | Escalates to C |
|---|---|---|
| IDOR read | PUT/PATCH/DELETE on same object | Full account/object manipulation |
| IDOR on address/invoice | use that ID in order/refund flow | Money impact |
| SSRF (internal hit) | cloud metadata endpoint | IAM creds → infra access (report, don't use) |
| XSS (stored) | non-HttpOnly session cookie / admin viewer | Session hijack → ATO |
| Open redirect | OAuth `redirect_uri` that accepts your domain | Auth-code theft → ATO |
| Host header injection | password-reset email flow | Reset poisoning → ATO ($35k precedent: interaction-free reset ATO) |
| CORS misconfig | credentialed endpoint (`Access-Control-Allow-Credentials: true` + reflected origin) | Cross-origin data theft |
| No rate limit on OTP/verify | OTP brute at realistic rates (respect rules!) | ATO |
| Info leak (internal host/ID) | SSRF or IDOR using the leaked identifier | Chain enabler |
| Leaked secret in bundle/repo | what does the credential REACH (registry, VPN, API write) | $5k–$50k (top corpus payout: GitHub token exposure) |
| Exposed control-plane UI (Argo CD, k8s API, mgmt console) | CSRF on its session, or credentialed API access | Cluster compromise ($4.6k Argo CSRF precedent; $25k exposed k8s API) |
| GraphQL introspection | field-level BOLA | Mass PII exfil |
| Self-XSS | login CSRF / forced-save | Stored XSS on victim |
| Unbound capability URL (unguessable-ID object) | where the ID leaks (logs, shares, referrer, support) | Permanent third-party read/write of live order |

Escalation discipline: each hop must be demonstrated, not assumed. "XSS could steal cookies" requires the cookie actually being non-HttpOnly.

## The 8-question gate (ALL yes, or don't report)

1. Working PoC I can run right now?
2. Affects a real user who did nothing unusual?
3. Impact is concrete (money / PII / ATO / RCE / integrity)?
4. Asset in program scope (rechecked against the current scope list)?
5. Dup check done (program's known-issues/disclosed reports)?
6. Not on the always-rejected list (below)?
7. Would a tired triager on Friday 5pm say "yes, real bug"?
8. **Precedent check**: does a similar bug appear in the bb-disclosures corpus with a real payout (`query.py --q "<pattern>" --min-bounty 500`)? If yes — does yours have the element that carried theirs (interaction-free, mass-scale, credentials-with-reach, control-plane state change)? If no — treat as P4 until chained.

## Always-rejected (never submit without a chain)
Missing CSP/HSTS/headers, SPF/DKARC/DMARC, GraphQL introspection alone, version disclosure without a working exploit, clickjacking on non-sensitive pages, CSV injection, CORS wildcard without credentialed exfil, logout CSRF, self-XSS, open redirect alone, SSRF DNS-pingback only, rate-limit absence on non-critical forms, cookie flags alone, internal IP disclosure alone, mixed content, weak TLS ciphers, username/email enumeration, verbose errors without sensitive data, exposed login page of an internal tool with anonymous auth verified disabled.

## Conditionally valid (only WITH the chain proven)
open redirect→OAuth theft; CORS→credentialed exfil; no-rate-limit→OTP brute; SSRF-DNS→internal proof; host-header→reset poisoning; self-XSS→login-CSRF delivery; internal-IP disclosure→used as SSRF/IDOR enabler; control-plane UI→CSRF or credentialed action.

## Escalation work order (when stuck at P4)
1. Re-read the corpus precedents for the class (`query.py --class <class> --min-bounty 3000 -n 10`) — list what the expensive ones had.
2. Attack the missing element directly: no victim interaction? find an auto-executing context (email viewer, webhook, import). Not mass? find the enumeration/fabrication path. No credentials? hunt tokens in bundles/repos/archives instead of hostnames.
3. Change one variable at a time on bypasses (encoding, case, path normalization, HTTP version, method) — log each attempt in audit.log.
4. Check the program's known-issues list twice: many "found it!" moments are pre-declared dupes.
5. If it can't be proven end-to-end, it goes in the report's OPEN SURFACES section as a lead — not as a finding.

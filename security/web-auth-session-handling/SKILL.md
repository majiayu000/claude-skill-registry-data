---
name: web-auth-session-handling
description: >
  Legitimately acquire and KEEP an authenticated session (through MFA/OTP) so you can test the
  post-auth attack surface, and hand that session to your tools without leaking secrets. Load when
  the high-value classes (IDOR/BOLA, mass assignment, injection on real data APIs) are blocked
  behind login/SMS-OTP/TOTP, when tokens keep expiring mid-test, or when Burp/Playwright keep
  logging you out. Distinct from attacking auth — this one authenticates and reuses the session.
domain: web
type: methodology
stability: learning
modes: [pentest, bugbounty]
severity: info
owasp: [A01:2021-Broken-Access-Control]
tools: [burp, playwright, caido, ffuf]
schema_version: 1
---

# Authenticated session handling

## When it applies
The interesting bugs live *after* login — cross-tenant IDOR/BOLA, mass assignment, injection on
the real data APIs — but the run keeps collapsing to pre-auth findings because login is gated by
MFA/OTP, or the token expires and every automated request 401s halfway through. This skill is the
setup step that makes authenticated testing actually work. It does **not** attack the auth
mechanism (`web-oauth`, `web-auth-jwt`, `api-auth-attacks` do that) — it obtains one legitimate
session and keeps it usable.

## Why it works
Post-auth coverage silently disappears when tooling can't hold a session: the scanner logs out,
the token lapses, or MFA can't be satisfied autonomously. Capturing the session as a *reusable
artifact* — the cookie/localStorage state for browser-driven testing and the raw bearer token for
direct API replay — decouples "log in once" from "test a thousand requests," so the whole
authenticated surface stays reachable for the life of the token.

## Method
1. **Get a real test account, in writing.** For a pentest, the client provides it; for bounty,
   use an account you own (register two: attacker + victim, for IDOR diffing). Record it by
   reference in `scope.txt` — never paste live credentials into notes or a prompt.
2. **Handle the MFA/OTP gate** by the least-privileged means available:
   - **TOTP seed shared** → generate the current code from the Base32 seed (`oathtool --totp -b <SEED>`)
     and submit it. Fully repeatable.
   - **Operator-relayed OTP** → drive login to the OTP prompt, a human supplies the code once, continue.
   - **Out-of-band / human-in-the-loop** → persist the pre-OTP browser context, pause, let the
     operator complete the challenge, then resume and capture state.
3. **Capture the session as artifacts:**
   - Browser state — Playwright `storageState.json` (`context.storage_state(path=...)`) holds cookies + localStorage.
   - API replay — the raw access/ID token plus its `expires_at`.
4. **Feed it to your tools:**
   - **Burp/Caido** — a session-handling rule + macro that re-auths on a logged-out signature
     (a redirect to `/login`, a 401, a specific body), so long scans don't drop the session.
   - **Playwright** — launch with `storage_state="storageState.json"`.
   - **API fuzzers** (`ffuf`, `api-fuzzing`) — inject the bearer as a header.
5. **Refresh, don't re-login.** Record `expires_at`; when a refresh token exists, refresh; only
   re-run the full login when it doesn't. A wave of sudden 401s means the token lapsed — refresh
   before you trust "not vulnerable."
6. **Diff two sessions for access control.** Hold A's and B's artifacts side by side and replay
   each other's object references (`web-idor`, `api-bola`) — the core authenticated test.

## Gotchas
- **Present creds ≠ working creds.** Before spawning a big authenticated scan, verify the session
  actually reaches a known post-auth endpoint (200 with your data) — otherwise you "test" a
  logged-out surface and report false negatives.
- **Never inline the token.** Pass sessions by file reference; keep secrets out of prompts, notes,
  and any committed file. The `engagements/` tree is git-ignored — keep them there.
- **If a realm truly can't be authenticated** (no test account, no OTP relay), say so honestly —
  record the post-auth surface as *deferred/untested*, don't fake an N/A or silently skip it.
- **Scope the session's blast radius** — a test account with real admin rights can do real damage;
  prefer least-privilege test roles, and treat destructive actions per RoE.

## Verify success
A request built entirely from your captured artifact (no live browser) returns a known post-auth
response with your account's data — and a two-session IDOR probe runs cleanly against it.

## References
Playwright authentication/storageState docs; Burp/Caido session-handling rules; RFC 6238 (TOTP).

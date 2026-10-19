---
name: web-race-conditions
description: >
  Exploit race conditions / TOCTOU — fire concurrent requests to break single-use limits. Load
  on "limit-once" actions: coupon/gift-card redemption, withdrawals, votes, invites, MFA/OTP
  attempts, balance changes. Signals: check-then-act on shared state, per-user quotas, "already used".
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp: [A04:2021-Insecure-Design]
cwe: [CWE-362]
tools: [burp, turbo-intruder]
schema_version: 1
---

# Race conditions (TOCTOU / limit-overrun)

## When it applies
An action is meant to happen once (or N times) and the server checks a condition, then acts, on
shared state — without atomicity. Concurrent requests slip between check and update.

## Why it works
Between "check if allowed" and "record that it happened" there's a window. Fire many requests in
that window and several pass the check before any updates the state — so a one-time coupon
redeems 10×, a balance is spent twice, a limit is overrun.

## Method
1. **Pick a limited action** with observable state (balance, redeemed flag, count).
2. **Send a burst in parallel** aligned to hit the window together: Burp **Turbo Intruder**
   (single-packet attack for HTTP/2, or last-byte sync for HTTP/1) — the point is simultaneity,
   not volume.
3. **Measure the overrun**: did the action succeed more times than allowed (2 redemptions, double credit)?
4. **Variants**: multi-endpoint races (state set by A, consumed by B), and MFA/OTP brute windows.

## Gotchas
- Sequential fast requests aren't a race — you need true concurrency (single-packet / synced send).
- Effect can be small (2× not ∞) but still valid; quantify the actual overrun.
- Idempotency keys / DB locks defeat it — a single success may just be correct behaviour.

## Verify success
The limited action occurs more times than the rules allow (e.g. one coupon applied twice,
balance double-spent), reproduced with the concurrent PoC.

## References
PortSwigger race-condition labs; James Kettle "Smashing the state machine"; Turbo Intruder.

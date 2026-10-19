---
name: bb-race
description: Hunt race conditions and TOCTOU bugs — coupon/voucher double redemption, double payouts and refunds, concurrent balance manipulation, confirmation-state bypasses (partner/email/order confirm), duplicate actions, limit bypass via parallel requests. Use whenever the user mentions race conditions, TOCTOU, double spend, concurrent requests, "redeem twice", limit bypass, or wants to test endpoints that check-then-act.
---

# Race Condition Hunter

Race bugs live where the server **checks then acts** in two steps without locking: `if balance >= cost` … `balance -= cost`. Fire the same request N times simultaneously so the check passes N times before any act lands.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$10,000** **Double Payout via PayPal** — the payout endpoint raced; one payment, two credits.
- **$15,250** **TOCTOU on partner email confirmation** → take over any store — a state-confirmation flow raced/bypassed, not a money counter.
- Corpus pattern: paid races sit on **money-out and entitlement-grant** endpoints (payout, redeem, confirm, grant), never on views.
Delta lesson: aim the burst at `payout`, `withdraw`, `redeem`, `confirm`, `claim`, `grant` — and at **confirmation state machines** (confirm-then-use across two objects), not just counters.

## Where races live (target list)
- Redeem: coupons, vouchers, gift cards, promo codes
- Money-out: withdraw, payout, transfer, tip, cashback claim, refund posting
- One-time actions: vote, claim bonus, spin/raffle, one-per-user signup credit
- Limits: rate/quota counters ("first 100 users"), stock reservation
- Email/OTP verification, referral credit posting
- **Confirmation flows**: confirm ownership/partnership of object A while acting on object B; confirm an already-confirmed state twice

Find the candidates in JS (js-recon): verbs like redeem, claim, withdraw, apply, transfer, confirm + state fields.

## Methodology
1. **Baseline**: single request, record response + state after (balance/coupon status). You must know the serial behavior first.
2. **Capture the exact request** (from proxy/cURL) with its CSRF tokens if any — replaying must be valid.
3. **Burst**: send N identical requests as simultaneously as possible:
   - `seq 20 | xargs -P 20 -I{} curl -s -X POST ... &` (simplest), or
   - Python + threads/httpx with a barrier, or single TCP connection pipelining when the stack allows.
   - Higher N helps but DoS is forbidden — cap at ~20-30 parallel, once or twice, never sustained.
4. **Measure state after**: coupon redeemed ×N? balance debited once but credit ×N? One payment → two shipments/payouts?

## Signals
- Divergent responses in one burst: one 200 + rest 409/429 → single-use check raced (the 200s count).
- Post-state ≠ expected single-action state (credits = 2×, stock = -1).
- Idempotency keys: if the API has an `Idempotency-Key` header, REUSE the same key across the burst — that's often the intended dedup, and racing different keys may bypass it.

## Constraints
- Own accounts, own coupons, own money — no third-party impact.
- Never sustain load; no "real" DoS. Program rules on automated scanning still apply (throttle between bursts).
- Payment-adjacent races (double refund, double payout): stop at proving the state delta; don't cash out.

## Evidence format
1. Serial baseline (one request → one effect).
2. Burst script + parameters.
3. After-state proof (two redemptions / double credit) — response bodies or account state screenshot/JSON diff.
Impact = the multiplier: "single coupon yields N redemptions", "one payout credited twice".

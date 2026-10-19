---
name: bb-bizlogic
description: Hunt business logic flaws in e-commerce and SaaS apps — price/quantity tampering, coupon and referral abuse, checkout workflow bypass, currency tricks, mass assignment on money fields, TOCTOU on confirmation/payout state, and money-out endpoint races. Use whenever the user says "business logic", mentions testing a shop/checkout/cart/coupon/refund/payout flow, wants "bugs most hackers miss", or asks to understand an app's money flows for bug hunting.
---

# Business Logic Hunter

Business logic bugs pay more per finding because scanners can't find them — they require understanding what the app *should* do with money, quotas, and state. Invest the first phase in comprehension, not payloads.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$15,250** Bypass partner email confirmation → **take over any store** given an employee email — TOCTOU on a confirmation state; email-confirmation flows are money.
- **$12,500** Internal attachments exportable via "Export as .zip" — export features skipping entitlement checks.
- **$12,000** Run pipeline jobs **as arbitrary user** — job/identity binding flaw.
- **$10,000** **Double Payout via PayPal** — payout endpoint raced (pairs with bb-race).
Delta lesson: the paid logic bugs cluster on **money-out and entitlement-grant** endpoints (payout, redeem, confirm, grant, export), not on browse/search. Map those first.

## Phase 1 — Model the business (mandatory)
Answer in writing before any payload:
1. **Money flows**: browse → cart → checkout → payment → fulfillment → refund/payout. Which endpoint applies prices, discounts, taxes? Client-sent or server-derived?
2. **State machines**: order statuses, coupon states, wallet/refund balances, trial→paid, unconfirmed→confirmed (partner/email/order). Which transitions does the UI enforce vs the API enforce?
3. **Trust boundaries**: every field the client sends that influences money or entitlement (`price`, `amount`, `quantity`, `currency`, `discount`, `total`, `is_gift`, `role`, `plan_id`).
4. **Quotas and one-time rules**: first-purchase bonuses, referral credits, one-per-customer coupons, free trials, per-store/partner confirmations.

Evidence source: JS bundles (js-recon) reveal the checkout API contract — including which quantity/price shapes the client is *allowed* to send (integer vs `{change,total}` objects); proxy history shows what the client actually sends.

## Phase 2 — The checklist (e-commerce oriented)

**Cart & checkout**
- Negative / zero / fractional quantities; quantity above stock; quantity change AFTER price snapshot.
- Price/total fields sent by client — replay add-to-cart with modified `price`/`unitPrice`/`amount` fields; compare server total. (Expect server-recompute on mature programs — record the negative.)
- Currency mismatch: pick item in EUR, pay request in a weaker/other currency code.
- Skip steps: hit the final confirm/buy endpoint directly with a crafted state; reorder with stale token; use `replace_cart`-style flags.
- Race the price snapshot: change cart between quote and charge.
- **Offer/discount state tampering**: item-level offers applied N times? discount clamped server-side? (Watch `CategoryOffers`/`Adjustments` arrays in responses — re-applying or stacking them is the modern coupon bug.)

**Coupons / promo / gift cards**
- Reuse: same code N times (see bb-race — single-request burst).
- Cross-account: apply other OWN account's coupon ID; stack incompatible discounts.
- Negative discount; discount > price; refund keeping the discount.
- Gift card: redeem same card on two own accounts concurrently.

**Refunds / payouts / wallet / credits**
- Refund more than paid (partial refund × N, or amount field tamper); refund then cancel; double refund via replay; **double payout** via concurrent payout requests.
- Referral self-abuse: own two accounts, refer yourself.
- Withdrawal/credit races. State the multiplier in impact ("one refund credited twice").

**Signup / trial / entitlement / partner flows**
- Mass assignment: `{"plan":"premium","role":"admin","trial_extended":true}` on profile/registration update.
- Trial reset via delete-account → re-register with same email.
- Integer overflow on quantities/credits (2147483647 + 1).
- **Email/partner confirmation bypass**: request confirmation for object A, confirm against object B; confirm an already-confirmed state twice; TOCTOU between check and state-flip (the $15k store-takeover shape).

## Phase 3 — Prove safely
- Own accounts only; never complete a real payment to prove a point unless the user explicitly says to buy.
- Capture before/after JSON (cart, order, balance) as evidence — the diff IS the PoC.
- Revert everything you can (cancel orders, remove coupons, empty baskets).
- The killer evidence format: two cURLs — (1) the crafted request, (2) the server response showing the wrong total/balance/refund.

## Verdict rules
- A tampered request the server *rejects* or *recomputes correctly* → TESTED-NEGATIVE, log it (e.g. `MaximumBasketSizeReached`, price fields silently ignored).
- "Would have worked" without the server's confirming response → not a finding.
- Impact = money language: "attacker obtains X EUR of goods for Y EUR", "N× refund of one payment".
- Calibrate against bb-disclosures (`--class "Business logic" --min-bounty 2000`) before setting severity.

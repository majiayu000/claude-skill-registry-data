---
name: productized-service
description: Productized service designer — turn custom work into fixed-scope, repeatable offers with landing, auto-sell, delivery, and referral.
personas:
  - FREELANCE
  - GROWTH
triggers:
  - productize
  - خدمة جاهزة
  - packaged service
  - productized service
  - خدمة معلبة
tech_stack:
  - invoiceninja/invoiceninja
  - lago/getlago
  - plausible/analytics
---
[SKILL] productized-service
[OBJ] Convert a custom freelance service into a productized offer — fixed price, fixed scope, repeatable delivery — to escape time-for-money and scale.

[RULES]
1. [REQ] Productize formula: one clear outcome + fixed scope + fixed price + fixed turnaround. No "it depends" in the offer.
2. [REQ] SOP build: document every step (intake→delivery→QA→handoff). Reusable checklist; enables delegation/delivery consistency.
3. [REQ] Landing page: one offer, one CTA, price visible, scope listed, FAQ, social proof. Build per `cro-optimization` + `seo-lord` (speed/CWV).
4. [CMD] Context7 IDs: `invoiceninja/invoiceninja` (recurring invoice), `lago/getlago` (subscription/plan), `plausible/analytics` (conversion).
5. [REQ] Auto-sell: payment (deposit/full) via `invoice-manager` on checkout; kickoff auto-triggers `client-onboarding`. No manual quoting per sale.
6. [REQ] Pricing: use `pricing-strategy` to set the fixed price above custom-equivalent hourly rate; offer 1-2 tiers (e.g., Standard/Pro).
7. [REQ] Delivery + referral: smooth delivery → auto-ask review + referral (link `client-retention`/`affiliate-manager`). Compound via word of mouth.
8. [REQ] Arabic/RTL: Arabic productized offers need RTL landing, SAR/AED/EGP pricing, Arabic SOP; mirror `arabic-freelance`.
9. [REQ] Measurement: orders, delivery time, refund rate, repeat%. Optimize weakest node via `cro-optimization`.
10. [REQ] Approval gate: publishing the offer/charging requires explicit user yes.

[PROHIBIT]
1. No productized offer without a written SOP.
2. No scope creep beyond the fixed offer.
3. No hidden or changing price at checkout.
4. No Arabic offer without RTL + local currency.

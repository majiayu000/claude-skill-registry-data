---
name: affiliate-manager
description: Affiliate manager — track links, commissions, payouts, and partner performance. Free-first self-hosted or platform-native programs.
personas:
  - MARKETING
triggers:
  - affiliate
  - عمولة
  - كسب من الروابط
  - affiliate manager
  - شراكة بالعمولة
tech_stack:
  - lago/getlago
  - twentyhq/twenty
  - plausible/analytics
---
[SKILL] affiliate-manager
[OBJ] Run an affiliate/referral program end-to-end — recruits, tracked links, commission rules, payouts, and partner performance — to grow revenue through third parties.

[RULES]
1. [REQ] Program design: commission model (CPA/rev-share/tiered), cookie window, payout threshold,accepted-promo rules. Document before recruiting.
2. [REQ] Link tracking: unique affiliate IDs + UTM; attribute conversions via `marketing-analytics` (last-click or custom). No manual credit without a link.
3. [CMD] Context7 IDs: `lago/getlago` (metered/billing engine for payouts), `twentyhq/twenty` (partner objects), `plausible/analytics` (link performance).
4. [REQ] Free-first: self-hosted affiliate via Lago (AGPL) for payouts, or platform-native (ShareASale/Impact) as parity; Twenty for partner CRM.
5. [REQ] Partner enablement: give affiliates copy, creative, and a dashboard. Cross-link `copy-frameworks` for swipe files.
6. [REQ] Fraud rules: detect self-referral, coupon-stacking, fake leads; hold payout 30d for validation. Align with `marketing-compliance`.
7. [REQ] Payouts: automated via Lago meter→invoice; threshold (e.g., $50) before release; tax form (W-8/W-9) collected. Feed `freelance-financials`.
8. [REQ] Arabic/RTL: Arabic-facing affiliates get RTL creative + local payout methods (bank transfer/SAR/AED/EGP); terms in Arabic.
9. [REQ] Performance review: rank affiliates by revenue + EPC (earnings per click); cut underperformers quarterly; double down on top.
10. [REQ] Approval gate: payout runs require explicit user approval (kernel write-gate).

[PROHIBIT]
1. No payout without tracked, validated conversion.
2. No undisclosed affiliate disclosure (FTC/ local law).
3. No payout run without explicit approval.
4. No Arabic terms shipped without RTL + local payout support.

---
name: client-retention
description: Client retention strategist — upsell, cross-sell, recurring check-ins, and referral programs. Grow lifetime value. Do not use for growth loops tasks — use `growth-loops` instead.
personas:
  - FREELANCE
  - SALES
triggers:
  - retention
  - احتفاظ
  - upsell
  - cross-sell
  - client retention
tech_stack:
  - twentyhq/twenty
  - lago/getlago
  - chatwoot/chatwoot
---
[SKILL] client-retention
[OBJ] Maximize client lifetime value — proactive check-ins, timely upsells/cross-sells, and a referral engine that turns happy clients into new business.

[RULES]
1. [REQ] Lifecycle map: post-delivery → 30-day check-in → quarterly review → renewal/upsell → referral ask. Each step scheduled in `lead-generation-crm`.
2. [REQ] Health score: track satisfaction (NPS/CSAT), on-time delivery, repeat engagement. Flag at-risk (<60) for human outreach.
3. [CMD] Context7 IDs: `twentyhq/twenty` (opportunity/renewal), `lago/getlago` (subscription/retainer), `chatwoot/chatwoot` (relationship inbox).
4. [REQ] Upsell triggers: new need detected, scope growth, anniversary. Offer via `pricing-strategy` (retainer/package). Never surprise-price mid-contract.
5. [REQ] Cross-sell: map complementary services (e.g., SEO client → `content-marketing`); one relevant offer per review.
6. [REQ] Referral program: ask at peak satisfaction; give template + incentive (link `affiliate-manager`). Track sources in CRM.
7. [REQ] Free-first: Twenty (AGPL) for accounts, Lago for retainers, Chatwoot (MIT) for touch; paid CS tools only as parity.
8. [REQ] Arabic/RTL: Arabic clients get RTL check-in templates, relationship etiquette per `arabic-freelance`, local holiday awareness.
9. [REQ] Win-back: lapsed clients get a 2-touch reactivation with a relevant offer; respect suppression (see `marketing-compliance`).
10. [REQ] Measurement: retention %, expansion MRR, referral rate, NPS. Feed `marketing-analytics`.

[PROHIBIT]
1. No upsell before value is demonstrated.
2. No excessive/unscheduled check-in spam.
3. No referral request from dissatisfied clients.
4. No Arabic retention message without RTL + etiquette.

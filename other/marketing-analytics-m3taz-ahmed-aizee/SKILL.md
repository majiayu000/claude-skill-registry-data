---
name: marketing-analytics
description: Marketing analytics and attribution architect — GA4, Mixpanel, Plausible, Umami, Matomo. Collect, unify, attribute, and report CAC/LTV/ROAS.
personas:
  - MARKETING
triggers:
  - mixpanel
  - attribution
  - marketing analytics
  - تحليلات تسويق
  - قياس العائد
tech_stack:
  - plausible/analytics
  - umami-software/umami
  - matomo-org/matomo
  - google/ga4

---
[SKILL] marketing-analytics
[OBJ] Measure what marketing actually does — unify channel data, build attribution models, and report the metrics that matter (CAC, LTV, ROAS, payback). Turns raw events into decisions.

[RULES]
1. [REQ] Metric hierarchy: (1) Acquisition (sessions, leads), (2) Conversion (CVR, CAC), (3) Retention (repeat, churn), (4) Economics (LTV, payback, ROAS). Report top-down.
2. [CMD] Context7 IDs: `plausible/analytics` (privacy-first goals/funnels), `umami-software/umami` (MIT event schema), `matomo-org/matomo` (campaign/referrer attribution, official RTL), `google/ga4` (Data API + Measurement Protocol, EU endpoint for GDPR).
3. [REQ] Free-first stack: Plausible (AGPL, self-host) or Umami (MIT) for privacy web analytics; GA4 free for depth; Matomo (GPL) for attribution. Mixpanel free tier for product events.
4. [REQ] Attribution models: implement last-click, first-click, linear, position-based, and data-driven. Default report shows ≥3 models side by side to avoid single-model bias.
5. [REQ] CAC = total acquisition spend / new customers in period. LTV = ARPU × gross margin / churn. Always state the window (e.g., LTV12). Feed to `freelance-financials` for planning.
6. [REQ] Event taxonomy: consistent `event_name` + `source` + `campaign` across tools so `attribution_model` can join. Define once, enforce everywhere.
7. [REQ] RTL/Arabic dashboards: Arabic labels, right-to-left layout, Hijri toggle optional. Matomo has official RTL; mirror Plausible/Umami via CSS dir=rtl.
8. [REQ] Data quality gate: reject reports where ≥30% of conversions are "(direct)/(none)" unexplained; fix tracking before declaring insights.
9. [REQ] Decision output: every analysis ends with 1-3 actions (scale/stop/iterate) tied to a metric movement, not a vanity number.
10. [REQ] Cross-link: funnel drop-off → `cro-optimization`; channel spend → `paid-ads`; lifecycle → `client-retention`.

[PROHIBIT]
1. No sending PII (email/phone) to analytics without consent.
2. No single-model attribution presented as truth.
3. No metric reported without its definition + window.
4. No GA4 EU data routed through non-compliant endpoints.

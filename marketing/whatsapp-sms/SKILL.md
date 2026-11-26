---
name: whatsapp-sms
description: WhatsApp and SMS campaign strategist — opt-in compliant broadcasts, templates, and automation. RTL-aware for Arabic audiences.
personas:
  - MARKETING
  - SALES
triggers:
  - whatsapp sms
  - whatsapp
  - sms
  - broadcast
  - whatsapp marketing
  - رسائل واتساب
  - حملة رسائل
tech_stack:
  - chatwoot/chatwoot
  - twentyhq/twenty
  - plausible/analytics

---
[SKILL] whatsapp-sms
[OBJ] Run high-intent WhatsApp and SMS programs — broadcasts, templates, and 1:1 flows — that respect opt-in and deliver strong ROI in MENA and emerging markets.

[RULES]
1. [REQ] Opt-in first: no message without explicit, documented consent (double opt-in preferred). Align with `marketing-compliance` (GDPR/CAN-SPAM equivalents, TCPA for SMS).
2. [REQ] Template approval: WhatsApp requires pre-approved templates per category (marketing/utility/auth). Draft compliant templates; avoid promotional language in utility.
3. [CMD] Context7 IDs: `chatwoot/chatwoot` (WhatsApp/SM channel, MIT), `twentyhq/twenty` (contact store), `plausible/analytics` (click tracking).
4. [REQ] Free-first: WhatsApp Business API via self-hosted Chatwoot (MIT) or free tier; Twilio free credit as parity; avoid vendor lock-in.
5. [REQ] Segmentation: message by lifecycle stage (lead/customer/lapsed) and language. Never blast the whole list indiscriminately.
6. [REQ] Arabic/RTL: Arabic WhatsApp needs RTL, proper diacritics optional, local sending windows (avoid late night GST), and Arabic opt-out keyword (مسح/إلغاء).
7. [REQ] Frequency cap: max 2-4 msgs/week per user; honor immediate stop. Reduce churn via `client-retention`.
8. [REQ] Measurement: delivery, read, reply, CTR, conversion. Feed `marketing-analytics`.
9. [REQ] Automation: opt-in→welcome→sequence via `marketing-automation`; human handoff for sales intent to `b2b-cold-outreach`.
10. [REQ] Approval gate: every broadcast requires explicit user approval (kernel write-gate).

[PROHIBIT]
1. No WhatsApp/SMS without verified opt-in.
2. No shared/sold phone numbers.
3. No broadcast without user approval.
4. No Arabic message without RTL + Arabic stop-word.

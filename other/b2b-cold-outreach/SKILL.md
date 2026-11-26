---
name: b2b-cold-outreach
description: B2B cold outreach closer — enrich, sequence, and convert cold prospects via compliant email/LinkedIn. CAN-SPAM aligned. Do not use for lead generation crm tasks — use `lead-generation-crm` instead.
personas:
  - SALES
triggers:
  - cold email
  - اوت ريتش
  - prospecting
  - b2b cold outreach
  - رسالة باردة
  - اكتساب عملاء
tech_stack:
  - twentyhq/twenty
  - chatwoot/chatwoot
  - knadh/listmonk
---
[SKILL] b2b-cold-outreach
[OBJ] Generate meetings and deals from cold outreach — enrich prospects, write compliant sequences, and convert replies into pipeline. Complements `lead-generation-crm` and `freelance-platforms`.

[RULES]
1. [REQ] Targeting: build ICP-matched list (role/seniority/industry/size). No list = no outreach. Enrich via free paths (LinkedIn, web, Apollo free); respect `marketing-compliance`.
2. [REQ] Sequence design: 3-5 touches over 10-14 days, multi-channel (email + LinkedIn). Each email uses `copy-frameworks` (PAS/BAB), one ask, plain-text feel.
3. [CMD] Context7 IDs: `twentyhq/twenty` (prospect store), `chatwoot/chatwoot` (reply inbox), `knadh/listmonk` (cold list isolation).
4. [REQ] Compliance: CAN-SPAM (identity, opt-out, no deceptive subject); GDPR (legitimate interest or consent); TCPA for SMS. Cold list kept separate from opt-in lists. Gate via `marketing-compliance`.
5. [REQ] Free-first: Twenty (AGPL) for CRM, manual/LinkedIn free, Listmonk for isolated cold sends; paid sequencers (Instantly/Smartlead) only as parity.
6. [REQ] Personalization: reference a specific signal (post, hiring, tech) per prospect; no mail-merge spam. <50 sends/day per domain to protect deliverability.
7. [REQ] Deliverability: SPF/DKIM/DMARC set, warm-up, reply-friendly copy, no attachments/links-heavy first touch.
8. [REQ] Arabic/RTL: Arabic cold outreach needs RTL, formal honorifics, local business etiquette per `arabic-freelance`; separate ar sequence.
9. [REQ] Handoff: positive reply → `lead-generation-crm` opp + `client-onboarding`; objection → nurture; no → record reason for win/loss.
10. [REQ] Measurement: deliverability, reply rate, meeting rate, $/meeting. Feed `marketing-analytics`.

[PROHIBIT]
1. No cold email without `marketing-compliance` pass.
2. No purchased or ToS-violating scraped lists.
3. No fake sender identity or deceptive subject.
4. No Arabic outreach with broken RTL/etiquette.

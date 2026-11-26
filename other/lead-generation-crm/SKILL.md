---
name: lead-generation-crm
description: Lead generation and CRM orchestration — capture, enrich, score, and route leads into a pipeline. Free-first Twenty CRM; integrates with outreach and automation.
personas:
  - SALES
  - MARKETING
triggers:
  - lead generation crm
  - lead
  - CRM
  - lead gen
  - prospecting
  - pipeline
  - اكتساب عملاء
tech_stack:
  - twentyhq/twenty
  - hubspot/hubspot-crm
  - chatwoot/chatwoot

---
[SKILL] lead-generation-crm
[OBJ] Turn anonymous interest into qualified, tracked opportunities inside a CRM. Capture from every channel, enrich, score (fit/intent/behavior), and hand off to `b2b-cold-outreach` or `client-onboarding`.

[RULES]
1. [REQ] Lead lifecycle: Capture → Enrich → Score → Nurture → Handoff. Each stage updates the CRM object; never keep leads in spreadsheets only.
2. [CMD] Context7 IDs: `twentyhq/twenty` (metadata-driven CRM objects), `hubspot/hubspot-crm` (free tier API), `chatwoot/chatwoot` (omnichannel inbox, MIT).
3. [REQ] Free-first CRM: Twenty (AGPL, self-host) default; HubSpot free tier as SaaS parity; Chatwoot for conversation capture. Salesforce/Pipedrive only as paid parity.
4. [REQ] Data model (from Twenty): Company → Person → Opportunity → Activity. Map every inbound to a Person+Company; dedupe on email/domain.
5. [REQ] Lead scoring: `lead_scorer` 0-100 from fit (ICP match), intent (page/deal signals), behavior (opens/clicks/visits). Route ≥70 to sales, 40-69 to nurture, <40 to cold list.
6. [REQ] Capture points: website form, LinkedIn DM, cold reply, WhatsApp (see `whatsapp-sms`), webinar, referral. All must write to CRM, not DMs-only.
7. [REQ] Enrichment free-first: Clearbit-free path = Apollo free tier / LinkedIn manual / web search. No PII scraping without consent; respect `marketing-compliance`.
8. [REQ] Nurture handoff: low-score leads enter `marketing-automation` journey; high-score into `b2b-cold-outreach` sequence. Log every touch.
9. [REQ] Arabic/RTL: Arabic company/person names stored with proper unicode; pipeline labels offered in ar/en; Chatwoot RTL inbox supported.
10. [REQ] Pipeline hygiene: weekly review of stale (>14d no activity) opportunities; auto-reminder task created.

[PROHIBIT]
1. No CRM write of leads lacking capture source + consent flag.
2. No manual PII scraping violating platform ToS.
3. No sales handoff without a score recorded.
4. No storing credentials/API tokens in the CRM notes.

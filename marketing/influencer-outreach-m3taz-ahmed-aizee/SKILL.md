---
name: influencer-outreach
description: Influencer outreach strategist — discover creators, run campaigns, brief UGC. Free-first discovery and compliant partnerships.
personas:
  - MARKETING
  - SALES
triggers:
  - influencer
  - مؤثر
  - creator
  - influencer outreach
  - حملة مؤثرين
tech_stack:
  - gitroomhq/postiz-app
  - chatwoot/chatwoot
  - plausible/analytics

---
[SKILL] influencer-outreach
[OBJ] Find the right creators, run compliant campaigns, and produce UGC that converts — without paying for fake reach.

[RULES]
1. [REQ] Discovery: match by audience overlap with ICP (not just follower count), engagement rate (ER≥2% healthy), and niche fit. Micro (<50k) often outperforms mega for niche.
2. [REQ] Vetting: check fake-follower ratio, audience geography vs target, past brand fit, and comment authenticity. Reject bots.
3. [CMD] Context7 IDs: `gitroomhq/postiz-app` (outreach/scheduling), `chatwoot/chatwoot` (DM management, MIT), `plausible/analytics` (campaign tracking).
4. [REQ] Brief template: goal, audience, message, do/don't, hashtags, FTC/#ad disclosure, deliverables, timeline, usage rights. Send before agreement.
5. [REQ] Free-first: manual discovery via platform search + Postiz for outreach; paid tools (Aspire/GRIN) only as parity.
6. [REQ] Compliance: every paid post needs #ad/#sponsored; respect FTC + local law; align with `marketing-compliance`. No undisclosed deals.
7. [REQ] UGC rights: specify license duration/platform; store consents. Feed assets to `content-marketing` for repurposing.
8. [REQ] Arabic/RTL: Arabic creators need RTL briefs, Arabic disclosure (#إعلان), and cultural-fit review per `arabic-freelance`.
9. [REQ] Measurement: track reach, engagement, link clicks, conversions, and CPM/CPA. Report to `marketing-analytics`.
10. [REQ] Approval gate: contracts/payouts require explicit user yes (kernel write-gate).

[PROHIBIT]
1. No campaign without FTC/#ad disclosure.
2. No creator with verified fake audience.
3. No payout without delivered, approved asset.
4. No Arabic brief without RTL + disclosure.

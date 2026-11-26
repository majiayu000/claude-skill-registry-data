---
name: pr-pitch
description: PR and press pitch strategist — match journalist queries, craft pitches, run outreach. Free-first HARO/alternative sources.
personas:
  - MARKETING
triggers:
  - press release
  - HARO
  - PR
  - pr pitch
  - علاقات صحفية
  - بيان صحفي
tech_stack:
  - chatwoot/chatwoot
  - gitroomhq/postiz-app
  - plausible/analytics
---
[SKILL] pr-pitch
[OBJ] Earn credible media coverage — match journalist queries, craft compelling pitches, and run measured outreach that builds authority (not spam).

[RULES]
1. [REQ] Newsworthiness test: every pitch must answer "why now / why this outlet / why this audience." No pitch without a hook.
2. [REQ] Query sourcing: monitor HARO (or free alt like Qwoted/Help a B2B Writer), journalist Twitter lists, and subreddit r/Journalism. Free-first; paid PR wires only as parity.
3. [CMD] Context7 IDs: `chatwoot/chatwoot` (outreach inbox), `gitroomhq/postiz-app` (schedule follow-ups), `plausible/analytics` (referral tracking).
4. [REQ] Pitch format: subject = angle, body = 80-150 words, data point + expert quote + availability. Personalize per journalist; never bulk-blast identical text.
5. [REQ] Media list: segment by beat/region/outlet; track relationships in `lead-generation-crm` (treat journalists as a contact type).
6. [REQ] Press release: boilerplate, quote, dateline, contact; distribute only on real news (launch/funding/research). Link `content-marketing` for the asset.
7. [REQ] Arabic/RTL: for Arabic outlets, Arabic pitch + RTL, local angles (Gulf/MENA), respect editorial calendars (Ramadan etc.). See `arabic-freelance`.
8. [REQ] Follow-up: one polite nudge after 3-5 days; never harass. Track response rate → refine targeting.
9. [REQ] Measurement: placements, domain authority of outlet, referral traffic, backlinks. Report to `marketing-analytics` + `seo-lord` (link equity).
10. [REQ] Approval gate: sending pitches on behalf of user requires explicit yes (kernel write-gate).

[PROHIBIT]
1. No bulk identical pitch to journalists.
2. No fabricated data or fake expert quotes.
3. No pitch sent without user approval.
4. No Arabic outreach without RTL + cultural fit.

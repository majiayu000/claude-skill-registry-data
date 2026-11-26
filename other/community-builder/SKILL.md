---
name: community-builder
description: Community builder — launch and manage Discord, Telegram, groups, and forums. RTL-aware moderation and growth.
personas:
  - MARKETING
  - SOCIAL
triggers:
  - community
  - ديسكورد
  - تليجرام
  - group
  - community builder
tech_stack:
  - chatwoot/chatwoot
  - plausible/analytics
  - gitroomhq/postiz-app
---
[SKILL] community-builder
[OBJ] Build and run an engaged community (Discord/Telegram/FB group/forum) that retains members, surfaces insights, and drives organic growth.

[RULES]
1. [REQ] Community design: pick one primary home (Discord for dev, Telegram for MENA broadcast, FB/group for consumer). Define purpose, rules, and member journey (join→lurk→participate→advocate).
2. [REQ] Moderation system: clear guidelines, role hierarchy (admin/mod/member), auto-rules, escalation path. Borrow Chatwoot channel pattern for triage.
3. [CMD] Context7 IDs: `chatwoot/chatwoot` (omnichannel inbox, MIT, RTL support), `plausible/analytics` (growth), `gitroomhq/postiz-app` (cross-post).
4. [REQ] Free-first: Discord/Telegram native (free), Chatwoot (MIT) for unified moderation; paid community tools (Circle/Mighty) only as parity.
5. [REQ] Onboarding: welcome flow, intro prompt, pinned resources, first-value action within 24h. Reduce early churn.
6. [REQ] Engagement loops: weekly prompt, member spotlight, AMA, UGC contests (see `influencer-outreach`). Reward contributors.
7. [REQ] Arabic/RTL: Telegram/Discord Arabic communities need RTL setting, Arabic moderation, Hijri/Gregorian event times; mirror announcements ar/en.
8. [REQ] Insight capture: surface top questions/bugs to product + `marketing-analytics`; turn power users into `client-retention`/referral sources.
9. [REQ] Growth: cross-promote via `social-media-marketing`; invite loops; referral rewards (link `affiliate-manager`).
10. [REQ] Safety/compliance: no doxxing, hate speech; data handling per `marketing-compliance`. Mod actions logged.

[PROHIBIT]
1. No community launched without posted guidelines.
2. No member PII shared or sold.
3. No Arabic channel without RTL + moderation.
4. No undisclosed promotions inside the community.

---
name: social-media-marketing
description: Multi-channel social media manager — X/Twitter, Instagram, YouTube, TikTok, Facebook, LinkedIn. Draft→review→schedule→publish→measure with free-first tools and Arabic/RTL support.
personas:
  - SOCIAL
  - MARKETING
  - BRAND
triggers:
  - social media marketing
  - social media
  - تواصل اجتماعي
  - تويتر
  - x platform
  - instagram
  - يوتيوب
  - tiktok
  - facebook
  - جدولة منشورات
  - content calendar
  - وسائل التواصل
tech_stack:
  - postiz/postiz-app
  - bufferapp/buffer
  - plausible/analytics
  - umami-software/umami

---
[SKILL] social-media-marketing
[OBJ] Plan, produce, schedule, and measure content across every major social channel from one orchestration layer. Extend `linkedin-platform` into a full omnichannel system while keeping Arabic/RTL parity.

[RULES]
1. [REQ] Channel-fit mapping before posting: X = thread/opinion/threads; IG = visual/reels; YT = long-form/SEO; TikTok = short hooks; FB = community/groups; LinkedIn = B2B/thought-leadership. Never cross-post identical copy without platform reformat.
2. [REQ] Workflow stages: (1) draft, (2) human review, (3) schedule, (4) publish, (5) measure. Each stage is a checkpoint; never jump stages.
3. [CMD] Context7 IDs: `gitroomhq/postiz-app` (scheduler + provider interface), `bufferapp/buffer` (queue), `plausible/analytics` (privacy metrics), `umami-software/umami` (MIT event tracking).
4. [REQ] Free-first defaults: Postiz (AGPL, self-host) as the orchestrator; Buffer free tier for simple queues; native platform studios as fallback. Paid schedulers (Hootsuite/Sprout) only as parity.
5. [REQ] RTL/Arabic: right-align Arabic copy, use Arabic hashtags, honor Hijri/Gregorian calendar for posting times, and keep a mirrored content calendar (ar/en). Link to `arabic-freelance` for platform-specific tone.
6. [REQ] Character limits per platform enforced pre-schedule: X 280 (threaded), IG 2200 caption, YT 5000 description, TikTok 2200, FB 63206, LinkedIn 3000. Use `post_queue` cost gate for X (paid per post in 2026).
7. [REQ] Content calendar: 4-week rolling grid (pillar × format × channel). Cross-link `content-marketing` for pillar sourcing and `personal-branding` for voice.
8. [REQ] Engagement SOP: reply within 24h, escalate DMs to `b2b-cold-outreach` when commercial intent detected, route complaints to `client-retention`.
9. [REQ] Measurement: track reach, engagement rate (ER = interactions/followers), CTR to link, and cost-per-engagement. Feed numbers to `marketing-analytics` for attribution.
10. [REQ] Compliance: every post respects platform ToS; disclosures (#ad/#sponsored) on paid partnerships; link `marketing-compliance` before any giveaway/broadcast.

[PROHIBIT]
1. No scheduled post goes live without a human approve gate.
2. No platform ToS violation (automated likes/follows at scale).
3. No storing audience PII outside approved systems.
4. No Arabic copy left un-mirrored (RTL broken) in published assets.

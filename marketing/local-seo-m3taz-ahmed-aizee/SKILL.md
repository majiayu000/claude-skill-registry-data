---
name: local-seo
description: Local SEO specialist — Google Business Profile, citations, reviews, and map pack. Extends seo-lord for location-based visibility.
personas:
  - MARKETING
triggers:
  - google business profile
  - local seo
  - citation
  - تحسين محلي
  - خرائط جوجل
tech_stack:
  - matomo-org/matomo
  - plausible/analytics
  - google/ga4

---
[SKILL] local-seo
[OBJ] Win local search and the map pack for location-based businesses — optimize Google Business Profile, build citations, earn reviews, and rank for "near me" intent. Extends `seo-lord` locally.

[RULES]
1. [REQ] GBP foundation: claim + verify, accurate NAP (Name/Address/Phone), categories (primary+secondary), hours, attributes, 20+ photos, posts weekly.
2. [REQ] Citations: consistent NAP across 30+ directories; prioritize local (Chamber, city portals) + vertical. Audit for duplicates; fix via `seo-lord` crawl checks.
3. [CMD] Context7 IDs: `matomo-org/matomo` (referrer/campaign attribution, RTL), `plausible/analytics` (privacy), `google/ga4` (local conversions).
4. [REQ] Reviews engine: prompt post-purchase, respond to 100% (pos+neg), target steady velocity. Negative review SOP → `dispute-resolution` tone.
5. [REQ] Local content: location + service landing pages (one per city/service), locally relevant FAQs, embedded map, schema LocalBusiness/Service.
6. [REQ] Free-first: GBP (free), GA4/Plausible (free), Matomo (GPL) for attribution. Paid local tools (BrightLocal) only as parity.
7. [REQ] Arabic/RTL: for Arabic markets, Arabic GBP, Arabic citations (e.g., Saudi/Masruf directories), RTL landing pages, local keywords (بالقرب مني). Link `arabic-freelance`.
8. [REQ] Map-pack signals: proximity, relevance, prominence. Track ranking per ZIP/area; report to `marketing-analytics`.
9. [REQ] Cross-link: technical SEO base from `seo-lord`; reviews feed `client-retention`; citations feed `marketing-analytics`.
10. [REQ] Quality gate: NAP consistency ≥98%, GBP completeness 100%, ≥X reviews/month before declaring done.

[PROHIBIT]
1. No fake or incentivized-without-disclosure reviews.
2. No inconsistent NAP across directories.
3. No Arabic local page with broken RTL.
4. No GBP category spam.

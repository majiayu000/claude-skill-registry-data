---
name: google-yandex-2gis-local-seo
description: Safe CIS local SEO workflow for Google Business Profile, Yandex Business, Yandex Webmaster, Yandex Maps, 2GIS/2ГИС, Google Maps, NAP consistency, LocalBusiness schema, city/location pages, reviews, photos, posts, citations, and local discovery. Use when the user asks for local SEO in CIS/RU/KZ markets, локальное SEO СНГ, Яндекс Бизнес, 2ГИС, Google Maps, map pack visibility, branch/location SEO, regional SEO, NAP audit, local schema, city landing pages, reviews, local citations, or local business profile automation.
---

# Google Yandex 2GIS Local SEO

## Operating Rule

Optimize only from verified business facts. Do not invent branches, addresses,
hours, service areas, prices, reviews, ratings, licenses, photos, awards, or
delivery promises. If a fact is not in the site data, official business profile,
owner-provided material, or another cited public source, mark it as missing.

Use official platform docs first:

- Google Search / Google Business Profile / Google Maps docs.
- Yandex Business / Yandex Webmaster / Yandex Maps docs.
- 2GIS/2ГИС Help, 2GIS for Business, and official 2GIS advertising docs.
- Local project data and live profile evidence.
- Practitioner research only as secondary prioritization, never as permission to
  violate platform rules.

For current facts, browse or use live local APIs/UI evidence. Prefer project
scripts, exports, and owner-provided artifacts before manual UI work.

## Safety Gates

- Default to read-only audit, draft, validation, and evidence capture.
- Require explicit user approval before writing to GBP, Yandex Business,
  Webmaster, Maps, directory listings, reviews, posts, photos, or live site.
- Treat `--execute`, `--repair`, bulk listing imports, profile photo uploads,
  review replies, post publishing, and generated artifact writes such as
  `business:kit:write` as explicit write operations unless the current repo docs
  clearly define them as safe local-only outputs for the task.
- Never automate login, 2FA, SMS, mail, video verification, or owner checks
  through cloud browsers. Local owner-controlled browser/CDP is acceptable for
  evidence and assisted UI work.
- Do not request or store passwords, cookies, verification codes, private keys,
  recovery codes, or raw OAuth tokens.
- Do not create fake review flows, review gating, self-reviews, keyword-stuffed
  names, virtual-office addresses, duplicate cards, fake service areas, or
  hidden schema facts.
- Refuse ranking, indexing, profile approval, or moderation guarantees. State
  platform-dependent outcomes as pending until verified.
- Treat Google/Yandex moderation as a real state. Do not claim changes are live
  until the profile/search result or API confirms it.

## Workflow

1. **Classify the business**
   - Storefront, service-area business, hybrid, multi-location, or chain.
   - For each location, identify official name, address, phone, URL, hours,
     category/rubric, coordinates, service area, and owner account status.

2. **Collect evidence**
   - Site source: contact page, footer, city pages, schema, sitemap, robots,
     visible phone/address/hours.
   - Platform source: GBP/Yandex Business profile UI/API/export, Yandex
     Webmaster regionality, GSC, Maps, 2GIS or other local citation pages.
   - Analytics/source status: GSC, Yandex Webmaster, Metrika/GA/PostHog if
     available.
   - Store evidence paths/URLs in the final answer or project status.

3. **Compare NAP**
   - Compare visible site NAP, JSON-LD, GBP, Yandex Business, Yandex Maps, 2GIS,
     social profiles, and directory citations.
   - Flag exact mismatches, missing fields, duplicate profiles, wrong URL
     variants, stale hours, wrong categories/rubrics, and inconsistent phones.

4. **Audit local pages**
   - Each real city/location should have crawlable, indexable, canonical pages
     with visible NAP, city-specific content, local proof, useful FAQ, internal
     links, and matching LocalBusiness/Florist/Organization schema.
   - Avoid doorway pages: if swapping only the city name still works, the page is
     too generic.
   - Keep schema representative of visible content and validate JSON-LD.

5. **Audit Google local presence**
   - GBP claimed/verified status, primary category, secondary categories,
     address/service area, hours/special hours, phone, website URL, description,
     photos/videos, products/services, posts/updates, review response posture,
     profile performance, and API quota/access state.
   - For profile writes, prefer validateOnly/dry-run API paths first when the
     project supports them.

6. **Audit Yandex local presence**
   - Yandex Business publication/moderation status, address confirmation,
     rubric/activity, site URL, contacts, hours/holiday hours, photos, reviews,
     publications, products/services/YML feeds if relevant, and Yandex Webmaster
     regionality.
   - Confirm site URL variants match between Business and Webmaster.

7. **Audit 2GIS/CIS local presence**
   - 2GIS card existence, claim/access state, address, map point, entrance,
     office/floor/intercom, phone, messengers, email, website, social links,
     hours, payment methods, services/products, prices when visible, rubrics,
     photos, review state, duplicate cards, and moderation/update status.
   - Treat 2GIS as a real CIS discovery channel, not a generic citation row.
     Work from official 2GIS cards or the 2GIS business cabinet; do not invent
     branches, extra rubrics, review content, prices, or photos.

8. **Prioritize actions**
   - Fix trust blockers first: wrong/duplicate profile, unverified/hidden card,
     wrong category/rubric, inconsistent NAP, missing real address/phone/hours,
     profile suspension/moderation, noindex/canonical/sitemap issues.
   - Then improve conversion/discovery: better city pages, schema completeness,
     photos, review response drafts, posts, citation cleanup, internal links.

9. **Verify**
   - Re-run local repo gates, API dry-runs, profile snapshots, live URL checks,
     sitemap submissions, IndexNow/Yandex/GSC status, and screenshots where
     appropriate.
   - Report what is verified, what is pending moderation, and what is blocked by
     account/API/quota access.

## Project Defaults

When working in a project repo:

- Read local project status/rules first when present.
- Treat the project's structured city/location data as the canonical NAP seed
  unless current owner/platform evidence overrides it.
- Prefer existing project scripts for readiness, listing exports, API dry-runs,
  sitemap/index submissions, and smoke checks.
- Keep GBP/Yandex/2GIS writes explicit, reviewed, and scoped to known real
  locations. Do not bulk-create cards from website pages alone.
- If the project goal says "on-site SEO only", treat GBP/Yandex/2GIS/Maps
  changes as separate approval-gated account work, even when credentials exist.
- For browser evidence, use the dedicated ops browser profile/local CDP helper
  if already configured; do not use cloud browser sessions for authenticated
  Google/Yandex owner accounts.

## Output Shape

Use this compact structure unless the user asks otherwise:

```text
Status:
- verified facts
- blockers
- risky assumptions

Priority fixes:
1. issue -> action -> verification
2. issue -> action -> verification

Safe drafts:
- GBP/Yandex/2GIS description/post/review response/schema/page copy, marked as draft

Evidence:
- commands, artifact paths, URLs, API/UI status
```

## References

Read `references/google-yandex-guardrails.md` when platform rules, citations, or
current official docs matter.

Read `references/2gis-cis-guardrails.md` when 2GIS, 2ГИС, Kazakhstan/Russia/CIS
map listings, rubrics, photos, reviews, product/service cards, or local
citations matter.

Read `references/skill-candidate-review.md` when deciding whether to import or
trust an external local SEO skill.

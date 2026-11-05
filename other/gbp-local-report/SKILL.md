---
name: gbp-local-report
description: Analyze Google Business Profile and local-search performance for visibility, search terms, calls, directions, website clicks, bookings/actions, reviews, profile completeness, local-pack presence, and local demand capture. Use when the user asks for a Google Business Profile/GBP report, local SEO report, Maps performance review, review/reputation audit, or provides GBP Performance exports/screenshots and wants to know how Nick's Tire & Auto is performing locally.
triggers: google business profile, gbp report, maps, local search, search terms, calls from google, directions, website clicks, reviews, local pack, profile completeness, local visibility
---

# GBP Local Report

Audit whether the Google Business Profile is increasing qualified local discovery and customer actions.

## Workflow

1. Establish business/location, exact date range, timezone, and available GBP metrics.
2. Use authorized profile data when available; otherwise analyze exports, screenshots, public profile evidence, review data, or local-rank grids supplied by the user.
3. Inspect the current data schema rather than assuming Google exposes the same metrics forever.
4. Analyze discovery and actions separately:
   - searches/search terms or discovery indicators when available
   - profile/views/impressions where available
   - calls
   - direction requests
   - website clicks
   - bookings/messages or other actions if enabled
5. Segment search demand into brand, service, tire/product, problem/symptom, and location intent when query data exists.
6. Audit reputation:
   - review volume and velocity
   - rating distribution
   - recent negative themes
   - recurring positive service themes
   - owner-response coverage/quality where relevant
7. Audit profile quality only where current evidence exists: categories, services/products, hours, attributes, photos, posts, Q&A, booking/website links, and policy/status issues.
8. If local-pack/rank-grid data exists, separate proximity effects from profile/content effects and avoid treating one grid snapshot as a durable ranking.
9. Connect GBP activity to downstream calls, bookings, arrivals, and revenue when joinable.
10. Read `references/report-contract.md` and follow its output structure.

## Rules

- Do not add calls, directions, and website clicks together and label the total "customers".
- Do not treat views or impressions as demand capture by themselves.
- Use exact dates and flag Google metric-definition changes that break period comparisons.
- When current Google Business Profile guidance or feature behavior matters, verify it with an authoritative current source.
- Prefer measurable profile experiments over generic local-SEO checklists.

## Useful triggers

Examples: "run the GBP report", "how is Nick's doing on Maps?", "audit our Google Business Profile", "why did calls from Google drop?", "check reviews and local visibility".

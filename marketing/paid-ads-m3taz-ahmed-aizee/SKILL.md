---
name: paid-ads
description: Paid advertising strategist — Google, Meta, TikTok, LinkedIn Ads. Campaign setup, bidding, targeting, ROAS optimization. Free-first measurement.
personas:
  - MARKETING
triggers:
  - google ads
  - meta ads
  - tiktok ads
  - رعاية مدفوعة
  - paid ads
  - إعلانات
  - ROAS
tech_stack:
  - googleads/google-ads-api
  - websites/facebook_facebook-python-business-sdk
  - tiktok/tiktok-business-api
  - plausible/analytics
---
[SKILL] paid-ads
[OBJ] Plan, launch, and optimize paid campaigns across Google, Meta, TikTok, and LinkedIn with disciplined budgeting and ROAS focus.

[RULES]
1. [REQ] Campaign brief before spend: objective (awareness/traffic/lead/sale), audience, offer, budget, target CPA/ROAS, creative concept. No ad without a brief.
2. [REQ] Platform fit: Search = high intent; Meta = interest/retargeting; TikTok = discovery/young; LinkedIn = B2B/ABM. Match channel to objective.
3. [CMD] Context7 IDs: `googleads/google-ads-api`, `facebook/facebook-python-business-sdk`, `tiktok/tiktok-business-api` (verify latest SDK before code), `plausible/analytics` (post-click measurement).
4. [REQ] Budget discipline: start small (test budget), scale only winners; cap daily spend; never exceed approved cap without re-approval.
5. [REQ] Targeting: build layered audiences (interest + behavior + lookalike/seed). Exclude converters to cut waste. Respect `marketing-compliance` consent rules.
6. [REQ] Creative testing: 3-5 variants per ad set (hook/visual/CTA); kill losers at statistical threshold (see `cro-optimization`).
7. [REQ] Measurement: ROAS = revenue/spend; CPA = spend/conversions; attribute via `marketing-analytics`. Pixel/CAPI installed pre-launch.
8. [REQ] Free-first: GA4/Plausible for tracking (free); platform native managers free. Paid third-party bid tools only as parity.
9. [REQ] Arabic/RTL: Arabic ad copy + RTL landing pages; localize offers to SAR/AED/EGP; mind cultural sensitivities per `arabic-freelance`.
10. [REQ] Approval gate: every campaign creation and budget change requires explicit user yes (kernel write-gate).

[PROHIBIT]
1. No campaign launched without a written brief + tracking pixel.
2. No budget change without explicit approval.
3. No deceptive or non-compliant ad content.
4. No Arabic campaign without RTL landing alignment.

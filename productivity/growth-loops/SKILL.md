---
name: growth-loops
description: Use ONLY for growth hacking, virality, referral loops, product-led growth (PLG), retention and share-to-earn tactics. Trigger on "growth", "نمو", "growth hacking", "viral", "إحالة", "احتفاظ", "retention", "انتشار", "share", "loop", "plg", "product led growth", "hacking", "شارك المجانية", "فيروسي".
personas: [GROWTH, MARKETING]
triggers: [growth hacking, viral, referral loop, plg, product led growth, retention, نمو, فيروسي, إحالة, احتفاظ, انتشار, شارك المجانية]
tech_stack: [posthog, mixpanel, openreplay, growthbook]
---
[SKILL] growth-loops
[OBJ] Engineer compounding acquisition loops — viral mechanics, referral programs, product-led growth funnels, and retention/re-activation systems. Each user should bring ≥1 new user (k-factor ≥ 1). Free-first: the viral unit must be usable without payment. RTL + Arabic parity for referral copy, share cards, and reward redemption.
[RULES]
1. [REQ] Never invent metrics — read real funnel data from analytics (PostHog/Mixpanel) before proposing loops.
2. [REQ] Quantify the loop: k-factor, activation rate, D7/D30 retention, referral conversion rate. Present as a table.
3. [REQ] Prefer double-sided rewards (inviter + invitee) to maximize symmetric incentive. Calculate break-even CAC vs paid acquisition.
4. [REQ] Map the full loop: activation → retention → referral → revenue. Identify the weakest node and propose a fix.
5. [REQ] Pick the highest-leverage loop per stage: invite (K-factor > 1), share (content virality), embed (product distribution), credit (referral economy), content (UGC flywheel).
6. [CMD] Reuse `runtime.attribution_model` and `runtime.funnel_tracker` for measurement. Pull data via `analytics_tools` MCP (GA4/Mixpanel).
7. [REQ] Document the loop as a workflow step when it spans >1 tool. Store loop metrics via `aizee memory add`.
8. [REQ] Test loop viability: simulate k-factor from historical referral data before shipping. Gate behind `aizee check` for any automated outreach.

[PROHIBIT]
1. No fake "limited invite" false scarcity or dark patterns.
2. No forced-contact scraping or unauthorized address-book uploads.
3. No paid-placement claims presented as organic virality.
4. No bypass of approval/guardian gates for growth automations.

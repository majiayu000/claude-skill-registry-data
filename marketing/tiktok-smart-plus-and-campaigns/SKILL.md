---
name: tiktok-smart-plus-and-campaigns
description: Build and manage TikTok campaigns in the unified 2026 Smart+ experience across full, partial, and manual automation. Use when the user asks how to set up a Smart+ campaign, which objective to pick (Sales, Lead Generation, App Promotion, Traffic), whether to let TikTok automate targeting and bidding or set them by hand, how the new asset-group ad model works, how automatic campaign budget differs from custom ad group budgets, how to migrate a legacy manual or Smart+ campaign into the unified flow, or how to create Smart+ campaigns through the Marketing API.
---

# TikTok Smart+ and campaigns

Set up and run a TikTok campaign in the 2026 unified experience, where the old manual and Smart+ flows are merged into one campaign builder with per-module automation. Decide, module by module, what TikTok automates and what you control, so you get automation lift where you have signal and keep the reins where the client needs guardrails. This is the campaign build and management skill, not the pixel and server-event skill.

This skill assumes you know CPA, ROAS, CPM, and how a campaign / ad group / ad hierarchy maps to budget and bidding. For that KPI math and shared terminology, see the `programmatic-foundations` skill. For sending web, app, and offline conversions server-side to power Smart+ optimization, see the `tiktok-events-api-server-side` skill. For the Meta equivalent (Advantage+ and OUTCOME_SALES), see the `meta-advantage-plus-campaigns` skill.

## When to use this skill

- "Set up a TikTok Smart+ campaign" / "How do I use the new unified TikTok campaign builder?"
- "Which objective do I pick, Sales, Lead Generation, App Promotion, or Traffic?"
- "Should I let TikTok automate targeting and bidding or set them manually?"
- "What is the asset-group ad model / why can I add up to 50 creatives to one ad?"
- "Automatic campaign budget vs custom ad group budgets, which do I use?"
- "How do I migrate my old manual or legacy Smart+ campaign into the unified flow?"
- "Create a Smart+ campaign through the TikTok Marketing API."

Boundaries with sibling skills:
- Sending conversions server-side (Events API, event_id deduplication, match keys): `tiktok-events-api-server-side`.
- KPI definitions and target-setting math (CPA, ROAS, break-even): `programmatic-foundations`.
- The Meta side of the same automation shift (Advantage+, OUTCOME_SALES, advantage_state): `meta-advantage-plus-campaigns`.
- Reconciling TikTok-reported conversions against a source of truth: `cross-platform-conversion-reconciliation`.
- Consent capture that gates whether ads data may flow at all: `gtm-consent-mode-v2` and `privacy-and-consent`.

## Quick reference

| Situation | Automation mode | Why |
| --- | --- | --- |
| New account, no first-party signal, want fast learning | Full automation (Smart+) | Nothing to hand-tune yet, let the system explore |
| Strong signal, but client mandates specific geos or exclusions | Partial automation | Lock targeting and brand safety, automate bidding and creative |
| Regulated vertical, hard placement or audience exclusions required | Manual on the gated modules | Compliance cannot be left to automation |
| Proven audience you must not drift off | Manual audience, automate the rest | Protect the audience, keep creative and bid lift |
| Testing a new creative concept at controlled spend | Manual budget and schedule, automate delivery | Cap the risk while the concept proves out |

Automation is set per module, not per campaign. A single campaign can run automatic budget at the campaign level, manual audience and placements at the ad group level, and automated creative at the ad level. Pick per module against the decision rules below.

The three supported Smart+ objectives are Sales, Lead Generation, and App Promotion. Traffic runs in the same unified builder as a Smart+ Traffic campaign. Awareness, reach, video views, and community-interaction objectives run in the standard (non Smart+) builder in the same interface.

## Core process

1. Confirm the objective first, because it fixes the optimization event and the eligible modules. Sales optimizes to a purchase or a defined conversion event, Lead Generation to a form submit or lead event, App Promotion to installs or in-app events, Traffic to landing-page views or clicks. A wrong objective cannot be fixed by tuning later, so get it right before building.
2. Confirm the conversion signal exists for the objective. Sales and Lead Generation need a working pixel or Events API feed with the right event firing, or the optimizer has nothing to learn from. If the feed is not live, stand it up first with the `tiktok-events-api-server-side` skill before you launch a conversion objective.
3. Choose the automation mode per module, not for the whole campaign. Default to full automation only when you lack signal or history. When the client has non-negotiable targeting, exclusions, or budget guardrails, set those modules manually and let TikTok automate the rest. See Decision rules.
4. Set budget at the right level. Automatic campaign budget lets the system move spend across ad groups toward the best performers, which suits automation but reduces per-ad-group control. Custom ad group budgets pin spend per ad group, which you want when a client requires a fixed split or an ad group must not starve. You cannot mix freely, so pick the model that matches the control the client needs.
5. Build the ad as an asset group. In the unified model an ad holds up to 50 creative assets with their own destination URLs and product sets, and the system assembles and rotates them. Supply strong, varied source assets, because automated creative can only recombine what you give it. Enhanced ad formats and auto-generated CTAs are opt-in at the ad level and can be turned off in Ads Manager at any time.
6. Set targeting and bidding to match the mode. Under full automation TikTok sets audience and placements and runs intelligent bidding to your goal. Under partial or manual, set audience, placements, brand safety, bid strategy, and schedule by hand on the ad group. Do not stack a hard bid cap onto an automated bid goal unless delivery forces it, because a low cap starves the optimizer.
7. Human-gate the launch. Read back the objective, optimization event, budget model and amount, targeting, exclusions, and bid strategy to the client before anything spends. Never push a live campaign or a budget change without explicit sign-off.
8. Hold through the learning window before judging. Automated delivery needs a stabilization window to calibrate, and every material edit (objective, optimization event, budget model, bid target) can reset it. Batch changes, then wait, rather than tuning daily.

## Decision rules and thresholds

### Full, partial, or manual

- Full automation when you lack first-party signal or account history, or when speed to learning beats fine control. The system sets audience, placements, and bidding.
- Partial automation when you have signal but a specific constraint: lock the constrained module (geo, audience, placements, or brand safety) and automate the rest. This is the common agency default because it captures automation lift without surrendering compliance-critical settings.
- Manual on a module when leaving it to automation creates legal or brand risk: mandated geo restrictions, required audience or placement exclusions in a regulated vertical, or a fixed budget split the client contracted for. Automate everything that is not gated.

Do not read "manual" as all-or-nothing. The point of the unified builder is that automation is per module. Automating creative while manually fixing audience is a valid, common configuration.

### Objective to optimization event

| Objective | Optimizes toward | Signal it needs |
| --- | --- | --- |
| Sales | Purchase / defined conversion event | Pixel or Events API purchase event live |
| Lead Generation | Form submit / lead event | Instant form or lead event feed live |
| App Promotion | Install or in-app event | App event feed via MMP or Events API |
| Traffic | Landing-page view or click | None required, but a pixel improves quality |

Pick the objective by the business outcome, not by what is easiest to hit. Optimizing Traffic to clicks when the client wants sales buys cheap clicks that do not convert.

### Budget model

- Automatic campaign budget: the system distributes across ad groups toward performance. Use it when you trust the automation to allocate and the client does not need a fixed per-ad-group split.
- Custom ad group budgets: spend is pinned per ad group. Use it when a client contracted a fixed split, when an always-on ad group must not be starved by a spikier one, or when you are isolating a test.
- Set a realistic daily budget for the optimization event. A budget too small to clear a handful of conversion events per day per ad group leaves the optimizer without enough events to calibrate.

### Creative asset groups

- Feed varied source assets. The ad holds up to 50 assets and the system recombines them, so diversity of hook, format, and message drives the lift. A single asset gives automation nothing to optimize.
- Enhanced ad formats and auto CTAs are opt-in and reversible. Turn them off when a regulated vertical forbids added claims or altered creative, then supply compliant assets directly.
- Turn off Smart+ generated creatives in Ads Manager when the client must approve every asset that runs.

### Learning and change discipline

- Treat the first stabilization window as read-only for structural settings. Changing the objective, optimization event, budget model, or bid target resets calibration and wastes the window.
- Batch edits, then hold. Daily tinkering keeps a campaign permanently in learning and starves it of the stable window automation needs.
- If delivery is flat, check budget size, event volume, and targeting breadth before touching the bid. A starved optimizer usually needs more events or broader targeting, not a bid change.

## Reference material

- `references/smart-plus-objectives.md`: the Smart+ and standard objectives in the 2026 unified builder, the optimization event and required signal for each, and which objectives run in Smart+ versus the standard flow. Read this when picking an objective or explaining why an objective needs a specific event feed.
- `references/module-by-module-automation.md`: every campaign, ad group, and ad module with what full automation sets, what partial and manual expose, and the agency decision (automate / lock) with the reason. Read this when deciding, module by module, what to automate and what to control for a specific client.
- `references/upgraded-smart-plus-api.md`: the TikTok Marketing API surface for creating and managing campaigns in the unified model, the campaign / ad group / ad creation methods and key fields, the legacy Smart+ dedicated endpoint sunset, and a safe read-first automation pattern. Read this when building or managing Smart+ campaigns programmatically.

## Templates and examples

- Direct-to-consumer skincare, strong pixel history, Sales objective: partial automation. Lock geo to US, exclude existing purchasers as an audience, automate bidding to a Target Cost purchase goal, feed 12 varied video assets into one ad as an asset group, automatic campaign budget at 800 USD/day. Hold the learning window before reading CPA.
- New mobile game, no account history, App Promotion objective: full automation. Let TikTok set audience and placements, optimize to the install event via the MMP feed, supply 8 gameplay hooks as assets, automatic campaign budget at 500 USD/day. Reassess after the stabilization window.
- Regulated financial-services lead-gen, App Promotion excluded, Lead Generation objective: manual on the gated modules. Set placements to feed-only, apply the required audience and content exclusions by hand, turn off enhanced formats and auto CTAs so only approved creative runs, custom ad group budgets to hold the contracted split, automate bidding only. Read every setting back to compliance before launch.
- Migrating a legacy Smart+ Sales campaign: rebuild it in the unified builder rather than editing in place, because the module structure and asset-group ad model differ. Map the old audience and budget to the new modules, choose the automation mode per module, and relaunch with the learning window in mind.

## Common pitfalls

- Wrong objective locks the wrong event. Traffic optimizes to clicks, not purchases. If the client wants sales, pick Sales, even though Traffic delivers cheaper headline numbers.
- Launching a conversion objective with no live event feed. Sales and Lead Generation need the pixel or Events API event firing before the optimizer can learn. Stand up the feed first with `tiktok-events-api-server-side`.
- Full automation in a regulated vertical. Letting the system pick audience and placements can breach mandated exclusions. Set the gated modules manually and automate only what is safe.
- One creative in an asset-group ad. Automated creative recombines what you supply, so a single asset gives it nothing to work with. Feed varied hooks and formats.
- Automatic campaign budget when the client contracted a fixed split. Automatic budget moves spend across ad groups, which breaks a mandated allocation. Use custom ad group budgets there.
- Daily tinkering. Every structural edit can reset the learning window. Batch changes and hold.
- A tight bid cap on an automated goal. A cap below the clearing price starves the optimizer. Remove or raise it if delivery suffers, or switch to a goal-based bid without a hard cap.
- Assuming the legacy Smart+ dedicated API still works. The old dedicated Smart+ creation path was retired in the unified move. Build through the standard campaign creation surface. See `references/upgraded-smart-plus-api.md`.

## Sources

- [About updates to Smart+](https://ads.tiktok.com/help/article/about-updates-to-smart-plus?lang=en) (as of July 2026)
- [About Smart+ campaign](https://ads.tiktok.com/help/article/about-smart-plus-campaign) (as of July 2026)
- [Getting started with the Events API](https://ads.tiktok.com/help/article/getting-started-events-api?lang=en) (as of July 2026)
- [Event deduplication](https://ads.tiktok.com/help/article/event-deduplication?lang=en) (as of July 2026)
- [Events API consolidated endpoint](https://ads.tiktok.com/business/en/blog/events-api-consolidated-endpoint) (as of July 2026)

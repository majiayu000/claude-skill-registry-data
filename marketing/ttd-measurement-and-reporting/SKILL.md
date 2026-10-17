---
name: ttd-measurement-and-reporting
description: Measure outcomes and read reporting in The Trade Desk at a publicly supportable level. Use when the user asks about "Trade Desk reporting", "TTD measurement", "TTD attribution", "TTD measurement marketplace", "TTD raw event data", "TTD brand lift", in-platform reporting, multi-touch attribution or media mix modeling on TTD, outcome and incrementality measurement, or pulling event-level data for advanced analysis. Covers in-platform reporting and attribution, the marketplace of independent measurement providers, brand lift and outcome measurement, and log-level event data, and flags every detail that requires a TTD partner account.
---

# The Trade Desk measurement and reporting

How to think about measurement and reporting in The Trade Desk (TTD) using only what the platform documents publicly, and where the line falls between public concepts and partner-gated detail. TTD frames measurement as part of how a campaign operates, not a post-campaign afterthought: you see the path from impression to outcome and optimize against it mid-flight. This skill covers four public pillars (in-platform reporting and attribution, the marketplace of independent measurement providers, brand lift and outcome measurement, and log-level event data), and it marks the specifics you can only confirm once you have TTD access.

For KPI math and metric definitions (CPM, CPA, VCR, reach, frequency, view-through vs click-through), see the `programmatic-foundations` skill. For building the right report for a campaign objective, see the `reporting-by-campaign-goal` skill. For multi-touch path analysis as a cross-DSP concept, see the `path-to-conversion-analysis` skill. This skill is about how measurement works on TTD specifically, not the shared math.

## Honest scope: what is public versus gated

Most of TTD's measurement help, the exact report names and columns, the data-feed schemas, and the field-level mechanics live behind the partner portal and require a TTD partner account and login. Treat the following as the rule, not the exception:

- **Public and citable:** the marketing-level description of measurement on the platform, the existence of a marketplace of independent measurement providers, the supported measurement approaches (multi-touch attribution, media mix modeling, brand lift, outcomes such as foot traffic and in-store sales), and first-party conversion-data integration. These come from TTD's public product pages and newsroom.
- **Gated, confirm in-platform:** exact in-platform report templates, dimension and metric names, attribution-window settings, brand-lift study minimums and provider lists, and the structure and field names of any log-level or raw event data feed. Do not invent these. When a user needs them, say plainly that they require TTD partner and platform access and point to the in-platform documentation.

When you are unsure whether a detail is public, assume it is gated and say so, rather than stating a specific report name, column, or number you cannot verify.

## When to use this skill

- "How does measurement work in The Trade Desk?" or "what can I measure on TTD?"
- "What is the TTD measurement marketplace?" or "which third-party measurement partners can I use?"
- "Set up attribution on TTD" or "multi-touch attribution vs media mix modeling on the platform."
- "Run a brand lift study on TTD" or "did the campaign move awareness or drive foot traffic?"
- "Can I get raw event data or log-level data from TTD for my own analysis?"
- "Pull a report from TTD" at the conceptual level (what is possible and how to think about it).

Boundaries with sibling skills:

- Programmatic API and the raw event data feed as an automation surface (auth, scheduling, safe-to-automate): the `ttd-api-and-automation` skill.
- What a good report looks like for a given objective: `reporting-by-campaign-goal`.
- Cross-DSP path-to-conversion thinking: `path-to-conversion-analysis`.
- Metric and KPI definitions and formulas: `programmatic-foundations`.

## Quick reference: match the method to the question

| Question | Approach on TTD | Public or gated |
| --- | --- | --- |
| Did users act after seeing the ad, against my own KPI? | Integrate first-party conversion data and measure outcomes in-platform | Public concept; exact setup gated |
| How is credit assigned across touchpoints? | Multi-touch attribution, or media mix modeling for top-down | Public concept; model config gated |
| Did the campaign change perception? | Brand lift study via a measurement provider | Public concept; minimums and providers gated |
| Did it drive real-world action (store visits, sales)? | Outcome measurement (foot traffic, in-store sales) via marketplace providers | Public concept; provider and method gated |
| Which measurement vendor should run it? | The marketplace of independent measurement providers | Marketplace is public; the directory is in-platform |
| Can I do my own modeling on event-level data? | Log-level / raw event data made available to partners | Existence is supportable; schema and access gated |

Rule of thumb, same as the rest of this library: pick the method by funnel stage and the business question, not by whatever data is easiest to pull. Lower-funnel goals are an attribution and outcome question; upper-funnel goals are a brand-lift question; planning and de-duplication are a reach question. See `reporting-by-campaign-goal` to turn the goal into a report.

## The four public pillars

### 1. In-platform reporting and attribution

TTD positions measurement as operational: you can see the entire path from impression to outcome inside the buying workflow and optimize against it mid-flight, rather than waiting for a wrap report. Publicly supportable points:

- **First-party conversion data.** You can integrate your own first-party conversion data to measure the outcomes you care about most. This is the backbone of performance measurement on the platform and what the AI optimizes toward when you set an outcome KPI.
- **Attribution approaches.** The platform supports integrating with your preferred measurement frameworks and models, including multi-touch attribution and media mix modeling, to support omnichannel measurement rather than relying on last-click alone. Use multi-touch when you have the touch-level data and want path-level credit; use media mix modeling for a top-down read across channels including offline.
- **What is gated.** The exact in-platform report builder, the named report templates, the available dimensions and metrics, and the attribution-window controls require platform access. Do not name a specific report or column you have not seen in the account. When asked for the precise setup, route the user to the in-platform documentation and their TTD representative.

For the difference between view-through and click-through and how lookback windows distort credit, see `programmatic-foundations` and the general guidance in `dv360-measurement-and-attribution`; the concepts carry across DSPs even though the controls differ.

### 2. The marketplace of independent measurement providers

TTD's public product page describes a marketplace of independent measurement providers you can tap into, alongside TTD's own measurement products, so you can prove impact across channels and choose a provider at each stage of the funnel.

- **What it is.** A managed marketplace inside the platform where you browse and request access to measurement solutions (third-party and first-party) rather than wiring up each vendor by hand. It gives buy-side choice and keeps measurement vendor-neutral.
- **Why it matters operationally.** You pick the measurement partner that matches the question (brand lift, foot traffic, sales, attention, verification) instead of being locked to one. Independent third-party measurement is also how brands satisfy agency and advertiser requirements for unbiased outcome verification.
- **What is gated.** The live provider directory, the exact list of partners, regional availability, and the request-access flow are in-platform. Do not assert which named vendors are present or absent for a given region or account. Confirm the current directory in the platform.

### 3. Brand lift and outcome measurement

For upper-funnel and real-world goals, TTD points to outcome measurement that goes beyond impressions and clicks.

- **Brand lift.** Measures whether exposure changed perception (awareness, consideration, favorability, intent, recall) by comparing exposed and control groups, typically run through a measurement provider in the marketplace. Use it when the objective is perception change and a conversion is not the outcome.
- **Outcomes.** TTD's public materials call out proving impact on outcomes that range from brand lift to foot traffic to in-store sales. These connect media to business results and are the right lens for retail, CPG, QSR, and other goals where the conversion happens offline.
- **Incrementality and modeling.** TTD frames measurement as understanding true incrementality across the customer journey rather than relying on last-click. Media mix modeling and multi-touch attribution are the supported ways to get there.
- **What is gated.** Study minimums (audience size and response thresholds), survey policy, the exact metrics each provider returns, and the configuration steps require platform and provider access. Apply the general brand-lift design discipline below, but do not quote TTD-specific numbers you cannot verify.

General brand-lift discipline that holds across DSPs (see `dv360-measurement-and-attribution` for the worked version): keep targeting broad enough to power the study, never retarget or exclude the control group, set frequency for reach, brand early in the creative, and treat "no measurable lift" as under-powered rather than proof of no effect.

### 4. Log-level and raw event data for advanced analysis

TTD makes event-level data available to partners so they can run their own analysis and modeling outside the in-platform reports. This is the foundation for custom measurement, joining ad exposure to first-party outcomes in a data warehouse, and feeding media mix or attribution models.

- **The supportable idea.** Beyond aggregated in-platform reporting, partners can access log-level or raw event data for advanced, privacy-conscious analysis. This is what custom measurement is built on: you bring the granular data into your own environment and model it.
- **What is gated, and strongly so.** The specific feed names, the schema, the columns, the delivery mechanism, the latency, the retention, and the access path are all partner-gated. Do not invent a feed name or a field name. State plainly that raw event data requires a TTD partner account and that the schema and access must be confirmed in the partner documentation and with the TTD representative.
- **Where automation lives.** Scheduling, authenticating, and pulling this feed programmatically is the job of the `ttd-api-and-automation` skill. This skill covers what the data is for; that skill covers how to move it safely.

## Decision rules

- **Goal is sales, leads, or a first-party KPI:** integrate first-party conversion data, measure the outcome in-platform, and choose multi-touch attribution when you have the touch-level data or media mix modeling for the top-down cross-channel read. Let the AI optimize toward the outcome rather than a proxy.
- **Goal is awareness, consideration, or recall:** run a brand lift study through a marketplace provider, protect the control group, and keep targeting broad enough to power it.
- **Goal is proving real-world action:** use outcome measurement (foot traffic, in-store sales) via a marketplace provider that matches the vertical.
- **Goal is custom modeling or a warehouse join:** plan around log-level / raw event data, and confirm the feed, schema, and access in the partner documentation before designing the pipeline. Hand the pull mechanics to `ttd-api-and-automation`.
- **You need exact report names, columns, windows, or provider lists:** stop and say these are partner-gated. Pull them from the in-platform documentation or the TTD representative rather than guessing.

## Common pitfalls

- **Stating a report name or metric you cannot verify.** TTD's report templates and columns are gated. Describe the capability, then route to in-platform docs. Never present a guessed report or field name as fact.
- **Naming specific measurement vendors as present.** The marketplace exists and is public; the directory is in-platform and regional. Confirm before claiming a given vendor is available.
- **Treating last-click as the answer.** TTD's whole measurement framing is incrementality and full-path outcomes. Reading only last-click undercuts the platform's strength and misallocates budget.
- **Inventing a raw-event-feed schema.** The existence of log-level data is supportable; its fields are not public. Do not fabricate columns or feed names. Confirm in the partner docs.
- **Quoting brand-lift minimums from memory.** TTD-specific thresholds are gated. Apply the general design discipline and verify numbers in-platform.
- **Optimizing on immature conversion data.** View-through and offline outcomes lag. A fresh "no conversions" read is usually incomplete; let the data mature before acting (see `programmatic-foundations`).

## Sources

- The Trade Desk, Measurement and Optimization (marketplace of independent measurement providers; multi-touch attribution and media mix modeling; first-party conversion data; outcomes from brand lift to foot traffic to in-store sales; path from impression to outcome): https://www.thetradedesk.com/our-demand-side-platform/advertising-campaign-performance-measurement (as of June 2026)
- The Trade Desk, Our Platform overview (measurement and optimization, identity, audiences, AI decisioning, retail data, OpenPath; outcome-based measurement across the funnel): https://www.thetradedesk.com/us/our-platform (as of June 2026)
- The Trade Desk launches Kokai (measurement framed inside the buying workflow; Partner Portal adapters for measurement and third-party audience data; retail measurement and benchmarking indices), June 2023: https://www.thetradedesk.com/press-room/the-trade-desk-launches-kokai-a-new-media-buying-platform-that-brings-the-full-power-of-ai-to-digital-marketing (as of June 2026)
- The Trade Desk announces major overhaul of digital advertising data marketplace (Audience Unlimited; AI scoring of third-party data segments from hundreds of providers), September 2025: https://investors.thetradedesk.com/news-and-events/news/news-details/2025/The-Trade-Desk-Announces-Major-Overhaul-of-Digital-Advertising-Data-Marketplace/default.aspx (as of June 2026)
- The Trade Desk press room (public newsroom index): https://www.thetradedesk.com/press-room (as of June 2026)

The Trade Desk's measurement help, the exact in-platform report templates, dimension and metric names, attribution-window controls, brand-lift study minimums and provider directory, and the schema and access path for any log-level or raw event data feed are documented on the partner portal and require a TTD partner account and login. They are described above at the publicly supportable level only. Where a user needs the exact names, columns, numbers, or feed schema, that detail requires TTD partner and platform access and must be confirmed in the in-platform documentation; this skill does not assume or invent it.

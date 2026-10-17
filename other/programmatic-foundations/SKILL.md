---
name: programmatic-foundations
description: The DSP-agnostic anchor for this library. Shared programmatic definitions, auction mechanics, and KPI math. Use when the user asks "what does CPM / CPA / VCR / win rate mean", wants the programmatic glossary, asks "how does the RTB auction work", "first-price vs second-price", "what is a PMP / deal ID / Floodlight", asks how to compute a metric (CPM, eCPM, ROAS, viewability rate), which KPI matters at which funnel stage, or "which skill should I use" for a DV360 task. Every other skill links here for definitions and formulas.
---

# Programmatic foundations

The shared base for the whole library. This is the single place where terms are defined,
auction mechanics are explained, and KPI math lives. Platform skills stay thin by linking
here instead of repeating definitions. Use it to settle "what does this term mean", "how is
this metric computed", and "which skill do I open for this task".

## When to use this skill

Reach for this skill when the question is conceptual, definitional, or about routing:

- A term needs a precise definition: DSP, SSP, exchange, RTB, OpenRTB, bid request, floor,
  deal ID, PMP, Programmatic Guaranteed, Preferred Deal, impression, viewable impression,
  reach, frequency, pacing, flight, IO, line item, working vs non-working media, brand safety
  vs brand suitability, IVT, GIVT, SIVT, Floodlight.
- A metric needs a formula or interpretation: CPM, CPC, CPA, CTR, CVR, VCR, CPCV, eCPM, ROAS,
  win rate, viewability rate, measurable rate.
- A concept needs explaining: how the auction works, first-price vs second-price, the
  viewability standard, the marketing funnel and the KPI for each stage.
- The user does not know which skill to open. Use the routing table below.

Hand off when the question is about doing something on the platform. This skill defines win
rate; `dv360-troubleshooting` fixes a bad one. This skill defines a bid strategy; choosing and
configuring one is `dv360-bid-strategy`. Define here, act there.

## Quick reference

| The user wants | Go to |
| --- | --- |
| A term defined | `references/glossary.md` |
| A KPI formula or what it means | `references/metrics.md` |
| The KPI for a funnel stage | Funnel model below, full table in `references/metrics.md` |
| To understand the RTB auction | "How the auction works" below |
| To know which DV360 skill to open | "Which skill do I use" routing table below |
| The trader / analyst / ops split | "Three hats" below |

## Core process

When a question lands here:

1. Classify it. Definition, formula, concept, or routing. This tells you which section or
   reference answers it.
2. For a definition, pull the exact wording from `references/glossary.md` rather than
   paraphrasing from memory, so the whole library stays consistent.
3. For a metric, give the formula and the one-line interpretation from `references/metrics.md`,
   and compute it if the user supplied numbers. State the unit and flag the per-mille factor
   on CPM and eCPM.
4. For routing, name the target skill from the table and hand off. Do not start solving the
   platform task inside this skill.
5. Tie the answer back to the user's objective. A number is only right or wrong relative to
   the funnel stage and goal it serves.

## How the auction works

The 100-millisecond path of one impression:

1. A user opens a page or app. The publisher's SSP packages the available ad slot into a
   bid request (slot size, position, site or app, allowed user and device signals, floor).
2. The SSP broadcasts that request to many DSPs over the OpenRTB protocol.
3. Each DSP evaluates the request against its active line items and decides whether to bid and
   how much. The trader's targeting, bid strategy, pacing, and frequency caps all resolve in
   this instant.
4. DSPs return bid responses (price, creative, any deal ID). The exchange runs the auction.
5. The highest bid that clears the floor wins. The winning creative serves and renders.

Two facts shape every downstream decision:

- **The open auction is first-price.** The winner pays exactly what they bid, so an
  overbid overpays on every win. Pacing and bid strategy exist to set the right price, not a
  loose ceiling. (Second-price, where the winner paid one cent over the runner-up, is largely
  historical for open auction but still appears in some explanations and legacy setups.)
- **A deal ID changes the venue, not the mechanics.** PMP, Preferred Deal, and Programmatic
  Guaranteed run over the same plumbing with a negotiated floor, priority, or guarantee
  attached to the ID. See `references/glossary.md` for each deal type and
  `dv360-deals-and-inventory` to set them up.

## Viewability standard

The MRC and IAB standard, implemented in Google Marketing Platform as Active View:

- **Display:** at least 50 percent of the ad's pixels in view for at least 1 continuous
  second.
- **In-stream video:** at least 50 percent of the ad's pixels in view for at least 2
  continuous seconds.
- **Large display (242,500 pixels or more, for example 970x250):** the threshold relaxes to
  30 percent of pixels for 1 second.

Served is not seen. Always read viewability rate next to measurable rate (the share of
impressions a vendor could measure at all); a strong viewability rate on a thin measurable
base means little. Both formulas are in `references/metrics.md`.

## Funnel model

Match the KPI to the objective. The single most common optimization error is judging a line
item by a metric from the wrong stage.

| Stage | What you are buying | Primary KPIs |
| --- | --- | --- |
| Awareness | Reach the right people at scale | Reach, CPM, viewability rate, VCR |
| Consideration | Earn interest and engagement | CTR, site visits, engagement |
| Conversion | Drive the action efficiently | CPA, ROAS, CVR |
| Retention | Keep and re-engage customers | Repeat conversion rate, CPA on retained segments |

Read the objective first; it names the primary KPI. Everything else is a guardrail (for
example viewability on an awareness buy) or a diagnostic. Full table with "what to ignore at
this stage" is in `references/metrics.md`.

## Three hats: trader, analyst, account ops

This library is organized around three jobs. The same person often wears all three, but the
mindset and the skills differ. Knowing which hat a task needs tells you which skills apply and
when work hands off.

- **Trader.** Builds and optimizes the buy. Owns campaign structure, bid strategy, targeting,
  deals, pacing, frequency, and brand suitability tuning. Question: "how do I deliver the
  goal efficiently?" Skills: `dv360-campaign-architecture`, `dv360-bid-strategy`,
  `dv360-targeting-and-audiences`, `dv360-deals-and-inventory`,
  `dv360-frequency-and-brand-safety`, `dv360-pacing-and-optimization`.
- **Analyst.** Measures, explains, and recommends. Owns reporting, attribution, advanced
  analysis, and the data behind custom bidding. Question: "what happened, why, and what
  should we do next?" Skills: `dv360-reporting`, `dv360-measurement-and-attribution`,
  `dv360-advanced-analytics-adh`, `dv360-custom-bidding`.
- **Account ops.** Structures, QAs, governs, and automates. Owns account setup and taxonomy,
  pre-launch QA, troubleshooting, and API and bulk-file automation. Question: "is it set up
  correctly, safely, and repeatably?" Skills: `dv360-account-setup-and-taxonomy`,
  `dv360-launch-qa`, `dv360-troubleshooting`, `dv360-api-and-sdf-automation`.

How they hand off:

1. Ops stands up the account and taxonomy, then hands a clean shell to the trader
   (`dv360-account-setup-and-taxonomy` to `dv360-campaign-architecture`).
2. The trader builds the campaign, then ops runs pre-launch QA and sign-off before anything
   goes live (`dv360-launch-qa`).
3. In flight, the analyst measures and the trader optimizes; a bad number routes to ops for
   troubleshooting (`dv360-reporting` and `dv360-pacing-and-optimization` to
   `dv360-troubleshooting`).
4. Recurring or large-scale changes move from manual trading to ops automation
   (`dv360-api-and-sdf-automation`).

## Which skill do I use

Route the user's question to the platform skill that owns it. When two could apply, pick by
the hat (build vs measure vs govern).

| The question is about | Open this skill |
| --- | --- |
| Partner, advertiser, campaign, IO, line item structure; when to split or merge | `dv360-campaign-architecture` |
| Fixed vs automated bidding, Target CPA / CPM / ROAS, maximize conversions or value, learning periods, why a line item is not winning | `dv360-bid-strategy` |
| First-party and Google audiences, audience combination, geo, device, contextual, viewability targeting | `dv360-targeting-and-audiences` |
| Open auction vs PMP vs Programmatic Guaranteed vs Preferred Deal, deal IDs, a deal not delivering | `dv360-deals-and-inventory` |
| Frequency caps, content and publisher exclusions, brand safety vs suitability, verification vendors | `dv360-frequency-and-brand-safety` |
| Pacing modes and math, under or over-delivery, impression loss diagnosis | `dv360-pacing-and-optimization` |
| Building reports, report types, the metric and dimension glossary, scheduling | `dv360-reporting` |
| Floodlight, Campaign Manager 360, attribution models, Brand Lift, reach and frequency studies | `dv360-measurement-and-attribution` |
| Ads Data Hub, privacy checks, BigQuery transfers, joining first-party data | `dv360-advanced-analytics-adh` |
| Rule-based, script, or Ads Data Hub custom bidding; scoring and staged rollout | `dv360-custom-bidding` |
| Account and advertiser setup, naming conventions, roles and permissions, governance | `dv360-account-setup-and-taxonomy` |
| Pre-flight QA checklist and sign-off before launch | `dv360-launch-qa` |
| No delivery, pacing, win rate, viewability, creative, or conversion problems in flight | `dv360-troubleshooting` |
| DV360 API, Structured Data Files, what is safe to automate | `dv360-api-and-sdf-automation` |

The table above is DV360. For Google Ads, Amazon DSP, StackAdapt, or The Trade Desk, the same
questions map to that platform's skills (the `google-ads-*`, `amazon-dsp-*`, `stackadapt-*`, and
`ttd-*` sets). Cross-platform work has its own skills: `dsp-selection` to choose a platform,
`reach-and-frequency-planning` for deduplicated reach across platforms,
`incrementality-and-experimentation` to prove lift, and `client-deliverable-templates` for
client-facing plans and reviews.

If the question is conceptual or definitional rather than a platform task, answer it here.

## Reference material

- `references/glossary.md`: the full glossary. Read it when a term needs a precise, canonical
  definition (the marketplace, deals, counting and reach, plan structure, safety and IVT,
  Floodlight).
- `references/metrics.md`: every KPI and auction formula with interpretation, the full funnel
  table with "what to ignore at each stage", and worked numeric examples. Read it when you
  need to compute or explain a metric.

## Common pitfalls

- **Judging a stage by the wrong KPI.** CPA on an awareness buy, or reach on a conversion
  buy. Anchor every metric to the funnel stage in `references/metrics.md`.
- **Treating served as seen.** Report viewable impressions and viewability rate for visibility
  goals, never raw impressions, and always alongside measurable rate.
- **Forgetting first-price.** On open auction the bid is the price paid, not a ceiling. An
  overbid overpays on every win.
- **Confusing brand safety with brand suitability.** Safety is the universal hard floor;
  suitability is the advertiser-specific layer. Conflating them over-blocks and loses scale.
- **Reading win rate without bid rate.** Win rate is wins over bids submitted, not over
  requests seen. A high win rate on few bids is not scale.
- **Comparing line items on different buy models directly.** Convert each to eCPM first.

## Sources

- Media Rating Council, Standards and Guidelines (viewable ad impression measurement
  guidelines): https://www.mediaratingcouncil.org/standards-and-guidelines (as of June 2026)
- Google Ad Manager Help, Active View viewability (display 50 percent for 1 second, video 50
  percent for 2 seconds): https://support.google.com/admanager/answer/4524488 (as of June 2026)
- Display & Video 360 Help, About Active View:
  https://support.google.com/displayvideo/answer/3214556 (as of June 2026)
- Display & Video 360 Help, Automated bid strategies:
  https://support.google.com/displayvideo/answer/2997422 (as of June 2026)
- Display & Video 360 Help, Overview of deals:
  https://support.google.com/displayvideo/answer/7243138 (as of June 2026)
- Display & Video 360 Help, About Floodlight and Floodlight activities:
  https://support.google.com/displayvideo/answer/3027419 (as of June 2026)
- Display & Video 360 Help home: https://support.google.com/displayvideo (as of June 2026)
- IAB Tech Lab, OpenRTB specification: https://iabtechlab.com/standards/openrtb/ (as of June 2026)
- IAB, standard terms and definitions for the advertising industry:
  https://www.iab.com/blog/iab-unites-the-industry-with-new-standard-terms/ (as of June 2026)

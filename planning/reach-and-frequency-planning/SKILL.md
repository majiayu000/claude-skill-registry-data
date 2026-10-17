---
name: reach-and-frequency-planning
description: Plan and read deduplicated reach and frequency across DSPs and channels. Use when the user asks about "reach and frequency", "effective frequency", "deduplicated reach", "cross-platform reach", "frequency cap planning", "the reach curve", "diminishing reach", "co-viewing", "1+ 2+ 3+ reach", "average frequency vs frequency distribution", or "how many people did we actually reach" across multiple platforms. Covers the math, why platform reach is non-additive and must never be summed, the identity fragmentation that makes cross-walled-garden frequency capping best-effort, and a triangulation method for one deduplicated number.
---

# Reach and frequency planning

Plan how many distinct people a campaign reaches, how often each sees it, and how to get one honest deduplicated number when the buy spans several DSPs and channels. This skill owns the cross-platform reach problem: the math, the identity limits, and the triangulation method. For base definitions of reach, frequency, and impression counting, see the `programmatic-foundations` skill. For pulling and reading one platform's native reach report inside Display & Video 360, see the `dv360-measurement-and-attribution` skill. For matching a reach report to a campaign objective, see the `reporting-by-campaign-goal` skill.

## When to use this skill

- "What is our deduplicated reach across DV360, The Trade Desk, and Amazon?"
- "How do I set a frequency cap across platforms?" or "why does my cross-platform cap leak?"
- "What is effective frequency for this campaign?" or "are we over-frequencying?"
- "Read me the reach curve" or "we added budget and reach barely moved, why?"
- "Average frequency vs 1+/2+/3+ reach, which should I report?"
- "Does co-viewing on connected TV inflate our frequency?"
- "How many people did we actually reach?" when more than one platform ran the flight.

Boundary. If the question is "what does reach or frequency mean", that is `programmatic-foundations`. If it is "pull the Reach report in this platform" or "what are the reach report constraints", that is the platform measurement skill (`dv360-measurement-and-attribution` for DV360). If it is "is this exposure causing the outcome", that is incrementality, see the `incrementality-and-experimentation` skill. This skill plans the reach target and reconciles reach across platforms; it does not run the buy or prove causality.

## Quick reference

| The user wants | Do this |
| --- | --- |
| One deduplicated reach number across platforms | Triangulate (see Core process). Never sum native reach reports. |
| To know if a frequency cap is realistic | Run the audience-times-cap feasibility check, `tools/frequency_delivery_check.py` |
| To set effective frequency | Anchor to the effective-frequency band for the goal (see Decision rules) |
| To report reach the right way | Lead with 1+ reach and the frequency distribution, not average frequency alone |
| To explain flat reach on added budget | Show the reach curve and diminishing marginal reach |
| A cross-platform frequency cap | Set it as best-effort on a shared identity spine; per-platform caps cannot see each other |
| True per-person CTV frequency | Adjust for co-viewing; one impression can be two or more viewers |

Rule of thumb: reach is non-additive. The moment two platforms run the same flight, their reach numbers overlap by an unknown amount, and adding them double-counts every shared person. Deduplicate or triangulate, never sum.

## The math and concepts

Carry these as working models, not trivia. Each one drives a planning decision.

- **Reach versus frequency tradeoff.** A fixed budget buys a fixed number of impressions. Impressions equal reach times average frequency, so for a given impression pool, reach and frequency trade directly against each other. Raise the frequency cap and you concentrate impressions on fewer people; lower it and you spread to more. Decide which the goal needs before you set the cap.
- **The reach curve and diminishing marginal reach.** Plot unique reach against impressions (or spend) and the curve rises fast, then flattens. Early impressions land on new people; later impressions increasingly hit people already reached. The flattening is diminishing marginal reach. It is why doubling budget never doubles reach, and why "add budget" stops buying incremental people once the curve bends. When reach goes flat against rising spend, you are paying for frequency, not reach. Widen targeting or add inventory to find new people, or accept that you have saturated the addressable audience.
- **Effective frequency and the effective-frequency band.** Effective frequency is the number of exposures needed before the ad does its job (recall, consideration, action). It is a band, not a point: too few exposures and the message does not register, too many and you waste impressions and risk fatigue. Plan to land most reached people inside the band, not to hit one average number. The band depends on goal, creative, category, and recency; treat any single published value as a starting assumption to validate with lift, not a law.
- **Frequency distribution (1+, 2+, 3+) versus average frequency.** Average frequency is impressions divided by reach. It hides the shape. A 3.0 average can mean almost everyone saw the ad three times, or half saw it once and a few saw it twenty times. The frequency distribution (the share of reached people at 1+, 2+, 3+, ... exposures) shows the truth. Plan and report on the distribution against the effective-frequency band. Average frequency alone is a vanity number that masks both under-exposed reach and over-frequencied waste.
- **Co-viewing on connected TV inflates true per-person frequency.** On CTV, more than one person often watches a single impression on a shared screen. Per-impression frequency math counts that as one exposure to one person, so it understates how many distinct people were reached and overstates per-person frequency unless the source models co-viewing. When a measurement source reports co-viewed reach, true reach is higher and true per-person frequency is lower than the raw impression-per-device math implies. Always note whether a CTV reach number is co-view-adjusted; an unadjusted number is not comparable to a co-view-adjusted one.

## The cross-platform problem

This is the core of the skill. Three facts govern everything.

- **Each platform's reach is non-additive.** A reach report is deduplicated only inside its own walls, against that platform's identity graph and the cookies, mobile IDs, and sign-in data it can see. Two platforms running the same audience overlap by an unknown amount, so their reported reach figures share people. Summing them counts every shared person twice. There is no arithmetic that recovers the true union from two walled numbers alone; you need a neutral source that sees both. Never add platform reach numbers, and never let a deck add them for you.
- **Identity fragmentation makes cross-walled-garden frequency capping best-effort.** Third-party cookies are gone in the open web, so the cross-site key that once linked exposures across sellers is unavailable. Mobile advertising IDs are limited by per-OS opt-in and are not present in many requests. Connected TV uses device IFAs that differ by device and platform and are often unavailable or reset. Most platforms cap and measure at the household or device level, not the individual, so "frequency per person" is already an approximation before any cross-platform join. The consequence: a frequency cap inside one platform is enforceable, but a cap across platforms can only be approximated by resolving exposures to a shared identity spine that every participating platform can map to. Treat cross-platform caps as best-effort, set per-platform caps deliberately so their sum is not absurd, and verify total frequency after the fact with a deduplicated source.
- **What you can and cannot deduplicate today.** Be honest about this with the user.

| Scenario | Deduplication today | How |
| --- | --- | --- |
| Within one DSP, across devices and channels | Yes, modeled | The platform's native reach report (deduplicated inside its walls) |
| Across DSPs that share an identity spine (for example a common UID2 or RampID footprint) | Partial, best-effort | Resolve exposures to the shared identifier, then dedupe on it |
| Across walled gardens (for example a self-attributing platform and an open-web DSP) | No direct join | Neutral panel or a clean room each platform feeds; never a direct ID match |
| Digital plus linear TV | Partial, modeled | A cross-media reach methodology that blends licensed third-party TV data with digital |
| Two reach reports from two platforms, added together | Never | This double-counts shared people; the number is wrong by construction |

## Core process

When the task is "how many people did we actually reach" or "set a cross-platform plan":

1. State the unit and the question. Individuals or households? In-market reach target, or a frequency cap to enforce? CTV in the mix (then co-viewing matters)? The wrong unit makes every later number unreadable.
2. Set the reach and frequency target from the goal. Pick the effective-frequency band for the objective (see Decision rules), then derive the reach the budget can support at that frequency. Reach equals impressions divided by the average frequency you are planning toward, and impressions equal budget divided by CPM times 1000.
3. Check that the frequency cap can deliver. Before committing, run the audience-times-cap feasibility check in `tools/frequency_delivery_check.py`. The most a capped buy can deliver is reachable audience times the cap; if required impressions exceed that, the cap or the audience will starve delivery no matter the bid. Raise the cap, widen the audience, or lower the impression target.
4. Pull each platform's native reach report. Get deduplicated, in-walls reach and the frequency distribution from every platform that ran the flight. For DV360 this is the Reach report and Cross-Media Reach reporting, covered in the `dv360-measurement-and-attribution` skill. For other DSPs, use that platform's reach report from its measurement skill (for example `ttd-measurement-and-reporting`, `amazon-dsp-measurement-and-reporting`, `stackadapt-reporting-and-attribution`).
5. Deduplicate across platforms with a neutral spine, never by adding. Pick one mechanism: a neutral panel measurement provider that sees all channels, a clean room each platform feeds so the union is computed on matched events, or an identity spine (UID2, RampID, or hashed email) that every platform can map exposures to. For event-level overlap on Amazon, see the `amazon-marketing-cloud` skill. For the UID2 footprint and how exposures resolve to it, see the `ttd-identity-and-uid2` skill.
6. Report the union, the overlap, and the distribution. Give one deduplicated reach number, the cross-platform overlap it removed, and the 1+/2+/3+ distribution against the effective-frequency band. Flag any CTV reach as co-view-adjusted or not. State the method and its confidence; a triangulated number is an estimate, label it as one.

## Decision rules and thresholds

- **Never sum reach across platforms or across report rows.** Deduplicated reach is not additive across platforms, days, or segments. If you need a total, triangulate it. This is the single rule that prevents the most common and most embarrassing reach error.
- **Lead with 1+ reach and the frequency distribution; treat average frequency as a guardrail only.** Report the distribution against the band. Use average frequency only as a quick gut check, never as the headline.
- **Pick the effective-frequency band by goal, then validate with lift.** As planning starting points to validate, not as fixed truth: a small number of exposures (roughly 1 to 3 in a window) is a reasonable opening assumption for direct response and retargeting where one or two exposures can drive the action; a mid-single-digit band (roughly 3 to 5, sometimes higher) is a common opening assumption for awareness and consideration where repetition builds memory. New brands and complex messages sit at the higher end; familiar brands and simple messages at the lower end. Confirm the real band with a Brand Lift or incrementality read rather than asserting a published number, see the `dv360-measurement-and-attribution` and `incrementality-and-experimentation` skills.
- **When reach goes flat against rising spend, stop buying frequency by accident.** A bending reach curve means added budget is hitting reached people again. Decide deliberately: more frequency is the goal (keep going), or it is not (widen targeting, add inventory, or shift budget to a channel with fresh reach).
- **Set per-platform caps so their uncoordinated sum is sane.** Platforms cannot see each other's caps. If three platforms each cap at 5 per week on the same audience, a person on all three can see 15. Split the intended total across platforms, weighted by each platform's reach contribution, and reconcile actual total frequency after the fact with a deduplicated source.
- **Treat household and individual as different currencies.** Most CTV and many cross-device caps operate at the household level. Do not compare a household frequency to an individual frequency, and tell the user which one a number is.
- **Label every CTV reach number as co-view-adjusted or not.** An unadjusted CTV reach understates people and overstates per-person frequency. Mixing adjusted and unadjusted numbers in one plan is meaningless.

## Reference material

- `tools/frequency_delivery_check.py` (bundled with this library): the audience-times-cap feasibility check. Run it before committing a frequency cap to confirm the cap and audience can deliver the impressions the plan needs. Example: `python3 tools/frequency_delivery_check.py --audience 500000 --freq-cap 10 --budget 30000 --cpm 6`.
- `programmatic-foundations`: base definitions of reach, frequency, impression, and viewable impression, and the funnel-to-KPI map.
- `dv360-measurement-and-attribution`: DV360 Reach reports, unique reach, co-viewing metrics, and Cross-Media Reach mechanics and constraints.
- `reporting-by-campaign-goal`: which reach and frequency view to present for each campaign objective.
- `amazon-marketing-cloud` and `ttd-identity-and-uid2`: the clean-room and identity-spine routes for cross-platform deduplication.

## Templates and examples

**Deriving the reach target from a budget.** Budget 30,000 USD, CPM 6 USD, planning average frequency 4 for an awareness goal. Impressions = 30,000 / 6 x 1000 = 5,000,000. Planned reach = 5,000,000 / 4 = 1,250,000 people. Now sanity-check the cap: if the addressable audience is only 800,000, a frequency cap of 4 caps total deliverable at 3,200,000 impressions, short of the 5,000,000 the budget buys, so the plan will over-deliver frequency or under-spend. Run `frequency_delivery_check.py --audience 800000 --freq-cap 4 --budget 30000 --cpm 6` to confirm and decide: raise the cap, widen the audience, or cut budget.

**Reporting cross-platform reach honestly.** Three platforms ran the flight. Native reports: DV360 900k, a second DSP 600k, a self-attributing platform 500k. Wrong: 900k + 600k + 500k = 2.0M reach (this double-counts everyone who appears in more than one). Right: a clean room matched exposures across all three and returned a union of 1.45M deduplicated people, meaning 550k of person-overlap was removed; the 2+ frequency share was 62 percent, inside the 3 to 5 band intent only at the top decile. Report: "1.45M deduplicated reach (estimate, clean-room matched), 550k overlap removed; average frequency 3.4 but distribution shows 38 percent reached only once, so consider shifting budget to lift the under-exposed tail."

**Explaining flat reach.** "Spend rose 40 percent week over week but unique reach rose 4 percent. The reach curve has bent: we have saturated the current audience, so new impressions are landing on people already reached. To buy incremental reach, widen the audience or add fresh inventory; otherwise the added budget is buying frequency, which only helps if we are still below the effective-frequency band."

## Common pitfalls

- **Summing platform reach reports.** The number is wrong by construction because shared people are counted once per platform. Triangulate or do not state a cross-platform total.
- **Reporting average frequency as the headline.** It hides both under-exposed reach and over-frequencied waste. Lead with the distribution.
- **Promising a hard cross-platform frequency cap.** Identity is fragmented; cross-walled-garden capping is best-effort. Set per-platform caps so their sum is sane and reconcile after the fact.
- **Ignoring co-viewing on CTV.** Unadjusted CTV reach understates people and overstates per-person frequency. Always state whether a number is co-view-adjusted.
- **Mixing household and individual frequency.** They are different currencies. Comparing them produces nonsense.
- **Treating a published effective-frequency number as proven for this campaign.** Bands shift by goal, creative, category, and recency. Use a published value as a starting assumption and confirm with lift.
- **Reading a single-platform reach report as the campaign's total reach.** It is deduplicated only inside that platform's walls. If other platforms ran, that report undercounts the union and ignores cross-platform overlap.

## Sources

- Media Rating Council, Standards and Guidelines (lists the Cross-Media Audience Measurement Standard, the Digital Audience-Based Measurement Standard, and the Audience Reach Measurement Guidelines): https://www.mediaratingcouncil.org/standards-and-guidelines (as of June 2026)
- IAB, Audience Reach Measurement Guidelines (measuring uniques, machine-based versus people-based measures): https://www.iab.com/guidelines/audience-reach-measurement-guidelines/ (as of June 2026)
- IAB, Guidelines hub: https://www.iab.com/guidelines/ (as of June 2026)
- IAB Tech Lab, CTV Programmatic Guide (audience targeting, identifiers and IFA on CTV, clean rooms for audience matches, measurement and verification): https://iabtechlab.com/standards/advanced-tv/ctv-programmatic-guide/ (as of June 2026)
- Display & Video 360 Help, Reach reports (unique reach across devices, average impression frequency, co-viewing for connected TV, deduplication using cookies, mobile device IDs, and aggregated sign-in data, 93-day window): https://support.google.com/displayvideo/answer/6170584 (as of June 2026)
- Display & Video 360 Help, Cross-Media Reach reporting (incremental and deduplicated reach across digital, CTV, and third-party TV data; spend and impressions sum, reach does not): https://support.google.com/displayvideo/answer/13955444 (as of June 2026)
- Unified ID 2.0 documentation, Overview (deterministic identity framework for the open internet, used to activate first-party data across publishers and platforms): https://unifiedid.com/docs/intro (as of June 2026)
- LiveRamp, Identity resolution and RampID (interoperable, durable people-based identifier connecting identity across the ecosystem for cross-platform activation and measurement): https://liveramp.com/our-platform/identity-resolution/ (as of June 2026)

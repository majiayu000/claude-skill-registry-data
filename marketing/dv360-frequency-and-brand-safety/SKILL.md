---
name: dv360-frequency-and-brand-safety
description: Set frequency caps and configure brand safety, suitability, viewability, and invalid-traffic controls in DV360. Use when the user asks about frequency caps, how many impressions per user, exposure limits, brand safety, brand suitability, content exclusions, digital content labels, sensitive category exclusions, publisher or app or URL exclusion lists, keyword exclusions, DoubleVerify or IAS, third-party verification, pre-bid avoidance segments, viewability targeting, Active View, MRC viewability, or invalid traffic (GIVT, SIVT, IVT).
---

# DV360 frequency, brand safety, and verification

Control how often a user sees an ad and where the ad runs. Frequency capping protects reach efficiency. Brand safety, suitability, viewability, and invalid-traffic controls protect the spend and the brand. This skill encodes where each control lives, which level to set it at, and how to avoid paying twice for the same protection.

For shared definitions (CPM, viewability, the MRC viewable standard, the awareness-to-retargeting funnel), see the `programmatic-foundations` skill. This skill encodes the DV360-specific settings and decision rules.

## When to use this skill

Use when the user wants to:

- Set or change a frequency cap, or reason about exposures per user.
- Decide caps by funnel stage (awareness vs retargeting).
- Configure brand safety or brand suitability: digital content labels, sensitive category exclusions, content theme exclusions, inventory source exclusions, publisher/app/URL exclusion lists, keyword or category exclusions.
- Add DoubleVerify or IAS pre-bid avoidance segments, or decide between pre-bid avoidance and post-bid measurement.
- Set viewability (Active View) targeting or interpret viewability measurement.
- Understand invalid traffic (GIVT vs SIVT) and how DV360 filters it.

Boundary with sibling skills:

- For audience targeting, geo, device, and contextual targeting mechanics, use `dv360-targeting-and-audiences`. Viewability and IVT overlap; this skill owns the brand-safety and quality lens, that skill owns audience construction.
- If a line item is not delivering because filters are too strict, diagnose pacing and impression loss in `dv360-pacing-and-optimization`, then return here to loosen a specific control.
- For ordered no-delivery and low-win-rate playbooks, hand off to `dv360-troubleshooting`.

## Quick reference

| Goal | Control | Where to set it |
| --- | --- | --- |
| Limit exposures per user | Frequency cap | Insertion order and line item |
| Block universally objectionable content | Brand safety: digital content labels, sensitive categories | Advertiser brand controls and line item |
| Align inventory to brand tone | Brand suitability: content theme exclusions, tiers | Advertiser brand controls and line item |
| Drop specific sites or apps | Inventory source exclusion, channel/URL/app exclusion, exclusion lists | Line item targeting (or advertiser-level lists) |
| Drop content matching words | Negative keyword targeting | Advertiser, campaign, insertion order, or line item |
| Avoid risky inventory pre-auction | DoubleVerify or IAS pre-bid avoidance segment | Line item targeting (or IO default targeting) |
| Measure quality after the bid | Third-party verification tag | Creative or measurement setup |
| Bid only on likely-viewable inventory | Active View viewability targeting | Insertion order or line item |
| Filter bots and fraud | Google IVT filtration (automatic) plus third-party | Automatic; verify in reporting |

## Core process

1. **Set the frequency cap at the right level first.** The insertion order cap is the ceiling for all its line items, the same way the IO budget caps line item spend. Set the strategic cap (the one the brand cares about) at the IO so it cannot be exceeded by any line item, then use line item caps only to go tighter for a specific tactic. A cap is `exposures` per `time period`. Time periods run from per-day up to longer windows. Lifetime caps were deprecated after February 28, 2025; the maximum window is now 30 days, so model "lifetime" intent as a 30-day cap plus campaign flight dates.

2. **Choose caps by funnel stage.** Awareness needs reach, so cap lighter to let more unique users in. Retargeting hits a small, known pool repeatedly, so cap tighter to avoid burning the same users and wasting spend on diminishing returns. See Decision rules for starting numbers.

3. **Set brand safety and suitability at the advertiser level, then exceptions at the line item.** Advertiser brand controls apply to every current and future campaign, insertion order, and line item under that advertiser and cannot be loosened below them at lower levels. Put the floor (the controls the brand requires everywhere) at the advertiser. Tighten further per line item when a specific buy needs it. This is the leverage point: one advertiser-level change protects the whole account.

4. **Exclude inventory with the cheapest tool that does the job.** Native DV360 exclusions (digital content labels, sensitive categories, content themes, inventory source exclusion, negative keywords, channel/URL/app exclusion lists) cost nothing extra. Reach for a paid third-party segment only when you need a control DV360 does not offer natively or a specific accredited vendor the client mandates.

5. **Decide pre-bid avoidance vs post-bid measurement, and do not pay for both on the same control.** Pre-bid avoidance (a DoubleVerify or IAS segment added in targeting) stops you bidding on inventory that fails the rule, so you never pay for the bad impression. Post-bid measurement (a verification tag) reports quality after delivery but does not prevent the buy. If you already enforce a category pre-bid, do not also pay a post-bid fee to measure the same category. Use pre-bid to control spend, post-bid only to verify or to satisfy a measurement contract.

6. **Use Active View viewability targeting to bid only on likely-viewable inventory, knowing it shrinks reach.** Set a predicted viewability threshold (for example 50% or greater) on the line item or IO. Higher thresholds match far less inventory and can starve pacing, so raise the threshold only as far as the viewability goal requires and watch impression loss. Mobile-app impressions that are not measurable for Active View should not be viewability-targeted, because no inventory qualifies.

7. **Treat invalid traffic as filtered by default, then verify.** DV360 removes invalid traffic pre-bid (never bought) or post-serve (credited back), across General Invalid Traffic and Sophisticated Invalid Traffic, with an added HUMAN integration that needs no configuration. You do not configure GIVT/SIVT filtration; you confirm it in reporting and add third-party verification only when a client requires an independent number.

## Decision rules and thresholds

- **Frequency cap starting points (tune with reach and frequency reporting):**
  - Awareness / upper funnel: roughly 2 to 3 per day, or a weekly cap, to maximize unique reach.
  - Consideration / mid funnel: roughly 3 to 5 per week.
  - Retargeting / lower funnel: a tight total cap, for example 3 to 5 over the campaign window (modeled as a 30-day cap plus flight dates), so a known user is not over-served.
  - Set the binding cap at the IO. Add a line item cap only to go tighter, never expecting it to raise the IO ceiling.

- **Cross-environment and cross-device capping is signal-limited.** Capping holds within an environment when a stable identifier exists. Across devices and environments it depends on available identifiers (for example IFA on connected TV, device or publisher-provided IDs in apps); impressions without a usable identifier fall outside the cap. Do not promise a hard cross-device cap. Treat the cap as best-effort across environments and tighten per-environment caps if over-exposure shows up in reporting.

- **Brand safety vs brand suitability.** Brand safety blocks content almost every advertiser rejects (the floor). Brand suitability tailors inventory to one brand's tolerance (the dial). Set the safety floor account-wide; tune suitability by campaign tone.

- **Digital content labels.** Exclude maturity tiers above the brand's tolerance (labels run from general audiences through families, parental guidance, teen, and mature; some inventory is not yet labeled). Excluding mature tiers is the common floor. Excluding too aggressively, including unlabeled inventory, can sharply cut scale.

- **Viewability threshold.** Match the threshold to the KPI. If the goal is a viewability rate, set predicted viewability near it, not far above, or you sacrifice reach and pacing for marginal viewability gain. Verify delivered viewability with measurement, since predicted is not guaranteed.

- **Do not stack duplicate controls.** One pre-bid avoidance source per risk category is enough. Layering DV360 native exclusions, a DoubleVerify segment, and an IAS segment on the same risk wastes fees and can over-filter into under-delivery.

## Reference material

- `references/brand-safety-controls.md`: full digital content label tiers, the sensitive category list, content theme exclusions, inventory source and exclusion-list mechanics, and the advertiser-vs-line-item control matrix. Read this when configuring exclusions in detail or auditing an advertiser's brand controls.
- `references/verification-and-viewability.md`: DoubleVerify and IAS pre-bid vs post-bid behavior, the Oracle Moat sunset note, Active View targeting limits, and the MRC-accredited viewability and IVT metric notes. Read this when choosing a verification vendor or interpreting viewability and IVT numbers.

## Templates and examples

**Awareness line item, three markets.** IO frequency cap 3 per day (the binding strategic cap). Advertiser brand controls exclude mature digital content labels and the sensitive categories the brand rejects. No paid pre-bid segment, native exclusions suffice. Active View targeting off or low, since awareness prioritizes reach over guaranteed viewability.

**Retargeting line item.** IO cap modeled as 4 exposures per 30 days plus tight flight dates, so a converted-intent user is not over-served. Inherit the advertiser brand-safety floor. Add one negative keyword list for terms the brand never wants nearby. Skip a second paid verification layer; the native floor plus the cap is the control.

**Premium-brand video buy with a mandated vendor.** Advertiser-level brand suitability set to the stricter tier. Add the client-mandated DoubleVerify or IAS pre-bid avoidance segment in line item targeting for the categories the contract names. Active View predicted viewability set to the contracted rate, not higher. Post-bid verification tag only because the contract requires an independent measured number, not to re-block what the pre-bid segment already blocks.

## Common pitfalls

- Setting the strategic frequency cap only at the line item, so another line item in the same IO re-exposes the same user. Put the ceiling at the IO.
- Promising a hard cross-device frequency cap. It is signal-limited; state it as best-effort.
- Treating "lifetime" as available. It is capped at 30 days now; pair a 30-day cap with flight dates.
- Loosening brand controls at the line item and expecting it to work. Advertiser-level controls are a floor lower levels cannot drop below.
- Paying for pre-bid avoidance and post-bid measurement on the same risk category. Pick pre-bid to control spend; add post-bid only for independent measurement.
- Setting predicted viewability far above the KPI and then filing an under-delivery ticket. High viewability targeting shrinks inventory; check impression loss in `dv360-pacing-and-optimization`.
- Adding redundant third-party segments on top of native exclusions, over-filtering into under-delivery.

## Sources

- Manage frequency with frequency caps: https://support.google.com/displayvideo/answer/2696786 (as of June 2026)
- Brand suitability: https://support.google.com/displayvideo/answer/3032915 (as of June 2026)
- Digital content labels in Display & Video 360: https://support.google.com/displayvideo/answer/2735881 (as of June 2026)
- Sensitive categories in Display & Video 360 brand safety targeting: https://support.google.com/displayvideo/answer/6327207 (as of June 2026)
- Inventory source targeting: https://support.google.com/displayvideo/answer/2726009 (as of June 2026)
- Keyword targeting: https://support.google.com/displayvideo/answer/2697825 (as of June 2026)
- About Integral Ad Science's media quality verification: https://support.google.com/displayvideo/answer/3297897 (as of June 2026)
- Viewability targeting: https://support.google.com/displayvideo/answer/6101342 (as of June 2026)
- Media Rating Council (MRC) accredited metrics: https://support.google.com/displayvideo/answer/7620594 (as of June 2026)
- Filtering invalid traffic to ensure quality: https://support.google.com/displayvideo/answer/6076504 (as of June 2026)

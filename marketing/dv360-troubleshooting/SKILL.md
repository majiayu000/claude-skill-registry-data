---
name: dv360-troubleshooting
description: Diagnose and fix a Display & Video 360 line item that is not performing. Use when the user says a line item is "not delivering", "no impressions", "zero spend", "underpacing", "overpacing", "low win rate", "low viewability", "creative disapproved" or "not serving", "no conversions", "low CTR", "a deal is not delivering", or asks "why is my line item broken". Walk the triage flow first, then the matching symptom playbook.
---

# DV360 troubleshooting

Ordered playbooks for the most common Display & Video 360 delivery and performance failures. The goal is to find the single binding constraint fast, fix it, and avoid the trap of changing five settings at once and learning nothing.

For KPI definitions, auction mechanics, and the impression-loss model, see the `programmatic-foundations` skill. This skill assumes you know what win rate, viewable rate, and pacing mean and tells you what to check, in what order, when one of them is wrong.

## When to use this skill

Use it when a campaign is live and a metric is wrong:

- No delivery, zero impressions, or zero spend on a line item or insertion order.
- Underpacing (will not finish the flight) or overpacing (will exhaust budget early).
- Low win rate, low viewability, low CTR or engagement, or low or no conversions.
- A creative is disapproved, rejected, or "not serving".
- A deal (PMP, Programmatic Guaranteed, Preferred Deal) is not delivering.

Boundaries with sibling skills:

- Choosing or tuning pacing modes and the pacing math: `dv360-pacing-and-optimization`.
- Choosing or fixing a bid strategy, learning periods, Target CPA or ROAS: `dv360-bid-strategy`.
- Frequency cap design, content and publisher exclusions, viewability and IVT standards: `dv360-frequency-and-brand-safety`.
- Deal setup, activation, and the full non-delivery deal tree: `dv360-deals-and-inventory`.
- Report types, metrics, and how to pull the numbers you need to diagnose: `dv360-reporting`.
- Floodlight, attribution windows, and conversion plumbing: `dv360-measurement-and-attribution`.

This skill is the entry point. It routes to those skills when the fix lives there.

## Quick reference: triage flow

Always run this top-down. Each step gates the next, so a problem high in the list masks everything below it. Do not jump to bids or creative before confirming status, budget, and flight.

1. **Status.** Is the line item, its insertion order, its campaign, and the advertiser all active and not paused, ended, or archived? Is the creative assigned and approved? A paused parent stops everything under it.
2. **Budget and flight.** Is today inside the flight dates? Is there unspent budget in the current pacing period? Has the insertion order cap been hit by sibling line items?
3. **Bid and win rate.** Is the bid above the floor for the inventory targeted? Is win rate plausible for the strategy, or is everything lost in the auction or below the minimum bid?
4. **Targeting size.** Is the addressable pool large enough after every targeting layer is intersected? Over-narrow targeting is the most common silent killer.
5. **Inventory or deal.** Is there matching open-auction supply, and for a deal, is the deal active, mapped, and prioritized so it can win?
6. **Creative.** Is a creative eligible (approved or servable), the right size and format for the inventory, and compatible with the line item type?
7. **Tracking.** If delivery is fine but conversions are missing, the fault is usually measurement, not delivery: Floodlight tags, attribution window, or the conversion column you are reading.

Run the official Troubleshooter on the line item to see where bids were filtered (by line item settings, creative requirements, or the auction), and read the Impressions lost chart to see which constraint is binding. Most data in that view is available within about one hour.

## The impression-loss model

When a line item delivers below plan, frame it as impressions lost to a specific cause, then fix that cause. DV360 reports impression loss in these official buckets:

- **No eligible creative.** No approved creative is assigned, so nothing can serve.
- **Frequency limited.** The frequency cap is reached, so no more impressions can be bought for capped users.
- **Below minimum bid.** The bid is under the floor price for the targeted inventory.
- **Budget or pacing.** The flight budget or the current pacing period budget is exhausted.
- **Auctions lost.** Lost to other line items inside DV360 (internal auction) or to other buyers on the exchange (external auction).

Brand safety, invalid traffic, and unauthorized-seller filters show up as prebid filtering in the deals and line items Troubleshooter rather than as an impression-loss bucket. Viewability is a delivery-quality metric, not an impression-loss bucket. Diagnose the bucket that is largest first, because shrinking a small bucket changes nothing.

## Symptom playbooks (summaries)

Each symptom has a full ordered playbook in `references/`. The summary below is the fast path. Open the reference when the fast path does not resolve it or when you need the complete ordered checklist.

### No delivery / zero impressions

Most often a status or eligibility gate, not a bidding problem. In order: confirm nothing in the parent chain is paused, ended, or archived; confirm today is inside the flight and budget remains; confirm an approved creative is assigned and matches the line item type; confirm the bid clears the floor; confirm targeting is not so narrow that the pool is empty. Full ordered checks in `references/no-delivery.md`.

### Under-pacing

The line item is delivering but will not finish the flight. Read the Impressions lost chart to find the binding constraint. Typical causes: bid too low (lost to auction or below minimum bid), targeting too narrow (thin pool), frequency cap too tight, ASAP not appropriate, or budget set below what the inventory can absorb. Raise the binding lever, not all of them. See `references/under-pacing.md`. For pacing-mode choice and pacing math, hand off to `dv360-pacing-and-optimization`.

### Over-pacing

The line item will exhaust budget before the flight ends, risking a dark period. Typical causes: ASAP pacing where even pacing was intended, daily cap too high, automated bidding spending into cheap inventory, or a flight shorter than planned. Switch to even pacing, set or lower a daily cap, and verify the flight dates. See `references/over-pacing.md` and `dv360-pacing-and-optimization`.

### Low win rate

You are bidding but rarely winning. Order: confirm the bid clears typical floors for the inventory; check whether loss is internal (your own higher-priority line items) or external (other buyers); check whether brand-safety, IVT, or seller filters are removing requests prebid; check that the bid strategy is not capped below market by a Target CPA or max bid that is too low. See `references/low-win-rate.md`. For strategy choice, hand off to `dv360-bid-strategy`.

### Low viewability

Delivery is fine but viewable rate is below target. Order: check the inventory mix (some placements and formats are structurally low-viewability, for example below-the-fold and certain out-stream); add or tighten a viewability prebid targeting threshold; exclude the worst placements; confirm measurement is actually firing. See `references/low-viewability.md`. For viewability standards and vendor setup, hand off to `dv360-frequency-and-brand-safety`.

### Creative disapproved or not serving

A creative cannot serve until its status is Approved or Servable. Pending and Rejected do not serve. Order: open the creative status and read the feedback; fix the cause (format, content policy, or landing page); resubmit, which restarts review and returns the creative to pending until it is servable again; for a policy error, dispute it. See `references/creative-issues.md`.

### Low CTR or engagement

Delivery is fine but response is weak. This is usually a creative, placement, or audience-relevance problem, not a delivery bug. Order: segment CTR by creative, placement, device, and audience to find where it collapses; rotate or refresh creative; prune low-CTR placements; tighten audience relevance. See `references/low-ctr.md`.

### Low or no conversions

If impressions are delivering but conversions are zero or far below plan, suspect measurement before media. Order: confirm the Floodlight tag fires and is attached to the campaign; confirm you are reading the right conversion column and attribution window (post-click versus post-view); confirm enough time has passed for view-through to register; only then question audience quality and bid strategy. See `references/low-conversions.md`. For Floodlight and attribution model details, hand off to `dv360-measurement-and-attribution`.

### Deal not delivering

A PMP, Programmatic Guaranteed, or Preferred Deal that is not spending. Order: confirm the deal is active and not expired on both buy and sell sides; confirm it is assigned and mapped to the line item; confirm the line item bid meets the deal floor; confirm targeting on the line item is not excluding the deal's inventory; for Programmatic Guaranteed, confirm priority so the deal is not outbid by your own open-auction line items. See `references/deal-not-delivering.md` and the full deal tree in `dv360-deals-and-inventory`.

## Common pitfalls

- **Changing many levers at once.** Move one lever, let it run, then read the result. Simultaneous changes make the cause unknowable.
- **Skipping the status check.** A paused insertion order or an unassigned creative produces zero delivery that looks like a bidding problem. Confirm the parent chain first.
- **Trusting fresh conversion data.** View-through and offline conversions lag. Do not declare "no conversions" or re-optimize on data that is only a few hours old.
- **Reading the wrong conversion column.** Post-click and post-view differ a lot. Confirm the column and the attribution window before concluding media is failing.
- **Treating viewability as an impression-loss bucket.** It is a quality metric. Low viewability is fixed through inventory mix and prebid thresholds, not by raising the bid.
- **Fixing a small loss bucket.** Always fix the largest impression-loss bucket first.

## Reference material

- `references/no-delivery.md`: zero impressions or zero spend, full ordered checks.
- `references/under-pacing.md`: under-delivery diagnosis and the binding-lever method.
- `references/over-pacing.md`: over-delivery and dark-period prevention.
- `references/low-win-rate.md`: internal versus external loss and floor diagnosis.
- `references/low-viewability.md`: inventory mix and prebid viewability thresholds.
- `references/creative-issues.md`: creative statuses, rejection causes, resubmission, appeals.
- `references/low-ctr.md`: segmenting engagement and refreshing creative.
- `references/low-conversions.md`: measurement-first conversion diagnosis.
- `references/deal-not-delivering.md`: deal activation, mapping, floor, and priority.

## Sources

- Monitor impression loss: https://support.google.com/displayvideo/answer/3103324 (as of June 2026)
- Troubleshoot your deals and line items: https://support.google.com/displayvideo/answer/6292894 (as of June 2026)
- Fix spend problems (troubleshooter): https://support.google.com/displayvideo/troubleshooter/4359120 (as of June 2026)
- Set budgets and control your pacing: https://support.google.com/displayvideo/answer/3114676 (as of June 2026)
- About the creative review process: https://support.google.com/displayvideo/answer/6063030 (as of June 2026)
- Find and fix rejected creatives: https://support.google.com/displayvideo/answer/12726387 (as of June 2026)

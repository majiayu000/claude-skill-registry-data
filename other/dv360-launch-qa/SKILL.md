---
name: dv360-launch-qa
description: Run a thorough pre-launch QA pass on a Display & Video 360 campaign and sign it off before go-live. Use when the user asks for pre-launch QA, a campaign checklist, whether a campaign is ready to launch, how to sign off before go-live, a launch checklist, or a final pre-flight review of setup, flights, budgets, bidding, targeting, brand safety, creatives, tracking, frequency, or billing.
---

# DV360 launch QA

The deliverable is a complete pre-flight QA pass: every setting that can waste budget, mis-deliver, or break measurement, checked before a single impression serves. A launch QA is cheap. A campaign that runs for two days against the wrong audience, with broken conversion tracking, or with no budget cap is not.

This skill gives you the grouped checklist to scan, a full line-by-line checklist to work through, a fill-in template to output and complete, and a sign-off workflow. For definitions and KPI math see `programmatic-foundations`.

## When to use this skill

- A campaign is built and someone asks "is this ready to launch?" or "can we go live?".
- You need a pre-launch checklist, a sign-off, or a peer-QA pass.
- A change freeze before go-live, or a post-launch check 24 to 48 hours after launch.

Boundaries with sibling skills. This skill verifies that setup is correct and complete. The how-to for each area lives elsewhere:
- Structure and hierarchy decisions: `dv360-campaign-architecture`.
- Bid strategy choice and configuration: `dv360-bid-strategy`.
- Deals, inventory sources, and deal health: `dv360-deals-and-inventory`.
- Brand suitability and frequency setup: `dv360-frequency-and-brand-safety`.
- A line item not delivering after launch: `dv360-troubleshooting`.
- Report setup and pacing dashboards: `dv360-reporting`.
- Naming, roles, and governance the QA enforces: `dv360-account-setup-and-taxonomy`.

## Quick reference: the ten QA groups

Work top to bottom. Each group has a full set of line items in `references/launch_qa_checklist.md`.

| # | Group | What you are confirming |
| --- | --- | --- |
| 1 | Campaign, IO, line item setup | Hierarchy, naming, ownership, and that every entity is built and linked |
| 2 | Flight, budget, pacing | Dates, budget caps at every level, pacing model, and that budgets reconcile to the buy |
| 3 | Bidding | The right strategy and goal value for the KPI, with sane floors and caps |
| 4 | Targeting, audiences, exclusions | Geo, audience, device, and that exclusions and brand-safety floors are applied |
| 5 | Inventory and deals | Deal IDs active, assigned to the right line items, and inventory sources correct |
| 6 | Brand safety, verification, viewability | Suitability tier, third-party verification, and viewability targets set |
| 7 | Creatives, trafficking, landing pages, tracking | Creatives approved and assigned, click-throughs and trackers correct, conversion tracking firing |
| 8 | Frequency | Frequency caps at the right level for the objective |
| 9 | Reporting and alerts | Reports scheduled, pacing visibility, and alerts configured |
| 10 | Billing and purchase order | PO in place, partner costs and fees set, billing reconciles |

## Core process

1. **Confirm scope and ownership first.** Identify the advertiser, the campaign, who built it, and who signs off. Pull the full structure so you are checking the live build, not a plan.
2. **Output the fill-in template** from `assets/launch_qa_checklist_template.md` for this campaign and work the groups in order. Do not skip a group because it "looks fine"; the cheap items (a missing budget cap, a wrong flight date) are the ones that hurt.
3. **Walk every line item in each group**, marking pass, fail, or not applicable with a short note. A line that fails blocks launch until fixed and re-checked.
4. **Verify the load-bearing items twice**: budget caps at every level, flight dates and timezone, conversion tracking firing, audience and geo targeting, and that every line item has at least one approved creative (a line item cannot serve until an assigned creative is approved).
5. **Run peer QA.** A second qualified person re-checks the high-risk groups (budget, targeting, tracking, bidding). Self-QA misses what you built blind.
6. **Freeze, then launch.** Once signed off, impose a short change freeze so no edit slips in between sign-off and go-live. Launch.
7. **Post-launch check at 24 to 48 hours.** Confirm delivery started, pacing is on track, conversions are recording, no line item is stuck unapproved, and spend matches intent. Catching a problem on day one saves the flight. Hand off to `dv360-troubleshooting` if something is not delivering.

## Decision rules and thresholds

- **No budget cap at any level is a blocker.** Confirm a cap exists at the insertion order and line item, and that the sum reconciles to the booked budget. Uncapped spend is the single most expensive mistake.
- **Flight dates and timezone must match the buy.** A campaign in the wrong timezone starts or ends a day off. Confirm start and end at campaign, IO, and line item, and that the timezone is the advertiser's billing timezone.
- **Every line item needs at least one approved creative before go-live.** A line item is not serveable until an assigned creative is approved, and review starts automatically and can take time. Assign creatives early and confirm Servable or Approved status at QA, not at launch.
- **Conversion tracking must be proven, not assumed.** Confirm the Floodlight or conversion setup is linked at the advertiser and that a test or recent conversion is recording. A campaign optimizing to conversions with broken tracking burns budget and learns nothing.
- **Targeting must be positively confirmed, not left default.** Verify geo, audience, language, and device against the brief, and confirm the brand-safety exclusion floor and any required exclusions are applied. A wrong inherited default mis-delivers silently.
- **Bid strategy must match the KPI.** Confirm the strategy and its goal value fit the objective and that floors and caps are sane. See `dv360-bid-strategy` for the choice itself.
- **Deals must be active and correctly assigned.** Confirm each deal ID is active and attached to the intended line items, not orphaned or attached to the wrong one.
- **Sign-off is a gate, not a formality.** Peer QA on the high-risk groups, then a change freeze, then launch. No freeze means a last-minute edit ships unreviewed.

## Reference material

- `references/launch_qa_checklist.md` - the full line-by-line checklist for all ten groups. Work through this for the actual QA; the table above is only the scan.

## Templates and examples

- `assets/launch_qa_checklist_template.md` - a fill-in checklist to output and complete per campaign. It carries every line item with a pass / fail / not-applicable column, a notes column, and the sign-off block (builder, peer QA, change freeze, go-live, post-launch). Emit it, fill it in as you QA, and attach it to the campaign record as the sign-off artifact.

## Common pitfalls

- **Trusting inherited defaults.** Partner and IO defaults cascade into new line items. Positively confirm targeting, brand safety, and pacing rather than assuming the default is right.
- **QA-ing the plan, not the build.** Check the live entities in the account, not the media plan. Builds drift from plans.
- **Skipping creative status.** A line item with no approved creative will not serve. Confirm Servable or Approved at QA, allowing for review time.
- **No change freeze.** An edit between sign-off and launch invalidates the QA. Freeze, then go live.
- **No post-launch check.** Problems that pass static QA (a deal that goes inactive, tracking that silently stops) only show in delivery. Check at 24 to 48 hours.
- **Self-QA only.** You are blind to your own build assumptions. Get a second person on budget, targeting, tracking, and bidding.

## Sources

- [Create a campaign](https://support.google.com/displayvideo/answer/7205081) (as of June 2026)
- [Create an insertion order](https://support.google.com/displayvideo/answer/2696705) (as of June 2026)
- [Create a line item](https://support.google.com/displayvideo/answer/2891312) (as of June 2026)
- [About the creative review process](https://support.google.com/displayvideo/answer/6063030) (as of June 2026)
- [Brand suitability](https://support.google.com/displayvideo/answer/3032915) (as of June 2026)
- [View and edit brand controls for your advertiser](https://support.google.com/displayvideo/answer/9179543) (as of June 2026)
- [About Floodlight and Floodlight activities](https://support.google.com/displayvideo/answer/3027419) (as of June 2026)
- [Archive campaigns, insertion orders, and line items](https://support.google.com/displayvideo/answer/6342906) (as of June 2026)

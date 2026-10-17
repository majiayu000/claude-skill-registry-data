---
name: cross-platform-launch-qa
description: Run a platform-neutral launch QA gate before campaigns go live, covering brief, budget, flights, structure, bidding, targeting, inventory, creative, tags, conversion signal, consent, reporting, taxonomy, approvals, and the first post-launch checks. Use for launches across DV360, Google Ads, Amazon DSP, StackAdapt, The Trade Desk, Meta, TikTok, Microsoft, and CM360.
---

# Cross-platform launch QA

Launch QA is where programmatic ops earns trust. The platform fields differ, but the failure
classes repeat: wrong budget, wrong dates, wrong audience, missing creative, broken click URL,
bad tag, missing conversion, blocked consent, wrong naming, and no approval.

This skill gives one launch gate across platforms. Use the platform-specific skill for the
exact field names, then use this skill to make the go or no-go decision.

## When to use this skill

- Any paid media campaign, line item, ad group, order, creative, tag, or placement is about to
  go live.
- A launch checklist needs to work across multiple platforms.
- A trader asks whether a campaign is safe to launch.
- A launch was rushed and needs a post-launch recovery check.

## Go or no-go criteria

No launch goes green unless all of these are true:

| Gate | Pass condition |
| --- | --- |
| Brief | Objective, KPI, budget, flight, geography, audience, and inventory match the approved plan |
| Structure | Campaign hierarchy, naming, IDs, and parent settings are correct |
| Budget and pacing | Budgets, daily caps, flights, pacing, and timezone align to the plan |
| Bidding | Bid strategy and targets match available signal and goal |
| Targeting | Required targeting is included and exclusions are present |
| Inventory | Deals, supply, placements, and channel settings are mapped and active |
| Creative | Assets are approved, assigned, previewed, click through, and meet spec |
| Tracking | Tags fire, conversions are mapped, click URLs and UTMs pass |
| Consent | Required consent and regional data controls are verified |
| Reporting | Required dimensions, taxonomy, and dashboard keys are present |
| Approval | Required approver signed off on the exact scope |
| Post-launch | First delivery, spend, tags, and reporting checks are scheduled |

## Core process

1. **Anchor to the source of truth.** Pull the approved brief, media plan, IO, taxonomy, tag
   sheet, creative spec, and approval matrix. The platform build is checked against those
   sources, not memory.
2. **Verify entity scope.** Confirm the account, advertiser, campaign, order, line item, ad
   group, placement, and creative IDs. A QA without IDs is not auditable.
3. **Check budget, flight, and pacing.** Confirm total budget, daily or line budgets, start and
   end dates, time zone, pacing mode, and billing model. Watch for flights that begin at
   midnight in the platform time zone.
4. **Check structure and taxonomy.** Names, IDs, labels, codes, UTMs, cost centers, buying
   type, funnel stage, market, format, and reporting join keys must match
   `cross-platform-taxonomy-governance`.
5. **Check buying setup.** Confirm bid strategy, bid target, optimization event, inventory,
   deal mapping, supply controls, geo, devices, frequency, audiences, exclusions, brand safety,
   and suitability controls.
6. **Check creative and trafficking.** Confirm approval status, asset spec, duration, size,
   language, landing page, click URL, macros, companion assets, third-party tags, VAST, and
   ad-server mapping.
7. **Check measurement and consent.** Confirm conversion actions, key events, Floodlight,
   pixels, deduplication keys, server-side events, Consent Mode or consent strings, and regional
   restrictions. Do not launch direct-response campaigns on an unverified conversion.
8. **Check reporting readiness.** Confirm the report or dashboard can read the campaign using
   the expected taxonomy and that early-life metrics are available.
9. **Record the launch decision.** Output `Go`, `No-go`, or `Conditional go`. Conditional go
   must name the acceptable residual risk, owner, expiry time, and rollback path.
10. **Run post-launch checks.** Within the first delivery window, verify serving, spend, tags,
   clicks, conversion collection, creative preview, and reporting rows. A campaign that is live
   but invisible to reporting is not fully launched.

## Conditional go rules

Conditional go is rare. It is allowed only when:

- The residual risk is known and documented.
- The issue does not affect spend control, brand safety, legal, consent, billing, or core
  conversion tracking.
- A named owner can clear it inside the first delivery window.
- The approver signs off on the exact risk.

Examples: a noncritical dashboard label cleanup may be conditional. A missing conversion tag,
unapproved creative, wrong budget, or relaxed brand-safety control is no-go.

## Launch QA output

```text
Launch QA decision: Go | Conditional go | No-go
Platform:
Advertiser:
Campaign/order/line IDs:
Launch date and time zone:
Reviewer:
Approver:

Passed gates:
Blocked gates:
Conditional risks:
Post-launch check time:
Rollback or pause path:
Evidence links:
```

## Common pitfalls

- Checking platform UI values without checking the approved plan.
- Treating creative approval as creative QA. Approved creative can still have a broken click URL.
- Launching before the dashboard can recognize the campaign.
- Forgetting time zone and midnight behavior.
- Skipping the post-launch check because the launch checklist passed.

## Related artifacts

- `templates/ops/cross-platform-launch-qa-checklist.md`
- `dv360-launch-qa`
- `cm360-trafficking-and-ad-tags`
- `gtm-qa-versioning-and-api`
- `consent-signal-verification-and-decode`
- `pre-launch-qa-gate`
- `floodlight-and-tag-pre-launch-gate`

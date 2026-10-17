---
name: cm360-verification-and-active-view
description: Measure and report viewability and ad verification in Campaign Manager 360 using Active View against the MRC standard, across the eligible, measurable, and viewable tiers. Use when the user asks about Active View, viewability, viewable impressions, viewable rate, measurable vs eligible impressions, why viewability is low or missing, the MRC 50%/1s display and 50%/2s video standards, non-measurable causes (cross-domain iframes, unsupported tags, VPAID, mobile app SDK), MRC accreditation, audible/AV video metrics, or pulling Active View metrics through the CM360 API v5.
---

# CM360 verification and Active View

Turn "was the ad actually seen?" into a number you can defend. Active View is the measurement layer inside Campaign Manager 360 that reports viewability against the Media Rating Council (MRC) standard, split across three tiers: how many impressions were eligible for measurement, how many were actually measurable, and how many cleared the viewable bar. The job here is to read those tiers correctly, compute the right denominator for a viewable rate, explain a low or missing number by tier and cause, and pull the Active View metrics through reports and the API v5 without mislabeling them.

This skill assumes you know impressions, CPM, and the difference between a served and a viewable impression. For that math see the `programmatic-foundations` skill. It reports what Active View already captured; it does not traffic tags or configure Floodlight.

## When to use this skill

- "What is our viewability / viewable rate?" / "Why is it low?" / "Why is it blank?"
- "What is the MRC standard?" / "50% for one second, is that display or video?"
- "Eligible vs measurable vs viewable, what is the difference?" / "Which one is the denominator?"
- "Why are these impressions not measurable?" / "Why did coverage drop?"
- "Which Active View metrics are MRC accredited?"
- "What about audible, AV, or completed-in-view video metrics?"
- "Pull Active View metrics through the CM360 API / into a warehouse."
- "Set up a viewability report by placement / site / creative."

Boundaries with sibling skills. This skill owns reading and explaining Active View viewability.
- Building or downloading a CM360 report, the async run-and-poll flow, and Trafficking API reads: `cm360-reporting-and-trafficking-api`. That skill runs the report; this one tells you which metrics to put in it and how to read them.
- Configuring Floodlight activities, conversion windows, and counting: `cm360-floodlight-and-conversions`. Viewability is not conversion measurement.
- Trafficking placements and ad tags, and picking the tag type that maximizes Active View coverage at trafficking time: `cm360-trafficking-and-ad-tags`. This skill diagnoses coverage after the fact; that skill sets the tags.
- Third-party verification vendors (IAS, DoubleVerify, Moat) wrapped as verification tags and their brand-safety / fraud signals: `brand-safety-and-suitability`. Active View is Google's first-party viewability, not a third-party vendor.
- Viewability on the buy side in DV360 (target viewable CPM, viewability targeting): `dv360-measurement-and-attribution` and `dv360-frequency-and-brand-safety`.
- Deduping viewability against DV360 or a DSP number: `cross-platform-conversion-reconciliation`.

## Quick reference: the three tiers

Active View reports funnel through three tiers. Get the tier right before you quote a rate.

| Tier | What it counts | API metric | Use it as |
| --- | --- | --- | --- |
| Eligible | Served impressions on supported creative and tag types | `activeViewEligibleImpressions` | The ceiling for what can ever be measured |
| Measurable | Eligible impressions where Active View actually captured viewability data | `activeViewMeasurableImpressions` | The denominator for viewable rate |
| Viewable | Measurable impressions that met the MRC bar (50% pixels for the required time) | `activeViewViewableImpressions` | The numerator for viewable rate |

Viewable rate = viewable / measurable, never viewable / eligible and never viewable / total served. Reporting viewable over served silently understates you by the unmeasurable slice. The MRC-accredited viewable rate uses the measurable denominator.

Two coverage ratios tell you whether the number is trustworthy:
- Measurable rate = measurable / eligible. Low means Active View could not read enough impressions; the viewable rate sits on a thin base.
- Eligible rate = eligible / total served. Low means unsupported tags or creatives are keeping impressions out of measurement entirely, a trafficking problem, not a media problem.

## Quick reference: the MRC standard

| Format | Viewable when | Threshold |
| --- | --- | --- |
| Display, under 242,500 pixels (smaller than 970x250) | 50% of pixels in view for 1 continuous second | Standard MRC display |
| Display, 242,500 pixels (970x250) or larger | 30% of pixels in view for 1 continuous second | Large-ad MRC rule |
| Video (in-stream) | 50% of pixels in view while playing for 2 continuous seconds | MRC video |

The large-ad 30% rule is the one people forget. A 970x250 or bigger unit only needs 30% in view, so do not flag a big-canvas placement as underperforming against the 50% display bar.

## Core process

1. Name the tier before the number. When someone asks for "viewability", decide whether they want the viewable rate (viewable / measurable) or absolute viewable impressions, and confirm the denominator. Most disputes are a denominator mismatch, not a real gap.
2. Pull all three tiers together, never viewable alone. Put `activeViewEligibleImpressions`, `activeViewMeasurableImpressions`, and `activeViewViewableImpressions` in the same report row (plus total impressions) so you can see eligible, measurable, and viewable side by side. A viewable count without its measurable base is unreadable.
3. Compute both coverage ratios. Measurable / eligible and eligible / served. A healthy viewable rate on a 20% measurable base is not a healthy number; it is a small sample. Coverage first, rate second.
4. If viewable rate is the concern, diagnose by tier. Walk the funnel: is the eligible rate low (trafficking, unsupported tags/creatives), the measurable rate low (cross-domain iframes, browser or connection cutoffs, backup/default ads), or is the viewable-over-measurable genuinely low (real below-the-fold placement)? Fix the tier that is actually leaking. See `references/non-measurable-causes.md`.
5. Match the standard to the format. Read display against 50%/1s (or 30%/1s for large units) and video against 50%/2s. Do not compare a video placement's rate to a display benchmark or vice versa; they clear different bars.
6. Segment before you conclude. Break Active View by placement, site, creative type, and device. Viewability is a placement and inventory property, so an account-level average hides the below-the-fold placements dragging it down. The average is a starting point, not a finding.
7. Flag accreditation when the number will be contractually enforced. Some Active View metrics are MRC accredited and some are not. If a viewability guarantee or a make-good hangs on the number, confirm the specific metric is accredited before you cite it. See `references/mrc-thresholds-display-and-video.md`.
8. Hand the report mechanics to the reporting skill. Building the report, running it, polling for the file, and downloading it is `cm360-reporting-and-trafficking-api`. This skill picks the metrics and reads them; that skill runs the pull.

Safe-by-default: everything here is read-only. Reading Active View metrics and computing rates changes nothing. If the diagnosis points at trafficking (wrong tag type, unsupported creative), do not re-traffic from here; hand the fix to `cm360-trafficking-and-ad-tags` behind a human review.

## Decision rules and thresholds

### Which denominator

- Viewable rate for MRC reporting and for a viewability guarantee: viewable / measurable. This is the accredited construction.
- Never viewable / eligible: eligible impressions include ones Active View never read, so the rate is diluted by the unmeasurable slice and understates true viewability.
- Never viewable / total served: same problem, worse, since served includes non-eligible creative and tag types too.
- Absolute delivery of viewable inventory (for a viewable-CPM invoice or a viewable-impression guarantee count): use `activeViewViewableImpressions` directly, not a rate.

### When a low viewable rate is a real problem vs a measurement artifact

- Measurable rate below roughly 70% of eligible: treat the viewable rate as low-confidence. A large unmeasurable slice can hide either good or bad viewability. Fix coverage before judging the rate. Common causes in `references/non-measurable-causes.md`.
- Eligible rate well below 100% of served: a trafficking problem. Unsupported tag types or creatives are excluding impressions from measurement entirely. The fix is the tag/creative, in `cm360-trafficking-and-ad-tags`, not the media buy.
- Measurable base healthy and viewable-over-measurable still low: a real inventory problem. The placement genuinely sits below the fold or closes fast. Shift budget, add viewability targeting on the buy side (DV360), or renegotiate placement.

### Tag type drives coverage

- ins tags give the best Active View coverage; JavaScript, iframe/JavaScript, and VAST are supported but read less. If eligible or measurable coverage is low, check the tag type first. Recommend ins tags at trafficking time in `cm360-trafficking-and-ad-tags`.
- Impression image (1x1 pixel) tracking ads report Active View only on YouTube with enhanced YouTube tracking; expect near-zero coverage elsewhere. That is expected, not a defect.

### Display vs video reading

- Display clears at 50%/1s (30%/1s for 970x250 and larger). Video clears at 50%/2s. Keep them in separate report views or at least a separate benchmark column; a blended "viewability" across both mixes two different bars.
- Video also carries audible and AV (audible-and-visible) and completed-in-view metrics. A video "viewable rate" that ignores audibility can overstate quality if the sound was off. Pull the audible and play-time metrics alongside when audio matters. Field map in `references/three-tier-reporting.md`.

### MRC accreditation

- MRC accredits some Active View viewable-impression metrics and some begin-to-render impression metrics, but not every column. When the number backs a contract, confirm the exact metric is accredited on the MRC accredited-metrics page rather than assuming the whole family carries the seal. See `references/mrc-thresholds-display-and-video.md`.

## Reference material

- `references/mrc-thresholds-display-and-video.md`: the MRC standard in full (display 50%/1s, large-ad 30%/1s at 242,500 pixels, video 50%/2s), how Active View applies it, which Active View metrics are MRC accredited vs not, and how accreditation interacts with viewability guarantees and make-goods. Read this when someone quotes a threshold, questions a benchmark, or ties money to the number.
- `references/three-tier-reporting.md`: the eligible/measurable/viewable model with the exact CM360 API v5 metric field names for every tier including the audible and play-time video family (`activeViewEligibleImpressions`, `activeViewMeasurableImpressions`, `activeViewViewableImpressions`, `activeViewPercentageViewableImpressions`, `activeViewNotMeasurableImpressions`, `activeViewNotViewableImpressions`, the audible and AV set, and the GroupM-verified set), the correct denominators, and worked rate calculations. Read this when building the report or writing the SQL that computes rates.
- `references/non-measurable-causes.md`: every reason an impression lands eligible-but-not-measurable or fails to be eligible at all, mapped to the tier it hits and whether the fix is trafficking or inventory (cross-domain iframes, unsupported tag/creative types, VPAID gaps, backup/default ads, mobile app SDK requirement, browser/connection cutoffs, browser closed early). Read this when coverage is low or a viewability number looks wrong.

## Templates and examples

Viewability report by placement (metrics to request, read mechanics in `cm360-reporting-and-trafficking-api`):

```
Report: type STANDARD
  dimensions: date, site, siteId, placement, placementId, creativeType
  metrics:
    impressions
    activeViewEligibleImpressions
    activeViewMeasurableImpressions
    activeViewViewableImpressions
    activeViewPercentageViewableImpressions   (the pre-computed viewable rate, viewable / measurable)
  dateRange: LAST_30_DAYS
Read as:
  eligible_rate   = activeViewEligibleImpressions   / impressions
  measurable_rate = activeViewMeasurableImpressions / activeViewEligibleImpressions
  viewable_rate   = activeViewViewableImpressions   / activeViewMeasurableImpressions
Flag any placement with measurable_rate < 0.70 as low-confidence before judging viewable_rate.
```

Worked example, why the "42% viewable" headline was wrong:

```
Placement: homepage_970x250_atf
  impressions served                 1,000,000
  activeViewEligibleImpressions        980,000   eligible_rate   0.98  (healthy trafficking)
  activeViewMeasurableImpressions      560,000   measurable_rate 0.57  (LOW: thin base)
  activeViewViewableImpressions        420,000
Wrong: 420,000 / 1,000,000 = 42%  (viewable over served, understated and non-MRC)
Right: 420,000 / 560,000   = 75%  (viewable over measurable, the MRC construction)
But: measurable_rate 0.57 means 43% of eligible impressions were never read, likely
     cross-domain iframes on this publisher. The 75% sits on a thin base; fix coverage
     (tag type / iframe) before trusting it. See references/non-measurable-causes.md.
Also: this is a 970x250 unit, so the viewable bar is 30% pixels / 1s, not 50%.
```

Video viewability with audibility, so "viewable" does not overstate quality:

```
Report metrics for in-stream video placements:
  activeViewViewableImpressions              (50% pixels, 2 continuous seconds)
  activeViewMeasurableImpressions
  activeViewAudibleMeasurableImpressions
  activeViewPercentAudibleAndVisible          (AV: audible and on-screen)
  activeViewAverageViewableTimeSecond
Read: a high viewable rate with a low audible-and-visible rate means the ad was
      on-screen but muted. For sound-on brand campaigns, hold the AV metric, not
      viewability alone.
```

## Common pitfalls

- Dividing viewable by served or by eligible. Both understate viewability and neither is the MRC construction. Viewable rate is viewable / measurable. Fix the denominator before anything else.
- Quoting a viewable rate on a thin measurable base. A 90% viewable rate on a 30% measurable base is a small sample dressed as a result. Report the measurable rate next to the viewable rate and flag low coverage.
- Reading a large unit against the 50% display bar. Ads 242,500 pixels (970x250) and larger clear at 30% in view for 1 second. Do not mark a big canvas as failing when it met its own standard.
- Blending display and video into one "viewability" number. Display is 50%/1s (or 30%/1s), video is 50%/2s. They are different bars; average them separately.
- Treating a video viewable rate as quality when the sound was off. Viewable means on-screen, not heard. For sound-on campaigns hold the audible-and-visible (AV) metric alongside.
- Blaming the media buy for a low eligible rate. A low eligible / served ratio is unsupported tags or creatives, a trafficking fix in `cm360-trafficking-and-ad-tags`, not a placement that needs replacing.
- Expecting Active View from 1x1 impression pixels. Image tracking ads report Active View only on YouTube with enhanced tracking. Near-zero coverage elsewhere is expected.
- Assuming every Active View metric is MRC accredited. Some are, some are not. If money rides on the number, confirm the specific metric carries accreditation.
- Comparing CM360 Active View one-to-one with a DSP or third-party vendor number. Different measurement engines and denominators produce a gap by design. Reconcile deliberately in `cross-platform-conversion-reconciliation`, do not expect an exact match.
- Chasing a viewability "drop" that is a coverage change. If measurable coverage fell (a publisher moved to cross-domain iframes, a creative type changed), the viewable rate can move without any real change in how often ads were seen. Check coverage before calling it a delivery problem.

## Sources

- [About Active View](https://support.google.com/campaignmanager/answer/6125292?hl=en) (as of July 2026)
- [Active View support](https://support.google.com/campaignmanager/answer/3424068?hl=en) (as of July 2026)
- [Active View: Measurable Impressions](https://support.google.com/campaignmanager/answer/6188678?hl=en) (as of July 2026)
- [Media Rating Council (MRC) accredited metrics, Campaign Manager 360](https://support.google.com/campaignmanager/answer/7620594) (as of July 2026)
- [Overview of Viewability and Active View, Google Ad Manager](https://support.google.com/admanager/answer/4524488?hl=en) (as of July 2026)
- [Limitations of Active View in Display & Video 360](https://support.google.com/displayvideo/answer/3214673?hl=en) (as of July 2026)
- [Dimensions, Metrics, and Filters, Campaign Manager 360 API v5](https://developers.google.com/doubleclick-advertisers/v5/dimensions) (as of July 2026)
- [Campaign Manager 360 API deprecation schedule](https://developers.google.com/doubleclick-advertisers/deprecation) (as of July 2026)
- [Campaign Manager 360 report types](https://support.google.com/campaignmanager/answer/2823790?hl=en) (as of July 2026)

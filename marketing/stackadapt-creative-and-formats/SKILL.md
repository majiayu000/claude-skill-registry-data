---
name: stackadapt-creative-and-formats
description: Brief, QA, and troubleshoot StackAdapt creative formats across native, display, HTML5, video, CTV, audio, DOOH, in-game, creative builder, tracking, and review. Use when the user asks for StackAdapt creative specs, display sizes, video formats, CTV or native assets, HTML5 or rich media, Creative Studio, or why a creative is not approved or not delivering.
---

# StackAdapt creative and formats

Prepare creative for StackAdapt campaigns across native, display, video, CTV, audio, DOOH, and other channels. This skill helps a campaign operator brief assets, check format fit, and spot creative blockers before launch. It does not replace the operator's final review in StackAdapt, Creative Studio, or the logged-in help center.

StackAdapt publishes useful public channel pages, while some detailed help-center and in-product specs can require account access. Use the public specs as the base, then confirm exact requirements in the platform for the account, channel, and publisher.

## When to use this skill

- "What creative do I need for a StackAdapt campaign?"
- "Which display sizes does StackAdapt support?"
- "Can I run HTML5, rich media, native video, in-stream video, outstream video, CTV, audio, or DOOH?"
- "Why did this StackAdapt creative get rejected?"
- "How do I brief Creative Studio?"
- "How many creative variants should I upload?"
- "What needs to be checked before launch?"

Boundaries with sibling skills:
- Campaign build order: `stackadapt-campaign-setup`.
- Targeting and audiences: `stackadapt-targeting-and-audiences`.
- Inventory and brand safety: `stackadapt-inventory-and-brand-safety`.
- Bidding and pacing: `stackadapt-bidding-and-budgets`.
- Reporting and attribution: `stackadapt-reporting-and-attribution`.
- Troubleshooting delivery and review statuses: `stackadapt-optimization-and-troubleshooting`.

## Quick reference

| Format | Operator check |
| --- | --- |
| Native | Headline, body, image or video, CTA, brand, landing page, and disclosure are complete |
| Display | Standard IAB sizes, accepted format, 750 KB max public spec, clear CTA |
| HTML5 / rich media | Built through Creative Builder or packaged as supported rich media, with safe interactions |
| In-banner video | Video embedded in a display unit, with click and audio behavior checked |
| Video | In-stream, native video, native outstream, or interstitial matched to campaign goal |
| CTV | TV-safe video asset, publisher/device specs, no web-only interaction dependency |
| Audio | Audio file, companion display where used, and landing or tracking behavior checked |
| DOOH | Screen dimensions, venue context, static or motion rules, and approval path checked |

## Core process

1. Match creative to channel and objective. Native fits content-led consideration, display fits scalable reach and retargeting, video and CTV fit awareness and storytelling, audio fits screen-free reach, and DOOH fits location presence. Do not force one asset into every channel.
2. Gather required components. Native needs component assets; display needs sized units; video and CTV need media files; audio needs sound assets; DOOH needs screen-specific files. Missing components block approval or reduce scale.
3. Check public specs first. StackAdapt's public display page lists common sizes such as 300x250, 728x90, 320x50, 160x600, 300x600, 970x250, and 970x90; accepted public formats include JPG, PNG, GIF, and HTML5 tags, with a public max file size of 750 KB for display.
4. Confirm logged-in or publisher-specific specs. Public pages do not cover every account setting, exchange, publisher, CTV device, or DOOH screen. Confirm the exact spec in-platform or with StackAdapt support before launch.
5. Build for rotation and learning. Upload at least two strong creative variants per ad group where the format allows, and vary one clear axis at a time: hook, offer, format, or CTA.
6. Check tracking and click behavior. Confirm landing URL, UTMs, click trackers, pixels, and any third-party measurement tags before review. A creative can be approved visually but fail the campaign if tracking is wrong.
7. Review brand safety and policy. Regulated verticals, claims, alcohol, finance, health, political, and location-sensitive creative need extra scrutiny. Do not let generated or remixed assets bypass approval.
8. Submit with buffer. Creative review takes time. Build and submit ahead of flight start, especially when Creative Studio, rich media, CTV, DOOH, or external approvals are involved.
9. Read creative performance by goal. Use CTR, CVR, VCR, completion, CPCV, CPA, ROAS, and lift based on objective. Do not crown a creative winner on a metric that does not match the campaign.

## Decision rules and thresholds

- Channel fit beats format availability. Just because StackAdapt can run a format does not mean that format serves the brief.
- Display sizes should cover the high-scale set first. Start with common IAB sizes before custom sizes.
- Native needs contextual alignment. A native unit must look and read like it belongs in-feed while staying clearly advertising.
- Video format follows attention context. In-stream reaches a video-watching user, outstream reaches article context, interstitial uses a natural app break, and CTV reaches shared-screen viewing.
- CTV creative cannot depend on web interactions. Build for lean-back viewing, clear audio, and publisher/device acceptance.
- Creative Studio is useful for scale, but review still matters. A generated size set or rich media build still needs brand, legal, and landing-page QA.
- Keep enough variants to optimize. One creative per ad group leaves no rotation learning. Too many weak variants can dilute spend. Start with two to five meaningful variants per ad group unless the plan needs more.

## QA checklist

- Channel, objective, and ad group assignment match the brief.
- Required assets for the format are complete.
- Display sizes and file weight checked against the public and in-platform spec.
- Video or CTV file meets publisher and device specs.
- Landing URL, UTMs, click trackers, and pixels are correct.
- Creative claim, price, offer, and disclaimer are approved.
- Brand safety and regulated-category constraints are checked.
- Creative variants test one clear difference.
- Review buffer exists before flight start.
- Reporting names let the operator read creative performance without guessing.

## Templates and examples

Display creative brief:

```text
Goal: Retarget site visitors to demo request.
Sizes: 300x250, 728x90, 320x50, 160x600, 300x600, 970x250.
Formats: JPG, PNG, GIF, or supported HTML5.
File size: Check platform, public display spec says 750 KB max.
Variants: 3 hooks, same offer, same landing page.
Tracking: UTM campaign, UTM content by creative concept, click tracker verified.
Approval: brand and legal sign-off before upload.
```

Video creative brief:

```text
Goal: Consideration and assisted conversions.
Formats: native video plus in-stream video.
Variants: product demo, customer proof, offer-led cutdown.
Metrics: VCR, CPCV, site visits, assisted conversions, post-click CVR.
Checks: aspect ratio, duration, audio, captions, landing URL, third-party measurement.
```

CTV creative brief:

```text
Goal: Reach and frequency in premium streaming.
Asset: TV-safe video, clear branding in first 3 seconds, audio mixed to publisher spec.
Do not rely on: hover, click-to-expand, small text, or web-only interactivity.
Checks: publisher/device spec, brand safety, frequency plan, measurement currency.
```

## Common pitfalls

- Uploading only one creative and expecting meaningful optimization.
- Treating native like a resized banner.
- Ignoring the public display file-size limit and finding out at upload.
- Running CTV creative with tiny text or a web-first CTA.
- Forgetting UTMs or mismatching creative names to report labels.
- Assuming Creative Builder output needs no review.
- Waiting until the flight start for creative approval.
- Reading video creative on CTR alone instead of completion, visits, conversions, and lift.

## Sources

- [Display Advertising Platform, StackAdapt](https://www.stackadapt.com/display-advertising) (as of July 2026)
- [Programmatic Video Advertising Platform, StackAdapt](https://www.stackadapt.com/video-advertising) (as of July 2026)
- [Connected TV Advertising, StackAdapt](https://www.stackadapt.com/connected-tv) (as of July 2026)
- [Programmatic Audio Advertising, StackAdapt](https://www.stackadapt.com/programmatic-audio) (as of July 2026)
- [StackAdapt Creative Studio](https://www.stackadapt.com/creative-studio) (as of July 2026)

---
name: dv360-creative-trafficking
description: Traffic a creative correctly in Display & Video 360 so it serves, renders, tracks, and clicks through, and diagnose what blocks it. Use when the user asks how to traffic a creative, about a third-party tag, VAST, VPAID, a click macro, a cachebuster, a secure or SSL tag, an impression pixel, why a creative is not rendering or not serving, creative QA, an ad tag, a companion banner, or a wrapper that makes a CTV deal serve zero.
---

# DV360 creative trafficking

The deliverable is a creative that serves: it renders in the placement, fires its impression pixel, fires its click tracker, lands the user on the right page, matches the placement format and size, and is approved or servable. Trafficking is half the ops job, and a creative that wins the auction but renders blank, double-counts impressions, or breaks the clickthrough wastes the spend the bid just won.

This skill covers the creative types, how third-party tags and tracking work, what video and connected TV require, and a render-to-click QA checklist. It assumes you know what an impression, a creative, a CPM, and an ad tag are. For shared definitions see the `programmatic-foundations` skill.

## When to use this skill

- "How do I traffic this creative?" / "Where does the third-party tag go?"
- "What is a click macro / cachebuster macro, and where does it go in the tag?"
- "What is the difference between the click tracker and the landing URL?"
- "Does this need a secure / SSL tag?" / "My creative was flagged for non-secure calls."
- "VAST vs VPAID." / "Why does my CTV deal serve zero impressions?"
- "The creative is not rendering / not serving / not tracking." / "Run creative QA on this."
- "Do I need a companion banner?" / "How do I add an impression pixel to a display creative?"

Boundaries with sibling skills. This skill is about trafficking and serving: what makes a creative serve, render, track, and click through, and what blocks it mechanically.
- Creative policy, disapprovals, appeals, and a creative that is "not serving" because it was rejected: hand off to `dv360-troubleshooting`. That skill owns the policy and delivery-failure side; this one owns the trafficking and serving side.
- The full pre-launch sign-off that creative trafficking is one group of: `dv360-launch-qa`.
- YouTube and in-stream video buying, formats, and line item setup: `dv360-youtube-and-video`.
- Brand-safety and suitability controls applied to where creatives run: `dv360-frequency-and-brand-safety`.
- Floodlight, attribution windows, and conversion plumbing: `dv360-measurement-and-attribution`.

## Quick reference: creative types

Pick the type that matches how the asset is hosted and what the line item and inventory accept.

| Creative type | What it is | Trafficking notes |
| --- | --- | --- |
| Hosted display | Image or HTML5 assets you upload, served by the platform | Add impression and click tracking; platform handles the clickthrough and macros |
| Third-party tag | An ad-server tag (JavaScript or iframe) that calls an external server | Paste the tag; the platform wraps it with impression and click macros for recognized servers, otherwise insert macros by hand |
| Rich media | Expandable, interstitial, in-banner video, parallax, and similar | Clickthroughs use exit events, not click tags; obeys size, file-weight, and HTTP-call limits |
| Native | Component assets (logo, image, headline, body, call to action) the publisher assembles | Supply every required asset for reach; the publisher renders the layout, so you do not control pixels |
| Video | A video asset or a VAST tag served into a publisher video player | Built to the VAST spec; supports companion banners and quartile tracking; see the video section below |

A creative serves only when it renders in the placement, matches the placement format and size, is secure, and is approved or servable. Any one of those failing blocks the impression.

Exact specs (dimensions, file weights, durations, accepted file types, bitrates) change and differ by placement and exchange. Do not hardcode a number from memory. Read the current value off the relevant help page in Sources before you build or brief a designer.

## Core process

1. Confirm what you were handed and how it is hosted. A hosted asset, a third-party tag, a VAST tag URL, or native components. The hosting model decides how tracking and macros are applied, so settle this first.
2. Match the creative to the line item type and the inventory. A display creative goes on a display line item, a video creative or VAST tag on a video line item, native video only on display line items. A creative whose type or size the placement does not accept will not render even after it serves.
3. Add the trackers. For a hosted or platform-synced creative, append the impression tracking pixel and confirm the clickthrough URL. For a third-party tag, confirm the platform inserted the impression and click macros, or insert them yourself if the server is not recognized.
4. Get the click split right. The click tracker records the click and the auction, then redirects to the landing URL. These are two different fields. Putting the landing URL where the click tracker belongs, or omitting the click macro, breaks tracking or the redirect. See the click-tracking section.
5. Make it secure. Every asset and tracker URL must be HTTPS, or review flags it for non-secure calls and it cannot serve on most inventory. Landing pages are the only URLs exempt from the HTTPS requirement.
6. For video, validate the VAST. Confirm the VAST version the inventory accepts, that the wrapper chain resolves inside the player timeout, and that companion banners and quartile trackers are present where the buy needs them. For connected TV, confirm the tag is plain VAST, because VPAID, MRAID, and tag wrapping are not supported on most CTV devices.
7. Run the render-to-click QA checklist (below) before you call it trafficked. Render, impression pixel, click tracker, clickthrough, format and size match, approved or servable. A creative is not trafficked until all six pass.
8. Submit for review and confirm status. Review starts automatically and can take time, so assign and submit early. A creative must be approved or servable before the line item can serve it. A rejection is a policy problem; hand off to `dv360-troubleshooting`.

## Third-party tags and ad serving

A third-party tag is an ad-server tag that, when it serves, calls an external ad server to fetch and render the ad and to count the impression and click on that server. The platform wraps recognized tags with its own macros so the click and the auction are attributed correctly inside the buy.

- **Impression and click trackers.** The impression pixel fires when the ad renders and counts the impression on the third-party server; the click tracker fires on click and counts the click before the redirect. Both must be present and both must be secure, or one side of measurement is blind.
- **Macros.** A macro is a placeholder (for example `${CLICK_URL}`) that the platform replaces with a real value as the creative serves. For a recognized third-party tag the platform inserts the click and cachebuster macros automatically; for an unrecognized tag you insert them by hand, or clicks go uncounted and cached ads misfire.
- **Click macro and the click-tracker versus landing-URL split.** The click macro produces a two-step redirect: the click first hits the platform to record the click and the auction, then forwards to the advertiser landing URL. The click tracker field and the landing URL field are separate. Encoded variants exist (single and double URL-encoded) for tags that pass the click URL through additional redirects; pick the encoding the receiving server expects. Getting this wrong sends users nowhere or strands the click uncounted.
- **Cachebuster macro.** The cachebuster macro inserts a random number into the ad request so the browser does not serve a cached ad on a repeat view. Without it, a user who revisits a page can see a stale ad and the impression goes uncounted.
- **Secure (SSL) tags.** Every asset and tracker URL in the tag must be HTTPS. Review tests each creative for non-secure (http://) calls and flags any it finds, and a non-secure creative cannot serve on most inventory. Landing pages are the only exception to the HTTPS requirement. China-served creatives are the documented exception to SSL enforcement.
- **Attribution hygiene.** When a third-party tag is also wrapped with the platform's own ad-server tracking, configure the attribution token and the ping-for-attribution option so the same event is not double-counted as two impressions. See the misplaced-attribution guidance in Sources.

## Video and connected TV

Video creatives serve into a publisher video player via the VAST (Video Ad Serving Template) standard, an IAB Tech Lab XML schema that hands ad metadata from the ad server to the player. Get the VAST wrong and the player drops the ad.

- **VAST, and the VPAID deprecation.** VAST carries the ad and its trackers. VPAID (the older interactive runtime) is deprecated and replaced by SIMID, and it is not supported on most CTV devices and is being dropped across many SSPs. Serve plain VAST. If a creative depends on VPAID for interactivity or measurement, it will fail on inventory that no longer runs VPAID.
- **Wrapper chains and redirect timeouts.** A VAST tag can be a wrapper that redirects to another VAST document, which can wrap another, forming a chain that resolves at play time. Each hop costs time, and the player abandons the ad if the chain does not resolve inside its timeout. Keep the chain short; a deep or slow wrapper chain shows up as no ad served even though the tag is valid.
- **Why a wrong wrapper makes a CTV deal serve zero.** CTV players do not run VPAID, MRAID, or tag wrapping on most devices. Hand a CTV deal a VPAID-wrapped or otherwise non-conformant tag and every impression is rejected at the player, so the deal serves zero while looking trafficked. For CTV, deliver plain VAST that meets the publisher and device requirements.
- **Server-side ad insertion (SSAI).** With SSAI the ad is stitched into the content stream server-side rather than called by a client player, common on CTV and live. SSAI environments are even less tolerant of client-side interactivity (VPAID, MRAID) and depend on clean server-to-server VAST and correctly passed macros and trackers. Confirm the creative and its tracking survive a server-side stitch, not just a client render.
- **Companion banners.** A video creative can carry a companion display ad that renders around the player. Where the buy or the publisher expects a companion, supply it at the required size or that placement of the inventory is left unfilled.
- **Specs are not hardcoded here.** VAST versions accepted, durations, file weights, resolutions, and bitrates differ by inventory and change. Confirm the exact spec the inventory and publisher require in the current help, in Sources, rather than trusting a remembered number.

## Render-to-click QA checklist

Run all six before calling a creative trafficked. A fail blocks serving until fixed and re-checked.

1. **Does the tag render?** The creative draws in the placement at the right size, not blank, not a broken frame. Preview it; a tag that throws on load or calls a dead asset renders nothing.
2. **Does the impression pixel fire?** The impression tracker fires on render and counts on the third-party server. If it is missing or non-secure, the impression goes uncounted.
3. **Does the click tracker fire?** A test click records the click and the auction before redirecting. A missing or malformed click macro leaves clicks uncounted.
4. **Does the clickthrough land?** The redirect resolves to the correct landing URL, with the right encoding, and does not dead-end. Confirm the click-tracker-versus-landing-URL split is correct.
5. **Does it match the placement format and size?** Type and dimensions match what the line item and inventory accept. A size or format the placement does not take will not render even after it serves.
6. **Is it approved or servable?** Status is approved or servable, not pending or rejected. A line item cannot serve a creative that is not yet approved. A rejection is a policy issue for `dv360-troubleshooting`.

## Decision rules and thresholds

- **A wrong creative type or size renders nothing.** Match the creative to the line item type and the placement before anything else; a mismatch serves blank no matter how the trackers are set.
- **Non-secure means non-serving.** Any http:// asset or tracker fails review on most inventory. Make every URL except the landing page HTTPS and re-check after any tag edit.
- **The click tracker and the landing URL are two different fields.** The click macro records the click then redirects to the landing URL. Never put the landing URL in the click-tracker slot or omit the click macro; pick the encoding the receiving server expects.
- **A missing cachebuster shows stale ads.** If the platform does not recognize the third-party server, insert the cachebuster and click macros by hand, or repeat views serve cached ads and undercount.
- **For CTV, serve plain VAST only.** VPAID, MRAID, and tag wrapping are unsupported on most CTV devices, so a wrapped or VPAID tag makes the deal serve zero. Confirm the accepted VAST version with the publisher.
- **Keep the wrapper chain short.** Every redirect hop risks the player timeout. A deep or slow chain reads as no ad served even with a valid tag.
- **Trafficked means all six QA checks pass.** Render, impression, click, clickthrough, format and size, approved or servable. Submit creatives early so review time does not block launch.

## Reference material

This skill does not reproduce a spec table or a macro dictionary, because exact specs and the full macro list change and differ by placement, and a stale value causes rejected creatives, blank renders, and miscounted clicks. The authoritative, current values live on the help pages in Sources. Read them when you need an exact dimension, duration, file weight, VAST version, or the precise macro string and its encoding variants.

## Templates and examples

A third-party display tag on a display line item:

```
Hosting: third-party JavaScript tag from the advertiser's ad server
Trafficking: paste tag; confirm platform inserted ${CLICK_URL} (click) and ${CACHEBUSTER}
             (cachebuster) macros; if server unrecognized, insert both by hand
Click split: click tracker field = platform click macro -> redirects to landing URL field
Secure: every asset and tracker URL is https; landing URL may be http
QA: renders at size, impression pixel fires, test click counts and lands, status servable
```

A connected TV video deal:

```
Hosting: VAST tag URL from the advertiser's video ad server
Trafficking: serve plain VAST at the version the publisher accepts; NO VPAID, MRAID, or
             tag wrapping (unsupported on most CTV); keep any wrapper chain short
Companion: supply the companion banner at the required size if the placement expects one
Secure: VAST and all trackers over https
QA: validate VAST resolves inside the player timeout; confirm it does not serve zero on the
    deal; quartile and impression trackers present
Why: a VPAID-wrapped or non-conformant tag is rejected at the CTV player and the deal serves
     zero while looking trafficked
```

A hosted display creative with a third-party impression tracker:

```
Hosting: HTML5 assets uploaded to the platform
Trafficking: set the clickthrough URL on the creative; append the third-party impression
             tracking pixel (an https image pixel) in the tracking field
Secure: all creative assets and the tracking pixel over https
QA: renders, impression pixel fires, clickthrough lands, status approved
```

## Common pitfalls

- **Creative type or size the placement does not accept.** It serves blank. Match type and dimensions to the line item and inventory first.
- **Landing URL dropped into the click-tracker field.** The redirect breaks or the click goes uncounted. Keep the click macro and the landing URL in their separate fields.
- **Missing click or cachebuster macro on an unrecognized tag.** Clicks go uncounted and cached ads misfire. Insert both by hand when the server is not recognized.
- **A non-secure (http://) asset or tracker.** Review flags it and it cannot serve on most inventory. Make every URL except the landing page HTTPS.
- **VPAID or a wrapped tag on CTV.** The player rejects it and the deal serves zero while appearing trafficked. Serve plain VAST that meets the publisher's spec.
- **A deep or slow VAST wrapper chain.** It times out in the player and reads as no ad served. Keep the chain short and confirm it resolves.
- **No companion banner where the placement expects one.** That part of the inventory goes unfilled. Supply the companion at the required size.
- **Hardcoding a spec from memory.** Dimensions, durations, file weights, and accepted VAST versions change and differ by placement. Read the current value off the help page every time.
- **Calling a creative trafficked before QA.** Render, impression, click, clickthrough, format and size, approved or servable. All six, every creative.

## Sources

- [Manage creatives](https://support.google.com/displayvideo/answer/7530472) (as of June 2026)
- [Video creatives](https://support.google.com/displayvideo/answer/6086451) (as of June 2026)
- [Connected TV creatives](https://support.google.com/displayvideo/answer/14175098) (as of June 2026)
- [Guidelines for native creatives](https://support.google.com/displayvideo/answer/7027896) (as of June 2026)
- [Guidelines for rich media creatives](https://support.google.com/displayvideo/answer/10260435) (as of June 2026)
- [Third-party display tags](https://support.google.com/displayvideo/answer/7129061) (as of June 2026)
- [Add macros to third-party display ad tags](https://support.google.com/displayvideo/answer/2591756) (as of June 2026)
- [Macros supported by Display & Video 360](https://support.google.com/displayvideo/answer/2789508) (as of June 2026)
- [Add third-party tracking tags to a display creative](https://support.google.com/displayvideo/answer/6248876) (as of June 2026)
- [Third-party in-stream video tags](https://support.google.com/displayvideo/answer/7277709) (as of June 2026)
- [Prevent misplaced attribution for third-party tags](https://support.google.com/displayvideo/answer/9280273) (as of June 2026)
- [About secure creatives](https://support.google.com/displayvideo/answer/6022213) (as of June 2026)
- [IAB Tech Lab: Digital Video Ad Serving Template (VAST)](https://iabtechlab.com/standards/vast/) (as of June 2026)

Exact creative specifications (dimensions, file weights, durations, accepted VAST versions, bitrates) and the full macro list change over time and differ by placement and exchange, and some of the in-console creative builder sits behind login. This skill therefore states the trafficking logic and points to the pages above for any exact number or macro string, rather than asserting a value it cannot verify on a public page. Confirm the current spec there before building.

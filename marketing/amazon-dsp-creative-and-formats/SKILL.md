---
name: amazon-dsp-creative-and-formats
description: Choose the right Amazon DSP creative type, meet its requirements, and follow creative best practices for Amazon supply. Use when the user asks about Amazon DSP creative, Amazon DSP ad formats, Amazon DSP creative specs, responsive e-commerce creative, display creative, online video creative, Amazon streaming TV creative, audio creative, third-party ad tags on Amazon, or where to find the exact creative specifications.
---

# Amazon DSP creative and formats

Pick the creative type that matches the line item's product type and supply, then build it to Amazon's
requirements so it is eligible to serve. The creative is what actually runs in the impression the bidding
won, so a line item with no eligible, approved creative does not deliver no matter how the goal is set.
This skill covers the creative types, where their specs live, how third-party tags fit, and the practices
that make a creative perform on Amazon supply.

Amazon DSP is Amazon's programmatic demand-side platform for display, video, streaming TV, and audio
across Amazon properties and third-party exchanges. Its creative model is distinct from Amazon Ads
sponsored ads (Sponsored Products, Sponsored Brands, Sponsored Display), which auto-generate retail-search
ad units from product listings. DSP creatives are assets you build and assign to a line item, including
exclusive Amazon options such as responsive e-commerce creatives that an off-Amazon DSP cannot run.

This skill assumes you know what an impression, a creative, a CPM, and an ad tag are. For shared
definitions, see the `programmatic-foundations` skill.

## When to use this skill

- "What creative type do I use for this Amazon DSP line item?"
- "What are the Amazon DSP creative specs / requirements for display / video / STV / audio?"
- "What is a responsive e-commerce creative?" / "How do dynamic e-commerce creatives work?"
- "Can I run a third-party ad tag on Amazon DSP?" / "1x1 tracking, VAST tag, audio tag."
- "Amazon streaming TV creative." / "Online video creative." / "Audio creative for Amazon."
- "Why is my creative rejected / not eligible / not serving?"

Boundaries with sibling skills:
- The full order and line item build sequence (where creative assignment is the last step): hand off to
  `amazon-dsp-campaign-setup`.
- Product types and where creative sits in the hierarchy: hand off to `amazon-dsp-account-structure`.
- Which supply and deals the creative will run against: hand off to `amazon-dsp-inventory-and-supply`.
- The optimization goal the creative is being judged against: hand off to
  `amazon-dsp-bidding-and-optimization`.
- Reading creative performance (CTR, VCR, detail page views by creative): hand off to
  `amazon-dsp-measurement-and-reporting` and the `reporting-by-campaign-goal` skill.
- Uploading creatives or assigning them through the API: hand off to `amazon-dsp-api-and-automation`.

## Quick reference

Match the creative type to the line item's product type. The product type is set first and constrains
which creative is eligible.

| Creative type | Runs on | Build from | Notes |
| --- | --- | --- | --- |
| Standard display | Desktop, mobile web, mobile app | IAB-standard sizes or custom display | Third-party tags supported; assets must pass Amazon policy |
| Responsive e-commerce creative | Amazon owned-and-operated and beyond | Product (ASIN) data, auto-assembled | Amazon-exclusive; pulls price, image, rating, badges live |
| Online video (OLV) | In-stream and out-stream, desktop and mobile | Video asset, common durations | Skippable and non-skippable inventory |
| Streaming TV (STV) video | Connected TV, plus mobile and desktop video | Full-screen video asset | Full-screen, non-skippable; interactive options exist |
| Audio | Audio supply, including Amazon Music and podcasts | Audio asset plus a companion image where supported | Non-skippable; interactive audio call-to-action options exist |

A creative is eligible to serve only when it matches the line item's product type, meets the format's
current spec, and passes Amazon's creative policy review. Any one of those failing blocks delivery.

Exact dimensions, file sizes, aspect ratios, durations, bitrates, and accepted file types change and
differ by placement. Do not hardcode a number from memory. Pull the current values from the Amazon Ads ad
specs page (in Sources) before you build or hand specs to a designer.

## Core process

1. Confirm the line item's product type first. Standard display, online video, streaming TV, or audio.
   The product type is set on the line item and decides which creative type is eligible, so a creative
   built for the wrong product type cannot be assigned. Product types are covered in
   `amazon-dsp-account-structure`.
2. Choose the creative type that matches the product type and the supply. For Amazon owned-and-operated
   retail supply, a responsive e-commerce creative usually outperforms a static banner because it shows
   live price, image, rating, and badges. For broad display reach, standard display covers desktop, mobile
   web, and mobile app in one type.
3. Pull the current spec before building. Open the Amazon Ads ad specs page and read the exact dimensions,
   file size, duration, aspect ratio, bitrate, and accepted file types for that creative type and
   placement. Specs differ by placement and change over time, so this is the step that prevents rework.
4. Build or source the asset to that spec. Provide every required size and the safe-area and
   text-overlay constraints for video and STV. For a responsive e-commerce creative, supply the product
   (ASIN) and let the template assemble the unit; the live retail data fills in.
5. Add tracking and any third-party tag. Standard display supports third-party ad tags and impression and
   click trackers; video placements take a VAST tag where supported. Confirm the tag type and the secure
   (HTTPS) requirement against the current spec, and make sure click-through URLs and trackers are valid.
6. Submit for creative policy review and fix rejections. Amazon reviews creatives against its acceptance
   policies; a rejected or pending creative does not serve. Read the rejection reason and correct the
   asset or claim rather than resubmitting unchanged.
7. Assign the approved creative to the line item. A line item with no eligible, approved creative does not
   deliver. This is the final pre-launch step in `amazon-dsp-campaign-setup`.

## Creative types in depth

- **Standard display.** IAB-standard sizes or custom display units across desktop, mobile web, and mobile
  app. The most flexible type for reach and the natural home for third-party ad tags. Supply the full set
  of sizes the placements call for so the line item is eligible across its inventory.
- **Responsive e-commerce creative.** An Amazon-exclusive format assembled from product (ASIN) data. It
  renders live retail signals (price, primary image, star rating, Prime and deal badges) and adapts across
  placements, so it stays current without a manual rebuild and tends to lift retail consideration. Use it
  whenever the goal is shopping behavior on Amazon and the products are in the catalog. Pair it with the
  retail goals in `amazon-dsp-bidding-and-optimization`.
- **Online video (OLV).** In-stream (before, during, or after video content) and out-stream (in non-video
  environments) across desktop and mobile, in skippable and non-skippable inventory. Build to one of the
  accepted durations and respect the safe area for any text or logo. Confirm the exact accepted durations
  on the ad specs page rather than assuming.
- **Streaming TV (STV) video.** Full-screen, non-skippable video on connected TV plus mobile and desktop
  video. Treat it like a TV spot: the viewer cannot skip, the screen is large, and legibility and audio
  matter. Interactive options (shop with the remote or a phone scan) exist for STV. Cap exposures tightly
  on the line item, because video wears out fast (frequency is set in `amazon-dsp-campaign-setup`).
- **Audio.** Non-skippable audio across audio supply, including Amazon Music's ad-supported tier and
  podcasts available programmatically. Most placements pair the audio with a companion display image, so
  supply both. Interactive audio call-to-action options exist on some inventory. Write for the ear: a
  clear single message and a spoken call to action.

## Decision rules and thresholds

- Product type gates the creative. Decide the line item's product type first; it determines which creative
  type can be assigned. A mismatch is the most common reason a creative cannot be attached.
- Prefer responsive e-commerce creative for retail goals on Amazon supply. It shows live price, image,
  rating, and badges and updates itself, which static banners cannot, so it lifts consideration and avoids
  stale-price rebuilds. Reserve static display for cases where brand art must be pixel-controlled.
- Supply every required size and asset. A display line item missing the sizes its placements need is
  under-eligible and underdelivers; a video or audio creative missing a companion or a required duration
  may be ineligible on part of its supply.
- Match creative weight and length to the channel. STV and OLV viewers cannot skip non-skippable
  inventory, so front-load the message; audio has no visual, so carry the message in voice.
- Third-party tags are allowed on display (and VAST on video where supported) but must meet the secure-tag
  and format requirements on the current spec. A non-secure or malformed tag is rejected.
- Never assert an exact spec from memory. Dimensions, file sizes, durations, aspect ratios, bitrates, and
  accepted file types differ by placement and change. Always read the current value off the ad specs page
  before building.

## Reference material

This skill deliberately does not reproduce a spec table, because exact creative specifications change and
differ by placement, and a stale number causes rejected creatives and rebuilds. The authoritative,
current values live on the Amazon Ads ad specs page in Sources. Read it when you need a dimension, file
size, duration, aspect ratio, bitrate, or accepted file type, and when you brief a designer.

## Templates and examples

A retail-consideration display line item on Amazon owned-and-operated supply:

```
Product type: standard display
Creative type: responsive e-commerce creative
Build: supply the promoted ASIN(s); template assembles unit with live price, image, rating, badges
Tags: Amazon-native; add impression/click tracking per current spec if required
Why: live retail data lifts detail page views and never shows a stale price; pairs with a DPVR or
     ROAS goal in amazon-dsp-bidding-and-optimization
```

A streaming TV awareness line item:

```
Product type: streaming TV
Creative type: streaming TV video (full-screen, non-skippable)
Build: video to the current STV spec (read durations, aspect ratio, file type off the ad specs page);
       keep text inside the safe area; mix audio for living-room playback
Tags: VAST where supported, per current spec
Frequency: tight cap on the line item (video wears out fast); set in amazon-dsp-campaign-setup
Why: non-skippable full screen means the message lands; legibility and audio carry it
```

An audio line item on Amazon Music and podcasts:

```
Product type: audio
Creative type: audio (non-skippable) + companion display image where supported
Build: audio asset to the current spec; supply the companion image at the required size
Copy: one clear message and a spoken call to action; consider an interactive CTA on eligible inventory
Why: no skip and no guaranteed screen attention, so the voice must carry the whole message
```

## Common pitfalls

- No eligible creative assigned, so the line item does not deliver. Creative assignment is the final
  gate; confirm it in `amazon-dsp-campaign-setup` before launch.
- Creative built for the wrong product type and cannot be attached. Set the product type first, then build
  to it.
- Hardcoding a spec from memory or an old brief. Specs differ by placement and change; pull the current
  value from the ad specs page every time.
- Missing sizes or a missing companion asset. The line item is under-eligible on part of its supply and
  underdelivers. Supply the full required set.
- A static banner where a responsive e-commerce creative belongs. On retail-goal Amazon supply you lose
  live price, rating, and badges and risk showing a stale price.
- A non-secure or malformed third-party tag. It fails policy review. Meet the secure-tag and format
  requirements on the current spec.
- Resubmitting a rejected creative unchanged. Read the rejection reason and fix the asset or the claim;
  policy review will reject it again otherwise.
- Treating this as sponsored ads creative. Sponsored ads auto-build retail-search units from listings;
  DSP creatives are assets you build and assign. If the request is about search-result ad units, it is
  sponsored ads, not the DSP.

## Sources

- [Amazon Ads ad specs (creative specifications and requirements)](https://advertising.amazon.com/resources/ad-specs/) (as of June 2026)
- [Amazon DSP: Advertise with a demand-side platform](https://advertising.amazon.com/solutions/products/amazon-dsp) (as of June 2026)
- [Streaming TV ads](https://advertising.amazon.com/solutions/products/streaming-tv-ads) (as of June 2026)
- [Online video ads (in-stream and out-stream OLV)](https://advertising.amazon.com/solutions/products/online-video-ads) (as of June 2026)
- [Audio ads](https://advertising.amazon.com/solutions/products/audio-ads) (as of June 2026)
- [amzn/ads-advanced-tools-docs (official Amazon Ads advanced tools documentation)](https://github.com/amzn/ads-advanced-tools-docs) (as of June 2026)

Amazon publishes the creative format families on the pages above, but the exact, current specifications
(dimensions, file sizes, durations, aspect ratios, bitrates, accepted file types) live on the Amazon Ads
ad specs page and change over time, and some placement-level detail and the in-console creative builder
sit behind login. This skill therefore states the creative types and general requirements and points to
the ad specs page for any exact number, rather than asserting a dimension or duration it cannot verify on
a public page. Confirm the current spec there before building.

---
name: ttd-creative-and-formats
description: Brief, QA, and troubleshoot The Trade Desk creative formats across display, HTML5, video, CTV, audio, DOOH, native, companions, third-party tags, and publisher deal specs. Use when the user asks for TTD creative specs, CTV creative blockers, VAST vs VPAID, display sizes, HTML5 packaging, companion banners, or creative approval risks on The Trade Desk.
---

# TTD creative and formats

Prepare creative for The Trade Desk so a trader can upload, route, and QA it without guessing at specs. This skill uses the public Creative Specifications PDF and public CTV guidance, then marks where exact in-platform fields, publisher requirements, and account-specific review rules require partner access. It helps operators run campaigns. It does not replace a trader, traffic creative without approval, or invent gated TTD platform details.

The Trade Desk specs vary by publisher, SSP, channel, region, and deal. Treat the public spec as the base check and the publisher or private-contract spec as the final authority.

## When to use this skill

- "What creative specs do I need for The Trade Desk?"
- "Can I run this display, HTML5, native, video, CTV, audio, or DOOH creative on TTD?"
- "Why is my TTD CTV creative blocked?"
- "VAST or VPAID for CTV on The Trade Desk?"
- "What companion banners should I send?"
- "How do I brief the designer for TTD display and video?"
- "Which creative issues need an account manager or publisher check?"

Boundaries with sibling skills:
- Campaign structure and ad groups: `ttd-campaign-structure`.
- CTV and video buying strategy: `ttd-ctv-and-video-buying`.
- Inventory and deals: `ttd-inventory-and-deals`.
- Bidding and optimization: `ttd-bidding-and-optimization`.
- Reporting and attribution: `ttd-measurement-and-reporting`.
- Bulk API and automation: `ttd-api-and-automation`.

## Quick reference

| Format | Operator check |
| --- | --- |
| Display image | Use accepted image type, common IAB sizes, clear full-canvas creative, click opens a new page |
| HTML5 | Package cleanly, include dimensions in `ad.size`, provide static backup, avoid unsupported dynamic or expandable behavior unless declared |
| Third-party display tag | Confirm supported ad server, HTTPS assets, click action, cache and click tracking behavior |
| Video | Match channel, duration, aspect ratio, bitrate, and VAST support to SSP or publisher |
| CTV | Use MP4 or VAST-only third-party tags, no VPAID for CTV, check private contract go-live requirements |
| Audio | Confirm audio file, companion banner, and publisher-specific requirements |
| DOOH | Confirm screen, SSP, publisher spec, location-specific dimensions, and whether the creative is static or video |
| Native | Supply the required image, logo, title, body, sponsor, CTA, and app or price fields where relevant |

## Core process

1. Identify the channel and hosting model. Record whether the asset is display, HTML5, native, audio, video, CTV, DOOH, hosted by The Trade Desk, or third-party hosted. The hosting model controls tracking and review.
2. Get the final spec owner. For open-market display, the public spec may be enough. For CTV, DOOH, PMP, and Programmatic Guaranteed, ask for the publisher, SSP, or private-contract spec. The public document says specs can vary by publisher and SSP, and those differences matter.
3. Check the asset against the base public spec. Validate file type, dimensions, file size, animation, duration, orientation, border, click action, audio loudness, companion, and fallback requirements.
4. Check the deal-specific spec. For private contracts and CTV, the go-live check can verify whether the creative format meets publisher requirements. Do not wait until activation day to discover a mismatch.
5. Confirm CTV safety. For CTV, use hosted video or third-party VAST tags. VPAID tags are not supported for CTV, and a VPAID dependency is one of the most common blockers.
6. Confirm tracking and measurement. Hosted video can carry third-party tracking pixels. Third-party hosted creatives depend on the ad server and publisher support. Do not assume every impression or viewability tracker works on every inventory type.
7. Share creative with the publisher when required. TTD's public CTV guidance recommends sharing the creative with publishers before activation to verify spec compliance.
8. Human-gate activation. The skill can produce the spec brief and QA findings. A trader or ad-ops owner approves upload, activation, budget movement, and live changes.

## Decision rules and thresholds

- Publisher and SSP specs override the public base spec. This is explicit in TTD's public specs, especially for CTV and DOOH.
- For CTV, VAST only. Do not upload VPAID tags for CTV. If the measurement vendor requires VPAID, find another measurement path or inventory type.
- Use hosted video for the broadest CTV compatibility when possible. Public TTD guidance recommends hosted video ads with the highest quality for publisher compatibility.
- Keep one tag per creative media asset on CTV. Do not rotate creative files through a single tag if the publisher or TTD guidance expects one media asset per tag.
- Upload the highest-quality source video you have. TTD does not upscale or stretch uploaded video assets.
- HTML5 needs a backup image. If JavaScript fails or is disabled, the backup prevents a blank render.
- DOOH is publisher-specific by design. Screen dimensions, file type, animation, duration, and location rules need the SSP or publisher spec.

## Format QA checklist

- Channel and hosting model recorded.
- Public spec checked for file type, dimensions, size, duration, and audio.
- Publisher, SSP, or deal spec checked where applicable.
- Creative is not sideways, segmented, illegible, or missing a border on partial black or white backgrounds.
- Click action opens a new page.
- Animation and auto-start video limits are respected for display.
- HTML5 package includes `ad.size` and static backup.
- CTV uses hosted video or VAST-only third-party tag, no VPAID dependency.
- Video duration and bitrate meet the publisher or contract spec.
- Companion banners exist when the buy requires them.
- Tracking pixels and viewability setup are supported for the inventory type.
- Private-contract go-live check risk is cleared before launch day.

## Templates and examples

Display brief:

```text
Channel: Display
Formats: 300x250, 300x600, 160x600, 728x90, 970x250
File type: GIF, JPEG, or PNG, with HTML5 only if packaged and backed up correctly
Creative rules: full-canvas asset, legible text, not sideways, border if partial black or white background
Click: opens a new page
Final check: confirm region and exchange availability in platform or with account manager
```

CTV brief:

```text
Channel: Connected TV
Hosting: TTD-hosted video preferred, or third-party VAST tag
Do not use: VPAID for CTV
Asset: MP4 source, highest-quality available, audio loudness checked to publisher spec
Deal check: publisher spec, private contract requirements, and go-live check reviewed before activation
Tracking: confirm third-party tracking pixels are supported for this publisher and device path
```

DOOH brief:

```text
Channel: DOOH
Spec source: SSP or publisher screen spec, not just the general TTD PDF
Required checks: screen dimensions, file type, duration, audio allowed or not, location restrictions
Approval: publisher and trader sign-off before activation
```

## Common pitfalls

- Treating a public display size list as a guarantee of supply in every region.
- Using VPAID for CTV and then wondering why the creative blocks delivery.
- Skipping publisher specs for CTV, DOOH, PMP, or Programmatic Guaranteed.
- Uploading low-quality source video and expecting the platform to upscale it.
- Rotating multiple CTV media files through one tag.
- Forgetting the static backup image for HTML5.
- Assuming third-party measurement works on every device and SSP.
- Waiting until launch day for the private-contract creative check.

## Sources

- [The Trade Desk Creative Specifications PDF](https://www.thetradedesk.com/assets/global/documents/Creative_Specifications-en.pdf) (as of July 2026)
- [Best practices for uploading your Connected TV creative, The Trade Desk](https://www.thetradedesk.com/resources/best-practices-for-uploading-your-ctv-creative) (as of July 2026)
- [The Trade Desk Partner Portal Creative API reference](https://partner.thetradedesk.com/v3/portal/api/doc/Creative) (partner-gated, checked as public URL July 2026)

---
name: dv360-video-creative-specs
description: Prepare, QA, and troubleshoot DV360 video creative specifications for hosted video, third-party VAST tags, companions, tracking URLs, duration, aspect ratio, transcodes, and CTV readiness. Use when the user asks for DV360 video specs, VAST versions, file formats, duration, size, bitrate, companion banners, third-party video tags, or why a DV360 video creative is rejected or not eligible.
---

# DV360 video creative specs

Prepare video assets for Display & Video 360 so they pass review, transcode correctly, match the inventory, and carry the tracking a trader needs. This skill is the current spec reference companion to `dv360-creative-trafficking`. It helps an operator brief, QA, and troubleshoot creative. It does not replace the operator's final spec check in DV360, Campaign Manager 360, or the publisher deal terms.

DV360 video specs change by inventory source and exchange. Use this skill to know what to check, then confirm exact requirements in the current official help and the publisher or deal spec before shipping.

## When to use this skill

- "What specs should I send the video team for DV360?"
- "Does DV360 support this video file type, duration, aspect ratio, or VAST version?"
- "Why did my video creative fail review or transcode?"
- "What companion banners do I need?"
- "Can I use a third-party VAST tag?"
- "CTV creative is uploaded but the deal serves zero."
- "What tracking URLs can I add to a video creative?"

Boundaries with sibling skills:
- Creative serving, click tracking, macros, secure tags, and render-to-click QA: `dv360-creative-trafficking`.
- YouTube and YouTube & partners video formats: `dv360-youtube-and-video`. This skill covers DV360 video creatives and does not apply to YouTube videos in YouTube & partners line items.
- CM360 video placement and ad-server wrapping: `cm360-trafficking-and-ad-tags`.
- CTV supply, ad pods, and pod-level buying logic: `ctv-supply-and-ad-pods`.

## Quick reference

Always verify in the current help before briefing a designer, but these are the public DV360 defaults to check first.

| Area | Current public DV360 guidance |
| --- | --- |
| Hosted video file types | `.avi`, `.mov`, `.mp4`, `.m4v`, `.mpeg`, `.mpg`, `.webm`, `.wmv` |
| Source file size | Hosted source files can be large, up to 1 GB on the guideline page |
| Serving file size | Transcoded serving files must be 10 MB or less to remain servable |
| Common best-practice lengths | 15 or 30 seconds, with inventory also supporting other durations |
| VAST support | VAST 2.0, 3.0, and 4.0, with wrapper depth kept short |
| Codec guidance | H.264 video, AAC or PCM audio, 48 kHz audio sample rate |
| Recommended dimensions | Landscape, portrait, and square source files at high resolution |
| Companions | Optional display creatives around the player, commonly 300x250, 728x90, and 300x60 |
| Tracking URLs | Impression, click, start, quartiles, complete, skip, pause, mute, full screen, and custom |

Publisher, exchange, CTV, and deal specs can be stricter than the general help. The stricter spec wins.

## Core process

1. Identify the serving path. Confirm whether the creative is a hosted video file in DV360, a CM360-synced video, or a third-party VAST tag. The path determines upload, tracking, companion, and troubleshooting steps.
2. Confirm the inventory context. Record line item type, exchange, deal ID, CTV versus web or app, skippable versus non-skippable, max duration, companion requirements, and any publisher spec sheet. General DV360 specs are not enough for a private deal.
3. Check the source asset. Verify file type, orientation, aspect ratio, duration, audio, resolution, file size, and whether subtitles are burned into the video when needed. DV360 video creatives do not support closed caption or `.srt` files, so captions must be inside the video.
4. Upload and inspect transcodes. After upload, check every generated serving file. If all serving files are over 10 MB or no servable file type remains, the creative cannot serve as intended.
5. Set the landing page or click tracker correctly. For a click tracker that redirects, enter it as the landing page URL in the asset setup. Do not add raw HTML to tracking URL fields.
6. Add tracking URLs. Use the built-in video tracking URL types for impression, click, start, first quartile, midpoint, third quartile, complete, mute, pause, rewind, full screen, stop, skip, progress, and custom events.
7. Add companions only when they are useful or required. Companion creatives are optional on most video inventory but can matter for publisher packages. Confirm whether the deal expects them and add each companion size once.
8. Validate third-party VAST tags. Confirm the tag resolves, the wrapper chain is short, the duration matches the actual media, and the tag is acceptable to the exchange or publisher. Wrapped tags can change duration and cause delivery into the wrong ad slot.
9. Run CTV-specific checks. For CTV, prefer plain VAST that the publisher accepts, avoid interactive dependencies that CTV cannot run, and confirm the publisher's device and SSAI requirements.
10. Submit early and check status. DV360 runs automated and manual creative review. A video asset is not ready until status is approved or servable and the exact line item or deal accepts it.

## Decision rules and thresholds

- The publisher or deal spec overrides the generic DV360 spec. If a PG or PMP deal requires a different bitrate, duration, companion, or VAST version, follow the deal.
- A source file is not the serving file. DV360 may accept a large source but drop serving files over the serving-file limit. Inspect transcodes before launch.
- Keep VAST wrappers short. DV360 supports wrappers, but long wrapper chains are a common player timeout and no-ad cause.
- Do not rely on `.srt` captions. Burn subtitles into the video if caption text must appear.
- Match duration to inventory. A 22-second video can fit 30-second inventory, but duration mismatch across rotating videos and wrapped tags can cause rejected or cut-off delivery.
- CTV is stricter than desktop video. Use CTV-safe VAST, check SSAI and publisher specs, and do not assume desktop VPAID-style measurement will work.
- Tracking is only useful if it fires. Preview and test tracker calls before calling the asset trafficked.

## QA checklist

Use this before handing the creative to the trader or launching a line item.

- Serving path confirmed: hosted DV360, CM360-synced, or third-party VAST.
- Inventory context recorded: web video, app video, CTV, deal, exchange, skippable status, duration.
- Source file type and orientation accepted.
- Duration matches the slot or publisher threshold.
- Audio is present when required and not out of spec.
- Captions are burned in if needed.
- Transcoded serving files include at least one servable file at or below the serving limit.
- Landing page or redirecting click tracker is in the right field.
- Tracking URLs added and formatted without HTML wrappers.
- Companion creatives added only where required or useful.
- VAST tag resolves and wrapper chain is short.
- Creative status is approved or servable.
- Publisher or deal-specific spec sheet has been checked.

## Templates and examples

Hosted DV360 video:

```text
Asset: 30-second MP4, 1920x1080, H.264, AAC audio, captions burned in.
Upload path: DV360 advertiser > Creatives > New > Upload > Video file.
After upload: confirm generated serving files include at least one <= 10 MB.
Tracking: add impression, start, quartiles, complete, skip, and click tracking URLs.
Companion: add 300x250 and 728x90 only if the package expects companions.
Launch gate: creative approved, assigned to video line item, publisher spec checked.
```

Third-party VAST tag:

```text
Asset: third-party VAST tag from ad server.
Check: tag resolves, duration in VAST matches media, wrappers limited, HTTPS throughout.
Tracking: confirm third-party server handles quartiles and click tracking, add DV360 tracking if needed.
CTV: confirm the publisher accepts this VAST and does not reject the tag in SSAI.
Launch gate: preview works and the line item/deal accepts the creative.
```

## Common pitfalls

- Treating the general help page as the deal spec. Deals and publishers can be stricter.
- Uploading a large source and never checking whether the serving files stayed under the limit.
- Using a VAST wrapper that changes the creative duration.
- Missing the landing page URL or putting a click tracker in the wrong place.
- Adding tracking URLs with HTML tags instead of plain URLs.
- Assuming companions always serve or always count separately.
- Sending `.srt` files and expecting DV360 to display closed captions.
- Using desktop video assumptions on CTV inventory.

## Sources

- [Guidelines for video creatives, Display & Video 360 Help](https://support.google.com/displayvideo/answer/3129957) (as of July 2026)
- [Video creatives, Display & Video 360 Help](https://support.google.com/displayvideo/answer/6086451) (as of July 2026)
- [Third-party in-stream video tags, Display & Video 360 Help](https://support.google.com/displayvideo/answer/7277709) (as of July 2026)
- [Connected TV creatives, Display & Video 360 Help](https://support.google.com/displayvideo/answer/14175098) (as of July 2026)
- [IAB Tech Lab VAST standard](https://iabtechlab.com/standards/vast/) (as of July 2026)

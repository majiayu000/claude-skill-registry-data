---
name: cm360-trafficking-and-ad-tags
description: Build the Campaign Manager 360 object hierarchy and traffic a campaign end to end so it serves, tracks, and clicks through. Use when the user asks how to traffic a CM360 campaign, set up an advertiser, campaign, site, placement, ad, or creative, generate or download placement tags, pick a tag type (JavaScript, iframe, standard, tracking ad, click tracker, INS, pre-fetch), fix a macro or cachebuster, set the ord value, wire a click command, or run pre-launch trafficking QA.
---

# CM360 trafficking and ad tags

The deliverable is a Campaign Manager 360 campaign that serves: every placement has a tag the publisher can drop in, every ad points at an approved creative, the impression and click counters fire, the ord cachebuster is in place, and the click command lands the user on the right page. Trafficking is the ad-ops job in an ad server. A placement whose tag is malformed, whose ord is static, or whose click command is missing counts nothing and wastes the media the buy paid for.

This skill covers the CM360 object model (account, advertiser, campaign, site, placement, ad, creative), the tag types CM360 generates, the macros inside those tags, and a trafficking QA pass. It assumes you know what an impression, a click, a placement, and an ad tag are. For shared definitions see the `programmatic-foundations` skill.

## When to use this skill

- "How do I traffic a campaign in CM360?" / "Set up the advertiser, campaign, placement, ad."
- "Which tag type do I give the publisher?" / "JavaScript vs iframe vs standard vs INS tag."
- "How do I generate and download placement tags?" / "The publisher needs the tag sheet."
- "What is the ord parameter / cachebuster and why is my count zero?"
- "What does the click= command do?" / "Set up a click tracker or a tracking ad."
- "What does %eadv! / %epid! / %n expand to?" / "Which macro carries the advertiser ID?"
- "Run trafficking QA before this launches." / "Why is this placement not counting?"
- "The tag needs GDPR/GPP consent macros for EU traffic."

Boundaries with sibling skills. This skill owns the trafficking mechanics: hierarchy, placements, ads, tag output, macros, and the QA that a tag will serve and count.
- Floodlight activities, conversion counting methods, conversion windows, and the Conversions API: hand off to `cm360-floodlight-and-conversions`. That skill owns the conversion side, this one owns the media-serving side.
- Wiring CM360 Floodlight to GA4, DV360, and SA360, and keeping one attribution model across Google Marketing Platform: `gmp-integration-floodlight-ga4-linking`.
- Deduping counts across CM360, GA4, and each DSP into a blended KPI: `cross-platform-conversion-reconciliation`.
- Trafficking creatives inside DV360 (not the CM360 ad server): `dv360-creative-trafficking`.
- Tag and pixel governance across the whole stack: `tag-and-pixel-governance`.

## Quick reference: the CM360 object hierarchy

Traffic top down. Each level inherits defaults from the level above (landing page, conversion window, tag settings), so set the default high and override only where you must.

| Level | What it is | You create it to |
| --- | --- | --- |
| Account | The CM360 network | Hold advertisers, users, and network defaults (set once) |
| Advertiser | One brand or client | Group its campaigns, default landing page, and Floodlight config |
| Campaign | One flight or initiative | Set start/end dates, default landing page, billing code, EU political declaration |
| Site | A publisher property | Represent where inventory runs, so a placement can attach to it |
| Placement | One ad slot on a site | Emit one placement tag, carry size, compatibility, dates, and pricing |
| Creative | The asset (image, HTML5, video, native) | Hold the file or third-party tag the ad displays |
| Ad | The rule joining creatives to a placement | Decide which creative serves in a placement and rotate/target |

CM360 builds an ad for each creative-placement assignment. Assign creatives to placements and CM360 creates the ads, assigns the creatives to them, and assigns the ads to the placements. You choose one ad for all creatives, or one ad per placement.

## Quick reference: which tag type to hand the publisher

| Situation | Tag type | Why |
| --- | --- | --- |
| Publisher accepts a general tag, serves image or rich media | Iframe/JavaScript | The most common type; delivers both standard images and rich media with fallbacks |
| Publisher uses a custom layout or its own iframe and avoids CM360 iframes | JavaScript | Delivers image, HTML5, and rich media without CM360 wrapping an iframe |
| 1x1 slot, image only | Standard | Only serves image files on a 1x1 placement; no rich media, no impression event tags |
| Publisher serves the ad through Google Ad Manager | Internal redirect (INS) | Lower latency, click consistency, and richer domain info in Verification |
| In-stream video or audio | Pre-fetch | Sends the ad content first and logs the impression after load; supports VAST 2.0/3.0/4.0 |
| Third-party or hardcoded creative you only need to count | Click tracker | Records clicks on non-CM360-served creatives, text links, emails; cache busting is automatic |
| Third-party ad where you need impressions and clicks | Tracking ad | Records impressions and clicks; easier than a separate pixel plus click tracker |

Do not hardcode a tag string from memory. Generate the tag from the placement in CM360 so the account, site, placement, and macro settings are correct, then download or send it. The full tag-type and macro map is in `references/tag-types-and-macros.md`.

## Core process

1. Confirm the advertiser and its defaults exist. The advertiser carries the default landing page and the Floodlight configuration every campaign under it inherits. Trafficking into the wrong advertiser puts the spend under the wrong Floodlight config and the wrong reporting rollup.
2. Create the campaign with real dates and a billing code. Start and end dates set the reporting period (they do not by themselves stop serving, so ad-level dates still matter). Set the campaign default landing page, the billing invoice code for reconciliation, and complete the EU political ads self-declaration, which is required.
3. Create or pick the sites. A site represents a publisher property. A placement must attach to a site, so stand the site up before the placement.
4. Create the placements. One placement equals one ad slot and emits one placement tag. Set compatibility (display, in-stream video, in-stream audio), size, active dates, and pricing. Placement active dates gate serving; get them right or the slot serves nothing or serves past flight.
5. Load the creatives. Upload hosted assets (image, HTML5) or paste the third-party tag, at the size the placement accepts. A creative whose size the placement does not accept will not render even after the ad serves.
6. Assign creatives to placements to build the ads. CM360 creates a default (standard) ad per creative-placement assignment, or one ad for all creatives, or one ad per placement, per your choice. Set rotation and any targeting on the ad.
7. Set the click-through URL and click command. The ad or creative carries the landing URL; the click command (`click=`) in the tag records the click on CM360 and, when a third party needs its own count, redirects through it. Keep the landing URL and the click command in their correct fields.
8. Confirm the ord cachebuster. Every served tag needs a unique random ord value per load so the browser does not serve a cached ad and miss the count. CM360 tags carry the `%n` random-number macro or the publisher populates `ord=` from its own counter. A static ord undercounts.
9. Add consent macros where the traffic needs them. For EU and other consent-gated traffic, include the TCF GDPR macros and, where required, the GPP macros so downstream vendors receive the consent string. CM360 tag generation exposes these options.
10. Generate, QA, then download or send the tags. Generate the placement tags, run the QA pass below, then hand the tag sheet to the publisher. Do not send tags that have not passed QA; a bad tag serves live and counts wrong until someone notices.

## Decision rules and thresholds

- **Traffic top down and override sparingly.** Landing page, conversion window, and tag defaults inherit from account to advertiser to campaign to placement. Set the default once high; override at the placement only when that slot genuinely differs. Overriding everywhere hides the intended default and makes reconciliation harder.
- **Match the tag type to the publisher, not to habit.** Iframe/JavaScript is the default for image plus rich media. Drop to standard only for a 1x1 image-only slot (it cannot carry impression event tags). Use INS when the ad serves through Google Ad Manager. Use pre-fetch for in-stream video/audio. The wrong type either will not render or will not count.
- **Tracking ad vs click tracker.** A click tracker records clicks only, on a creative CM360 does not serve. A tracking ad records both impressions and clicks and is easier than pairing an impression pixel with a click tracker. If you need impressions counted on a third-party creative, use a tracking ad, not a click tracker.
- **A static or missing ord means undercounting.** The ord value must be a unique random number per tag load (alphanumeric and periods, 8 characters minimum, 10 to 15 preferred). CM360-served tags use the `%n` macro; publisher-served tags populate `ord=` from their counter. Click tracker tags need no ord, because cache busting on clicks is automatic. A fixed ord makes the browser serve a cached ad and the impression goes uncounted.
- **The click command and the landing URL are separate.** `click=` records the click on CM360 (and optionally redirects through a third party for its own count) before sending the user to the landing URL. Never drop the landing URL into the click-command slot or omit `click=`; you break the redirect or leave clicks uncounted.
- **EU political and consent are not optional.** The EU political ads declaration is required at the campaign. For EU and other consent-gated traffic, include the TCF GDPR macros (and GPP macros where required) in the generated tag, or downstream vendors receive no consent signal and may drop the call.
- **Generate tags from CM360, never hand-write them.** A hand-typed tag drifts from the account, site, placement, and macro settings. Generate from the placement so the IDs and macros are correct, then download or send.

## Reference material

- `references/object-hierarchy-and-placements.md`: the account-to-ad object model, what each level owns and inherits, placement compatibility and properties, packages and roadblocks, ad types (standard, tracking, click tracker), and how creative-placement assignment builds ads. Read this when structuring a new campaign or deciding where a setting belongs.
- `references/tag-types-and-macros.md`: every CM360 placement tag type mapped to its use, and the full CM360 macro table (%n, %c, the %e-accessor ID macros like %eadv!/%epid!/%ecid!/%eaid!, %edclid!, %g, %u, and the click=/adj parameters), plus the ord cachebuster mechanics and the TCF GDPR and GPP consent macro options. Read this when picking a tag type, reading a macro, or debugging a count.
- `references/trafficking-qa-checklist.md`: the pre-launch QA pass (hierarchy, placement dates and size, creative-ad assignment, click command and landing URL, ord/cachebuster, secure calls, consent macros, tag delivery) with the failure each check catches, plus the CM360 Trafficking API v5 resource and method map for automating and auditing at scale. Read this before sending tags or when auditing a live campaign.

## Templates and examples

A standard display placement handed to a publisher:

```
Hierarchy: Advertiser "Acme Retail" > Campaign "Acme Q3 Prospecting" (2026-07-01 to 2026-09-30,
           billing code ACME-Q3-DISP, EU political declaration completed)
Site: "PublisherX.com"
Placement: "PubX_ROS_300x250" size 300x250, compatibility Display, active 2026-07-01 to 2026-09-30
Creative: hosted HTML5 300x250, clickthrough https://acme.com/summer
Ad: standard ad, one creative-placement assignment, even rotation
Tag type given to publisher: Iframe/JavaScript
Cachebuster: %n random-number macro present in the tag
Click command: click= present; landing URL in the ad's clickthrough field (not in click=)
QA: renders at 300x250, impression counts, test click records and lands, ord unique per load
```

A click tracker on a hardcoded email creative:

```
Purpose: count clicks on a creative CM360 does not serve (a link in a client newsletter)
Object: click tracker ad on a placement; no image served, clicks only
Tag: click tracker tag; no ord needed (click cache busting is automatic)
Click command: click= records the click on CM360, then redirects to the landing URL
QA: test click records in CM360 and lands on the correct page
Note: if the client also needs impressions counted, switch to a tracking ad, not a click tracker
```

An in-stream video placement:

```
Placement compatibility: In-stream video
Creative: video creative or third-party VAST tag at the accepted VAST version
Tag type: Pre-fetch (sends ad content first, logs impression after load; VAST 2.0/3.0/4.0)
Consent: TCF GDPR macros included for EU traffic; GPP macros where the vendor requires them
QA: VAST resolves in the player timeout, impression logs after load, quartile trackers present
```

## Common pitfalls

- **Trafficking under the wrong advertiser.** The spend inherits the wrong Floodlight config and lands in the wrong reporting rollup. Confirm the advertiser and its default landing page and Floodlight config before building the campaign.
- **Placement active dates wrong.** A placement that starts late serves nothing; one that never ends serves past flight and overspends. Set placement active dates to the flight, and remember campaign dates set the reporting period, not the serving stop.
- **Wrong tag type for the publisher.** A standard tag on a rich-media slot will not render; a standard tag cannot carry impression event tags. Match the type to the publisher and the creative, defaulting to iframe/JavaScript.
- **Static or missing ord.** The browser serves a cached ad and the impression goes uncounted. Confirm the `%n` macro is in the served tag, or that the publisher populates `ord=` uniquely per load.
- **Landing URL in the click-command slot, or a missing click= command.** The redirect breaks or clicks go uncounted. Keep the landing URL in the ad's clickthrough field and `click=` as the click command.
- **Click tracker used where impressions are needed.** A click tracker counts clicks only. Use a tracking ad when the third-party creative also needs impressions.
- **Consent macros omitted on EU traffic.** Downstream vendors receive no consent string and may drop the call, and the campaign is not defensible. Include the TCF GDPR macros (and GPP where required) at tag generation, and complete the EU political declaration.
- **Hand-written tags.** A hand-typed tag drifts from the real placement and macro settings and counts wrong. Generate the tag from CM360, QA it, then send it.
- **Sending tags before QA.** A bad tag serves live and miscounts until caught. Run the QA pass in `references/trafficking-qa-checklist.md` before you download or send.

## Sources

- [Overview of Campaign Manager 360](https://support.google.com/campaignmanager/answer/2709362?hl=en) (as of July 2026)
- [Trafficking workflow](https://support.google.com/campaignmanager/answer/3419088?hl=en) (as of July 2026)
- [Set up a campaign](https://support.google.com/campaignmanager/answer/2838056?hl=en) (as of July 2026)
- [Create, copy, or archive placements](https://support.google.com/campaignmanager/answer/2829205?hl=en) (as of July 2026)
- [Ads overview](https://support.google.com/campaignmanager/answer/2837647?hl=en) (as of July 2026)
- [Ad creation for creative-placement assignments](https://support.google.com/campaignmanager/answer/3414002?hl=en) (as of July 2026)
- [Placement tags](https://support.google.com/campaignmanager/answer/2826636?hl=en) (as of July 2026)
- [Campaign Manager 360 macros](https://support.google.com/campaignmanager/table/6096962?hl=en) (as of July 2026)
- [Set up tracking ads](https://support.google.com/campaignmanager/answer/3040965?hl=en) (as of July 2026)
- [ORD values](https://support.google.com/campaignmanager/answer/2828443?hl=en) (as of July 2026)
- [Campaign Manager 360 REST API (v5)](https://developers.google.com/doubleclick-advertisers/rest) (as of July 2026)
- [Campaign Manager 360 API changelog](https://developers.google.com/doubleclick-advertisers/changelog) (as of July 2026)
- [Campaign Manager 360 API deprecation schedule](https://developers.google.com/doubleclick-advertisers/deprecation) (as of July 2026)

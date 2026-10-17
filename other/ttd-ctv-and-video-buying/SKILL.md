---
name: ttd-ctv-and-video-buying
description: Run a live connected TV and video book on The Trade Desk in Kokai. Use when the user asks about "TTD CTV", "Trade Desk connected TV", "TTD video buying", "Kokai CTV", "Ventura ecosystem", "curated CTV marketplace", "CTV pause ads", "live events forecasting on TTD", "live sports on The Trade Desk", "Koa on video", "Sincera ad quality", "OpenPath for CTV", or how to make CTV inventory addressable with UID2 or EUID.
---

# TTD CTV and video buying

Plan, build, and optimize a connected TV (CTV) and video campaign on The Trade Desk in the
Kokai platform, including where premium video supply comes from (Ventura, OpenPath, curated
CTV marketplaces), how to make it addressable (UID2 and EUID on logged-in inventory), the newer
video formats (CTV pause ads, live events), and how Koa AI assists the buy. CTV is The Trade
Desk's flagship channel, so this is the video-specific playbook, not general inventory or
identity theory.

This skill assumes you know what a CPM, a completed view, a video completion rate (VCR), an ad
pod, and a deal ID are. For those definitions and the shared KPI math, see the
`programmatic-foundations` skill. For DSP-agnostic CTV supply mechanics (ad pods, competitive
separation, pod position, frequency in pods), see the `ctv-supply-and-ad-pods` skill.

A sourcing note that governs the whole TTD skill set: The Trade Desk's operational knowledge base
and API reference sit behind a partner login, and in-platform help is visible only to logged-in
seat holders. Everything here comes from public pages. Where an exact menu path, field name,
endpoint, or number would need platform access, this skill states the public concept and flags
that the specifics live in the partner platform. It does not invent screen names or values.

## When to use this skill

- "How do I run CTV / connected TV / streaming video on The Trade Desk?"
- "What is the Ventura ecosystem and should I buy through it?"
- "Set up a curated CTV marketplace / curated CTV deal on TTD."
- "What are CTV pause ads and how do I use them?"
- "How do I plan a live sports or live event CTV flight on The Trade Desk?"
- "What does live events forecasting do?"
- "How do I make CTV inventory addressable with UID2 / EUID?"
- "What does Koa do on a video buy?" / "What is Sincera / improved ad quality controls?"
- "Why is my CTV line under-delivering / capping frequency wrong / running the wrong pod?"

Boundaries with sibling skills. This skill is the CTV and video buying playbook on The Trade
Desk. Hand off when the task is not video-specific:

- General inventory access paths (open market, PMP, Programmatic Guaranteed, OpenPath mechanics)
  across all channels: `ttd-inventory-and-deals`. This skill uses those paths for video and
  does not redefine them.
- The UID2 and EUID identifier model (how a token is generated, rotated, decrypted): the
  `ttd-identity-and-uid2` skill. This skill applies that identity to CTV addressability only.
- Audience building and contextual targeting on top of the inventory: `ttd-targeting-and-audiences`.
- Bid pricing, pacing, and optimization mechanics: `ttd-bidding-and-optimization`.
- Campaign and ad group hierarchy: `ttd-campaign-structure`.
- Reporting, attribution, measurement: `ttd-measurement-and-reporting`, with goal framing in
  `reporting-by-campaign-goal`.
- Bulk API and automation of any of the above: `ttd-api-and-automation`.
- Platform orientation and Kokai/Koa basics: `ttd-platform-overview`.

For how a walled garden approaches the same CTV problem when a client also runs Google DV360,
see `dv360-youtube-and-video` and `dv360-deals-and-inventory`. This skill does not configure
DV360.

## Quick reference

| The goal | Reach for | Why |
| --- | --- | --- |
| Premium, transparent CTV supply at scale | Ventura ecosystem plus OpenPath direct paths | Shortens the CTV supply chain and adds bid-data transparency |
| One-click access to top CTV publisher inventory | Curated CTV marketplace in the Deal Desk | Pre-curated biddable CTV supply without negotiating each deal |
| Reserved premium CTV (sponsorship, tentpole, roadblock) | Programmatic Guaranteed via `ttd-inventory-and-deals` | Fixed price, guaranteed delivery for must-run flights |
| Engage a paused viewer on the big screen | CTV pause ad format | Non-interruptive, complements the viewing experience |
| Plan a live sports or live event flight | Live events forecasting before you commit | Predicts spend, reach, impressions for spiky, time-boxed demand |
| Make logged-in CTV addressable | UID2 / EUID on authenticated inventory | Deterministic identity survives cookieless and no mobile ad ID |
| Filter low-quality video supply | Improved ad quality controls (Sincera) | Deeper inventory-quality evaluation before you bid |
| Let AI guide the video optimization | Koa via Advanced AI controls | Steer optimization toward performance, price, or your priority |

Kokai is the current generation of the platform (Solimar is retired). Everything below runs in
the Kokai experience. Nothing here should reference Solimar as current.

## Core process

1. **Name the video objective and the currency first.** Upper-funnel reach and brand favor CTV,
   online video, and live events measured on reach, VCR, and completed views. Lower-funnel favors
   video with conversion or outcome measurement in place. The objective picks the supply mix, the
   format, and the KPI, so fix it before touching inventory. Frame the KPI with
   `reporting-by-campaign-goal`.
2. **Choose the CTV supply path.** Decide among open market video, curated CTV marketplace, PMP,
   Programmatic Guaranteed, and OpenPath direct supply, and whether to buy through the Ventura
   ecosystem for a shorter, more transparent CTV chain. Supply mechanics live in
   `ttd-inventory-and-deals`; this skill maps them to video in the reference file.
3. **Curate CTV supply in the Deal Desk.** Use a curated CTV marketplace to reach top publisher
   inventory as biddable supply without negotiating each deal, then tighten with the upgraded
   Deal Desk (customizable lookback windows, filters, metadata). Curating up front is cheaper
   than blocking bad supply after it spends.
4. **Make the inventory addressable.** On logged-in CTV, apply UID2 (or EUID for European and UK
   traffic) so first-party audiences resolve deterministically. CTV has no third-party cookie and
   no mobile ad ID to fall back on, so authenticated identity is the addressability layer. The
   identifier model is in `ttd-identity-and-uid2`; audience build-out is in
   `ttd-targeting-and-audiences`.
5. **Pick the video format to the moment.** Standard in-stream video for reach and storytelling,
   CTV pause ads to engage a viewer who paused without interrupting playback, and live events for
   tentpole and live sports moments. Match creative specs to the channel and the deal.
6. **Set frequency and competitive separation at the pod and household level.** CTV serves in ad
   pods, so manage frequency across the household and guard against the same or competing brand
   appearing twice in one pod. Pod mechanics live in `ctv-supply-and-ad-pods`; apply them here.
7. **Turn on the quality and AI controls, human-gated.** Enable improved ad quality controls
   (Sincera) to evaluate inventory quality, and use Koa via the Advanced AI controls to guide
   optimization toward your priority (performance, price, or another goal). Read Koa's
   recommendations and approve changes; do not auto-apply spend or live-config changes.
8. **Forecast before you commit spikes.** For live events and live sports, run live events
   forecasting to estimate spend, reach, and impressions, because live demand is spiky and
   time-boxed and cannot be paced like evergreen inventory. Human-approve the plan before booking.
9. **Launch, then read against the objective.** Verify delivery, VCR, reach, frequency, and pod
   position, and reconcile platform-reported reach against the contracted measurement currency
   where a guaranteed flight requires it. See `ttd-measurement-and-reporting` and, for currency
   reconciliation, the `ctv-measurement-currencies` skill.

## Decision rules and thresholds

- **Lead with the objective, then the supply path.** Brand and reach weight toward curated CTV,
  PMP, Programmatic Guaranteed, and live events. Performance weights toward biddable video with
  measurement in place. Most plans blend paths.
- **Curate before you block.** A curated CTV marketplace filters to quality supply up front, which
  is cheaper and cleaner than bidding broadly and blocking waste after it spends. Turn on improved
  ad quality controls (Sincera) so the quality signal informs the bid, not just a post-hoc report.
- **Prefer the shorter, more transparent CTV path.** When the same CTV supply is reachable through
  Ventura or OpenPath (a direct connection to the seller with bid-data visibility) and through a
  longer chain, the direct path usually means more transparency and fewer fees skimmed by
  intermediaries that add little value. Ventura targets exactly the CTV supply-chain opacity
  problem, so weight toward it for premium CTV where path quality matters.
- **Programmatic Guaranteed for must-deliver, sized to need.** Reserve fixed-price CTV volume only
  for sponsorships, roadblocks, and tentpoles that cannot miss. Guaranteed volume is an
  obligation; size it to the reserved need and let auction supply flex around it.
- **A floor is a hard gate.** If the bid cannot clear the CTV deal floor or fixed price, the deal
  cannot win, full stop. Check this before blaming targeting or creative.
- **Authenticated identity is the CTV addressability layer.** CTV has no third-party cookie and no
  mobile ad ID. If you need deterministic audience matching on CTV, it rides UID2 or EUID on
  logged-in inventory. Non-authenticated CTV falls back to contextual and household signals.
- **Pause ads complement, they do not interrupt.** Use CTV pause ads to engage a viewer who paused
  content, not as a replacement for in-stream reach. They fit a lighter, contextual message.
- **Forecast live before you book live.** Live events and live sports demand is spiky and
  time-boxed. Run live events forecasting to size spend, reach, and impressions, because standard
  pacing assumes evenly available inventory and live inventory is not evenly available.
- **Koa assists, a human approves.** Treat Koa recommendations and the Advanced AI controls as
  guidance. Read the recommendation, then human-gate any change that moves spend or alters live
  config. Never auto-apply.

## Reference material

- `references/kokai-ctv-buying.md`: the end-to-end CTV and video buy in Kokai. Supply-path-to-goal
  decision table for video, curated CTV marketplace and Deal Desk workflow, Koa and Advanced AI
  controls on video, Sincera ad quality controls, UID2/EUID addressability on CTV, and video KPI
  targets. Read this when building or optimizing a CTV or video line.
- `references/ventura-ecosystem-and-openpath.md`: what the Ventura ecosystem is, the CTV
  supply-chain problem it targets, the first collaborators (V and Nexxen), how it relates to
  OpenPath and Sincera, and a decision table for when to buy through Ventura versus a curated
  marketplace, PMP, or Programmatic Guaranteed. Read this when choosing the CTV supply path or
  explaining Ventura to a client.
- `references/ctv-pause-ads-and-live-events.md`: the CTV pause ad format (what it is, when it
  fits, creative considerations), the live events and live sports workflow, live events
  forecasting inputs and outputs, and a pre-flight checklist for a live buy. Read this when
  planning a pause-ad or live-event flight.

## Templates and examples

Premium CTV brand flight, must deliver (tentpole sponsorship):
- Objective: reach and brand on the big screen during a tentpole moment. KPI: reach at a target
  VCR, viewability-verified completed views.
- Supply: Programmatic Guaranteed with the publisher for the reserved sponsorship, plus a curated
  CTV marketplace for scaled biddable CTV around it, routed through Ventura or OpenPath where a
  direct path is available.
- Identity: UID2 on logged-in inventory for a suppression and reach audience.
- Format: standard in-stream CTV; add CTV pause ads for a light contextual touch during the same
  content.
- Controls: Sincera ad quality on, Koa guiding optimization toward reach efficiency, frequency
  capped at the household with competitive separation in pods.
- Check: deal accepted both sides, creative matches CTV specs and is approved, bid equals the
  fixed price on the guaranteed deal and clears the floor on the curated deal.

Live sports flight (single tentpole event):
- Objective: peak-moment reach during a live event.
- Pre-flight: run live events forecasting to estimate spend, reach, and impressions for the event
  window, then human-approve the plan and budget before booking.
- Supply: biddable live event inventory plus a Programmatic Guaranteed reservation for guaranteed
  in-event delivery.
- Pacing: do not pace this like evergreen inventory. Concentrate budget in the live window the
  forecast identified.
- Check: creative approved ahead of the live window (no time to fix mid-event), frequency and pod
  competitive separation set, measurement currency reconciliation planned if the buy is
  currency-guaranteed (`ctv-measurement-currencies`).

Performance video, blended supply:
- Objective: outcomes from video with conversion measurement in place.
- Supply: open market and curated CTV marketplace for the scaled base, a PMP for two premium
  publishers, OpenPath for one premium publisher where a direct transparent path is wanted.
- Identity: UID2 for audience match and outcome joins on logged-in inventory.
- Controls: Sincera on to filter low-quality supply, Koa guiding toward the performance goal,
  human-approving material bid or budget moves.
- Check: floors clearable by the bid, measurement wired to read outcomes by goal
  (`ttd-measurement-and-reporting`).

## Common pitfalls

- **Buying CTV like display.** CTV serves in ad pods on a shared screen with no cookie and no
  mobile ad ID. Manage frequency at the household, guard pod competitive separation, and lean on
  UID2/EUID for addressability. Treating it as another banner buy wastes reach and double-serves.
- **Skipping the curated layer and blocking after the fact.** Bidding broadly on open CTV and then
  blocking waste burns budget first. Curate to a CTV marketplace and turn on Sincera quality
  controls so quality shapes the bid, not a post-mortem.
- **Pacing a live event like evergreen inventory.** Live demand is spiky and time-boxed. Standard
  even pacing starves the live window. Forecast the event, then concentrate budget in the window.
- **Treating pause ads as a reach format.** Pause ads engage a viewer who paused; they are not a
  substitute for in-stream reach. Use them as a complementary, contextual touch.
- **Auto-applying Koa recommendations.** Koa and the Advanced AI controls assist; a human approves
  anything that moves spend or changes live config. Read the recommendation, then gate the change.
- **Confusing Ventura with an SSP or a walled garden.** Ventura is an industry collaboration to
  make the CTV supply chain more transparent and revenue-optimized, uniting TV operating systems
  and streaming platforms. Describe it as a supply-path and marketplace collaboration, not a
  media owner or a supply-side platform.
- **Calling Solimar current.** Kokai is the current platform generation. Solimar is retired. Never
  frame the buy in the previous generation's terms.
- **Assuming public docs cover the platform clicks.** The concepts here are public. The exact
  Deal Desk screens, curated CTV enablement, Ventura seat access, pause-ad trafficking steps, and
  the API reference require partner access. Flag those as platform-gated when scoping work.

## Sources

- [The Trade Desk introduces the Ventura Ecosystem to advance the future of CTV advertising; V and Nexxen join as the first collaborators](https://www.thetradedesk.com/press-room/the-trade-desk-introduces-the-ventura-ecosystem-to-advance-the-future-of-ctv-advertising-v-and-nexxen-join-as-the-first-collaborators) (as of July 2026)
- [The Trade Desk Q2 2026 release highlights (CTV pause ads, live events forecasting, improved ad quality controls with Sincera, Advanced AI controls, Audience Unlimited, Audience Assistant, omnichannel insights, upgraded Deal Desk)](https://www.thetradedesk.com/resources/q2-2026-release-highlights) (as of July 2026)
- [OpenPath, The Trade Desk (direct connection between buyers and sellers, bid-data transparency, shorter supply chain)](https://www.thetradedesk.com/our-demand-side-platform/openpath) (as of July 2026)
- [Google NewFront: rethink CTV beyond streaming with Display & Video 360 (curated CTV auction, live inventory, DV360 CTV context for a walled-garden comparison)](https://blog.google/products/marketingplatform/360/google-newfront-rethink-ctv-beyond-streaming-with-display-video-360/) (as of July 2026)
- [New biddable capabilities for live sports with Display & Video 360 (biddable live sports, NBCUniversal Olympic Winter Games, for a walled-garden comparison)](https://blog.google/products/marketingplatform/360/new-biddable-capabilities-for-live-sports-with-display-video-360/) (as of July 2026)

Operational specifics that require The Trade Desk platform or partner access (not cited above
because the relevant pages sit behind a partner login): the live Koa recommendations and
Advanced AI controls in a seat, the exact Deal Desk and curated CTV marketplace screens, Ventura
seat access and enablement, CTV pause-ad trafficking steps, and the API reference. For those, use
the partner platform and its in-platform help.

---
name: ctv-supply-and-ad-pods
description: Buy connected TV correctly across DSPs. Use when the user asks about CTV or streaming TV supply, ad pods, pod position (first, mid, last), frame-based vs duration-based pods, competitive separation, SSAI vs CSAI, why CTV impressions have no viewability or click data, VAST wrapper or beacon loss, dropped tracking on SSAI, live sports pods, OTT vs CTV, premium publisher direct deals, or how to structure a CTV line item so pods and measurement work.
---

# CTV supply and ad pods

Buy connected TV so the pod structure, the ad-server-side insertion method, and the measurement all
line up before spend goes live. CTV is not display with a bigger screen. Ads run inside pods (linear
style commercial breaks stitched into a stream), the stream is usually assembled server-side, and that
assembly silently strips the tracking beacons display buyers take for granted. Get the pod and the
insertion method right and the campaign delivers with clean measurement. Get them wrong and you pay
premium CPMs for impressions you cannot verify, viewability you cannot report, and frequency you cannot
cap.

This skill covers CTV supply mechanics that apply across DSPs (DV360, The Trade Desk Kokai, Amazon DSP).
It assumes you know CPM, viewability, and reach. For that KPI math see the `programmatic-foundations`
skill.

## When to use this skill

- "How do CTV ad pods work?" / "Frame-based vs duration-based pods?" / "What is pod position?"
- "How do I set competitive separation on CTV?" / "Two auto ads ran back to back on a streaming break."
- "SSAI vs CSAI, which do I need?" / "Why do my CTV impressions have no viewability or click data?"
- "My VAST beacons are not firing on CTV." / "Tracking dropped on server-side ad insertion."
- "How do I buy live sports CTV pods?" / "How do I structure a premium publisher CTV deal?"
- "Why is CTV frequency capping not working across apps?" / "OTT vs CTV, what is the difference?"

Boundaries with sibling skills:
- The YouTube and Google video partners line item family (TrueView, bumpers, CPV, YouTube on CTV):
  `dv360-youtube-and-video`. YouTube CTV is bought as YouTube, not as third-party pod-based CTV, so it
  lives there. This skill is the non-YouTube streaming supply (Hulu, Disney, NBCU, Netflix, Roku, Tubi,
  Samsung, LG, and the like) bought through deals and open CTV auctions.
- Deal type selection and how a deal ID is plumbed to a line item: `dv360-deals-and-inventory` (DV360)
  or `ttd-inventory-and-deals` (Kokai) or `amazon-dsp-inventory-and-supply`. This skill is what the
  deal must contain for CTV to work, not the deal mechanics.
- Reducing the number of SSPs between the DSP and the publisher: `curation-and-supply-path-optimization`.
- Frequency-cap policy and brand-safety exclusions in general: `dv360-frequency-and-brand-safety`.
- Cross-screen reach and frequency planning math: `reach-and-frequency-planning`.
- Bid strategy for the line item (fixed for guaranteed, automated for biddable): `dv360-bid-strategy`.

## Quick reference

Decide these four things in order before you launch a CTV buy.

| Decision | Options | Pick this when |
| --- | --- | --- |
| Pod construction | Frame-based (fixed slots) vs duration-based (fill a time budget) | Frame gives predictable slot count and clean competitive separation; duration maximizes fill on long breaks. The publisher usually dictates this. |
| Pod position | First, mid, last, or unrestricted | First and last cost more and complete more. Buy position only when completion or attention justifies the premium. |
| Insertion method | SSAI (server-side) vs CSAI (client-side) | Almost all premium CTV is SSAI. CSAI only on app environments that run a full VPAID/OM-capable player, which is rare on TV. |
| Measurement plan | OM SDK server-side beacons, publisher-passed macros, or MRC-accredited third party | Choose before launch. SSAI breaks client-side beacons, so you need server-side measurement or you fly blind. |

The single most expensive CTV mistake: buying premium SSAI inventory with a display measurement setup,
then discovering post-launch that viewability, IVT, and click beacons never fired. Confirm the
measurement path in the deal, not after the first invoice.

## Core process

1. Confirm the supply is actually CTV, not OTT-on-mobile mislabeled. CTV means the ad renders on a
   television (smart TV OS, streaming stick, game console, set-top box). OTT is any over-the-top
   delivery including phones and desktops. Device-type and app-bundle targeting keep a "CTV" line item
   from leaking onto phone screens, because the two clear at very different CPMs and attention levels.
2. Read the pod construction from the deal or supply description. Frame-based pods expose a fixed number
   of ad slots (for example a 4-slot pod); duration-based pods expose a time budget the exchange fills
   with any mix of durations (for example a 90-second break filled by 30s + 30s + 15s + 15s). This
   decides how you set creative duration and how competitive separation is enforced.
3. Decide whether pod position matters for this goal. First-position and last-position slots complete at
   higher rates and command a premium. For a completion-sensitive or attention goal, buy position; for
   efficient reach, take unrestricted position and save the premium.
4. Set competitive separation expectations. Separation (no two competing brands, and no duplicate creative,
   in the same pod) is enforced by the publisher or SSP ad server, not by your DSP alone. On open CTV
   auction you cannot fully guarantee it, so for brand-sensitive advertisers require separation in a deal.
5. Identify the insertion method and its measurement consequence. If the supply is SSAI (it usually is),
   plan for server-side measurement. See `references/ssai-vs-csai-tradeoffs.md` for exactly which signals
   survive SSAI and which do not, and how OM SDK server-side and passed macros recover them.
6. Pin the measurement path in writing before launch. Confirm which viewability and IVT vendor the
   publisher supports server-side, and confirm the impression and completion beacons will fire through the
   SSAI stitcher. Do not assume the DSP's standard tracking works.
7. For premium and live inventory, buy through a deal, not open auction. Live sports pods, first-position
   slots, and competitive separation are contractual guarantees that only a Programmatic Guaranteed or
   private deal delivers reliably. See `references/premium-publisher-supply-structure.md`.
8. Cap frequency at the household or device level, and know it degrades on SSAI. SSAI can obscure the
   device identifier, so cross-app household frequency capping is weaker than on client-rendered supply.
   Where cross-publisher frequency matters, consolidate through fewer supply paths and a shared identity.

## Decision rules and thresholds

### Frame-based vs duration-based pods

- Frame-based (also called slot-based): the pod has a fixed number of positions. You know a 4-slot pod
  holds exactly four ads. Competitive separation and position targeting are cleaner because slots are
  discrete. Cut creative to the standard slot durations the publisher accepts (commonly 15s and 30s).
- Duration-based: the pod is a time budget the exchange fills to maximize monetization. A 120-second
  break might be four 30s ads or eight 15s ads. Fill is higher, but slot count and your neighbors are
  less predictable, so competitive separation is harder to guarantee.
- Rule: for brand-sensitive buys where who-you-run-next-to matters, prefer frame-based pods in a deal.
  For scaled reach where fill and price matter more, duration-based open supply is fine.

### Pod position

- First and last positions complete at higher rates and draw more attention, so publishers price them
  up. Mid-pod positions are cheaper and complete lower.
- Only pay the position premium when the goal rewards it (completion guarantees, attention studies,
  premium brand placement). For cost-efficient reach, take unrestricted position.
- Position targeting is a deal feature. Open CTV auction rarely lets you dictate position, so if position
  is non-negotiable, it belongs in a Programmatic Guaranteed or private deal.

### Competitive separation

- Separation prevents two competitors (or two copies of your own creative) inside the same pod. On CTV it
  is enforced by the publisher/SSP stitching the pod, because the DSP does not control the full break.
- On open auction you get best-effort separation at most. For regulated or brand-sensitive categories,
  require category-level separation contractually in the deal, and confirm the publisher can enforce it.
- Do not rely on your DSP's own frequency cap to prevent same-pod duplication; the pod is assembled before
  your DSP sees the full slate.

### SSAI vs CSAI

- SSAI (server-side ad insertion): the publisher's server stitches the ad into the video stream before it
  reaches the device, so the ad arrives as part of the content. This is how nearly all premium CTV
  (live sports, major streamers, TV OS inventory) is delivered, because it defeats ad blocking and gives
  a seamless, buffer-free viewing experience. The cost: the ad is not running in an interactive client
  player, so client-side VAST tracking, VPAID, and many verification beacons do not fire on their own.
- CSAI (client-side ad insertion): the device's video player requests and renders the ad, so it can run a
  full VAST/OM-capable player and fire client-side beacons. This exists mostly in app environments with a
  capable SDK player. On living-room TV OS supply it is the minority.
- Rule: assume SSAI on premium CTV and plan server-side measurement from the start. Only assume CSAI when
  the publisher confirms a client player that supports OM SDK and VPAID. The signal-by-signal survival
  table is in `references/ssai-vs-csai-tradeoffs.md`.

### Measurement under SSAI

- Client-side impression, quartile, and completion beacons in a VAST wrapper may not fire when the stream
  is stitched server-side. Recover them with OM SDK running server-side (OMID), publisher-passed VAST
  macros filled at stitch time, or an MRC-accredited vendor the publisher integrates on the server.
- OM SDK 1.5 adds Samsung and LG smart-TV support alongside Android TV and tvOS, so cross-TV-OS
  server-side measurement is more attainable than it was, but it still requires the publisher to have
  integrated it. Confirm coverage per publisher; do not assume.
- If you cannot secure a server-side measurement path, treat viewability, IVT, and click reporting for
  that supply as unavailable, and price and evaluate the buy accordingly (completion rate and delivery
  become your primary in-platform signals).

### CTV vs OTT device leakage

- A line item labeled CTV can serve on phones and desktops if device targeting is loose, because OTT
  includes those screens. Restrict to connected-TV device types and, where possible, an app-bundle
  allowlist, so you buy the living-room screen you are paying a CTV CPM for.

## Reference material

- `references/pod-construction-and-position.md`: frame-based vs duration-based pod anatomy, pod-position
  economics, competitive-separation enforcement, VAST ad-pod signaling, and the DV360 / Kokai / Amazon DSP
  controls that map to each. Read this when structuring a pod buy or diagnosing back-to-back competitor ads.
- `references/ssai-vs-csai-tradeoffs.md`: a signal-by-signal table of what survives SSAI and what breaks,
  the OM SDK server-side and passed-macro recovery paths, and a pre-launch measurement checklist. Read this
  when CTV impressions have no viewability, no clicks, or missing quartile beacons.
- `references/premium-publisher-supply-structure.md`: how premium and live CTV supply is structured (direct
  PG, curated CTV marketplaces, live sports packages), the DSP-by-DSP landscape as of 2026, and how to buy
  position and separation contractually. Read this when building a premium or live-sports CTV buy.

## Templates and examples

- Live sports, brand advertiser, completion-sensitive: Programmatic Guaranteed deal with NBCUniversal live
  sports inventory, frame-based 4-slot pods, first-position slot, category competitive separation required,
  server-side OM SDK measurement confirmed with the publisher, 30s creative, fixed bid at the deal rate,
  device restricted to connected TV. Buy through DV360 curated live sports packages or a Kokai live-events
  deal. Do not run this on open auction; position and separation would not be guaranteed.
- Scaled CTV reach, performance advertiser, efficiency goal: open CTV auction plus a few private deals on
  Tubi and Roku, duration-based pods, unrestricted position, 15s and 30s creative, automated bidding toward
  a reach or viewable-CPM goal, household frequency cap set knowing SSAI weakens cross-app enforcement,
  connected-TV device restriction with an app-bundle allowlist to block mobile OTT leakage.
- Diagnosing "no viewability on my CTV line item": confirm the supply is SSAI (it almost certainly is),
  then confirm whether the publisher passes server-side OM SDK or macro-based beacons. If not, viewability
  is genuinely unavailable for that supply, not a DSP bug. Switch to publishers with server-side
  measurement or accept completion rate as the proxy.

## Common pitfalls

- Buying SSAI supply with a display measurement plan. The impression fires but the viewability, IVT, and
  click beacons do not, and you discover it after launch. Confirm the server-side measurement path in the
  deal first.
- Assuming your DSP frequency cap prevents same-pod competitor collisions. The pod is stitched by the
  publisher before the DSP sees the full slate; competitive separation must be a deal requirement.
- Treating YouTube-on-CTV as if it were third-party pod CTV. YouTube CTV is bought as YouTube (see
  `dv360-youtube-and-video`); its pods, formats, and measurement work differently from streamer supply.
- Letting a CTV line item leak onto mobile OTT. Loose device targeting serves phone impressions at a CTV
  CPM. Restrict to connected-TV device types.
- Expecting reliable cross-app household frequency on SSAI. The device identifier can be obscured at the
  stitch, so cross-publisher frequency capping is weaker; consolidate supply paths and use a shared
  identity where cross-publisher frequency is the goal.
- Paying for first-position on open auction. Open CTV auction rarely honors position; if you need it, put
  it in a deal or you are paying a premium you cannot enforce.
- Cutting creative to durations the pod does not accept. A duration-based pod that fills 15s and 30s slots
  will not place a 20s or 45s spot; match the publisher's accepted slot durations.

## Sources

- [New biddable capabilities for live sports with Display & Video 360](https://blog.google/products/marketingplatform/360/new-biddable-capabilities-for-live-sports-with-display-video-360/) (as of July 2026)
- [Google NewFront: Rethink CTV beyond streaming with Display & Video 360](https://blog.google/products/marketingplatform/360/google-newfront-rethink-ctv-beyond-streaming-with-display-video-360/) (as of July 2026)
- [Open Measurement SDK, IAB Tech Lab](https://iabtechlab.com/standards/open-measurement-sdk/) (as of July 2026)
- [Display & Video 360 upcoming changes and announcements](https://support.google.com/displayvideo/answer/17006423?hl=en) (as of July 2026)
- [Display & Video 360 API release notes (v4)](https://developers.google.com/display-video/api/release-notes) (as of July 2026)
- [Display & Video 360 API v4 REST reference](https://developers.google.com/display-video/api/reference/rest/v4) (as of July 2026)

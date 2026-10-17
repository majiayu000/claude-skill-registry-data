---
name: ttd-inventory-and-deals
description: Decide where impressions come from on The Trade Desk across the open internet and get a deal or direct supply path delivering. Use when the user asks about "Trade Desk inventory", "TTD CTV inventory", "OpenPath", "TTD deals", "TTD supply", "private marketplace on TTD", "PMP vs Programmatic Guaranteed", "omnichannel", "connected TV", "streaming", "audio", "native", "digital out-of-home", "DOOH", "supply path optimization", or the sellers and supply-chain transparency concept.
---

# TTD inventory and deals

Choose the channel mix and the inventory access path on The Trade Desk, then wire a deal or direct supply route so it actually spends. The Trade Desk buys omnichannel inventory across the open internet, with connected TV and streaming as the flagship channel. For definitions of CPM, floor price, PMP, deal ID, and auction mechanics, see the `programmatic-foundations` skill. For who to target inside that inventory, hand off to `ttd-targeting-and-audiences`. For framing inventory and deal performance against the objective, see the `reporting-by-campaign-goal` skill.

## When to use this skill

Use this when the task is about WHERE inventory comes from and how a deal or supply path is plumbed, including:

- Selecting channels: connected TV and streaming, online video, display, audio, native, and digital out-of-home (DOOH).
- Choosing among open marketplace, private marketplace (PMP), Programmatic Guaranteed, and OpenPath direct supply.
- Understanding OpenPath: The Trade Desk's more direct connection between buyers and a publisher's ad server, why it reduces intermediaries, and where it helps.
- Reasoning about supply path optimization and the sellers and supply-chain transparency concept (who is in the path and how much value they add).
- Setting up a deal end to end at a conceptual level: negotiate, receive a deal ID, apply it in the platform, and match creative specs.
- Tiering premium guaranteed and PMP against scaled open marketplace for brand versus performance goals.

Boundaries with sibling skills:
- Audience and contextual targeting layered on top of the inventory lives in `ttd-targeting-and-audiences`.
- The identity layer (UID2, EUID) that makes inventory addressable lives in `ttd-identity-and-uid2`.
- Campaign and ad group structure lives in `ttd-campaign-structure`; bid pricing against a floor lives in `ttd-bidding-and-optimization`.
- Measuring delivery and outcomes lives in `ttd-measurement-and-reporting`, with goal framing in `reporting-by-campaign-goal`.

## Quick reference

Channels The Trade Desk buys across the open internet:

| Channel | Notes | Typical use |
| --- | --- | --- |
| Connected TV and streaming | Premium streaming content including live sports and high-profile events; the flagship channel. | Reach and brand on the biggest screen, with logged-in addressability. |
| Online video | In-stream and outstream video beyond CTV. | Upper and mid funnel storytelling. |
| Display | Standard banner inventory at scale. | Efficient reach, retargeting, performance. |
| Audio | Streaming audio and podcasts. | Incremental reach, screenless moments. |
| Native | Format that matches the host page. | Engagement and content alignment. |
| Digital out-of-home (DOOH) | Programmatic screens in physical spaces. | Local and contextual brand presence. |

Inventory access paths, from most scaled to most committed:

| Path | What it is | Price and volume | Typical use |
| --- | --- | --- | --- |
| Open marketplace | Auction across broad public supply, no deal. | Clears at market, no volume commitment. | Scaled reach and performance, the base layer. |
| Private marketplace (PMP) | Invite-only auction on curated publisher inventory via a deal ID. | Auction against a floor, no commitment. | Quality pockets, brand-safe context, competitive. |
| Programmatic Guaranteed | Reserved volume at a fixed price via a deal. | Fixed price, guaranteed volume you commit to. | Sponsorships, roadblocks, must-deliver flights. |
| OpenPath | The Trade Desk's direct connection to a publisher's ad server, fewer intermediaries. | Depends on the underlying buy; adds path transparency. | Premium supply with a cleaner, more transparent path. |

Setup in one line: pick the channel and access path the goal needs, negotiate a deal when you want curated or reserved supply, apply the deal ID in the platform, match creative specs and the floor, and read delivery against the objective.

## Core process

### Choose the channel mix

1. **Lead with the objective, then the channel.** Brand and reach goals weight toward CTV and streaming, online video, and DOOH. Performance and direct-response goals weight toward display, native, and online video with measurement in place. Most plans blend channels.
2. **Treat CTV as the flagship, not a novelty.** Premium streaming, including live sports, is where The Trade Desk concentrates and where logged-in audiences make impressions addressable. Plan CTV deliberately rather than as spillover from video.
3. **Use audio and DOOH for incremental reach.** They reach people in moments other channels miss (commutes, screens in physical space), so use them to extend reach rather than to carry a performance goal alone.

### Choose the inventory access path

1. **Match the path to the goal.** Open marketplace buys scale and price efficiency. PMP buys curated, brand-safe context with competition. Programmatic Guaranteed buys delivery certainty and premium placement. OpenPath buys a cleaner, more transparent path to premium publisher supply.
2. **Use Programmatic Guaranteed when delivery is non-negotiable.** It reserves a fixed volume at a fixed price, so use it for sponsorships, takeovers, and flights that must deliver. You commit to the volume, so size it to what the plan actually needs.
3. **Use PMP for curated, competitive quality.** A private marketplace invites a limited set of buyers to bid against a floor on inventory the publisher curated. No volume commitment; you compete on price for quality pockets.
4. **Use the open marketplace for the scaled base.** It carries no deal and clears at market. It is the widest pool and the cheapest path to reach, and it backstops everything else.

### Use OpenPath for a more direct supply path

1. **Understand what OpenPath is.** It is a buying solution that creates a direct connection between advertisers and a publisher's ad server, reducing the number of intermediaries between buyer and seller and adding transparency, including direct visibility into bid data. The Trade Desk is explicit that OpenPath is not a supply-side platform or a yield-management tool; publishers keep their existing transparent demand tools such as OpenRTB and Prebid.
2. **Know why it exists.** Publishers have historically received only about half of every ad dollar, with the rest going to a long chain of intermediaries, some adding little value. OpenPath, launched in 2022, closes that gap by shortening the path between advertiser and publisher.
3. **Use it for premium supply where path quality matters.** Reach for OpenPath when you want premium publisher inventory through a transparent, direct route rather than through a long, opaque chain. Treat it as a supply path choice that complements your deal strategy, not a replacement for targeting or measurement.

### Supply path optimization and the sellers concept

1. **Reason about the path, not just the impression.** The same impression can be reachable through many supply paths at different costs and with different intermediaries. Supply path optimization means consolidating onto the cleaner, more direct, more transparent routes (OpenPath being one) and trimming redundant or low-value hops.
2. **Care about who the seller is.** Supply-chain transparency is about knowing which sellers and intermediaries sit in the path and how much value each adds. Prefer paths where the seller relationship is clear and the value is real, which is the whole premise behind shortening the chain.

### Set up a deal

1. **Negotiate with the publisher or exchange.** Agree on inventory, price, volume (for guaranteed), flight, and creative specs. The seller creates the deal on their side.
2. **Receive the deal ID.** The deal ID is the handle that ties the negotiated terms to your buy.
3. **Apply the deal ID in the platform and match specs.** Attach the deal to the buy, confirm the creative formats and sizes match what the deal supports, and confirm the bid meets or beats the floor or fixed price. Bid pricing detail lives in `ttd-bidding-and-optimization`.

Platform access note: the exact deal-application screens, OpenPath inventory enablement and seat access, the supply and sellers data inside the platform, and the step-by-step PMP and Programmatic Guaranteed setup live in The Trade Desk platform behind partner login. The concepts above are public; the operational clicks require platform access. Flag those as platform-gated when scoping work, and confirm seat-level access before promising a setup.

## Decision rules and thresholds

- **Tier the mix to the goal.** Premium guaranteed and PMP buy controlled context and delivery certainty at a higher CPM; open marketplace buys scale and efficiency. Brand-led plans weight toward guaranteed, PMP, and CTV; performance-led plans weight toward open marketplace with PMP for quality pockets.
- **Commit only what guaranteed delivery requires.** Programmatic Guaranteed volume is an obligation. Size it to the reserved need and let auction supply flex around it.
- **A floor is a hard gate.** If the bid cannot clear the floor or fixed price, the deal cannot win, full stop. Check this before blaming targeting.
- **Prefer the shorter, more transparent path.** When the same supply is reachable directly (for example through OpenPath) and through a longer chain, the direct path usually means more transparency and fewer fees skimmed by intermediaries that add little value.
- **Match creative to the channel and the deal.** A CTV deal will not serve display creatives, and a size the deal does not support never renders. Confirm specs against the deal sheet and the channel.
- **Judge inventory by outcome, not by label.** Premium and direct are inputs. Read delivery and results against the objective using `reporting-by-campaign-goal`.

## Troubleshooting a deal that is not delivering

Work this in order; stop when spend resumes. Earlier causes are more common and cheaper to fix.

1. **Deal status and dates.** Confirm the deal is active and accepted on both sides and that today falls inside the flight. A pending, paused, or expired deal cannot serve.
2. **Bid below floor.** Confirm the bid or bid-strategy ceiling meets or exceeds the floor or fixed price. Below-floor bids are filtered before the auction.
3. **Deal not applied to the buy.** Confirm the deal ID is attached to the campaign or ad group that is meant to use it.
4. **Targeting over-restriction.** Layered audience, geo, daypart, or contextual targeting can shrink the eligible pool to near zero. Peel back the tightest layer; see `ttd-targeting-and-audiences`.
5. **Creative spec or channel mismatch.** Confirm creative sizes, formats, and channel match what the deal supports and that creatives are approved.
6. **Budget, pacing, or frequency limits.** Confirm budgets are not exhausted and pacing or frequency settings are not throttling delivery.
7. **Seller-side pause or no inventory.** The publisher may have paused the deal or have no matching inventory. Confirm with the seller.

If the deal checks out at every step and still will not spend, open the seller conversation in parallel and escalate to `ttd-bidding-and-optimization` for a fuller delivery review.

## Reference material

- See the `programmatic-foundations` skill for CPM, floor price, first vs second price auctions, PMP, and deal-ID basics. This skill does not redefine them.
- See the `reporting-by-campaign-goal` skill for how to present inventory and deal performance against the campaign objective.
- The OpenPath resources in the Sources cover the buyer and publisher benefits, the supply-chain problem, and the position that OpenPath is not an SSP. Read them before recommending OpenPath so the framing is accurate.

## Templates and examples

Brand sponsorship on CTV, must deliver:
- Channel: connected TV and streaming on premium content.
- Path: Programmatic Guaranteed with the publisher, fixed CPM, reserved impressions for the flight.
- Setup check: deal accepted both sides, creatives match the CTV specs and are approved, flight dates aligned, bid equals the fixed price.

Performance plan, blended supply:
- Channels: display and online video, with audio for incremental reach.
- Paths: open marketplace for the scaled base, a PMP for two premium publishers, and OpenPath for one premium publisher where a direct, transparent path is wanted.
- Setup check: PMP and OpenPath floors are clearable by the bid, open marketplace carries the bulk of budget, measurement is in place to read outcomes by goal.

Supply path cleanup:
- Audit the paths buying the same publishers, consolidate onto the most direct and transparent routes (OpenPath where available), and trim redundant intermediaries that add little value.
- Expected payoff: fewer fees lost in the chain and clearer visibility into who is in the path.

## Common pitfalls

- **Bidding below the floor.** The most common reason a freshly applied deal shows zero spend. The bid is filtered before the auction, so nothing serves. Check the floor first.
- **Forgetting to apply the deal ID to the buy.** The deal exists but no campaign or ad group points at it, so nothing uses it. Applying the deal is a separate step from negotiating it.
- **Creative or channel mismatch.** A CTV deal will not serve display, and an unsupported size never renders. Match specs to the deal sheet and the channel.
- **Treating OpenPath as an SSP or yield tool.** It is a more direct buying path, not a supply-side platform. Publishers keep their own demand tools. Describe it accurately or the recommendation misleads.
- **Over-committing guaranteed volume.** Programmatic Guaranteed is an obligation. Reserving more than the plan needs locks budget you cannot redeploy. Size it to the reserved need.
- **Assuming public docs cover the platform clicks.** The concepts are public; deal-application screens, OpenPath enablement, and sellers data require partner access. Flag those as platform-gated rather than promising a self-serve setup.

## Sources

Official The Trade Desk pages and The Current, The Trade Desk's news publication, all verified as of June 2026.

- The Trade Desk demand-side platform overview (omnichannel: connected TV and streaming, video, display, audio, native, and DOOH): https://www.thetradedesk.com/our-demand-side-platform
- OpenPath product page (direct connection between buyers and sellers, bid-data transparency, omnichannel demand): https://www.thetradedesk.com/our-demand-side-platform/openpath
- What is OpenPath and how publishers benefit (direct connection to a publisher's ad server, not an SSP, works with OpenRTB and Prebid, true price discovery): https://www.thetradedesk.com/resources/what-is-openpath
- OpenPath launch coverage on The Current (2022 launch, direct access to premium publisher inventory, the supply-chain transparency problem): https://www.thecurrent.com/the-trade-desk-closes-the-gap-between-advertisers-and-publishers-with-debut-of-openpath

As of June 2026.

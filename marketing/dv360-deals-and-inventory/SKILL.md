---
name: dv360-deals-and-inventory
description: Choose the right inventory type in Display & Video 360 and get a deal delivering. Use when the user asks about open auction vs PMP vs Programmatic Guaranteed, private auction, Preferred Deal, how to set up a deal, what a deal ID is, how to assign a deal to a line item, inventory priority, premium vs scaled inventory mix, or troubleshooting a deal that is not delivering.
---

# DV360 deals and inventory

Decide where impressions come from (open marketplace vs negotiated deals) and wire a deal so it
actually spends. This skill covers inventory sourcing and deal mechanics. For who to target inside
that inventory, hand off to `dv360-targeting-and-audiences`. For definitions of CPM, floor price,
and auction mechanics, see `programmatic-foundations`.

## When to use this skill

Use this when the task is about WHERE inventory comes from and how a deal is plumbed, including:

- Choosing among open auction, Private Marketplace and private auction, Preferred Deal, and
  Programmatic Guaranteed.
- Understanding inventory priority and how guaranteed and deal inventory relate to open auction.
- Setting up a deal end to end: negotiating, receiving a deal ID, finding the deal in DV360, and
  assigning it to a line item.
- Tiering premium guaranteed and PMP against scaled open auction for brand vs performance goals.
- Diagnosing a deal that is approved but not delivering.

Boundaries with sibling skills:
- Audience and contextual targeting layered on top of the inventory live in
  `dv360-targeting-and-audiences`.
- Splitting insertion orders by buying type, and overall campaign structure, live in
  `dv360-campaign-architecture`.
- Frequency caps and brand-safety policy live in `dv360-frequency-and-brand-safety`.
- Bid pricing against a floor lives in `dv360-bid-strategy`.
- Packaging audience or data onto inventory as a single curated deal ID lives in
  `curation-and-curated-marketplaces`; this skill only covers how such a deal is plumbed into DV360.
- For a structured, ordered delivery investigation that goes beyond deals, hand off to
  `dv360-troubleshooting`.

## Quick reference

Inventory types, from most scaled to most committed. The first column is the buyer vocabulary
practitioners use; the second is how Display & Video 360 names and groups it today.

| Practitioner name | DV360 grouping | Price | Volume | Typical use |
| --- | --- | --- | --- | --- |
| Open auction | Open marketplace, no deal | Auction, clears at market | None | Scaled reach and performance |
| Private Auction / PMP | Non-guaranteed auction | Auction with a floor | None | Curated inventory, competitive |
| Preferred Deal | Non-guaranteed fixed deal | Fixed, you are not obligated to buy | None | First look at a fixed CPM |
| Programmatic Guaranteed | Guaranteed deal | Fixed | Guaranteed (reserved) | Premium, reserved, must-deliver |

Priority an expert assumes: negotiated deals and guaranteed inventory take precedence over the open
auction, and the publisher can rank deal types so a fixed deal is served ahead of an auction deal
ahead of open auction. Inside DV360 you also control which of your own line items wins internal
competition through line item priority, so a guaranteed line item can be set to win over a
lower-priority open-auction line item competing for the same impression.

Deal setup in one line: negotiate with the publisher, receive a deal ID (for a new non-guaranteed
deal the seller now syncs it to your seat rather than you keying it in), find the deal in DV360 My
Inventory, assign it to a line item as the inventory source, match the line item type and creative
specs the deal expects, and make sure your bid meets or beats the floor. A curated deal ID arrives
the same way and already carries its audience and inventory as one package; see
`curation-and-curated-marketplaces`.

## Core process

### Choosing the inventory type

1. **Match inventory to the goal.** Brand and high-impact goals that need guaranteed delivery and
   premium context map to Programmatic Guaranteed and PMP. Performance and reach goals that need
   scale and price efficiency map to open auction plus selective PMP. Most plans blend the two.
2. **Use guaranteed when delivery is non-negotiable.** Programmatic Guaranteed reserves a fixed
   volume at a fixed price, so use it for sponsorships, roadblocks, and flights that must deliver.
   You commit, so only buy what the plan needs.
3. **Use a Preferred Deal for a fixed-price first look without obligation.** A non-guaranteed fixed
   deal gives you priority access at a negotiated CPM but no volume commitment, so it is the safe
   way to lock a price on inventory you want but cannot fully forecast.
4. **Use a private auction for curated, competitive inventory.** A non-guaranteed auction invites
   you and a limited set of buyers to bid against a floor on inventory the publisher curated. No
   commitment; you compete on price.
5. **Use open auction for the scaled base.** It carries no deal and clears at market. It is the
   widest pool and the cheapest path to reach, and it backstops unsold deal inventory.

### Setting up a deal

1. **Negotiate with the publisher, exchange, or curator.** Agree on inventory, price, volume (for
   guaranteed), flight, and creative specs offline or via an RFP. The seller creates the deal on
   their side. For non-guaranteed deals the seller now sends the deal to your seat over the deal
   sync path (the Seller API) rather than you keying in a deal ID by hand; manual creation of
   non-Programmatic-Guaranteed deals is being deprecated in 2026, targeted for April 2026 per
   Google's own estimate, so treat the synced deal as how a new non-PG deal arrives. Existing
   manually keyed deals keep serving. This same path carries curated deals, where a single curated
   deal ID bundles the audience or data segment together with the inventory; hand off to
   `curation-and-curated-marketplaces` for how that packaging and its fees work.
2. **Receive the deal ID.** The deal ID is the handle that ties the negotiated terms to your seat.
   For a curated deal, that one ID already encodes both the audience and the inventory the curator
   assembled, so you do not layer the audience again on the DV360 side.
3. **Find the deal in DV360.** Negotiated deals appear under Inventory, My Inventory. Synced deals
   arrive automatically as an inventory source once the seller pushes them. Guaranteed deals that
   still need configuration surface in an action-required state; other deal types appear in the
   general list.
4. **Assign the deal to a line item as its inventory source.** Either attach it to an existing line
   item or create a new line item with its own targeting, flight, budget, and creatives. For
   Programmatic Guaranteed the insertion order can be set up automatically in the selected advertiser
   once the deal is accepted and configured.
5. **Match line item type and creative specs.** The line item type (display, video, audio) and the
   creative sizes and formats must match what the deal expects, or it will not serve.
6. **Make the bid meet or beat the floor.** For auction and fixed deals, confirm your bid (or bid
   strategy ceiling) meets or exceeds the deal floor or fixed price. See `dv360-bid-strategy`.

## Decision rules and thresholds

- **Tier the mix to the goal.** Premium guaranteed and PMP buy controlled context and delivery
  certainty at a higher CPM; open auction buys scale and efficiency. Brand-led plans weight toward
  guaranteed and PMP; performance-led plans weight toward open auction with PMP for quality pockets.
  Split these across separate insertion orders by buying type so pacing and reporting stay clean;
  see `dv360-campaign-architecture`.
- **Commit only what guaranteed delivery requires.** Guaranteed volume is an obligation. Size it to
  the reserved need and let auction and open inventory flex around it.
- **Deals outrank open auction, so do not let an open-auction line item starve a deal.** If a deal
  and an open-auction line item compete internally, use line item priority so the deal wins the
  impressions it was negotiated for.
- **A floor is a hard gate.** If the bid cannot clear the floor, the deal cannot win, full stop.
  Check this before blaming targeting.

## Troubleshooting a deal that is not delivering

Work this in order; stop when spend resumes. Earlier causes are both more common and cheaper to fix.

1. **Deal status and dates.** Confirm the deal is active and accepted on both sides and that today
   falls inside the deal flight. A pending, paused, expired, or not-yet-started deal cannot serve.
2. **Bid below floor.** Confirm the bid or bid-strategy ceiling meets or exceeds the deal floor or
   fixed price. Below-floor bids are filtered before the auction.
3. **Line item not targeting the deal.** Confirm the deal is assigned as the line item inventory
   source. If the line item is not pointed at the deal, it will not use it.
4. **Audience or geography over-restriction.** Layered audience, geo, daypart, or content targeting
   can shrink the eligible pool to near zero. Peel back the tightest layer; see
   `dv360-targeting-and-audiences`.
5. **Creative size or spec mismatch.** Confirm the creative sizes, formats, and line item type match
   what the deal supports, and that creatives are approved by the exchange.
6. **Budget, pacing, or frequency caps.** Confirm the line item and insertion order budgets are not
   exhausted, pacing is not throttling, and frequency caps are not blocking delivery; caps live in
   `dv360-frequency-and-brand-safety`.
7. **Publisher-side pause or no inventory.** The publisher may have paused the deal or have no
   matching inventory available. Confirm with the seller.
8. **Seat or advertiser not on the deal.** Confirm the deal was made to the correct buyer seat and
   that the advertiser using it is the one the deal targets. A deal scoped to a different seat or
   advertiser will not serve for yours.

If the deal checks out at every step and still will not spend, escalate to `dv360-troubleshooting`
for a fuller delivery investigation, and open the publisher conversation in parallel.

## Reference material

- See `programmatic-foundations` for CPM, floor price, first vs second price auctions, and win-rate
  math. This skill does not redefine them.
- The DV360 API models negotiated inventory as an inventory source with a deal ID, a commitment
  (guaranteed or non-guaranteed), a delivery method, and a rate type (CPM fixed, CPM floor, and
  others). Read the inventorySources resource in the Sources when automating deal assignment or
  reconciling deal terms; `dv360-api-and-sdf-automation` covers the automation workflow.

## Templates and examples

Brand sponsorship, must deliver:

- Inventory: Programmatic Guaranteed with the homepage takeover publisher, fixed CPM, reserved
  impressions for the flight.
- Line item: dedicated insertion order for guaranteed buying, line item priority set so the
  guaranteed line item wins internal competition.
- Setup check: deal accepted both sides, creatives match the takeover specs and are exchange
  approved, flight dates aligned, bid equals the fixed price.

Performance plan, blended mix:

- Inventory: open auction line item for scaled reach, plus a private auction PMP for two premium
  publishers, plus a Preferred Deal locking a fixed CPM on one high-intent site.
- Structure: split open auction and deal buying into separate insertion orders so pacing and
  reporting stay clean.
- Setup check: PMP and Preferred Deal floors are clearable by the bid strategy; open auction line
  item carries the bulk of the budget; deal line items set to win internally where they overlap.

## Common pitfalls

- **Bidding below the floor.** The most common reason a freshly assigned deal shows zero spend. The
  bid is filtered before the auction, so no impression is ever served. Check the floor first.
- **Forgetting to assign the deal as the inventory source.** The deal exists in My Inventory but no
  line item points at it, so nothing uses it. Assigning the deal is a separate step from accepting
  it.
- **Creative or line item type mismatch.** A video deal will not serve display creatives, and a size
  the deal does not support will never render. Match specs to the deal sheet.
- **Letting an open-auction line item outcompete a deal internally.** Without line item priority set
  correctly, your own open-auction line item can win impressions you negotiated a deal to get. Set
  priority so the deal wins.
- **Over-committing guaranteed volume.** Guaranteed is an obligation. Reserving more than the plan
  needs locks budget you cannot redeploy. Size it to the reserved need.
- **Blaming targeting before checking deal status and floor.** Status, dates, and floor are faster
  to verify and more often the cause than audience or geo restriction. Work the order above.

## Sources

Official Display & Video 360 Help and Display & Video 360 API documentation. Core deal-mechanics
lines verified as of June 2026; the synced-deal and manual-creation-deprecation lines verified as of
July 2026.

- Overview of deals (deal types and what a deal is): https://support.google.com/displayvideo/answer/7243138
- Programmatic Guaranteed deals (reserved volume, fixed price, setup, auto-created insertion order): https://support.google.com/displayvideo/answer/7067656
- About non-guaranteed auctions (private auction and fixed deals, inventory priority, unsold reverts to open auction): https://support.google.com/displayvideo/answer/3289702
- Manage your deals (My Inventory, action-required vs everything else, assigning a deal to a line item): https://support.google.com/displayvideo/answer/6224774
- About synced deals (deals synced from the exchange or seller create an inventory source; manually keyed deals do not auto-sync): https://support.google.com/displayvideo/answer/9900183
- Coming soon: Display & Video 360 updates in Q2 2026 (manual non-Programmatic-Guaranteed deal creation being deprecated, Deal Sync as the path for new non-PG deals, estimated April 2026): https://support.google.com/displayvideo/answer/17006423
- Troubleshoot your deals and line items (non-delivery causes): https://support.google.com/displayvideo/answer/6292894
- DV360 API v4, inventorySources resource (deal ID, commitment, delivery method, rate type): https://developers.google.com/display-video/api/reference/rest/v4/inventorySources
- Curation and the single curated deal ID that packages audience with inventory: see the `curation-and-curated-marketplaces` skill and its Sources.

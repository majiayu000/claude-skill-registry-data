---
name: curation-and-curated-marketplaces
description: Build and buy curated PMP deals that package audience or contextual data onto premium inventory and hand the buyer a single Deal ID. Use when the user asks about curation, curated marketplaces, sell-side curation, a curation platform, data-onboarded deals, packaging first-party or third-party data into a Deal ID, buy-side vs sell-side curation, curated PMP, Amazon Certified Supply, Index Exchange or Magnite or PubMatic curation, fee stacking or take rates on curated deals, or whether curation is cheaper than DSP-side targeting.
---

# Curation and curated marketplaces

Package data and premium supply into one Deal ID a buyer can activate in seconds, and understand who takes a cut along the way. Curation moves the targeting decision from the buy side (a DSP audience segment layered on open auction) to the sell side (a curator who pre-selects inventory, attaches data, and exposes it as a private deal). Done right it cuts data-match loss, cleans the supply path, and hands a trafficker a working deal instead of a segment build. Done wrong it stacks a curation fee on top of the SSP fee on top of the DSP fee, and the advertiser pays three intermediaries to reach inventory they could have bought direct.

This skill covers curation mechanics that apply across curators and DSPs (DV360, The Trade Desk Kokai, Amazon DSP). It assumes you know CPM, PMP, Deal ID, take rate, and match rate. For that math and those definitions see the `programmatic-foundations` skill.

## When to use this skill

- "What is curation / a curated marketplace / sell-side curation?"
- "Should I build the audience on the sell side or the buy side?" / "Buy-side vs sell-side curation?"
- "Package our first-party or a third-party segment into a Deal ID." / "How do I onboard data into a curated deal?"
- "What is Amazon Certified Supply / Index Exchange curation / Magnite ClearLine / PubMatic Activate?"
- "How much does curation cost?" / "What is the fee stack on a curated deal?" / "Is curation cheaper than DSP targeting?"
- "The curated deal is underdelivering / the CPM is higher than expected / the match rate looks low."

Boundaries with sibling skills:
- Reducing the number of SSPs and reseller hops between the DSP and the publisher, DSP-side SPO controls, OpenPath, and transparency data (sellers.json, OpenRTB SupplyChain, Sincera): `curation-and-supply-path-optimization`. Curation and SPO overlap because a good curator also shortens the path, but that skill is the path, this skill is the packaged deal.
- Which retail or commerce network to buy and the onsite/offsite/in-store surfaces: `retailmedia-foundations-and-networks`. Amazon Certified Supply lives at the seam; this skill is the curation mechanic, that skill is the network choice.
- How a Deal ID is plumbed into a line item once you have it: `dv360-deals-and-inventory` (DV360), `ttd-inventory-and-deals` (Kokai), or `amazon-dsp-inventory-and-supply`. This skill is what goes into the deal and who gets paid; those skills are the trafficking.
- Whether your first-party segment is even legal to onboard and activate in a given region, and consent to do so: `data-subject-rights-and-subprocessor-governance` and `consent-signal-verification-and-decode`.
- Bidding the deal once it is on a line item (fixed for guaranteed rate, automated for a floor-priced deal): `dv360-bid-strategy`.

## Quick reference

Decide these in order before you build or buy a curated deal.

| Decision | Options | Pick this when |
| --- | --- | --- |
| Curate or not | Curated deal vs open auction + DSP segment | Curate when the data does not travel well buy-side (low match, signal loss), when you need the supply pre-vetted, or when you want a trafficker-ready Deal ID. Skip curation when your DSP already has the segment at scale and a clean path. |
| Where the data lives | Sell-side (curator attaches it) vs buy-side (DSP layers it) | Sell-side when the match happens closer to supply (higher effective match, less cookie loss), or the data owner only exposes it via a curator. Buy-side when your DSP holds the segment natively. |
| Who curates | Retail or commerce curator (Amazon, retailer clean rooms) vs independent SSP curator (Index Exchange, Magnite, PubMatic, and curation-native platforms) vs your own agency curation seat | Retail curator for closed-loop shopper data; SSP curator for scaled contextual and third-party data; agency seat when you run enough volume to justify operating a curation platform. |
| Deal type | Programmatic Guaranteed, Preferred/Private Auction (single-buyer PMP), or open-with-data (curated PMP available to a buyer list) | PG for guaranteed volume at a fixed rate; private auction for priority with a floor; curated PMP for scaled data-attached supply at a floor. |
| Fee posture | Accept the curator fee vs go direct vs negotiate a disclosed take rate | Accept the fee when curation adds match, path cleanliness, or access you cannot get otherwise. Go direct when the curator only re-wraps supply you could buy at the SSP. Always ask for the take rate in writing. |

The one-line model: a curator sits on the sell side, pre-selects inventory, attaches audience or contextual data to it, and exposes the package as a single Deal ID that any authorized DSP seat can activate. The buyer trades a curation fee for a working deal and, often, a higher effective match rate than layering the same data buy-side.

## Core process

1. Decide whether the job even needs curation. If your DSP already holds the segment natively, at scale, on a clean path, layering it buy-side is cheaper (no curation fee). Curation earns its fee when the data matches better near supply, when signal loss on the open path is killing buy-side match, when the data owner only exposes the segment through a curator, or when you want a trafficker-ready Deal ID instead of a segment build. State the reason before you curate.
2. Choose the curator by data type. Closed-loop shopper or loyalty data lives in retail and commerce curators and clean rooms (Amazon Certified Supply exposes Amazon Shopper Insights packages through Magnite, PubMatic, and Index Exchange). Scaled contextual and third-party audience data lives in independent SSP curation platforms. If you run enough volume, an agency curation seat lets you build and resell your own packages.
3. Define the package: supply plus data plus terms. Name the inventory set (publisher list, formats, channels, geos), the data attached (your first-party segment onboarded, or a third-party segment licensed through the curator), and the deal terms (rate or floor, volume, position or separation if premium). The curator builds this into a Deal ID.
4. Confirm the data is legal to onboard and activate here before it goes live. First-party data needs a lawful basis and consent to onboard into a curator and activate against a user. Suppress denied users. Hand off to `consent-signal-verification-and-decode` and `data-subject-rights-and-subprocessor-governance`. Do not skip this because the curator says the data is "already matched."
5. Map the fee stack before you accept the deal. Every hop takes a cut: DSP fee, curation fee, SSP fee, and any data-license fee. Ask each intermediary for its take rate in writing and compute the working media percentage (the share of the advertiser's dollar that reaches the publisher). If curation adds a fee without adding match, path cleanliness, or access, buy direct instead. Full stack math is in `references/fee-stacking-and-savings.md`.
6. Traffic the Deal ID and verify it delivers against the package, not just against any impression. A Deal ID is a pointer; confirm the deal is targeting the curated supply and data you specified, that the seat is authorized, that the floor is not above the clearing price, and that match rate and CPM match the quote. Deal plumbing is in the DSP sibling skills; verification is below.
7. Recommend, then human-gate. Read the deal, model the fee stack and expected match, and recommend a posture (curate, go direct, or renegotiate the take rate). Do not commit spend or accept a deal on the client's behalf. A human approves the curated deal and its terms.

## Decision rules and thresholds

### When curation wins over buy-side targeting

- Match rate is the deciding number. Layering a segment buy-side loses matches to cookie and identifier loss on the open path. Sell-side curation matches closer to supply and on the SSP's own graph, so effective match is usually higher. If your buy-side match on a segment is weak (many DSP audiences match well under half of a segment in signal-degraded environments), a sell-side curated version of the same data often reaches more of it. Confirm the actual match on both sides before deciding; do not assume.
- The data owner only exposes the segment through a curator. Some first-party and retail datasets are activatable only as a curated Deal ID, never as a portable segment. Then curation is not optional.
- You want the supply pre-vetted. A curator can pre-filter to brand-safe, MFA-free, well-performing supply so the buyer does not rebuild that exclusion list per campaign.
- You want a trafficker-ready deal. One Deal ID beats a segment build plus an inventory package plus an exclusion list, especially across many advertisers.

### When to skip curation and buy direct or buy-side

- Your DSP holds the segment natively at scale on a clean path. Layering it buy-side avoids the curation fee entirely.
- The curator only re-wraps supply you could buy at the SSP with no added data, no added match, and no cleaner path. That is a fee for nothing. Buy the SSP deal direct.
- The fee stack pushes working media below what the incremental match justifies. If curation adds five to fifteen points of fee and lifts effective match by only a few points, the math loses. Model it (see the fees reference).

### Sell-side vs buy-side, the rule

Put the data where it matches best and travels least. Match near supply (sell-side) when the open path degrades identifiers and your buy-side match is weak. Keep it buy-side when your DSP holds the segment natively and the path is clean, because you avoid a fee. The tie-breaker is the measured match-rate delta minus the curation fee, not the sales pitch.

### Deal type inside a curated package

- Programmatic Guaranteed: fixed rate, committed volume, guaranteed delivery. Bid it fixed (the rate is set). Use for premium supply where you need the volume locked.
- Private auction / preferred deal (single-buyer PMP): priority access at a floor, no hard volume commitment. Bid automated with the floor as the price. Use for scaled priority with data attached.
- Curated PMP open to a buyer list: the same data-attached package offered to several seats at a floor. Bid automated. Use for scaled reach where you do not need exclusivity.

The mechanics of a Deal ID (packaged vs curated, single-DSP vs multi-DSP, always-on vs campaign-scoped) are in `references/deal-id-mechanics.md`.

### Take-rate discipline

Ask every intermediary for its take rate in writing. A curated deal can pass through a DSP fee, a curation fee, an SSP fee, and a data-license fee. Compute working media (publisher share of the advertiser dollar). If any party will not disclose its take rate, treat that as a reason to prefer a more transparent path, because you cannot value the deal without it. The 2026 push across the ecosystem is disclosed take rates and shorter paths; hold curators to it.

## Reference material

- `references/sell-side-vs-buy-side-curation.md`: the full side-by-side of where data is matched and activated, the match-rate mechanics that make sell-side win in degraded environments, the 2026 curator landscape (Amazon Certified Supply through Magnite/PubMatic/Index Exchange, independent SSP curation platforms, agency curation seats), and a decision table by data type and DSP. Read this when choosing where to put the data and which curator to use.
- `references/deal-id-mechanics.md`: how a curated Deal ID is constructed and travels, the deal-type field map (PG vs private auction vs curated PMP) per DSP, seat authorization and multi-DSP activation, the OpenRTB deal object and pmp/deals fields, and a verification checklist for why a curated Deal ID is not delivering. Read this when building, plumbing, or debugging a curated Deal ID.
- `references/fee-stacking-and-savings.md`: the full fee-stack model (DSP, curation, SSP, data-license fees), a worked working-media calculation with real percentages, when curation saves money versus when it stacks cost, the take-rate disclosure questions to ask, and how curation interacts with supply path optimization to net a saving. Read this when modeling the economics or deciding whether the curation fee is worth it.

## Templates and examples

- Retail closed-loop shopper deal: an advertiser wants to reach lapsed category buyers on premium CTV. The retailer's shopper segment is activatable only as a curated Deal ID (for example Amazon Shopper Insights packaged through PubMatic into Amazon Certified Supply). Curate it. The data matches on the retailer's closed-loop graph, which no buy-side layer can reach. Bid the PG deal fixed at the quoted rate. Confirm consent to activate the shopper data in each region first.
- First-party CRM segment, weak buy-side match: an advertiser's CRM segment matches only about a third buy-side after identifier loss. Onboard the same segment sell-side through an SSP curation platform, which matches closer to supply on the SSP graph and reaches more of the list. Compare the two match rates directly before committing, then curate if the sell-side delta beats the curation fee.
- Contextual package the DSP already has: the advertiser wants a standard contextual category the DSP offers natively at scale. Do not curate. Layer the DSP's contextual segment on a clean open-auction path and skip the curation fee. Curation would add cost with no added match or access.
- Curator re-wrapping open supply: a curator quotes a "premium curated PMP" that, on inspection, is open-auction supply from one SSP with no data attached and no exclusion list. Buy the SSP deal direct or run open auction with your own exclusions. The curation fee buys nothing here.

## Common pitfalls

- Paying for curation that adds no match. The fee is only worth it if it buys higher effective match, cleaner supply, or access you cannot get otherwise. Re-wrapped open supply with a fee on top is the most common trap. Model the fee against the measured match delta.
- Skipping the consent check because "it is already matched." Onboarding and activating first-party or licensed data still needs a lawful basis and consent, and denied users must be suppressed, regardless of who did the match. This is a legal exposure, not a technicality. Route through `consent-signal-verification-and-decode`.
- Not asking for the take rate. If you cannot see the curation fee, the SSP fee, and the data-license fee, you cannot compute working media and you cannot value the deal. Undisclosed take rates hide fee stacking. Ask in writing.
- Confusing curation with SPO. Curation packages data onto supply; supply path optimization shortens the path to that supply. A strong curator does both, but assuming a curated deal is automatically a clean path is wrong. Verify the path with transparency data (see `curation-and-supply-path-optimization`).
- Trafficking the Deal ID and assuming it targets the package. A Deal ID is a pointer to a deal on the SSP; if the seat is not authorized, the floor is above the clearing price, or the deal was built against the wrong supply, it silently underdelivers or delivers the wrong impressions. Verify match rate and CPM against the quote (see the deal-id mechanics reference).
- Curating a segment your DSP already has natively at scale. You pay a curation fee to reach data you could have layered buy-side for free on a clean path. Check the native DSP option first.

## Sources

- [The Trader's Guide to Supply Path Optimization (SPO)](https://www.thetradedesk.com/resources/the-traders-guide-to-supply-path-optimization-spo) (as of July 2026)
- [OpenPath, The Trade Desk](https://www.thetradedesk.com/our-demand-side-platform/openpath) (as of July 2026)
- [Amazon Certified Supply Exchange](https://advertising.amazon.com/library/news/certified-supply-exchange) (as of July 2026)
- [sellers.json, IAB Tech Lab](https://iabtechlab.com/sellers-json/) (as of July 2026)
- [Amazon Marketing Cloud](https://advertising.amazon.com/solutions/products/amazon-marketing-cloud) (as of July 2026)

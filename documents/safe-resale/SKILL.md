---
name: safe-resale
description: "Plans the safe sale of a valuable item (watch, bag, jewellery, collectible, camera, electronics, art) for the best realistic net amount. Identifies the item exactly, gathers authenticated sold comps instead of asking prices, works out net proceeds per channel after fees, shipping, insurance and time, compares buyout, consignment, auction, authenticated marketplaces and local sales, checks buyers for scam patterns, and writes a step-by-step sale plan with safe payment, handover, shipping and photo-privacy rules. Use when someone says \"sell my watch\", \"where should I sell this\", \"what is my bag worth\", \"is this buyer a scam\", \"consign or sell\", \"should I take this offer\", or \"how do I ship this safely\"."
---

# Safe Resale

Most people price from asking prices and meet whoever messages first. That is how they get underpaid, scammed or robbed. This skill picks the channel with the best **expected net after all costs and risks**, then makes the sale boring and safe.

## What it does

Identifies the item, finds sold comps, computes net per channel, ranks the channels, screens buyers for scams, and writes a sale plan from `templates/SALE-PLAN.md`.

## What you need

- Brand, model, reference or SKU, size, colour, material, year if known.
- Photos of the item now (not purchase-day photos), including every flaw.
- What comes with it: box, papers, receipt, warranty card, service records, accessories.
- Where the item is, and whether you will ship it or only sell locally.
- Your priority: fastest cash, highest net, least effort, or lowest risk.
- Any offers or buyer messages you already have, pasted in full.

If something is missing, plan anyway and list the gaps as risks.

## Steps

### 1. Identify the item exactly

Price depends on the exact reference, size, material, colour, year and edition. Read model numbers, date codes and hallmarks from the photos. Map each receipt and accessory to the right item. Receipts and boxes support provenance; they do not prove authenticity. Never declare an item authentic from photos alone.

Give a named condition grade (new, excellent, good, fair, damaged) and cite the photo that justifies it.

### 2. Gather sold comps

Rank evidence in this order:

1. Recent authenticated sold prices for the same model, condition and accessories.
2. Written buyout quotes from specialist dealers.
3. Consignment or auction realized prices.
4. Active asking prices, only as a weak ceiling.

Drop mismatches, bundles, personalised pieces and outliers. Report comp count, date range and middle of the range. Retail price is cost, not value.

### 3. Work out net per channel

For each channel, use one formula and show the inputs:

```
net = expected sale price
      - commission or seller fee
      - payment processing fee
      - shipping + insurance + packaging
      - authentication or listing fees
      - customs, duty or currency conversion (if cross-border)
      - expected markdowns (consignment) or unsold-lot fees (auction)
```

Then adjust for time and risk:

```
risk-adjusted net = net x probability the sale completes cleanly
```

Example to check, not a quote: if a consignment channel might sell at price P with a commission of C percent after one markdown of M percent, net = P x (1 - M) x (1 - C) - shipping. Look up real fee tables; get the item's category and fee tier in writing when it changes the commission.

### 4. Compare channels

| Channel | Usually best for | Main trade-off |
|---|---|---|
| Instant buyout / dealer | Speed, zero buyer risk | Lowest price |
| Managed marketplace with authentication (Chrono24, The RealReal, Vestiaire, eBay authenticity programs) | Balance of price and protection | Fees, holds, disputes still possible |
| Consignment | No buyer contact | Slow, markdowns, commission |
| Auction house (Christie's and similar) | Rare or high-demand pieces | Lot must be accepted, fees, payout waits on buyer |
| Peer-to-peer local (local marketplaces) | Highest gross | Highest scam and safety risk |

Default order for counterfeit-sensitive or portable items: buyout, authenticated marketplace, consignment, auction, local peer-to-peer last. A buyout offer within a few percent of the best risk-adjusted net is usually the right call because it removes transit, return and chargeback risk.

Get two or three written buyout quotes with the same photos before revealing any other offer or your floor.

### 5. Screen the buyer and the payment

Run every offer through the red flags below. One flag means slow down. Two means walk away.

### 6. Hand over safely

**In person:** meet in a bank lobby during business hours (best when paying cash, since the teller can check and deposit it) or an official police-station safe exchange zone. Bring another adult and share your location. Keep the item in your hands during inspection. Confirm funds **in your own banking app or at the teller**, never on the buyer's phone. Sign two copies of a bill of sale, then hand over.

**Shipping:** ship only to the address on the platform order. Use a rigid box, staffed counter drop-off (no drop box), tracking, full declared-value insurance and signature on delivery. Film the packing continuously, photograph the sealed box and label, and keep the receipt. Insurance covers loss and damage in transit, not authenticity disputes or chargebacks. For cross-border sales, declare contents and value truthfully; never mark goods as a gift.

### 7. Document everything

Before handover, take timestamped photos of every side, serial, marking, accessory and flaw. Keep the listing, messages, authentication result, bill of sale and payment record. An "as-is" note records condition; it does not stop every dispute.

### 8. Redact listing photos

Before anything goes public, hide: full serial numbers (show a partial if buyers expect it), receipt addresses, account and card digits, order and authorization codes, signatures, faces, and reflections in polished metal, glass or screens that show you, your home or a window view. Also strip location data (EXIF) from photos. Share unredacted documents only with the authenticator or buyer platform that requires them.

## Scam red flags

- **Fake payment proof:** a screenshot or email saying "payment sent". Only your own account counts.
- **Overpayment:** buyer sends more than the price and asks for the difference back. The original payment later bounces.
- **Chargeback setups:** card or goods-and-services payment, buyer later claims "not as described" or "not received".
- **PayPal friends and family (or any no-protection transfer) offered by the buyer to "save fees":** it protects neither side and is common in both directions of fraud. Treat peer-to-peer apps as reversible if the sender's account was stolen.
- **Escrow scams:** buyer insists on an escrow site you have never heard of, sends the link themselves.
- **Shipping to a forwarder, a different address, or "my courier will collect":** the item vanishes, and platform protection is void.
- **Verification-code requests:** "send me the code to prove you are real". It is an account takeover.
- **Checks, cashier's checks, money orders, gift cards, crypto, wires from strangers.**
- **Pressure:** urgent deadlines, sob stories, full price sight unseen, last-minute meeting changes.
- **"Let me take it to get it authenticated":** never let the item leave before payment clears.
- **Return substitution:** buyer returns a fake or a damaged one. Record serials and close-up marks so you can prove what left.

## Output

A filled `templates/SALE-PLAN.md`: the recommended channel in two sentences, item identity and grade, comps (sample size, dates, middle of range), a channel table with risk-adjusted net shown as formula plus inputs, your list price, accept and walk-away numbers, handover or shipping steps, the photo, document and redaction checklists, and sources with the date checked.

## Honest limits

- Not legal, tax or financial advice. Selling above cost can be taxable; rules on reporting, consumer rights and cross-border sales vary by country and region. Check local rules or ask a professional.
- Fees, authentication programs, carrier coverage and safe-zone locations change. Verify on the official page before relying on any of them, and note the date.
- Photos cannot prove authenticity. Only a physical inspection by a qualified authenticator can.
- No method removes all risk. This plan lowers it and leaves a paper trail if something goes wrong.

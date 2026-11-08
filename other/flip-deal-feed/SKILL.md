---
name: flip-deal-feed
description: Sweep live residential and small-commercial listings in a target buy-box, screen every one through the 70% flip rule, firm ARV from real sold comps, and surface a ranked shortlist with first-pass deal briefs (buy-right number, rehab scope, cash in, monthly payment, net upside as a range) — plus NOI-over-cap valuation and a levered underwrite for small multifamily value-add. Use when evaluating properties to buy-renovate-resell, building a "what should we go look at" list, or pressure-testing whether a candidate property pencils.
compatibility: >-
  Python 3 scripts are offline. Listing sweeps fetch public listing pages; comps use grounded search with the user's own key.
metadata:
  network-hosts: "www.century21.com www.commercialsearch.com generativelanguage.googleapis.com"
  network-purpose: "read public listing pages and search for sold comps"
---

# Flip Deal Feed

Turn a whole metro's listings into a handful of properties worth driving to. Given a **buy-box** (cities + drive-time constraint) and a **budget**, this sweeps the live listings, screens each through the **70% rule**, estimates ARV from real sold comps, and ranks by margin of safety — then writes a practical, no-nonsense brief for the survivors.

Reference run (2026): a five-suburb inner-ring buy-box, 276 listings swept, 5 prospects surfaced. The screen/calculator engine is `scripts/flip_screen.py`; the commercial underwrite is `scripts/cre_underwrite.py`. Both run standalone (`python3 flip_screen.py` prints a demo on fictional listings).

Write plainly (see `copy-voice`). The brief is for **someone evaluating a buy** — practical and specific (what needs doing, what to offer, what to confirm onsite), never hype.

## The honest tooling split (read first)

- **Sweeping listings = `WebFetch` the listing pages.** NOT Gemini. The pages below render server-side, so the native `WebFetch` tool retrieves them cleanly. (Redfin, Zillow, homes.com, Movoto, LoopNet, Crexi all **403** automated fetches — don't bother.)
- **ARV + comps + rents = grounded web search** (`gemini-web-search`). Finding recent sold comps near an address, or a commercial building's submarket rents, is a *research* question. Using search to fetch a known listing URL is the wrong tool.

## Step 1 — Sweep the buy-box (WebFetch)

**Residential — Century21** (renders, returns structured rows):
```
https://www.century21.com/real-estate/<city>-<st>/LC<ST><CITYUPPERNOSPACES>/
# e.g. springfield-il/LCILSPRINGFIELD/  (state code lower in the slug, upper in the id)
```
Fetch one city per call; ask for address, price, beds, baths, sqft; exclude condos/townhomes.
A city page returns ~50–75 single-family rows. Sweep every city in the box.

**Commercial — CommercialSearch** (renders; the residential sibling point2homes 403s):
```
https://www.commercialsearch.com/for-sale/commercial-real-estate/us/<st>/<city>/
```
Ask for address, price, type, building sqft, units, and any cap/NOI. Skip vacant land.
**But CommercialSearch is thin** — most box inventory is over-budget, "contact for
pricing," or missing NOI. For the small **multifamily value-add** plays (4–16 units,
the real commercial fit for "renovate → raise rents → resell"), **use grounded search** — it
reads Google's index and surfaces Crexi/Zillow/LoopNet listings (with address, price,
units, even the in-place NOI) that all 403 a direct fetch:
```bash
python3 gemini_search.py "small apartment buildings 4-16 units for sale under \$1.5M in <cities>, with address, price, units, NOI"
```

**Commercial valuation (NOI ÷ cap), `flip_screen.py`:**
```python
from flip_screen import value_add
value_add(noi_now, noi_stabilized, market_cap=0.0575, price=795_000)
# going-in cap, in-place value at market cap, stabilized value, value created
```
Value = NOI ÷ cap, not a comp spread. The value-add lever is below-market rents +
trimmed opex; every $1 of NOI growth = $1 ÷ cap of value. **Commercial is a 12–24mo
reposition, not a 6-month flip** — say so; the timeline differs from residential.

**Full levered underwrite** (DSCR, cash-on-cash, IRR, exit at a cap range):
`scripts/cre_underwrite.py` — `underwrite(price, noi_in,
noi_stab, capex, down=, rate=, exit_cap=)`. Models a value-add ramp (negative year-1
carry for a vacant-on-purchase deal). Always run the **buy-below-ask + cheaper-debt**
scenario — at ask it usually looks like a dud.

## Step 2 — Screen through the 70% rule (`flip_screen.py`)

```python
from flip_screen import screen
rows = screen(listings, arv_by_city)   # ranked; clears_at_ask flag + discount_to_offer_pct
```
- **MAO = 0.70 × ARV − rehab.** The 30% gap is financing + holding + selling + profit.
- Rehab is a uniform desk estimate ($/sqft); the brief refines it per property.
- **The deals are the listings priced *below* the area cluster.** At-retail listings won't clear — that's normal. Surface the mispriced/distressed ones and the value-add plays (2/1 → 3/2, add a bath, finish a basement).

## Step 3 — Firm the ARV (grounded search)

For each survivor, pull real recent sold comps to replace the desk ARV:
```bash
python3 gemini_search.py "recent sold comparable homes near <address>, renovated, <beds>bd <sqft>sqft, last 6 months, with sale prices"
```
Show ARV as a **range, not a point** (`flip_screen.deal()` returns net upside across an ±8% ARV band). A flip lives or dies on ARV − all-in; never print a fake-precise profit.

## Step 4 — The deal math (`flip_screen.deal()`)

Generic, no lender required — vary down% and rate to see the levers:
```python
from flip_screen import deal
deal(purchase=160_000, rehab=50_000, arv=320_000, down=0.20, rate=0.08, months=6)
# -> cash_in, monthly_payment, net_low/mid/high
```
Report the three numbers the buyer asks for: **cash down needed · monthly payment · net upside (range).**

## Step 5 — The prospect brief (the deliverable)

One page per survivor, built from data we have, with the unknowables flagged:

1. **Snapshot** — address, ask, beds/baths/sqft, year built, last sale, assessed value, days-on-market (county record + listing; all real).
2. **Buy-right number** — MAO vs ask. "Offer $X. Asking $Y. Gap $Z." The go/no-go.
3. **ARV** — 3–5 real sold comps (grounded search), as a range.
4. **Rehab scope** — line items from photos/age with $ ranges, and explicit **`CONFIRM ONSITE`** for what a desk can't see (foundation, sewer line — get a $150 scope, panel, asbestos/lead pre-1978, roof + mechanicals age). Note where the buyer's own sweat labor halves a cosmetic line, but keep licensed trades at full price.
5. **Deal math** — cash in, monthly, net upside range.
6. **Verdict** — GO / NO-GO / WALK IT.

## Buy-box / drive-time

Confirm each candidate against the drive-time constraint before it counts (e.g. within 20 minutes of two anchor addresses). A cheap house outside the box is not a prospect.

## Learnings / guardrails (earned on the reference run — don't relearn them)

1. **A cheap attached unit is not a discounted house.** Century21 sweeps include
   townhomes/condos. A "$160K, 3/2" looked like a 50%-off distress vs a
   $320K SFR ARV — it was a **1983 townhome** whose **portal AVM ($160,431) = the list
   price.** No discount; priced right. **Verify property TYPE and cross-check list
   price against an AVM (Redfin/Zillow estimate) before calling anything a discount.**
   `flip_screen.screen()` now flags `type` in {townhome,condo} and `ask >= 0.93*avm`.
2. **Verify ACTIVE status before briefing.** A 4-plex
   had the biggest rent gap on the board — and was **Pending.** Search results can be
   stale (it surfaced a 2024 status). Confirm the listing is live, not pending/sold.
3. **Opex structure is the value driver, not just rents.** An 8-unit (owner pays
   heat+water+trash → 46% opex) vs a 7-unit (electric separately metered,
   owner pays only water/sewer → ~35%). Capture **who pays which utility** — master-
   metered heat/water is the RUBS/sub-meter upside, often bigger than the rent bump.
4. **Use the right cap rate for the class/era.** 1950s–60s Class-C walk-ups traded
   ~**6.5–8%** in the reference market, NOT the 5.6–5.75% institutional Class-B figure. Using
   the low cap overstated value-creation ~2× on the first pass. Show a
   **cap-rate football field** (value at 6.0/6.5/7.0/7.5%) — never a single cap.
5. **Run the going-in DSCR.** At ~7% commercial debt, these buildings' in-place NOI
   barely covers debt service (DSCR ~1.03 at 25% down). The deal only
   becomes financeable *after* the value-add — plan 30%+ down or a buy-down, and say so.
6. **Strategic read for that box (check yours):** SFR flips are priced efficiently (retail) — the
   survivors are mostly cheap attached units with no real margin. **The edge here is
   small-multifamily value-add, not house flips.** Steer effort accordingly.
7. **Negative leverage is the trap whenever cap < debt rate (it was in 2026).** These small-MF/industrial deals list at
   ~6–6.5% caps while debt is ~7% — cap < rate, so **leverage drags returns down.** At
   ask, all three live prospects underwrote to 1–4% levered IRR. They only reach a
   real return (12%+) by **buying ~12% under ask** (push going-in cap above debt cost)
   **+ cheaper agency/credit-union debt (~6.5%).** Always lead the underwrite with that
   scenario; never present an at-ask IRR as the deal. The money is made on price, not reno.

## Done when

- The whole box is swept (every city), not one city — state the count evaluated.
- Survivors are ranked by margin of safety, ARVs are real comps (not desk estimates), and each has a target offer.
- Every figure is real public data or a clearly-labeled estimate — nothing invented.
- The brief reads practical and specific (what to offer, what to fix, what to confirm onsite), plain language holds.
- Commercial survivors carry an NOI/rent-roll caveat if the listing didn't publish one (value = NOI ÷ cap).


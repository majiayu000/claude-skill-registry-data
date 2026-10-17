---
name: cost-estimation
description: Use when constructing the Estimated cost ballpark section of a trip plan. Encodes bucket structure (flights+pass+lodging+food+extras), 2026 family-of-N anchors, and the re-verify-at-booking marker. Invoked by trip-planner.
type: reference
---

# cost-estimation

A ballpark that gives the family enough information to decide go/no-go without pretending to be a quote. Always frame as "planning estimate, re-verify at booking."

## The bucket structure

Always render as a Markdown table with **bucket | per-person | family total** columns. Don't skip buckets — visibility is the point.

```markdown
| Bucket | Per person | Family of N |
|---|---:|---:|
| Flights / fuel | $X | $Y |
| Transit pass / car rental | $X | $Y |
| Scenic-train supplements / paid attractions | $X | $Y |
| Lodging — <base 1>, N nights | — | $Y |
| Lodging — <base 2>, N nights | — | $Y |
| Food | — | $Y |
| Local cable cars / tours / extras / tips | — | $Y |
| **Trip total** | — | **$lo – $hi** |
```

## Why ranges, not point estimates

A point estimate ("$8,500") feels precise but is wrong. Always render as a range (`$8,300 – $13,000`) so the family understands the swing. Communicate which buckets drive the swing — usually flights and lodging-tier.

## 2026 family-of-4 anchors (re-verify at booking)

These are calibration anchors, not quotes. Use them to sanity-check estimates; always state "re-verify at booking."

### International flights from IAH (round-trip, mid-range main cabin)

| Destination | Per person | Family of 4 |
|---|---:|---:|
| London / Paris (LHR / CDG) | $700 – $1,200 | $2,800 – $4,800 |
| Frankfurt / Zurich (FRA / ZRH) | $900 – $1,500 | $3,600 – $6,000 |
| Rome / Madrid | $850 – $1,400 | $3,400 – $5,600 |
| Tokyo (NRT / HND) | $1,200 – $1,900 | $4,800 – $7,600 |
| Reykjavík (KEF) | $700 – $1,100 | $2,800 – $4,400 |
| Cancún / Caribbean | $400 – $700 | $1,600 – $2,800 |

Add ~30% in summer / Christmas / spring break.

### Domestic flights from IAH (RT mid-range)

| Destination | Per person | Family of 4 |
|---|---:|---:|
| Denver / Phoenix / Salt Lake City | $250 – $450 | $1,000 – $1,800 |
| LA / SF / Seattle | $300 – $550 | $1,200 – $2,200 |
| Miami / Orlando | $200 – $400 | $800 – $1,600 |
| New York / Boston | $250 – $500 | $1,000 – $2,000 |

### Lodging (per-night, family room or 2BR)

| Region | Mid-range | Notes |
|---|---:|---|
| Switzerland | $300 – $700 | Highest in Europe |
| Italy / France / Spain | $180 – $450 | Cinque Terre / Paris highest |
| UK | $200 – $400 | London highest |
| Japan | $150 – $400 | Ryokan with meals separate tier |
| Iceland | $250 – $500 | Reykjavík highest |
| US national park town | $200 – $450 | In-park lodges 30% premium |
| US Gulf beach (Destin / 30A) | $250 – $600 | Peak summer; off-season half |
| US mid-tier road trip | $130 – $250 | Hampton / Holiday Inn Express |
| Cabin / Airbnb (US rural) | $150 – $350 | Beavers Bend, Hocking Hills |

### Food (family of 4, per day)

| Region | Cooking-mix | Restaurants-only |
|---|---:|---:|
| Switzerland / Norway / Iceland | $130 – $200 | $250 – $400 |
| France / Italy / Spain | $100 – $160 | $180 – $300 |
| UK / Germany | $90 – $150 | $160 – $260 |
| Japan | $80 – $140 | $140 – $240 |
| US (mid-tier) | $80 – $130 | $130 – $220 |
| Caribbean all-inclusive | included | — |

### Driving (US)

- Gasoline: 25 mpg car × $3.20/gal × distance ÷ 25 = fuel cost
- Tolls: variable; budget $30–$100 round-trip on east-coast / Texas trips
- Wear & tear: $0.20/mile is a planning rule of thumb
- Rental car (mid-size, 1 week): $400 – $700 + insurance + fuel

### Rail passes

| Pass | Adult cost (2026) | Notes |
|---|---:|---|
| Swiss Travel Pass 8-day 2nd class | ~$510 | Kids < 16 free with Family Card |
| Swiss Travel Pass 6-day 2nd class | ~$430 | |
| JR Pass 7-day | ~$340 | (post-2024 hike) |
| JR Pass 14-day | ~$540 | |
| Eurail Global 7-day-in-1-month | ~$510 | |
| BritRail 8-day | ~$380 | |

### Notable extras

| Item | Cost |
|---|---|
| Jungfraujoch (with 50% Swiss Travel Pass discount) | ~$95/adult |
| Glacier Express seat reservation supplement | ~$45/person |
| Antelope Canyon tour | ~$120/person |
| Vatican Museums skip-line | ~$45/person |
| Northern Lights Iceland tour | ~$120/person |
| Disney Park 1-day ticket (peak) | ~$170/person |

## The "swing factor" rule

When the range is wide, name what drives it. Example for #68:

> Big swings come from flights (book early) and lodging tier. Switzerland is genuinely expensive — budget closer to the top of that range if traveling in school summer holidays.

This converts an opaque range into actionable intel.

## Always include the re-verify marker

Every cost section must include this line (or equivalent), prominently, before the table:

> Planning estimate only — re-verify everything at booking. Prices in USD, rounded.

This protects against quotation-creep where the family takes the number as a commitment.

## Currency handling

For non-USD destinations:

- Quote in USD for the family's mental model (they're Houston-based)
- For flagship items (the big rail pass, the headline experience), parenthetically include the local currency for booking-page reference: `~$510 (CHF 460 / 8-day 2nd class)`
- Note the currency in the watch-outs section: "Switzerland uses CHF, not Euros."

## What to deliberately leave out

- Travel insurance — varies wildly; mention as a checklist item
- Souvenirs — unbounded
- Specific restaurant prices — too volatile
- Cellular roaming — depends on carrier plan
- Lost-luggage / weather contingency — by definition unpredictable

State explicitly that these are not in the estimate so the family doesn't expect the budget to cover them.

## Reference

- **#41 Beavers Bend:** mid-tier US cabin trip; total ~$1,500 – $2,500 family of 4 for 4 nights
- **#68 Switzerland:** family-of-4, 7 days, $8,300 – $13,000 range; flights and lodging swing-factors named explicitly

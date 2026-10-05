---
name: fleet-fuel-card-programs
description: |
  Use when a carrier asks about fuel-card vendor selection (Comdata, EFS, WEX, RTS, Pilot Flying J,
  Love's Connect), discount levels, fraud control, driver authorization PINs, IFTA reporting features,
  cash advance, money codes, or how the card fits into payroll/settlement workflows.
---

# Fleet Fuel Card Programs

A fuel card is the operating layer for every motor carrier. It controls fuel purchases, captures IFTA data, enforces driver limits, prevents fraud, and provides discounts at major truck stops.

## Major vendors

| Card | Network strength | Discount range | Fee structure |
|---|---|---|---|
| Comdata | Largest national network, all major stops | $0.04–$0.10/gal off cash | Monthly card fee + per-transaction |
| EFS (WEX-owned) | TA/Petro strong, also Pilot/Love's | $0.04–$0.08/gal | Subscription + transaction |
| WEX | All Loyal + Pilot/Love's | $0.03–$0.07/gal | Per-transaction |
| RTS Financial | Bundles with factoring | $0.04–$0.06/gal | Often free with factoring |
| Pilot Flying J My Rewards | Pilot/Flying J only | $0.04–$0.06/gal | Free |
| Love's Connect | Love's only | $0.04–$0.06/gal | Free |
| OTR Solutions | Bundles factoring + fuel | Varies | Bundled |

Most fleets use **Comdata or EFS** as primary and supplement with **Pilot/Love's branded** at preferred stops to layer discounts.

## Discount mechanics

Truck stops display two prices: **cash retail** and **cash discount**. The fuel-card discount applies to cash discount (NOT pump price). At Pilot/Flying J:

- Pump price: $3.95
- Cash discount: $3.85
- Loyalty discount: -$0.02
- Card discount: -$0.06
- **Final price: $3.77**

A driver buying 150 gallons saves $0.18 × 150 = $27 per fill vs cash retail at the pump.

## Driver authorization controls

Cards can be locked to:
- Specific driver (PIN required)
- Specific truck (VIN matched at pump)
- Specific stops (whitelist by chain or location)
- Time windows (no fuel purchases 11 PM–4 AM, etc.)
- Gallon limits per fill (prevents fueling unauthorized trucks)
- Dollar limits per day / week
- Product restrictions (diesel only — no cash advance, no merchandise)

These controls cut fraud rates by 80–90%. A single fraudulent fill (driver fills personal vehicle, sells gallons to other trucks, etc.) can be $400–$800.

## IFTA data capture

Every fuel transaction is captured with:
- State of purchase
- Gallons
- Price
- Date / time
- Card / driver / truck

This feeds **IFTA quarterly reporting** directly — no manual receipt entry. Most carriers connect fuel-card data to their TMS or to IFTA software (TruckBytes, IFTA Plus, etc.).

## Cash advance / money codes

When a driver needs cash (lumper fees, scale tickets, lodging), the dispatcher issues a "money code" or "Comchek" against the card. Driver redeems at any participating location.

| Money code use | Typical amount | Fee |
|---|---|---|
| Lumper service | $50–$300 | $1–$3 |
| Scale ticket | $10–$25 | $1 |
| Lodging | $80–$120 | $1–$3 |
| Emergency repair | $50–$500 | $1–$5 |

Money codes flow into accounting as a driver advance — reconciled at payroll.

## Settlement / payroll integration

Comdata/EFS export driver fuel data into payroll systems:
- Driver fuel purchases → deducted from driver settlement if driver-paid model
- Maintenance / per-stop fees → tracked against truck cost
- Cash advance → driver loan balance

For owner-operators leased on, the carrier passes fuel charges through at cost (with markup for handling — typically $0.005/gal).

## Fraud patterns to watch

| Pattern | Detection method |
|---|---|
| Driver fueling personal vehicle | VIN-tied card or gallon-limit alert |
| Multiple fills same day at different stops | Daily-volume report flag |
| Fuel + non-fuel purchase outside whitelist | Restriction policy + alert |
| Card use after driver termination | Same-day deactivation policy |
| Diesel purchased at suspicious volume vs hours driven | Reconciliation report monthly |

A weekly fuel-card variance review (gallons purchased vs miles driven × MPG) catches most fraud within 7 days.

## Card-program negotiation levers

When changing or adding a fuel-card vendor:
- **Volume commitment** → bigger discount (typically 5,000+ gal/mo unlocks tier 2)
- **Multi-stop loyalty** → stack chain loyalty programs (TA Ultra ONE, Pilot Frequent Fueler) on top of card discount
- **Roll-back** vs **fixed-discount** structure (roll-back gives 1¢ extra at premium stops)
- **Card fees** — negotiable, $4–$6/card/mo typical
- **Transaction fees** — negotiable per stop or waived entirely on volume

## Common mistakes

- Letting drivers fuel at random truck stops without card discount
- Not enforcing PIN per driver — fraud risk
- Skipping the IFTA-data export and re-keying receipts (waste)
- Using one fuel card for owner-operators that they can't see real-time — disputes
- Not deactivating card on driver termination day
- Failing to negotiate annual renewal — discounts compress over time
- Letting drivers buy non-diesel items on the card (food, showers, merchandise) blowing up reconciliation

## Where this fits in X3

X3 imports fuel-card transactions from Comdata, EFS, WEX. Each transaction is matched to truck + driver + odometer (when available) and feeds:
- IFTA quarterly report
- Per-truck MPG calculation
- Driver fuel-economy score
- Fraud detection (gallons vs miles)
- Per-load cost analysis (fuel for that trip)

Onboarding a fuel-card integration is one of the first connections a new X3 carrier makes — high-leverage data with zero driver friction.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=fleet-fuel-card-programs

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

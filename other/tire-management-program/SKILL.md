---
name: tire-management-program
description: |
  Use when a carrier asks about tire program design, when to retread vs replace, position management
  (steer vs drive vs trailer), inflation pressure standards, casing management, scrub rates, road-call
  prevention, or vendor program selection (Bridgestone, Michelin, Continental, Goodyear). Covers
  49 CFR 393.75 and DOT roadside out-of-service criteria.
---

# Tire Management Program

Tires are the #3 maintenance cost line item after fuel and tractor depreciation, and the #1 cause of preventable roadside breakdowns. A managed tire program cuts tire cost-per-mile by 25–40% and out-of-service events by half.

## Cost-per-mile baseline

A typical tractor tire (steer or drive) costs $500–$650 new and lasts 100,000–200,000 miles depending on position, weight, and route. CPM range:

| Position | Tire | CPM range |
|---|---|---|
| Steer | New premium 295/75R22.5 | $0.005–$0.008 |
| Drive | New premium 11R22.5 | $0.006–$0.010 |
| Trailer | New + 1 retread | $0.004–$0.007 |

A 7-axle 18-wheeler runs 18 tires. Tire CPM rolls up to $0.06–$0.10/mile — substantial.

## DOT out-of-service criteria (49 CFR 393.75 + Annex)

A tire is OOS at roadside inspection if:
- Tread depth < 4/32" on any **steer** position
- Tread depth < 2/32" on any **non-steer** position (drive or trailer)
- Visible fabric, cord, or belt
- Tread or sidewall separation
- Flat or noticeable leak
- Cut exposing cord or fabric
- Regrooved tire on a steer position (prohibited)
- Mismatched tire size or load rating on same axle

These are the most common pre-trip-inspection findings. A blown tire on the road can shut down a truck for 4–8 hours and cost $400–$800 service call.

## Inflation pressure — the most-violated standard

Per Bridgestone/Goodyear/Michelin specs:
- Steer: 110 psi
- Drive: 100–105 psi (loaded)
- Trailer: 100 psi

Under-inflation by 10% reduces tire life ~10% AND reduces fuel economy ~0.3 MPG. A 20% under-inflated tire can lose 25% of its expected miles.

### Inflation maintenance

| Method | Cost | Effectiveness |
|---|---|---|
| Pre-trip gauge check | $0 (driver labor) | Inconsistent enforcement |
| Tire pressure monitoring system (TPMS) | $1,500–$3,000 retrofit | High — alerts in cab |
| Automatic tire inflation system (ATIS) on trailer | $1,200–$1,800 per axle | Highest — maintains pressure on the move |

ATIS is now standard on most new trailers. Retrofit ROI: 12–18 months on a high-utilization trailer.

## Position management

Tires rotate "downward" through positions to maximize mileage:

| Stage | Position | Miles | Action at pull |
|---|---|---|---|
| 1 | New on steer | 100K–150K | Pull at 6/32" → drive position |
| 2 | Run on drive | 100K–200K | Pull at 5/32" → retread for trailer |
| 3 | Retread on trailer | 100K–200K | Scrap or second retread |
| 4 | Second retread | 80K–120K | Scrap |

A quality casing can be retreaded 2–3 times. Total miles per casing across full lifecycle: 400K–700K.

## Retreading economics

Retread cost: ~$200–$300 each (vs $500–$650 new). Per-mile cost of a retreaded tire is 40–50% of a new tire. Industry-wide ~50% of trailer tires are retreads.

Casing yield: 65–80% of pulled casings are retreadable when properly maintained. Casing yield is the single best measure of program quality.

## Vendor / network programs

| Vendor | Strengths | Network |
|---|---|---|
| Bridgestone (Bandag) | Casing program, retread network | 250+ U.S. retread plants |
| Michelin (Oliver) | Premium new tires, low rolling resistance | Premium pricing |
| Continental (ContiLifeCycle) | TPMS integration, fleet portal | Strong in EU + U.S. |
| Goodyear (Goodyear Total Solution) | Roadside network breadth | TVR program for trailer |

Most fleets standardize on one OEM for steer/drive, one OEM for trailer, one retread program — simplifies casing flow and pricing.

## Roadside breakdown prevention

Tire failures account for ~30% of all on-road breakdowns. Drivers of typical fleets:
- 1 in 6 trucks has a tire blowout per year
- Average roadside cost: $450 (mobile service) + 4 hours of downtime
- Annualized cost per truck: $700–$1,200 in tire-related downtime alone

Mitigation:
- TPMS reduces blowout rate ~40%
- Weekly driver inflation check (mandated in driver handbook) reduces ~25%
- Pull-point review every 30 days reduces unscheduled replacements ~30%

## Trailer wheel-end maintenance

Often packaged with tire program. Includes:
- Hub-cap oil seal inspection
- Brake-adjustment check
- Wheel-bearing repack at 100K
- Wheel-end heat sensor (optional)

## Common mistakes

- Mismatched dual tires (one new, one worn) — uneven wear shreds the new tire
- Mounting a retread on a steer position (prohibited 49 CFR 393.75(d))
- Skipping pre-trip inflation check because TPMS is installed (TPMS lags — gauges find slow leaks first)
- No casing-yield tracking — buying new tires every cycle, paying CPM 2× what it should be
- Buying lowest-bid retread without specifying mileage warranty
- Letting drivers buy random brands at truck stops on emergency replacements — mixed brands across same axle is OOS

## Where this fits in X3

X3 captures every tire purchase against the unit ID for CPM rollup, flags missing inflation checks in DVIRs, and surfaces OOS-risk tires from inspection data. The fleet manager dashboard widget shows tire CPM trend, casing yield, and blowout count YoY.

Tire program ROI is measurable — usually within 90 days of standardization, CPM drops noticeably.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=tire-management-program

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

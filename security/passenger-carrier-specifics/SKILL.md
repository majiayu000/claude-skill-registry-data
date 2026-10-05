---
name: passenger-carrier-specifics
description: |
  Use this skill when the user asks about passenger-carrying CMVs — buses, motorcoaches, charter operations, school buses, limousines, shuttle services. Covers different HOS rules (10-hour driving / 15-hour on-duty / no 34-restart), Class C CDL with P endorsement, S endorsement for school bus, FMCSA Hours-of-Service for passenger vehicles, $5M insurance minimum, BMC-32 filing, accessibility requirements, and how passenger ops differ from property. Cite 49 CFR 395.5 + 387.33.
---

# Passenger-Carrying CMV Specifics

Passenger CMV operations (≥ 9 passengers including driver for compensation, or ≥ 16 passengers regardless of compensation, or any school bus) have DIFFERENT rules than property carriers. This skill covers what's different.

## HOS rules for passenger drivers (49 CFR 395.5)

| Limit | Property | Passenger |
|---|---|---|
| Driving limit per shift | 11 hours after 10 hours off | **10 hours after 8 hours off** |
| On-duty limit | 14-hour window | **15-hour limit** |
| Break required | 30-min after 8 hours driving | NO 30-min break required |
| Cumulative limit | 60/7 or 70/8 | 60/7 or 70/8 (same) |
| 34-hour restart | Yes (optional) | **No 34-hour restart** |
| Sleeper berth | 10-hour off-duty allowed via 8/2 or 7/3 split | 8 consecutive hours minimum, may extend with 2 hours off-duty |

The big differences: passenger drivers have LESS driving time per shift but NO mandatory 30-min break, AND there's no 34-hour restart option.

## CDL requirements

**Class C CDL with P endorsement** required for vehicles designed to transport 16+ passengers including driver. Class B CDL with P endorsement may apply for buses below 26,001 lb but at 16+ passenger capacity.

**S endorsement** additionally required for school bus drivers.

Background check via TSA Security Threat Assessment may be required for some passenger operations (similar to hazmat H endorsement).

## Insurance minimums (49 CFR 387.33)

Passenger carriers have higher insurance minimums than property carriers:

| Type | Minimum |
|---|---|
| Passenger ≤ 15 (small bus) | $1.5 million |
| Passenger 16+ (motorcoach) | $5 million |
| Charter / tour operations | $5 million |
| School bus (Federal contracts only) | $5 million (state contracts may differ) |

Filing: **BMC-32** — the passenger-carrier insurance filing form. Filed by your insurance company directly with FMCSA.

## Pre-trip + post-trip inspection (49 CFR 392.7-9)

Same as property but with **passenger-specific** items:

- Emergency exits (windows, doors)
- Fire extinguisher accessibility
- First aid kit (passenger-specific)
- Reflectorized triangles
- Seat belts (if equipped)
- Wheelchair lifts / accessibility equipment
- Heating/cooling systems (passenger comfort)
- Aisle clearance, handrails
- Emergency lighting

## Accessibility (49 USC 12162; Americans with Disabilities Act + DOT ADA)

Passenger carriers operating to the public must:

- Have accessible vehicles or service alternatives
- Train drivers in accessibility procedures
- Maintain wheelchair lifts (if equipped)
- Provide reasonable accommodations
- Comply with state-specific accessibility rules

Smaller fleets (1-2 buses) may have exemptions under transition rules. Charter operations have specific carve-outs.

## Operating authority

Passenger carriers require their own MC number — **MC-Passenger** authority, distinct from property MC.

Common operation types:
- **Class A** — fixed-route operation (regular bus routes)
- **Class B** — charter / tour bus
- **Class C** — special operations
- **Class D** — Para-transit / on-demand

Each has different fleet-size + insurance minima.

## What's the same as property

- USDOT number required
- BOC-3 process agent designation
- UCR (Unified Carrier Registration) annual fee
- IRP for interstate operations 26,001+ lb
- IFTA if operating in 2+ jurisdictions at 26,001+ lb
- Drug & alcohol testing program (49 CFR 382 — same)
- Driver Qualification File (49 CFR 391 — same)
- Vehicle maintenance program (49 CFR 396 — same)

## What's also different beyond HOS

- **Driver age** — interstate passenger drivers must be 21+ (same as property)
- **Hazardous condition reporting** — passenger operations have specific protocols for bomb threats, hijackings, suspicious passengers
- **Random testing rates** — alcohol 10%, drug 50% (same as property as of 2024)
- **Safety performance history** — must inquire to previous employers for last 3 years, same as property

## Common mistakes

1. **Property-carrier HOS applied to passenger operations.** Drivers run 11 hours when they should run 10.
2. **No 34-hour restart available** but driver assumes it is. They miss the cumulative limit.
3. **Insurance filed as property carrier** instead of BMC-32 for passenger. Operating illegally.
4. **CDL endorsements expired.** P endorsement renewal isn't on most fleets' radar.
5. **Sleeper berth math wrong** for passenger drivers (8/2 vs 7/3 splits differ slightly).

## Schools-specific

School bus operations have ADDITIONAL requirements:

- S endorsement on CDL (separate test + background check)
- Specific training on school bus operation
- Special school bus safety zones (state-specific)
- Federal school bus standards (FMVSS 220, 222) for crashworthiness
- "Yellow school bus" markings + flashing lights + stop arm + crossing arm requirements

State school bus departments often have their own oversight + audit programs.

## Quirks worth knowing

- **Operating across the US/Mexico border** — additional clearance required for passenger carriers
- **Operating across the US/Canada border** — Transport Canada equivalents apply
- **Charter to other states** — base state's authority covers operations in destination states
- **Special events** — temporary permit may be needed (e.g., Super Bowl ground transport)

## Where this fits in X3

X3's product is primarily designed for property carriers but can support passenger operations. The HOS rule set in `hos-eld.html` includes a "passenger" mode that swaps in 10-hour / 15-hour limits. Insurance filing tracking in `settings.html` accommodates BMC-32 as well as property variants.

If asked about a specific charter or fixed-route operation, ask follow-ups about:
- Vehicle size (passenger capacity)
- Operation type (charter / fixed-route / school)
- Cross-state vs intrastate
- Insurance carrier


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=passenger-carrier-specifics

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

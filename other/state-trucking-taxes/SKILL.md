---
name: state-trucking-taxes
description: |
  Use this skill when the user asks about state-specific trucking taxes BEYOND IFTA — NY Highway Use Tax (HUT), KY Kentucky Intrastate Tax (KIT), Oregon Weight-Mile Tax, New Mexico Weight-Distance Tax, Connecticut Highway Use Fee, or other state-level road-use taxes for commercial vehicles. Covers thresholds, rates, registration, filing cadence, and how these differ from IFTA. Reference state DOT/DOR resources.
---

# State-Specific Trucking Taxes (Beyond IFTA)

Five US states impose road-use taxes on CMVs that are SEPARATE from IFTA. Carriers operating in or through these states must register + file in addition to their IFTA returns.

## 1. New York Highway Use Tax (HUT)

**Who pays:** Motor vehicles using NY public highways at 18,001+ lb gross weight.

**Registration:** Apply for NY HUT permit + decals via NY DTF. ~$1.50 per truck registration.

**Filing cadence:** Quarterly (Q1 due April 30, Q2 July 31, Q3 Oct 31, Q4 Jan 31).

**How taxed:**
- **Gross Weight Method** — calculated by maximum gross weight of the vehicle + miles driven in NY
- **Unloaded Weight Method** — based on unloaded vehicle weight + miles driven in NY
- Operator picks one method per truck and uses consistently

**Rates (approximate, as of 2026):**
- 18,001-26,000 lb: $0.005 per mile
- 26,001-29,000 lb: $0.008 per mile
- 29,001-32,000 lb: $0.012 per mile
- ... scaling up
- 80,001+ lb: $0.057 per mile

**Records retained:** 4 years.

**Special note:** Bobtail (no trailer attached) operations and certain ag/forestry vehicles may be exempt.

## 2. Kentucky Intrastate Tax (KIT) / KY Weight-Distance Tax

**Who pays:** Motor vehicles using KY highways at 60,001+ lb (KIT). Also a separate **Kentucky Highway Use Tax** for 26,001+ lb.

**Filing cadence:** Quarterly.

**Rates:**
- KIT rate: $0.0285 per mile (one of the highest weight-distance rates)

**Records retained:** 4 years.

## 3. Oregon Weight-Mile Tax

**Who pays:** Vehicles using OR public highways at 26,001+ lb registered gross weight.

**Filing cadence:** Monthly (most carriers) OR quarterly (lower-mile fleets — annual mileage < 100K).

**Registration:** Apply via OR DOT. Permit + temporary trip permit options.

**Rates (approximate):**
- Calculated by combined weight × miles in OR
- Heavy hauler (80,001+ lb): ~$0.16 per mile

**How it's filed:** Submit monthly weight-mile report. Includes:
- Total miles in OR
- Combined weight
- Trip records

**Special quirks:**
- Oregon has NO IFTA participation (Oregon doesn't collect fuel tax at the pump for CMVs; weight-mile is the equivalent)
- Out-of-state carriers pay through trip permits OR full registration
- Configuration changes (e.g., adding pup trailers) require updating the registration

**Records retained:** 3 years (Oregon-specific).

## 4. New Mexico Weight-Distance Tax

**Who pays:** Vehicles using NM highways at 26,001+ lb gross weight.

**Filing cadence:** Quarterly.

**Rates:**
- Variable by weight class
- Typical: $0.01-$0.04 per mile depending on weight

**Registration:** Apply via NM Taxation & Revenue Department.

**Records retained:** 3 years.

## 5. Connecticut Highway Use Fee

**Who pays:** Vehicles ≥ 26,000 lb traveling in CT (newer — enacted 2023).

**Filing cadence:** Monthly.

**Rates:**
- Variable by weight class
- 26,001-28,000 lb: $0.025/mile
- 28,001-30,000 lb: $0.028/mile
- ... scaling up
- 80,001+ lb: $0.175/mile

**Registration:** Apply via CT DRS. Free registration.

## Comparison + summary

| State | Threshold | Filing | Rate range |
|---|---|---|---|
| **NY HUT** | 18,001+ lb | Quarterly | $0.005-$0.057/mi |
| **KY KIT** | 60,001+ lb intrastate | Quarterly | $0.0285/mi |
| **OR Weight-Mile** | 26,001+ lb | Monthly/Quarterly | Up to $0.16/mi |
| **NM Weight-Distance** | 26,001+ lb | Quarterly | $0.01-$0.04/mi |
| **CT Highway Use** | 26,000+ lb | Monthly | $0.025-$0.175/mi |

## Why these are separate from IFTA

IFTA covers **fuel tax** (federal motor fuel tax distributed to states based on miles). These state taxes are **road-use** taxes (paying for road wear caused by heavy vehicles) — a different revenue stream.

Practical implication: a truck operating in NY pays IFTA on fuel consumed there AND HUT on miles driven there. Two separate quarterly filings.

## Records to keep

Across all these state taxes, retain for **at least 3-4 years**:

- Daily trip log per vehicle (date, route, miles per state)
- Beginning + ending odometer per state border crossing
- Fuel purchase receipts
- Tax filings + receipts of payment

Most ELD providers can export per-state mileage reports. Use those.

## Common mistakes

1. **Not registering with the state before operating.** Operating without a permit can result in penalties or temporary bans.
2. **Mixing OR weight-mile filing with IFTA filings.** OR is NOT an IFTA state; separate.
3. **Filing only annually** when state requires quarterly or monthly.
4. **Reporting truck-only miles** when state requires combination weight. Pup trailers + bobtail need to be reported correctly.
5. **Missing the recent CT Highway Use Fee** — it's new (2023) so many out-of-state carriers don't know it exists.

## Where this fits in X3

X3's `ifta.html` page is currently IFTA-focused. State-specific weight-distance taxes are a future v2 feature. For now, X3 customers operating in NY/KY/OR/NM/CT should use the state's own filing portals + maintain mileage records.

If asked about specific state filing portals:
- NY: tax.ny.gov (Highway Use Tax)
- KY: revenue.ky.gov (KIT)
- OR: oregon.gov/odot (Weight-Mile)
- NM: tax.newmexico.gov (Weight-Distance)
- CT: portal.ct.gov/DRS (Highway Use Fee)


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=state-trucking-taxes

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

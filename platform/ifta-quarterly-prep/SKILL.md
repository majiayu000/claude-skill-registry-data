---
name: ifta-quarterly-prep
description: |
  Use this skill when the user asks about International Fuel Tax Agreement (IFTA) compliance — quarterly returns, jurisdiction reporting, fuel + miles reconciliation, IFTA-100/101 forms, base jurisdiction selection, IFTA license + decals, recordkeeping requirements, common IFTA audit findings, or how to handle non-IFTA jurisdictions. Cite IFTA Articles of Agreement.
---

# IFTA Quarterly Returns

IFTA (International Fuel Tax Agreement) is a base-state agreement among the 48 contiguous US states + 10 Canadian provinces. Replaces individual fuel tax reporting per state.

## Who needs IFTA

A motor carrier needs IFTA if:

- Operates in **2+ jurisdictions** (interstate), AND
- The qualified motor vehicle is either:
  - GVWR ≥ 26,001 lb, OR
  - Has 3+ axles regardless of weight, OR
  - Used in combination when combined weight ≥ 26,001 lb

Intrastate-only carriers do NOT need IFTA.

## IFTA license + decals

- Apply through your base jurisdiction (state where vehicles are registered, dispatched, and where records are maintained).
- Receive 1 IFTA license per fleet + 2 decals per vehicle (one for each side of cab).
- License renews annually; decals replaced annually.

## Quarterly return cycle

| Quarter | Reporting Period | Due Date |
|---|---|---|
| Q1 | Jan 1 - Mar 31 | April 30 |
| Q2 | Apr 1 - Jun 30 | July 31 |
| Q3 | Jul 1 - Sep 30 | October 31 |
| Q4 | Oct 1 - Dec 31 | January 31 |

If the due date is a weekend or holiday, the deadline rolls to the next business day.

## What the return contains

For each jurisdiction operated in during the quarter:

- **Miles driven** in that jurisdiction (total + taxable)
- **Gallons of fuel purchased** in that jurisdiction
- **Calculated tax owed or credit** (compute fuel consumed in jurisdiction × jurisdiction's tax rate, then subtract tax already paid at the pump in that jurisdiction)

Net is summed across all jurisdictions: positive = remit to base state; negative = refund/credit.

## The math (per jurisdiction)

```
Total Miles in JX  =  raw odometer or GPS data per jurisdiction
Total Gallons      =  fleet-wide gallons consumed in the quarter
Fuel Used in JX    =  (Total Miles in JX) / (fleet MPG)
Tax Liability      =  (Fuel Used in JX) × (JX's tax rate)
Tax Paid at Pump   =  fuel receipts purchased in JX × that JX's rate
Net for JX         =  Tax Liability − Tax Paid
```

Sum across all jurisdictions. Pay base state OR claim refund.

## Recordkeeping (4-year retention)

- **Daily distance records** by jurisdiction (typically from IVMR — Individual Vehicle Mileage Reports — or ELD/GPS data)
- **Fuel purchase receipts** with date, jurisdiction, gallons, $ amount, vehicle ID
- **Trip records** showing routes + jurisdictions traversed
- **MPG calculation** (total gallons / total miles)

Records retained for **4 years** from the return due date.

## Sources of distance data

- **IVMR** — paper or electronic; per vehicle per trip
- **ELD GPS** — most modern fleets pull jurisdiction data from the ELD
- **Trip recorder / GPS device** — third-party telematics

## Common IFTA audit findings

1. **Distance per jurisdiction can't be verified.** No supporting records.
2. **Fuel receipts don't tie to vehicle.** A pile of fleet card statements without per-vehicle attribution.
3. **MPG is unreasonable.** If reported MPG is 12+ for an OTR fleet, auditor suspects manipulation.
4. **Non-IFTA mileage included.** Operating in Alaska, Hawaii, DC, Mexico, Yukon, or NWT — these are non-IFTA jurisdictions; miles must be tracked but not taxed under IFTA.
5. **Returns not filed for "no operation" quarters.** Even if zero miles, you must file a "no operation" return.

## Where this fits in X3

X3's `ifta.html` page imports ELD data, computes per-jurisdiction miles + fuel, and generates a draft IFTA-100/101 return. `agent-ifta-quarterly-reminder` fires 30 days before due date.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=ifta-quarterly-prep

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

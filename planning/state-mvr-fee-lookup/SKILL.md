---
name: state-mvr-fee-lookup
description: |
  Use this skill when the user asks the cost of pulling a Motor Vehicle Record (MVR) in a specific state, or wants to compare MVR fees across multiple states, or is budgeting annual compliance costs for a multi-state fleet. Reference the canonical fee table below; flag that fees change (re-verify with state DMV before annual budget planning).
---

# State MVR Fee Lookup

State DMVs charge for MVR pulls. Fees vary widely. This is a reference table for budgeting annual driver compliance costs at the federally-required minimum (one MVR per driver per state per year — 49 CFR 391.25).

## Fee table (as of 2026)

| State | 3-year MVR | 5/7/10-year MVR | Notes |
|---|---|---|---|
| Alabama | $5.50 | $8.50 | |
| Alaska | $10.00 | $10.00 | |
| Arizona | $5.00 | $5.00 | |
| Arkansas | $8.50 | $8.50 | |
| California | $2.00 | $5.00 | Driver consent + reason required |
| Colorado | $9.08 | $9.08 | |
| Connecticut | $20.00 | $20.00 | Premium fee |
| Delaware | $25.00 | $25.00 | One of the highest |
| Florida | $8.00 | $8.00 | |
| Georgia | $6.00 | $8.00 | |
| Hawaii | $23.00 | $23.00 | |
| Idaho | $9.00 | $9.00 | |
| Illinois | $20.00 | $20.00 | |
| Indiana | $12.00 | $12.00 | |
| Iowa | $5.50 | $5.50 | |
| Kansas | $7.00 | $7.00 | |
| Kentucky | $3.00 | $3.00 | |
| Louisiana | $18.00 | $18.00 | |
| Maine | $7.00 | $12.00 | |
| Maryland | $15.00 | $15.00 | |
| Massachusetts | $20.00 | $20.00 | |
| Michigan | $8.00 | $8.00 | |
| Minnesota | $9.00 | $9.00 | |
| Mississippi | $14.00 | $14.00 | |
| **Missouri** | **$0.12** | **$0.12** | **Cheapest in the US** |
| Montana | $7.16 | $7.16 | |
| Nebraska | $4.50 | $4.50 | |
| Nevada | $7.00 | $7.00 | |
| New Hampshire | $15.00 | $15.00 | |
| New Jersey | $15.00 | $15.00 | |
| New Mexico | $5.00 | $7.00 | |
| New York | $7.00 | $10.00 | |
| North Carolina | $11.00 | $11.00 | |
| North Dakota | $3.00 | $3.00 | |
| Ohio | $5.00 | $5.00 | |
| **Oklahoma** | **$25.00** | **$27.50** | **Highest in the US tied with DE** |
| Oregon | $2.00 | $4.00 | |
| Pennsylvania | $12.50 | $12.50 | |
| Rhode Island | $20.00 | $20.00 | |
| South Carolina | $6.00 | $6.00 | |
| South Dakota | $4.00 | $4.00 | |
| Tennessee | $5.50 | $7.00 | |
| Texas | $6.50 | $8.00 | |
| Utah | $7.50 | $7.50 | |
| Vermont | $20.00 | $20.00 | |
| Virginia | $8.00 | $8.00 | |
| Washington | $13.00 | $13.00 | |
| West Virginia | $11.00 | $11.00 | |
| Wisconsin | $8.00 | $8.00 | |
| Wyoming | $5.00 | $5.00 | |

**Note:** These are state DMV fees only. Vendor markups (Checkr, SambaSafety, Foley, etc.) typically add $5-15 per MVR for processing, identity verification, and continuous-monitoring service.

## CDLIS supplementary fee

A CDLIS pull (national CDL Information System, separate from any single state's MVR) is typically **$1-3** depending on the vendor. Useful for cross-state convictions that haven't synced to the home-state record yet.

## Fleet-cost calculator example

50-driver fleet, all single-state Texas drivers:
- 50 × $6.50 = $325/year minimum (state fees)
- Plus vendor markup: 50 × $12 = $600/year (Checkr or similar)
- **Total: ~$925/year**

50-driver fleet, mixed multi-state (10 in OK, 10 in IL, 10 in TX, 10 in CA, 10 in MO):
- 10 × $25.00 (OK) = $250
- 10 × $20.00 (IL) = $200
- 10 × $6.50 (TX) = $65
- 10 × $2.00 (CA) = $20
- 10 × $0.12 (MO) = $1.20
- **Total state fees: ~$536**
- Plus vendor markup ~$600
- **Total: ~$1,136/year**

## Continuous monitoring vs annual pulls

- **Annual pull only:** state fee per driver per year (above)
- **Continuous monitoring:** typically $3-15/driver/month subscription + state fees for any "events" detected
  - Annual cost for 50 drivers: ~$1,800-9,000/year just for monitoring
  - But catches mid-year violations + insurance discounts often offset

Most carriers run BOTH: annual pull for DQF + continuous monitoring for risk management.

## When this skill fires

If the user is:
- Budgeting compliance costs for next year
- Comparing vendor options (Checkr vs SambaSafety etc.)
- Wondering why an MVR pull cost so much
- Building a multi-state expansion model

Look up the relevant state's fee from the table. If the user is in a state not listed, recommend they call the state DMV directly — fees change annually.

## Where this fits in X3

X3 hard-codes the state MVR fee table in `_shared/twilio.ts getMvrStateFeeCents()` (now extended to all states). This feeds the `passthrough_cost_cents` field on `vendor_orders` so customers see the true cost of an MVR.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=state-mvr-fee-lookup

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

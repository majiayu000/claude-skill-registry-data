---
name: ifta-fuel-tax-return-filing
description: |
  Use this skill to file your IFTA quarterly fuel tax return. Covers filing windows, calculation, payment, and refund situations.
---

# IFTA Quarterly Return Filing

IFTA quarterly returns are due 30 days after the end of each quarter. Q1 due April 30, Q2 due July 31, Q3 due October 31, Q4 due January 31 of following year.

## Quarterly cycle
- **Q1** (Jan-Mar) — due April 30
- **Q2** (Apr-Jun) — due July 31
- **Q3** (Jul-Sep) — due October 31
- **Q4** (Oct-Dec) — due January 31 of next year

## What's in the return
- Total miles driven during the quarter
- State-by-state miles
- Total fuel purchased
- State-by-state fuel purchases
- Calculation of taxes owed/refund per state
- Net tax due or refund

## Calculation per state
For each state:
- (Miles driven in state ÷ Total miles) × Total fuel purchased = "Fuel allocated to state"
- Fuel allocated × State tax rate = Tax obligation
- Less: Fuel purchased in state (already paid tax)
- Net = Refund (if you bought more than you used) or Tax due (if you bought less than you used)

## Total tax due
- Sum of state-by-state tax obligations
- Plus state administrative fees (varies)
- Paid to base state; base state distributes to other states

## Refunds
- If you bought more fuel in some states than miles driven (uncommon)
- Some states delay refund until annual reconciliation
- Some carriers prefer to leave credit on file rather than refund

## Late filing consequences
- $50 penalty + 1% per month interest (typical)
- Some states impose harsher penalties for repeated late filing
- May trigger audit selection
- May trigger registration suspension (rare)

## Common errors
- Miles not added across quarters (Q1 + Q2 should equal H1 total)
- Fuel receipts duplicated
- State allocations wrong (rounding errors)
- Fuel taxes not paid in state where purchased

## Compass IFTA module
- Auto-generates quarterly IFTA returns from fuel + miles data
- Pre-fills the base state's IFTA form (electronic submission)
- Calculates refunds vs taxes due
- Quarterly review report shows variances + adjustments before submission

## CFR citations
- **IFTA Procedures Manual**

## How Compass surfaces this
Searchable in Compass Ask. Runs against carrier fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=ifta-fuel-tax-return-filing

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

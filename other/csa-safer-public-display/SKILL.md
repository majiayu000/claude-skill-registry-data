---
name: csa-safer-public-display
description: |
  Use this skill to understand what CSA data the public sees about your carrier and how that affects business. Covers SAFER, accessibility, and what's hidden vs visible.
---

# SAFER Public CSA Score Display

FMCSA SAFER (Safety and Fitness Electronic Records) is the public-facing system for carrier safety data. Customers, brokers, insurance companies, and the public can search your carrier.

## What's public
- Carrier name + DOT number + MC number
- Carrier address + contact info
- Operating authority
- Insurance status (active/lapsed)
- Last inspection details
- BASIC percentile scores (when above intervention threshold)
- Crash count (24-month)
- Out-of-service rate

## What's NOT public
- BASIC scores BELOW intervention threshold (you have to be in alert range)
- Specific violation details (only aggregated)
- Individual driver records
- Financial information

## How customers use it
- Brokers verify carrier insurance + authority before tendering loads
- Customers (shippers, receivers) check operating status
- Insurance carriers use for underwriting
- Other carriers check before lease/contract

## Impact on business
- Public BASIC alerts may reduce shipper willingness to use you
- Operating authority issues can shut down business
- Recent crash history affects insurance quotes

## How to monitor
- Check SAFER monthly (fmcsa.dot.gov)
- Confirm your data is current (carrier address, insurance, operating authority)
- Flag any incorrect information for correction (DataQ for inspection issues; carrier MCS-150 update for company data)

## What to do if you have alert BASICs
- Address underlying causes (CSA-driving training, dispatch changes)
- Reverse via DataQ where possible (contestable violations)
- Be transparent with customers (proactively communicate improvement plan)
- Consider carrier-level interventions (compliance review may help)

## Compass display
Compass CSA module:
- Mirrors your SAFER public profile
- Shows BASIC scores with alert/clean indicators
- Provides historical 24-month trend
- Identifies actions to reduce alert BASICs

## CFR citations
- **49 CFR § 385.4**
- **FMCSA SAFER public website**

## How Compass surfaces this
Searchable in Compass Ask. Runs against the carrier's actual fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=csa-safer-public-display

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

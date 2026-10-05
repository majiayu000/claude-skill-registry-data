---
name: csa-peer-group-reassignment
description: |
  Use this skill when a carrier's CSA peer group changes. Covers what triggers reassignment, how percentile changes affect alert status, and how to interpret the shift.
---

# CSA Peer Group Reassignment

Peer groups are reassigned quarterly. A reassignment can move a carrier in or out of alert status — even with no behavioral change.

## How peer groups are determined
- Number of power units
- Average inspection volume (3-year average)
- Time in operation
- Carrier type (general / hazmat / passenger)

## Reassignment triggers
- Acquired carrier(s) increase power-unit count
- Reduced fleet size
- New entrant status concluded
- Changed authority (interstate to intrastate, etc.)
- Audit changing carrier type classification

## Impact on percentile
- Moving from smaller peer group → larger one typically reduces percentile volatility
- Moving from larger → smaller can cause score swings
- New peer group may have different distribution = different alert risk

## What to watch
- Quarterly reassignment notice from FMCSA
- Your peer group ID changes
- Your percentile vs your prior peer group

## When reassignment helps
- Smaller carrier acquired by larger fleet — joins larger peer group with calmer scores
- Carrier reduces fleet but stays in same peer tier — score may improve relative to larger peers

## When reassignment hurts
- Carrier grows out of "new entrant" peer group
- Carrier moves to higher inspection-volume tier
- Carrier becomes hazmat from general freight (suddenly subject to 60th threshold)

## Compass monitoring
- Tracks your peer group changes quarterly
- Alerts when reassignment causes percentile to cross threshold
- Provides historical context

## CFR citations
- **FMCSA SMS Methodology**
- **49 CFR § 385.4**

## How Compass surfaces this
Searchable in Compass Ask. Runs against the carrier's actual fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=csa-peer-group-reassignment

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

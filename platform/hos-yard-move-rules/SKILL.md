---
name: hos-yard-move-rules
description: |
  Use this skill when a driver needs to move a CMV within a yard, terminal, or property under § 395.8 yard-move provisions. Covers what counts as yard move, ELD configuration, and where yard move ends and on-duty driving begins.
---

# HOS Yard Move Exemption Boundaries

Yard move is a duty status used when a driver moves a CMV on private property (yard, terminal, customer site) without being on a public road. ELD-equipped drivers can flag yard-move to keep the time off the 11-hour drive limit (still counts as on-duty).

## What qualifies
- Movement entirely within the bounds of a single property (yard, lot, terminal)
- The vehicle does NOT enter a public roadway
- The driver remains on-duty (not off-duty)

## What does NOT qualify
- Crossing a public road between two parts of a yard — that's on-duty driving
- Moving to a public-side fuel island — public roadway use
- Long-distance "yard moves" across multiple addresses

## ELD configuration
Yard-move status must be enabled by the carrier in the ELD device settings. The driver selects "yard move" before moving. Some ELDs auto-revert to "driving" if speed exceeds 20 mph (configurable).

## Common audit findings
- Driver used yard-move on a public road (defeats the protection — violation)
- Yard-move time > 1 hour on a single move (suspicious; inspectors will ask for the GPS track)
- Yard-move logged during the 30-minute break period (rule allows it; some drivers use this — defensible)

## CFR citations
- **49 CFR § 395.8(a)(2)**
- **FMCSA Regulatory Guidance to § 395.8 (yard move)**

## How Compass surfaces this
This skill is searchable in the Compass Ask interface and runs against the carrier's actual fleet data when invoked from within the relevant tracker. It is read-only — no actions are taken without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=hos-yard-move-rules

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

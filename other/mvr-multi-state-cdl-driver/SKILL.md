---
name: mvr-multi-state-cdl-driver
description: |
  Use this skill when a driver holds CDLs in multiple states or has resided in multiple states. Covers what MVRs to pull, federal recordkeeping requirements, and state-specific issues.
---

# MVR for Multi-State CDL Drivers

Per § 391.23(a)(1), a carrier must inquire to every state where the driver was licensed to drive in the past 3 years. The driver's primary CDL state holds the most current record.

## Required MVR pulls
- **State of current CDL issuance** — annual review per § 391.25
- **Every state where driver was licensed in past 3 years** — pre-employment + within DQF

## Multi-state scenario
A driver who lived/worked in 3 states in past 3 years:
- Pull MVR from each state at pre-employment
- Annual review uses current state of CDL issuance
- Driver self-certification at the state level resolves which state is "current"

## States with continuous MVR monitoring services
- All US states allow individual MVR pulls
- Continuous monitoring services (SambaSafety, Foley, Driver iQ) cover all states
- Pricing varies by state (some states charge $3, others $25)

## Driver moving between states
Driver moves from TX to CA:
1. Driver surrenders TX CDL
2. Driver applies for CA CDL (typically 30-day transfer)
3. Carrier should pull both TX and CA MVRs for the transition period
4. Driver self-certifies in CA
5. After CA CDL issued, annual review uses CA MVR

## What to look for across states
- Suspensions or revocations in any state
- Reciprocal-state convictions
- Habitual offender designations in any state
- DUI/DWI history (states differ on retention periods)

## Compass automation
Compass MVR module:
- Tracks driver's CDL state(s)
- Auto-pulls MVR from primary state annually
- Alerts on state changes (via SambaSafety or carrier upload)
- Flags multi-state inconsistencies

## CFR citations
- **49 CFR § 391.23(a)(1)**
- **49 CFR § 391.25**

## How Compass surfaces this
This skill is searchable in Compass Ask and runs against the carrier's actual fleet data when invoked from the relevant tracker. Read-only; no actions taken without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=mvr-multi-state-cdl-driver

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

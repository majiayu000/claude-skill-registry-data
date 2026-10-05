---
name: mvr-disqualifying-offenses
description: |
  Use this skill to understand which MVR violations disqualify a driver under federal rules. Covers § 391.15 disqualifications, varying state rules, and CSA impact.
---

# MVR Disqualifying Offenses

Per § 391.15, certain offenses disqualify a person from driving a CMV in interstate commerce. These are federal — state DQ rules may be stricter.

## Federally disqualifying offenses
- **DUI/DWI**: 1-year minimum disqualification (3-year for hazmat)
- **DUI involving fatality**: lifetime disqualification (10-year minimum)
- **Felony involving CMV**: 1-year minimum
- **Two serious traffic offenses in 3 years**: 60-day disqualification
- **Three serious traffic offenses in 3 years**: 120-day disqualification
- **Leaving the scene of an accident involving a CMV**: 1-year minimum
- **Drug-related offense**: 1-year minimum (lifetime if second)

## What's a "serious traffic offense"
- Excessive speeding (15+ mph over)
- Reckless driving
- Improper lane change
- Following too closely
- Drug-related offense (any)
- Driving CMV without CDL
- Driving CMV with suspended/revoked CDL
- Causing injury or death in a CMV-related incident

## Disqualification triggers (cumulative)
- Two serious in 3 years → 60-day DQ
- Three serious in 3 years → 120-day DQ
- This is per the driver — runs across all employers

## Reinstatement
- After DQ period, driver may apply to reinstate CDL
- Some states require road test or written exam
- Driver must self-certify the disqualification ended

## What carriers must do
- Check MVR for disqualifying convictions at pre-employment
- Annual review of MVR for new convictions
- Investigate driver's prior 3-year history for cumulative offenses
- Disqualified driver cannot operate CMV during DQ period

## Compass tracking
Compass MVR module:
- Pulls historical convictions from state MVR
- Flags any disqualifying offense within DQ period
- Calculates cumulative serious-offense count
- Alerts on new convictions if continuous monitoring is enabled
- Generates required reporting documentation

## Common pitfall
Driver moves between states; convictions in former state are not automatically transferred. Federal Motor Carrier Safety Administration maintains the federal record (CDLIS — Commercial Driver License Information System), which is what continuous monitoring services query.

## CFR citations
- **49 CFR § 391.15**
- **49 CFR § 383.51**

## How Compass surfaces this
This skill is searchable in Compass Ask and runs against the carrier's actual fleet data when invoked from the relevant tracker. Read-only; no actions taken without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=mvr-disqualifying-offenses

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

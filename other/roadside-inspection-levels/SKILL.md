---
name: roadside-inspection-levels
description: |
  Use this skill when the user asks about CMV roadside inspection levels (Level I through Level VIII), what each level inspects, average inspection times, CVSA decal eligibility, what triggers a level upgrade, and how to coach drivers through a roadside inspection. Reference CVSA North American Standard Inspection Program.
---

# Roadside Inspection Levels — CVSA North American Standard

The Commercial Vehicle Safety Alliance (CVSA) standardizes inspection levels across the US, Canada, and Mexico. Drivers see Levels I-VIII at weigh stations + roadside checks.

## The 8 levels

| Level | What it covers | Avg time | CVSA decal? |
|---|---|---|---|
| **I — North American Standard** | Driver + vehicle. Most comprehensive. | 45-90 min | Yes, if pass |
| **II — Walk-Around Driver/Vehicle** | Driver + visible vehicle items (no under-vehicle) | 20-40 min | No |
| **III — Driver/Credential/Administrative** | Driver-only: docs, HOS, ELD, license | 15-30 min | No |
| **IV — Special Study** | Single-item targeted (e.g., tires only, brakes only) | Varies | No |
| **V — Vehicle-Only (no driver present)** | Terminal-yard inspection without driver | 30-60 min | Yes, if pass |
| **VI — Enhanced NAS Radioactive Materials** | Required for highway-route-controlled radioactive | 60-120 min | Yes |
| **VII — Jurisdiction-Mandated Commercial Vehicle** | State-specific (e.g., school bus annual) | Varies | No |
| **VIII — North American Standard Electronic Inspection** | NEW — automated electronic check via roadside cameras + telematics. No driver-officer contact. | 1-5 min | Limited |

## Level I — The big one

Includes everything in Levels II and III plus an **under-vehicle inspection**. The inspector physically gets under the truck to check:

- Frame condition
- Suspension components
- Air brake plumbing
- Drive train
- Underside cargo securement

Driver portion (Level III) covers:
- CDL + medical cert
- HOS / ELD records (current day + previous 7 days)
- Drug & alcohol test compliance (Clearinghouse status)
- Shipping papers (if hazmat)
- Seatbelt usage
- Vehicle registration / IRP / IFTA / UCR

Vehicle portion covers:
- Brakes (push-rod stroke, slack adjusters, drum + lining condition)
- Tires (tread depth, sidewall, inflation)
- Wheels (rims, fasteners)
- Lights + reflectors
- Steering + linkage
- Coupling devices
- Exhaust
- Frame + body
- Cargo securement
- Fuel system

If everything passes, the inspector applies a **CVSA decal** (valid for 90 days). A CVSA-decaled vehicle is less likely to be re-inspected within the 90-day window.

## Level II — Walk-around

Like Level I but inspector doesn't go under the vehicle. So you might miss:
- Frame cracks (only visible under)
- Suspension defects
- Brake plumbing leaks (often only visible under)

Otherwise covers driver + walk-around vehicle.

## Level III — Driver-only

The driver-focused inspection. Inspector reviews:
- All driver paperwork (CDL, med cert, HOS records)
- ELD data transfer
- Drug & alcohol Clearinghouse status (looked up real-time)
- Whether the driver matches their documents
- HOS logs for current day + last 7 days

No vehicle inspection at Level III. Driver violations only.

## Level IV — Special study

Targeted at a specific item. Examples:
- Brake-only inspection during a state's "Brake Safety Week"
- Tire inspection during winter safety initiative
- Speed limiter inspection
- Auxiliary fuel tank inspection

Usually triggered by enforcement initiatives or a previously-observed defect.

## Level V — Vehicle-only

Performed at a terminal yard WITHOUT the driver. Inspector checks everything Level I covers except the driver portion. Often happens during fleet audits at the carrier's yard.

If the vehicle passes Level V, it gets a CVSA decal even though no driver is there.

## Level VI — Radioactive materials

Required for any CMV transporting **highway-route-controlled quantities** of radioactive materials. Very thorough; can take 2+ hours. Special escort + route restrictions often apply.

## Level VII — State-mandated

Specific to a state's regulatory framework. Examples:
- California's BIT (Basic Inspection of Terminals)
- New York's School Bus Annual Inspection
- State-specific hazmat inspections

## Level VIII — Electronic (new since 2018)

A relatively new level. The CMV's electronic systems (ELD + telematics + transponder) communicate with roadside electronic scanners. The inspector verifies HOS + credentials + Clearinghouse status without physically stopping the vehicle.

If the electronic profile is clean, the truck rolls through without delay. If flagged, may be diverted for Level III or higher.

## What triggers a level upgrade

A roadside encounter that starts as Level III can escalate to Level I if:
- Inspector observes a visible vehicle defect
- HOS log shows a violation requiring vehicle examination
- Driver acts suspicious or evasive
- Truck appears to have been recently in an accident

## Inspector discretion

Inspectors have significant discretion. They can:
- Inspect any vehicle at any time
- Upgrade an inspection level mid-process
- Place the driver/vehicle OOS for any qualifying defect
- Issue citations for findings

## Driver coaching for roadside

When a driver gets pulled in:

1. **Be polite + cooperative.** Hostility prolongs the inspection.
2. **Have documents organized + accessible.** Don't scramble.
3. **Don't volunteer information.** Answer what's asked.
4. **Don't sign anything you don't understand.** Citations can be challenged.
5. **Document the inspection.** Note officer name, badge, inspection level, findings.
6. **Photograph the violation if you disagree** (for DataQ dispute).
7. **Don't argue with the OOS decision** at roadside. File a DataQ dispute after.

## Where this fits in X3

X3's `inspections.html` records each roadside inspection encountered by the fleet. The CVSA decal expiry is tracked per vehicle. Roadside violation patterns feed into the CSA scoring (`csa-scores.html`). Any violation can be the subject of a DataQ dispute (see the dataq-disputes skill).


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=roadside-inspection-levels

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

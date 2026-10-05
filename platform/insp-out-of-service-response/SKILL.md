---
name: insp-out-of-service-response
description: |
  Use this skill when a driver receives an out-of-service (OOS) violation. Covers the immediate compliance, paperwork retention, and CSA impact.
---

# Out-of-Service Violation Response

An out-of-service (OOS) violation means the vehicle or driver cannot continue operating until the issue is corrected. Specific rules apply per § 396.9(c).

## Driver OOS triggers
- HOS violation: 14-hour limit exceeded, 11-hour limit exceeded, no 10-hour rest
- License issues: suspended, expired, wrong class
- Medical: expired certificate
- Substance abuse: failed test, refusal
- Driving without ELD when required

## Vehicle OOS triggers
- Brake adjustment: out of tolerance
- Steering: dangerous play or wear
- Tires: ply separation, broken cords, tread depth below limit
- Lighting: critical lights out
- Coupling devices: missing/damaged
- Hazmat-related: missing placards, leaks, etc.

## What happens when OOS
1. Inspector writes OOS violation
2. Driver/vehicle stops operating
3. Driver receives OOS sticker (driver-OOS) or vehicle OOS sticker (vehicle-OOS)
4. Driver waits for correction (8 hours min for HOS-OOS; equipment-OOS requires repair confirmation)

## Carrier obligations
- Communicate with driver immediately
- Coordinate repair/correction
- Document the OOS event in carrier records
- Driver's DQF and inspection records updated
- Carrier reviews root cause + corrective action

## How OOS affects CSA
- All OOS violations heavily weighted in BASICs (typically 2-3× regular violation weight)
- OOS rate is tracked separately and visible in SAFER
- Pattern of OOS violations may trigger Compliance Review

## DataQ for OOS
OOS violations can be challenged if:
- Officer error documented (e.g., brake test result was within tolerance)
- Driver wasn't actually driving the vehicle
- Vehicle was already in repair status when inspected

## Compass response workflow
- Driver OOS alert via Compass HOS module immediately when ELD detects
- Vehicle OOS triggers maintenance workflow
- Compass Inspections module logs the OOS event + CSA impact
- DataQ assessment if grounds exist for challenge

## CFR citations
- **49 CFR § 396.9(c)**
- **49 CFR § 396.11**

## How Compass surfaces this
Searchable in Compass Ask. Runs against carrier fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=insp-out-of-service-response

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

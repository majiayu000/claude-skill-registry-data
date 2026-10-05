---
name: vehicle-inspection-dvir
description: |
  Use this skill when the user asks about CMV vehicle inspections under 49 CFR 396 — DVIRs (Driver Vehicle Inspection Reports), pre-trip inspections, post-trip inspections, periodic inspections, annual inspections, who can perform inspections, OOS criteria, and what makes a "no defect" DVIR valid. Cite 49 CFR 396.
---

# Vehicle Inspections & DVIRs — 49 CFR 396

## DVIR — Driver Vehicle Inspection Report (49 CFR 396.11)

**Post-trip DVIR:** A driver must prepare a written report at the completion of each day's work on each vehicle operated. The report must cover at least the following parts:

- Service brakes (including trailer brake connections)
- Parking brake
- Steering mechanism
- Lighting devices and reflectors
- Tires
- Horn
- Windshield wipers
- Rear vision mirrors
- Coupling devices
- Wheels and rims
- Emergency equipment

The DVIR must:
- Identify the vehicle (unit number, plate number)
- Identify the driver
- Identify defects or list "no defects"
- Be signed by the driver

**Pre-trip inspection (49 CFR 396.13)** — Before operating a vehicle:

- Driver must be satisfied the vehicle is in safe operating condition
- Review the last DVIR (if any) and certify that defects have been repaired or that repair is not needed
- Sign the previous DVIR (acknowledging the certification)

## DVIR with vs without defects

- **No defects:** Driver simply prepares the report listing parts inspected and marks "no defects." Most carriers no longer require physical retention of no-defect DVIRs (since the 2014 rule change — see 49 CFR 396.11(a)(1)). Carrier must retain at least one cycle for audit.
- **Defects found:** DVIR must be retained for **3 months** from the date of preparation. Carrier must:
  1. Repair the defect(s).
  2. Have a mechanic certify the repair on the DVIR.
  3. The next driver pre-trips and certifies that defects were repaired (or that repair isn't necessary).

## Periodic / Annual Inspection (49 CFR 396.17)

Each vehicle must undergo an **annual inspection** by a qualified inspector (mechanic or shop). The inspection covers:

- Brakes (service + parking)
- Coupling devices
- Exhaust system
- Frame
- Fuel system
- Lighting devices
- Cargo securement
- Steering mechanism
- Suspension
- Tires and wheels
- Windshield glazing and wipers
- Emergency equipment
- And more (see 49 CFR 396 Appendix G — "Minimum Periodic Inspection Standards")

The inspection report must be:
- Maintained in the vehicle (a copy) AND
- Kept at the principal place of business for 14 months from the inspection date

**Substitute:** A state-equivalent inspection (e.g., commercial state safety inspection from a state that has one) can substitute for the federal periodic inspection. Verify with FMCSA list.

## Who can perform a periodic inspection? (49 CFR 396.19)

A qualified inspector — at minimum:

1. 1 year of training/experience as a mechanic OR
2. 1 year of training in a vocational school, college, or similar OR
3. Has performed roadside CMV inspections under MCSAP for 1+ year

Carrier maintains documentation of inspector qualification (resume, training certificate).

## Roadside inspection vs DVIR vs annual inspection

| Type | Performed by | Frequency | Document |
|---|---|---|---|
| Pre-trip | Driver | Each shift | None required; verbal certification |
| Post-trip / DVIR | Driver | End of each shift | DVIR form |
| Annual / Periodic | Qualified inspector | Once every 12 months | Annual inspection sticker + report |
| Roadside | DOT inspector | Random / triggered | DOT-1A or similar |

## Out-of-Service (OOS) criteria

A vehicle can be placed OOS at roadside if defects meet the **CVSA OOS criteria**. Examples (not exhaustive):

- Brake friction material < 1/8" thickness
- Brake stroke beyond adjustment limits
- Brake hose chafed to inner ply
- Front tire tread depth < 4/32"
- Rear tire tread depth < 2/32"
- Defective steering linkage
- Inoperative low air pressure warning device
- Cracked frame member
- Inoperative service brakes (> 20% defective)
- Cargo securement deficiencies (failed straps, missing tiedowns)

A driver placed OOS may NOT operate the vehicle. The vehicle must be repaired (or towed to repair facility) before continuing.

**Driver OOS** can happen too — for HOS violations, drug/alcohol, CDL issues, etc.

## DVIR fraud / falsification

The penalty for a DVIR falsification is potentially:
- $1,150 per violation (carrier or driver)
- Disqualification of driver (for repeat falsification)
- CSA points to the carrier

DVIRs are a high-priority audit target because they're a primary source of vehicle-related BSI in the Vehicle Maintenance BASIC.

## Brake-system "post-trip" exception

A driver who operates a CMV equipped with anti-lock brake systems (ABS) and full air brakes still must perform a post-trip inspection. The fact that a vehicle has ABS does not exempt anyone from the inspection requirement.

## Quick math

A fleet of 10 power units running annual inspections at $80-150 each:
- Cost: $800-1,500/year just for paid inspectors
- Plus internal mechanic time for periodic checks

DVIRs are free (driver time only) but must be tracked + retained.

## Where this fits in X3

X3's `vehicles.html` page tracks per-vehicle DVIR history, annual inspection due dates, and roadside inspection reports. `send-compliance-notification` fires `vehicle_pm_overdue` when a periodic inspection deadline lapses. Driver-uploaded DVIRs feed into the Vehicle Maintenance BASIC score.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=vehicle-inspection-dvir

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

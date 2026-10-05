---
name: vehicle-maintenance-records
description: |
  Use this skill when the user asks about CMV maintenance program requirements under 49 CFR 396.3 — what records must be kept, retention periods (12-18 months on vehicle file + 1 year after disposal), what counts as systematic inspection/repair/maintenance, preventive maintenance scheduling, brake adjustment records, and what auditors look for in vehicle files. Cite 49 CFR 396.3 + 396.21.
---

# Vehicle Maintenance Records — 49 CFR 396.3 + 396.21

Every motor carrier must "systematically inspect, repair, and maintain" every CMV under its control. The carrier (not the driver) is responsible.

## Records the carrier MUST maintain (49 CFR 396.3(b))

For every vehicle under your control for 30+ consecutive days:

1. **Identification** — make, model, year, owner (if not the carrier), VIN, tire size
2. **Servicing schedule** — a means to indicate the nature + due date of various inspection / maintenance operations
3. **Inspection / repair / maintenance records** — date, nature of inspection performed, who performed it (or company name)
4. **Tests of pushrod travel** — for any vehicle with manual brake adjusters (49 CFR 396.25)
5. **Lubrication records**

Retention: **at minimum 12 months on the vehicle's file** + **6 months after a vehicle is sold / leased / otherwise disposed of**.

## What counts as a "systematic" program

A "systematic" program means written, scheduled, and consistent. Auditors look for:

- A written PM (preventive maintenance) schedule by vehicle / mileage / time
- Documented PM completion (work orders, invoices)
- Defect-discovery → repair → mechanic certification chain (matches the DVIR workflow)
- Records of each individual vehicle, not just fleet-wide notes

## Periodic / annual inspection (49 CFR 396.17) — separate

Every vehicle gets an annual inspection by a qualified inspector (covered in the `vehicle-inspection-dvir` skill). The annual inspection report goes in the vehicle file too — retention 14 months at principal place of business.

## What goes in a vehicle file (recommended layout)

```
Vehicle file (paper or digital, one per unit):
  ├── Title / registration / IRP cab card
  ├── VIN, plate, year/make/model record
  ├── Annual inspection certificates (last 14+ months)
  ├── PM schedule + completion records (12+ months)
  ├── DVIRs with defects (last 3 months minimum)
  ├── Repair invoices / work orders + mechanic certifications
  ├── Roadside inspection reports
  ├── Brake adjustment records (manual brake systems only)
  ├── Tire records (rotation, replacement)
  └── Insurance card / proof of coverage
```

## Brake adjustment limit (49 CFR 396.25)

Vehicles with manual brake adjusters must have brake stroke checked periodically. Maximum allowable stroke varies by chamber size. CVSA OOS at roadside if more than 20% of brakes are out of adjustment.

Auto-slack adjusters generally don't need periodic adjustment but DO need replacement if found defective.

## Common audit findings

1. **No written PM schedule.** Auditor asks "show me your PM program" and gets a verbal "we change oil every 25,000 miles."
2. **DVIRs with defects, no repair certification.** The driver wrote up a defect; no repair record follows.
3. **Annual inspection sticker on vehicle but no report in file.** The sticker alone isn't enough; auditor wants the actual report.
4. **Records destroyed too soon.** 12-month retention on the vehicle file isn't suggestion; it's required.
5. **Vehicles operated past expired annual inspection.** Day after the 12-month anniversary = unqualified vehicle.

## Where this fits in X3

X3's `vehicles.html` page tracks PM schedules, DVIR history, annual inspection due dates, and uploads of inspection reports + repair invoices. A `vehicle_pm_overdue` notification fires through the notification routing helper.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=vehicle-maintenance-records

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

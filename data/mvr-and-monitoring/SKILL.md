---
name: mvr-and-monitoring
description: |
  Use this skill when the user asks about Motor Vehicle Records (MVRs), 49 CFR 391.25 annual MVR review, continuous MVR monitoring services (SambaSafety, Foley, etc.), state MVR fees, what to look for on an MVR, CDLIS (Commercial Driver License Information System), or how often MVRs must be pulled. Cite 49 CFR 391.25 and 391.27.
---

# MVR & Driving Record Monitoring — 49 CFR 391.25

## What 49 CFR 391.25 actually says

Every motor carrier shall, **at least once every 12 months**, make an inquiry to obtain the motor vehicle record of each driver. The inquiry must cover all states where the driver held a license during the prior 12 months.

After reviewing the MVR, a company official must:

1. **Consider** the driver's qualifications, taking into account any accidents and traffic violations.
2. **Sign a note in the DQF** indicating the review was performed (49 CFR 391.25(c)).
3. **Retain the MVR + signed note** for length of employment + 3 years.

Carriers must also obtain a **list of violations** signed by the driver (49 CFR 391.27) annually — or a certification of no violations.

## State MVR fees (sample — varies)

States set their own fees. As of 2026 (subject to change):

| State | Fee |
|---|---|
| Oklahoma | $25.00 |
| Delaware | $25.00 |
| Connecticut | $20.00 |
| Illinois | $20.00 |
| Hawaii | $23.00 |
| Louisiana | $18.00 |
| Maryland | $15.00 |
| Indiana | $12.00 |
| Texas | $6.50 |
| Florida | $8.00 |
| Wisconsin | $8.00 |
| Michigan | $8.00 |
| Ohio | $5.00 |
| North Dakota | $3.00 |
| Kentucky | $3.00 |
| California | $2.00 |
| Missouri | $0.12 |

This is why MVR pulls can cost $5-25 per driver per year just in state fees. Multi-state drivers add up fast.

## CDLIS (Commercial Driver License Information System)

CDLIS is the national database operated by AAMVA (American Association of Motor Vehicle Administrators). It tracks CDL records across all 51 jurisdictions. An MVR pull from a single state will only show:

- That state's record, AND
- Convictions reported by other states FOR offenses while licensed by other states (a quirky data-sharing reality)

For a **comprehensive** record on a driver, pull both:

1. The MVR from the driver's current state, AND
2. A CDLIS report (separate query) to surface anything the home state hasn't received from other jurisdictions.

For drivers who've moved states in the last 3 years, pull MVRs from each prior state too.

## Continuous monitoring vs annual pulls

**Annual pull (the regulatory minimum):**
- Pull once every 12 months
- File the MVR + signed note in DQF
- Cheap (state fee only)
- Risk: between pulls, you don't know if a driver got a DUI or suspension

**Continuous monitoring (recommended):**
- Vendor (e.g. SambaSafety, Foley, DriverFacts) monitors the state DMV record in near-real-time
- You get an alert within 1-3 days of any change (new violation, license suspension, medical cert update)
- Cost: $3-15/driver/month subscription + state fees
- Insurance carriers often discount premiums when continuous monitoring is enabled

**Both:** Many carriers run continuous monitoring AND pull an annual MVR for the DQF record. The annual pull satisfies 391.25(a); the monitoring catches in-year drift.

## What to look for on an MVR

**Disqualifying violations** (49 CFR 391.15 + 383.51) — driver is unqualified for at least 60 days:

- DUI / DWI
- Leaving the scene of an accident
- Felony involving CMV
- Driving a CMV while CDL is revoked/suspended
- Two or more serious violations within 3 years
- Three or more serious violations within 3 years (1-year disqualification)

**Serious violations** (49 CFR 383.51) — disqualifying after 2+ in 3 years:

- Speeding 15+ mph over limit
- Reckless driving
- Improper lane change
- Following too closely
- Texting/distracted driving while operating CMV
- Driving a CMV without proper class CDL
- Driving without a CDL in possession
- Operating CMV with no Med Cert in CDLIS

**Railroad-highway grade crossing violations** (49 CFR 383.53) — different penalty schedule:

- 1st offense: 60 days
- 2nd offense: 120 days
- 3rd offense: 1 year

## Common MVR-review mistakes

1. **Missed the 12-month deadline.** Day 366 since last pull = violation. Don't anchor pulls to hire date if it drifts; track explicit 12-month-from-last-pull deadlines.
2. **No signed note from supervisor.** The MVR pull alone doesn't satisfy 391.25. The carrier official must document their review with a signed note.
3. **Annual violations list not collected.** 391.27 requires a driver-signed list of all violations (or cert of none) in the past 12 months. Separate from MVR.
4. **MVR shows medical cert downgrade and carrier doesn't act.** If the state has the medical cert on file as expired or downgraded, the driver may not be qualified — even if you have a paper copy. The state's record is authoritative.
5. **CDLIS not queried for multi-state drivers.** State MVR misses out-of-state convictions until the home state syncs.

## When the MVR shows a problem

If a violation surfaces that disqualifies the driver:

1. **Remove from safety-sensitive function immediately.**
2. Document the disqualification in the DQF.
3. Notify the driver in writing.
4. Determine the disqualification period and re-evaluate post-period.
5. If permanent (e.g., 2+ DUIs): the driver is permanently disqualified from CMV operation; consider non-CMV roles or termination.

## Quick math

A 25-driver fleet operating in MI:

- 25 drivers × $8 MI MVR fee = $200/year minimum (just for annual pulls)
- Plus $50-150/month if continuous monitoring is enabled = $600-1,800/year
- Plus admin time: 30 min per MVR review × 25 = 12.5 hours/year of safety manager time

Continuous monitoring usually pays for itself by catching 1 disqualifying event mid-cycle (which would have caused a roadside OOS if undetected).

## Where this fits in X3

X3's `mvrs.html` page tracks pull dates, results, and the signed note workflow. `agent-driver-reminders` (rebuilt 2026-05-12) now fires an `annual_mvr_due` reminder 30 days before the 12-month deadline. The `vendor_orders` table can be used to order an MVR through Checkr (or SambaSafety for continuous monitoring once that integration ships).


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=mvr-and-monitoring

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

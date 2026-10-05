---
name: dot-compliance-fundamentals
description: |
  Use this skill when the user asks anything that touches US Department of Transportation (DOT) or Federal Motor Carrier Safety Administration (FMCSA) regulation for commercial motor vehicles (CMVs) — including who's regulated, MC vs DOT number differences, operating authority, BOC-3 process agents, MCS-150 biennial updates, intrastate vs interstate distinctions, exemptions, or pointing to the right CFR section. Cite the actual regulation when answering. Don't guess; if you're not sure which Part applies, ask the user to clarify the operation type (for-hire vs private, passenger vs property, intra vs interstate, hazmat, gross weight rating).
---

# DOT Compliance Fundamentals

## Who is regulated

A motor carrier needs **operating authority + a USDOT number** if they:

- Operate a CMV in **interstate commerce**, AND
- The vehicle meets ONE of: (a) GVWR ≥ 10,001 lb, (b) designed to transport ≥ 9 passengers including driver (for compensation), (c) designed to transport ≥ 16 passengers (regardless of compensation), (d) transports hazmat in placardable quantities.

**Intrastate** carriers may also need a USDOT number — depends on the state. Most states require USDOT + ≥ 10,001 lb GVWR even intrastate.

## USDOT number vs MC number

- **USDOT number** = safety identifier. Used by FMCSA for inspections, accidents, compliance reviews. Every regulated carrier gets one. Free.
- **MC (Motor Carrier) number** = for-hire authority. Only for-hire carriers (charging customers to move freight or passengers) need an MC. Private carriers (hauling their own product) do NOT need an MC. $300 application fee per authority type.

A for-hire carrier needs BOTH. A private carrier needs only a USDOT.

## The application stack (for-hire interstate)

1. **USDOT number** — Free, fmcsa.dot.gov via Unified Registration System (URS).
2. **MC number** — $300, same URS application.
3. **BOC-3 process agent** — Required for interstate. A blanket designation of a registered process agent in each state. ~$25-75 from a process agent service.
4. **Insurance filing** — MCS-90 endorsement for hazmat carriers; BMC-91/91X for property carriers ($750K-$5M minimum). BMC-32 for passenger carriers. Filed by the insurance company directly with FMCSA.
5. **Unified Carrier Registration (UCR)** — Annual fee based on fleet size. Pay through state UCR system.
6. **IFTA** — Interstate Fuel Tax Agreement. Quarterly returns reporting fuel + miles per jurisdiction. Required for interstate ≥ 26,001 lb or 3+ axles.
7. **IRP** — International Registration Plan apportioned plate. Required for interstate ≥ 26,001 lb or 3+ axles.

**New entrant safety audit** happens 12-18 months after USDOT number issuance.

## MCS-150 biennial update

Every motor carrier MUST update their MCS-150 every 24 months. Schedule based on the last digit of the USDOT number + the next-to-last digit:

- Next-to-last digit even → update in even years
- Next-to-last digit odd → update in odd years
- Last digit determines the month (1=Jan, 2=Feb, ..., 0=Oct)

Penalties: up to $1,150/day for failure to update; deactivation of operating authority after 90 days overdue.

## Operations classification

- **For-hire vs Private:** for-hire = paid to move; private = move own goods.
- **Property vs Passenger:** different insurance minimums + authority types.
- **General Freight vs Household Goods (HHG):** HHG has additional consumer protections (49 CFR 375).
- **Hazmat:** triggers 49 CFR 171-180 + driver hazmat endorsement + hazmat permit (HMSP) if shipping ≥ certain quantities.
- **Interstate vs Intrastate:** interstate = crossing state lines OR a continuation of interstate journey. Intrastate = entirely within one state's borders. Federal rules apply to interstate; intrastate carriers follow state CMV rules, which often mirror federal but vary.

## Where to look things up

| Need | Source |
|---|---|
| Driver Qualification | 49 CFR 391 |
| Driving / Hours of Service | 49 CFR 395 |
| Drug & Alcohol | 49 CFR 382 + 40 |
| Vehicle Inspection / Repair / Maintenance | 49 CFR 396 |
| Inspection report (DVIR) | 49 CFR 396.11 |
| Accident Register | 49 CFR 390.15 |
| Hazmat | 49 CFR 171-180 |
| Insurance | 49 CFR 387 |
| New Entrant Safety Audit | 49 CFR 385 |
| FMCSA Portal | https://portal.fmcsa.dot.gov |
| Carrier Snapshot | https://safer.fmcsa.dot.gov |
| Clearinghouse | https://clearinghouse.fmcsa.dot.gov |
| Pre-Employment Screening Program (PSP) | https://www.psp.fmcsa.dot.gov |

## Common terminology decoded

| Acronym | What it means |
|---|---|
| CMV | Commercial Motor Vehicle |
| GVWR | Gross Vehicle Weight Rating (manufacturer max) |
| GVW | Gross Vehicle Weight (actual loaded) |
| GCWR | Gross Combination Weight Rating (tractor + trailer) |
| CDL | Commercial Driver License |
| CLP | Commercial Learner's Permit |
| HOS | Hours of Service |
| ELD | Electronic Logging Device |
| AOBRD | Automatic On-Board Recording Device (predecessor to ELD; phased out) |
| DVIR | Driver Vehicle Inspection Report |
| MVR | Motor Vehicle Record |
| DQF | Driver Qualification File |
| MRO | Medical Review Officer (drug test results) |
| SAP | Substance Abuse Professional |
| RTD | Return-to-Duty |
| PSP | Pre-Employment Screening Program (FMCSA-run) |
| CSA | Compliance, Safety, Accountability (FMCSA enforcement program) |
| BASIC | Behavior Analysis and Safety Improvement Category (CSA scoring) |
| SMS | Safety Measurement System (CSA scoring engine) |
| ISS | Inspection Selection System (roadside trigger) |
| OOS | Out of Service |
| FAST Act | Fixing America's Surface Transportation Act |
| MAP-21 | Moving Ahead for Progress in the 21st Century Act |
| ELDT | Entry-Level Driver Training (49 CFR 380) |
| HMSP | Hazmat Safety Permit |
| MCS-150 | Motor Carrier Identification Report (the biennial update) |
| MCS-90 | Insurance endorsement (hazmat) |
| BMC-91/91X | Property insurance filing |
| BOC-3 | Process Agent Designation |
| BSI | BASIC Severity Indicator |
| OBSI | Observed BASIC Severity Indicator (CSA) |
| IFTA | International Fuel Tax Agreement |
| IRP | International Registration Plan |
| UCR | Unified Carrier Registration |
| HUT | Highway Use Tax (state-level, e.g. NY) |

## When in doubt

Tell the user to call their state's DOT/PUC office for state-specific rules, and call FMCSA at 1-800-832-5660 for federal questions. If the question involves enforcement action (audit, OOS, penalty), recommend they consult a DOT compliance attorney before responding.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=dot-compliance-fundamentals

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

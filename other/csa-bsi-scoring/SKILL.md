---
name: csa-bsi-scoring
description: |
  Use this skill when the user asks about FMCSA Compliance Safety Accountability (CSA) program scoring — the seven BASIC categories, BASIC Severity Indicator (BSI), peer percentiles, intervention thresholds, how violations age out, SMS Methodology, ISS (Inspection Selection System), what "alert" status means, Safety Measurement System mechanics, or DataQ disputes. Cite SMS Methodology v3.20.
---

# CSA / SMS Scoring — FMCSA Compliance Safety Accountability

## The seven BASICs (Behavior Analysis & Safety Improvement Categories)

Each BASIC is scored separately. Violations from roadside inspections + crashes accumulate over a 24-month rolling window.

| BASIC | What it covers | Inspection types | Normalization |
|---|---|---|---|
| **Unsafe Driving** | Speeding, reckless driving, lane changes, following too closely, texting, seatbelt | Driver inspections | Per driver inspection |
| **Hours of Service Compliance** | HOS violations: log book, ELD, fatigue | Driver inspections | Per driver inspection |
| **Driver Fitness** | CDL, medical cert, ELDT, training | Driver inspections | Per driver inspection |
| **Controlled Substances / Alcohol** | D&A violations | Driver inspections | Per driver inspection |
| **Vehicle Maintenance** | Brakes, tires, lights, leaks, body, frame | Vehicle inspections | Per vehicle inspection |
| **Hazardous Materials Compliance** | Hazmat placarding, labeling, packaging, training | Vehicle inspections (hazmat) | Per hazmat inspection |
| **Crash Indicator** | DOT-recordable crashes; NOT public-facing | Crashes | Per power-unit-mile (hybrid) |

## How violations score

Each violation has a **severity weight (1-10)** assigned by FMCSA based on its causal relationship to safety. Examples:

- Following too closely: 10
- Speeding 15+ mph over: 7
- No medical cert: 5
- Logbook violation (form/manner): 4
- Tire tread depth: 3
- Headlamp out: 1

Violations age out: full weight for first 6 months, then weight decreases as the violation passes the 12 and 18 month marks.

## BSI calculation per BASIC

```
Raw BSI = Σ (severity × time_weight × OOS_modifier × VIOL_TYPE_modifier)
                     /  exposure_factor
```

Where:
- **OOS modifier** = +2 if the violation was an OOS (Out of Service) violation
- **Time weight** = 3 for violations 0-6 months old; 2 for 6-12 months; 1 for 12-24 months
- **Exposure factor** = denominator that normalizes for fleet size

## Exposure factors (denominators)

| BASIC | Denominator |
|---|---|
| Unsafe Driving | Driver inspections |
| HOS Compliance | Driver inspections |
| Driver Fitness | Driver inspections |
| Controlled Substances | Driver inspections |
| Vehicle Maintenance | Vehicle inspections |
| HM Compliance | HM inspections |
| Crash Indicator | Power units × VMT (vehicle miles traveled) × utilization factor |

This means: a carrier with very few inspections may have a HIGH BSI even with only one or two violations (small denominator), while a high-inspection carrier with many small violations may have a LOW BSI.

## Peer percentile (the actual public score)

FMCSA groups carriers into peer-similarity buckets:

- **Safety Event Group (SEG)** — for non-crash BASICs, groups based on # of inspections
- **Carrier Size** — for Crash Indicator, groups based on power-unit count + VMT

Within each peer group, your BSI is compared to peers. Your score is your **peer percentile** (0-100). Higher = worse.

## Intervention thresholds

| BASIC | Hazmat/PAX threshold | General threshold |
|---|---|---|
| Unsafe Driving | 65% | 65% |
| HOS Compliance | 65% | 65% |
| Driver Fitness | 80% | 80% |
| Controlled Substances | 80% | 80% |
| Vehicle Maintenance | 75% | 80% |
| HM Compliance | 80% | 80% |
| Crash Indicator | 65% | 65% |

If a carrier exceeds a threshold in any BASIC = **"Alert"** status = increased likelihood of FMCSA intervention (warning letters, on-site investigations, compliance reviews).

## Inspection Selection System (ISS)

ISS is the roadside priority score (0-100) that determines whether a CMV is selected for inspection at a weigh station or random roadside check. Computed from BSIs across all BASICs:

- **0-49** = "Pass" — minimal inspection priority
- **50-74** = "Optional" — inspector's discretion
- **75-100** = "Inspect" — high priority for inspection

So a carrier with even one BASIC near alert threshold will have an elevated ISS — meaning drivers get pulled in more often, more violations accumulate, scores climb further. Vicious cycle.

## How to reduce BSI

1. **Fix the underlying behavior.** Bad brake checks? Fix preventive maintenance. HOS issues? Audit ELD usage. Speeding tickets? Coach + telematics.
2. **Increase clean inspections.** Each clean inspection adds to the denominator. Encourage drivers to participate in voluntary inspections.
3. **Dispute incorrect violations via DataQ.** If a violation was wrongly issued (e.g., driver wasn't your employee, vehicle wasn't yours, violation cited the wrong CFR), file a DataQ dispute. Successful DataQ disputes remove the violation from your BASIC.
4. **Wait for old violations to age out.** After 24 months, the violation drops off the SMS window entirely.

## DataQ dispute process

Go to `dataqs.fmcsa.dot.gov`:

1. Identify the violation report.
2. Submit a Request for Data Review (RDR).
3. FMCSA assigns to a state Disposition Office.
4. State investigates (typically 30-60 days).
5. Outcome: violation amended, removed, or upheld.

Common successful DataQ outcomes:
- Driver wasn't on duty (PC time misclassified as on duty)
- Vehicle wasn't yours (leased, sold, returned)
- Violation cited wrong CFR
- Inspector error (wrong measurement, wrong weight)
- Carrier wasn't the responsible party

## Where the SMS Methodology document lives

`https://csa.fmcsa.dot.gov/Documents/SMSMethodology.pdf` — currently v3.20 (Sept 2025 rev). FMCSA updates approximately every 12-18 months. The document has the full severity weight tables (Appendix A) and the acute/critical violations list (Appendix B).

## The "BSI Crash" — Crash Indicator BASIC

Crash Indicator is calculated differently:

- Only **DOT-recordable** crashes count (49 CFR 390.5: fatality OR injury away from scene OR disabling damage)
- Crashes count regardless of fault (preventability is captured in a separate program, but not for SMS scoring as of 2024)
- Exposure factor is power units × VMT × utilization (hybrid)
- Not publicly visible (private to the carrier + FMCSA)

## Where this fits in X3

X3's `csa-scores.html` page surfaces all 7 BASICs with peer percentile + trend. `agent-csa-monitor` runs monthly and pulls fresh BSI from FMCSA. The X3 Risk Index (proprietary) blends SMS BSI with our own internal signals (driver retention, training completion, internal inspection outcomes). The SMS methodology constants are encoded in `_shared/sms_methodology.ts`.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=csa-bsi-scoring

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

---
name: medical-certification
description: |
  Use this skill when the user asks about CDL driver medical certification — 49 CFR 391.41-49 medical qualifications, medical examiner's certificate (Long Form 5876 + Short Form 5875), National Registry of Certified Medical Examiners (NRCME), medical restrictions, federal disqualifying conditions, exemption programs (vision, diabetes, hearing), the FMCSA Medical Examiner's Handbook, or what to do when a driver's medical cert is downgraded. Cite specific 49 CFR 391 sections.
---

# Medical Certification — 49 CFR 391.41-49

Every interstate CDL driver must hold a current valid Medical Examiner's Certificate, issued by an NRCME-certified medical examiner after a Department of Transportation (DOT) physical examination.

## How long is a certificate valid?

**Up to 24 months.** The examiner can issue for shorter periods (3, 6, 12 months) if conditions warrant monitoring. The expiration date is on the certificate; check it.

## Who can issue a certificate?

Only an examiner listed on the **National Registry of Certified Medical Examiners (NRCME)**. Verify at `nationalregistry.fmcsa.dot.gov`. Drivers should be advised to verify their examiner is currently registered BEFORE the exam (some examiners have been delisted; certs from delisted examiners are invalid).

## Common federal disqualifying conditions (49 CFR 391.41(b))

A driver is medically unqualified if they have:

1. **Loss of foot, leg, hand, or arm** — interferes with safe operation (a Skill Performance Evaluation can grant exemption).
2. **Impairment of the limbs** — same; SPE exemption available.
3. **Diabetes** requiring insulin for control — exemption via Diabetes Exemption Program possible (proves stable control + endocrinologist letter).
4. **Cardiovascular disease** — MI, angina, syncope, dyspnea, collapse, congestive cardiac failure. Conditional on cardiologist clearance + ECG/stress test.
5. **Respiratory dysfunction** — likely to interfere with safe driving.
6. **Hypertension** — uncontrolled. Stage 1: 1-year cert; Stage 2: 3-month cert with treatment; Stage 3: disqualified until controlled.
7. **Musculoskeletal limitations** — interferes with safe operation.
8. **Mental disorders** — clinical diagnosis of psychiatric illness likely to interfere with safe driving.
9. **Vision impairment** — corrected visual acuity worse than 20/40 in each eye; field of vision < 70° in horizontal meridian; inability to recognize colors of traffic signals. Vision Exemption Program possible.
10. **Hearing loss** — perception of a forced whisper voice at no less than 5 feet OR hearing test with average loss ≥ 40 dB in better ear at 500 Hz, 1000 Hz, 2000 Hz. Hearing Exemption Program possible.
11. **Substance abuse** (drug or alcohol) — current diagnosis or evidence of habitual use. Disqualifying.
12. **Epilepsy or convulsive disorder** — disqualifying unless seizure-free off medication for 10+ years (with specific neurological clearance).

## Certificate types

- **Long Form 5876** — completed by examiner during exam. Stays with examiner or carrier; not given to driver.
- **Short Form 5875 (Medical Examiner's Certificate)** — the wallet-sized "Med Card" the driver carries; copy goes in DQF.
- **Medical Examination Report (MER)** — actually the Long Form 5876. Detailed record of findings.

## CDLIS interaction (49 CFR 383.71)

Since 2014, CDL holders self-certify their interstate or intrastate, excepted vs non-excepted status:

- **Non-excepted interstate** — must have a valid Med Cert on file with the state DMV. State updates CDLIS.
- **Excepted interstate** — typically intrastate-only or military. Med cert not required for CDL.
- **Non-excepted intrastate** — state-specific rules (most mirror federal).
- **Excepted intrastate** — state-specific.

If a driver's medical cert expires AND the state has not received an updated cert, the state DMV will **downgrade** the CDL to a non-commercial license. The driver then cannot legally operate a CMV — even if they hand-carry an unexpired paper cert.

**Critical:** The state's CDLIS record is authoritative. A driver might have a current paper card but be downgraded in CDLIS. Verify both.

## When a medical condition develops

If a driver develops a disqualifying condition between certs:

1. Driver must report to the employer immediately.
2. Carrier removes driver from safety-sensitive function.
3. Driver consults the NRCME examiner.
4. New medical exam: pass = continue; fail = disqualification or pursue exemption.

## Exemption programs

FMCSA has formal exemption programs for:

- **Vision Exemption Program** — for monocular vision or below-spec acuity. Requires 3-year monitoring period.
- **Diabetes Exemption Program** — for insulin-using drivers. Requires endocrinologist letter + monitoring.
- **Hearing Exemption Program** — for severe hearing loss.
- **Skill Performance Evaluation (SPE)** — for limb impairment / amputation. Driver demonstrates safe operation of a CMV.
- **Seizure Disorder Exemption** — rarer; requires 8+ year seizure-free + specific neurological criteria.

Each exemption requires an application + supporting clinical documentation + monitoring. Average processing time: 6-12 months. Apply via FMCSA.

## DOT exam: what's tested

- Vital signs (BP, pulse, temp, height/weight)
- Vision (acuity 20/40 each eye, depth perception, color)
- Hearing (forced whisper at 5 ft OR audiometer ≥ 40 dB)
- Pulmonary function (spirometry if indicated)
- Cardiovascular (ECG if indicated, BP)
- Urinalysis (NOT drug test; just protein/sugar/blood)
- Musculoskeletal (range of motion, grip strength)
- Mental/emotional health
- Neurological
- Substance abuse / mental health history
- Sleep history (sleep apnea screening; if positive, CPAP compliance required)

## Sleep apnea (specific to CMV drivers)

FMCSA recommends (not formally requires) that any driver with BMI ≥ 33 AND multiple risk factors be screened for obstructive sleep apnea (OSA). Examiners typically:

- Refer for a sleep study if risk factors present
- Issue a short-term cert (3 months) pending sleep study
- Require CPAP compliance documentation (download report from CPAP machine) for ongoing certification

A driver who refuses sleep study or fails to comply with CPAP may be disqualified.

## What the carrier needs in the DQF

- Copy of the **current** Medical Examiner's Certificate (Short Form 5875)
- Verification of NRCME registration of the examiner (a print/screenshot from nationalregistry.fmcsa.dot.gov)
- If exemption: copy of exemption + monitoring records

## Common medical cert mistakes

1. **Driving past the expiration date.** Even 1 day expired = unqualified. CSA violation if caught at roadside.
2. **Failure to verify NRCME currency.** Examiner may have been delisted; their cert is invalid even if not yet expired.
3. **Mismatch between paper card and state CDLIS.** Driver carries the paper card but state hasn't received notice; CDLIS is authoritative.
4. **Restrictions on cert not communicated to dispatch.** "Wearing corrective lenses" or "no nighttime driving" — must be respected.
5. **Examiner issues a 12-month cert but carrier files it as 24-month.** Track the actual issuance date + duration, not assumption.

## Where this fits in X3

X3's `dq-files.html` shows medical cert expiry dates; `agent-driver-reminders` fires email at 30/14/7-day thresholds + SMS at 1 day. Continuous monitoring (via SambaSafety or similar) detects when the state CDLIS record downgrades a driver — fires an immediate safety-manager alert.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=medical-certification

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

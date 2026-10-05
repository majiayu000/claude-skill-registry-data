---
name: dot-physical-exam-decoder
description: |
  Use this skill when the user asks how to interpret a DOT medical examiner's findings — what restrictions mean (corrective lenses, hearing aid, no insulin, etc.), what conditions trigger short-term vs 24-month certificates, vision/hearing thresholds, blood pressure categories, sleep apnea screening, when to seek an exemption program, and how to handle a downgrade or denial. Cite 49 CFR 391.41-49 and the FMCSA Medical Examiner Handbook.
---

# DOT Physical Exam — Decoder

When a CDL driver completes a DOT physical, the examiner issues a Medical Examiner's Certificate (Short Form 5875) with a duration + restrictions. This skill decodes what's on the cert.

## The certificate fields (Short Form 5875)

1. **Driver name + DOB** + signature
2. **Examiner name + NRCME registration number**
3. **Exam date**
4. **Expiration date** (max 24 months out)
5. **Restrictions** (list, can be blank)
6. **Examiner's signature + seal**

## Common duration variations

- **24 months** — full pass. No conditions requiring monitoring.
- **12 months** — minor conditions (e.g., controlled hypertension). Re-eval in 1 year.
- **3-6 months** — monitoring required (e.g., sleep apnea + CPAP pending, recovering from cardiac event).
- **Disqualified** — fails one of the 49 CFR 391.41(b) conditions; cert NOT issued.

## Restrictions decoded

Common restrictions you'll see on the cert:

| Code | What it means | Operational implication |
|---|---|---|
| **B** | Wearing corrective lenses | Driver must wear glasses/contacts while driving |
| **C** | Hearing aid | Driver must wear hearing aid |
| **E** | No manual transmission | Driver may operate only automatic |
| **F** | Outside mirrors required | Vehicle must have both side mirrors |
| **G** | Daytime driving only | Sunrise to sunset only |
| **H** | Insulin-using (with exemption) | OK to drive with diabetes exemption letter |
| **K** | Intrastate only | Cannot operate interstate |
| **L** | No tractor-trailer | Single-unit vehicles only |
| **M** | No Class A | Class B and below only |
| **N** | No Class A or B | Class C only |
| **O** | No tractor-trailer | Same as L |
| **P** | No passengers | School bus drivers etc. with passenger restriction |
| **R** | No exemption program | Active exemption (e.g., diabetes, vision) |
| **V** | Medical variance | Approved exemption from a disqualifying condition |
| **X** | Vision in one eye | Monocular vision (with exemption) |

A driver with restriction B can drive — but only with corrective lenses on. If pulled over without glasses = violation.

## Vision requirements (49 CFR 391.41(b)(10))

- **Visual acuity:** Each eye must have ≥ 20/40 vision (with correction allowed)
- **Field of vision:** ≥ 70° in horizontal meridian in each eye
- **Color recognition:** Must distinguish traffic signal colors (red, green, amber)
- **No monocular vision** (one eye) unless granted a Vision Exemption

Vision Exemption Program — separate FMCSA process; 3-year monitoring; ~6-12 month application timeline.

## Hearing requirements (49 CFR 391.41(b)(11))

Driver must hear:

- **Forced whisper** at ≥ 5 feet (with or without hearing aid), OR
- **Audiometer test:** average hearing loss ≤ 40 dB at 500 Hz, 1000 Hz, and 2000 Hz in the better ear

Hearing Exemption Program — separate FMCSA process.

## Blood pressure categories (FMCSA Medical Examiner Handbook)

| BP Category | Reading | Cert Duration | Conditions |
|---|---|---|---|
| Stage 1 | 140-159 / 90-99 | 1-year cert | Recheck in 1 year; lifestyle modification recommended |
| Stage 2 | 160-179 / 100-109 | 3-month cert | Treatment required; cert renewed only after BP controlled |
| Stage 3 | ≥ 180 / ≥ 110 | Disqualified | Cannot certify until controlled below Stage 2 |

Controlled hypertension (BP under control with medication) typically gets a 1-year cert.

## Sleep apnea screening

Drivers with risk factors for obstructive sleep apnea (OSA) — particularly BMI ≥ 33 and a sleep history — are typically:

- Issued a short-term cert (3 months) pending sleep study
- Required to complete a sleep study + CPAP compliance documentation
- Re-evaluated with CPAP compliance data (machine download report)

A driver who refuses sleep study or fails CPAP compliance may be disqualified.

## Diabetes (49 CFR 391.46)

- **Type 2 diabetes, no insulin** — qualified if controlled
- **Type 2 diabetes, oral medication** — qualified if controlled
- **Insulin-using diabetes** — DISQUALIFIED unless granted Diabetes Exemption

Diabetes Exemption Program — requires endocrinologist letter, A1C monitoring, no severe hypoglycemic events for 12+ months. Quarterly monitoring during certification.

## Cardiovascular (49 CFR 391.41(b)(4))

History of:
- Myocardial Infarction (MI / heart attack)
- Angina pectoris
- Congestive heart failure
- Syncope (fainting)
- Dyspnea (severe shortness of breath)
- Cardiac surgery

Requires cardiologist clearance, ECG, stress test results, ejection fraction documentation. Cert duration: 1 year typically; some conditions warrant 2 years.

## Mental health

- Active psychosis or severe mood disorder → disqualifying
- Controlled depression/anxiety with medication compliance → typically qualified
- Recent suicide attempt or violent psychiatric history → individualized review

## When a cert is downgraded

A driver's cert can be downgraded if:

- Medical condition develops between exams
- CDLIS shows the cert as expired or invalid
- Driver had a non-DOT health event (cardiac, neurological) that surfaces
- A second-opinion exam by a different NRCME examiner

When this happens, driver is unqualified until re-certified.

## What carriers should do

1. **Verify NRCME registration** of the examiner before the exam (or right after) at `nationalregistry.fmcsa.dot.gov`.
2. **Photocopy the certificate** for the DQF immediately.
3. **Note the expiration date** in a tracking system — flag for 30/14/7/1-day reminders.
4. **Don't accept generic doctor notes** — only NRCME-issued certs are valid.
5. **For drivers with restrictions** — communicate to dispatch (e.g., "Driver Y has restriction E: no manual transmission").
6. **For short-term certs** — schedule the next exam within the cert duration; don't let the driver lapse.

## Where this fits in X3

X3's `dq-files.html` decodes the Medical Examiner's Certificate including restrictions. `agent-driver-reminders` fires medical-cert expiry reminders at 30/14/7/1-day thresholds (now policy-routed via the notification_routing helper). The X3 dashboard surfaces drivers with active restrictions to dispatchers so they don't assign vehicles outside their certified class.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=dot-physical-exam-decoder

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*

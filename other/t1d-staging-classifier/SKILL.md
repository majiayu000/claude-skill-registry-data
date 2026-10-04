---
name: t1d-staging-classifier
description: Classify a person with a positive islet autoantibody screen into a specific stage of type 1 diabetes (At Risk / Stage 1 / Stage 2a / Stage 2b / Stage 3a / Stage 3b / Stage 4) using the international consensus staging framework based on autoantibody count and glycaemic status. Use when a clinician asks how to stage a positive autoantibody screen, what stage of T1D is this, is this early-stage T1D, does this child need insulin yet, is this presymptomatic T1D, does this qualify for teplizumab, or presents a person with any combination of islet autoantibodies + glucose data. Applies across paediatric and adult populations. Grounded in Hussain et al 2026 (Diabetes, Obesity and Metabolism, IDF Europe consensus, DOI 10.1111/dom.70569).
---

# Type 1 Diabetes Staging Classifier

Assign the correct stage of type 1 diabetes to a person with detectable islet autoantibodies. Staging determines monitoring intensity, eligibility for disease-modifying therapy (teplizumab), and whether insulin is required.

---

## Step 1 — Confirm the autoantibody status is real

Before staging, verify:

- The **positive screen has been confirmed in a second sample** — a single positive result is not sufficient
- Confirmation used **two independent laboratory methods** (e.g. radiobinding assay + ELISA)
- The **specific antibodies** are documented (GAD65 / IAA / IA2 / ZnT8)
- **Negative status for the OTHER islet autoantibodies** has been confirmed on the same second sample

If any of the above is missing → arrange confirmation testing **before** staging. An unconfirmed positive cannot be staged.

---

## Step 2 — Count the confirmed autoantibodies

| Confirmed autoantibody count | Direction |
|---|---|
| **0** (all negative on confirmation) | Not T1D by antibody criteria. Consider other causes of hyperglycaemia if present |
| **1 confirmed** (single positive, second sample positive for the SAME antibody with 2 methods) | **At Risk** (see Step 4) |
| **Transient single positive** (second sample negative) | **At Risk** — arrange repeat testing per Step 4 |
| **≥2 confirmed** | Proceed to Step 3 to assign Stage 1, 2, or 3 |

---

## Step 3 — Combine antibody count with glycaemic status

Get the person's most recent glycaemic profile:

- Fasting plasma glucose (FPG) in **mmol/L (mg/dL)**
- 2-hour value on OGTT
- HbA1c in **mmol/mol (%)**
- If available, CGM data — % time above 7.8 mmol/L (140 mg/dL)
- Presence or absence of osmotic symptoms (polyuria, polydipsia, weight loss)

Apply this table (in order — assign the FIRST matching row):

| Autoantibodies | Glycaemia | Symptoms | **Stage** |
|---|---|---|---|
| ≥2 confirmed | **Normal** (FPG <5.6 mmol/L / <100 mg/dL, 2h OGTT <7.8 mmol/L / <140 mg/dL, HbA1c <39 mmol/mol / <5.7%) | Asymptomatic | **Stage 1** |
| ≥2 confirmed | **Mild dysglycaemia**: ≥1 of — FPG 5.6–6.9 mmol/L (100–124 mg/dL) / 2h OGTT 7.8–11.0 mmol/L (140–198 mg/dL) / HbA1c 39–47 mmol/mol (5.7–6.4%) | Asymptomatic | **Stage 2a** |
| ≥2 confirmed | **Notable dysglycaemia below ADA thresholds**: one of the Stage 2a glycaemic indicators AND CGM time >7.8 mmol/L (>140 mg/dL) of **>10%** | Asymptomatic | **Stage 2b** |
| ≥2 confirmed | **Meets ADA diagnostic criteria** for diabetes (FPG ≥7.0 mmol/L / ≥126 mg/dL on two occasions, OR 2h OGTT ≥11.1 mmol/L / ≥200 mg/dL, OR HbA1c ≥48 mmol/mol / ≥6.5%, OR random glucose ≥11.1 mmol/L with symptoms) | **Asymptomatic** | **Stage 3a** |
| ≥2 confirmed | Meets ADA diagnostic criteria | **Symptomatic** (osmotic symptoms, weight loss, DKA) | **Stage 3b** |
| Present | Established insulin-treated T1D of long duration | — | **Stage 4** |

---

## Step 4 — Special case: single or transient single autoantibody ("At Risk")

**Confirmed single autoantibody positive** (second sample confirms the same antibody, other antibodies negative):

- **~10–15% risk of progression to Stage 3 T1D over 15 years** (vs 0.3% general population)
- Retesting and glucose monitoring is **less stringent** than for multi-antibody individuals
- **No indication for teplizumab** at this stage
- **Retest islet autoantibodies periodically** (e.g. annually or per local protocol) — a person can progress from single to multiple antibodies
- Education about T1D symptoms (osmotic symptoms, weight loss, DKA) is still valuable

**Transient single positive** (initial positive, second sample negative):

- Interpret as "at risk" — the antibody may fluctuate
- Repeat testing within an appropriate interval (e.g. 6–12 months)
- Do NOT stage as Stage 1 unless ≥2 antibodies are confirmed

---

## Step 5 — Downstream action per stage

Once stage is assigned, the management pathway is:

| Stage | Priority action |
|---|---|
| **At Risk** | Retesting cadence, symptom education, no monitoring program |
| **Stage 1** | **Enrol in early-stage T1D monitoring program** (education, glucose monitoring, psychological support, DKA prevention). No disease-modifying therapy yet |
| **Stage 2** (2a or 2b) | Enrol in monitoring program AND **evaluate teplizumab eligibility** — Stage 2 is the approved indication in FDA, EMA, MHRA, Health Canada |
| **Stage 3a** (asymptomatic) | May not need insulin immediately; some evidence supports observation with close monitoring, others start insulin. Individual decision |
| **Stage 3b** (symptomatic) | **Insulin therapy required** — standard T1D management. Assess for DKA at presentation |
| **Stage 4** | Standard long-term T1D management (glucose monitoring, complication surveillance, comorbidity management) |

---

## Guardrails

- **Never stage on a single positive screen without confirmation** — single unconfirmed positives are common false positives. Staging on unconfirmed data leads to overdiagnosis, unnecessary anxiety, and potentially inappropriate therapy
- **Stage 3 is a biochemical diagnosis, not a symptom diagnosis** — a person can meet ADA criteria without osmotic symptoms (Stage 3a). Do not withhold the T1D label just because they feel well
- **A person can move between stages** — retest glycaemia at each contact. A Stage 1 individual may become Stage 2 with mild FPG rise; a Stage 2 can progress to Stage 3 over weeks to months in adolescents
- **Osmotic symptoms at any point trigger urgent evaluation** — do not wait for a scheduled visit. Educate the family/patient to seek care immediately for polyuria/polydipsia/weight loss/vomiting
- **DKA at presentation is a preventable failure** — the whole point of staging early is to catch progression BEFORE DKA. If a monitored person presents in DKA, review why the monitoring didn't detect the transition earlier
- **Stage 3a is genuinely controversial** — some clinicians and guidelines start insulin at Stage 3a (biochemical); others observe carefully with rapid escalation ready. Discuss both approaches with the patient/family and document the shared decision
- **Progression to Stage 3 approaches 100% in children/adolescents with confirmed ≥2 autoantibodies** — this is not "risk" language; it is near-certainty. Communicate it appropriately without inducing distress. Progression is slower in adults (research ongoing)
- **Progression risk is not the same as immediate diabetes** — average time from Stage 1 to Stage 3 in children is years, and in adults is likely longer. There is time to prepare
- **Stage 2b (CGM-defined) requires CGM data** — if CGM is not available, use whichever Stage 2a criterion is met and label as Stage 2 (subtype not further specified)
- **HbA1c can miss early dysglycaemia** — in a person with ≥2 autoantibodies and normal HbA1c, still perform OGTT or arrange CGM before concluding "Stage 1"

---

## Related MD2SKILL skills

- `t1d-islet-autoantibody-screening-confirmation` — how to run the screen and confirm a positive
- `teplizumab-eligibility-and-course` — for Stage 2 T1D
- `nd-t2d-oad-selector` — if the diagnosis turns out to be T2DM, not T1DM (distinguishable partly by autoantibody status)
- `gcih-patient-classifier` — for inpatient hyperglycaemia distinguishable from new-onset T1D

---

## Source

Hussain S, Tree T, Mathieu C, Klupa T, Tuomaala A-K, de Wit M, Kordonouri O, Braune K, Pall J, Castano L, Besser REJ, Galhardo J, Ulivi F, Bosi E, Bogdanovic U, Alabert C, Battelino T. **An international consensus on screening and monitoring early-stage type 1 diabetes: A roadmap to European implementation.** *Diabetes, Obesity and Metabolism.* 2026;28:3535–3556. DOI: 10.1111/dom.70569. Open-access under Creative Commons Attribution (CC-BY). Section 3 and Figure 1.

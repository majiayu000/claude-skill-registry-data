---
name: endo-dose-escalation
description: Guides dose escalation for obesity pharmacotherapy based on efficacy and tolerability while staying within approved upper dose limits. Triggers include clinician questions like "How should I titrate naltrexone/bupropion if the starting dose is tolerated?" or "What is the maximum liraglutide dose I can use?"
---

# Guide dose escalation based on efficacy/tolerability

## STEP 1 — Gather Information
Collect current medication, dose, duration, weight change (% body weight), adverse effects, comorbidities, concomitant medications, baseline weight, and patient goals. **Action:** Determine if the patient has tolerated the current dose and whether weight loss is below the efficacy threshold for that agent.

## STEP 2 — Rule In / Rule Out
Is the patient tolerating the current dose (no severe or persistent side effects) AND has suboptimal response (weight loss <3% at 12 weeks for phentermine/topiramate, <5% at 12 weeks for naltrexone/bupropion or liraglutide, or <2% at 12 weeks for orlistat/lorcaserin)? 
- **Yes:** Proceed to dose escalation. 
- **No:** Maintain current dose if tolerable and partially effective, reduce dose if intolerable, or discontinue if ineffective and not tolerable.

## STEP 3 — Classify or Stratify
Identify the specific obesity medication to select the appropriate dose-escalation schedule:
| Medication | Starting dose | Step 1 | Step 2 | Step 3 (max) |
|------------|---------------|--------|--------|--------------|
| Phentermine/topiramate ER | 3.75/23 mg QD | 7.5/46 mg QD | 11.25/69 mg QD | 15/92 mg QD |
| Naltrexone/bupropion | 1 tablet QAM | 1 tablet BID (weeks 2‑3) | 2 tablets QAM + 1 tablet QPM (week 4) | 2 tablets BID |
| Liraglutide | 0.6 mg SC QD | +0.6 mg weekly → 1.2 mg | → 1.8 mg | → 2.4 mg | → 3.0 mg |
| Lorcaserin | 10 mg QD | 10 mg BID (max) | — | — |
| Orlistat | 60 mg TID (OTC) | 120 mg TID (prescription) | — | — |
**Action:** Select the next dose level in the schedule based on current dose and tolerance.

## STEP 4 — Decide
If the next dose level is within the upper approved limit and the patient remains tolerant, **prescribe the escalated dose** and schedule follow‑up in 4 weeks to reassess tolerance and weight change. If the patient is already at the maximum approved dose, **maintain** that dose and evaluate need for alternative therapy.

## Clinical Guardrails / Mimics / Pitfalls
Do not exceed the upper approved dose for any agent; avoid escalation if emergent or worsening side effects (e.g., hypertension, tachycardia, mood changes, GI intolerance); do not escalate in pregnancy, uncontrolled hypertension, or recent MAOI use; monitor weight and adverse effects monthly; consider discontinuation if no ≥5% weight loss at max dose after 12 weeks.

## Concrete Clinical Example
A 45‑year‑old woman with BMI 34 starts naltrexone/bupropion 8 mg/90 mg (1 tablet) each morning. After 4 weeks she reports mild nausea that resolved, and has lost 2% of body weight. Since she tolerates the dose and weight loss is <5%, the dose is escalated to 1 tablet BID (morning and evening). After another 4 weeks she tolerates the regimen and loses an additional 3%; dose is then increased to 2 tablets QAM + 1 tablet QPM, then to 2 tablets BID as tolerated.

**Source:** Pharmacological Management of Obesity: An Endocrine Society Clinical Practice Guideline, Endocrine Society, 2015, DOI:10.1210/jc.2014-3415

> **TODO:** consider adding scripts/calc.py for the endo-dose-escalation calculator

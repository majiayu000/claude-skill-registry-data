---
name: ata-di-workup
description: This skill guides the simultaneous measurement of serum and urine osmolarity to evaluate polyuria for central diabetes insipidus. It is triggered when a patient presents with polyuria exceeding 50 mL/kg/24 hours or 3.5 L/day in a 70‑kg individual.
---

# Workup polyuria for central diabetes insipidus

## STEP 1 — Gather Information
- Confirm polyuria: urine output >50 mL/kg/24 h or >3.5 L/24 h in a 70‑kg adult.
- Measure serum osmolarity (mOsmol/L).
- Measure urine osmolarity (mOsmol/L).
- Perform urine dipstick for glucose.
- Record patient weight if needed for volume threshold.

## STEP 2 — Rule In / Rule Out
- Is serum osmolarity >295 mOsmol/L?
  - **No** → Consider non‑DI causes of polyuria (e.g., primary polydipsia, osmotic diuresis); stop DI workup here.
  - **Yes** → Proceed to step 3.

## STEP 3 — Classify or Stratify
- Calculate urine:serum osmolarity ratio (urine ÷ serum).
- Is urine osmolarity ≈600 mOsmol/L **and** ratio ≥2 **and** urine dipstick negative for glucose?
  - **Yes** → Classify as consistent with central diabetes insipidus.
  - **No** → Consider nephrogenic DI, hyperglycemia‑induced osmotic diuresis, or primary polydipsia; pursue further testing (e.g., water deprivation test, ADH challenge).

## STEP 4 — Decide
- If central DI is confirmed, initiate a therapeutic trial with desmopressin or proceed to formal water deprivation test for definitive diagnosis.
- If DI is not confirmed, investigate alternative etiologies of polyuria based on clinical context.

## Clinical Guardrails / Mimics / Pitfalls
- Do not diagnose DI based on a single urine osmolarity without simultaneous serum; hyperglycemia can artifactually raise urine osmolarity.
- Rule out osmotic diuresis (glucose, mannitol) by ensuring urine dipstick is negative for glucose and serum glucose is normal.
- Primary polydipsia may show low urine osmolarity despite high fluid intake; a water deprivation test helps differentiate.
- Nephrogenic DI presents with high serum osmolarity but inappropriately low urine osmolarity (<300 mOsmol/L) despite ADH administration.
- Avoid using random urine samples; timed collections improve accuracy.

## Concrete Clinical Example
A 65‑kg man reports 4 L/day urine output. Serum osmolarity 302 mOsmol/L, urine osmolarity 610 mOsmol/L, urine dipstick negative for glucose. Ratio = 610/302 ≈ 2.0. Meets criteria for central diabetes insipidus.

**Source:** Hormonal Replacement in Hypopituitarism in Adults: An Endocrine Society Clinical Practice Guideline, Endocrine Society, 2016, DOI:10.1210/jc.2016-2118
> **TODO:** consider adding scripts/calc.py for the ata-di-workup calculator

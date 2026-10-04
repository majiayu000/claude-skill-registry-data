---
name: jes-pa-screening-arr-arc
description: Interprets the aldosterone-to-renin ratio using active renin concentration (ARC) to screen for primary aldosteronism. Triggered when a clinician has PAC and ARC results and asks 'How do I interpret this ARR using active renin concentration?'
---

# Interpret aldosterone-to-renin ratio screening test using PAC/ARC

## STEP 1 — Gather Information
Collect plasma aldosterone concentration (PAC) measured by CLEIA and active renin concentration (ARC) results. Ensure PAC is ≥60 pg/mL for further interpretation.

## STEP 2 — Rule In / Rule Out
Calculate ARR = PAC (pg/mL) / ARC (pg/mL). If ARR ≥40 and PAC ≥60 pg/mL → screen positive for primary aldosteronism. If ARR between 20 and 40 (inclusive) and PAC ≥60 pg/mL → provisionally positive (borderline). If ARR <20 or PAC <60 pg/mL → screen negative.

## STEP 3 — Classify or Stratify
For positive screen (ARR ≥40, PAC ≥60 pg/mL): proceed to confirmatory testing. For provisional positive (ARR 20–40, PAC ≥60 pg/mL): individualized management considering patient desire, age, hypokalemia, adrenal tumors on CT.

## STEP 4 — Decide
If screen positive: order a confirmatory test (e.g., captopril challenge test, saline infusion test). If provisional positive: discuss individualized next steps, which may include repeat testing, confirmatory test, or medical therapy based on risk factors.

## Clinical Guardrails / Mimics / Pitfalls
Do not rely on ARR alone if PAC <60 pg/mL; false negatives may occur. Avoid using plasma renin activity (PRA) conversion factors; the guideline specifies direct ARC use. Be aware that medications like ACE inhibitors, ARBs, calcium channel blockers, and alpha-blockers generally do not affect ARR screening results, but beta-blockers may cause false-positive and diuretics false-negative results.

## Concrete Clinical Example
A 55‑year‑old hypertensive patient has PAC 70 pg/mL (CLEIA) and ARC 1.5 pg/mL. ARR = 70 / 1.5 ≈ 46.7, which is ≥40 and PAC ≥60 pg/mL → screen positive for primary aldosteronism; proceed to confirmatory testing.

**Source:** Japan Endocrine Society clinical practice guideline for the diagnosis and management of primary aldosteronism 2021, Japan Endocrine Society, 2022, https://doi.org/10.1007/s00223-022-00903-9
> **TODO:** consider adding scripts/calc.py for the jes-pa-screening-arr-arc calculator

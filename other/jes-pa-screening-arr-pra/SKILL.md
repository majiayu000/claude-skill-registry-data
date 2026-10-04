---
name: jes-pa-screening-arr-pra
description: Determines if PAC/PRA ratio and PAC levels indicate positive or provisionally positive screening for primary aldosteronism. Triggered when a clinician has PAC and PRA results and asks “Is this screening test positive for PA?” or needs to interpret borderline results.
---

# Interpret aldosterone-to-renin ratio screening test using PAC/PRA

## STEP 1 — Gather Information
Collect plasma aldosterone concentration (PAC) in pg/mL and plasma renin activity (PRA) in ng/mL/h (or active renin concentration ARC in pg/mL/h). Ensure samples are drawn after overnight fasting, seated or supine, and that the patient is on medications that minimize interference (e.g., calcium channel blockers or alpha‑blockers; avoid beta‑blockers, ACEi/ARBs, diuretics if possible). Record units and note any interfering drugs.

## STEP 2 — Rule In / Rule Out
Calculate ARR = PAC (pg/mL) ÷ PRA (ng/mL/h). If ARR ≥ 200 and PAC ≥ 60 pg/mL → screen positive. If ARR between 100–200 and PAC ≥ 60 pg/mL → provisionally positive. If using ARC, calculate ARR = PAC ÷ ARC; positive if ≥40 and PAC ≥60 pg/mL, provisionally positive if 20–40 and PAC ≥60 pg/mL. Otherwise screen negative.

## STEP 3 — Classify or Stratify
Classify result as: Positive screening (ARR ≥200 or PAC/ARC ≥40 with PAC ≥60), Provisionally positive (ARR 100–200 or PAC/ARC 20–40 with PAC ≥60), or Negative (below these thresholds). Note that provisionally positive results require individualized next steps.

## STEP 4 — Decide
If screen positive → proceed to a confirmatory test (e.g., captopril challenge or saline infusion). If provisionally positive → individualize management: consider patient age, hypokalemia, adrenal tumor on CT, desire for further testing, and either proceed to confirmatory test or monitor. If screen negative → consider alternative causes of hypertension; remember that PA is not completely excluded by a negative screen.

## Clinical Guardrails / Mimics / Pitfalls
Avoid false‑positive spikes from beta‑blockers (raise ARR) or false‑negative drops from diuretics (lower PAC). Low PRA (<0.5 ng/mL/h) can inflate ARR; verify renin measurement adequacy. ACE inhibitors, ARBs, and direct renin inhibitors may suppress renin and alter ARR; hold if possible. Ensure PAC assay is CLEIA‑based; if using RIA, apply conversion (≈0.65×). Do not rely solely on ARR without PAC ≥60 pg/mL cutoff.

## Concrete Clinical Example
A 58‑year‑old hypertensive patient has PAC 55 pg/mL and PRA 0.2 ng/mL/h. ARR = 55 ÷ 0.2 = 275, PAC <60 pg/mL → screen negative despite high ARR; advise repeat PAC after correcting for assay cutoff or consider clinical suspicion.

**Source:** Japan Endocrine Society clinical practice guideline for the diagnosis and management of primary aldosteronism 2021, Japan Endocrine Society, 2021

> **TODO:** consider adding scripts/calc.py for the jes-pa-screening-arr-pra calculator

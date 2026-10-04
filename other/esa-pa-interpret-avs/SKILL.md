---
name: esa-pa-interpret-avs
description: Determines unilateral vs bilateral aldosterone excess based on cortisol-corrected aldosterone ratios from adrenal venous sampling, with ratio >4:1 indicating unilateral excess, ratio 3:1 suggestive of bilateral hypersecretion, and interpretation dependent on cosyntropin stimulation protocol used during sampling. Use when analyzing AVS results to guide surgical vs medical treatment decisions; triggers include 'AVS lateralization ratio', 'cosyntropin-stimulated AVS', 'aldosterone-to-cortisol ratio >4:1', and 'ratio 3:1 suggestive of bilateral disease'.
---

# Interpret Adrenal Venous Sampling Results for PA

## STEP 1 — Gather Information
Collect aldosterone and cortisol concentrations from the right adrenal vein (RAV), left adrenal vein (LAV), and a peripheral vein (e.g., cubital or iliac). Document whether cosyntropin stimulation was administered (continuous infusion, bolus, or none) and note patient age, serum potassium, and adrenal CT findings (unilateral lesion, bilateral hyperplasia, or normal).

## STEP 2 — Rule In / Rule Out
Determine if cosyntropin stimulation was used during AVS. If yes, proceed to calculate the high-side/low-side cortisol-corrected aldosterone ratio (higher aldosterone/cortisol divided by lower). If no, proceed to calculate adrenal vein aldosterone/cortisol ratios and compare each to peripheral vein ratio while assessing contralateral suppression (contralateral aldosterone/cortisol not higher than peripheral).

## STEP 3 — Classify or Stratify
If cosyntropin used: a cortisol-corrected aldosterone ratio >4:1 indicates unilateral aldosterone excess; a ratio of 3:1 suggests bilateral hypersecretion; a ratio between 3:1 and 4:1 is indeterminate and requires correlation with clinical setting, CT, and possible repeat AVS. If cosyntropin not used: unilateral disease is suggested when the high-side/low-side ratio >2:1 (or adrenal vein aldosterone/cortisol ratio ≥2.5 times peripheral) with contralateral suppression; bilateral disease is suggested when ratios are similar or lack contralateral suppression.

## STEP 4 — Decide
If unilateral aldosterone excess is confirmed, recommend laparoscopic adrenalectomy of the affected side (surgical cure). If bilateral hypersecretion or indeterminate result, recommend medical therapy with a mineralocorticoid receptor antagonist (e.g., spironolactone) and consider repeat AVS or ancillary tests if indeterminate.

## Clinical Guardrails / Mimics / Pitfalls
Do not rely on AVS if catheterization unsuccessful (especially right adrenal vein); avoid interpreting results without cortisol correction; do not use AVS in patients with low aldosterone levels (<15 ng/dL) as ratios may be falsely elevated; do not overlook contralateral suppression; avoid AVS in patients with uncontrolled hypertension or severe hypokalemia without preparation; do not ignore clinical context (age <35 with spontaneous hypokalemia and unilateral CT lesion may proceed to surgery without AVS); do not mistake CT unilateral nodules for unilateral disease in bilateral hyperplasia.

## Concrete Clinical Example
A 32‑year‑old woman with spontaneous hypokalemia, PAC 32 ng/dL, AVS performed with continuous cosyntropin infusion. Right adrenal vein: aldosterone 1800 ng/dL, cortisol 20 µg/dL (ratio 90). Left adrenal vein: aldosterone 400 ng/dL, cortisol 22 µg/dL (ratio 18.2). Peripheral: aldosterone 10 ng/dL, cortisol 10 µg/dL. High/low ratio = 90/18.2 ≈ 4.9 (>4:1), indicating unilateral aldosterone excess (right side). Laparoscopic right adrenalectomy is recommended.

**Source:** The Management of Primary Aldosteronism: Case Detection, Diagnosis, and Treatment: An Endocrine Society Clinical Practice Guideline, Endocrine Society, 2016, doi:10.1210/jc.2015-4061
> **TODO:** consider adding scripts/calc.py for the esa-pa-interpret-avs calculator

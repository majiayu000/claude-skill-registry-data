---
name: mathodology-award-gates
description: Use when reviewing mathematical validity, evidence, reproducibility, figures or a submission draft.
---

# Mathodology Review Questions

The legacy skill name is retained for discovery. Review the substance of the
work; do not estimate awards from invented numeric thresholds or require a
particular handoff format. Scale review to the claims and the deadline.

## Mathematical and empirical questions

- Does the solution answer every required question and represent its essential mechanisms?
- Are equations, units, constraints and limiting cases consistent? Is the solution feasible?
- Can the parameters be identified from the available observations?
- Does the described method match the code, including preprocessing and exclusions?
- Is a reported advantage measured against an appropriate baseline on comparable data?
- Are fitting, tuning and evaluation separated where the claim requires it?
- Are outcomes forced by normalization or constraints labeled as such?
- Could plausible changes to important assumptions reverse the recommendation?
- Are confidence intervals, predictive intervals and simulation variability distinguished?
- Can reported numbers be traced to data, code, a derivation or a stated assumption?
- Are evidence gaps, failed runs and material limitations disclosed?

Use relevant questions, not every possible test. When scenarios share comparable
random inputs, paired simulations may improve precision; explain the coupling.
Use Monte Carlo uncertainty for estimated probabilities, and disclose the number
of simulations. Do not claim proof from a handful of successful runs.

## Figures and paper

Load [figure presets](../mathodology-figure-presets/SKILL.md). Read figures at the
size used in the final document. Check labels, uncertainty definitions, legends,
color scales and captions against the underlying results. Inspect dense pages
of the compiled PDF as well as individual exports. Image2 imagery must remain
consistent with the mechanism; generated pixels are not quantitative evidence.

The optional [PDF overview utility](scripts/make_contact_sheet.py) requires
Poppler's pdftoppm and Matplotlib. It creates a page overview for visual review:

```bash
python3 .claude/skills/mathodology-award-gates/scripts/make_contact_sheet.py solution.pdf -o overview.png
```

An overview helps find layout problems; zoom into dense pages to judge actual
legibility. A successful render is not a certificate of quality.

## Useful review output

Explain each material issue, its evidence, its effect on the conclusion and a
concrete fix. Distinguish errors from optional improvements. Correct consequential
errors before relying on the result; disclose unresolved uncertainty. Never
require the user to approve routine fixes or invent a scoring ceremony.

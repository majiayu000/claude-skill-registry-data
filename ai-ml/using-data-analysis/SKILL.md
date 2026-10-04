---
name: using-data-analysis
description: Route data analysis and machine learning work to the right skill in this suite. Use when starting any analysis, modeling, validation, or reproducibility task and the matching specialized skill is not yet clear; not needed when one specific skill already clearly applies.
---

# Using Data Analysis Skills

Pick the narrowest skill that covers the current task. When the work spans
multiple lifecycle stages, start from the orchestrator and let it call the
others.

| Situation | Skill |
| --- | --- |
| An end-to-end project or an ambiguous modeling request | `running-decision-grade-data-science` |
| Data meaning, joins, labels, or ground truth may be untrustworthy | `auditing-data-and-ground-truth` |
| Designing splits, feature eligibility, baselines, or comparisons | `designing-leakage-safe-experiments` |
| A metric dropped, results disagree, or training-serving mismatch | `diagnosing-ml-failures` |
| Reviewing whether results support a claim or launch decision | `validating-models-and-claims` |
| Packaging finished work for independent reproduction | `shipping-reproducible-results` |

Each skill states its own non-goals in its description; respect them. The
orchestrator `running-decision-grade-data-science` already routes to the
other five at the right lifecycle stage, so do not stack it with them
manually for the same step.

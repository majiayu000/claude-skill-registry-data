---
name: dataset-audit
description: Audit a dataset and its preprocessing for validity, leakage, licensing, and bias before training or evaluation. Use when a dataset is ingested, merged, transformed, or split.
---

# Dataset Audit

1. Record dataset origin, version, license/terms, collection date, intended use, and permitted redistribution.
2. Inspect schema, counts, labels, missing values, duplicates, corrupt examples, class balance, and sensitive fields.
3. Check train/validation/test separation for entity, time, user, patient, source, or near-duplicate leakage.
4. Review preprocessing and label transformations for information leakage or target contamination.
5. Examine sampling bias, coverage gaps, class imbalance, annotation quality, and subgroup performance risks.
6. Keep raw data immutable; make transformations reproducible and log exclusions.
7. Protect personal, proprietary, and restricted data. Avoid uploading it to unapproved external tools.
8. Produce an audit report with checks, findings, unresolved risks, and a go/no-go recommendation.

Do not assume a public URL means unrestricted use. Do not remove difficult examples merely to improve metrics. Distinguish measured data properties from hypotheses about representativeness.

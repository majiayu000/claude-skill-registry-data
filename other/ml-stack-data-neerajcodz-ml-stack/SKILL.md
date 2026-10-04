---
name: ml-stack-data
description: Inspect local or remote datasets when a user asks about schema, splits, samples, statistics, labels, leakage, privacy, licensing, SFT, DPO, GRPO, or vision annotations; produce a formatter or preprocessor handoff without inventing remote execution.
---

# ML data

Activate for dataset selection, intake, audit, formatting, preprocessing, or leakage review. Require the path or dataset identifier, task/target, split intent, schema expectations, sensitivity, license, and permitted transformations.

## Workflow

1. Inventory schema, row/sample counts, splits, nulls, types, target, time, groups, IDs, duplicates, and representative samples.
2. Check train/validation/test boundaries, temporal and group separation, near-duplicates, label leakage, prompt/completion contamination, and benchmark overlap.
3. Record privacy, PII, secrets, sensitivity, provenance, license, consent, retention, and intended publication boundary.
4. Validate conversation shapes for SFT/DPO/GRPO and annotation contracts for classification, detection, and segmentation.
5. Invoke `ml_stack.audit_data` only for a supported local path. For Dataset Viewer or other remote HF operations, emit a bounded inspection plan with endpoint, revision, fields, and expected outputs; do not claim remote inspection.
6. Hand a versioned formatter/preprocessor contract to `ml-stack-training` and validation exclusions to `ml-stack-experiment`.

## Safety and outputs

Never load untrusted code, reveal sensitive samples, silently drop rows, or rewrite source data. Abstain when provenance, license, target semantics, split identity, or privacy status is unknown. Return measured statistics, sample redactions, leakage findings, decisions, source revision/hash, and exact next owner. Next owner: `ml-stack-training` for formatting and preprocessing, `ml-stack-experiment` for immutable validation design, or `ml-stack-audit` for release review.

See [dataset contracts](references/dataset-contracts.md), [leakage checklist](references/leakage-checklist.md), [training formats](references/training-formats.md), and [remote handoff](references/remote-dataset-handoff.md).

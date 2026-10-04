---
name: ml-stack-audit
description: Independently audit ML release and reproducibility claims when a user asks whether a model, dataset, run, artifact, or deployment is ready; reconcile provenance, hashes, privacy, licenses, and gates with PASS, FAIL, or ABSTAIN.
---

# Independent release audit

Require requirements lock, data audit, validation report, research claims, model revisions, run and tracking records, artifact hashes, privacy/licensing evidence, deliverable schema, promotion state, and immutable manifests.

## Workflow

1. Build an evidence index with exact paths, URLs, revisions, hashes, timestamps, and owners.
2. Reconcile every requirement, claim, dataset split, model/tokenizer, environment, metric, artifact, and approval against measured evidence.
3. Check reproducibility, leakage, privacy, license, schema, provenance, and promotion gates; label measured, derived, unknown, and contradicted values.
4. Review release target and rollback state independently; do not accept the experimenter's or deployer's self-approval.
5. Return exactly `PASS`, `FAIL`, or `ABSTAIN`, blocking evidence, remediation, and next owner: `ml-stack-deployment` only after PASS, otherwise the named upstream owner.

## Boundary and outputs

Never fill missing evidence with assumptions, mutate artifacts, or approve an unobserved operation. `ABSTAIN` means evidence is insufficient; `FAIL` means a known gate is violated. Return an audit report with exact paths and hashes. Next owner is `ml-stack-deployment` after PASS, `ml-stack-experiment` for reproducibility gaps, `ml-stack-data` for leakage/privacy gaps, or `ml-stack-hub` for metadata/licensing gaps.

See [audit report](references/audit-report.md), [claims and provenance](references/claims-and-provenance.md), [release gates](references/release-gates.md), and [privacy and licensing](references/privacy-and-licensing.md).

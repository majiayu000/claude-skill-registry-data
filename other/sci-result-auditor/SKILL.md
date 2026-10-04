---
name: sci-result-auditor
description: Perform read-only consistency and reproducibility audits across experiment cards, raw results, indexes, registries, claim-evidence maps, handoffs, manuscripts, and public artifacts. Use when checking whether claims are supported, metrics and protocols are compatible, results are traceable, or project memory is internally consistent. Return findings to the requester; involve sci-research-manager only for a requested project decision or evidence transition. Repairs are separately authorized, not auditor mutations.
---

# SCI Result Auditor

Audit trustworthiness, traceability, and consistency. Follow project-local rules and the evidence hierarchy in `sci-research-manager`.

## Start narrow

Use the supplied claim/ID/artifact and its relevant protocol first; consult handoff, query map, or index only to resolve missing context. Audit selected claims/IDs when possible; state scope before a broad audit. Reuse unchanged verified context, but reopen decisive raw evidence when an exact claim or conflict requires it.
Do not connect to remote hosts during a local/read-only audit unless the user explicitly requests remote verification.

## Audit experiment evidence

Check:

- stable ID and canonical card;
- raw result, config, command/run path, code commit, dataset/version, split, seeds, metric definition, baseline, and selection rule;
- reproducibility of reported numbers from the cited artifact;
- protocol compatibility and baseline fairness;
- test-set checkpoint/threshold/method selection;
- required controls and competing explanations;
- separation of supports, does-not-support, and confounds.

Never infer a result from a filename or chat summary.

## Audit claims and paper artifacts

Check:

- every claim has evidence and calibrated strength;
- exploratory, diagnostic, trend, source-only, or mismatched evidence is not promoted into a main claim;
- old-route residue and unsupported contribution language are absent;
- figures/tables, manuscript, supplementary material, data/code statements, and public code use canonical compatible results;
- negative boundaries and contrary evidence are disclosed when material.

## Audit files and memory

Check that referenced cards/raw paths exist or are marked missing; experiment IDs resolve across indexes and claim maps; current paper status/handoff agree; archived records point to their replacement; and navigation/provenance checks pass.

Use `scripts/check_project_consistency.py` for the deterministic first pass. It prints a report by default and writes only when `--output` is explicitly supplied.

## Report decisions without repairing silently

For every issue, state severity, evidence, impact, and recommended repair. For each audited result, separate:

- `supports`;
- `does_not_support`;
- `claim_strength`;
- optional `paper_role` or placement when the project records it separately;
- `risk`;
- `next_action`.

Return findings to the current requester; involve `sci-research-manager` when a project decision or evidence transition is requested, not merely to close a direct audit. Do not change route state, promote evidence, or repair canonical artifacts during the audit. Do not recommend larger training merely because evidence is weak or confounded; identify the smallest check that resolves the uncertainty.

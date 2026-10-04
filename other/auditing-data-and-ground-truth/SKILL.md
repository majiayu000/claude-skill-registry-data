---
name: auditing-data-and-ground-truth
description: Audit datasets, joins, labels, and ground truth before analysis or modeling. Use when data meaning, row grain, time semantics, source-of-truth reliability, or label construction may invalidate conclusions; not for general model evaluation after the evidence base is already trusted.
---

# Audit Data and Ground Truth

Determine what the data actually represents and whether its labels can support the intended claim. The outcome is an evidence-backed readiness judgment, not a generic profile report.

## Anchor the audit

State the intended decision, entity, row grain, target, prediction moment, outcome window, and population. If these are not known, surface that uncertainty before interpreting columns or labels.

Preserve source data unchanged. Work from read-only inputs or documented snapshots, and keep every correction, exclusion, or derived label traceable to its source.

## Inspect in risk order

1. **Source and lineage:** Identify origin, owner, extraction time, filters, transformations, versions, and competing sources of truth.
2. **Structure:** Measure row and entity counts, schema, types, key uniqueness, duplicates, missingness, ranges, and category cardinality. Report both counts and rates where scale matters.
3. **Meaning:** Confirm units, code sets, null semantics, sentinel values, event meanings, and whether one row means what the analysis assumes.
4. **Relationships:** Test key uniqueness on each side before joining. State expected and observed cardinality, unmatched rates, row multiplication, and aggregation effects.
5. **Time:** Separate event time, record time, update time, and availability time. Check impossible orderings, late arrivals, backfills, and future knowledge.
6. **Ground truth:** Trace each label from operational event to encoded value. Verify annotator or system provenance, adjudication, label maturity, class definitions, coverage, disagreement, and missing-label behavior.
7. **Reconciliation:** Compare raw records with independent records or a stratified sample. Do not let agreement with a downstream table validate the upstream process that created both.

Read [references/audit-playbook.md](references/audit-playbook.md) when selecting concrete tests or grading the severity of a finding.

## Protect semantics

- Do not silently interpret missing as negative, absence as zero, or the latest value as historically available.
- Do not deduplicate until the real-world uniqueness rule is established.
- Do not repair values in place; produce a derived correction with a reason and impact count.
- Do not accept labels merely because they are named `target`, `truth`, `gold`, or `final`.
- Do not average away disagreements that reveal a definition or annotation problem.

Within already authorized data, systems, and compute, run read-only or reversible tests and document the evidence. Obtain approval before choosing a new source of truth, changing label policy, excluding a material population, applying irreversible corrections, accessing a new or sensitive source, incurring material cost, involving an external reviewer, or sharing records outside the approved boundary.

## Issue a readiness judgment

Use [assets/data-and-ground-truth-audit.md](assets/data-and-ground-truth-audit.md) for the deliverable. For every material finding, record evidence, affected scope, consequence, and recommended treatment. End with one status:

- **ready:** evidence supports the intended use;
- **ready with conditions:** use is supportable only under named constraints;
- **not ready:** a known defect can change the conclusion;
- **unknown:** critical evidence is missing or cannot be independently checked.

Never upgrade `unknown` to `ready` because no defect was observed.

---
name: batch-impact-regression
description: Analyze change impact and combination regression for existing C# batches backed by SQL Server stored procedures. Use when a business requirement changes a batch whose rules, validation, calculations, updates, or combination validity may be split between C# and SQL Server, especially when the candidate space is large and no formal test dataset exists.
---
<!-- xid: 517E99B3082E -->
<a id="xid-517E99B3082E"></a>


# Batch Impact Regression

## Purpose

Establish the existing batch's observed behavior as a baseline, compare the
old and changed versions on the same deterministic inputs, and produce an
evidence-linked report for human business judgment. The Skill controls the
workflow; deterministic scripts generate combinations, apply only explicitly
configured constraints, normalize results, compare outcomes, aggregate counts,
and select a reproducible regression set.

## Required Knowledge (XID)

- [Skill operating contract](../../../../docs/core/contracts/058_skill_operating_contract.md#xid-B7A2C94F0E61)
- [Context direction guard](../../../../knowledge/organization/160_context_direction_guard_rules.md#xid-7A2F4C8D1601)

## Optional References

- [Workflow and decision rules](./references/workflow.md)
- [Configuration schema](./references/config-schema.md)
- [C# and SQL Server analysis checklist](./references/csharp-sql-analysis.md)
- [Adapter boundary](./references/adapter-contract.md)
- [Code table extraction](./references/code-table-extraction.md)
- [Configuration template](./references/config.template.json)

## Inputs and Outputs

Inputs are a configuration file, source locations, safe test-DB execution
details, old/new version selectors, explicit combination values and
constraints, expected differences, and old/new result files or adapters.
Outputs are JSON/CSV candidate and comparison reports, a reduced regression
set, an evidence-backed impact note, unresolved human decisions, and a
release-time full-run procedure. Real batch/DB execution is available only
through an explicitly implemented adapter; fixture mode must be labeled as
fixture mode.

## Workflow

Follow the 15-step sequence in `references/workflow.md` without skipping the
safe-execution gate. Inspect C# and SQL Server as one execution path: trace C#
entry points and parameters into SPs, then trace child SPs, functions, views,
tables, dynamic SQL, transactions, result contracts, and side effects.

Use `scripts/batch_regression.py extract-tables <source-root> -o <report.json>`
to scan C# and `.sql` source for conservative condition evidence, decision
table rows, inferred factor values, and a strength-2 pairwise covering-table
candidate (an orthogonal-table candidate, not a proof of a mathematically
balanced orthogonal array).
Treat `<unknown>` values and all scanner limitations as human-review items.
Use `scripts/batch_regression.py` for deterministic processing. Never send the
full candidate space to the model. Do not infer a business constraint from a
source condition or treat the baseline as business truth.

## Required Classification and Comparison Rules

Keep these outcomes distinct: `baseline_match`, `planned_difference`,
`unexplained_difference`, `business_invalid`, `upstream_absent`, `uncertain`,
`system_error`, and `not_executed`. Normalize only configured non-deterministic
fields. Preserve input, old result, new result, constraint evidence, planned
requirement relation, and C#/SP path references for every difference.

## Human Boundary and Closure

The human decides business validity, whether a baseline defect is accepted,
which planned differences are allowed, and whether unexplained differences
may block release. Stop and escalate when a required rule, dynamic SQL/SP
target, DB side effect, or expected difference lacks evidence. Closure requires
the deterministic report, reduced-set recipe, full-run procedure, all unknowns
and risks resolved or escalated, and an explicit handoff to the business owner
and release/test owner.

## Reporting Contract (共通報告)



- reporting_profile: summary_first

Use the shared [Skill Reporting Contract](../../../../docs/core/contracts/081_skill_reporting_contract.md#xid-6B2D9F4A1C73) in the final report. Start with these headings in this order:

1. Status — done, partial, blocked, or escalated
2. Result — what was produced or decided
3. Evidence — output, evidence, checks, or XIDs
4. Open Items — unresolved unknowns, risks, judgments, or なし
5. Handoff — next owner and next action, or なし

Keep this summary-first section visible before Skill-specific detail; do not omit empty sections.

---
name: batch-impact-regression
description: Analyze change impact and combination regression for existing C# batches backed by SQL Server stored procedures.
---
<!-- xid: 517E99B3082E -->
<a id="xid-517E99B3082E"></a>

# Batch Impact Regression

Use this Skill when a requirement changes an existing C# batch and SQL Server
stored-procedure execution path. Inspect C# and SQL as one execution path,
trace parameters and database dependencies, and keep business constraints
separate from source conditions.

Follow the 15-step workflow in `references/workflow.md`. Use the deterministic
tools in `scripts/` for combination generation, constraint application,
source decision-table extraction, result normalization, comparison, and
regression-set selection. Never send the full candidate space to the model.

```powershell
python scripts/code_tables.py C:\path\to\source -o tables.json
python scripts/batch_regression.py report config.json old.json new.json -o report.json
```

The real batch and database require an isolated adapter. Do not execute against
production. Treat dynamic SQL, unresolved dynamic procedure names, missing
business evidence, and unexplained differences as unknowns requiring human
judgment. The baseline is observed current behavior, not proof of business
correctness.

## Required outputs

- decision table and orthogonal-table candidate
- JSON or CSV regression report
- reduced regression set and reproducible recipe
- C#/SP execution-path evidence
- unknowns and human handoffs

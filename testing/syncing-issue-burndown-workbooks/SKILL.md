---
name: syncing-issue-burndown-workbooks
description: Use when producing a reproducible issue-burndown workbook from a generic local data adapter and validating the resulting spreadsheet.
---

# Syncing Issue Burndown Workbooks

Create a portable `.xlsx` burndown workbook from a local JSON issue snapshot. The reference implementation uses only the Python standard library and synthetic data.

## What this skill does

- Accepts a normalized issue snapshot through a file adapter.
- Calculates total, completed, and remaining work by day.
- Builds an interoperable workbook with `Issues` and `Burndown` sheets.
- Validates the generated workbook structure and writes a report.

## Adapter boundary

The workflow accepts records with `key`, `opened`, `closed`, and `status`. A production connector belongs outside this public skill: translate its response into this schema before calling the workbook generator. Do not include a private system URL, credential, query, field identifier, or raw payload in this repository.

## Workflow

1. Run `python scripts/check_prereqs.py`.
2. Replace the synthetic input only with a sanitized, locally approved normalized snapshot.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Inspect `validation-report.json` and open `synthetic-burndown.xlsx` in a spreadsheet application.
5. Run the repository leakage scan before packaging or sharing the skill.

## Data rules

- Use ISO dates (`YYYY-MM-DD`) and one of `Open`, `Blocked`, or `Done`.
- Use synthetic keys such as `DEMO-100` in public examples.
- Omit names, customer data, descriptions, comments, attachments, and source-system metadata from public fixtures.

## Validation

```powershell
python -m unittest discover -s skills/syncing-issue-burndown-workbooks/tests -t skills/syncing-issue-burndown-workbooks -v
```

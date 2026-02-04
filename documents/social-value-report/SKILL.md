---
name: social-value-report
description: Generate the social value report from CSV inputs by detecting CSVs, anonymising them, and producing a month-by-month markdown report.
---

# Social Value Report

Use this skill when the user asks to produce or refresh the social value report.

## Workflow

1) **Locate CSV data**
- List CSV files in the current directory.
- If none exist, ask the user to provide the latest dataset.
- If any CSV files lack the timestamp pattern (`YYYYMMDD_HHMMSS`), anonymise them before proceeding.

2) **Anonymise input**
- Use the anonymise skill to strip PII and timestamp the file
- The anonymise skill auto-detects new CSVs or accepts a specific filename
- Confirm the timestamped file was created and the original removed.

3) **Generate the report**
- Run the report generator (defaults to the newest anonymised CSV if none is specified):
  - `python3 skills/social-value-report/report.py [path/to/anonymised.csv]`
- This produces `social-value-YYYY-MM-DD.csv` (dated) with one row per month and prints a console summary.
 - Column mappings are read from `config/social-value-report.json` (no hard-coded headers).

4) **Deliver results**
- Share key findings and point to `social_value_report.md`.
- Flag if no records are found.
- Keep output in British English and avoid reintroducing PII.

## Notes
- Counting rules:
  - Programme type **25** → Apprentices (counted).
  - Programme type **32** with funding indicator **2** → sponsored Skills Bootcamp (counted in its own column for reference only).
  - Programme type **32** with any other funding indicator → Skills Bootcamp (social value).
- Each record is counted for every month overlapping its start/end dates (end missing → treated as ongoing to today).
- Column selection prefers **aim 2** fields (start date, end date, programme type, funding indicator) and falls back to aim 1 if aim 2 is missing.
- Column names are supplied via `config/social-value-report.json`; update that file if headers change.
- Platform-agnostic; no vendor-specific commands.
- Uses the anonymised dataset only.
- If multiple new CSVs are present, ask which to use before anonymising.

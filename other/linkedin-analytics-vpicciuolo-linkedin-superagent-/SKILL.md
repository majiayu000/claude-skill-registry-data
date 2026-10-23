---
name: linkedin-analytics
description: Analyze a LinkedIn content export or pasted performance table, compare normalized metrics, find patterns, and recommend experiments. Use for CSV analytics, post performance, content audits, monthly reviews, or deciding what to repeat and stop.
license: MIT
metadata:
  version: "2.2.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# LinkedIn analytics

Read `../../references/session-and-safety.md`,
`../../references/content-system.md`, and
`../../references/analytics-schema.md`.

Inspect the available columns before analyzing. Ask for the user's goal and
follower baseline when relevant. Preserve blanks as unknown.

When a CSV is available, run:

```text
python <plugin-root>/scripts/oyyo_linkedin.py analytics <csv-file>
```

Add `--followers N` only when the user supplied a valid baseline. Use `--json`
when another workflow needs structured output.

Report:

- date range, sample size, missing fields, and excluded rows;
- medians, ranges, and averages;
- top and bottom posts by goal-relevant normalized metrics;
- patterns by pillar, format, or hook only when sample sizes support them;
- anomalies and alternative explanations;
- two or three next experiments with decision rules.

Correlation is not causation. Do not claim that day, time, length, or format
caused a result from a small observational sample.

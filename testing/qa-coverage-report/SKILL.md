---
name: qa-coverage-report
section: pipeline
description: "Reads issues.jsonl after the audit, writes coverage-report.json, and prints a terminal summary. Does NOT write a markdown file."
---

# qa-coverage-report

Reads all issues from `.tmp/qa-<run-id>/issues/`, deduplicates, writes a compact JSON report, and prints a terminal summary. No markdown file is written.

## On Activation

1. Scan `{project-root}/.tmp/qa-<run-id>/issues/` for all `.jsonl` files
2. Parse every JSON line → deduplicate by `issueId` (keep first occurrence)
3. Read `qa-state.json → chronicIssues`
4. Read `audit-plan.json` for the full cell list (for coverage counts)

## Write JSON Report

Write `{project-root}/.tmp/qa-<run-id>/coverage-report.json`:

```json
{
  "runId": "qa-20260520-abc1",
  "completedAt": "ISO-8601",
  "cellsTotal": 60,
  "issuesTotal": 35,
  "bySeverity": { "critical": 0, "high": 12, "medium": 15, "low": 8 },
  "bySkill": { "qa-detect-overflow": 3, "qa-test-navigation": 2 },
  "bugsFiledCount": 12,
  "chronicIssuesCount": 2,
  "coverage": [
    { "route": "/dashboard", "mobile": 1, "tablet": 0, "desktop": 0 }
  ]
}
```

## Print Terminal Summary

Print this to stdout — this is the only output shown to the user:

```
┌────────────────────────────────────────────────────────────┐
│  Argus — Run Complete                                      │
├────────────────────────────────────────────────────────────┤
│  Run        : {runId}                                      │
│  Cells      : {cellsRun} / {cellsTotal}                    │
│  Routes     : {routeCount}                                 │
├────────────────────────────────────────────────────────────┤
│  Issues                                                    │
│    Critical : {critical}                                   │
│    High     : {high}                                       │
│    Medium   : {medium}                                     │
│    Low      : {low}                                        │
│    Total    : {issuesTotal}                                │
├────────────────────────────────────────────────────────────┤
│  Bugs filed : {bugsFiledCount}                             │
│  Report     : .tmp/{runId}/coverage-report.json            │
│  Screenshots: .tmp/{runId}/screenshots/                    │
└────────────────────────────────────────────────────────────┘
```

If `chronicIssues.length > 0`, append after the box:

```
Chronic ({n} issues seen 3+ consecutive runs):
  • {description} — {route} ({seenCount} runs)
```

## Rules

- Severity order in `bySeverity`: critical → high → medium → low
- `bugsFiledCount` = count of issues where `adoWorkItemId` is present and non-null
- Coverage cell value = count of issues on that route+viewport combination

## Paths

| Artifact | Path |
|---|---|
| Issues | `{project-root}/.tmp/qa-<run-id>/issues/**/*.jsonl` |
| Audit plan | `{project-root}/.tmp/qa-<run-id>/audit-plan.json` |
| Run state | `{project-root}/.claude/qa-state.json` |
| Output | `{project-root}/.tmp/qa-<run-id>/coverage-report.json` |

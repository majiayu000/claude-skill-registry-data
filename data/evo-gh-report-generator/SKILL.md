---
name: evo-gh-report-generator
description: Computes community pulse metrics from raw PR and issue data and writes a structured report.json file. Calculates PR counts by state, average time-to-merge, top contributor, bug issue counts, and resolved bugs. Use when you need to generate GitHub repository health metrics reports.
---

# evo-gh-report-generator

Processes fetched PR/issue data to compute all required metrics and serialize results to report.json.

## Key Concepts

- PR states: REST API returns state as 'open'/'closed' with separate 'merged' boolean
- Time-to-merge: measured from created_at to merged_at in days, rounded to 1 decimal
- Top contributor: person who opened the most PRs (by user.login)
- Bug detection: any issue where at least one label name contains substring 'bug' (case-insensitive)
- Resolved bugs: bug issues where state == 'closed'
- closed PRs: PRs with state 'closed' that are NOT merged (merged == false)

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-gh-report-generator/scripts')
from utils import compute_pr_metrics, compute_issue_metrics, generate_report

# prs = list of PR dicts from GitHub REST API
# issues = list of issue dicts from GitHub Search API

pr_metrics = compute_pr_metrics(prs)
issue_metrics = compute_issue_metrics(issues)
report = generate_report(pr_metrics, issue_metrics, "/app/report.json")
```

## Functions

- `is_bug_issue(issue_data)` - Check if issue has a bug label
- `identify_top_contributor(prs)` - Find top PR author by count
- `compute_pr_metrics(prs)` - Compute total/merged/closed/avg_merge_days/top_contributor
- `compute_issue_metrics(issues)` - Compute total/bug/resolved_bugs
- `generate_report(pr_metrics, issue_metrics, output_path)` - Write report.json

## Output Format

```json
{
  "pr": {
    "total": <int>,
    "merged": <int>,
    "closed": <int>,
    "avg_merge_days": <float>,
    "top_contributor": <str>
  },
  "issue": {
    "total": <int>,
    "bug": <int>,
    "resolved_bugs": <int>
  }
}
```

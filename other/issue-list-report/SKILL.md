---
name: issue-list-report
description: Create a well-formatted local report for a provided list of issues.
compatibility: opencode
metadata:
  audience: issue-tracking
  purpose: list-reporting
---
# Issue list report generation

## What I do

- maintain the requested local issue list document using the issue list document content format below
- remove issues that are no longer open or have been assigned to others
- tag issues with a PR submitted note when a fix has been submitted
- strike through issue text when fixes have been submitted if the workflow expects that representation

## When to use me

Use this after querying the issue tracking system for a list of issues and generating a local report.
Use this after finding that an issue is no longer available because it was cancelled or assigned to someone else.
Use this after proposed fixes are generated and submitted as a PR.

## Guidelines

- understand the format before generating the output
- keep the report concise and easy to scan
- prefer high-signal issue summaries over tracker noise

## Issue list document content format

```markdown
# [issue list report name]

Generated: [date and time] | Total issues: [total count]
Filter: [friendly description of filter and sort]

## Highlights

- Total issues: [total issue count]
- New today: [count of issues created in the last 24 hours]
- [severity name]: [count]
- [severity name]: [count]

## Issue List

### [issue id] - [title]
Severity: [severity name] | Reporter: [reporter] | Created: [date created] | Age: [days open]
[one or two sentence description of the issue and any notes or important information in the comments or history that seems helpful]
```

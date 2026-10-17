---
name: report-deep
description: Create a detailed deep report across every dimension with a 7-column table and 4-part summary
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - deep-analyze
  - report
  - suggest-next-action
  - update-docs

---

## Goal

Create a detailed, actionable, and complete deep report with a 7-column table and a 4-part summary

## Scope

Use to create a deep report after reviewing a codebase or analyzing a system — reporting detailed findings. Not used to create or update analyzers

## Execute

### 1. Gather Data

> Goal: collect data from review workflows and codebase analysis

1. Use `/deep-review-codebase` to analyze the codebase across every dimension
2. Use `/deep-analyze` for deeper analysis if additional data is needed
3. Gather findings from review results and codebase analysis
> Goal: complete data from review workflows and codebase analysis

### 2. Classify Findings

> Goal: classify findings to prepare table data

1. For each finding from review results:
   1. Set Scope: `Domain > Category` (e.g. `Code & Architecture > Completeness`)
   2. Set File: the file and line with the issue (e.g. `apps/website/src/routes/__root.tsx:26`)
   3. Analyze Cause: root cause of the problem
   4. Set Solutions: actionable and specific fixes
   5. Set Severity: Critical > High > Medium > Low
   6. Set Review Workflow: the `/review-*` workflow from AGENTS.md
   7. Identify Evidence: the code snippet or pattern that triggered the finding
2. False positive → note in the Cause column: `False positive: <reason>`
3. Sort by severity: Critical first, then High
> Goal: every finding has all column data filled with root cause analysis

### 3. Build Report Table

> Goal: create the deep-report table per the 7-column format

1. Use `/report` to format the table
2. Create a table with 7 columns: Scope, File, Cause, Solutions, Severity, Review Workflow, Evidence
3. Group by `reviewWorkflow` to link to `/review-*` workflows from AGENTS.md
4. Within each group, sort by severity: Critical first, then High
5. Filter to show only categories with findings (don't show pass)
6. Every row must have verifiable evidence
> Goal: table grouped by review workflow with verifiable evidence

### 4. Build Deep Summary

> Goal: create a comprehensive 4-part summary at the end of the report

1. Domain Breakdown — score and status for every domain:
   - User-Facing, Security & Compliance, Backend & Data, Infrastructure, Code & Architecture
   - Per domain: score %, pass/warn/fail counts, top finding
2. Severity Distribution — finding count by severity:
   - Critical, High, Medium, Low
   - Compare with the previous run (if data exists)
3. False Positive Analysis — summary of false positives found and fixed:
   - List of findings that are false positives
   - Root cause for each false positive
   - Fix applied
4. Recommended Actions — action items prioritized:
   - Quick wins: low effort, high impact
   - Major improvements: high effort, high impact
   - Per action: recommended reviewWorkflow, estimated effort, expected impact
> Goal: 4-part summary covering every dimension and leading to action

### 5. Suggest Next Actions

> Goal: recommend next actions based on findings

1. Use `/suggest-next-action` per the prioritized findings
2. Recommend the `/review-*` workflow for each finding based on the `reviewWorkflow` field
3. Recommend `/update-agents-md` if AGENTS.md doesn't match current dependencies
> Goal: clear action items prioritized

## Rules

### 1. Table Columns

The deep-report table has 7 columns in order:

| Column | Description | Required |
|---|---|---|
| Scope | `Domain > Category` where the issue was found | Yes |
| File | File and line with the issue | Yes |
| Cause | Root cause of the problem | Yes |
| Solutions | Actionable and specific fixes | Yes |
| Severity | Critical > High > Medium > Low | Yes |
| Review Workflow | `/review-*` workflow from AGENTS.md | Yes |
| Evidence | Code snippet or pattern that triggered the finding | Yes |

### 2. Grouping

- Group by `reviewWorkflow` to link to `/review-*` workflows
- Within each group, sort by severity: Critical first, then High
- Use headers for grouping per `/report`

### 3. Evidence Requirement

- Every row must have verifiable evidence
- Evidence must be a code snippet, grep output, or the pattern that triggered the finding
- No verifiable evidence → state `Manual review required`

### 4. False Positive Handling

- False positive → note in the Cause column: `False positive: <reason>`
- Note the fix in the Solutions column: `Fixed: <what was changed>`
- Include in the False Positive Analysis section of the deep summary

### 5. Root Cause Analysis

- The Cause column must be root cause, not a symptom
- False positive → explain why the analyzer was wrong
- Real issue → explain what the code does wrong and why

### 6. Solutions Quality

- The Solutions column must contain actionable and specific fixes
- Never use generic advice like "improve code quality"
- Name the file and function to fix when possible

### 7. Summary Completeness

- The deep summary must have all 4 parts: Domain Breakdown, Severity Distribution, False Positive Analysis, Recommended Actions
- Missing data for a part (e.g. no false positives) → state `None found`
- Use /update-docs if needed


- Final report via `/report-review` — one chat table (No./Action/Evidence/Severity/Risk/Priority/Owner skill/Status), no report files

## Expected Outcome

- A 7-column deep-report table with verifiable evidence
- 4-part summary: Domain Breakdown, Severity Distribution, False Positive Analysis, Recommended Actions
- Grouped by `reviewWorkflow` from AGENTS.md
- Every finding has root cause analysis and actionable solutions
- Action items prioritized: quick wins first, major improvements next

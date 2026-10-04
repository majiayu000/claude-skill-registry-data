---
name: review-changes
description: Review all uncommitted changes in the current repo and produce a structured code review report.
whenToUse: When the user asks to review their changes, check their code, or wants feedback before committing.
context: fork
allowedTools:
  - Bash
  - Read
  - Grep
---

## Task

Review all uncommitted changes in the current Git repository and produce a structured code review report.

## Steps

1. Run `git diff --stat` to get an overview of changed files
2. Run `git diff` to get the full diff content
3. For each changed file, read enough surrounding context to understand the change
4. Analyze each change for:
   - **Correctness**: Logic errors, off-by-one, null/undefined risks, race conditions
   - **Style**: Naming, formatting, consistency with surrounding code
   - **Performance**: Unnecessary allocations, missing caching, N+1 queries
   - **Security**: Input validation, injection risks, credential exposure
   - **Maintainability**: Missing error handling, unclear intent, missing types

## Output format

Return a markdown report with this structure:

### Summary

One paragraph overview: how many files changed, what the changes do at a high level, overall assessment (looks good / needs attention / has issues).

### File-by-file review

For each file with findings:

- **File path** and brief description of what changed
- Specific findings as bullet points, each with severity (🟢 nit / 🟡 suggestion / 🔴 issue)
- Include the relevant code snippet when pointing out an issue

### Verdict

A final one-line recommendation: "Ready to commit", "Consider addressing N issues first", or "Needs revision".

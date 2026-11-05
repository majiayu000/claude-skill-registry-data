---
name: assessing-code-health
description: Run linters/typecheckers to calculate health score.
phase: 10 (Compliance)
role: Reviewer
---

# Assessing Code Health

**Role Constraints:** Reviewer (STRICTLY READ-ONLY for application code). You MAY NOT modify, fix, or write to application source code.
**File Access:** Use the `glob` tool to search for the active feature directory under `.jonggrang/.output/features/`. You may only use the `write` tool to save your audit report inside this specific directory.

## Objective
Run read-only static analysis tools (linters, typecheckers, etc.) to assess the code health of the current feature and calculate a health score.

## Execution Steps

1. **Information Gathering:**
   - Find the active feature directory using `glob`.
   - Identify the project's build and linting commands (e.g., `package.json` scripts like `npm run lint`, `tsc --noEmit`).
2. **Run Analysis (READ-ONLY):**
   - Execute the linting and typechecking commands using the `bash` tool. 
   - DO NOT run commands that auto-fix or format code (e.g., do not use `--fix`).
   - Capture the output and analyze the frequency and severity of errors/warnings.
3. **Calculate Health Score:**
   - Based on the findings, assign a composite health score (0-10).
   - Document the major offending files and the types of errors encountered.
4. **Generate Report:**
   - Write the results and the calculated health score to `.jonggrang/.output/features/<active-feature-dir>/health-report.md` using the `write` tool.

## Completion Signal
When the health assessment report is saved, output exactly:

HEALTH_ASSESSMENT_COMPLETE

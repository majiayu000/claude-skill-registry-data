---
name: input-validation-audit
description: "Input validation audit: statically detects all input surfaces (HTTP params, CLI args, env vars, file reads, stdin) across a codebase, classifies their validation state (none/weak/adequate), and flags high-risk gaps. Produces an evidence-backed report with severity, location, and remediation suggestions. Read-only. Trigger: /input-audit"
trigger: /input-audit
---

## What this is for

Every external input crosses a trust boundary. HTTP request parameters, CLI
arguments, environment variables, file contents, and stdin are untrusted until
validated. In practice, validation is often missing, inconsistent, or applied
too late.

This skill finds every input surface in a codebase and checks whether validation
exists nearby. It combines a deterministic collector (regex-based detection of
8 surface types across 10 languages) with LLM context analysis that validates
each finding, filters false positives, and produces an actionable report.

**Audience:** Senior > Vibe
- Seniors use it as a systematic pre-release validation gap audit and a way to
  prove that all external inputs are accounted for.
- Vibe-coders get an automatic safety net: the LLM explains what's at risk and
  how to fix it, so every finding is a learning opportunity.

### Trigger: `/input-audit`

Intervention-free static analysis. The collector reads only - never writes,
never executes the target code, never connects to a network.

## PROTECTION RULE - never `~/.claude/`

This skill analyzes foreign projects. It is read-only. The protection guard
is still active: if the skill ever gets a write mode, target path validation
must be implemented.

## What You Must Do When Invoked

### Step 1 - `-help`/`-h` check
If invoked with `-help` or `-h`, print the usage block below and stop.

### Step 2 - Confirm `-ProjectDir`
If not provided, prompt the user. Confirm the path exists. Print:
`Input validation audit on <path> ...`

### Step 3 - Run Collector
```powershell
& .\scripts\input-scan.ps1 -ProjectDir "<path>"
```

Parse the JSON output. If exit code != 0, report error and stop.

### Step 4 - Validate Each Finding
For each finding in the JSON:
1. Read the `context` block (5 lines around the surface line).
2. Determine if this is a **true positive**, **false positive**, or **uncertain**.
3. Assign confidence: `proven`, `likely`, `suspected`.
4. For `env-var` surfaces with hardcoded fallback values: check if the fallback
   constitutes validation (e.g., `port = process.env.PORT || 3000` is not real
   validation - it only provides a default, not a format check).
5. For `sql` sink surfaces: confirm the SQL query is indeed parameterized or
   concatenated with the input.

### Step 5 - Consistency Analysis
Group findings by parameter name across different files. Flag when:
- Same field (e.g., `email`, `userId`) validated in one handler but not another
- Different validation approaches for semantically equivalent fields

### Step 6 - Produce Report
Write `input-validation-report.md` to the working directory:

```
# Input Validation Report - <project-name>

## 1. Summary
- <count> input surfaces: <n> unvalidated, <m> validated
- <p> high-severity, <q> medium-severity, <r> low-severity

## 2. Critical Gaps (high severity + unvalidated)
| # | File | Line | Surface | Sink | Context |
|---|---|---|---|---|---|
| 0 | src/api/users.ts | 42 | req.body.email | sql | ... |

## 3. Medium Gaps
Grouped by surface type: http-query, http-body, env-var, etc.

## 4. Low / Informational
Validated surfaces with risky patterns (env fallback, type coercion only).

## 5. Consistency Issues
Same field name, different validation across handlers.

## 6. Validation Patterns Catalog
Libraries and approaches found: Joi, Zod, typeof checks, etc.

## 7. False Positives Removed
Each dismissed finding with reason.

## 8. Open Questions
Uncertain findings needing manual review.
```

## Usage

```powershell
# Full scan
& .\scripts\input-scan.ps1 -ProjectDir "C:\Projects\my-api"

# Scan with severity threshold
& .\scripts\input-scan.ps1 -ProjectDir "C:\Projects\my-api" -MinSeverity high

# Scan specific extensions only
& .\scripts\input-scan.ps1 -ProjectDir "C:\Projects\my-api" -Extensions "*.js,*.ts"

# Exclude test files
& .\scripts\input-scan.ps1 -ProjectDir "C:\Projects\my-api" -Exclude "test,spec,fixture"
```

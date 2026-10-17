---
name: healthcheck-mapper
description: "Healthcheck mapper: inventory all health/readiness/liveness endpoints, map against service dependencies, LLM judges each as adequate/weak/missing. Read-only. Trigger: /healthcheck"
trigger: /healthcheck
---
# /healthcheck

Most healthchecks return 200 even when the DB is down. This skill audits coverage and quality.

## What this is for

- Generic `/health` that doesn't check actual dependencies
- Missing readiness probes, inconsistent check coverage across services
- Liveness vs readiness confusion
- **Read-only skill.** No endpoint modification, no deployment changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/healthcheck -help` or `/healthcheck -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/healthcheck-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read each health endpoint:

- Does it check all critical dependencies (DB, cache, external API)?
- Is there a false-sense-of-security endpoint (always 200)?
- Is liveness vs readiness properly separated?
- What failure modes are covered?

### Step 5 - Write report

File `healthcheck-report.md` in current working directory:

1. **Summary** - total endpoints, adequate, weak, missing.
2. **Endpoint table** - per endpoint: path, type, checked deps, missing deps, assessment.
3. **Per-service recommendations** - what each endpoint should check.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight weakest endpoints.

## Usage

```
/healthcheck               # interactive
/healthcheck <dir>         # scan project
/healthcheck -help
```



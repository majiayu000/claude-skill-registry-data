---
name: env-drift-tracker
description: "Env drift tracker: compare config values across environments (dev/staging/prod), LLM flags each difference with risk assessment. Read-only. Trigger: /env-drift"
trigger: /env-drift
---
# /env-drift

Config values that differ between environments are the #1 cause of 'works on my machine'. This skill finds dangerous drifts.

## What this is for

- Feature flag in dev but missing in prod
- DB pool size 5 in staging, 100 in prod - hiding a leak?
- Stripe API key pointed at test in production
- **Read-only skill.** No config modification, no environment changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/env-drift -help` or `/env-drift -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/env-diff.ps1" -ProjectDir "<path>"
```

### Step 4 - Analysis

Read each config drift:

- Is this intentional? (Different log levels, different DB hosts)
- Or dangerous? (Different secret values, missing required keys)
- Risk level: safe / review / critical

### Step 5 - Write report

File `env-drift-report.md` in current working directory:

1. **Summary** - total keys, drifts, safe/review/critical counts.
2. **Drift table** - critical first. Per key: values per env, missing envs, risk, recommendation.
3. **Consistent keys** in appendix (candidates for defaults).
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight critical drifts.

## Usage

```
/env-drift               # interactive
/env-drift <dir>         # scan project
/env-drift -help
```



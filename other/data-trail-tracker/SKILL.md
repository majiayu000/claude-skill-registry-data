---
name: data-trail-tracker
description: "Maps PII fields and their sinks - logs, third-party APIs, exports - purely via field names, never via actual data. Trigger: /data-trail-tracker"
trigger: /data-trail-tracker
---
# /data-trail-tracker

## What this is for

"Where is all the personal data?" - the GDPR question no team can fully answer.
This skill scans code for PII field patterns (email, iban, phone, address,
etc.) in model definitions and traces where those fields flow to logs,
external APIs, exports, storage, and deletion sites.

Scans codebase for PII field candidates (email, iban, phone, address, etc.) in
TS/JS, SQL, and Prisma model definitions, then traces where those fields flow:
log statements, external API calls, file exports, storage writes, and
deletion/anonymization signals.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` or `-h` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/pii-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output and maps each PII candidate to its sinks,

### Step 5

identifies gaps (PII defined but unsinked), and assesses deletion

### Step 6

readiness.

### Step 7

5. Write `data-trail-report.md` to the working directory.

## Usage

```
/data-trail-tracker                    # interactive, prompts for directory
/data-trail-tracker <dir>              # scan project directory
/data-trail-tracker -help              # show usage
```

Returns JSON with `piiCandidates` (structure, field, file, source) and `sinks`
(log, external, export, storage, deletion).

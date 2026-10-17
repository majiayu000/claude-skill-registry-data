---
name: timebomb-scanner
description: "Time bomb scanner: finds hardcoded dates, expiry deadlines, cert references, 32-bit time usage and 'temporary' markers rotting since years (git age via blame), then has the LLM classify each finding as live bomb / rotten provisional / false alarm and produce a defusal list ranked by detonation date. Read-only. Trigger: /timebomb"
trigger: /timebomb
---
# /timebomb

Every codebase ticks. This one tells you when. Finds hardcoded
expiry dates, expiry keywords, rotten "temporary" markers (with
git age) and 32-bit time suspicion - prioritized by detonation date.

## What this is for

- Hardcoded years, coupon deadlines, "// temporary, will be removed next week"
  from years ago - these bombs remain invisible because they are scattered and
  only explode on detonation day.
- **Read-only skill.** No automatic defusal, no certificate file parsing (only
  paths/mentions), no external expiry registries.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/timebomb -help` or `/timebomb -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Record today's date (reference for "overdue").
Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/timebomb-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each finding in context (if unclear, check the file location via Read):

- **Live bomb**: behavior changes on a concrete date. Name the detonation date;
  if in the past: **overdue** (highest priority - the bomb may have already
  exploded, describe possible symptom).
- **Rotten provisional**: `rotten` marker - what was the author's intent, what
  is the risk of the permanent state (blame date as evidence).
- **False alarm**: year in copyright, test data, token limits (e.g.
  `maxOutputTokens: 2048`), changelog - sort out, list in appendix. The
  collector deliberately reports broadly (even isolated years without
  comparison context); sorting them out is the core task here, not a side note.
- **32-bit findings**: only report if the type actually stores time
  (`suspected` when uncertain).

### Step 5 - Write report

File `timebomb-report.md` in the current working directory:

1. **Summary** - count: overdue / ticking / rotten.
2. **Defusal list** - sorted: overdue first, then by detonation date ascending,
   then provisionals by age descending. Per finding: class, detonation date or
   age, evidence (`file:line`, blame date), concrete defusal suggestion.
3. **False alarms** in appendix.
4. **Open questions**.

Evidence requirement: detonation date only from the literal, age only from
blame; no estimated date without `suspected` label.

### Step 6 - Summarize

State the report path, summarize overdue findings first.

## Usage

```
/timebomb               # interactive
/timebomb <dir>         # scan project
/timebomb -help
```



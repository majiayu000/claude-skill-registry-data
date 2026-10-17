---
name: dependency-graveyard
description: "Dependency graveyard: inventory every dependency, check registry health metadata, then LLM judges each as healthy/aging/zombie/dead. Read-only. Trigger: /dep-graveyard"
trigger: /dep-graveyard
---
# /dep-graveyard

Every project has dead dependencies. This skill inventories them and classifies each by life-cycle status.

## What this is for

- Packages with no recent commits, no downloads, unmaintained for years
- CVEs without fix, deprecated API versions, no migration path
- **Read-only skill.** No package removal, no lockfile update, no automated remediation.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/dep-graveyard -help` or `/dep-graveyard -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/dep-inventory.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each dependency in context:

- **Healthy**: actively maintained, recent releases, responsive to issues
- **Aging**: maintained but slow, no new features, stable API
- **Zombie**: no activity but stable API, no CVEs, works as-is
- **Dead**: abandoned, CVEs unfixed, no migration path, deprecated

### Step 5 - Write report

File `dependency-report.md` in current working directory:

1. **Summary** - counts per classification, total deps, critical count.
2. **Priority action list** - dead first, then zombie with CVEs. Per dep: name, current version, latest, last publish, classification, evidence, recommendation (update/fork/migrate/accept).
3. **Healthy deps** in appendix for completeness.
4. **Open questions**.

### Step 6 - Summarize

State report path, highlight dead deps with CVEs.

## Usage

```
/dep-graveyard               # interactive
/dep-graveyard <dir>         # scan project
/dep-graveyard -help
```



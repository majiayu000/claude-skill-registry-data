---
name: tech-debt-narrator
description: "Tech-debt narrator: finds suppress comments, TODOs, empty catches, workarounds, legacy imports, and type-loosening patterns. Clusters them into logical groups and narrates repayment strategies with effort estimates. Collector scans for 6 debt types with file-level git age; LLM clusters, narrates, and estimates. Read-only. Audience: Senior. Trigger: /tech-debt"
trigger: /tech-debt
---

## What this is for

`eslint-disable`, TODO from 2019, empty catches, `as any` - listed as a flat checklist they are noise. Clustered by logical group they become actionable: "auth-middleware has 3 related debt items, fixing them together costs S not M." This skill finds, clusters, and narrates a repayment strategy.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/debt-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding in `debts[]`:

### Step 5

- **Suppress/todo/empty-catch/workaround/legacy/type-loosen**: is this genuine debt or legitimate usage? (`@ts-ignore` next to a known-unsound interop vs one hiding a type error).

### Step 6

5. Cluster debts into logical groups (e.g. all items in `auth-middleware` that touch the same function). Per cluster:

### Step 7

- **Narrative description**: what is the debt, why was it introduced, what breaks if not fixed.

### Step 8

- **Repayment strategy**: refactor / rewrite / retire.

### Step 9

- **Estimated effort**: S / M / L.

### Step 10

6. Write `tech-debt-report.md` to the working directory.

## Usage

```
/tech-debt                           # interactive
/tech-debt <dir>                     # scan project
/tech-debt -help                     # show usage
```

Returns JSON with `debts[]` (file, line, type, text, ageDays, severity), `counts{}` plus cluster hints.

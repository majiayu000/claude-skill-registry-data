---
name: invariant-miner
description: "Invariant miner: scans for code signals that imply hidden invariants (array[0] without guards, division by computed values, JSON.parse assumptions, Async state-readiness patterns) and presents them to the LLM with context for each. The LLM extracts invariant sentences and judges guaranteed-by-construction vs fragile. Read-only. Audience: Senior. Trigger: /invariants"
trigger: /invariants
---

## What this is for

Every function body relies on implicit invariants nobody wrote down:
"list is never empty here", "id is always positive", "config is loaded
by now". Daikon mines invariants dynamically from execution traces.
This skill mines them STATICALLY from code structure: array-index without
bounds check, division by computed values, JSON.parse without schema
validation, async-state expectations.

Each signal the collector finds becomes a candidate invariant sentence. The
LLM judges whether the assumption is guaranteed-by-construction or fragile
and proposes an assertion or doc comment to make the implicit explicit.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/assumption-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each signal:

### Step 5

- Read the `context` lines.

### Step 6

- Formulate the implicit invariant as a sentence.

### Step 7

- Judge: `guaranteed-by-construction` / `probably-holds` / `fragile`.

### Step 8

- For `fragile` signals: propose a guard (assertion) or doc comment.

### Step 9

5. Write `invariant-report.md` to the working directory.

## Usage

```
/invariants                       # interactive
/invariants <dir>                 # scan project directory
/invariants -help                 # show usage
```

Returns JSON with `signals[]` (kind, subject, expression, context, file, line)
plus summary counts.

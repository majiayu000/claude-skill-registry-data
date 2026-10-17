---
name: api-footgun-reviewer
description: "API footgun reviewer: harvests exported function/method signatures, flags boolean-trap positions (multiple bare bool params in a row), same-type-adjacent swaps (from/to, save/loadUntil), and inconsistent family conventions (create*/update* with different param orders or arities). Read-only. Audience: Senior > Vibe. Trigger: /footguns"
trigger: /footguns
---

## What this is for

Internal APIs are the ones we use daily and have full control of - that is
exactly why they grow footguns. Boolean trap: `saveFile(overwrite, verbose)`
with two bare bools. Same-type swap: `send(from, to, subject)` where from/to
are interchangeable by mistake. Inconsistent family: `createThing(a, b, c)`
versus `createThingPrefixed(a, b, c, d)` with different param orders that
look identical at the caller.

Spectral and API-design linters exist for public REST APIs. None of them
catch in-code function-signature footguns. This skill does.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/signature-harvest.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- Is this distinction intentional (e.g., from this library for type

### Step 6

safety) or a real footgun?

### Step 7

- Check call sites. How many places invoke this with the bare-bool or

### Step 8

adjacent-type ambiguity? Higher count = higher severity.

### Step 9

- For inconsistent family: is the order alphabetical, type-grouped,

### Step 10

or just historical? Make it intentional.

### Step 11

5. Propose a fix per finding. For booleans, prefer options-object. For

### Step 12

same-type, name the params (`fromAddress`, `toAddress`). For families,

### Step 13

choose one convention.

### Step 14

6. Write `footgun-report.md` to the working directory.

## Usage

```
/footguns                          # interactive
/footguns <dir>                    # scan project directory
/footguns -help                    # show usage
```

Returns JSON with `signatures[]`, `similarityGroups{}`, `findings[]`
plus summary counts.

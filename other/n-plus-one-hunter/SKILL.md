---
name: n-plus-one-hunter
description: "N+1 query hunter: traces loop-to-query data flows in source code, identifies ORM N+1 patterns, and distinguishes real N+1 problems from intentional batch/join patterns. Read-only. Audience: Both. Trigger: /n-plus-one"
trigger: /n-plus-one
---

## What this is for

ORM N+1 queries are the #1 performance antipattern in web applications. A loop
that fetches 100 parent rows then executes 100 more queries for each child
produces 101 database round-trips where 1 would suffice. This skill finds the
pattern statically by tracing loop constructs to ORM data-access calls, then
the LLM distinguishes real N+1 problems from intentional batch patterns.

The dominant failure mode is the hidden N+1 that degrades production performance
linearly with data growth - invisible in development with small datasets.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/loop-query-trace.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each candidate:

### Step 5

- Read the `loopType`, `loopSource`, and `queryCall` fields.

### Step 6

- Check `hasBatchHint`: does the query use IN clause, whereIn, include, or relations?

### Step 7

- If hasBatchHint is false and the query is inside a loop: real N+1.

### Step 8

- If hasBatchHint is true: intentional batch or eager-loaded pattern.

### Step 9

5. Confidence: `proven` (query inside loop with no batch hint), `likely`

### Step 10

(query inside loop with partial batch hint), `suspected` (ambiguous).

### Step 11

6. Write `n-plus-one-report.md` to the working directory.

## Usage

```
/n-plus-one                         # interactive, prompts for directory
/n-plus-one <dir>                   # scan project directory
/n-plus-one -help                   # show usage
```

Returns JSON with `candidates[]`: each entry `{file, line, loopType,
loopSource, queryCall, queryArgs, hasBatchHint}` plus `counts: {scannedFiles,
totalCandidates, byVerdict}`.

## Report Format

`n-plus-one-report.md` with:
- Executive summary (total candidates, real N+1 vs batch vs eager-loaded)
- Critical findings (real N+1 - O(n) queries where O(1) would work)
- Non-issues (batch queries and eager-loaded relations)
- Confidence column for every finding
- Open questions (suspected, needs human review)

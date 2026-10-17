---
name: migration-limbo-detector
description: "Migration limbo detector: screens for half-finished migrations by counting usage of competing patterns (axios/fetch, moment/date-fns, jest/vitest, require/import, redux/zustand, joi/zod, ...), reconstructing the migration timeline via git log, and estimating completion effort. Custom pattern pairs supported via -CustomPairs. Read-only. Audience: Senior. Trigger: /migration-limbo"
trigger: /migration-limbo
---

## What this is for

Every codebase contains half-finished migrations: both axios AND fetch, both
moment AND date-fns, both require AND import in the same folder. The old
pattern, the new pattern, the transitional pain - nothing tells the team
which pattern is the target. This skill counts competing patterns in the
source, reconstructs the migration timeline via git log per side, and tells
the LLM which files are next.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/pattern-census.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each detected schism:

### Step 5

- Is this an intentional split (e.g. legacy vs new module folders) or

### Step 6

genuine limbo?

### Step 7

- Git timeline: which side has more recent commits, and by whom?

### Step 8

- Migration direction: which side is the target? Are the older files the

### Step 9

flagged ones for migration?

### Step 10

5. Estimate remaining effort (files to migrate, conflicts to resolve).

### Step 11

6. List concrete next files to migrate, ordered by tenant-impact (callers).

### Step 12

7. Write `migration-limbo-report.md` to the working directory.

## Usage

```
/migration-limbo                              # interactive, prompts for directory
/migration-limbo <dir>                        # scan project directory
/migration-limbo <dir> -CustomPairs "react,preact;mocha,vitest"
/migration-limbo -help                        # show usage
```

Built-in pairs (18): HTTP_CLIENT, DATE_LIB, TEST, PROMISE, MODULE, STATE_LIB,
VALIDATION, FORM, STYLE, LOGGER. Custom pairs via `;`-delimited
`sideA,sideB;sideA,sideB`.

Returns JSON with `schisms[]`:
`{patternName, kind, sideA, sideB, filesA[], filesB[], countA, countB,
firstA, lastA, firstB, lastB}` plus summary.

## Report Format

`migration-limbo-report.md`:
- Executive summary (count of schisms, oldest limbo, biggest one)
- Per Schism:
  - Side counts and histories (first/last commit)
  - Recommendation (target side, files to migrate, estimated effort)
- Open questions (suspected, needs human review)

---
name: changelog-narrator
description: "Changelog narrator: reads the diff between two tags/commits, clusters changes into logical groups (features, bugfixes, refactoring, dependencies), and writes a semantic changelog with breaking changes, migration notes, and deployment risk. Collector extracts git diff and clusters by module; LLM classifies each change as feature/bugfix/chore/refactor/breaking, writes migration notes, and assesses deployment risk. Read-only. Audience: Both. Trigger: /changelog"
trigger: /changelog
---

## What this is for

`git log` tells you what changed. It does not tell you what *kind* of change it is, whether it breaks callers, or what the deployment risk is. This skill reads a git diff, clusters changes by module, classifies each cluster by semantic type, writes migration notes for breaking changes, and produces a deployment risk assessment.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/diff-trace.ps1 -ProjectDir "<path>"` (optional: `-FromRef`, `-ToRef`).

### Step 4

4. LLM reads the JSON output. For each module in `modules[]`:

### Step 5

- **Feature**: new capability. Describe what it does and who benefits.

### Step 6

- **Bugfix**: defect corrected. Reference the symptom and impact.

### Step 7

- **Refactoring**: structural change with no external behaviour change. Why was it done?

### Step 8

- **Chore**: dependency update, tooling, CI. Note any breaking version bumps.

### Step 9

- **Breaking change**: API renaming, removed exports, changed signatures. Write migration note.

### Step 10

5. Per breaking change, write a **migration note**: old call site, new call site, automated migration if possible.

### Step 11

6. Assess **deployment risk** per change group: None / Low / Medium / High.

### Step 12

7. Write `CHANGELOG.md` to the working directory.

## Usage

```
/changelog                            # interactive (default HEAD~10..HEAD)
/changelog <dir>                      # scan project
/changelog <dir> -FromRef v1.0 -ToRef v1.1
/changelog -help                      # show usage
```

Returns JSON with `commits[]`, `files[]`, `modules[]`, `stats{}`, `changeSummary{}`.

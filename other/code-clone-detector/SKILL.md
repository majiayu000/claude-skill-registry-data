---
name: code-clone-detector
description: "Code clone detector: finds exact (Type 1), parameterized (Type 2), near-miss (Type 3), and semantic (Type 4) clones. Risk-tiered report with deduplication proposals. Read-only. Audience: Both. Trigger: /code-clone"
trigger: /code-clone
---
# /code-clone - Code Clone Detector

## What this is for

Code clones - identical or near-identical code blocks - are a maintenance
liability: bugs must be fixed in N places, refactoring carries hidden scope,
and the codebase grows without corresponding value. This skill systematically
finds all 4 clone types, validates each cluster, and produces deduplication
proposals.

Detects all 4 clone types in a target directory. Produces a structured report
with similarity scores, risk tiers, and LLM-validated deduplication proposals.

## Usage

```
/code-clone              # interactive (prompts for directory)
/code-clone <dir>        # scan directory directly
/code-clone -help        # show usage
```


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. `-help` / `-h` -> print usage, exit 0.

### Step 2

2. Confirm target directory exists.

### Step 3

3. Run `scripts/clone-scan.ps1 -ProjectDir <dir>`.

### Step 4

4. LLM reads the JSON output, validates each clone cluster:

### Step 5

- Type 1-3: verify cluster, determine risk tier, propose deduplication strategy.

### Step 6

- Type 4 candidates: read both files, determine if semantic clone exists,

### Step 7

assign confidence level.

### Step 8

5. Filter false positives (framework boilerplate, test doubles, generated files,

### Step 9

trivial wrappers).

### Step 10

6. Write `clone-report.md` to the working directory.

## Clone Types

| Type | Name | Detection | Similarity |
|------|------|-----------|------------|
| 1 | Exact | Whitespace-normalized content hash | 1.0 |
| 2 | Parameterized | Token-normalized (ids/literals as placeholders) | 1.0 |
| 3 | Near-miss | Token Jaccard similarity within Type 2 groups | >= 0.7 |
| 4 | Semantic | LLM validation of file-level fingerprint pairs | LLM-determined |

## Risk Tiers

| Tier | Meaning |
|------|---------|
| Critical | Both blocks actively maintained, diverging logic risks bugs |
| Medium | One block is a copy of the other, likely a quick paste |
| Low | Generated code, test fixtures, intentional duplication |

## Output

`clone-report.md` with:
- Executive summary (total clusters, clone density, distribution by type)
- Critical findings (sorted by risk, with locations and deduplication proposal)
- Medium findings (grouped by clone type)
- Low / informational findings (intentional duplicates with justification)
- False positives (dismissed with reason)
- Open questions (all suspected clusters, Type 4 needing manual review)

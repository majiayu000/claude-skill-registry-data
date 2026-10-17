---
name: code-smell-detection
description: "Code smell detector: statically identifies 10 families of structural code quality issues (long methods, deep nesting, god classes, feature envy, primitive obsession, data clumps, shotgun surgery, message chains, refused bequest, speculative generality). Evidence-based report with metrics and LLM validation. Read-only. Audience: Both. Trigger: /code-smell"
trigger: /code-smell
---
# /code-smell - Code Smell Detector

## What this is for

Structural code smells indicate design problems that make the codebase hard to
change, understand, or extend. This skill scans for 10 smell families,
quantifies each finding with metrics, and validates them against code context
for actionable, evidence-based refactoring proposals.

Detects 10 code smell families in a target directory. Produces a structured report
with metrics, evidence, and LLM-based validation of each finding.

## Usage

```
/code-smell              # interactive (prompts for directory)
/code-smell <dir>        # scan directory directly
/code-smell -help       # show usage
```


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. `-help` / `-h` â†’ print usage, exit 0.

### Step 2

2. Confirm target directory exists.

### Step 3

3. Run `scripts/smell-scan.ps1 -ProjectDir <dir>`.

### Step 4

4. LLM reads the JSON output, validates each finding against the code context,

### Step 5

assigns confidence, and suggests a refactoring path.

### Step 6

5. Write `code-smell-report.md` to the working directory.

## Supported Smell Families

| # | Smell | Severity | Metric |
|--|----|-----|----|
| 1 | Long method | medium | >30 executable lines |
| 2 | Deep nesting | medium | >4 indentation levels |
| 3 | God class | high | >300 lines, >10 methods, low cohesion |
| 4 | Feature envy | medium | more external than internal symbol references |
| 5 | Primitive obsession | low | repeated primitive type parameters |
| 6 | Data clump | medium | same 3+ parameters repeated across methods |
| 7 | Shotgun surgery | high | single concept scattered across many files |
| 8 | Message chain | low | a.b.c.d().e() style chains |
| 9 | Refused bequest | medium | subclass ignores inherited members |
| 10 | Speculative generality | low | unused abstract classes/interfaces |

## Output

`code-smell-report.md` with:
- Executive summary (total findings, severity breakdown)
- Detailed findings per smell family (id, file, line, metric, confidence, suggestion)
- False positives section (rejected by LLM analysis)
---
name: spec-lie-detector
description: "Requirements lie detector: reads a corpus of specs/tickets (text files) and finds contradictions, gaps, ambiguities, silent assumptions and untestable statements - each finding with quote, location, severity and a concrete clarification question. Read-only. Trigger: /spec-check"
trigger: /spec-check
---
# /spec-check

Reads a corpus of specs/tickets (text files) and finds contradictions, gaps,
ambiguities, silent assumptions and untestable statements - each finding with quote,
location, severity and a concrete clarification question.

## What this is for

- Check a requirements corpus for internal consistency BEFORE development starts,
  instead of discovering contradictions in sprint review or in production.
- Humans overlook contradictions 40 pages apart - an LLM checks the entire corpus
  in one pass.
- **Read-only skill.** Does not evaluate domain correctness, only internal
  consistency, gaps and testability. No access to live ticket systems, no
  PDF/Word conversion.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/spec-check -help` or `/spec-check -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify source

Clarify: either `-SpecDir` (a directory, recursively searched for `.md`/`.txt`)
or an explicit file list. If both missing, ask. Show what was detected:

```
Source: <directory or file list>
Continue? (yes/no)
```

Only continue after confirmation.

### Step 3 - Create inventory

```powershell
& "<SKILL_DIR>/scripts/intake.ps1" -SpecDir "<path>"
# or: -Files "<file1>","<file2>"
```

Read the JSON output. If the script aborts with Exit-Code != 0: show message,
stop. If `count: 0`: inform the user that no matching files were found, stop
(do not guess).

If > 30 files in the inventory: show the inventory first (paths + sizes), user
selects a subset or confirms the full run.

### Step 4 - Read and analyze all files

Read each inventoried file (not `excluded`) fully with the Read tool
(for `oversized: true` read section-wise via offset/limit). Then actively search
for each of the 5 finding categories, do not just note what happens to catch your
eye:

1. **Contradiction** - two places demand incompatible things (quote both, name both
   locations).
2. **Gap** - a referenced case is nowhere defined (error cases,
   edge values, permissions, empty states are the usual suspects).
3. **Ambiguity** - ambiguous wording that allows >= 2 implementations
   (write out both interpretations).
4. **Silent assumption** - the spec only works if something unstated holds true.
5. **Untestable** - statement without measurable criterion ("fast",
   "user-friendly").

Per finding: category, severity (`high` = wrong product risk, `medium` = rework
risk, `low` = style issue), verbatim quote + `file:line` (for contradictions:
both locations), one concrete, closed-form clarification question.

Standard confidence levels apply: a "contradiction" at
level `suspected` goes into "Open questions", not into the findings list.

### Step 5 - Write report

Report structure (Markdown), file `spec-check-report.md` in the current
working directory (**not** into the checked directory):

1. **Summary** - finding count per category and severity.
2. **Findings** - sorted by severity (high -> low), per finding: category, quote(s)
   + location(s), clarification question.
3. **Clarification questions (copy-ready for the PO)** - only the questions, without
   context, directly copyable.
4. **Open questions** - everything at confidence level `suspected`.

### Step 6 - Summarize

Tell the user the report path. Summarize the 3 most important clarification questions
first, then the total number of findings per severity.

## Usage

```
/spec-check                    # interactive: ask for spec directory
/spec-check <dir>              # check all text files under <dir>
/spec-check <file1> <file2>    # check explicit files
/spec-check -help              # show usage, stop
```



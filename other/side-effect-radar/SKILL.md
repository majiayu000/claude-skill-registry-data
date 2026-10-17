---
name: side-effect-radar
description: "Blast-radius predictor for a planned change: combines a static reference scan (which files mention the target's exported symbols) with git co-change analysis (which files historically changed together with the target), then produces a risk-tiered report with concrete review/test recommendations. Read-only. Trigger: /blast"
trigger: /blast
---
# /blast

Combines static reference search with historical co-change analysis (which
files in the past were almost always changed together with the target) into
a risk-tiered blast radius report before a planned change.

## What this is for

- Before a risky change, know what is affected - not just statically
  (references), but also historically coupled (files without import relationship
  that were always changed together).
- **Read-only skill.** No real AST/type graph - text-based, language-agnostic
  reference search at grep level suffices for risk hints (Simplicity First).
  No dynamic analysis.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/blast -help` or `/blast -h` (without further arguments) is invoked: output
the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target and change

Clarify: `-ProjectDir` (repo root or a subfolder), target file(s) (the
planned change location), and a short free-text description of the planned change
(determines which symbols are relevant - e.g. "change signature of X" vs. "internal
optimization"). If something is missing, ask. Get confirmation:

```
ProjectDir: <path>
Target file(s): <files>
Planned change: <free text>
Continue? (yes/no)
```

### Step 3 - Identify symbols

Read target file(s) with the Read tool, identify exported/public symbols
(language-dependent, no script - when uncertain take all top-level identifiers).

### Step 4 - Collect evidence

```powershell
& "<SKILL_DIR>/scripts/ref-scan.ps1" -ProjectDir "<path>" -Symbols <symbols>
& "<SKILL_DIR>/scripts/co-change.ps1" -ProjectDir "<path>" -Files <target files>
```

If `co-change.ps1` aborts with "No git repo": continue with `ref-scan.ps1` alone,
explicitly note the missing historical analysis in the report
(no abort - edge case of the sprint file).

### Step 5 - Analysis

1. Evaluate static hits from `ref-scan.ps1`: actual usage vs.
   name collision/comment/string (line content is available). Sort out
   collisions, but list in the report appendix.
2. Form risk tiers:
   - **Tier 1 - directly affected** (`proven`): files with actual symbol usage.
   - **Tier 2 - historically coupled** (`likely`): co-change ratio >= 0.4
     without static reference - the most dangerous category. Explicitly explain WHY
     the coupling might exist (deduce from file names/paths), give confidence
     honestly.
   - **Tier 3 - periphery**: weak coupling (ratio < 0.4, >= MinCoChanges), list
     only.
3. Incorporate the user's change description: which tier 1/2 locations are
   affected by the CONCRETE change.
4. `capped: true` for a symbol: note in the report that the symbol was too
   generic for a complete static analysis.

### Step 6 - Write report

File `blast-report-<file>.md` in the current working directory (**not** into the
analyzed repo):

1. **Summary** - risk assessment in 3 sentences.
2. **Tier 1 - directly affected** - with `file:line`.
3. **Tier 2 - historically coupled** - with coupling numbers (n of N commits, ratio)
    and the suspected explanation.
4. **Tier 3 - periphery** - short list.
5. **Recommendations** - concrete ("before merge: run test X, review file Y,
    inform owner of Z").
6. **Open questions**.

### Step 7 - Summarize

State the report path, reproduce the summary directly in chat.

## Usage

```
/blast                          # interactive
/blast <repo> <file> [...]      # blast radius for planned change at <file>
/blast -help
```



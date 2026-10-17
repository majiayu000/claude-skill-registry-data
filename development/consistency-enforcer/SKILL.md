---
name: consistency-enforcer
description: "Finds duplicated BUSINESS LOGIC (not duplicated text): extracts rule candidates (validations, calculations, domain constants, regexes, status logic) from a codebase, then has the LLM cluster semantically equal rules across different implementations and flag divergent ones with a single-source-of-truth proposal. Read-only. Trigger: /consist"
trigger: /consist
---
# /consist

Finds semantically identical business rules in different code (not
text duplicates) and reports divergences between their implementations with a
single-source-of-truth proposal.

## What this is for

- The same domain rule - a price calculation, an age limit, an
  email validation - often lives in many places in the system, each slightly
  differently implemented (`if (age >= 18)` vs. `isAdult(user)` vs. `MINIMUM_AGE = 18`).
  Classic clone detection is blind to this; semantic equivalence can only be
  detected by an LLM.
- **Read-only skill.** No automatic refactoring, only a proposal.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/consist -help` or `/consist -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target and focus

Clarify: `-ProjectDir` and optionally a domain focus (free text, e.g. "everything
related to pricing" - narrows the LLM clustering, NOT the extraction). Get
confirmation.

### Step 3 - Extract candidates

```powershell
& "<SKILL_DIR>/scripts/rule-candidates.ps1" -ProjectDir "<path>"
```

If `candidates.Count: 0`: cleanly report ("no rule candidates found"),
do not write an empty pseudo-report, stop.

### Step 4 - Analysis

1. Review candidates, discard obvious noise (loop indices,
   test numbers, HTTP status codes in framework code) - name discarded categories
   in the report appendix.
2. **Cluster by domain meaning**, not by text: "everything that checks
   adulthood", "everything that calculates VAT". If > 300 candidates: roughly
   cluster by category first, then analyze deeply per category. If focus is
   set: only deeply analyze matching clusters, list rest as inventory.
3. Per cluster with >= 2 locations:
   - All locations with `file:line` + code snippet.
   - **Consistency verdict**: `consistent` (same semantics, same values) or
     `DIVERGENT` (e.g. `>= 18` vs. `> 18`; `0.19` vs. `19`) - precisely name
     the deviation and what incorrect behavior it can produce.
   - **SSoT proposal**: where the rule should live exclusively in the future
     (prefer existing constant/function, otherwise proposal with module location),
     state confidence.
4. Do NOT exclude test files (they often encode the "true" rule), but mark
   as test in the cluster. Cross-language clusters (e.g. code + SQL) are
   explicitly desired.
5. Evidence requirement: no cluster claim without all locations; divergence verdict
   only with direct code quote from both sides (confidence level must be `proven` for equivalence claims).

### Step 5 - Write report

File `consist-report.md` in the current working directory (**not** into the analyzed
repo):

1. **Summary** - X rules implemented multiple times, Y of them divergent.
2. **Divergences** first (severity: divergent values = high).
3. **Consistent multiple implementations**.
4. **SSoT proposals**.
5. **Open questions** (clusters at confidence level `suspected`).

### Step 6 - Summarize

State the report path, reproduce the summary directly in chat - divergences
first.

## Usage

```
/consist                  # interactive
/consist <dir>            # entire directory
/consist <dir> "<focus>"  # with domain focus
/consist -help
```



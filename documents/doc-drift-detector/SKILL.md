---
name: doc-drift-detector
description: "Documentation drift detector: extracts verifiable claims from a repo's markdown docs (file paths, commands/scripts, config keys, endpoints, versions, referenced symbols) and statically verifies each one against the actual code, reporting every stale claim with a concrete fix suggestion. Never executes documented commands. Read-only. Trigger: /doc-drift"
trigger: /doc-drift
---
# /doc-drift

Your README has been lying for six months. Time to catch it. Extracts verifiable
claims from docs (paths, commands, config keys, endpoints,
versions, symbol references) and statically checks each against the code reality.

## What this is for

- README mentions commands that no longer exist, paths that moved,
  env vars that were renamed - nobody checks this systematically because it is
  tedious manual work at scale.
- **Read-only skill. Documented commands are NEVER executed** -
  purely static comparison (safety over completeness). No external
  links, no prose evaluation.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/doc-drift -help` or `/doc-drift -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/claim-extract.ps1" -ProjectDir "<path>"
```

If `docFiles` is empty: inform the user that no doc files were found
(README*/*.md/docs/**/*.md/CONTRIBUTING*), stop.

### Step 4 - Verification (NEVER execute commands)

Check each claim statically against the repo (Grep/Glob/Read):

- **path**: does file/directory exist? On failure: search for similar paths
  (moved?) -> correction suggestion.
- **command**: match npm scripts against `package.json` `scripts` (analogous
  Makefile targets, pyproject scripts) - existence logic only,
  **never execute**. Not statically checkable -> `not-checkable`.
- **config**: grep key in code/config - is it read/defined?
- **endpoint**: does route exist in code?
- **version**: compare against engines/target entries in manifests.
- **symbol**: does identifier exist in code (word-boundary grep)?

Special cases: future announcements ("coming soon...") -> `not-checkable`, not drift.
Placeholders (`<your-key>`, `$VAR`): normalize, only check structure.
Monorepo: try path relative to doc directory AND repo root.
Auto-generated docs (generator marker): exclude, only list. Anchor links
(`#section`) not checked (out of scope).

Verdict per claim: `correct` / `DRIFT` (with both locations: doc line +
repo evidence or absence) / `not-checkable` (with reason). Severity for
drift: `high` (command/path in setup path) / `medium` / `low`.

### Step 5 - Write report

File `doc-drift-report.md` in the current working directory:

1. **Summary** - total claims, drift ratio, high-severity findings.
2. **Drift findings** by severity, per finding: correction suggestion (concrete
   replacement text).
3. **Not-checkable list**.
4. **Correct count**.
5. **Open questions**.

Evidence requirement: each drift verdict with both locations.

### Step 6 - Summarize

State the report path, drift ratio and high-severity findings first.

## Usage

```
/doc-drift               # interactive
/doc-drift <dir>         # check repo docs
/doc-drift -help
```



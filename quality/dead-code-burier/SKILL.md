---
name: dead-code-burier
description: "Dead-path undertaker: identifies provably unreachable code by combining static reachability (unreferenced exports/files), optional runtime evidence (coverage reports, logs) and git age, then produces a burial list ranked by evidence strength. NEVER deletes automatically - prepares patches for individual user approval only. Trigger: /bury"
trigger: /bury
---
# /bury

Identifies provably unreachable code (static unreachability +
optional runtime evidence + git age) and buries it - but **never
automatically**, only after your explicit individual approval per candidate.

## What this is for

- Safely identify dead paths (never-called functions, orphaned files) instead of
  never deleting out of fear of "that one hidden call".
- Combines static unreachability with runtime evidence (coverage, logs, if
  available) and git history into a solid verdict per candidate - including
  honest residual risk (reflection/DI/route conventions are NOT reliably detected).

## PROTECTION RULE - never `~/.claude/`

The target directory must under no circumstances be `C:\Users\ostol\.claude\` (or
its subdirectories). If the user proposes `~/.claude/` as target, abort immediately.

## PROTECTION RULE - deletions ONLY after individual approval

**This skill NEVER deletes automatically.** The report is always only a
proposal. A deletion (edit in the target project) occurs exclusively when the
user explicitly approves A SPECIFIC candidate by number/name - never
blanket ("just delete everything"), never without asking. Without any approval the
flow ends at the report.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/bury -help` or `/bury -h` (without further arguments) is invoked: output
the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir` (not `~/.claude/`, see protection rule) and optionally paths to
a coverage report (`coverage-summary.json` or `lcov.info`) and/or a
log directory. Get confirmation.

### Step 3 - Static reachability

```powershell
& "<SKILL_DIR>/scripts/reachability.ps1" -ProjectDir "<path>"
```

Redirect output to a file (needed for Step 3 as `-Candidates`).

### Step 4 - Runtime evidence (if provided)

```powershell
& "<SKILL_DIR>/scripts/evidence.ps1" -ProjectDir "<path>" -Candidates "<file-from-step-2>" [-CoverageFile "<path>"] [-LogDir "<path>"]
```

Without coverage/logs: continue with the raw reachability data from Step 2,
note the missing runtime evidence in the report.

### Step 5 - Age evidence

Per candidate: `git -C "<ProjectDir>" log -1 -format=%ci - "<file>"` (no
custom script needed). No git repo: age evidence omitted, note in report.

### Step 6 - Analysis

1. Validate candidates: actively check known false-positive classes and
   SORT OUT or downgrade - framework conventions (route handlers,
   lifecycle methods, DI registrations, reflection strings, dynamic imports,
   public package API for libraries - check `package.json`/`pyproject.toml`
   `main`/`exports`). Justify each removal.
2. Evidence strength per remaining candidate:
   - **Strong**: 0 references + 0 coverage + no log hits + > 2 years untouched.
   - **Medium**: 0 references + (coverage OR age), no runtime data against.
   - **Weak**: statically only, young file or no runtime data available.
3. Very generic symbol name: reference count is unreliable - check hit context,
   otherwise downgrade.
4. Evidence requirement: no candidate without complete evidence line (refs, coverage,
   logs, age - even if a field is "no data", state it explicitly).

### Step 7 - Write report

File `bury-report.md` in the current working directory (**not** into the analyzed
repo):

1. **Summary** - X candidates: strong/medium/weak.
2. **Burial list** - sorted by strength, per candidate: all evidence (refs,
   coverage, logs, last commit + hash), residual risk note (which dynamic
   call type could NOT be excluded), diff preview of the deletion.
3. **Sorted out** - with justification.
4. **Open questions**.

### Step 8 - Get approval, ONLY THEN delete

Summarize the report, then ask: "Which candidates (number) should be buried?"
Only the individually named candidates via Edit in the target project -
never more than explicitly named. After each deletion: recommend the user run
build and tests of the target project. No answer/no approval: flow ends at the
report, nothing is changed.

## Usage

```
/bury                                # interactive
/bury <dir>                          # static + git age only
/bury <dir> -coverage <report>       # plus coverage evidence
/bury <dir> -logs <logdir>           # plus log evidence
/bury -help
```



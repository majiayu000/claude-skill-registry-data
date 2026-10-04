---
name: verify-before-fix
description: >-
  Execute bug fixes from an issue description when locations may be stale, paths may not match repo layout, and bugs may already be partially fixed on the current branch. Verify each listed bug before touching code.
version: 1.0.0
author: Yuno
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    category: software-development
    tags: ['bug-fixes', 'issue-execution', 'verification', 'workflow']
    related_skills: ['systematic-debugging', 'github-issues', 'greyscript-compiler-debugging']
changelog:
  1.1.0 (2026-07-07): Variant B (priority-ordered fix loop), regression-test step after each fix, batch-final-verify phase, references/fix-loop-reproduction.md.
  1.0.0 (2026-07-07): Initial version — extracted from Issue
agent: Verifier
routing_hint: |
  **Agent-Scope:** Adversarial QA, audits, security scans, gates. Off-scope: building, designing, writing — return to Yuno for re-route.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Verify Before Fix: Issue-Driven Bug Fix Execution

When a task asks you to fix bugs defined by an issue with pre-specified
file:line locations (e.g. "Issue #43: 11 GreyScript syntax bugs in
`bin/ps.src`, `xmem.src`, …"), the issue is a **hypothesis, not ground truth**.
It may reference stale paths, already-fixed bugs, or files that no longer exist.

**Core rule (inherited from systematic-debugging):** No fixes without
verification first. Always.

## When to Load This Skill

- The task references a specific issue number with a bug list
- A multi-bug issue gives explicit file:line locations for each fix
- You're working on a branch that may already have partial fixes
- The issue's file paths don't match what you see in the repo
- You need to decide which bugs are truly unfixed before editing

## The Workflow

### Step 1: Find the Right Repo

First, locate the actual repo. The working directory hint may be wrong —
check multiple likely locations:

```bash
find ~ -maxdepth 4 -type d -name "<repo-name>" 2>/dev/null
```

Then read the repo structure:

```bash
ls -la <repo>
git branch
git log --oneline -5
```

### Step 2: Map Issue Paths to Repo Layout

Issue paths often follow a different layout than the actual repo:

| Issue says | Repo has | Map |
|---|---|---|
| `bin/ps.src` | `tools/ps/ps.src` | One level deeper, in a named tool dir |
| `test/test_core.src` | `tests/` or no such file | May not exist at all |
| `lib_core` | `libs/lib_core.src` | Moved or renamed |

**Don't jump to conclusions.** A missing file doesn't mean the repo is wrong —
it means the issue path needs remapping. Start by reading the repo root.

### Step 3: Detect Partial Fixes on the Branch

If you're on a feature/fix branch (not `main`), earlier commits may have
already addressed some or all of the listed bugs:

1. **Check git blame** on the suspected files to see when they were last changed
2. **Look for fix comments** in the code — `// FIX NP-49`, `// FIX BUG F-1`,
   `// Fixed 2026-07-04`, etc. These document intentional fixes, not stale code.
3. **Check the branch title** — if the branch is `fix/merge-…-fixes-into-…`,
   it's explicitly a branch carrying partial fixes.

**Crucial:** A fix-comment in the code means the bug was intentionally
corrected. Do NOT re-apply a "fix" to code that was already fixed.

### Step 4: Verify Each Bug Before Touching Code

For each bug in the list, run through this checklist:

1. **Does the file exist** at the mapped path? If not, find it or determine
   it was deleted/renamed.
2. **Does the stated line number** still contain the buggy pattern? (Line
   numbers drift with every commit — always check the actual line.)
3. **Is the bug pattern actually present AND active?** A `"char(10)"` inside a
   `// FIX BUG` comment is **documentation**, not a bug.
4. **Is the bug exclusive to code?** Grep the exact broken pattern and
   subtract matches inside comments. Only code-level matches count.
5. **If the path or line is wrong**, find the actual coordinates. The bug
   may still exist — just not where the issue says it does.

**Verification rule of thumb:** A listed bug is "already fixed" only if
every code-level occurrence of the broken pattern is gone. If even one
code-level occurrence exists anywhere, the bug is still open.

**Useful verification commands:**

```bash
# Check a specific pattern across all .src files
grep -rn '"char(10)"' <repo> --include="*.src" | grep -v '://'

# Check get_shell with parameters
grep -rEn 'get_shell\s*\(' <repo> --include="*.src" | grep -v 'get_shell$'

# Check import_code without .src extension
grep -rEn 'import_code\("[^"]+"\)' <repo> --include="*.src" | grep -v '\.src"'
```

### Step 5: Report a Structured Summary

After verification, organize findings into clear categories. Do NOT just say
"some were already fixed" — enumerate them:

- **Fixed (no action):** Bugs already handled on the branch. For each one,
  state the evidence (fix comment, git log, etc.).
- **Wrong coordinates:** Bugs where the stated file path or line number was
  incorrect. Say what the correct location is, if applicable.
- **Verified broken — fixed now:** The subset you actually edited, with the
  change applied.
- **Out-of-scope sibling bugs:** Additional bugs of the same families found
  during verification but not listed in the issue. Report with file:line.
  Do NOT silently fix or silently ignore — flag them for the user.

### Step 6: Fix Only the Verified-Broken Subset

Apply mechanical fixes only to what was confirmed broken at verified
coordinates. Do not touch already-fixed code, even if the issue claims
it needs fixing.

1. Use `patch(mode='replace')` for minimal, targeted changes
2. Verify the change with a follow-up `read_file`
3. **Write a regression test** that asserts the exact bug symptom is gone.
   The test must go RED on the old code and GREEN on the new code. Prefer
   pytest tmp_path fixtures for hermetic file-based inputs.
4. **Run the regression test** alone first to confirm it catches the fix.
5. **Run the full existing test suite** to confirm no regressions from this
   single fix.
6. If instructed not to commit/push, leave changes unstaged.
7. **Only then** mark the bug as done and move to the next one.

**Why regression tests after each fix (not all at once):**
- Each fix is independently verifiable — when a later test suite run fails,
  you know the last fix caused it, not some earlier one.
- The test represents the bug's exact contract — future changes that reintroduce
  the symptom will be caught immediately.
- Cumulative evidence: the final report shows N bugs fixed and N+M tests green.

### Step 7: Record Sibling Bugs (Out-of-Scope)

If verification reveals additional bugs of the same families outside the
issue's scope:

- List them in the summary as a separate section
- Do NOT fix them unless explicitly asked
- Let the user decide whether to create a follow-up issue

This respects the scope boundary while surfacing valuable context.

### Step 8: Batch Final Verification

After ALL fixes and their individual regression tests are applied, run the
**complete test suite** one final time. This catches interaction regressions
— cases where Fix A didn't break anything alone but breaks when combined
with Fix B's data state change.

```bash
cd <project-dir>
pytest tests/ -v 2>&1 | tail -15
```

The batch verification output is the **only** admissible evidence in the final
report. Individual "it worked after the fix" claims from Step 6 loop are not
sufficient — the final green run is the deliverable.

Report the result as: `M passed / N total (P regressions)` where M, N, P come
from the actual terminal output, not from memory or intermediate checks.

## Variant B: Priority-Ordered Fix Loop

Use this variant when bugs arrive **pre-sorted by severity** (HIGH / MED / LOW
with reproducible repro commands for each) rather than as a raw issue list.
This is the Yuno default for explicit fix-loop runs (e.g. Verifier output).

**Key difference from the main workflow:** Do NOT verify all bugs before fixing
any. Instead, fix in priority order: reproduce → fix → add test → next.
This gets the highest-value fixes applied fastest and surfaces blocking
questions early.

### Step 1: Build a Todo List with Priority

Create a `todo()` list ordered by severity: all HIGH first, then MED, then LOW.
Each entry says what the bug is and the one-line repro command:

```json
[
  {"id": "1", "content": "Fix Bug #2: fmean crashes on NaN/Inf", "status": "pending"},
  {"id": "2", "content": "Fix Bug #3: ragged-row detector broken", "status": "pending"},
]
```

### Step 2: Per-Bug Cycle (Repeat for Each Bug in Priority Order)

For each bug, run this tight loop:

1. **Reproduce** — Run the Verifier's repro command or build your own.
   Confirm it's red (exhibits the bug). Takes 1 terminal call.
2. **Root cause** — Read the relevant code. Identify the exact line/pattern
   causing the symptom. Takes 1–2 read_file calls.
3. **Fix** — Apply the minimal change via `patch(mode='replace')`. One call
   per bug.
4. **Re-run repro** — Confirm the repro command is now green. One call.
5. **Write regression test** — Add a pytest test to the test suite that
   asserts the exact bug symptom is resolved:
   - Use `tmp_path` fixtures for hermetic file-based inputs
   - Assert on exit code, stdout content, and stderr (no "Traceback")
   - The test must be RED on old code, GREEN on new code
6. **Run the full suite** — Confirm no regressions from this single fix.
   `pytest tests/ -q` — one call.
7. **Mark todo completed** — Only now.

**Important:** Do NOT batch marks. Each bug gets its own fix → test → verify
cycle. `todo` status transitions from `in_progress` → `completed` only after
a real tool-call produced evidence (test output, file diff, etc.).

### Step 3: Batch Final Verification

After the last bug is fixed and its regression test passes, run the full
test suite one last time as the **definitive evidence** for the report.
Report exact counts from terminal output: M passed / N total.

### When to switch back to Variant A

- Bug list covers multiple repos → you need Variant A's path-mapping first
- Bugs have stale coordinates (file:line from an old release) → Variant A's
  verification comes BEFORE fixing
- Branch may have partial fixes already → you need Variant A's partial-fix
  detection first
- The fix is in GreyScript / unusual language → Variant A's grep patterns apply

When in doubt: **Variant A for stale/uncertain inputs, Variant B for verified
fresh inputs with clean repros.**

## References

- `references/fix-loop-reproduction.md` — Concrete fix patterns from a real
  Verifier session: math.isfinite for NaN/Inf, csv.reader for ragged rows,
  argparse type=validators, ascii-bar truncation. Browse for technique
  inspiration when facing the same bug families.

## Pitfalls

### Issue Paths Are Not the Repo Truth

The most common pitfall: the issue says `bin/ps.src` and you spend 10
calls searching for it before realizing the repo has `tools/ps/ps.src`.
Always read the repo root first — it costs one `ls` call.

### Comments Mask as Bugs (False Positive)

A grep for `"char(10)"` will match both:
- `// FIX: split("char(10)") was wrong — corrected 2026-07-04`
- `cache_file_content.split("char(10)")  // still broken`

Only the second one is a real bug. Always verify the match is in code,
not a comment.

### Fix-Comments Signal Fixes, Not Stale Code

If a file has `// FIX NP-49` or `// FIX BUG F-1` in its comment block,
the fix was already applied. Do not re-apply it. The presence of a
documentation comment about a bug means the bug is already corrected.

### Line Number Drift

Issue line numbers are never trustworthy after the first commit on a
branch. Always read the actual line content at the stated position,
then search for the pattern independently.

### The Sibling-Bug Dilemma

When you find 9 out-of-scope bugs of the same families, you have two
bad options: (a) fix them and expand scope without asking, or (b) say
nothing and leave them unfixed. The correct answer is (c): report them
and let the user decide. Do not pick (a) or (b).

### Todo-Execution Dicipline

Do NOT mark a bug as `todo(status="completed")` without an intervening
tool-call (read_file, terminal with test output, patch, etc.). The
`todo` tracker is not a "done in my head" tool. Mark `completed` only
after real evidence exists on disk or in terminal output.

## Related Skills

- `systematic-debugging` — The parent discipline: find unknown bugs.
  This skill handles the special case of bugs already *described* by
  an issue but whose description may be stale.
- `github-issues` — Create/triage/manage the issues that produce these
  fix lists.
- `greyscript-compiler-debugging` — GreyScript-specific bug patterns
  and fix recipes. Load alongside this skill when the bugs are in .src files.
- `ki-murks-verhindern` — Quality gates for agent workflows. Verification
  is a quality gate; this skill is one specific gate implementation.

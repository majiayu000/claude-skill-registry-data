---
name: worker-proof-planning
description: Use when writing an implementation plan, fix-up plan, or task list that a separate, less capable model (a Haiku worker, a subagent, or another session) will execute without access to this conversation, or when checking a worker's completion report against the repository. Triggers include "write a plan for my worker", "plan this for Haiku", "create tasks for my workers", and "verify the worker's report".
---

# Worker-Proof Planning

## Overview

A worker follows a plan literally, cannot ask questions, and reports success whether or not it succeeded. A plan works only if every step can be carried out and checked mechanically, and only if the planner has executed the plan's own text before handing it over.

**REQUIRED BACKGROUND:** superpowers:writing-plans for the document header and task structure.

## The step contract

Use only these forms. Put paths in backticks; `references/simulate_plan.py` executes exactly this phrasing.

| Form | Plan text |
|---|---|
| Edit | "In `path`, find:" + block of complete old lines, then "Replace with:" + block. The old text must occur exactly once. |
| Whole file | "Replace the whole contents of `path` with:" + block |
| New file | "Create `path` with:" + block |
| Append | "Append this to the end of `path`:" + block |
| Mechanical change | a ```bash block with a script, for syncing a file into a doc, reformatting, or bulk renames |
| Check | a ```bash block, then "Expected output, exactly:" + a ```text block with the **complete** output |
| Script for later | "Save this exact content to `path`:" + block, then a ```bash block that runs it |

- Every step ends with a Check. Test durations are ignored. Write `<sha>` where a commit hash may vary; a literal hash must match exactly.
- Every command the worker runs is in a ```bash block, never in prose.
- Never locate anything by line number, and never write "same as Task 3": repeat the text.
- Give each heredoc a delimiter that cannot occur in its content, such as `EOF_7Q2Z`.

## Required parts of every plan

1. **Step 0, starting state:** Checks for the exact starting commit, an empty `git status --porcelain --untracked-files=no`, and passing tests. "If this differs, stop and report." If the plan commits, also check that `git config user.email` prints a value in the repository the worker uses. A fresh clone has no local identity, so a worker that starts from one must be told which identity to set.
2. **Global constraints:**
   - Type code exactly as given. Do not restructure, rename, reorder, or simplify.
   - Change only what a step names.
   - One commit per task, with the given message and file list. Never amend, rebase, reset, or split a commit.
   - If a Check's output differs from the expected output, stop. Fix only your last edit, never the Check. If it still differs, report the step, the command, and the output.
3. **Red before green:** each regression test has a Check showing its exact failing output before the fix.
4. **Final gate:** a script with one PASS/FAIL line per requirement in the brief, ending in `ALL CHECKS PASS`. List the brief's requirements first, and give each one a line; a requirement without a line is how a plan drops it. Compare regions that must not change with their original text from the starting commit, not just with a heading. Check each commit's file list.
5. **Report contract:** paste the named outputs verbatim, including the red Check; list every deviation, or write "none".

## Before handing over: execute the plan

```bash
python3 <skill-dir>/references/simulate_plan.py PLAN.md REPO [--identity "Name <email>"]
```

`<skill-dir>` is this skill's directory, shown as its base directory when the skill loads.

It clones REPO, applies every edit, runs every command, and compares every Check with its expected block. The clone takes REPO's git identity. Pass `--identity` only if the plan tells the worker to set one; otherwise a missing identity fails the simulation, as it would fail the worker. Hand the plan over only at `0 problem(s)`. Then revert the fix in a scratch clone (`--keep` keeps one) and confirm the final gate fails: a gate that cannot fail proves nothing. If the plan contains code for later tasks, build and test all of it too.

## Verifying the worker's report

The report is a claim. Before accepting it:

1. Run the final gate yourself.
2. Run the simulator with `--at <start commit> --keep` and diff its tree against the worker's. Every difference is a deviation, whatever the report says.
3. Revert the fix in a scratch copy and confirm the new tests fail.
4. Read each commit's message and file list.

## Common mistakes (each one observed)

| Mistake | What happened | Prevent with |
|---|---|---|
| "at roughly line 3190", "match on the quoted code" | Worker skipped 2 of 4 edits | An Edit with the complete old text |
| "use the version from Task 4 Step 3" | Half a function copied | Repeat the full text |
| Code inside markdown edited by hand | Partial sync; unrelated comment deleted | A script and a byte-identical check |
| Given code "improved" by the worker | New resource leak on 3 paths | "Type exactly" rule, byte-identical gate |
| Requirement with no gate line | Fix silently discarded the close error | One gate line per requirement |
| Gate on commit count only | Worker split a commit to hit the number | File list per commit |
| Expected output written from memory | Worker stops on a correct result | Run the simulator |
| Simulated with a git identity the worker will not have | Plan passed; a real worker stops at Step 0 | Let the simulator copy REPO's identity; `--identity` only when the plan sets one |
| Test passing on the buggy code; race test run once | Bug shipped with green tests | Red before green; loop a race test 100 times |
| Report accepted as written | Fix incomplete, report said done | Verify the report |

## Red flags: stop

- "The worker can work out where this goes."
- "I checked that the code works." Run the plan's text, not the code.
- Expected results written as prose: "confirm the tests pass".
- "The report says ALL CHECKS PASS."

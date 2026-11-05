---
name: passes
description: Run the recurring passes between batches (tests/CI, performance, memory, cleanup, and the workflow pass) that are due after a batch closes - fixes only, with a report the user approves. Use after /close-batch, or when the user says "run the passes" or names a pass.
---

# Passes between batches

Read `planning/PASSES.md` (the passes, their schedule, thresholds, baselines, last runs). No time estimates.

0. **A standards pass** (the coding standards over an existing code base, once): split by area, one agent per area in parallel, each applies the standards inside its area and lists renames that reach outside it; then one agent applies all the renames in one sweep (old file and config keys stay as aliases). The cleanup pass after that checks only the code changed since the last cleanup.
1. **Pick the due passes**: by schedule (batches since the last run), or at once when the last wave crossed a threshold (benchmark drop, memory growth), or the ones the user names. Tell the user which passes run and why.
2. **Write a pass file** for each: `planning/passes/YYYY-MM-DD-<pass>.md` with the goal, the baseline numbers, the limits, and an effort score (`EFFORT.md`).
3. **Brief one agent per pass**, in parallel, each in its own worktree and branch `pass-<pass>-<date>`, with:
   - **Fixes only.** No new features, no behaviour changes that a user would notice (except fixing a regression). Anything bigger goes to `planning/batches/proposed/` as a unit file.
   - Follow the code repo rules (tests first, deep modules, product docs in ASD-STE100).
   - Measure before and after with the same command, and report both numbers.
   - Run `date -u +%FT%TZ` at start and end; re-check the effort score.
   - Report: each fix (what, why, where), the numbers before and after, how to check it, proposed units.
4. **Log** each pass in the time log (kind `pass`) at launch, done, and merge.
5. **Merge** each pass branch, then run the full checks and benchmarks once.
6. **Report** in each pass file (`## Report`): the fixes, before and after, how to check. Update `PASSES.md`: the date of the run, the batch it followed, the new baselines.
7. **The workflow pass** is done by the coordinator, not an agent in a worktree: read the time log, the reviews, the pass reports and the word-vomit records since the last workflow pass; list what slowed things down or kept coming back; propose changes to the rules, skills, effort score, passes or batch size, each with its evidence and a recommendation (AskUserQuestion, recommendation first). Apply the approved ones, log each in `DECISIONS.md` under "Workflow changes", and commit the planning repo.
8. **Ask the user to approve** each pass (or write changes in its `## Review`; a change round fixes them). The next batch starts when the due passes are approved.

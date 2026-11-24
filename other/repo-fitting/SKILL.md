---
name: repo-fitting
description: "Use when a tracker step finds no repo config, or a repo lacks a guard it keeps needing: commit gate, import rules, git safety. Installing or editing config needs OK."
user-invocable: false
---
# Repo fitting
Gate: get the user's OK before installing packages, editing scripts, hooks, CI, repo config or instruction files, creating labels, or committing setup files (G2, G3). See gates.md in the skill house-rules.
Job: Fit a repo with one thing it needs, and prove it works.
Takes: a repo and a fitting.   Gives: recorded config or an installed guard, proven pass, fail, pass.

Other blocks call this block when they find something missing. They don't tell the user to set it up. A worker that needs a fitting stops and reports it under `Needs OK`.

## Steps

1. Name the one fitting and open its recipe in this skill's `recipes/` folder.

   | The repo needs | Recipe |
   |---|---|
   | Tracker, label and docs config | `recipes/tracker.md` |
   | Mechanical block on destructive git commands | `recipes/git-safety.md` |
   | Formatting, type and test checks at commit | `recipes/commit-gate.md` |
   | Package boundaries a machine enforces | `recipes/import-rules.md` |
   | Type casts gone from tests | `recipes/test-casts.md` |

2. Inspect before proposing anything: the toolchain, lockfiles, existing config for this fitting, hooks, CI, instruction files. Report what is already there. A guard that exists but doesn't run is a repair, not a new install.
3. Decide the smallest change that does the job. Ask only what inspection can't answer, one topic at a time, each with a recommendation.
4. Show the exact change: files, packages, config sections. Get the OK in the gate's form.
5. Apply it. Merge with what exists rather than overwrite. Keep every other section of a shared file intact. Edit the instruction file the repo already has, and never add a second one.
6. Prove it by observing all three states:
   - pass: the guard runs clean on the repo as it stands
   - fail: a real sample trips the guard, and the failure names the rule
   - pass: the sample is reverted and the guard runs clean again

   A fitting with nothing to trip, such as tracker config, proves itself with a real read through the mapping instead.
7. Commit only with an OK, and only the setup files.
8. Report what was added, where it lives, which state each proof reached, and what it doesn't cover.

## Done when

- The recipe's own finish condition is met.
- Pass, fail and pass were each observed on the real repo and appear in the report as `[observed]` with their commands.
- Nothing outside the fitting changed, and every surrounding section of a shared file is intact.
- Any sample used to trip the guard is reverted.
- Anything left uncovered is named: another host, a missing script, a CI step the user must add.

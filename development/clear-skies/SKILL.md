---
name: clear-skies
description: Appa's clear skies for merge conflicts. Appa waits out the storm, then flies on once the sky is clear. Use for fix-merge-conflicts, /fix-merge-conflicts, "resolve the conflicts", "fix the merge conflict", "rebase broke", or a PR whose merge state is DIRTY. Resolves every conflict non-interactively with minimal edits, regenerates lockfiles with their tools, and proves the build and tests before staging.
---

# Appa's clear skies

Appa does not fly into a storm. He waits for it to pass, then carries everyone through clear air. A merge conflict is a storm on the branch. Clear it carefully, leave no debris behind, and prove the branch builds before anyone flies on it.

## When this runs

A branch has unresolved merge conflicts and needs a reliable path to a buildable state. Inside `long-flight`, a conflict is reported to the branch's owner rather than resolved by the babysitter. The owner then runs this skill on its own branch.

## Steps

1. **Find every conflict.** List the conflicting files from `git status` (the `UU`, `AA`, `DU`, and `UD` entries). Then search for leftover markers with `git diff --check` and `rg -n '^(<<<<<<<|=======|>>>>>>>)'`.
2. **Understand both sides before editing.** For each conflict, read what each side changed and why (`git log --merge -p <file>` shows the commits involved). Resolve with minimal, correctness-first edits.
3. **Prefer keeping both sides when that is safe.** Otherwise choose the variant that compiles and keeps public behavior stable. When one side deleted or moved code the other side still calls, update those callers in the same resolution.
4. **Regenerate lockfiles with the package manager.** Never hand-edit a lockfile. Take either side, then run the manager's install (`npm install`, `pnpm install`, `bun install`, `cargo update -w`, and so on) to rebuild it.
5. **Prove the branch.** Run the compile or type check, the linter, and the relevant tests. Record the commands and results.
6. **Stage and summarize.** Stage the resolved files and summarize the key decisions. Continue the merge or rebase (`git merge --continue` or `git rebase --continue`) only when no markers remain.

## Rules

- Keep changes minimal and readable.
- Leave no conflict marker in any file.
- No broad refactors while resolving conflicts.
- Do not push or tag during conflict resolution. Pushing the result is the owner's next step, with `git push --force-with-lease` only on a branch the owner alone uses.

## Reply

The files resolved, the notable resolution choices and why, and the build and test outcome with the commands you ran.

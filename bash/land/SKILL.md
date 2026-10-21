---
name: land
description: Land a ready branch - push, PR, pinned CI watch, squash-merge, issue verification, cleanup. Use for every PR landing; encodes the run-ID pinning and cleanup discipline.
argument-hint: "<branch> [worktree-path]"
---

# Land a Branch

Take a committed branch through push → PR → CI → merge → cleanup. One invocation per branch; serialize when branches share files.

## Arguments

- `$ARGUMENTS` — branch name; optionally the worktree path holding it (default: search `git worktree list`).

## Pre-flight

1. `pwd` + `git branch --show-current` in the branch's checkout — **CWD drift is real**: finished background agents move the orchestrator's shell CWD. Anchor every command with explicit `cd`.
2. Branch is committed and clean (`git status --short` empty).
3. Merge current main in: `git fetch origin main && git merge origin/main`. On conflict in triage tables → union-of-flips; in tests → usually keep both.
4. Re-gate after the merge: targeted tests for touched modules (`cargo test --features cuda-index --lib <filter>` with a private `CARGO_TARGET_DIR`), and the provenance lint:
   ```bash
   git diff origin/main...HEAD -- '*.rs' | python3 scripts/check_comment_provenance.py
   ```
   CI diffs the merge ref, so MOVED comment lines count as added — a local pass on the pre-merge diff can be a false negative.

## Push and PR

5. Push: `git push origin <branch>` (direct WSL usually works; on "could not read Username" fall back to `powershell.exe -Command "cd C:\Projects\cqs; git push origin <branch>"`).
6. Body to `/mnt/c/Projects/cqs/pr_body.md` (NEVER inline; must live on C: for Windows gh). Include `closes #N` for every issue the branch resolves. Delete the file after.
7. `powershell.exe -Command 'cd C:\Projects\cqs; gh pr create --head <branch> --title "..." --body-file pr_body.md'`

## CI — pin the run ID

`gh pr checks --watch` latches onto the PREVIOUS commit's completed run. Always:

```bash
sleep 50   # new run needs ~45s to register
powershell.exe -Command 'gh run watch $(gh run list -R jamie8johnson/cqs --branch <branch> --workflow CI --limit 1 --json databaseId --jq ".[0].databaseId") -R jamie8johnson/cqs --exit-status'
```

Background this (run_in_background) and do other work; the notification carries the exit code.

## Merge and verify

8. On green: `powershell.exe -Command 'gh pr merge <N> -R jamie8johnson/cqs --squash --delete-branch'`, then confirm `gh pr view <N> --json state` == MERGED.
9. **Verify every linked issue actually closed** (`gh issue view <N> --json state`); close manually with a PR pointer if GitHub missed it. "Partially addresses" PRs: comment the remaining scope on the issue instead.
10. Cleanup: `cd /mnt/c/Projects/cqs && git pull origin main --ff-only`, `git worktree remove <path> --force`, `git branch -D <branch>`, `cqs index` (inotify misses bulk git ops on /mnt/c).

## On CI failure

Read the failing job log before touching anything (`gh run view <id> --log-failed`). Provenance-lint failures → scrub audit IDs from comments (state the invariant instead). Don't retry CI blind.

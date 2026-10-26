---
name: push
description: Push the current branch to origin (never force), verify it landed, and check on CI. Use when the user asks to push, or chained from /commit on "commit and push".
user-invocable: true
allowed-tools: Bash, Read, Grep
---

# /push — Publish the branch to origin

## Steps

### 1. Preflight

```powershell
git status --short          # must be clean — uncommitted work does not travel
git status -sb              # confirm the branch and how far ahead of origin
git log --oneline origin/<branch>..HEAD
```

If the tree is dirty, stop — that's `/commit`'s job first. Read the list of
commits about to publish; if any looks like it isn't this session's work,
say so before pushing.

### 2. Push — plain, never forced

```powershell
git push origin <current-branch>
```

- **Never `--force` / `--force-with-lease` to a shared branch** (hard rule).
- If the push is rejected non-fast-forward, someone else pushed: fetch,
  rebase or merge deliberately, re-run the checks, then push. Do not force
  through it.
- PowerShell quirk: git writes progress to stderr, so a *successful* push can
  surface as a NativeCommandError with a nonzero exit code. Judge success by
  the `old..new  branch -> branch` line and by step 3 — not by the exit code.

### 3. Verify it landed

```powershell
git status -sb    # branch must show level with origin (no "ahead")
```

### 4. Watch CI — and fix it if it fails

Every push runs `.github/workflows/checks.yml` (`tools.checks all` on a
Windows runner). A push is not "done" until that run is green — watch it:

```powershell
gh run list --branch <branch> --limit 1        # find the run this push started
gh run watch <run-id> --exit-status            # blocks until it finishes
```

(`gh run watch` can take 10–20 min on the Windows runner; run it in the
background and continue only non-code work meanwhile.)

**If the run fails:**

```powershell
gh run view <run-id> --log-failed              # the actual failing output
```

1. Diagnose from the real log — never guess. A local green with a red CI is
   environment drift (a missing workflow dep, a path assumption, a
   Windows-runner difference), and each is fixable in the workflow or code.
2. Fix it, re-run the relevant local check, `/commit`, push again, watch
   again. Loop until green.
3. If the failure is in something you cannot fix from here (billing, runner
   outage, permissions), report exactly what the log says and stop.

While `docs/simon-handover/readiness-checklist.md` still has an open CI row,
the first green run is what ticks it.

## Never

- push with a dirty tree, or force-push a shared branch
- push around a failed local check "to see what CI says"
- declare a push done while its CI run is red or still unwatched

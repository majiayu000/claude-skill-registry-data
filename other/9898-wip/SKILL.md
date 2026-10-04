---
name: wip
description: >-
    Run on /wip or for a whole-repository cleanup spanning multiple worktrees and branches. Trigger
    when the request combines operations such as removing stale worktrees, rebasing all branches,
    retesting, and pushing, including "clean up my worktrees and branches", "rebase all my branches
    and get them tested and pushed", or "settle my WIP". The workflow gates destructive and
    outward-facing actions, never uses --force, and handles worktree, rebase, and test edge cases.
    Defer to single-operation git skills when the user targets one specific branch or worktree.
    Wraps git:clean-worktrees and build:test-all.
---

# /wip — work-in-progress cleanup pipeline

Drive a repo full of leftover worktrees and half-finished branches toward a clean, landed state. Four phases run in order, each gated:

- **Worktrees**: remove every worktree except the main and protected ones, freeing their branches.
- **Rebase + GC**: rebase every branch onto upstream main (`j g` / `git-all`) and delete merged branches.
- **Test**: retest the rebased commits.
- **Push**: push the green branches. The user opens and merges PRs.

Opening PRs, CI, review, and merging are the user's call. If the repo or user documents a WIP state model, follow it for those stages.

## Golden Rules

- **Never `--force`.** Remove worktrees with `git worktree remove --no-force` (write the flag explicitly) and push with a pinned `--force-with-lease`. Git's refusal is the safety net for uncommitted work and unexpected remote changes.
- **The worktree and branch set is a moving target.** Other agents and the user create, switch, and merge while you work. Recompute with `git worktree list --porcelain` / `git for-each-ref` immediately before each action, and re-`git fetch` before testing and pushing.
- **Gate irreversible and outward-facing steps.** Removing a worktree with WIP, force-pushing, and `delete-merged` (which deletes remote branches) need the user's OK. Until the flow is proven smooth in a repo, ask at each phase boundary.
- **Keep the main checkout clean.** Rebases and tests check out commits, so run them in throwaway worktrees (`git worktree add`) and tear those down afterward.

## Protected Worktrees

The main worktree is the first entry of `git worktree list --porcelain` (the one whose gitdir is `git rev-parse --git-common-dir`). Never remove it.

Permanent worktrees are listed per repo in `.llm/wip.json`:

```json
{"protectedWorktrees": ["/Users/you/projects/some-permanent-worktree"]}
```

If the file is missing, only the main worktree is protected, but ask before removing any long-lived worktree you're unsure about. `git worktree lock` also works, since a locked worktree can't be removed without `--force`.

## Phase 1 — Worktree Cleanup

- Compute the removal set live: `git worktree list --porcelain` minus main minus protected. Use plain `git worktree list`, never a user shell alias like `git worktrees`.
- Remove them one at a time from the main repo via the `git:clean-worktrees` skill, writing the flag explicitly: `git -C <main> worktree remove --no-force <dir>`.
- Stop on the first failure and never retry with `--force`. A dirty worktree fails with `fatal: '<dir>' contains modified or untracked files, use --force to delete it` (exit 128). Show `git -C <dir> status --short` and ask whether to **commit** the WIP (single line, via `git:commit`), **stash** it, or **leave** the worktree.
- A brand-new clean, empty worktree (0 commits ahead, no changes) is probably someone about to start work. Surface it rather than deleting it.
- Finish with `git -C <main> worktree prune --verbose`.

## Phase 2 — Rebase Every Branch + GC

Use the `git-all` script (`rebase-all` → `git worktree prune` → `delete-merged`; the user may alias it as `j g`) rather than bare `rebase-all`, so merged branches get cleaned up. It needs `UPSTREAM_REMOTE` (default `upstream`; many repos use `origin`, so check `git remote -v` and the project's `.envrc`). `origin/main` in these examples and in `references/pipeline.md` stands for `$UPSTREAM_REMOTE/main`. Substitute it when the upstream isn't `origin`, or every rebase and "all clean" check runs against a stale base and silently reports success.

- **Report the scope first.** Every local branch not containing upstream main can be dozens (stale `dev`, `main4`, experiments, `pr*-fix`). Count them and let the user confirm.
- **Conflicts.** `git-all` halts on the first conflict mid-rebase. Resolve genuine conflicts with the `git:conflicts` skill. Verify `git rerere` replays rather than trusting them, and beware false-positive conflict-marker greps in files that legitimately contain `=======` (ASCII banners, markdown headings).
- **`delete-merged` is outward-facing.** It also runs `git push --delete origin <branch>` for merged remote branches (excluding main/HEAD/`origin/pr/*`). Gate it.

Read `references/pipeline.md` before this phase. It covers the co-pointed-branch fallback (when several branch names point at one commit, `rebase-all` skips them all and you must rebase the leftovers directly) and the worktree-per-branch parallel rebase.

Afterward, `git for-each-ref refs/heads/ --no-contains origin/main` should be empty.

## Phase 3 — Test the Rebased Commits

Rebasing invalidates prior test results, so every rebased branch needs a retest. Re-`git fetch` first.

Run `build:test-all` (per branch: `git test run <FLAGS> origin/main..BRANCH`) in a dedicated worktree, since git-test checks out each commit. See `references/pipeline.md` for the worktree and env setup and the flaky-retest rule.

## Phase 4 — Push Only

Record each branch's remote sha (`git rev-parse refs/remotes/origin/<branch>`) before re-`git fetch`ing, then push every branch ahead of upstream main:

- If `refs/remotes/origin/<branch>` exists: `git push --force-with-lease=<branch>:<recorded-sha> origin <branch>:<branch>`. Pin the sha: a bare `--force-with-lease` baselines on the remote-tracking ref, which the re-fetch just advanced, so it would clobber a teammate's new commit instead of refusing.
- Otherwise: `git push origin <branch>:<branch>`.

Don't open or merge PRs unless asked. Expect per-push permission prompts.

## Ask vs. Automate

Automate: detecting main, reading the protected list, computing sets live, `worktree remove --no-force`, `worktree prune`, clean rebases, tests, and pinned `--force-with-lease` pushes of branches the user has scoped.

Ask: what to do with a dirty worktree, whether to remove a brand-new one, the scope of a big rebase or push batch, how to resolve a genuine conflict, and any outward step (`delete-merged`, force-push, merge).

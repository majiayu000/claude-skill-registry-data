---
name: github-workflow
description: "The git and GitHub SOP for Struq Voice: branch, commit, open a PR, and merge. Use whenever a task involves committing, branching, a pull request, 'ship this', 'commit this', 'open a PR', 'land this', merging, or when finished work needs to reach main. Covers the branch-per-change rule, one branch in flight, conventional commits, which verification tier decides who may merge, the PR body and its probe, merge versus squash, and what an agent must never do to git. NOT for cutting a version or publishing a release (use shipping-a-release) or for the gate commands themselves (use verification-gates)."
argument-hint: "[branch | commit | pr | merge]"
---

# Git and GitHub SOP for Struq Voice

The only authority in this repo for branches, commits, PRs and merges.

## Start

1. Inspect `git status` and the current branch before touching anything.
2. **Preserve unrelated changes.** Never reset, stash or discard work you did
   not create. If the worktree is dirty with someone else's work, stage
   explicit paths rather than `git add -A`.
3. Branch from an updated `main`. Never stack feature branches.
4. **One branch in flight.** Land it before cutting the next. Every extra day
   a branch stays open grows the surface it can collide on.
5. **Size a branch to one verification sitting.** If Roy cannot check it in
   fifteen minutes it is too big, and a branch he cannot check is a branch
   that waits.

```bash
git switch main && git pull
git switch -c <type>/<short-description>
```

Do these without asking. **Never commit directly to `main`.**

## The tier decides who merges

From the `verification-gates` skill, repeated here only as the merge rule:

| Tier | Touches | Who merges |
|---|---|---|
| T1 | docs, copy, screenshots, comments | the agent, once gates and CI are green |
| T2 | renderer views, state machines, IPC, engines | Roy |
| T3 | native modules, updater, paste, meeting worker, release scripts | Roy |

**T1 is the only tier an agent may merge**, and it is narrow on purpose. If
the change alters behavior a person could notice, it is not T1. Approval to
implement, commit, push or open a PR is **not** merge approval.

## Commit

- Conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`,
  `chore:`, `build:`.
- **One concern per commit.** A screenshot refresh and a crash fix are two
  commits even when they were written in the same sitting.
- Commit completed slices as you go, not one final bundle.
- Stage explicit paths when the worktree carries unrelated work.
- Explain **why** in the body, not just what. The diff already says what.
- No agent-specific authorship or co-author trailers.
- Record only checks actually observed.

## Docs move in the SAME commit

If the running system changed, its doc changes with it. Not a follow-up.

| Change | Also update |
|---|---|
| An IPC channel added or renamed | `src/shared/ipc.ts` is the source; check the `ipc-architecture` skill still describes it |
| A new view or user-visible capability | `docs/FEATURES.md` |
| Release, signing or update behavior | `docs/RELEASING.md` |
| A native module or its degradation path | `docs/TROUBLESHOOTING.md`, `native-modules` skill |
| A new invariant or boundary | `AGENTS.md` |
| A repeated failure that cost real time | `docs/TROUBLESHOOTING.md`: symptom, cause, fix |

## Open the PR

```bash
git push -u origin <branch>
gh pr create --base main --head <branch> --title "..." --body "..."
```

Open it only after the branch is complete and gated. The body states the
goal, what changed, the tier, the checks that were run, the risks, and
anything **not** verified.

**Give it a probe**: the exact commands or clicks that prove it,
copy-pasteable, so verification is five minutes of following instructions
rather than five minutes of working out what to try.

**Stop after opening the PR unless the branch is T1 and green.**

## Merge

| Situation | Do this |
|---|---|
| branch is behind `main` | `git merge main` |
| landing **more than one logical change** | `gh pr merge --merge --delete-branch` |
| landing **one logical change** | `gh pr merge --squash --delete-branch` |
| undoing something that landed | `git revert -m 1 <merge sha>`, or `git revert` the squash commit |

**The test is what the branch IS, not how big it is.** A multi-slice branch is
several decisions that happened to travel together; squash it and a later
`git bisect` lands on one commit touching nine files and says "somewhere in
here". Merge it and the same bisect names the slice and hands you forty lines.

`git log --first-parent main` already gives the one-line-per-PR changelog
view, so the tidy-log argument for squashing costs something and buys nothing.

Whichever is used, it cannot be changed afterwards without force-pushing
`main`, which is forbidden. Choose before the merge button.

After merge:

1. Confirm the PR merged.
2. Switch to `main` and fast-forward.
3. Delete the merged local branch, and the remote one if the PR did not.
4. Confirm the worktree is clean.

## What an agent never does to git

- Commit or push to `main` directly. Every change arrives as a PR, because a
  PR is one revertible unit.
- Force-push, or rewrite any pushed commit.
- Reset, stash or discard work it did not create.
- Merge a T2 or T3 branch without Roy approving that exact PR.
- Claim a gate passed without pasting what it printed.
- Move a version by hand. `package.json`, the `v*` tag, `main` and the update
  feed are one fact in four places. Only the release pipeline changes them;
  see the `shipping-a-release` skill.

Locally, `git reflog` plus `git reset --hard <sha>` recovers any position HEAD
held for 90 days. That is what makes local mistakes cheap and pushed rewrites
expensive.

## Two rules that are easy to get wrong

**If a command can answer it, a doc does not get to assert it.** What landed
is `git log`. Whether a branch is merged is
`git rev-list --count main..<branch>`. A file named for state goes stale.

**Never commit secrets.** No API keys in code, in logs, or across IPC. If one
is exposed: revoke first, explain second.

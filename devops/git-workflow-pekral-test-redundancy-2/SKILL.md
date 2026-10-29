---
name: git-workflow
description: "Use when choosing a Git branching strategy or handling merge vs rebase, conflicts, undoing mistakes, and release tagging — complementing the commit/PR conventions in the git rules."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Commit, PR, and merge conventions live in `@rules/git/general.md` — English `type(scope)` commits, lowercase, no trailing period, no push to `main`, `Closes #` issue linking, English PR titles, rebase-and-merge, `gh` CLI. This skill does NOT restate them.
- Branch cleanup is owned by `@skills/cleanup-local-branches/SKILL.md`. Defer to it; do not duplicate.
- PR merging is owned by `@skills/merge-github-pr/SKILL.md`. Defer to it; do not duplicate.
- This skill covers only the complementary gaps below.

## Use when
- Choosing or changing a branching strategy.
- Deciding merge vs rebase for a specific situation.
- Resolving a merge conflict.
- Undoing a mistake (bad commit, wrong reset, accidental change).
- Cutting a release and tagging a version.

## Branching strategies

### GitHub Flow (simple, recommended for most)
`main` is always deployable. Branch from `main`, open a PR, merge after review and green CI, deploy. Best for SaaS and web apps with continuous deployment.

### Trunk-based (high-velocity)
Everyone integrates into `main` via very short-lived branches (1–2 days). Incomplete work hides behind feature flags. CI must pass before merge. Needs strong CI/CD and discipline.

### GitFlow (release-cycle driven)
`main` holds production code, `develop` is the integration branch, with `release/*` and `hotfix/*` branches. Heavyweight; only worth it for scheduled, regulated releases.

| Strategy | Team size | Release cadence | Best for |
|----------|-----------|-----------------|----------|
| GitHub Flow | any | continuous | SaaS, web apps, startups |
| Trunk-based | 5+ experienced | multiple/day | high-velocity teams using feature flags |
| GitFlow | 10+ | scheduled | enterprise, regulated industries |

Default to GitHub Flow unless the team has a concrete reason for another model. It aligns with the rebase-and-merge + short-focused-branches conventions in `@rules/git/general.md`.

## Merge vs rebase mechanics

### Merge (preserves history)
```bash
git checkout main
git merge feature/user-auth   # creates a merge commit
```
Use when preserving exact history matters or several people worked on the branch.

### Rebase (linear history)
```bash
git checkout feature/user-auth
git fetch origin
git rebase "origin/$DEFAULT_BRANCH"   # replays your commits on top of the default branch
```
Use to update your local branch with the latest default branch before opening or refreshing a PR. Keeps history linear. Resolve `DEFAULT_BRANCH` as in *Pull policy* below; never hardcode `origin/main`.

```bash
# only if you are the sole contributor on the branch
git push --force-with-lease origin feature/user-auth
```
Always `--force-with-lease`, never plain `--force`.

### Pull policy: sync a side branch before pulling it
`@rules/git/general.md` *Pull Policy* requires every non-default branch to be rebased onto the latest default branch so it always carries the newest default-branch history. The default branch is `main` on some repos and `master` on others — resolve it instead of hardcoding `origin/main` (which does not exist on a `master`-default repo and makes the command fail). Order matters: take the branch's own remote **first**, then rebase the default branch in, then force-push — do not pull again afterwards.
```bash
DEFAULT_BRANCH="$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's@^origin/@@')"
git checkout feature/user-auth
git fetch origin
git pull --rebase                     # 1) take the branch's own remote first
git rebase "origin/$DEFAULT_BRANCH"   # 2) bring the latest default branch in
# resolve conflicts if any, then: git rebase --continue
git push --force-with-lease           # 3) publish; do NOT git pull again — it would undo the rebase
```
The rebase in step 2 replayed every commit onto a different base, so the head commit now has a tree that was never gated. That is caught at the merge boundary: `@rules/git/general.md` *The merged head is green; intermediate commits are not gated* runs the project's gate on the new head before the merge, and a reshaped branch never inherits an earlier verdict.
The one exception is a rebase that only moved the base and brought in changes unrelated to the branch, per `@skills/resolve-issue/references/quality-gates.md` *Rebase that moves the head — analyse the incoming changes first*. Replaying the whole range with `git rebase --exec '<the project gate>' <base>` is available when a bisectable history is wanted. `<the project gate>` is the project's gate command, discovered per `@skills/resolve-issue/references/quality-gates.md`.

Run that replay only when you actually want a bisectable history — it executes the whole gate once per commit, which is the cost the single end-of-work gate exists to avoid:

```bash
git rebase --exec '<the project gate>' "origin/$DEFAULT_BRANCH"   # optional; stops on the first commit that fails
```
If the rebase changed `composer.lock` (the default branch updated dependencies), reinstall before continuing so the installed packages match the new lockfile:
```bash
composer install                      # run only when composer.lock actually changed
```
The default branch itself is exempt — pull it directly with `git pull`. Read-only review skills are exempt too: they `git pull` only to read the diff and never rebase.

### Never rebase shared/public history
Do NOT rebase a branch that has been pushed and that others may have based work on, nor any protected branch (`main`, `develop`), nor already-merged history. Rebase rewrites commits and breaks everyone downstream. For published branches, fix forward with `git revert` instead.

## Conflict resolution

A conflict is a question about **intent**, not a formatting problem. Both sides compiled and passed review on their own branch; the merge is where you decide what the combined codebase should mean. Resolve it in this order — the commands are the last step, not the first.

**1. See the current state.** `git status` lists the conflicted files; `git log --merge -p <file>` shows only the commits that touched the conflicting hunks from both sides.

**2. Find the primary source of each side.** Read the commit message, the PR, and the linked issue for both branches. A hunk you cannot explain is a hunk you cannot resolve — you can only guess, and a guess here silently reverts someone's work.

**3. Resolve each hunk.** Preserve both intents wherever they are compatible. Where they genuinely conflict, keep the one matching the merge's stated goal and record the trade-off in the merge commit body. **Never invent new behaviour in a conflict resolution** — a merge commit is the worst place to introduce a change nobody reviewed, because reviewers read the diff against each parent and a third behaviour appears in neither.

**4. Run the tests covering the conflicted code.** Use the project's own test command, discovered per `@skills/resolve-issue/references/quality-gates.md`. A conflict resolved to something that compiles is not the same as one resolved correctly; the tests are what tell the two apart. The full gate runs once at the merge boundary (see *Hooks* below).

**5. Finish.** Stage and continue (`git commit` for a merge, `git rebase --continue` for a rebase, repeating until every commit is replayed).

```bash
git status                       # 1. which files conflict
git log --merge -p path/to/file  # 2. the commits behind this hunk

# 3. Edit each file. Markers:
#    <<<<<<< HEAD ... ======= ... >>>>>>> feature/user-auth
#    Delete all three markers — a committed marker breaks the file silently.

# Accept one whole side ONLY when you have established that side is complete:
git checkout --ours  path/to/file    # keep current branch version
git checkout --theirs path/to/file   # keep incoming version

git add path/to/file             # 4. after the covering tests pass
git commit                       # 5. merge
git rebase --continue            #    or rebase, until all commits are replayed
```

**`--ours` / `--theirs` discard a whole file.** They are a shortcut for "that side's version is already correct in full", which you must have verified. During a **rebase** the two are inverted relative to a merge — `--ours` is the branch being rebased onto, `--theirs` is your own work — so reaching for them from muscle memory mid-rebase is how a branch loses its own changes.

**Aborting is a decision, not an escape.** `git merge --abort` / `git rebase --abort` are correct when the merge itself was wrong (wrong base, wrong branch, or a scope you now know needs splitting). They are not a way out of a conflict that is merely hard — abandoning the resolution leaves the same conflict for the next person with less context than you have now. Abort deliberately, and say why.

Prevention: keep branches small and short-lived, rebase onto the default branch frequently, and coordinate before touching shared files.

Adapted from [mattpocock/skills — resolving-merge-conflicts](https://github.com/mattpocock/skills/blob/main/skills/engineering/resolving-merge-conflicts/SKILL.md).

## Undoing mistakes
```bash
# Undo the last commit, keep the changes staged
git reset --soft HEAD~1

# Undo the last commit AND discard the changes (destructive)
git reset --hard HEAD~1

# Reverse an already-pushed commit safely (public-history safe)
git revert <sha>

# Fix the last commit message
git commit --amend -m "feat(auth): correct subject"

# Add a forgotten file to the last commit (only before it is pushed)
git add forgotten-file
git commit --amend --no-edit

# Restore a single file to its committed state
git checkout HEAD -- path/to/file
```
Rule: `reset --hard` and `--amend` rewrite history — safe only on unpushed, local-only commits. Once pushed and shared, undo with `revert`.

## Semantic versioning and release tagging
`MAJOR.MINOR.PATCH`: MAJOR for breaking changes, MINOR for backward-compatible features, PATCH for backward-compatible fixes.

```bash
git tag -a v1.2.0 -m "Release v1.2.0"   # annotated tag
git push origin v1.2.0
git tag -l                               # list tags
git tag -d v1.2.0 && git push origin --delete v1.2.0   # remove a tag

# Draft release notes from the commit range
git log v1.1.0..v1.2.0 --oneline --no-merges
```
Conventional `type(scope)` subjects from `@rules/git/general.md` make this changelog range readable.

## Laravel .gitignore essentials
```gitignore
/vendor/
/node_modules/
.env
.env.*.local
/public/build
/storage/*.key
.phpunit.result.cache
.DS_Store
```
Never commit `.env`, the `vendor/` or `node_modules/` trees, the Vite build output in `/public/build`, or generated keys.

## Hooks
A pre-commit or pre-push hook must **not** run the project's full gate — that gate runs once at the end of the work (`@skills/resolve-issue/references/quality-gates.md` *Gate placement — deferred to the merge boundary*), and a hook repeating it per push is exactly the cost that placement removes. A hook that runs only the tests covering the change is fine; use the project's own test command rather than ad-hoc tooling.

## Defer to
- `@rules/git/general.md` — commit, PR, and merge conventions.
- `@skills/cleanup-local-branches/SKILL.md` — deleting stale local branches.
- `@skills/merge-github-pr/SKILL.md` — merging a ready PR.

## Done when
- A branching strategy is chosen with a stated reason.
- Merge vs rebase is applied correctly and no shared/public history was rebased.
- A non-default branch was synced (own remote pulled, then the resolved default branch rebased in, then force-pushed — never hardcoding `origin/main`), and `composer install` was re-run whenever that rebase changed `composer.lock`.
- Conflicts are resolved with markers removed and project checks re-run.
- Any undo used the right tool for whether the commit was pushed.
- Releases are tagged with annotated semver tags pushed to origin.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.

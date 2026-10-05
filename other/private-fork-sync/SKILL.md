---
name: private-fork-sync
description: Make a public GitHub fork private and keep it synced with its upstream parent. Use when the user wants to make a fork private, or to pull/sync newer commits from the upstream parent into their fork.
---

Convert a fork's visibility to private, then keep it current by fetching from the parent. The whole workflow stays effortless on one condition: the fork's default branch is a **clean mirror** of upstream, so every sync is a **fast-forward** — no merge commits, no conflicts.

Prerequisite: `gh` authenticated with `repo` scope, plus a local clone of the fork. Examples use `master`; if the repo's default branch is `main`, substitute it (`gh repo view <owner>/<fork> --json defaultBranchRef -q .defaultBranchRef.name`).

## Make a fork private

GitHub now converts a fork's visibility in place — historically this was blocked, which is why mirror-clone workarounds still circulate; you don't need them.

```
gh repo edit <owner>/<fork> --visibility private --accept-visibility-change-consequences
```

`--accept-visibility-change-consequences` is required, and the command prints nothing on success.

Completion: `gh repo view <owner>/<fork> --json visibility,isPrivate` reports `PRIVATE` / `true`.

Tell the user two consequences:
- While private, you can't open PRs from the fork to the public parent. Reverse with `--visibility public --accept-visibility-change-consequences` when you want to contribute upstream.
- Anyone who could see the public fork now needs to be added as a collaborator.

If the direct change is ever rejected (e.g. org policy), fall back to the documented mirror method: create a new private repo, then `git clone --bare` the fork and `git push --mirror` into it.

## Set up syncing (one-time)

Add the parent as a fetch-only `upstream` remote, with push disabled so you can never accidentally push to a repo you don't own:

```
git remote add upstream https://github.com/<parent-owner>/<repo>.git
git remote set-url --push upstream DISABLE
git fetch upstream
```

Completion: `git remote -v` shows `upstream` fetch plus push URL `DISABLE`.

## Sync when upstream has new commits

```
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

One-liner alternative (relies on the same **clean mirror** condition): `gh repo sync <owner>/<fork> -b master` then `git pull origin master`.

Completion: `git rev-list --left-right --count master...upstream/master` prints `0	0` (local neither ahead nor behind).

## Keep the mirror clean

The **fast-forward** guarantee holds only while `master` carries no commits of your own. Custom work goes on a separate branch, never on the mirror branch:

```
git switch -c my-changes        # do your work here, not on master
git switch my-changes && git rebase master   # pick up upstream after each sync
```

If `master` has already diverged, `git rev-list` above shows a nonzero left count and the merge stops fast-forwarding — move those commits onto a branch and hard-reset `master` to `upstream/master` to restore the mirror.

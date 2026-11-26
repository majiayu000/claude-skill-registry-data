---
name: "exp-start"
description: "Create or join an experiment branch. Experiments run on short-lived `exp/<slug>` branches in a dedicated worktree. They never merge to `main` and neve"
---

# exp-start command

Apply this command workflow. Treat any text after its invocation as the command input.

Create or join an experiment branch. Experiments run on short-lived `exp/<slug>` branches in a dedicated worktree. They never merge to `main` and never get PRs or issues. Keepers are distilled onto `gh-*` branches via `/gh-issue-push` + `/gh-issue-pop`.

Two modes:

- **Local-only** (default): the experiment lives entirely on this repository's `origin`.
- **Remote-backed** (`--remote`): the experiment additionally syncs two ways with a separate repository through `git subtree` — remote content lives under a deterministic prefix inside the experiment branch, and local changes to that prefix can be pushed back.

## Input

$ARGUMENTS

Syntax: `<slug> [--remote <url-or-owner/repo>] [--branch <upstream-branch>] [--prefix <path>]`

The slug is kebab-case (e.g. `transformer-perf`). `--remote` accepts a full Git URL or `owner/repo` shorthand (normalized to `https://github.com/owner/repo.git`). `--branch` names the upstream branch to sync with (default: the remote's default branch). `--prefix` sets the subtree path (default: `experiments/<slug>`). If no slug is given, ask the user for one.

## Phase 1 -- Validate

1. Validate the slug is kebab-case (`[a-z0-9]+(-[a-z0-9]+)*`). Reject anything else.
2. If `--remote` is given, normalize it: `owner/repo` becomes `https://github.com/owner/repo.git`; URLs pass through. Record `REMOTE_URL`.
3. Confirm we are in the main repo directory, not inside a worktree, and the current branch is `main`:
   ```bash
   git branch --show-current
   ```
   If not on `main`, warn the user and stop. Experiment branches are created from the main repo only.

## Phase 2 -- Create or join

```bash
git fetch origin
git ls-remote --heads origin exp/<slug>     # does it already exist?
```

**Join** (the branch exists): create the worktree with the git-crypt-aware
sequence — the conditional is a no-op in an unenrolled repository:

```bash
git worktree add --no-checkout ../exp-<slug> exp/<slug>
if [ -d .git/git-crypt ]; then ln -s ../../git-crypt .git/worktrees/exp-<slug>/git-crypt; fi
git -C ../exp-<slug> checkout exp/<slug>
```

If
the worktree holds `.exp-sync.yaml`, it is remote-backed — read it and rebuild
the sync remote on this machine from its `remote_name` and `remote_url`
(Phase 3 step 2). Report the join and print the Phase 4 sync commands.

**Create** (it does not): branch, init beads, commit the marker.

```bash
git worktree add --no-checkout ../exp-<slug> -b exp/<slug>
if [ -d .git/git-crypt ]; then ln -s ../../git-crypt .git/worktrees/exp-<slug>/git-crypt; fi
git -C ../exp-<slug> checkout    # the conditional serves git-crypt repos; a no-op elsewhere
cd ../exp-<slug>
bd init
git add -A
git commit -m "exp/<slug>: initialize experiment

Skill: exp-start
Called-by: <invoking skill, or 'user'>"
git push -u origin exp/<slug>
```

## Phase 3 -- Remote-Backed Setup (only with --remote)

All commands run inside the worktree at `../exp-<slug>`.

1. Determine the upstream branch. If `--branch` was given, use it. Otherwise detect the remote's default branch:
   ```bash
   git ls-remote --symref <REMOTE_URL> HEAD | sed -n 's|^ref: refs/heads/\(.*\)\tHEAD|\1|p'
   ```
   Record `UPSTREAM_BRANCH`.

2. Add the sync remote under a deterministic name and fetch it:
   ```bash
   git remote add exp-<slug>-remote <REMOTE_URL> 2>/dev/null || true
   git fetch exp-<slug>-remote
   ```

3. Add the subtree under the prefix (default `experiments/<slug>`):
   ```bash
   git subtree add --prefix=<prefix> exp-<slug>-remote <UPSTREAM_BRANCH> --squash
   ```

4. Record the sync metadata so any machine can rejoin and continue syncing. Write `.exp-sync.yaml` at the worktree root:
   ```yaml
   slug: <slug>
   remote_name: exp-<slug>-remote
   remote_url: <REMOTE_URL>
   upstream_branch: <UPSTREAM_BRANCH>
   prefix: <prefix>
   push_branch: exp/<slug>
   ```
   The `push_branch` is the branch created **in the remote repository** when local subtree changes are pushed back; it follows the same never-merge convention there.

5. Commit and push the metadata and initial subtree state:
   ```bash
   git add .exp-sync.yaml
   git commit -m "exp/<slug>: configure subtree sync with <REMOTE_URL>

   Skill: exp-start
   Called-by: user"
   git push
   ```

## Phase 4 -- Ongoing Two-Way Sync (remote-backed)

Subtree operations always name the remote and branch explicitly, so plain `git push`/`git pull` stay unambiguous: they talk only to this repository's `origin` and the `exp/<slug>` branch, never to the sync remote.

Pull remote updates into the prefix:

```bash
cd ../exp-<slug>
git fetch exp-<slug>-remote
git subtree pull --prefix=<prefix> exp-<slug>-remote <UPSTREAM_BRANCH> --squash
git push   # share the merged state on origin exp/<slug>
```

Push local subtree changes back to the remote repository:

```bash
cd ../exp-<slug>
git subtree push --prefix=<prefix> exp-<slug>-remote exp/<slug>
```

This creates or updates branch `exp/<slug>` in the remote repository. It never touches the remote's default branch; landing changes there is the remote repo's own review flow, out of scope here.

## Phase 5 -- Report

Print the worktree path and the convention reminders:

```
Experiment ready at ../exp-<slug> (branch exp/<slug>).
<if remote-backed:>
Syncing with <REMOTE_URL> (<UPSTREAM_BRANCH>) under <prefix>/.
  pull:  git subtree pull --prefix=<prefix> exp-<slug>-remote <UPSTREAM_BRANCH> --squash
  push:  git subtree push --prefix=<prefix> exp-<slug>-remote exp/<slug>

Reminders:
- Never merge exp/* to main. Never open a PR or GitHub issue from it.
- Treat every push as potentially permanent — no secrets or sensitive data.
  Remote-backed: subtree pushes land in the OTHER repository and survive
  local cleanup.
- To keep a result, distill it onto a gh-* branch via /gh-issue-push + /gh-issue-pop.
- To conclude the experiment, run /exp-stop <slug>.
- On other machines, run /exp-start <slug> to join this experiment
  (remote-backed sync reconstructs itself from .exp-sync.yaml).
```

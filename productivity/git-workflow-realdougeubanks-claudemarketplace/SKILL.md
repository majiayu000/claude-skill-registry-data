---
name: git-workflow
description: "Enforces the release-branch Git model: scaffold feature branches, open PRs with review checks, cut releases with tags, and view workflow reference."
argument-hint: "[start | pr | release | conflict | stash]"
allowed-tools: Read, Glob, Edit, Bash
---

# Git Workflow — Release-Branch Model

Enforce the release-branch Git model and help execute the correct git operations for your current context: start new work, open a PR, cut a release, or view the workflow reference.

## Hard Rules (always enforced, no exceptions)

- **Never commit or push directly to `main`.** If the current branch is `main`, stop and create a new branch before making any changes.
- **Never force-push to `main`.**
- All changes must reach `main` via a PR from a release branch.

## Instructions

When invoked, ask the user what they want to do (if not already specified):

> "What would you like to do?
> (a) View the Git workflow reference
> (b) Start new work — scaffold a feature or fix branch
> (c) Open a PR for the current branch
> (d) Cut a release — merge release branch to main and tag
> (e) Resolve a merge conflict on the current branch
> (f) Manage stashes — list, view, apply, or drop stashes"

Then execute the appropriate action below.

---

### Action (a) — View Workflow Reference

Print the full Git Workflow Reference section below.

---

### Action (b) — Start New Work

1. Use Bash to identify the current release branch:
   ```bash
   git branch -r | grep release | sort -V | tail -1
   ```

   **No-release-branch fallback:** If the command above returns no output (no `release/*` branch exists), fall back to branching from `main` and target `main` for the PR. Inform the user:
   > "No release branch found. Branching from `main` and the PR will target `main` directly. This is normal for simple repos and early-stage projects that do not yet use the release-branch model."
   In this case, replace `origin/<release-branch>` in step 4 with `origin/main`, and use `--base main` in the `gh pr create` call in Action (c).

2. Ask the user:
   - Is this a new **feature** or a **bug fix**? (determines `feature/` vs `fix/` prefix)
   - What is the task ID or short description? (e.g. `task-042`, `login-crash`)

3. Construct the branch name: `feature/task-XXX-short-description` or `fix/task-XXX-short-description`.

4. Use Bash to fetch the latest remote state, then create and check out the branch from the release branch:
   ```bash
   git fetch origin
   git checkout -b <branch-name> origin/<release-branch>
   ```
   Without the fetch, a stale remote-tracking ref would create the branch off an old tip.

5. Confirm the branch was created and remind the user:
   - Never commit directly to `main` or the release branch.
   - Open a PR from this branch into the release branch when work is complete.

---

### Action (c) — Open a PR

1. Use Bash to check the current branch and recent commits:
   ```bash
   git branch --show-current
   git log --oneline -10
   ```

2. Use Glob to check if `handoffs/reviews/` exists. If it does, use Read on any open review artifacts to check for unresolved findings with `severity: critical | severe | moderate`. If any exist, **block the PR** and inform the user these must be resolved first.

3. Use Bash to identify the target release branch:
   ```bash
   git branch -r | grep release | sort -V | tail -1
   ```

4. Use Read to check `handoffs/plans/` for context to include in the PR description.

5. Produce a PR description with: summary of changes, related task IDs, testing notes. Then use Bash:
   ```bash
   gh pr create --title "<title>" --body "<description>" --base <release-branch>
   ```
   If `gh` is not available, print the PR body for the user to paste manually.

---

### Action (d) — Cut a Release

1. Use Bash to confirm the current release branch is clean and all PRs are merged:
   ```bash
   git status
   git log --oneline origin/main..HEAD
   ```

2. Ask the user for the version tag (e.g. `1.0.0`).

3. Open a release PR from the release branch into `main` — all changes reach `main` via PR, including releases:
   ```bash
   gh pr create --base main --head release/<version> --title "Release v<version>" --body "<release summary>"
   ```
   If `gh` is not available, print the PR body and ask the user to open the PR manually.

4. After the PR is approved and merged, tag the release on `main`. Confirm before pushing the tag:
   ```bash
   git checkout main
   git pull origin main
   git tag v<version>
   git push origin v<version>
   ```

5. Remind the user to invoke `/abd-docs` (or the Documentation agent) to create the changelog for this release in `docs/CHANGELOG.md` or `docs/changelogs/<version>.md`.

---

### Action (e) — Resolve a Merge Conflict

1. Use Bash to identify all conflicted files:
   ```bash
   git status
   ```
   List each file that shows `both modified`, `deleted by us`, `deleted by them`, or any other conflict marker.

2. Use Bash to fetch the latest remote state and show how far behind the current branch is:
   ```bash
   git fetch origin
   git log --oneline HEAD..origin/$(git branch --show-current)
   ```
   Report how many commits the remote is ahead. If the remote branch no longer exists, note that and continue with local conflict resolution.

3. Ask the user whether to **rebase** or **merge** to incorporate upstream changes, and explain the tradeoffs:
   > - **Rebase** (`git rebase origin/<branch>`): rewrites your local commits on top of the upstream tip, producing a linear history. Best for feature branches that are not shared with others. Avoid rebasing branches that other people have checked out.
   > - **Merge** (`git merge origin/<branch>`): creates a merge commit that preserves the full history of both sides. Safer for shared or long-lived branches where rewriting history would disrupt collaborators.

   Wait for the user's choice before proceeding.

4. For each conflicted file identified in step 1:
   a. Use Read to display the file and locate the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
   b. Explain to the user what each side of the conflict contains:
      - **HEAD (your changes):** the lines between `<<<<<<< HEAD` and `=======`.
      - **Incoming (their changes):** the lines between `=======` and `>>>>>>> <ref>`.
   c. Ask the user which resolution to apply (keep yours, keep theirs, or combine), or propose a resolution if the intent is clear from context.
   d. Use Edit to apply the agreed resolution, removing all conflict markers so the file is valid.

5. After all conflicted files are resolved, use Bash to stage **only the resolved files by name** (never `git add .`, which would sweep untracked files like build output or `.env` into the commit) and complete the rebase or merge:
   - If **rebase** was chosen:
     ```bash
     git add <resolved-file-1> <resolved-file-2> ...
     git rebase --continue
     ```
     If additional conflict rounds occur, repeat steps 4–5 for each round until the rebase completes.
   - If **merge** was chosen:
     ```bash
     git add <resolved-file-1> <resolved-file-2> ...
     git merge --continue
     ```

6. Use Bash to confirm the branch is clean and ready to push:
   ```bash
   git status
   git log --oneline -5
   ```
   Verify there are no remaining conflict markers and the working tree is clean. Remind the user:
   - If rebase was used, a force-push is required: `git push --force-with-lease origin <branch>`. Only do this if the branch is not shared.
   - If merge was used, a regular push is safe: `git push origin <branch>`.

---

### Action (f) — Manage Stashes

1. Use Bash to list all stashes:
   ```bash
   git stash list
   ```
   If the list is empty, inform the user and stop.

2. Show the stash list to the user and ask what they want to do:
   > "(i) Inspect a stash — show its diff
   > (ii) Apply a stash — apply without dropping
   > (iii) Pop a stash — apply and drop
   > (iv) Drop a stash — delete without applying
   > (v) Drop all stashes — clear the entire stash list (confirm first)"

3. Execute the chosen sub-action:

   **Sub-action (i) — Inspect a stash**

   Ask the user which stash number (N) to inspect. Then:
   ```bash
   git stash show -p stash@{N}
   ```
   Display the diff and provide a plain-language summary of what changes are stashed (files changed, nature of changes).

   **Sub-action (ii) — Apply a stash**

   Ask the user which stash number (N) to apply. Then:
   ```bash
   git stash apply stash@{N}
   ```
   After applying, check for conflicts:
   ```bash
   git status
   ```
   If any conflicts are present (files show `both modified` or similar), inform the user and run Action (e) to resolve them.

   **Sub-action (iii) — Pop a stash**

   Ask the user which stash number (N) to pop. Then:
   ```bash
   git stash pop stash@{N}
   ```
   After popping, check for conflicts the same way as sub-action (ii). If conflicts are found, run Action (e) to resolve them.

   **Sub-action (iv) — Drop a stash**

   Ask the user which stash number (N) to drop. Show the stash message and confirm:
   > "This will permanently delete stash@{N}: `<message>`. Confirm? (y/n)"

   If confirmed:
   ```bash
   git stash drop stash@{N}
   ```

   **Sub-action (v) — Drop all stashes**

   Count the total number of stashes and confirm with the user:
   > "This will permanently delete ALL X stashes. This cannot be undone. Confirm? (y/n)"

   If confirmed:
   ```bash
   git stash clear
   ```

4. After any sub-action completes, run `git stash list` again and show the user the updated stash state.

---

## Git Workflow Reference

### Branch Model

| Branch | Purpose | Rules |
|--------|---------|-------|
| `main` | Production-ready history | Never commit directly. Only merge from release branches. |
| `release/<version>` | Integration branch per release | Never commit directly. All feature/fix PRs target this. |
| `feature/task-XXX-description` | New work | One per task. Created from the release branch. |
| `fix/task-XXX-description` | Bug fixes | One per issue. Created from the release branch. |

### Flow

```
feature/* or fix/*
       ↓  (PR)
release/<version>
       ↓  (PR when release is ready)
      main  →  tag v<version>
```

### Who Does What

| Action | Responsible |
|--------|------------|
| Create feature/fix branch | Planning or Dev agent |
| Open PR | Dev agent (the one that did the work) |
| Code review | Tech Review + Security agents |
| Approve PR | Tech Review + Security; Planning after triage |
| Merge to release | Planning or designated agent |
| Cut release (release → main + tag) | Planning or DevOps |
| Create changelog | Documentation agent |

### Naming Conventions

- Feature branches: `feature/task-NNN-short-description`
- Fix branches: `fix/issue-NNN-short-description`
- Version tags: `vMAJOR.MINOR.PATCH` (e.g. `v1.0.0`)
- Changelog: `docs/CHANGELOG.md` or `docs/changelogs/<version>.md`

### Merge Style

Document the chosen merge style in `docs/assumptions.md` at project start. Default: merge commit (`--no-ff`) to preserve branch history.

### Changelogs

The Documentation agent creates or updates changelogs in `docs/` for each release. Format: version, date, sections for Added / Changed / Fixed / Security, links to PRs or handoff artifacts.

## Output Format

After completing any action, confirm:
- What git operations were run (list commands with output).
- The current state of relevant branches.
- What the next step is.

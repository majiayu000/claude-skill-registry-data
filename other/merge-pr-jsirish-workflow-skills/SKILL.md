---
name: merge-pr
description: Merge an approved GitHub PR or GitLab MR (gh/glab), then clean up branches and sync the local repo. Use when asked to "merge this PR", "merge the MR", "land it", "ship the PR", or run /merge_pr. Checks mergeability and CI first; strategy follows repo policy, not a default.
---

# Skill: Merge PR

**Goal:** Safely merge an approved Pull/Merge Request, clean up associated branches, and synchronize the local repository.

The workflow is host-agnostic — the phases are the same everywhere; only the CLI and status-field names differ. GitHub calls it a Pull Request (`gh`), GitLab a Merge Request (`glab`); "PR" below means either.

---

## Phase 0: Detect the Host

```bash
git remote get-url origin
```

| Remote host | CLI | Verify with |
|---|---|---|
| `github.com` (or GitHub Enterprise) | `gh` | `gh auth status` |
| `gitlab.com` (or self-managed GitLab) | `glab` | `glab auth status` |
| anything else | none assumed | — |

If the host has no supported CLI, don't improvise: tell the user, and offer either a merge through the host's UI or — only if the target branch is unprotected — a plain-git merge and push.

---

## Phase 1: Pre-Merge Verification

Verify, in the host's terms:

1. The PR is **open**.
2. It is **mergeable** with **no conflicts**.
3. CI is **passing — if CI exists**. Absence of any pipeline or checks is *not* a blocker (many repos have no CI); a failing or pending one is.
4. Host-specific gates are satisfied (see below).
5. The source branch on the remote actually contains the expected commits. A push can silently fail to land, and an "approved" but empty PR merges nothing — `git ls-remote origin <branch>` is proof; local state is not.
6. Confirm explicit user approval to merge.

**GitHub:**
```bash
gh pr view <pr-number> --json state,reviewDecision,statusCheckRollup,mergeable,mergeStateStatus,headRefName,baseRefName
```
-   `state: "OPEN"`, `mergeable: "MERGEABLE"`, `mergeStateStatus: "CLEAN"`.
-   `statusCheckRollup` empty = no CI configured = fine; failures = blocker.

**GitLab:**
```bash
glab mr view <mr-number>
glab api "projects/:fullpath/merge_requests/<mr-number>"   # for the fields below
```
-   `state: "opened"`, `detailed_merge_status: "mergeable"`, `has_conflicts: false`, `draft: false`.
-   `blocking_discussions_resolved: true` — projects often enforce resolved threads at merge; resolve them first, don't bypass.
-   `head_pipeline: null` = no CI configured = fine; `"failed"` = blocker.

> [!NOTE]
> Review approval is convention on both hosts unless the repo configures otherwise.
> On GitHub, `reviewDecision` only gates the merge when **CODEOWNERS or required
> reviewers** exist — a blank `reviewDecision` is not a blocker. On GitLab,
> approvals are optional on the Free tier and approval *rules* are Premium — treat
> missing approvals the same way. In both cases the user's go-ahead plus the
> mergeability checks above are sufficient.

---

## Phase 2: Merge

**Determine the merge strategy — do not assume squash.** Strategy is repo policy, not skill policy. Resolve it in this order:

1.  An explicit instruction from the user or repo docs (`CONTRIBUTING.md`, `CLAUDE.md`).
2.  The host's own settings:
    -   GitHub: `gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed`
    -   GitLab: `merge_method` and `squash_option` from `glab api "projects/:fullpath"`
3.  Recent history: `git log --oneline --merges -5` — a history of merge commits should not suddenly acquire squashes, and vice versa.
4.  Only then default to squash.

**GitHub:**
```bash
gh pr merge <pr-number> <--squash|--merge|--rebase> --delete-branch --subject "<commit-subject>" --body "<commit-body>"
```

**GitLab:**
```bash
glab mr merge <mr-number> [--squash] --remove-source-branch --yes
```

-   **Commit Message (when squashing):** Synthesize a clean, descriptive subject using conventional commits (e.g., `feat: PR title`). If the PR description contains important details, include them in the commit body.
-   `--subject` / `--body` apply to `--squash` and `--merge` only; drop them for `--rebase`.
-   `--delete-branch` (gh) / `--remove-source-branch` (glab) handles the remote branch cleanup on the source repository.

---

## Phase 3: Local Cleanup and Sync

First, detect whether you are inside a linked git worktree:
```bash
if [ "$(git rev-parse --git-dir)" != "$(git rev-parse --git-common-dir)" ]; then
  echo "linked worktree"
else
  echo "primary checkout"
fi
```

### If running in a worktree (Claude Code default)

`git checkout` and `git branch -D` both fail in a worktree: the default branch is checked
out in the primary worktree (two worktrees cannot share a branch), and the feature branch
is the current worktree itself. Skip both steps. Sync the primary worktree directly:

```bash
# Resolve primary worktree root — first entry in worktree list is always primary
PRIMARY=$(git worktree list --porcelain | awk '/^worktree /{sub(/^worktree /, ""); print; exit}')
git -C "$PRIMARY" fetch origin
git -C "$PRIMARY" checkout <default-branch>
git -C "$PRIMARY" pull origin <default-branch> --ff-only
```

The feature branch worktree is cleaned up automatically by Claude Code when the session
ends — no manual deletion needed.

### If running in the primary checkout

1.  **Switch to Default Branch:**
    ```bash
    git remote show origin | grep 'HEAD branch'
    git checkout <default-branch>
    ```
2.  **Pull Latest Changes:**
    ```bash
    git fetch origin
    git pull --ff-only origin <default-branch>
    ```
3.  **Sync Fork (if applicable):**
    If working on a fork, sync with upstream:
    ```bash
    git remote | grep -qx upstream && git fetch upstream && git merge --ff-only upstream/<default-branch> && git push origin <default-branch>
    ```
4.  **Delete Local Branch:**
    ```bash
    git branch -D <feature-branch>
    ```
    Use `-D`, not `-d`: after a squash or rebase merge the branch tip is not an ancestor of the default branch, so `-d` refuses. The PR is already merged, so nothing is lost.

---

## Phase 4: Post-Merge Verification

1.  **Verify PR Closure:**
    Confirm the PR reports merged (`gh pr view` / `glab mr view`) and any linked issues are also addressed — `Closes #N` auto-closes on both hosts.

> [!NOTE]
> **Do not auto-invoke `/handoff` from this skill.** Handoff is **user-invoked
> only** — the user decides when the session's work is complete and runs
> `/handoff` themselves as a separate step (cadence: `pr-review` → `merge-pr` →
> `handoff`). Merging one PR does not mean the session is over.

---

## Important Reminders

- **CLI merges are worktree-safe.** Both `gh pr merge` and `glab mr merge` use the host's API and do not require being in the primary checkout. The Phase 3 split above is only about the local sync steps.
- **Branch Deletion:** Automatic source-branch deletion works when permissions allow. For PRs from forks, deletion may fail or require manual cleanup on the fork.
- **Merge Conflicts:** If the PR has conflicts, resolve them before attempting to merge.
- **Verification:** Always verify that the merge was successful and that the primary worktree is on a clean, updated default branch.

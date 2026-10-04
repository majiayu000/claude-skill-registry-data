---
name: fast-pr-workflow
description: "Git and GitHub PR workflow: branch from the task, commit, and create or update the pull request without merging or rebasing unless asked. Use to create PR, update PR, commit, push, or ship this work. Merge, squash, and land requests route here so the main-branch guard applies."
license: MIT
allowed-tools: Bash(gh auth status:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(git rev-parse:*), Bash(git rev-list:*), Bash(git merge-base:*), Bash(git branch --show-current), Bash(git remote -v), Bash(git ls-files:*), Bash(git add:*), Bash(git commit -m:*), Bash(git fetch:*), Bash(git switch -c:*), Bash(git switch --create:*), Bash(git checkout -b:*), Bash(git push -u origin HEAD), Bash(git push --set-upstream origin HEAD), Bash(git push origin HEAD), Bash(gh pr list:*), Bash(gh pr view:*), Bash(gh pr checks:*), Bash(gh pr status:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(gh pr edit:*)
metadata:
  display-name: "Fast PR Workflow"
  version: "1.8"
  platforms: "claude-code codex"
  tags: "git github pr workflow"
---

# Fast PR Workflow

Perform only the explicitly authorized branch, commit, push, pull-request, or merge mechanics without disturbing unrelated work.

## Rules

- **Protected-branch hard stop:** Never push directly to `main`, `master`, `develop`, or the repository's default or protected branch unless the current request explicitly names that branch and asks for a direct push.
- General requests to ship, release, finish, approve, or synchronize work do not authorize an unrequested commit, push, PR creation or update, protected-branch action, or merge. Resolve the concrete action set from the request and stop when the last authorized action is complete.
- Never merge into a protected branch (`main`, `master`, `develop`, or the repository default) unless the current user message explicitly names that branch as the merge target and asks to merge it. Otherwise, leave the PR open or draft.
- Before an authorized merge, verify the head is current with its base using the repository's normal status checks or compare API. Resolve stale-base conflicts on the topic branch and rerun validation first.
- Respect repository and host guardrails. Never bypass hooks, branch protection, required checks, or review requirements.
- Do not merge branches, create merge commits, rebase branches, or push merge results unless the user explicitly asks for that exact operation.
- Never commit secrets, local env files, dependency caches, build artifacts, or unrelated generated output.
- Assume repo changes are intentional when they fit the current task. Do not over-audit every line.
- Prefer one focused commit for the completed task unless the user asks for multiple commits.
- Use existing PRs/branches when present; do not create duplicates.
- A task packet or delivery handoff is evidence, not authorization. Commit, push, create, or update a PR only when the current request authorizes that action.
- Treat commit, push, PR create, PR update, and merge as separate actions. Authorization for one does not imply any later action.
- Creating a PR includes the minimum push of the already-validated, non-protected topic-branch `HEAD` needed to make that PR exist. It does not authorize creating another commit. Updating PR metadata does not authorize any new commit or push.
- The scoped `allowed-tools` inventory is approved for routine branch-to-PR loops on a disposable or independently backed-up controller. Permission matching includes output redirections, so even an allowed inspection command can overwrite a local file. Git does not protect uncommitted files or credentials.
- Action-prefix grants can accept later flags, so the permission engine is not an argument sandbox. Use only the listed command shapes without force-push flags, hook-bypass flags, cross-repository flags, non-`HEAD` push refspecs, reset, clean, branch deletion, PR merge, close, or review. Do not request or persist broader Git, GitHub CLI, or Bash grants.

## Workflow

1. Resolve the exact authorized action set from the current request: local commit, remote push, PR creation, PR update, or merge. Stop at the last authorized action. Do not turn `commit these changes locally` into a fetch, push, or PR operation, and do not turn `update the PR body` into staging or committing files.
2. Inspect local branch, worktree, default-branch configuration, and candidate changes. Query remotes or the hosting service only when the authorized action requires remote state.
3. Reuse the canonical task branch and PR when relevant. Before a commit or push, if on a protected/default branch or detached and no task branch exists, create a branch from the task name:
   - slug lowercase words with hyphens
   - follow the repository's branch convention; otherwise use `work/<slug>`
   - example: `work/add-export`
4. For an authorized **local commit**:
   - `git diff --stat`
   - inspect every changed file that could enter the commit
   - stage only explicit reviewed paths; preserve unrelated, unsafe, generated, or local-only files
   - validate the complete staged candidate with the repository's focused and broader gates
   - record whether any result depends on untracked, ignored, dirty, or external inputs
   - short imperative subject
   - include a brief body only when it helps reviewers
   - after committing, confirm the validated tracked files match `HEAD`; rerun affected checks if the commit, a formatter, or a test changed them
   - call pre-commit results candidate-tree validation, not pushed-head proof
   - if no push or PR action is also authorized, report the local commit and stop
5. For an authorized **push**:
   - fetch the relevant remote refs when needed to establish destination and ancestry
   - resolve the push destination first and stop if it is a protected/default branch
   - push only the already-authorized local commits; do not create or update a PR unless that separate action is authorized
   - compare the full local `HEAD` and remote branch object IDs after the push
6. For an authorized **PR creation**:
   - fetch/query the required remote and hosting state
   - reuse any matching open PR; otherwise push the already-validated topic-branch `HEAD` if needed and create one with a concise summary and validation
   - enter a shipping freeze and verify the exact repository, base ref, head ref, commit ID, and `OPEN` state
   - require exactly one canonical PR for that repository, base, and head; a missing, mismatched, duplicated, closed, or misdirected PR fails the action
7. For an authorized **PR update**:
   - query and resolve the one intended open PR before changing it
   - update only the requested title, body, reviewers, labels, or other PR metadata
   - do not stage, commit, or push repository files unless those actions are separately authorized
   - verify the requested metadata and the PR's repository, base, head, commit ID, and `OPEN` state after the update
8. For an authorized **merge**, apply every protected-branch and stale-base guard above. Do not create a merge commit, rebase, squash, or push a merge result unless that exact operation is authorized.
9. When a validation handoff exists, carry its non-sensitive commands, results, evidence boundary, blockers, and remaining risks into an authorized PR body. A later tracked-file fix requires separately authorized commit and push actions plus affected validation.

Only call validation pushed-head proof when the tested commit and every required input match the verified remote and PR head. Otherwise preserve the narrower candidate-tree claim.

## PR Body

Keep it short:

```markdown
## Summary
- Changed X
- Added/fixed Y

## Validation
- `command`
```

If validation was not run, say `Not run (reason)`.

## Useful Commands

- Current branch/cleanliness: `git status --short --branch`
- Existing PR for branch: `gh pr view --json number,title,url,state`
- Create PR: `gh pr create --fill`
- Update PR body: `gh pr edit <number> --body-file <file>`
- Push branch: `git push -u origin HEAD`

## Output To User

Report only the essentials: branch, commit hash, PR URL, and validation. Mention blockers directly if auth, network, or repo state prevents completion.

---
name: ship-changes
description: "Use when shipping current work end-to-end — creating a branch, committing, pushing, and opening a PR. Invoke when the user says 'ship this', 'create a PR', or when work is complete and ready for review."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before shipping end-to-end (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/git-hosts.md`

Run the full shipping pipeline: branch, commit, push, and open a PR.

## Operations

| Operation | Tool (see `<project-root>/docs/git-hosts.md`) | CLI fallback per `<project-root>/docs/git-hosts.md` |
|-----------|--------------|--------------|
| Pre-scan change state | git host change scan (see `<project-root>/docs/git-hosts.md` in the project root) | `git branch --show-current` + `git status --short` + `git diff --stat` + `git diff --cached --stat` + `git log @{u}..HEAD --oneline` |

Forward git host tool availability to subskills so they skip their own change scan and PR diff calls when possible. Follow `<project-root>/docs/git-hosts.md` in the project root for all git/gh operations.

### 1. Interpret Arguments

- Ticket URL/reference → `<ticket-url>`
- Wording influencing branch name/commit message → `<additional-context>`
- Base branch → `<base>`
- Otherwise undefined

### 2. Pre-Scan Changes (Shared Context)

Run the change scan once here and forward results to every subskill so they skip their own Load/Analyze step.

Run the change scan from the operations table above. Store:
- `<current-branch>` — current branch
- `<uncommitted>` — combined status + diff stat
- `<ahead-commits>` — ahead-commits log via range `@{u}..HEAD` (empty if none)

Build `<change-summary>` from `<uncommitted>` (primary) or `<ahead-commits>` (fallback): group into 2-4 logical themes, summarize what and why (not how), and consider `<additional-context>`.

Derive `<branch-category>` from `<change-summary>` (`feature`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`, `ci`).

Blocker: if `<uncommitted>` and `<ahead-commits>` are both empty, STOP: "Nothing to ship."

Forward to every subskill: `<current-branch>`, `<uncommitted>`, `<ahead-commits>`, `<change-summary>`, and `<branch-category>`. When provided, subskills must skip their own Load Changes, Analyze Scope, and Determine Category steps.

### 3. Create Work Branch

Gate: skip this step if `<current-branch>` is not `master` AND `<current-branch>` is already ticket-related. If skipped, set `<new-branch>` to `<current-branch>`.

Otherwise, create a new branch. Pass `<additional-context>`, `<current-branch>`, `<uncommitted>`, `<ahead-commits>`, `<change-summary>`, and `<branch-category>`. Store the resulting branch as `<new-branch>`. If the result is "Nothing to branch from" or "Branching skipped", STOP and report.

### 4. Commit and Push

Gate: if `<uncommitted>` is empty, skip the commit substep; still push the branch if `<ahead-commits>` is non-empty. If both are empty, the pre-scan blocker already stops.

Commit and push changes. Pass `<additional-context>`, `<uncommitted>`, `<ahead-commits>`, and `<change-summary>`. Store the commit hash as `<hash>` and the push target as `<push-target>`. If the result is "Nothing to commit or push", STOP and report.

### 5. Create Pull Request

Create a pull request. Pass `<change-summary>` (reuse the pre-scan summary; scan the post-commit git state itself but reuse the semantic summary). If `<ticket-url>` is defined, pass it. If `<base>` is defined, pass it as the base branch. Output the PR URL when complete.

**Mandatory:** ensure the pr-create subskill runs its PR-template check (Step 6) before composing the body. Forwarded `<change-summary>` triggers the skip path in pr-create Step 4 — that does NOT exempt the template check. Do not accept `<pr-template>` = `none` unless the subskill confirms it probed the repo.


---
name: ss-create-pr
description: Use once coding and code review are complete and it's time to open a pull/merge request. Runs pre-flight checks (tests, cleanup scan), rebases onto the target branch, verifies again if the rebase changed anything, then opens a PR on GitHub (via gh) or an MR on GitLab (via glab) depending on the repository's remote. Falls back to a local conventional-commit summary if there's no remote or forge CLI available, or if the user declines — that fallback is a normal outcome, not a failure.
---

# Create Pull/Merge Request

Finalize development work once coding and review are done: run pre-flight checks, clean up, rebase, and open a PR/MR — or, if that's not possible, land the work with a clean conventional-commit history and a written summary instead.

**Core principle:** archive specs → verify → clean → rebase → verify again → ship. Never open a PR/MR with failing tests, debug artifacts, unresolved conflicts, or an unarchived delta spec. Avoid redundant test runs — if a prior coding step already verified tests at the current commit, trust that result.

**This is the last step of a development workflow.** It assumes implementation is complete (e.g., via the `ss-coding` skill or manual work) and review is done (e.g., via the `ss-code-review` skill or manual review), with all review issues addressed.

## Inputs

- Target branch (optional — defaults to the remote's detected default branch).
- `--draft` to open the PR/MR as a draft.
- Delivery mode, if this skill is running standalone rather than as part of a larger workflow: **full** (the normal case — this skill actually opens a PR/MR) or **lite** (the calling workflow already decided to skip PR creation and land changes locally; if so, skip straight to "Local fallback" below).

## Ground rules

1. **Tests must pass before opening a PR/MR.** If they haven't been verified at the current commit, run them; if they fail, stop and fix first. Don't re-run tests already verified at the same commit.
2. **No debug artifacts** — stray `console.log`, debugger statements, TODO/HACK markers, disabled test selectors, secrets — must be removed first.
3. **Rebase, never merge** the target branch into the feature branch.
4. **Verify again after rebase only if the rebase actually changed code.** A no-op rebase (already up to date) needs no re-verification.
5. **Never force-push without explicit consent.** A first-time push never needs force.
6. **The PR/MR description must be substantive** — auto-generate one from the commit history if the user doesn't supply one.
7. **Archive any active delta spec first** — run the `ss-archive` skill; it's idempotent and no-ops when there's no active delta.

## Step 0 — Archive the delta spec

Run the `ss-archive` skill before anything else. Expect it to merge any delta specs into the authoritative spec tree and move the change into the archive, committing and pushing as needed — or no-op if there's nothing to archive.

If archiving reports validation errors or unresolved merge conflicts, stop. Don't open the PR/MR until it succeeds or the user explicitly confirms this is a zero-spec change.

## Step 1 — Detect the environment and the forge

```bash
# Worktree vs. plain checkout
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
[ "$GIT_DIR" != "$GIT_COMMON" ] && echo "Worktree environment: $(git rev-parse --show-toplevel)"

# Current branch
CURRENT=$(git branch --show-current)
[ -z "$CURRENT" ] && { echo "Detached HEAD — create a branch first."; exit 1; }

# Target branch (local-first, no network required)
TARGET=${user_specified:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')}
TARGET=${TARGET:-$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')}
TARGET=${TARGET:-main}
```

**Determine the forge from the remote URL:**

```bash
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
```

- `REMOTE_URL` contains `github.com` (or a configured GitHub Enterprise host) → forge = GitHub, use `gh`.
- `REMOTE_URL` contains `gitlab.com` (or a configured self-hosted GitLab host) → forge = GitLab, use `glab`.
- No `origin` remote at all, or the host doesn't look like either → forge = none. Go to **Local fallback**.

**Check the matching CLI is present and authenticated:**

```bash
# GitHub
command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1
# GitLab
command -v glab >/dev/null 2>&1 && glab auth status 2>&1 | grep -q "Logged in"
```

If the forge was detected but its CLI is missing or unauthenticated, tell the user, offer to continue with **Local fallback** instead, and proceed only on their confirmation (or automatically if the calling workflow already allows silent degrade).

## Step 2 — Pre-flight checks

Run all of these; all must pass before continuing.

1. **No uncommitted changes.** `git status --porcelain` must be empty — commit or stash first.
2. **On a feature branch**, not `main`/`master`/a shared integration branch. Refuse if `CURRENT` is one of those.
3. **Commits ahead of target.** If `git log origin/$TARGET..HEAD --oneline` is empty, there's nothing to open a PR/MR for — report and stop (not an error).
4. **No active delta spec remains** after Step 0 — if one is still found, stop and point back to `ss-archive`.
5. **Test verification, conditional.** Skip a redundant full run if there's clear evidence tests already passed at this exact commit — e.g., a completed task/plan file with every checkbox checked, or a recent commit message that says so explicitly. Otherwise, auto-discover and run the test command for the stack in use (Maven, Gradle, `go test`, `npm test`, `make test`, `pytest`, etc.). Being inside a worktree is *not*, on its own, evidence that tests passed — worktrees are the default output of `ss-create-branch` for all development, so their mere presence carries no information about test status.
6. **Lint**, if the project defines one — always run it; it's fast and catches regressions.

If any check fails, stop and fix the issue before retrying from Step 2.

## Step 3 — Cleanup scan

Scan only the files changed on this branch (`git diff --name-only origin/$TARGET...HEAD`) for:

1. Debug artifacts — stray print/log/debugger statements in any language.
2. Disabled test selectors (`.only(`, `.skip(`, etc.) left behind.
3. TODO/HACK/FIXME introduced by this branch's new lines.
4. Patterns that look like a hardcoded secret (API key, password, token literals) in new lines.
5. Large blocks of commented-out code.

If anything is found:

- List it with exact file:line.
- Remove automatically what's clearly safe (stray debug logs, `.only(`, unused imports).
- Ask the user about TODOs — they may be intentional.
- **Stop for anything that looks like a secret** — never commit it; get explicit confirmation first.
- Commit the cleanup separately: `git commit -m "chore: remove debug artifacts"`.

## Step 4 — Rebase onto the target

```bash
git fetch origin $TARGET
git rebase origin/$TARGET
```

On conflicts: list the conflicting files, and for each, read the conflict markers and attempt a resolution. Resolve and continue automatically only when the resolution is unambiguous (your change plus their unrelated change); otherwise stop, show the conflicts, and ask for guidance. If the rebase produces an empty commit, skip it (`git rebase --skip`).

After a successful rebase, if the branch already exists on the remote, a force-push is needed — **confirm with the user first**, then use `git push origin $CURRENT --force-with-lease` (never a bare `--force`).

## Step 5 — Post-rebase verification

Only if the rebase actually changed something (`ORIG_HEAD` differs from `HEAD` *and* the tree diff is non-empty): run tests for the affected modules if you can determine them from the changed paths, otherwise fall back to the full suite; then run lint again.

If the rebase was a no-op, skip this step — the code is byte-identical to what was already verified.

If tests fail after rebase, the rebase introduced a problem: fix it, commit, and re-verify. Never open a PR/MR with failing tests.

## Step 6 — Format the PR/MR

Check for a project template first (e.g., `.github/pull_request_template.md`, `.gitlab/merge_request_templates/*.md`); use it if present.

**Title**, using Conventional Commits: `<type>(<scope>): <description>` — `type` from the branch prefix (`feat/`→feat, `fix/`/`hotfix/`→fix, `refactor/`→refactor, `docs/`→docs), `scope` from the primary modified module, `description` from the commit messages or the user.

**Description**, if no template exists — draw on the commit history and any available plan/proposal documents:

```markdown
## Background
<goal and context, from a plan/proposal doc if one exists, otherwise inferred from commit messages>

## Changes
<one bullet per commit>

## Impact
- Database changes: <yes/no, list migration files>
- API changes: <yes/no, list new/changed endpoints>
- Config changes: <yes/no, list config files>

## Testing
- [x] Unit test coverage
- [x] Local tests pass
- [ ] <anything needing manual verification>

## Release notes
<one sentence for product/ops>
```

## Step 7 — Push and open the PR/MR

If the branch isn't on the remote yet, push it (`git push -u origin $CURRENT`); otherwise it's already there from Step 4.

Decide on squash: default to squashing `feat/`/`feature/` branches, keep full history for `fix/`, `hotfix/`, `refactor/`, `docs/`.

**On GitHub:**

```bash
gh pr create \
  --title "<formatted-title>" \
  --body "<formatted-description>" \
  --base "$TARGET" \
  --head "$CURRENT" \
  ${DRAFT_FLAG:+--draft}
```

**On GitLab:**

```bash
glab mr create \
  --title "<formatted-title>" \
  --description "<formatted-description>" \
  --target-branch "$TARGET" \
  --remove-source-branch \
  ${SQUASH:+--squash} \
  ${DRAFT_FLAG:+--draft}
```

## Step 8 — Verify creation and report

Confirm the PR/MR actually exists (`gh pr view` / `glab mr view`, both headless-safe — never open a browser) and report:

```
PR/MR created:
- Title: <title>
- Target: <target>
- URL: <url>
- Status: open (or draft)
- Squash: yes/no

Next steps:
- Wait for CI
- Request reviewer approval
- Merge once CI passes and it's approved
- Run the `ss-cleanup` skill afterward to remove the worktree and delete the branch
```

## Local fallback (no remote, no forge CLI, or user declines)

This is a normal, expected outcome — not a failure. It also applies directly when the calling workflow's delivery mode is **lite**.

1. Run Steps 2–3 (pre-flight checks and cleanup scan) exactly as above — quality gates don't change based on delivery mode.
2. Skip rebase/PR steps that require a remote or forge.
3. Land the work as clean Conventional Commits on the current branch: squash or reorganize commits as needed so the history reads as a coherent, reviewable sequence.
4. Push the branch if a remote exists and the user wants it pushed (optional in this mode).
5. Produce a written change summary in place of a PR/MR description — same content as the Step 6 template (Background / Changes / Impact / Testing / Release notes) — and hand it to the user directly, so it can be pasted wherever the PR/MR would normally have gone (e.g., into a manual PR later, a commit message, or shared with a reviewer).

## Edge cases

| Case | Handling |
|------|----------|
| No forge CLI, or not authenticated | Offer the local fallback rather than failing outright |
| No commits ahead of target | "Branch is up to date with target — nothing to open." Exit, not an error |
| Branch already has an open PR/MR | Report its URL; ask whether to update its description or leave it |
| Detached HEAD | Stop — create a branch first |
| PR/MR creation fails (permission/network) | Report the error and show the equivalent manual `gh`/`glab` command to retry |
| Target branch doesn't exist on the remote | Stop — list the branches that do exist |
| Multiple remotes | Warn, default to `origin`, ask if a different one was intended |
| In a worktree | Proceed normally; note the worktree path; don't remove the worktree here — that's `ss-cleanup`'s job |
| Rebase makes all commits empty | All changes already in target — report and exit |

## Anti-patterns

| Anti-pattern | Why it's harmful | Do this instead |
|--------------|-------------------|------------------|
| Open a PR/MR with failing tests | Wastes reviewer time, breaks CI | Verify tests pass first |
| Re-run the full suite unnecessarily | Wastes significant time per redundant run | Trust a prior verified result at the same commit |
| Leave debug artifacts or secrets in | Security risk, unprofessional | Run the cleanup scan |
| Merge target into the feature branch | Merge commits pollute history | Always rebase |
| Force-push without consent | Can overwrite a teammate's work on the same branch | Confirm first |
| Empty PR/MR description | Reviewer has no context | Auto-generate from commits/plan/proposal |
| Treat "no forge CLI" as a hard failure | Blocks solo/offline workflows for no reason | Fall back to local commits + summary |
| Unconditional squash | Not every branch type benefits from it | Only squash `feat/` branches by default |

## Stop signs

- Tests failing → stop, fix first.
- On `main`/`master` → stop, wrong branch.
- Uncommitted changes → stop, commit or stash first.
- About to force-push without consent → stop, ask first.
- A rebase conflict you can't confidently resolve → stop, ask the user.
- A potential secret found in the cleanup scan → stop, confirm with the user.
- A PR/MR already exists for this branch → stop, confirm intent first.
- Detached HEAD → stop, create a branch first.

## Examples

```
Open a PR
Open a PR against main
Open a draft MR against the testing branch
```

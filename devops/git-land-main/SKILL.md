---
name: git-land-main
description: >-
  Safely land one or many topic branches onto main via GitHub PR: inventory,
  commit leftovers, push, open/update PR, verify (hosted Actions if it actually
  ran, else a local gate), merge or squash (repo norm), sync local main, then
  delete local/remote branches only after main contains the work. Use when the
  user asks to merge/squash/commit/PR/push to main, land a branch, land multiple
  branches, clean up merged branches, or close out feature/fix/chore/slice
  branches. Never commit or push directly to main; never force-push main; never
  delete a branch until origin/main has it. GitHub Actions billing is not a
  merge blocker; do not make repos public to get free minutes.
---

# Git land → main

Walk **one branch or a queue of branches** onto `main` the safe way: topic
branch → commit → push → PR → verify → merge/squash → sync `main` → delete
branches. Nothing is deleted until `origin/main` contains the work. Verify
means **hosted Actions if jobs actually ran**, otherwise a **local gate**.
A GitHub red X from billing / spending limits is not a failed test.

**Outcome when done**

1. Every intended branch is on `main` via a merged GitHub PR
2. Local checkout is on synced `main` (even with `origin/main`)
3. Landed topic branches are deleted locally and on the remote
4. Unrelated WIP, stashes, and secrets are still present (nothing discarded)

**Hard rules**

- Never commit, amend, or push directly to `main` / `master`
- Never force-push `main` / `master`
- Never `--no-verify` unless the user explicitly requests it
- Never merge when **verification failed** (hosted tests that ran, or the local gate)
- Hosted Actions **unavailable** (billing, spending limit, disabled, jobs never started) is not a failed gate — run the local gate and land if it passes
- Never ask the user to pay for GitHub Actions, and never make a repo public, to unblock a land
- Never `--admin` to bypass required status checks or reviews
- Never discard uncommitted work or drop stashes without an explicit order
- Never commit secrets (`.env`, `.env.local`, credentials, private keys)
- Never `git branch -D` / `git push --delete` until merge is **confirmed on `origin/main`**
- Prefer merge of `origin/main` into the topic branch over rebase (no force-push of shared branches)
- Rebase only on **private unpushed** branches when the user asks
- Invoking this skill authorizes commit + PR + merge + branch delete for the named (or current) branches — not Vercel deploy

**Related**

- `slice-complete` — Movemental `slice/Sxx-*` close-out (same land path, slice naming)
- `git-github-expert` — land **plus** `vercel --prod`
- This skill if the ask is merge/squash/PR/push to main, **multiple branches**, or safe delete after main

---

## Progress checklist

Copy and update as you go:

```
git-land-main:
- [ ] 0 Inventory (branches, PRs, dirty tree, stashes)
- [ ] 1 Queue + merge method (squash vs merge commit)
- [ ] 2 Per branch: switch safely (stash/commit; no WIP mix)
- [ ] 3 Commit leftovers on the topic branch
- [ ] 4 Update branch from origin/main
- [ ] 5 Push
- [ ] 6 PR open / updated vs main
- [ ] 7 Merge gate green (hosted CI that ran, else local) + mergeable
- [ ] 8 Merge PR (squash or merge)
- [ ] 9 Sync local main; verify work is on origin/main
- [ ] 10 Delete branch (local + remote) only after verify
- [ ] 11 Next queued branch, or done report
```

For each queued branch, repeat phases 2–10. Do not start the next branch until the previous one is on `main` and deleted (or explicitly skipped).

---

## Phase 0 — Inventory (nothing lost)

Run in the **repo root** (parallel):

```bash
git status -sb
git status --porcelain
git branch -vv
git branch -a
git rev-parse --abbrev-ref HEAD
git remote -v
git fetch --prune origin
git stash list
git log -5 --oneline
gh pr list --state open --base main
```

**Zero-loss protocol**

| Situation | Action |
|-----------|--------|
| Dirty working tree | Commit on the owning topic branch (Phase 3) or `git stash push -u -m "wip <branch>"` before switching. Never `git reset --hard` / `git clean -fd` |
| Untracked files that belong | Include in commit (unless secrets / noise) |
| Existing stashes | List them; do **not** drop. Pop only if the message matches the branch you are landing |
| Detached HEAD | Create/checkout a topic branch before committing |
| Secrets in status | Leave untracked / unstaged; warn in done report |
| Other worktree has a branch checked out | Do not delete that branch until the worktree is removed or switched |

Default base branch: `main`, or `master` if that is what `origin` uses. Confirm with `git symbolic-ref refs/remotes/origin/HEAD` (or `gh repo view --json defaultBranchRef`).

---

## Phase 1 — Queue + merge method

### Queue

Build a land queue. Skip `main` / `master`.

| User said | Queue |
|-----------|--------|
| One named branch | That branch only |
| “this branch” / current work | `HEAD` if it is a topic branch; if on `main` with dirty work, create `feat/<short-slug>` (or `fix/` / `chore/` / `docs/` / `refactor/` / `test/` / `slice/Sxx-*` to match the repo) and move work there |
| “all branches” / “multiple branches” / unnamed extras | See [reference.md](reference.md) — classify merged vs unmerged, detect stacks, ask once if order or intent is ambiguous |

**One checkout at a time.** Never cherry-pick or mix commits from two concerns onto one PR unless the user asked to combine them.

Stacked branches: land the **ancestor** (closest to main) first. After each land, update remaining branches from new `origin/main`. Details in [reference.md](reference.md).

Already fully merged into `origin/main` (no unique commits): do not open a PR; go to Phase 10 delete after verify.

### Merge method (squash vs merge commit)

Detect once per repo, then use for every PR in this run unless the user overrides (“squash this” / “merge commit”).

```bash
gh repo view --json deleteBranchOnMerge,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
git log origin/main -20 --oneline
```

| Signal | Method |
|--------|--------|
| User said squash / squash-merge | `gh pr merge --squash --delete-branch` |
| User said merge commit / no squash | `gh pr merge --merge --delete-branch` |
| Recent main is mostly `Merge pull request #N` | `--merge` |
| Recent main is flat conventional commits (no merge commits) | `--squash` |
| Only squash allowed by GitHub | `--squash` |
| Only merge commits allowed | `--merge` |
| Tie / unclear | `--squash` (clean main; PR keeps full history) |
| Rebase-merge | Only if the user explicitly asks |

Do **not** use `--admin` / bypass. Do **not** `git merge` into local `main` as a substitute for the PR.

---

## Phase 2 — Switch onto the next queued branch

If already on it and the tree belongs to this branch → continue.

Before switching:

```bash
git status -sb
```

| Tree | Action |
|------|--------|
| Clean | `git switch <branch>` |
| Dirty, belongs to **current** branch | Commit (Phase 3) on current, then switch; or stash `wip <current>` if leaving it for later |
| Dirty, belongs to **target** branch | Stash or finish current first; then switch; then pop only the matching stash |
| Dirty, unrelated | Stash `wip <current>`; do not carry it onto the land branch |

Never start a land from `main` with uncommitted feature work still on `main`.

---

## Phase 3 — Commit leftovers

1. `git status` / `git diff` / `git diff --cached` / `git log -5 --oneline`
2. Stage relevant files (never secrets)
3. Conventional commit via HEREDOC (`feat|fix|chore|docs|refactor|test`); message focuses on **why**
4. Do not open a PR of half-committed intentional work unless the user asked for a draft PR

```bash
git commit -m "$(cat <<'EOF'
feat(area): short why

EOF
)"
git status -sb   # clean, or only noted exclusions
```

---

## Phase 4 — Update from `origin/main`

```bash
git fetch origin
git merge origin/main
```

Resolve conflicts preserving branch intent + main correctness. If intents conflict, stop and ask. Do not rebase a branch that already has a remote / open PR unless the user asks (would need force-push).

---

## Phase 5 — Push

```bash
git push -u origin HEAD
```

Non-fast-forward on the **topic** branch: fetch, merge the remote topic branch, push. No force unless the user explicitly allows force on that topic branch only. Never force `main`.

---

## Phase 6 — Pull request

```bash
gh pr view --json number,url,state,baseRefName,headRefName,mergeable,statusCheckRollup,title
```

If none exists:

```bash
gh pr create --base main --title "<conventional title>" --body "$(cat <<'EOF'
## Summary
- <1–3 bullets>

## Test plan
- [ ] Local typecheck / unit tests green
- [ ] Hosted CI green if Actions ran; else local gate (do not wait on billing-red)
- [ ] Spot-check: <paths touched>

EOF
)"
```

Ensure `baseRefName` is `main` (or the repo default). Return the PR URL.

Title: match recent merged PRs.

---

## Phase 7 — Merge gate (hosted CI or local)

The gate is **verification**, not billed GitHub minutes. Classify checks before
waiting or stopping.

```bash
gh pr checks
gh pr view --json mergeable,mergeStateStatus,statusCheckRollup,reviewDecision
```

If a check failed in a few seconds with empty steps, read the run annotations
(`gh run view <id>`). Billing / spending-limit text means jobs **never started**.

### Hosted CI classification

| Situation | Classification | Action |
|-----------|----------------|--------|
| Jobs in progress / queued with a runner | Hosted CI running | Wait / re-poll; do not merge |
| Required (or all) checks success | Hosted CI green | Phase 8 |
| Failure with install / typecheck / test / lint logs | Tests failed | Fix, commit, push, re-poll |
| Failure in seconds, empty steps, annotation about payments, spending limit, or Actions disabled | Hosted CI **unavailable** | Local gate. Do not ask to pay. Do not make the repo public |
| No checks configured | Hosted CI unused | Local gate |
| User said they don’t pay for Actions / skip GHA | Hosted CI out of scope | Local gate |
| Flaky / unrelated after merging `origin/main` | Out of scope | If hosted was otherwise usable: report and stop. If hosted is unavailable: local gate |
| Merge conflicts | — | Merge `origin/main` into the branch, resolve, push |
| Reviews required and blocking | — | Ask the user; do not `--admin` |
| GitHub **blocks** merge on required checks that never ran (Pro/public protection) | Blocked | Stop. Do not `--admin`. User may drop the requirement; paying is their choice, not this skill’s unblock |

Private GitHub Free repos typically **cannot** require status checks. A
billing-red X there does not block `gh pr merge`.

### Local gate (hosted unavailable or unused)

Run from the repo root. Fail-stop. Prefer `pnpm` when the repo uses it.

If `package.json` has `land`, `check`, or `build:check`, run that **instead** of
inventing a pack. Otherwise, first match per slot:

1. **Types:** `typecheck` (not `typecheck:tools` / `typecheck:all` unless that is the documented land command)
2. **Unit tests:** `test:run`, else `vitest run`, else skip and note it
3. **Lint:** `lint` only if the script exists and is the repo’s usual cheap gate

Do **not** default to Playwright e2e or `pnpm build` locally (slow, env-heavy).
Note them as not run in the done report.

If the local gate fails: fix at the lowest layer, commit, push, re-run. Same as
a real hosted failure.

If it passes and the PR is mergeable (not blocked by reviews or conflicts):
Phase 8. Record `gate=local` plus the commands in the done report.

Never flip repo visibility, buy minutes, or `--admin` to get a green GitHub check.

---

## Phase 8 — Merge

Only when the merge gate is green (hosted CI that **ran**, or local gate) and
the PR is mergeable.

```bash
# merge commit (history shows "Merge pull request #N")
gh pr merge --merge --delete-branch

# squash (flat main)
gh pr merge --squash --delete-branch
```

`--delete-branch` removes the **remote** topic branch after merge. Confirm:

```bash
gh pr view --json state,mergedAt,mergeCommit,url
```

State must be `MERGED`. If merge fails, stop — do not land via local merge to `main`.

---

## Phase 9 — Sync local main (required before delete)

```bash
git fetch --prune origin
git switch main
git pull --ff-only origin main
git status -sb
git log -1 --oneline
```

Assert:

- Current branch is `main`
- `main` is even with `origin/main`
- The landed commit (merge commit or squash SHA from the PR) is an ancestor of `HEAD`

```bash
git merge-base --is-ancestor <mergeCommit-or-squash-sha> HEAD && echo ON_MAIN
```

If `ON_MAIN` is missing, do not delete anything. Re-fetch; if still missing, stop and report.

---

## Phase 10 — Delete branches (only after Phase 9)

Remote is usually already gone from `gh pr merge --delete-branch`. Then:

```bash
git branch -d <topic-branch>          # safe delete; MUST fail if not merged
git fetch --prune origin
git remote prune origin
```

| Result | Action |
|--------|--------|
| `git branch -d` succeeds | Done for this branch |
| `git branch -d` refuses | **Stop.** Do not `-D`. Work is not on main (or this checkout diverged). Diagnose. |
| Remote branch still exists after merged PR | `git push origin --delete <topic-branch>` only after Phase 9 `ON_MAIN` |
| Branch checked out in another worktree | Remove/switch that worktree first; then `-d` |

Do not delete `main`. Do not prune stashes. Do not delete branches that were **not** in the land queue unless they are already merged and the user asked to clean leftovers.

---

## Phase 11 — Next branch or done report

If the queue has more entries: return to Phase 2.

When the queue is empty, report:

1. Branches landed (name + PR URL + squash vs merge)
2. Merge gate used: hosted CI, or local (commands run) because Actions was unavailable
3. Confirm: on `main`, synced with `origin/main`
4. Branches deleted (local / remote)
5. Skipped / still open (with why)
6. Stashes left untouched, secrets excluded, other follow-ups

---

## Anti-patterns

- Committing or merging on `main` directly
- Squashing or merging locally into `main` to “skip the PR”
- `git branch -D` / deleting remote before `origin/main` has the work
- Force-pushing `main`
- Switching branches with mixed WIP
- Landing two independent concerns in one PR without being asked
- Declaring done before main sync + verified ancestor + branch delete
- Including `.env` / secrets
- Dropping stashes
- `--admin` merge / `--no-verify`
- Rebase + force-push of a shared topic branch without an explicit ask
- Refusing to merge solely because GitHub Actions could not start (billing / spending limit)
- Making a repo public, or asking the user to pay for Actions, to unblock a land

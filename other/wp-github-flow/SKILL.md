---
name: wp-github-flow
description: "Use when shipping work through GitHub — fixing a GitHub issue by URL/number, or committing and PR-ing uncommitted working-tree changes. Covers resolving ISSUE_REPO vs CODE_REPO, grouping changes into scoped conventional commits (type(scope): summary), branching from fresh origin/base, discovering labels via gh label list, opening PRs with gh pr create, cross-repo Closes footer, merging with --merge (never --squash), and re-syncing after merge. Triggers: \"commit my changes\", \"commit scope by scope\", \"create a branch and PR\", \"open a PR for these changes\", \"fix issue #NNN\", \"debug this GitHub issue\", \"group my changes into commits\", \"push and open a PR\", \"what branch should I use\", \"conventional commit for this change\", \"close this issue with a PR\", \"write a PR description\", \"gh pr create\", \"gh issue view\", \"Closes footer\", \"branch name for this fix\", \"gh label list\", \"bugfix branch\", \"cross-repo close\", \"ISSUE_REPO vs CODE_REPO\", \"stale remote origin\", \"PR body template\", \"merge the open PR\", \"re-sync after merge\", \"sequential PRs\". Not for: plugin version releases — use `wp-plugin-release`; WP.org SVN — use `wp-org-submission`."
---

# GitHub Contribution Flow

> **Model note:** Issue-driven mode (root-cause tracing + fix) requires `sonnet` or `opus`. Changes-driven mode (group + commit existing edits) is mechanical and works well on `haiku`.

## Overview

Two entry modes that converge on the same shipping flow (branch → scoped commits → push → PR):

- **Issue-driven** — fetch issue → trace root cause → fix → ship. Wraps `superpowers:systematic-debugging`. Root cause MUST be confirmed before any fix is written.
- **Changes-driven** — read the working tree → group changes by conventional-commit scope → one commit per scope → ship. No issue required.

Both end at **§6 Branch, Commit, PR**, which is shared.

## When to use

**Issue-driven:**
- User says "analyze/debug/fix/investigate issue #NNN"
- User pastes a GitHub issue URL and asks to debug it
- User says "find the root cause of this bug" with an issue reference

**Changes-driven:**
- "commit my changes", "commit these scope by scope", "commit by scope"
- "create a branch and PR", "open a PR for these changes"
- "read all changes from X and commit + create PR"
- Any request whose end goal is commits/branch/PR from existing working-tree edits

**Not for:** Plugin version releases or WP.org SVN deploy — use `wp-plugin-release` and `wp-org-submission`. QA failure triage on an already-open PR — use `wp-ci-qa`.

## Required Sub-Skill

**Issue-driven only:** Invoke `superpowers:systematic-debugging` before any fix. Do NOT skip Phase 1 (root cause investigation). Changes-driven mode skips this — the edits already exist.

## References

- `references/gh-reference.md` — `gh` CLI commands, branch naming rules, label discovery, PR template sections, common CI failures
- `references/project-entry-points.md` — project layout template: repos, plugin dirs, entry-point files, and key conventions; copy and fill in for your project
- `references/conventional-commits.md` — type/scope table, WP-specific scope list, summary rules, multi-commit PR rules, footer conventions, rebase reword

## Repo ≠ where the issue lives

The repo that **hosts the issue** is often NOT the repo that **holds the code / receives the PR**. Resolve two names up front and keep them distinct:

- `ISSUE_REPO` — where `gh issue view` / `gh issue edit` run.
- `CODE_REPO` — where the affected code lives; where you branch, push, and `gh pr create --repo "$CODE_REPO"`.

When they differ, the PR's close footer must be **cross-repo**: `Closes ISSUE_OWNER/ISSUE_REPO#N` (a bare `Closes #N` only closes an issue in the same repo).

Real example: issues live in `my-org/my-plugin`, but the buggy code + PR live in `my-org/my-plugin-pro` → PR opens on `my-plugin-pro`, body says `Closes my-org/my-plugin#247`.

---

## Changes-Driven Workflow

Use this when the user wants to ship existing uncommitted edits. Skip to §6's mechanics but commit **scope by scope** rather than one lump.

### A. Read every change

```bash
git status
git diff           # unstaged
git diff --staged  # staged
```

Read the **full diff**, not just the file list — a single file can contain edits belonging to different scopes, and the commit message's "why" depends on what actually changed.

### B. Group changes by scope

Map each change to one conventional-commit scope. **Scopes are project-defined — read the repo's CLAUDE.md for the list, don't assume.**
- ShopFlow: `api, cart, checkout, orders, products, customers, payments, shipping, taxes, coupons, inventory, admin, dashboard, blocks, spa, database, templates, email, reports, build, i18n`.

Group by **what the change is about**, not just which directory it lives in. Examples from real sessions:
- `pages/Coupons/index.jsx` + `pages/Coupons/CouponList/index.jsx` → both `coupons`
- `pages/AbandonedCart/index.jsx`, `pages/Transactions/...` → `admin`
- `.yarnrc.yml`, `package.json` → `build`

One scope can span multiple files; one file *can* split across commits via `git add -p` if it genuinely mixes concerns (rare — prefer not to).

**Exception — one cohesive cross-cutting task = one commit.** Scope-by-scope is the default, but when the change is a *single logical task* that inherently touches many files across categories (e.g. fixing all findings from an audit, a mechanical rename, a dir restructure), a single commit with an **enumerated body** is cleaner and more honest than forcing fragile per-file `git add -p` splits. Judge by intent: distinct concerns → separate commits; one purpose expressed across many files → one commit.

### C. Branch first, then commit each scope

Create the branch (§6.1), then make **one commit per scope** so each is independently reviewable and revertable:

```bash
git add <files-for-scope-1>
git commit -m "fix(coupons): <imperative summary>"

git add <files-for-scope-2>
git commit -m "fix(admin): <imperative summary>"
# ...repeat per scope
```

Use the correct `<type>` per scope (`fix`, `feat`, `build`, `refactor`, …) — don't blanket-`fix` everything. Use `caveman:caveman-commit` for terse, exact messages.

### D. Push + PR

Push and open the PR via §6 — but the PR body summarizes **all** scopes, and there is no `Closes #N` unless an issue was given. PR title uses the dominant scope or a neutral summary across scopes.

> **Heads-up:** only commit what the user asked for. If `git status` shows unrelated files (e.g. a stray `package.json` from another task), call them out and leave them unstaged rather than sweeping them in.

---

## Issue-Driven Workflow

### 1. Detect Canonical Repo(s)

Before anything else, resolve the true repo(s) — remotes go stale when orgs rename or transfer, and the issue repo may differ from the code repo (see "Repo ≠ where the issue lives").

```bash
# What git thinks origin is, vs what GitHub actually says (follows redirects)
git remote get-url origin
gh repo view --json nameWithOwner -q .nameWithOwner

# If they differ — update origin
git remote set-url origin $(gh repo view --json cloneUrl -q .cloneUrl)
```

Store BOTH names — they may be the same, but never assume it:
```bash
ISSUE_REPO=my-org/my-plugin                # where the issue is tracked
CODE_REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)  # where you'll PR
```

### 2. Fetch Issue

```bash
gh issue view <number> --repo "$ISSUE_REPO" --comments
```

Extract: title, description, screenshots, reproduction steps, error messages, **and the comment thread** (assignee, "need to update API", "issue not found" all live there). For a parent/tracking issue, also fetch each sub-issue + its comments.

### 3. Locate Affected Code

- `grep -r` for identifiers, class names, function names from the issue
- Trace from UI/endpoint inward to data origin
- Check recent commits: `git log --oneline -- <file>`
- **Find the code's repo.** It may not be the issue repo, and not even the same plugin (free vs pro). `git -C <plugin-dir> remote get-url origin` to confirm which GitHub repo each path maps to → that's `CODE_REPO`.

### 4. Root Cause Investigation

Follow `superpowers:systematic-debugging` Phase 1 fully:

1. Read error messages / inspect screenshots carefully
2. Reproduce data flow mentally (or add logging)
3. Form ONE explicit hypothesis: "Root cause is X because Y"
4. Confirm hypothesis before writing any fix

**No fixes until root cause is stated and confirmed.**

### 5. Fix

One minimal change. No cleanup, no refactoring, no "while I'm here" edits.

### 6. Branch, Commit, PR  *(shared by both modes)*

```bash
# Confirm base branch with user if unclear — never assume main/develop
BASE_BRANCH=<ask-user>
```

**6.1 — Create branch from the FRESH base.** Local branches go stale; always branch from `origin/<base>` after fetching, so the PR diff is clean.

```bash
git fetch origin "$BASE_BRANCH"
git checkout -b <branch> "origin/$BASE_BRANCH"
```

Name it by mode:
- Issue-driven: `bugfix/<issue-number>-<short-description>`
- Changes-driven: `<type>/<short-description>` (e.g. `fix/container-height-full`)

**Cluster (multiple sub-issues):** do NOT lump fixes for several issues into one branch. One branch + one PR **per issue**, each cut fresh from `origin/$BASE_BRANCH`, each `Closes` its own issue. Fix file A on its branch → push → PR → `git checkout "$BASE_BRANCH"` → next. Independent files = no conflicts.

**6.2 — Commit.** Use `caveman:caveman-commit` for messages.
- *Issue-driven:* one minimal commit, with `Closes #<issue-number>` footer.
- *Changes-driven:* one commit **per scope** (see Changes-Driven §C). No `Closes` unless an issue was given.

```bash
git add <files-for-scope>
git commit -m "fix(<scope>): <imperative summary>"   # +blank line + why + Closes when issue-driven
```

Follow project conventions in the repo's CLAUDE.md — check it for deprecated function patterns, naming conventions, and scope definitions before committing.

**6.3 — Push (must happen before the PR).** `gh pr create` fails with *"must first push the current branch"* if you skip this.

```bash
git push -u origin <branch>
```

**6.4 — Discover labels, THEN create the PR.** Label names are per-repo; `gh pr create` **aborts the whole command** if any `--label` doesn't exist (e.g. `needs testing` vs `needs-testing`). List them first and map to what's real:

```bash
gh label list --repo "$CODE_REPO"
```

Then create — always pass `--repo "$CODE_REPO"` (gh context can differ from git remote), `--assignee @me`, and only labels that exist. Common mapping: a "ready for QA" label (`needs-testing` / `needs testing`) + an area label (`frontend`, `backend`). **Never add `bug` — QA assigns it if they find issues; dev-added `bug` conflicts with QA triage.** Cross-repo close footer when `ISSUE_REPO ≠ CODE_REPO`.

```bash
gh pr create \
  --repo "$CODE_REPO" \
  --base "$BASE_BRANCH" \
  --assignee @me \
  --label "<verified-qa-label>" \
  --label "<verified-area-label>" \
  --title "<type>(<scope>): <summary>" \
  --body "$(cat <<'EOF'
## 📝 Summary
<what this PR does — cover all scopes if multi-commit>

---

## 🛠️ Related Issues / Tickets
Closes <ISSUE_OWNER>/<ISSUE_REPO>#<issue-number>   <!-- bare "Closes #N" only if same repo; omit section if no issue -->

---

## 📦 Type of Change
- [x] 🐛 Bug fix   <!-- adjust to feat/refactor/build as appropriate -->

---

## 🔍 Changes Made
- <bullet per scope: what changed and why>

---

## 🧪 Test Instructions
1. <step>
2. <step>

---

## ✅ Checklist
- [x] My code follows the project's coding style and conventions
- [x] This PR is scoped, focused, and doesn't mix unrelated changes
EOF
)"
```

> **Verification honesty:** if an automated test isn't feasible (e.g. Elementor edit-mode render needs a bootstrap the suite lacks), say so plainly in the checklist and rely on `php -l` + manual steps — don't claim a test you didn't write.

**6.5 — Merge PR.** When the user asks to merge a PR, always use a **regular merge commit** (`--merge`). Never squash (`--squash`) — it collapses the branch's individual commits into one, destroying the per-scope history that §6.2 deliberately preserved. Never rebase (`--rebase`) unless the user explicitly requests it.

```bash
gh pr merge <number> --merge --delete-branch
```

`--delete-branch` is safe and keeps the remote tidy. Do not add `--squash` or `--rebase`.

**6.6 — After merge: verify, then re-sync before the next branch.** A merge isn't done until it's confirmed landed and local `main` is caught up — otherwise the next branch is cut from a stale base.

```bash
gh pr view <number> --json state,mergedAt -q '{state: .state, mergedAt: .mergedAt}'  # expect MERGED
git checkout "$BASE_BRANCH"
git pull origin "$BASE_BRANCH"
git rev-parse "$BASE_BRANCH"; git rev-parse "origin/$BASE_BRANCH"   # must match
```

## Sequential PRs in one session

When an open PR already exists and the user asks for the **next** piece of work, do NOT stack the new changes on the unmerged branch. The user's preferred flow:

1. **Merge the open PR first** (`gh pr merge <n> --merge --delete-branch`).
2. **`git checkout "$BASE_BRANCH"` + `git pull`** so the base is current.
3. **Branch fresh** off the updated base for the new work.

If the new work genuinely depends on the unmerged branch and can't wait, branch off *that* branch and rebase onto the base once it merges (the cluster pattern) — but the default is merge-first.

## Keep an open PR's body in sync

If you push **more commits** to a branch whose PR is already open (scope grew mid-review), update the PR title/body so the description still matches the diff:

```bash
gh pr edit <number> --title "<updated>" --body "$(cat <<'EOF'
...all scopes now in the PR...
EOF
)"
```

A PR body that lists only half the commits reads as "the rest snuck in."

---

## Quick Reference

| Step | Tool |
|------|------|
| Detect code repo | `gh repo view --json nameWithOwner` / `git -C <dir> remote get-url origin` |
| Fix stale remote | `git remote set-url origin <new-url>` |
| Fetch issue + comments *(issue mode)* | `gh issue view <n> --repo "$ISSUE_REPO" --comments` |
| Read changes *(changes mode)* | `git status`, `git diff`, `git diff --staged` |
| Find code | `grep -r`, `find`, file reads |
| Branch from fresh base | `git fetch origin "$BASE_BRANCH" && git checkout -b <b> "origin/$BASE_BRANCH"` |
| Commit message | `caveman:caveman-commit` |
| Discover labels (before PR) | `gh label list --repo "$CODE_REPO"` |
| Push (before PR) | `git push -u origin <branch>` |
| Create PR | `gh pr create --repo "$CODE_REPO" --base "$BASE_BRANCH" --assignee @me --label "<verified>"` |
| Merge PR | `gh pr merge <number> --merge --delete-branch` — **never `--squash` or `--rebase`** |
| Verify merge + re-sync | `gh pr view <n> --json state,mergedAt` then `git checkout <base> && git pull` (rev-parse local == origin) |
| Update open PR after new commits | `gh pr edit <number> --title … --body …` |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoded repo name | Always derive from `gh repo view --json nameWithOwner` |
| Assuming issue repo == code repo | Resolve `ISSUE_REPO` + `CODE_REPO` separately; PR on `CODE_REPO`; cross-repo `Closes owner/repo#N` |
| Stale `origin` remote | Run remote detect step (§1) before every push |
| Branching off a stale local base | `git fetch origin <base>` then branch from `origin/<base>` |
| `gh pr create` without `--repo` | `gh` context can differ from `git` remote — always pass `--repo "$CODE_REPO"` |
| PR command before pushing branch | Push first — `gh pr create` errors "must first push the current branch" |
| Hardcoded label aborts PR | `gh label list` first; one unknown `--label` fails the whole `gh pr create` |
| Lumping multiple issues in one branch | One branch + PR per issue, each from fresh `origin/<base>` |
| Claiming an automated test you didn't write | If a test isn't feasible, say so; rely on lint + manual steps, stated plainly |
| One lumped commit for mixed changes | Changes mode: split by scope, one commit each |
| Reading only the file list | Read full `git diff` — a file can mix scopes, and the "why" needs the actual change |
| Sweeping in unrelated files | Only stage what the user asked for; flag stray changes, leave them unstaged |
| Blanket `fix:` on everything | Pick the right `<type>` per scope (`feat`/`build`/`refactor`/…) |
| `Closes #N` with no issue | Omit the issue section entirely in changes mode |
| Fix without root cause *(issue mode)* | State hypothesis explicitly before coding |
| Fixing symptom not origin *(issue mode)* | Trace full data flow to find where bad value is born |
| Wrong base branch | Ask user; never assume `develop` or `main` |
| Missing assignee | Always pass `--assignee @me` |
| Missing QA label | Add the repo's "ready for QA" label (verify exact name via `gh label list`) |
| Missing area label | Add the repo's area label (`frontend`/`backend`/…) — whatever exists; never add `bug` |
| Adding `bug` label on a dev PR | **Never.** `bug` is QA's label — they add it only if they find issues during testing. Dev-adding it conflicts with QA triage. |
| Bundled refactoring in fix | One change only — keep diff minimal |
| Squash merge | **Never** use `--squash` — destroys per-scope commit history. Use `--merge` always. |
| Rebase merge without being asked | Never use `--rebase` unless user explicitly requests it — rewrites SHAs, breaks bisect. |
| Stacking next task on an unmerged PR branch | Merge the open PR first, `git pull` the base, then branch fresh (Sequential PRs). |
| Branching after merge without re-pulling | A merge updates the remote base, not your local — `git checkout <base> && git pull` before the next branch. |
| Open PR body stale after new commits | `gh pr edit` the body to cover every commit now on the branch. |
| Forcing per-file splits on one cohesive task | An audit cleanup / rename / restructure is one commit with an enumerated body — not fragile `git add -p`. |

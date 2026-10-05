---
name: github
description: Complete GitHub workflow — auth, PRs, code review, issues, repo management. Works with gh CLI or git+curl fallback.
version: 2.0.0
tags: [GitHub, Git, Pull-Requests, Code-Review, Issues, Repositories, CI/CD]
---

# GitHub

Unified GitHub workflow. Each section shows `gh` CLI first, then `git` + `curl` fallback for environments without `gh` installed. All sections share the same auth bootstrap (see §Auth).

## Detecting Auth Method

At the start of any GitHub workflow, determine what's available:

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH=***  AUTH=***
fi
# Fallback: extract token from env, ~/.hermes/.env, or ~/.git-credentials
if [ -z "$GITHUB_TOKEN" ]; then
  if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
    GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
  elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
    GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  fi
fi
```

### gh CLI first, Python urllib last

When fetching GitHub data (issue lists, PR lists, commit search, repo metadata): **default to `gh`** — `gh issue list --search`, `gh pr list --search`, `gh search commits`, `gh api repos/...`. Don't reach for `python3 -c "import urllib.request; json.load(...)"` to hit the GitHub API. Reasons:

- `gh search <type> ... --json ... --jq ...` is one command. Python + urllib is a 5-line subprocess with quoting hazards.
- `gh` handles auth, pagination, rate-limit headers, and error formatting for you.
- Subshelling output into `python3 -c` triggers Hermes' smart-approval gate on every call.

Use raw curl/python only when `gh` cannot do what you need (e.g. custom GraphQL queries, multi-endpoint scripts that need fine-grained control). For "show me upstream issues about X", `gh issue list --repo upstream --search X --json ... --jq ...` is the right tool.

Within `gh`, prefer structured output (`--json` + `--jq`) over `grep`-ing human output — same reason, plus it's parseable programmatically.

Extract owner/repo from git remote:
```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

## §Auth — Authentication Setup

### Git-Only (HTTPS Token)

1. User creates a **personal access token** at https://github.com/settings/tokens with `repo`, `workflow`, `read:org` scopes
2. Set up credential helper: `git config --global credential.helper store`
3. Do a test operation that triggers auth — username is their GitHub username, password is the token
4. Configure identity: `git config --global user.name "Name"` and `git config --global user.email "email"`

### Git-Only (SSH)

```bash
ssh-keygen -t ed25519 -C "email" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub  # Add to https://github.com/settings/keys
ssh -T git@github.com
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### gh CLI Auth

```bash
echo "<token>" | gh auth login --with-token
gh auth setup-git
```

### Helper script

`scripts/gh-env.sh` — reusable auth detection script.

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | Use personal access token as password, not GitHub password |
| `gh` commands return `EOF` on WSL with proxy | Prefix with `no_proxy='*'` |
| Credentials not persisting | Check `git config --global credential.helper` |

## §PR — Pull Request Workflow

### Complete PR Lifecycle

```bash
# 1. Branch
git checkout main && git pull origin main
git checkout -b feat/description

# 2. Commit (Conventional Commits)
git add <files>
git commit -m "feat: short description

- Detail 1
- Detail 2"

# 3. Push
git push -u origin HEAD

# 4. Create PR
gh pr create --title "feat: ..." --body "...\nCloses #42"
# Or curl: POST /repos/$OWNER/$REPO/pulls with head=<branch> base=main
```

**Branch naming:** `feat/`, `fix/`, `refactor/`, `docs/`, `ci/`

**Commit format:** See `references/conventional-commits.md`

### Monitoring CI

```bash
gh pr checks
gh pr checks --watch  # poll until done
```

**Auto-fix CI loop:** Check status → read failure logs → fix code → commit+push → re-check (max 3x). See `references/ci-troubleshooting.md`.

### Merging

```bash
# Squash merge
gh pr merge --squash --delete-branch
# Auto-merge when checks pass
gh pr merge --auto --squash --delete-branch
```

### WSL Proxy Pitfall

When running `gh` in WSL with local HTTP proxy (`http://127.0.0.1:7890`), prefix all `gh` and `curl` GitHub API calls with `no_proxy='*'`. Git operations (push/pull/clone) work fine — only `gh`'s REST/GraphQL API calls need this.

### PR Body Templates

- `templates/pr-body-feature.md`
- `templates/pr-body-bugfix.md`

## §Review — Code Review

### Pre-Push Review (git only)

```bash
git diff main...HEAD --stat
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|debugger"
```

### PR Review Workflow

1. Gather context: `gh pr view N`, `gh pr diff N --name-only`, `gh pr checks N`
2. Check out locally: `git fetch origin pull/N/head:pr-N && git checkout pr-N`
3. Review against the checklist below
4. Post review:

```bash
gh pr review N --approve --body "LGTM!"
gh pr review N --request-changes --body "See inline comments."
```

### Review Checklist

- **Correctness:** Does it do what it claims? Edge cases?
- **Security:** No hardcoded secrets, input validation, no SQLi/XSS
- **Code Quality:** Clear naming, DRY, single responsibility
- **Testing:** New paths tested? Happy + error cases?
- **Performance:** No N+1 queries, appropriate caching
- **Documentation:** Public APIs documented, README updated

**Output format:** See `references/review-output-template.md`

## §Issues — Issue Management

### View and Create

```bash
gh issue list --state open --label "bug"
gh issue view 42
gh issue create --title "..." --body "..." --label "bug,backend" --assignee "username"
```

### Manage

```bash
gh issue edit 42 --add-label "priority:high" --add-assignee @me
gh issue comment 42 --body "..."
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### Templates

- `templates/bug-report.md`
- `templates/feature-request.md`

## §Repo — Repository Management

### Common Operations

```bash
# Create
gh repo create my-project --public --clone

# Clone
git clone https://github.com/owner/repo.git
git clone --depth 1 https://github.com/owner/repo.git

# Fork
gh repo fork owner/repo --clone
git remote add upstream https://github.com/owner/repo.git

# Secrets
gh secret set API_KEY --body "value"
gh secret list

# Releases
gh release create v1.0.0 --title "v1.0.0" --generate-notes

# CI/Actions
gh workflow list
gh run list --limit 10
gh run view <ID> --log-failed
gh run rerun <ID>
```

### Fork Sync

#### Quick Diagnostics

Before syncing, check the fork's relationship to upstream:

```bash
# Check if behind/ahead (no local clone needed)
no_proxy='*' gh api repos/$OWNER/$REPO/compare/NousResearch:main...main \
  --jq '{status, ahead_by, behind_by}'

# Try GitHub's native fork sync (only works when cleanly behind)
no_proxy='*' gh api repos/$OWNER/$REPO/merge-upstream -X POST -f branch=main
```

#### Manual Sync (local clone)

```bash
git fetch upstream && git rebase upstream/main && git push --force-with-lease origin main
```

Use `rebase` + `--force-with-lease` instead of `merge` to keep history clean when the fork has its own commits (workflows, patches). The fork's commits stay on top.

**Check branch protection first** — force push fails on protected branches:
```bash
gh api repos/$OWNER/$REPO/branches/main/protection
# HTTP 404 → not protected → force push OK
# 200 → protected → either disable protection or use merge strategy
```

#### Diagnosing "Sync fails repeatedly"

Before debugging further, identify whether the failure is:

1. **Network / auth** — fetch log says "could not resolve" or "401". Fix token.
2. **Workflow-level error** — see `references/ci-troubleshooting.md`.
3. **Merge conflict storm** — log shows dozens of `CONFLICT (add/add)` lines. Read below.

**Conflict storm** means the fork was many weeks/months behind. Three or fewer conflicts → resolve by hand. Tens to hundreds → reset path. See "Reset path when conflicts are unrecoverable" below.

#### Verifying a workflow YAML fix

After any change to `.github/workflows/*.yaml`:

```bash
# Re-trigger immediately (don't wait for next schedule)
gh workflow run <workflow-file> -R OWNER/REPO

# Wait + read the actual failure, not your YAML interpretation
sleep 15 && gh run view $(gh run list -R OWNER/REPO --workflow=<file> --limit 1 --json databaseId -q '.[0].databaseId') --log-failed
```

This is the fastest loop: edit YAML → push → `gh workflow run` → log shows real cause. Cheaper than rerunning CI in your head.

**Also `prettier --check` it** if the repo has prettier configured — many Next.js / Vercel-deployed repos run `prettier --check` in CI over the entire repo including `.github/workflows/*.yaml`. Cron strings must be single-quoted (`'0 0 * * *'`, not `"0 0 * * *"`) to match the project's `.prettierrc.json` `singleQuote: true`. Format drift = CI fails despite correct semantics.

```bash
npx prettier --check .github/workflows/<file>.yaml
```

#### Upstream repo moved / got renamed

### Bug-fix path: search upstream first, don't fork-patch based on guesswork

When investigating a fork-only build failure or runtime bug that **might be an upstream regression**:

1. **Search upstream issues before proposing a fork patch.** `gh issue list -R <upstream> --search "<exact error fragment>"`, `gh pr list --state all -R <upstream> --search "<error fragment>"`. If a closed issue + merged PR exists, the canonical fix path is to wait for it OR cherry-pick onto the fork.
2. **Search upstream commit history.** `gh search commits "<error fragment>" -R <upstream> --json sha,commit`. If 0 results, the issue IS novel — and your fork patch is the first instance, not a duplicate.
3. **Read the actual error log, not your interpretation.** `gh run view <id> --log-failed`, `curl .../v1/deployments/dpl_<id>/events`, or `gh pr checks` + artifacts. Don't summarize "this is upstream's fault" from a one-line summary field.
4. **One-line guard on the fork is correct when upstream is silent.** Don't add "wait for upstream to fix it" as the default. Upstream maintainers are slow on edge-case schema bugs (Notion block schema edge cases, slow gitignore additions, etc.). A one-line Array.isArray guard on the fork is the lazy fix: small diff, deletable once upstream ships the proper fix.

The wrong reflex: see build error → assume "upstream must be broken, reverting is safest" → tell user to roll back the fork. That removes the bug from sight but loses all the upgrade. The right reflex is the four steps above.

### Conflict-storm fork reset (canonical example)


```bash
# Is the configured upstream_repo still a real repo?
gh api repos/tangly1024/NotionNext 2>&1 | head -3   # returns 404 if moved
```

If moved, edit the workflow's `upstream_sync_repo:` to the new path and push. **One-line semantic fix**, but it does NOT resolve existing conflict accumulation — that still requires manual sync (see "Reset path" below).

#### Reset path when conflicts are unrecoverable

When `git rebase upstream/main` (or `git merge upstream/main`) produces **20+ add/add conflicts across themes/, components/, blog.config.js, package.json**, the fork and upstream have diverged enough that hand-merging is no longer the right move. Branch protection rules or auto-release workflows on the fork will reject naive merges.

**Pattern: identify fork-only commits, then `git reset --hard upstream/main`.**

```bash
# 1. Identify fork-only commits
MERGE_BASE=$(git merge-base origin/main upstream/main)
git log origin/main ^$MERGE_BASE --oneline --no-merges

# 2. Back up fork-only files BEFORE resetting (e.g. blog.config.js, personal themes)
cp blog.config.js /tmp/blog.config.js.backup

# 3. Reset hard to upstream
git fetch upstream main
git reset --hard upstream/main

# 4. Re-apply fork-only files (or cherry-pick their commits)
cp /tmp/blog.config.js.backup blog.config.js
# If fork has real commits worth keeping, cherry-pick them:
git cherry-pick <fork-only-sha1> <fork-only-sha2>

git push --force-with-lease origin main
```

**Before reset — check branch protection** as in the prior section.

This is destructive. Get user confirmation before running it against any repo that's not a personal fork. For their own fork with no active downstream consumers, prefer reset over drowning them in 200+ conflict markers.

**Safer alternative: reset onto a NEW branch and open a PR** — when the fork is the live deployment (e.g. a Vercel deploy hooked to `main`, or a personal blog with active traffic), force-pushing `main` is risky even with `--force-with-lease`. Reset onto a new orphan branch and let the user review-merge.

### When the orphan PR also conflicts — promote reset-upstream branch to default

If the resulting PR against the divergent `main` shows `mergeable: CONFLICTING` with 1000+ changed files, hand-merging is again not viable. **Promote the reset branch to the new default, then replace `main` via the API in four steps.** GitHub's REST API refuses `DELETE` on the default branch (HTTP 422 "Cannot delete the default branch"), so you cannot delete `main` first — you must point default elsewhere, delete, recreate.

```bash
# 1. Point default at the reset branch (the API will let you delete main after this)
no_proxy='*' gh api repos/$OWNER/$REPO -X PATCH -f default_branch=reset-upstream

# 2. Now main is deletable
no_proxy='*' gh api repos/$OWNER/$REPO/git/refs/heads/main -X DELETE

# 3. Recreate main pointed at the reset branch's HEAD SHA
SHA=$(no_proxy='*' gh api repos/$OWNER/$REPO/git/refs/heads/reset-upstream --jq '.object.sha')
no_proxy='*' gh api repos/$OWNER/$REPO/git/refs -X POST -f ref=refs/heads/main -f sha="$SHA"

# 4. Delete the temporary reset branch and restore default to main
no_proxy='*' gh api repos/$OWNER/$REPO/git/refs/heads/reset-upstream -X DELETE
no_proxy='*' gh api repos/$OWNER/$REPO -X PATCH -f default_branch=main
```

After this, `main` HEAD == reset branch HEAD; the conflicting PR auto-closes (base removed). Run the sync workflow once to confirm the reset repo is in a clean sync state:

```bash
gh workflow run "Upstream Sync" -R $OWNER/$REPO
sleep 15 && gh run view $(gh run list -R $OWNER/$REPO --workflow="Upstream Sync" --limit 1 --json databaseId -q '.[0].databaseId') -R $OWNER/$REPO --json status,conclusion
# Expect: conclusion=success, log line "No new commits to sync. Finishing sync action gracefully."
```

### Local clone fails or PR diff explodes — drive everything via gh API

For forks that timeout on `git fetch` (large repos, shallow history, WSL+proxy), or whose PR diff exceeds GitHub's 300-file limit (`HTTP 406: PullRequest.diff too_large`):

- Skip the local clone. Use `gh api .../git/refs/heads/X --jq '.object.sha'` to read SHAs, `gh api .../git/refs -X POST` to create refs, `gh api .../contents/path -X PUT -f base64content` to write files.
- For PR review, dump files via `gh pr view N --json files` and `diff --name-only` the reset branch against upstream `git diff upstream/main origin/reset-upstream --stat` — gives a clean overlay view even when the fork main and reset-upstream have wildly diverged histories.
- For the conflict-storm reset itself, read fork-only files via `git show origin/main:<path>` into `/tmp`, then `cp` them back on top of `git checkout --orphan ... upstream/main`. No full clone needed.

### `merge-base` returns nothing with shallow clones against huge upstream

When `git fetch --depth=N upstream main` fails with `Could not read <sha>` / `Failed to traverse parents` (too shallow for that root) but you cannot `--unshallow` because the upstream is too big, swap who you shallow: clone the **fork side** with enough history (`git fetch --unshallow origin main` works because the fork is small), then run `git merge-base origin/main upstream/main`. The merge-base only needs enough fork-side history to reach a common ancestor.

```bash
# Orphan branch on top of upstream
git checkout --orphan reset-upstream upstream/main
git pull upstream main

# Re-apply fork-only overlays
cp /tmp/blog.config.js.backup blog.config.js
# ... other overlays ...
git add -A && git commit -m "chore(rebase): reapply fork overlays on upstream <version>"

git push origin reset-upstream
gh pr create --repo OWNER/REPO --base main --head reset-upstream \
  --title "chore(rebase): reapply fork overlays on upstream <version>" \
  --body "$(cat <<'EOF'
## 背景
<why reset was needed — usually 1.5+ months of conflict accumulation>

## Reapplied N fork-only files
- blog.config.js (personal config)
- conf/*.config.js (overrides)
- public/css/custom.css, public/favicon.ico

## 砍掉的 fork 历史
<list dropped commits / sync-merge traces>

> 没动 main。review 完 diff 觉得 OK 再 merge。
EOF
)"

# Wait for user to merge; do NOT auto-merge.
```

The PR diff will show **thousands of files** because the fork main and upstream main have diverged histories — that's normal, not a bug. Add a review comment explaining how to see the *real* overlay:

> PR diff 大但是正常。真实 overlay 只有 11 个文件:
>
> `git fetch origin reset-upstream && git diff upstream/main origin/reset-upstream --stat`
>
> GitHub 跟分叉的 main 三方 diff 会把历史里"消失"的所有文件列成 deletion —— 不影响实际 review。

After merge, manually trigger the sync workflow once to verify the reset-to-upstream state is now sync-clean:
```bash
gh workflow run "Upstream Sync" -R OWNER/REPO
```

#### Auto-release workflows clash with manual pushes

Many forks enable `bump-version-on-main` (or similar) auto-bump workflows. Result: between your `git fetch` and your `git push`, a release commit lands on `origin/main`, and your push is rejected for non-fast-forward.

**Always pull --rebase before push on any fork with scheduled auto-bump workflows:**

```bash
git pull --rebase origin main && git push origin main
```

Or check with `git fetch origin main` first, then rebase — either way the local branch must fast-forward cleanly.

#### Automated Sync via GitHub Actions

For forks that should stay continuously synced, use a scheduled workflow. Create it directly on the fork via the API (no local clone needed):

```bash
# Create workflow file via API
cat > /tmp/sync.yml << 'EOF'
name: Sync Upstream
on:
  schedule:
    - cron: "0 3 * * *"   # daily at 3 AM UTC
  workflow_dispatch:       # manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    if: github.repository == 'OWNER/REPO'   # guard: only run on fork
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - run: |
          git remote add upstream https://github.com/UPSTREAM_OWNER/UPSTREAM_REPO.git
          git fetch upstream main
          BEHIND=$(git rev-list --count HEAD..upstream/main)
          if [ "$BEHIND" -eq 0 ]; then
            echo "Already up to date"
            exit 0
          fi
          echo "Syncing $BEHIND commit(s)..."
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git rebase upstream/main
          git push --force-with-lease origin main
EOF

CONTENT=$(base64 -w0 /tmp/sync.yml)
no_proxy='*' gh api --method PUT \
  repos/OWNER/REPO/contents/.github/workflows/sync-upstream.yml \
  -f message="ci: add upstream auto-sync" \
  -f content="$CONTENT" \
  -f branch="main"

# Trigger immediately to verify
gh workflow run sync-upstream.yml -R OWNER/REPO
sleep 15 && gh run view $(gh run list -R OWNER/REPO --workflow sync-upstream.yml --limit 1 --json databaseId -q '.[0].databaseId') -R OWNER/REPO --log | grep -E "(Already|Syncing)"
```

**Default branch not protected** is required on the fork for `--force-with-lease`. The `if: github.repository` guard prevents the workflow from accidentally running in the upstream repo.

#### Creating/Updating Files via gh API

When you need to write a file to a repo without cloning it locally:

```bash
# Create (no sha param):
CONTENT=$(base64 -w0 file.txt)
gh api --method PUT repos/OWNER/REPO/contents/path/to/file \
  -f message="commit message" -f content="$CONTENT" -f branch="main"

# Update (requires sha of current file):
SHA=$(gh api repos/OWNER/REPO/contents/path/to/file --jq '.sha')
gh api --method PUT repos/OWNER/REPO/contents/path/to/file \
  -f message="update" -f content="$CONTENT" -f sha="$SHA" -f branch="main"
```

See `references/fork-sync-workflow.yml` for the ready-to-use template.

### GitHub Pages Subdirectory Pitfall

When deploying to `https://<user>.github.io/<repo>/`, asset paths MUST include the repo name as a prefix. For Next.js: `basePath: "/repo-name"` in `next.config.ts`.

### API Cheatsheet

See `references/github-api-cheatsheet.md` for full REST API reference.

## Quick Reference

| Action | gh | curl |
|--------|-----|------|
| List PRs | `gh pr list` | `GET /repos/{o}/{r}/pulls` |
| View PR diff | `gh pr diff N` | `git diff main...HEAD` |
| Create PR | `gh pr create ...` | `POST /repos/{o}/{r}/pulls` |
| Merge PR | `gh pr merge --squash` | `PUT /repos/{o}/{r}/pulls/N/merge` |
| List issues | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| Close issue | `gh issue close N` | `PATCH /repos/{o}/{r}/issues/N` |
| Create repo | `gh repo create name` | `POST /user/repos` |
| Fork | `gh repo fork o/r` | `POST /repos/o/r/forks` |
| Create release | `gh release create v1` | `POST /repos/o/r/releases` |
| List workflows | `gh workflow list` | `GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `PUT /repos/o/r/actions/secrets/KEY` |

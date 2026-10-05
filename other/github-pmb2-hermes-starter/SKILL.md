---
name: github
description: "Complete GitHub workflow management — authentication setup, repository management, issue triage, PR lifecycle (branch/commit/open/CI/merge), code review (local and PR), release management, actions workflows, secrets, and repo creation. One class-level skill replacing five narrow siblings."
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, pull-requests, issues, code-review, ci-cd, repositories, auth, releases, actions, secrets]
    triggers:
      - github authentication
      - github PR workflow
      - github code review
      - github issues
      - github repo management
      - github release
      - github actions
      - github secrets
      - git setup on github
    related_skills: [vcs-management, github]
---

# GitHub Workflow Management

Complete tooling for all GitHub operations — authentication, repos, PRs, issues, code review, releases, CI/CD. One umbrella replacing five narrow skills.

**Structure:**
1. **Shared Setup** — auth detection, owner/repo extraction
2. **Authentication** — tokens, SSH, gh CLI
3. **Repository Management** — clone, create, fork, settings, secrets, releases
4. **PR Workflow** — branch, commit, push, CI monitoring, auto-fix, merge
5. **Code Review** — local changes, PR review, inline comments, review submission
6. **Issue Management** — create, triage, label, assign, comment, close

---

## 1. Shared Setup

Every GitHub workflow starts with auth detection and owner/repo extraction:

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
  GH_USER=$(gh api user --jq '.login' 2>/dev/null)
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
  GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])" 2>/dev/null || echo "")
fi

REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

---

## 2. Authentication

Two methods — `gh` CLI or git-only (token/SSH).

### gh CLI
```bash
gh auth login          # interactive
echo "$TOKEN" | gh auth login --with-token  # headless
gh auth setup-git      # propagate to git
```

### Git-Only — HTTPS Token
```bash
git config --global credential.helper store
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
# First push prompts for username + token (not password)
```

### Git-Only — SSH
```bash
ssh-keygen -t ed25519 -C "email@example.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub  # add to github.com/settings/keys
ssh -T git@github.com      # verify
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### Troubleshooting
| Problem | Fix |
|---------|-----|
| `Permission denied` | Token lacks `repo` scope |
| `git push` asks for password | Use personal access token as password |
| SSH port 22 blocked | Add `Host github.com` with `Port 443` to `~/.ssh/config` |
| `gh: command not found` | Use git-only method |

---

## 3. Repository Management

### Clone / Create / Fork

```bash
# Clone
git clone https://github.com/owner/repo.git
gh repo clone owner/repo

# Create (gh) — fresh project
gh repo create my-project --public --clone
gh repo create my-project --private --description "..." --clone

# Create (gh) — from existing local directory with files
# Initialize locally first, then push to a new repo:
git init && git add -A && git commit -m "Initial commit"
gh repo create my-project --private --description "..." --source . --remote origin --push

# Or: create empty repo first, then point local dir at it:
gh repo create my-project --private
git remote add origin https://github.com/OWNER/my-project.git
git push -u origin main

# Create (curl)
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"my-project","private":false,"auto_init":true}'

# Fork
gh repo fork owner/repo --clone
# Or via API + git
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/forks
git clone https://github.com/$GH_USER/repo.git
cd repo && git remote add upstream https://github.com/owner/repo.git

# Keep fork in sync
git fetch upstream && git checkout main && git merge upstream/main && git push origin main
```

### Repository Settings

```bash
# gh
gh repo edit --description "..." --visibility public
gh repo edit --enable-wiki=false --default-branch main
gh repo edit --add-topic "machine-learning,python"

# curl
curl -s -X PATCH -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{"description":"...","has_wiki":false}'

# Branch protection
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{"required_status_checks":{"strict":true,"contexts":["ci/test"]},"required_pull_request_reviews":{"required_approving_review_count":1}}'
```

### Secrets (GitHub Actions)

```bash
gh secret set API_KEY --body "value"
gh secret set SSH_KEY < ~/.ssh/id_rsa
gh secret list
```

For curl, encrypt with the repo's public key (see `references/secrets-curl.md`).

### Releases

```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease
gh release create v1.0.0 ./dist/binary --title "v1.0.0"
gh release list
gh release download v1.0.0 --dir ./downloads

# curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{"tag_name":"v1.0.0","name":"v1.0.0","draft":false,"prerelease":false}'
```

### Actions Workflows

```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main

# curl
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10"
# Re-run
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun-failed-jobs
```

### Gists

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list

# curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/gists \
  -d '{"description":"...","public":true,"files":{"script.py":{"content":"print(\"hello\")"}}}'
```

---

## 4. PR Workflow

### Branch + Commit

```bash
git fetch origin
git checkout main && git pull origin main
git checkout -b feat/add-auth

# After making changes:
git add src/auth.py src/models/user.py
git commit -m "feat: add JWT-based user authentication"
git push -u origin HEAD
```

### Create PR

```bash
gh pr create \
  --title "feat: add JWT-based authentication" \
  --body "## Summary\\nAdds login/register endpoints.\\n\\nCloses #42" \
  --label "enhancement"

# curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d '{"title":"feat: ...","head":"feature-branch","base":"main"}'
```

Options: `--draft`, `--reviewer user1,user2`, `--base develop`

### Monitor CI

```bash
gh pr checks
gh pr checks --watch  # polls every 10s

# curl polling
SHA=$(git rev-parse HEAD)
for i in $(seq 1 20); do
  STATUS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")
  [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] && break
  sleep 30
done
```

### Auto-Fix CI Failures

```bash
# Get failure details
gh run list --branch $(git branch --show-current) --limit 5
gh run view <RUN_ID> --log-failed

# Fix, commit, push
git add <fixed_files>
git commit -m "fix: resolve CI failure"
git push
```

### Merge

```bash
gh pr merge --squash --delete-branch          # merge + cleanup
gh pr merge --auto --squash --delete-branch   # auto-merge when CI passes

# curl
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR/merge \
  -d '{"merge_method":"squash"}'
git push origin --delete $BRANCH
```

---

## 5. Code Review

### Local Changes (Pre-Push)

```bash
# Get scope
git diff main...HEAD --stat
git diff main...HEAD

# Check for common issues
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|debugger"
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*="
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

### Review a PR on GitHub

```bash
# View details
gh pr view 123
gh pr diff 123

# Check out locally
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Review against base
git diff main...pr-123

# Post comments
gh pr comment 123 --body "Overall looks good."
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."

# Inline comments via API
gh api repos/$OWNER/$REPO/pulls/123/comments --method POST \
  -f body="Use parameterized queries." \
  -f path="src/auth.py" -f line=45 -f side="RIGHT"
```

### Review Checklist

- **Correctness**: Edge cases, error paths, null/empty handling
- **Security**: Hardcoded secrets, SQL injection, XSS, path traversal, auth bypass
- **Quality**: Clear naming, DRY, single responsibility, no unnecessary complexity
- **Testing**: New paths covered? Happy + error cases?
- **Performance**: N+1 queries, unnecessary computation, blocking in async
- **Documentation**: Public APIs documented, non-obvious logic explained

### Review Output Format

Present as: **Critical** (blocking), **Warnings** (should fix), **Suggestions** (nice to have), **Looks Good**.

---

## 6. Issue Management

```bash
# List
gh issue list
gh issue list --state open --label "bug"
gh issue list --assignee @me
gh issue list --search "auth error" --state all

# View
gh issue view 42

# Create
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body "## Description\\nSteps to reproduce..." \
  --label "bug,backend" \
  --assignee "username"

# Triage
gh issue edit 42 --add-label "priority:high,bug"
gh issue edit 42 --add-assignee @me
gh issue comment 42 --body "Investigated — root cause in auth middleware."
gh issue close 42
gh issue reopen 42

# Link to PR — use keywords in PR body:
# Closes #42, Fixes #42, Resolves #42
```

### Bug Report Template
```
## Bug Description
## Steps to Reproduce
## Expected Behavior
## Actual Behavior
## Environment
```

### Feature Request Template
```
## Feature Description
## Motivation
## Proposed Solution
## Alternatives Considered
```

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Token in git history | Never push `.env` files; add `*.env` to `.gitignore`. Use `gh secret set` for CI tokens. |
| Force-push on shared branches | Prefer `git revert` over `git push --force`. If force is needed, rebase only on your own feature branch. |
| Merge conflicts from stale forks | Sync upstream (`git fetch upstream && git merge upstream/main`) before pushing PR changes. |
| Detached HEAD after rebase | Use `git push --force-with-lease` instead of `--force` — it refuses if your remote ref is out of date. |
| Missed CI failure | Run `gh pr checks --watch` before requesting review. Don't rely on email notifications alone. |
| Oversized PRs | Keep PRs under 400 lines. Split large features into stacked PRs against a feature branch. |
| `trust this machine` on shared hosts | Use `GIT_TERMINAL_PROMPT=0` and `gh auth login --with-token` instead of interactive auth. |
| Stale issue auto-close | Add `close` keywords to PR body. Don't close issues manually — let the merge do it. |

## Verification Checklist

- [ ] `gh auth status` succeeds before any workflow step
- [ ] Token scopes include at least `repo` and `workflow`
- [ ] Remote URL points to the correct owner/repo
- [ ] Branch name follows convention (`feat/`, `fix/`, `chore/`, `docs/`)
- [ ] PR title uses conventional commit format
- [ ] `gh pr diff` contains only intended changes (no debug logs, no merge artifacts)
- [ ] CI passes before requesting review
- [ ] PR contains an issue link (Fixes/Closes/Relates to #N)
- [ ] No hardcoded secrets in diff (grep for `password`, `secret`, `api_key`, `token`)
- [ ] Branch deleted after merge

### Quick Reference

| Action | gh | curl endpoint |
|--------|-----|--------------|
| List issues | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| View issue | `gh issue view N` | `GET /repos/{o}/{r}/issues/N` |
| Create | `gh issue create ...` | `POST /repos/{o}/{r}/issues` |
| Add labels | `gh issue edit N --add-label ...` | `POST /repos/{o}/{r}/issues/N/labels` |
| Assign | `gh issue edit N --add-assignee ...` | `POST /repos/{o}/{r}/issues/N/assignees` |
| Comment | `gh issue comment N --body ...` | `POST /repos/{o}/{r}/issues/N/comments` |
| Close | `gh issue close N` | `PATCH /repos/{o}/{r}/issues/N` |
| Search | `gh issue list --search "..."` | `GET /search/issues?q=...` |

## References

- `references/secrets-curl.md` — Encrypting secrets via API (curl + NaCl)
- `templates/bug-report.md` — Bug report template
- `templates/feature-request.md` — Feature request template
- `templates/pr-body-bugfix.md` — PR body template for bug fixes
- `templates/pr-body-feature.md` — PR body template for features
- `scripts/gh-env.sh` — Auth detection script

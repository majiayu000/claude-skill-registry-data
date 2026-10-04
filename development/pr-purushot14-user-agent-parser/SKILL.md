---
name: pr
description: Create or update a pull request from current branch to origin main with auto-generated title and description
argument-hint: "[base-branch]"
---

# /pr - Smart Pull Request Creator & Updater

## Usage

```
/pr              # Create or update PR to origin/main (default)
/pr develop      # Create or update PR to specified base branch
```

## Workflow

### Step 1: Check for Uncommitted Changes
```bash
git status
```

**If there are uncommitted changes:**
- Invoke the `/commit` skill first to commit all pending changes
- Wait for commit to complete before proceeding

### Step 2: Detect Remote and Branch Info
```bash
# This is a direct repo (not a fork) — remote is always origin
git remote -v
BRANCH=$(git branch --show-current)
BASE_BRANCH=${1:-main}  # Default base is main

# Get repo from origin
REPO=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/.*github.com[:/]\(.*\)/\1/')

# Fetch latest
git fetch origin
```

### Step 3: Check if PR Already Exists
```bash
# Check for existing PR from current branch
gh pr list --repo $REPO --head $BRANCH --json number,url,title,body
```

**If PR exists:** Go to **UPDATE MODE** (Step 4a)
**If no PR:** Go to **CREATE MODE** (Step 4b)

---

## UPDATE MODE (PR Already Exists)

### Step 4a: Push New Commits
```bash
git push origin $BRANCH
```

### Step 5a: Analyze New Commits Since PR Creation
```bash
gh pr view $PR_NUMBER --repo $REPO --json commits
git log origin/$BASE_BRANCH..HEAD --oneline
```

### Step 6a: Update PR Description
Update the PR body to:
1. Add new changes to Summary section
2. Mark completed TODOs with `[x]`
3. Add any new test plan items

```bash
gh pr edit $PR_NUMBER --repo $REPO --body "$(cat <<'EOF'
<updated-description>
EOF
)"
```

### Step 7a: Report Update
```
✅ PR #123 updated successfully!

**URL:** https://github.com/owner/user-agent-parser/pull/123
**New commits pushed:** 2
**Description updated:** Yes
```

### Step 8a: Review Updated PR
Invoke the `/pr-review` skill on the PR number.

---

## CREATE MODE (No Existing PR)

### Step 4b: Push Current Branch to Origin
```bash
git push -u origin $BRANCH
```

### Step 5b: Analyze Commits for PR Content
- Review all commits between `origin/main` and HEAD
- Group changes by type (feat, fix, refactor, etc.)
- Identify the **primary/dominant** change type for PR title
- Extract key changes for summary bullets

### Step 6b: Generate PR Title
Format: `<emoji> <type>(<scope>): <subject>` (max 70 chars)

**Same format as commit messages.** If multiple types, use the dominant one. If equal, prioritize: fix > feat > refactor > test > docs > style.

### Step 7b: Generate PR Description

```bash
gh pr create --repo $REPO --base $BASE_BRANCH --head $BRANCH \
  --title "<emoji> <type>(<scope>): <subject>" \
  --body "$(cat <<'EOF'
## Summary
- <emoji> <change 1>
- <emoji> <change 2>
- <emoji> <change 3>

## Changes

### <Category 1>
- **Component**: Description of change

## Testing
- [ ] `poetry run pytest` — all tests pass
- [ ] `poetry run pytest -q --cov=user_agent_parser --cov-report=xml` — coverage not decreased
- [ ] `poetry run ruff check && poetry run ruff format --check` — no lint issues

## Compatibility
- [ ] Python 3.8+ syntax only (no match/case, no X|Y unions)
- [ ] `parse()` returns 7-tuple — backward compatible
- [ ] Public API signatures unchanged (or documented as breaking)
- [ ] `@lru_cache` functions return immutable types
- [ ] CI matrix passes (Python 3.8–3.15)

## Test plan
- [ ] Test item 1
- [ ] Test item 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 8b: Review the Created PR
Invoke the `/pr-review` skill on the new PR number.

---

## Type Reference (same as commits)

| Type | Emoji | Use Case |
|------|-------|----------|
| feat | ✨ | New feature |
| fix | 🐛 | Bug fix |
| docs | 📝 | Documentation |
| style | 💄 | Formatting only |
| refactor | ♻️ | Code restructure |
| perf | ⚡ | Performance |
| test | ✅ | Tests |
| build | 📦 | Dependencies |
| ci | 🌐 | CI/CD |
| chore | 🔧 | Maintenance/mixed changes |
| revert | ⏪ | Revert commit |
| remove | 🔥 | Remove code/files |

## Scope Priority (same as commits)

| Priority | Scope | File Paths |
|----------|-------|------------|
| 1 | parser | `user_agent_parser/parser.py` |
| 2 | engine | `user_agent_parser/advanced_engine.py` |
| 3 | analytics | `user_agent_parser/analytics.py` |
| 4 | devices | `user_agent_parser/modern_devices.py`, constants device entries |
| 5 | constants | `user_agent_parser/constants.py` |
| 6 | api | `user_agent_parser/__init__.py` |
| 7 | tests | `tests/*` |
| 8 | ci | `.github/workflows/*` |
| 9 | deps | `pyproject.toml`, `poetry.lock` |

## Rules

| Rule | Details |
|------|---------|
| Uncommitted Changes | Run `/commit` skill first |
| Existing PR | Detect and switch to UPDATE mode |
| Remote | Always `origin` (direct repo, not a fork) |
| Base Branch | Default `main` |
| Push | Push to origin before creating/updating PR |
| Title Format | `<emoji> <type>(<scope>): <subject>` |
| Title Length | Max 70 chars |
| TODO Updates | Mark completed items with `[x]` in update mode |
| Review | Invoke `/pr-review` skill after create/update |

## Error Handling

| Error | Action |
|-------|--------|
| Uncommitted changes | Run `/commit` skill first |
| On main branch | Ask user to create a feature branch first |
| No commits ahead of origin/main | Report "Nothing to create PR for" |
| Push fails | Report error and stop |
| gh CLI not authenticated | Run `gh auth login` |

## Output to User

**CREATE MODE:**
```
✅ PR created successfully!

**Title:** ✨ feat(parser): add Brave browser detection
**URL:** https://github.com/owner/user-agent-parser/pull/42
**Base:** origin/main
**Head:** feature-branch
**Commits:** 3 commits
**Files changed:** 4 files

Running /pr-review to check PR...
```

**UPDATE MODE:**
```
✅ PR #42 updated successfully!

**URL:** https://github.com/owner/user-agent-parser/pull/42
**New commits pushed:** 2
**Description updated:** Yes

Updates made:
- ✨ Added: "Add parametrized test cases for Brave"
- ✅ Completed: "poetry run pytest passes"

Running /pr-review to check PR...
```

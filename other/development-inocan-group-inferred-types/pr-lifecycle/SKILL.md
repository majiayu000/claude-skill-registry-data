---
name: pr-lifecycle
description: Enforce project hygiene throughout the PR lifecycle. Use before creating PRs to validate worktrees, branch naming, and issue linking. Use when creating PRs to ensure proper "Fixes #XYZ" keywords, conventional commit titles, and complete PR bodies. Use after PR merge for cleanup guidance and issue closure verification.
---

# PR Lifecycle Management

Enforce project hygiene throughout the pull request lifecycle. This skill provides checklists, validation commands, and templates to ensure PRs properly close issues and follow project conventions.

## Critical Constraints - Session Statelessness

**IMPORTANT:** You are operating in a stateless session. Each Claude Code session is isolated.

**You CANNOT:**
- Track issues across sessions
- Remember to do something later
- Follow up on tasks in the future
- Promise to handle something "in a follow-up"

**You MUST NOT say things like:**
- "I'll track this in a follow-up issue"
- "I'll remember to fix this later"
- "I'll handle this in a subsequent PR"

## PR Comment Response Decision Framework

When addressing review comments, choose ONE of these options:

### Option 1: Implement Now (Preferred)
**When:** Change is small-ish and worth doing.
**Action:** Implement fix, commit, reply with: "Fixed in commit {sha}: {description}"

### Option 2: Defer with Issue (Expensive - use sparingly)
**When:** Change is large AND worth doing AND not critical to PR.
**Action:**
1. Create GitHub issue NOW using `gh issue create`
2. Add to same milestone as PR's issue
3. Add as sub-issue using `gh sub-issue add`
4. Reply: "Created #XYZ to track this. Not addressing in this PR because {reason}."

### Option 3: Disagree / Won't Fix
**When:** Suggestion is nitpicky, negligible, or you disagree.
**Action:** Reply explaining why not addressing. Be professional.
**NEVER use for:** Test failures, errors, security concerns.

## Overview

**Project Hygiene Invariant:** Each PR should:
1. Close exactly one GitHub issue
2. Include "Fixes #XYZ" (or similar keyword) in PR body
3. Be created from a proper worktree using the `.claude/skills/git-worktrees` skill (you should not be in `/workspace`, which should always be kept up to date with origin main - instead you should be in `wip/<feature branch>`)
4. Follow branch naming convention: `m<milestone_id>-p<parent_issue_id>-i<issue_num>-<slug>` (with appropriate variations)
5. Use Conventional Emoji Commits for PR title

**Why This Matters:** PRs #221 and #222 didn't include "Fixes #XYZ" keywords, causing issues to remain open after merge. This skill prevents such "orphan PRs."

## Tmux Window Naming Convention

When working in a tmux session, window names reflect the current PR lifecycle phase for quick visual reference.

**Format:** `<emoji><prefix><number>`

**Prefix Conventions:**
- `i` = Issue number (e.g., `💻i483` = coding on issue #483)
- `pr` = Pull request number (e.g., `🔧pr485` = maintaining PR #485)

**Examples:**
- `💻i483` - Coding on issue #483
- `🚀i483` - Submitting PR for issue #483
- `🔧pr485` - Maintaining PR #485
- `⏳pr485` - Waiting for tests on PR #485

**Phase Emojis:**

| Phase | Emoji | When Used | Format Example | Command |
|-------|-------|-----------|----------------|---------|
| 1. Gathering information | 🔍 | Research/discovery | `🔍i483` | Manual |
| 2. Coding | 💻 | Active development | `💻i483` | `/gh-start-issue` |
| 3. Waiting for tests | ⏳ | CI/CD checks running | `⏳pr485` | `/pr-workflow` |
| 4. Waiting for user | ❓ | Needs input/clarification | `❓i483` or `❓pr485` | Manual |
| 5. Submitting PR | 🚀 | Creating/pushing PR | `🚀i483` | `/pr-workflow` |
| 6. PR maintenance | 🔧 | Addressing feedback/fixes | `🔧pr485` | `/pr-workflow` |
| 7. Cleanup | 🧹 | Post-merge cleanup | `🧹pr485` | Manual |

**Automatic Updates:**
- `/gh-start-issue` sets tmux to `💻i<issue_num>` (coding phase on issue)
- `/pr-workflow` updates tmux through phases:
  - `🚀i<issue_num>` → (PR created) → `🔧pr<pr_num>` → `⏳pr<pr_num>` → `🔧pr<pr_num>`
  - Note: Transitions from issue number to PR number after PR is created

**Manual Updates:**
```bash
# Update tmux window name manually for issue work
ISSUE_NUM=<your_issue_number>
tmux rename-window "🔍i${ISSUE_NUM}"  # Research phase on issue

# Update tmux window name manually for PR work
PR_NUM=<your_pr_number>
tmux rename-window "🔧pr${PR_NUM}"  # PR maintenance
```

**Why This Convention:**
- **Information density**: Maximizes useful info in limited tmux window title space (5-7 chars vs 50+)
- **Clear distinction**: Instantly know if you're working on issue or PR
- **Visual status**: Emoji provides at-a-glance phase indication
- **WCAG compliance**: Window title colors meet AAA accessibility standards (see `.devcontainer/.tmux.conf`)

## Phase 1: Before Creating PR

### Pre-PR Checklist

Run these validations before creating a PR:

```bash
# 1. Verify you're in a worktree (not main)
pwd | grep -q "wip/" && echo "In worktree" || echo "WARNING: Not in wip/ worktree"

# 2. Check branch name follows convention
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
# Should match: m<id>-p<id>-i<num>-<slug> or variants (p<id>-i<num>-<slug>, i<num>-<slug>)

# 3. Extract issue number from branch (look for i<num> pattern)
ISSUE_NUM=$(echo "$BRANCH" | grep -oP 'i\K[0-9]+' || echo "$BRANCH" | grep -oE '[0-9]+' | head -1)
echo "Issue number: $ISSUE_NUM"

# 4. Verify issue exists and is open
gh issue view "$ISSUE_NUM" --json state,title

# 5. Check commits for "Fixes #" keyword
git log origin/main..HEAD --oneline | grep -i "fixes #\|closes #\|resolves #" || echo "WARNING: No 'Fixes #' keyword found in commits"
```

### Validation Details

#### Worktree Verification

**Why:** Feature work should happen in worktrees, not the main worktree.

```bash
# List all worktrees
git worktree list

# Verify current directory is in wip/
pwd | grep -q "wip/" && echo "In worktree" || echo "WARNING: Not in wip/ worktree"
```

**Expected:** You should be in a `wip/<branch-name>/` directory.

#### Branch Naming Convention

**Format variations:**
- With milestone & parent: `m<milestone_id>-p<parent_id>-i<issue_num>-<issue_slug>`
- With parent only: `p<parent_id>-i<issue_num>-<issue_slug>`
- With milestone only: `m<milestone_id>-i<issue_num>-<issue_slug>`
- Standalone: `i<issue_num>-<issue_slug>`

**Examples:**
- `m8-p123-i234-add-authentication`
- `p123-i234-add-authentication`
- `i42-add-authentication`

**Validation:**
```bash
BRANCH=$(git branch --show-current)

# Check format: must contain i<number> pattern
if [[ "$BRANCH" =~ i[0-9]+ ]]; then
  echo "Branch name follows convention"
else
  echo "WARNING: Branch name '$BRANCH' doesn't follow convention (missing i<number>)"
fi
```

#### Issue Verification

**Check issue exists and is open:**
```bash
ISSUE_NUM=$(git branch --show-current | grep -oE '[0-9]+' | head -1)

# View issue details
gh issue view "$ISSUE_NUM" --json number,title,state,labels

# Verify it's open
STATE=$(gh issue view "$ISSUE_NUM" --json state -q '.state')
if [ "$STATE" = "OPEN" ]; then
  echo "Issue #$ISSUE_NUM is open"
else
  echo "WARNING: Issue #$ISSUE_NUM is $STATE"
fi
```

#### Commit Message Check

**Verify commits reference the issue:**
```bash
# Check for GitHub closing keywords in commits
git log origin/main..HEAD --pretty=format:"%s" | \
  grep -iE "(fix(es)?|close[sd]?|resolve[sd]?)\s*#\d+" || \
  echo "WARNING: No GitHub closing keywords found in commit messages"
```

**GitHub closing keywords:** `close`, `closes`, `closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`, `resolved`

## Phase 2: Creating PR

### PR Title Convention

**Format:** `<emoji> <type>[scope]: <description>`

**Common Types:**
| Type | Emoji | Use For |
|------|-------|---------|
| feat | ✨ | New features |
| fix | 🩹 | Bug fixes |
| docs | 📚 | Documentation |
| refactor | ♻️ | Code refactoring |
| test | 🧪 | Tests |
| build | 🔧 | Build system |
| perf | ⚡️ | Performance |
| release | 🔖 | Releases |

**Examples:**
- `✨ feat(cli): add deployment management commands`
- `🩹 fix: resolve race condition in thread handler`
- `📚 docs: add PR lifecycle skill`

### PR Body Template

**Always include "Fixes #XYZ" to auto-close the issue:**

```markdown
## Summary
<1-3 bullet points describing the changes>

## Changes
- <specific change 1>
- <specific change 2>

## Related Issues
Fixes #<issue_number>

## Test Plan
- [ ] <test item 1>
- [ ] <test item 2>

---
Generated with [Claude Code](https://claude.com/claude-code)
```

### Adding PR to Milestone

If the issue that the PR fixes is part of a milestone, add the PR to that milestone.

### Create PR Command

**Using gh CLI with proper body:**
```bash
ISSUE_NUM=$(git branch --show-current | grep -oE '[0-9]+' | head -1)

gh pr create \
  --title "✨ feat: <description>" \
  --body "$(cat <<EOF
## Summary
- <summary point>

## Changes
- <change 1>
- <change 2>

## Related Issues
Fixes #$ISSUE_NUM

## Test Plan
- [ ] <test item>

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Verify PR Will Close Issue

**After creating PR, verify the link:**
```bash
# Get PR number
PR_NUM=$(gh pr view --json number -q '.number')

# Check closing issues
gh pr view "$PR_NUM" --json closingIssuesReferences -q '.closingIssuesReferences[].number'

# Should output the issue number
```

## Phase 3: After PR Creation

### Monitor for Automated Reviews

Copilot and other automated reviewers may add comments. Monitor and address them:

```bash
PR_NUM=$(gh pr view --json number -q '.number')

# Get owner/repo dynamically from current repository
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Check for Copilot comments (use --paginate to get ALL comments)
gh api repos/$REPO/pulls/$PR_NUM/comments --paginate \
  --jq '.[] | select(.user.login == "copilot") | {id, body, path, line}'

# Check for all review comments (use --paginate to get ALL comments)
gh api repos/$REPO/pulls/$PR_NUM/comments --paginate \
  --jq '.[] | {id, user: .user.login, body: .body[0:100]}'
```

### Reply to Review Comments

**After addressing feedback, reply with commit reference:**

**Note:** Do not at-mention copilot in your reply, otherwise copilot will try to implement something.

```bash
PR_NUM=$(gh pr view --json number -q '.number')
COMMENT_ID=<comment_id>
COMMIT_SHA=$(git rev-parse --short HEAD)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

gh api repos/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies \
  -f body="Fixed in commit $COMMIT_SHA: <brief description>"
```

### Check PR Status

```bash
PR_NUM=$(gh pr view --json number -q '.number')

# View PR checks
gh pr checks "$PR_NUM"

# View PR status
gh pr view "$PR_NUM" --json state,mergeable,reviewDecision
```

## Phase 4: After PR Merge

### Verify Issue Closure

**Check if the issue was auto-closed:**
```bash
ISSUE_NUM=<issue_number>

# Check issue state
STATE=$(gh issue view "$ISSUE_NUM" --json state -q '.state')
echo "Issue #$ISSUE_NUM state: $STATE"

if [ "$STATE" = "CLOSED" ]; then
  echo "Issue #$ISSUE_NUM was auto-closed"
else
  echo "WARNING: Issue #$ISSUE_NUM is still OPEN"
  echo "Manually close with: gh issue close $ISSUE_NUM"
fi
```

### Manual Issue Closure (If Needed)

**If the issue wasn't auto-closed:**

Ask the user first before doing this:
```bash
ISSUE_NUM=<issue_number>
PR_NUM=<pr_number>

# Close with reference to PR
gh issue close "$ISSUE_NUM" --comment "Closed via PR #$PR_NUM"
```

### Cleanup: Remove Worktree

**After PR merge, clean up the worktree:**
```bash
# Switch to main worktree first
cd /workspace

# Remove the worktree
WORKTREE_PATH="wip/<branch-name>"  # e.g., wip/i42-add-auth or wip/m8-p123-i234-add-auth
git worktree remove "$WORKTREE_PATH"

# Prune stale references
git worktree prune --verbose
```

### Cleanup: Delete Branch

**Delete local and remote branches:**
```bash
BRANCH="<branch_name>"  # e.g., i42-add-auth or m8-p123-i234-add-auth

# Delete local branch
git branch -d "$BRANCH"

# If not fully merged, force delete
# git branch -D "$BRANCH"

# Delete remote branch (GitHub usually does this automatically)
git push origin --delete "$BRANCH" 2>/dev/null || echo "Remote branch already deleted"
```

### Cleanup: Ensure /workspace is up to date

* `/workspace` should be kept up to date with origin main
* after merging, `cd /workspace` then ensure workspace is refreshed from origin main
  * in the unlikely case that another agent has put WIP in `/workspace` (instead of `wip/<feature branch>`) that would be affected by this action, ask user what to do 

### Complete Cleanup Workflow

```bash
# Variables
ISSUE_NUM=225
BRANCH="claude/225-pr-lifecycle-skill"
WORKTREE_PATH="wip/claude-225-pr-lifecycle-skill"

# 1. Verify issue closed
gh issue view "$ISSUE_NUM" --json state -q '.state'

# 2. Switch to main worktree
cd /workspace

# 3. Pull latest changes
git checkout main
git pull origin main

# 4. Remove worktree
git worktree remove "$WORKTREE_PATH"

# 5. Delete local branch
git branch -d "$BRANCH"

# 6. Prune
git worktree prune --verbose

# 7. Verify cleanup - should only show main worktree
git worktree list

# Show only non-main branches (should be empty after cleanup)
git branch | grep -v "^\*" | grep -v "main\|master"
```

## Quick Reference

### Pre-PR Checklist

| Check | Command | Expected |
|-------|---------|----------|
| In worktree | `pwd` &#124; `grep wip/` | In wip/ directory |
| Branch format | `git branch --show-current` | `user/num-slug` |
| Issue open | `gh issue view N --json state` | `OPEN` |
| Has "Fixes #" | `git log` &#124; `grep -i "fixes #"` | Found keyword |

### GitHub Closing Keywords

Any of these in PR body will auto-close the linked issue:
- `close`, `closes`, `closed`
- `fix`, `fixes`, `fixed`
- `resolve`, `resolves`, `resolved`

**Format:** `Fixes #123` or `Fixes owner/repo#123`

### PR Title Emojis

| Emoji | Type | Triggers |
|-------|------|----------|
| ✨ | feat | MINOR bump |
| 🩹 | fix | PATCH bump |
| 🚨 | BREAKING | MAJOR bump |
| 📚 | docs | No bump |
| ♻️ | refactor | No bump |
| 🧪 | test | No bump |
| 🔧 | build | No bump |
| 🔖 | release | N/A |

### Common API Commands

```bash
# Get owner/repo for API calls
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# View issue
gh issue view <num> --json number,title,state

# View PR
gh pr view --json number,title,state,closingIssuesReferences

# PR comments (for reviews) - use --paginate to get ALL comments
gh api repos/$REPO/pulls/<num>/comments --paginate

# Reply to comment
gh api repos/$REPO/pulls/<num>/comments/<id>/replies -f body="message"

# Close issue manually
gh issue close <num> --comment "Closed via PR #N"
```

## Integration with Other Skills

### With `git-worktrees` Skill

Use git-worktrees skill to create proper worktrees before starting work:
```bash
# Create worktree for new issue
git worktree add -b alice/42-new-feature wip/alice-42-new-feature main
```

### With `gh-sub-issue` Skill

For issues with parent-child relationships, verify PR targets:
```bash
# Check if issue has parent
gh sub-issue list 42 --relation parent

# If parent exists, PR should target parent branch, not main
```

## Troubleshooting

### "Issue not closed after merge"

**Cause:** Missing "Fixes #N" keyword in PR body.

**Solution:**
```bash
# Close manually
gh issue close <num> --comment "Closed via PR #<pr_num>"

# Prevent future issues: always include "Fixes #N" in PR body
```

### "Branch name doesn't match issue"

**Cause:** Branch created without following convention.

**Solution:** Rename branch before PR:
```bash
git branch -m old-name i42-proper-name
git push origin -u i42-proper-name
git push origin --delete old-name
```

### "Can't determine issue number"

**Cause:** Branch name doesn't contain issue number.

**Solution:** Check branch name, rename if needed:
```bash
git branch --show-current
# If no number, rename branch to include issue number
```

### "PR shows wrong closing issues"

**Cause:** Wrong issue number in PR body.

**Solution:** Edit PR body on GitHub or:
```bash
gh pr edit <num> --body "$(cat updated-body.md)"
```

## See Also

- **git-worktrees skill** - Create and manage worktrees for issue branches
- **gh-sub-issue skill** - Manage parent-child issue relationships
- **GitHub Workflow Documentation** - `@docs/dev/github-workflow.md`
- **Git SCM Conventions** - `@docs/dev/git-scm-conventions.md`
- **GitHub Keywords Docs** - https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue

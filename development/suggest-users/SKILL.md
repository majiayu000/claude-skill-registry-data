---
name: suggest-users
description: Suggests reviewers for PRs and assignees for issues by ranking users based on CODEOWNERS match, file expertise, recent activity, and workload balancing. Use when creating PRs to suggest reviewers, creating issues to suggest assignees, or re-requesting review after addressing comments.
allowed-tools: Bash, Read
context: fork
agent: Explore
---

# Suggest Users

This skill provides intelligent user suggestions for PRs (reviewers) and issues (assignees) based on GitHub repository data, file ownership, and activity patterns.

## Purpose

Instead of manually picking reviewers or assignees, this skill analyzes:
- CODEOWNERS file for explicit ownership
- Recent PR activity for active contributors
- File-specific commit history for expertise
- Current review load to balance workload

## Configuration

Read activity lookback settings (local > project > user > defaults):
```bash
LOOKBACK_DAYS=$(jq -r '.review.activityLookbackDays // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$LOOKBACK_DAYS" ] && LOOKBACK_DAYS=$(jq -r '.review.activityLookbackDays // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$LOOKBACK_DAYS" ] && LOOKBACK_DAYS=$(jq -r '.review.activityLookbackDays // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$LOOKBACK_DAYS" ] && LOOKBACK_DAYS="30"

FALLBACK_DAYS=$(jq -r '.review.activityFallbackDays // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$FALLBACK_DAYS" ] && FALLBACK_DAYS=$(jq -r '.review.activityFallbackDays // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$FALLBACK_DAYS" ] && FALLBACK_DAYS=$(jq -r '.review.activityFallbackDays // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$FALLBACK_DAYS" ] && FALLBACK_DAYS="90"
```

## Quick Reference

### Get Suggested Reviewers for a PR

```bash
# 1. Get repository info
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# 2. Get changed files in PR
CHANGED_FILES=$(gh pr view {PR_NUMBER} --json files --jq '.files[].path')

# 3. Check CODEOWNERS matches
gh api repos/$REPO/contents/.github/CODEOWNERS --jq '.content' | base64 -d 2>/dev/null

# 4. Get collaborators with push access
gh api repos/$REPO/collaborators --jq '.[] | select(.permissions.push) | .login'

# 5. Get recent PR authors/reviewers
gh pr list --state merged --limit 20 --json author,reviews --jq '.[].author.login, .[].reviews[].author.login' | sort | uniq -c | sort -rn

# 6. Get file-specific contributors (last 30 days)
git log --format='%an' --since="$LOOKBACK_DAYS days ago" -- {changed_files} | sort | uniq -c | sort -rn
```

### Get Suggested Assignees for an Issue

```bash
# 1. Get repository info
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# 2. Get collaborators
gh api repos/$REPO/collaborators --jq '.[] | select(.permissions.push) | .login'

# 3. Get recent issue assignees by label
gh issue list --state closed --limit 20 --label "{label}" --json assignees --jq '.[].assignees[].login' | sort | uniq -c | sort -rn

# 4. Get team members if applicable
gh api repos/$REPO/teams --jq '.[].slug' 2>/dev/null
```

## Scoring Algorithm

### For Reviewers (PR Context)

| Signal | Points | Rationale |
|--------|--------|-----------|
| CODEOWNERS match | +50 | Explicit ownership declaration |
| Commits to changed files (last LOOKBACK_DAYS) | +10 per match | File-level expertise |
| Recent PR reviews | +5 per review (max 25) | Active reviewer |
| Recent PR authorship | +3 per PR (max 15) | Active contributor |
| Same team membership | +10 | Team context |
| Open review load | -3 per open review | Workload balancing |
| Is PR author | -100 | Cannot self-review |

### For Assignees (Issue Context)

| Signal | Points | Rationale |
|--------|--------|-----------|
| Recent issues with same label | +10 per issue | Domain expertise |
| Recent commits to related files | +5 per commit | Code familiarity |
| Current open issue count | -2 per issue | Workload balancing |
| Explicit @mention in issue | +20 | Stakeholder indication |

## Usage Workflow

### Step 1: Gather Data (Parallel)

Execute these commands in parallel to collect all signals:

```bash
# Repository info
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# Collaborators
gh api repos/$REPO/collaborators --jq '.[] | select(.permissions.push) | {login: .login, admin: .permissions.admin}'

# CODEOWNERS (may not exist)
gh api repos/$REPO/contents/.github/CODEOWNERS --jq '.content' 2>/dev/null | base64 -d

# Alternative CODEOWNERS location
gh api repos/$REPO/contents/CODEOWNERS --jq '.content' 2>/dev/null | base64 -d

# Recent merged PRs with authors and reviewers
gh pr list --state merged --limit 30 --json number,author,reviews,mergedAt --jq '.[] | {author: .author.login, reviewers: [.reviews[].author.login]}'

# Open PRs with pending reviews (for workload)
gh pr list --state open --json number,reviews --jq '.[] | {number, pending_reviewers: [.reviews[] | select(.state == "PENDING") | .author.login]}'
```

### Step 2: Match CODEOWNERS

Parse CODEOWNERS file and match against changed files:

```
# CODEOWNERS format examples:
# * @default-owner
# /src/api/ @api-team
# *.ts @typescript-owners

# Match rules:
# 1. More specific paths take precedence
# 2. Multiple owners can be specified per pattern
# 3. Teams use @org/team-name format
```

### Step 3: Calculate Scores

For each potential reviewer/assignee:

```markdown
## Scoring: {username}

| Signal | Value | Points |
|--------|-------|--------|
| CODEOWNERS match | Yes/No | +50/0 |
| File commits (LOOKBACK_DAYS d) | {N} files | +{N*10} |
| Recent reviews | {M} PRs | +{min(M*5, 25)} |
| Open reviews | {K} PRs | -{K*3} |
| **Total** | | **{sum}** |
```

### Step 4: Present Suggestions

Use the **AskUserQuestion tool** with ranked options:

```markdown
## Suggested Reviewers

Based on file ownership, recent activity, and current workload:

| Rank | User | Score | Reasons |
|------|------|-------|---------|
| 1 | @alice | 75 | CODEOWNERS (+50), 2 file commits (+20), low workload (+5) |
| 2 | @bob | 45 | 4 recent reviews (+20), 2 file commits (+20), 1 open review (-3) |
| 3 | @carol | 30 | 3 file commits (+30), no ownership |
```

Then invoke AskUserQuestion:
- **Option 1**: "@alice (Recommended)" - Top ranked reviewer
- **Option 2**: "@bob" - Active reviewer
- **Option 3**: "@carol" - File expertise
- **Option 4**: "Someone else" - Manual selection

## Integration Points

### In gh-pr Command

```markdown
## Phase 4: Reviewer Suggestion

1. Invoke suggest-users skill
2. Get changed files from staged commits
3. Calculate scores for all collaborators
4. Present top 3-4 suggestions with AskUserQuestion
5. Add selected reviewers to PR creation command
```

### In gh-address Command

```markdown
## Reviewer Re-engagement

1. Fetch previous reviewers from PR
2. Score based on: previous review (+30), comment count (+5 per)
3. Suggest re-requesting review from engaged reviewers
```

### In gh-review Command

```markdown
## Alternative Reviewer Suggestion

If current reviewer wants to defer:
1. Calculate scores excluding current reviewer
2. Suggest alternatives with expertise in PR's changed files
```

### In gh-issue Command

```markdown
## Assignee Suggestion

1. Parse issue labels and title
2. Find users with history on similar issues
3. Present suggestions with AskUserQuestion
```

## CODEOWNERS Parsing

### Pattern Matching Rules

```bash
# Pattern precedence (later = higher priority)
*                    # Default owners for everything
*.js                 # All JavaScript files
/docs/               # /docs/ directory at root
docs/                # docs/ directory anywhere
/src/api/**/*.ts     # TypeScript files in src/api/

# Multiple owners
/src/core/ @alice @bob @org/core-team

# Escaping special characters
/path/with\ space/   # Space in path
```

### Team Resolution

When CODEOWNERS specifies a team (`@org/team-name`):

```bash
# Resolve team members
gh api orgs/{org}/teams/{team-name}/members --jq '.[].login'
```

## Workload Balancing

To prevent overloading active reviewers:

```bash
# Count open reviews per user
gh pr list --state open --json reviews --jq '
  [.[].reviews[] | select(.state == "PENDING" or .state == "COMMENTED") | .author.login]
  | group_by(.)
  | map({user: .[0], count: length})
  | sort_by(-.count)
'
```

Apply penalty: `-3 points per open review`

## Edge Cases

### No CODEOWNERS File

Fall back to:
1. Recent file contributors
2. Recent PR reviewers
3. All collaborators (alphabetical)

### No Recent Activity

If no commits or PRs in last LOOKBACK_DAYS (default: 30):
1. Extend window to FALLBACK_DAYS (default: 90)
2. Fall back to all collaborators

### Private Repository / API Limits

If API calls fail:
1. Use git log for local contributor data
2. Present collaborator list from gh api
3. Allow manual input

### Single Contributor Repository

Skip suggestion and note:
```markdown
**Note**: Single contributor detected. Self-review checklist recommended instead of external reviewer.
```

## Output Format

When invoked by other commands, return structured data:

```markdown
## User Suggestions

**Context**: {PR/Issue} #{number}
**Changed Files**: {count} files
**CODEOWNERS Matches**: {yes/no}

### Ranked Suggestions

1. **@{user1}** (Score: {N})
   - {reason1}
   - {reason2}

2. **@{user2}** (Score: {M})
   - {reason1}

3. **@{user3}** (Score: {K})
   - {reason1}

### Recommendation

Based on scoring, **@{user1}** is the recommended {reviewer/assignee} because:
- {primary reason}
- {secondary reason}
```

## Best Practices

1. **Always check CODEOWNERS first** - Explicit ownership trumps heuristics
2. **Balance workload** - Don't always suggest the most active reviewer
3. **Show reasoning** - Users should understand why suggestions were made
4. **Allow override** - Always provide "Someone else" option
5. **Cache results** - Don't re-fetch data within same session
6. **Handle failures gracefully** - API errors shouldn't block workflow

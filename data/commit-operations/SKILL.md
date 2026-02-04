---
name: commit-operations
description: View and analyze commits in GitHub repositories - commit history, diffs, and commit details using gh CLI
---

# GitHub Commit Operations Skill

This skill provides operations for viewing and analyzing commits in GitHub repositories, including commit history, diffs, and commit details.

## Available Operations

### 1. List Commits
View commit history for a repository or specific branch.

### 2. View Commit Details
Get detailed information about a specific commit.

### 3. Compare Commits
Compare differences between commits, branches, or tags.

### 4. Search Commits
Search for commits by message, author, or other criteria.

## Usage Examples

### List Commits

**List recent commits in repository:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | {sha: .sha[0:7], message: .commit.message, author: .commit.author.name, date: .commit.author.date}'
```

**List commits with gh CLI:**
```bash
cd repo-name
git log --oneline -20
```

**List commits for specific branch:**
```bash
gh api repos/owner/repo-name/commits?sha=branch-name --jq '.[] | "\(.sha[0:7]) \(.commit.message)"'
```

**List commits with author:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | "\(.commit.author.name): \(.commit.message)"'
```

**List commits in date range:**
```bash
gh api "repos/owner/repo-name/commits?since=2025-01-01T00:00:00Z&until=2025-12-31T23:59:59Z" --jq '.[] | "\(.commit.author.date) \(.commit.message)"'
```

**List commits with pagination:**
```bash
# First page (default 30 items)
gh api repos/owner/repo-name/commits

# Specific page
gh api repos/owner/repo-name/commits?page=2&per_page=50
```

**Filter by author:**
```bash
gh api repos/owner/repo-name/commits?author=username --jq '.[] | "\(.sha[0:7]) \(.commit.message)"'
```

**Filter by path:**
```bash
gh api repos/owner/repo-name/commits?path=src/main.js --jq '.[] | "\(.sha[0:7]) \(.commit.message)"'
```

### View Commit Details

**View specific commit:**
```bash
gh api repos/owner/repo-name/commits/abc123def --jq '{
  sha: .sha,
  message: .commit.message,
  author: .commit.author.name,
  date: .commit.author.date,
  stats: .stats,
  files: [.files[].filename]
}'
```

**View commit in terminal (if repo is cloned):**
```bash
cd repo-name
git show abc123def
```

**View commit files changed:**
```bash
gh api repos/owner/repo-name/commits/abc123def --jq '.files[] | {filename, status, additions, deletions, patch}'
```

**View commit stats:**
```bash
gh api repos/owner/repo-name/commits/abc123def --jq '.stats'
# Returns: { additions, deletions, total }
```

**View commit parents:**
```bash
gh api repos/owner/repo-name/commits/abc123def --jq '.parents[] | .sha'
```

**View commit signature:**
```bash
gh api repos/owner/repo-name/commits/abc123def --jq '.commit.verification'
```

### Compare Commits

**Compare two commits:**
```bash
gh api repos/owner/repo-name/compare/abc123...def456 --jq '{
  ahead_by: .ahead_by,
  behind_by: .behind_by,
  total_commits: .total_commits,
  files_changed: [.files[].filename]
}'
```

**Compare branches:**
```bash
gh api repos/owner/repo-name/compare/main...feature-branch --jq '.commits[] | "\(.commit.message)"'
```

**Compare with base:**
```bash
gh api repos/owner/repo-name/compare/main...HEAD --jq '{
  status: .status,
  ahead_by: .ahead_by,
  behind_by: .behind_by,
  commits: [.commits[].sha[0:7]]
}'
```

**View diff between commits:**
```bash
cd repo-name
git diff abc123..def456
```

**View diff for specific file:**
```bash
cd repo-name
git diff abc123..def456 -- src/main.js
```

**Compare tags:**
```bash
gh api repos/owner/repo-name/compare/v1.0.0...v2.0.0 --jq '.commits | length'
```

### Search Commits

**Search by commit message:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | select(.commit.message | contains("fix bug"))'
```

**Search by author:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | select(.commit.author.name == "John Doe")'
```

**Search by date:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | select(.commit.author.date > "2025-01-01")'
```

**Using git log search (in cloned repo):**
```bash
cd repo-name

# Search by message
git log --grep="bug fix"

# Search by author
git log --author="John Doe"

# Search by date
git log --since="2025-01-01" --until="2025-12-31"

# Search by file
git log -- src/main.js

# Search by code content
git log -S"function name"

# Combine filters
git log --author="John" --grep="feature" --since="2025-01-01"
```

## Common Patterns

### View Recent History

```bash
# Clone and view history
gh repo clone owner/repo-name
cd repo-name

# View last 10 commits
git log --oneline -10

# View with details
git log -5 --pretty=fuller

# View with stats
git log -5 --stat

# View graphical history
git log --graph --oneline --all -20
```

### Analyze Specific Commit

```bash
# Get commit SHA from list
gh api repos/owner/repo-name/commits --jq '.[0].sha'

# View full details
gh api repos/owner/repo-name/commits/<sha>

# View what changed
gh api repos/owner/repo-name/commits/<sha> --jq '.files[] | "\(.status): \(.filename) (+\(.additions) -\(.deletions))"'

# View commit locally
cd repo-name
git show <sha>
```

### Track File History

```bash
# Via API
gh api repos/owner/repo-name/commits?path=src/main.js --jq '.[] | "\(.sha[0:7]) \(.commit.author.date) \(.commit.message)"'

# Via Git
cd repo-name
git log --follow --oneline -- src/main.js

# View changes to file
git log -p -- src/main.js
```

### Find Specific Changes

```bash
# Find when a function was added
cd repo-name
git log -S"function functionName"

# Find when a line was changed
git blame src/main.js

# Find commits that changed specific lines
git log -L 10,20:src/main.js
```

### Release Comparison

```bash
# Compare releases
gh api repos/owner/repo-name/compare/v1.0.0...v2.0.0 --jq '{
  commits: .total_commits,
  files: [.files[].filename],
  authors: [.commits[].commit.author.name] | unique
}'

# Generate changelog
gh api repos/owner/repo-name/compare/v1.0.0...v2.0.0 --jq '.commits[] | "- \(.commit.message)"'

# See contributors between releases
gh api repos/owner/repo-name/compare/v1.0.0...v2.0.0 --jq '[.commits[].commit.author.name] | unique | .[]'
```

### Audit Trail

```bash
# List all commits by author
gh api repos/owner/repo-name/commits?author=username --jq '.[] | {
  date: .commit.author.date,
  message: .commit.message,
  files: [.files[].filename]
}'

# Find commits in time period
gh api "repos/owner/repo-name/commits?since=2025-01-01T00:00:00Z" --jq '.[] | "\(.commit.author.date): \(.commit.message)"'

# Track specific file changes
gh api repos/owner/repo-name/commits?path=config.yml --jq '.[] | {
  date: .commit.author.date,
  author: .commit.author.name,
  message: .commit.message
}'
```

### Branch Comparison

```bash
# See commits in feature branch not in main
gh api repos/owner/repo-name/compare/main...feature-branch --jq '.commits[] | "\(.sha[0:7]) \(.commit.message)"'

# Count commits ahead/behind
gh api repos/owner/repo-name/compare/main...feature-branch --jq '{ahead: .ahead_by, behind: .behind_by}'

# See files that differ
gh api repos/owner/repo-name/compare/main...feature-branch --jq '.files[] | .filename'
```

## Advanced Usage

### Commit Statistics

**Get commit activity:**
```bash
gh api repos/owner/repo-name/stats/commit_activity --jq '.[] | {week: .week, commits: .total}'
```

**Get contributor stats:**
```bash
gh api repos/owner/repo-name/stats/contributors --jq '.[] | {
  author: .author.login,
  total: .total,
  weeks: .weeks | length
}'
```

**Code frequency:**
```bash
gh api repos/owner/repo-name/stats/code_frequency --jq '.[] | {week: .[0], additions: .[1], deletions: .[2]}'
```

### Commit Verification

**Check commit signature:**
```bash
gh api repos/owner/repo-name/commits/abc123 --jq '.commit.verification | {
  verified: .verified,
  reason: .reason,
  signature: .signature
}'
```

**List verified commits:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | select(.commit.verification.verified == true) | "\(.sha[0:7]) \(.commit.message)"'
```

### Working with Git Directly

**Clone and explore:**
```bash
gh repo clone owner/repo-name
cd repo-name

# Beautiful log
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# Find merge commits
git log --merges --oneline

# Find specific author's work
git shortlog -sn --author="John Doe"

# Show commits by date
git log --since="2 weeks ago" --until="yesterday"
```

## Output Formatting

### Custom Formats

**Concise commit list:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"'
```

**Detailed with stats:**
```bash
gh api repos/owner/repo-name/commits --jq '.[] | {
  commit: .sha[0:7],
  author: .commit.author.name,
  date: .commit.author.date,
  message: .commit.message,
  additions: .stats.additions,
  deletions: .stats.deletions
}'
```

**CSV format:**
```bash
gh api repos/owner/repo-name/commits --jq -r '.[] | [.sha[0:7], .commit.author.name, .commit.author.date, .commit.message] | @csv'
```

## Error Handling

### Commit Not Found
```bash
# Verify commit exists
gh api repos/owner/repo-name/commits/abc123 2>&1 | grep -q "Not Found" && echo "Commit not found"
```

### Rate Limiting
```bash
# Check rate limit
gh api rate_limit --jq '.resources.core'

# Use authenticated requests
gh auth status
```

### Repository Access
```bash
# Verify you have access
gh repo view owner/repo-name

# Check permissions
gh api repos/owner/repo-name --jq '.permissions'
```

## Best Practices

1. **Use short SHAs**: 7 characters is usually sufficient
2. **Filter early**: Use API parameters to reduce data transfer
3. **Cache locally**: Clone repos for intensive commit analysis
4. **Use jq effectively**: Filter and format API responses
5. **Respect rate limits**: Use authenticated requests
6. **Pagination**: Handle large commit histories properly
7. **Date formats**: Use ISO 8601 format for consistency
8. **Verify commits**: Check signatures for security-critical repos

## Integration with Other Skills

- Use `pull-request-management` to see commits in PRs
- Use `issue-management` to link commits to issues
- Use `repository-management` to clone repos for commit analysis
- Use `code-review` to review specific commits

## Git Commands Reference

```bash
# History
git log                    # View commit history
git log --oneline         # Condensed view
git log --graph           # Graphical view
git log -p                # Show patches
git log --stat            # Show statistics

# Specific commits
git show <sha>            # View commit details
git show <sha>:file       # View file at commit

# Search
git log --grep="text"     # Search messages
git log --author="name"   # Filter by author
git log -S"code"          # Search code changes

# Comparison
git diff <sha1>..<sha2>   # Compare commits
git diff branch1..branch2 # Compare branches

# Statistics
git shortlog -sn          # Commits per author
git log --since="date"    # Time-based filter
```

## References

- [GitHub API Commits Documentation](https://docs.github.com/en/rest/commits/commits)
- [Git Log Documentation](https://git-scm.com/docs/git-log)
- [Git Show Documentation](https://git-scm.com/docs/git-show)
- [GitHub CLI Manual](https://cli.github.com/manual/)

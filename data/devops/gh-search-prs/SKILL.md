---
name: gh-search-prs
description: Use when searching GitHub pull requests ACROSS REPOSITORIES or organizations - provides syntax for filtering by draft status, merge status, review state, CI checks, branches. For current repo PRs, use gh pr list instead.
---

# GitHub CLI: Search Pull Requests

## Overview

Search for pull requests **across GitHub repositories** using `gh search prs`. Includes PR-specific filters like draft status, merge state, review status, and CI checks.

## ⚠️ CRITICAL: Search vs List Commands

**`gh search prs`** - GitHub-wide search (THIS SKILL):
- Searches across **multiple repositories** or organizations
- Searches in **specific repos outside your current directory**
- Uses GitHub's search query syntax with qualifiers
- Examples: "Find draft PRs in kubernetes repos", "Search for approved PRs in microsoft org"

**`gh pr list`** - Current repository only (NOT THIS SKILL):
- Lists PRs in **your current working directory's repo**
- Uses simple flag-based filtering
- Examples: "Show my PRs in this repo", "List open PRs here"

**When user says "my PRs" or "PRs here" → Use `gh pr list` (NOT this skill)**
**When user specifies repo/org or cross-repo search → Use `gh search prs` (THIS skill)**

## When to Use This Skill

Use this skill when the user explicitly indicates:
- Searching across **multiple repositories or organizations**
- Searching in a **specific repo** (e.g., "in kubernetes/kubernetes")
- Cross-GitHub searches (e.g., "all draft PRs across the organization")
- Complex queries needing search qualifiers (e.g., "approved PRs with >10 comments in golang repos")

**DO NOT use this skill when:**
- User asks about "PRs in this repo" or "my PRs here"
- No repo/org is specified and context is clearly current repository
- Use `gh pr list` for current repo operations instead

## Syntax

```bash
gh search prs [<query>] [flags]
```

## Key Flags Reference

### PR-Specific Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--draft` | Filter draft PRs | `--draft` |
| `--merged` | Filter merged PRs | `--merged` |
| `--merged-at <date>` | Merged at date | `--merged-at ">2024-01-01"` |
| `-B, --base <string>` | Base branch name | `--base main` |
| `-H, --head <string>` | Head branch name | `--head feature-auth` |
| `--review <string>` | Review status | `--review approved` |
| `--review-requested <user>` | Review requested from | `--review-requested @me` |
| `--reviewed-by <user>` | Reviewed by user | `--reviewed-by octocat` |
| `--checks <string>` | CI check status | `--checks success` |

### User Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--author <string>` | Created by user | `--author octocat` |
| `--assignee <string>` | Assigned to user | `--assignee @me` |
| `--mentions <user>` | Mentions specific user | `--mentions octocat` |
| `--commenter <user>` | Commented by user | `--commenter octocat` |
| `--team-mentions <string>` | Mentions team | `--team-mentions myteam` |

### PR Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--label <strings>` | Has specific labels | `--label bug,urgent` |
| `--state <string>` | PR state: open or closed | `--state open` |
| `--milestone <title>` | In specific milestone | `--milestone v1.0` |
| `--locked` | Locked conversation | `--locked` |
| `--no-label` | Has no labels | `--no-label` |

### Repository Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--owner <strings>` | Repository owner | `--owner github` |
| `-R, --repo <strings>` | Specific repository | `--repo cli/cli` |
| `--language <string>` | Repository language | `--language typescript` |
| `--visibility <strings>` | Repo visibility | `--visibility public` |
| `--archived` | In archived repos | `--archived` |

### Engagement Metrics

| Flag | Purpose | Example |
|------|---------|---------|
| `--comments <number>` | Number of comments | `--comments ">5"` |
| `--reactions <number>` | Reaction count | `--reactions ">10"` |
| `--interactions <number>` | Comments + reactions | `--interactions ">15"` |

### Date Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--created <date>` | Creation date | `--created ">2024-01-01"` |
| `--updated <date>` | Last update date | `--updated ">2024-06-01"` |
| `--closed <date>` | Close date | `--closed "<2024-12-31"` |

### Search Scope

| Flag | Purpose | Example |
|------|---------|---------|
| `--match <strings>` | Search in: title, body, comments | `--match title` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by: comments, created, reactions, etc. | `--sort updated` |
| `--order <string>` | Sort direction: asc or desc | `--order desc` |
| `--json <fields>` | JSON output | `--json number,title,state,isDraft` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

`assignees`, `author`, `authorAssociation`, `body`, `closedAt`, `commentsCount`, `createdAt`, `id`, `isDraft`, `isLocked`, `isPullRequest`, `labels`, `number`, `repository`, `state`, `title`, `updatedAt`, `url`

## Exclusion Syntax (Critical!)

When using inline query exclusions (negations with `-`), you MUST use the `--` separator:

✅ Correct: `gh search prs -- "search-terms -qualifier:value"`
❌ Wrong: `gh search prs "search-terms" --flag=-value`
❌ Wrong: `gh search prs "search-terms" --flag=!value`
❌ Wrong: `gh search prs --label=-WIP`

**Examples:**
- `gh search prs -- "feature -label:draft"` (exclude label)
- `gh search prs -- "fix -is:draft"` (exclude draft PRs)
- `gh search prs -- "deploy -author:bot"` (exclude author)
- `gh search prs -- "security -review:changes_requested"` (exclude review status)

**Why the `--` separator is required:**
The `--` tells the shell to stop parsing flags and treat everything after it as arguments. Without it, `-qualifier:value` inside quotes may be misinterpreted.

## Critical Syntax Rules

### When to Use Flag Syntax vs Query Syntax

**Decision Tree:**
```
Does your search include:
  - Any exclusions (NOT, minus, without, except)?  → Use Query Syntax with `--`
  - Complex boolean logic (OR, AND)?              → Use Query Syntax with `--`

Otherwise:
  - Simple positive filters only?                  → Use Flag Syntax
```

**Flag Syntax** (for positive filters):
```bash
gh search prs "refactor" --draft --state open
```

**Query Syntax with `--`** (required for exclusions):
```bash
gh search prs -- "refactor -label:wip -is:draft"
```

**⚠️ NEVER mix both syntaxes in a single command!**

### 1. Exclusions and Negations

**CRITICAL:** When excluding results, you MUST use query syntax with the `--` separator.

#### Exclusion Syntax Rules:
1. Use the `--` separator before your query
2. Use `-qualifier:value` format (dash prefix for negation)
3. Quote the entire query string

#### Examples:

**Single exclusion:**
```bash
# Exclude specific label
gh search prs -- "refactor -label:wip"

# Exclude draft PRs
gh search prs -- "feature -is:draft"
```

**Multiple exclusions:**
```bash
# Exclude multiple labels
gh search prs -- "bug -label:wip -label:blocked"

# Exclude draft PRs and specific review status
gh search prs -- "security -is:draft -review:changes_requested"
```

**Combine with positive filters using flags:**
```bash
# Wrong - mixing syntaxes:
gh search prs "fix" --state open -label:wip  # ❌

# Correct - use query syntax for everything when excluding:
gh search prs -- "fix state:open -label:wip"  # ✅
```

**PowerShell exclusions:**
```powershell
# Use --% to prevent PowerShell parsing
gh --% search prs -- "refactor -label:wip"
```

#### Common Exclusion Patterns:

| User Request | Command |
|--------------|---------|
| "Find PRs but not drafts" | `gh search prs -- "feature -is:draft"` |
| "PRs excluding specific label" | `gh search prs -- "bug -label:wip"` |
| "PRs not from bot authors" | `gh search prs -- "update -author:dependabot -author:renovate"` |
| "PRs excluding failed checks" | `gh search prs -- "deploy -status:failure"` |
| "PRs not targeting main branch" | `gh search prs -- "feature -base:main"` |
| "PRs excluding review status" | `gh search prs -- "fix -review:changes_requested"` |
| "PRs not merged yet" | `gh search prs -- "feature -is:merged"` |

### 2. Special Values

- `@me` - Current authenticated user
  ```bash
  gh search prs --review-requested @me --state open
  ```

### 3. Review Status Values

- `none` - No reviews
- `required` - Review required
- `approved` - Approved
- `changes_requested` - Changes requested

### 4. Check Status Values

- `pending` - Checks pending
- `success` - All checks passed
- `failure` - Checks failed

### 5. Quoting Rules

**Multi-word search:**
```bash
gh search prs "bug fix"
```

**Labels with spaces:**
```bash
gh search prs -- 'refactor label:"needs review"'
```

**Comparison operators need quotes:**
```bash
gh search prs "performance" --comments ">5"
```

## Common Use Cases

**Find your open PRs across all of GitHub:**
```bash
gh search prs --author @me --state open
```

**Find PRs awaiting your review in an organization:**
```bash
gh search prs --review-requested @me --state open --owner kubernetes
```

**Find draft PRs in a specific repo:**
```bash
gh search prs --draft --repo microsoft/vscode
```

**Find merged PRs in date range across an org:**
```bash
gh search prs --merged --merged-at "2024-01-01..2024-12-31" --owner golang
```

**Find PRs with failing checks in specific repos:**
```bash
gh search prs --checks failure --state open --repo cli/cli
```

**Find approved PRs not yet merged in a repo:**
```bash
gh search prs --review approved --state open --repo kubernetes/kubernetes
```

**Find PRs by base branch in an organization:**
```bash
gh search prs --base main --state open --owner github
```

**Find PRs with specific head branch pattern across repos:**
```bash
gh search prs --head feature-* --state open --language go
```

**Exclude specific labels in cross-repo search:**
```bash
gh search prs -- "refactor -label:wip -label:draft" --owner myorg
```

**Find stale PRs across multiple repos:**
```bash
gh search prs --state open --updated "<2024-01-01" --owner rust-lang
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `--label="NOT wip"` or `--draft=-true` | Flag syntax doesn't support negation | Use query: `-- "-label:wip"` or `-- "-is:draft"` |
| `gh search prs fix -label:wip` | `-label` interpreted as flag | Use `--`: `-- "fix -label:wip"` |
| `"fix NOT label:wip"` | `NOT` keyword doesn't work | Use `-`: `-- "fix -label:wip"` |
| Mixing syntaxes: `--draft "fix -label:wip"` | Can't mix flags with query qualifiers | Use query for all: `-- "fix is:draft -label:wip"` |
| `--review-requested @username` | Invalid `@` prefix | Use `@me` or drop `@`: `--review-requested username` |
| Not quoting comparisons | Shell interprets `>` | Quote: `--comments ">5"` |
| `label:"needs review"` outside quotes | Shell parsing error | Quote query: `'label:"needs review"'` |
| Using `--merged` with `--state open` | Contradictory filters | Merged PRs are closed; remove `--state` |
| PowerShell without `--%` | Breaks with exclusions | Add: `gh --%` |

## Installation Check

If `gh` command not found:
```bash
# Check if gh is installed
which gh

# Install: https://cli.github.com/manual/installation
```

If not authenticated:
```bash
# Authenticate with GitHub
gh auth login
```

## Comparison Operators

- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal
- `..` - Range: `10..50` or `2024-01-01..2024-12-31`

## Field Qualifiers

Use `in:` to search specific fields:
- `in:title` - Search in title only
- `in:body` - Search in body only
- `in:comments` - Search in comments only

Example: `gh search prs "authentication in:title" --state open`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests
- For searching other resources: `gh-search-code`, `gh-search-commits`, `gh-search-issues`, `gh-search-repos`

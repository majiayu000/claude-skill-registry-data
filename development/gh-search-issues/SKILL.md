---
name: gh-search-issues
description: Use when searching GitHub issues ACROSS REPOSITORIES or organizations - provides syntax for filtering by labels, state, assignees, authors, comments, reactions, dates. For current repo issues, use gh issue list instead.
---

# GitHub CLI: Search Issues

## Overview

Search for issues **across GitHub repositories** using `gh search issues`. Add `--include-prs` flag to also search pull requests.

## ⚠️ CRITICAL: Search vs List Commands

**`gh search issues`** - GitHub-wide search (THIS SKILL):
- Searches across **multiple repositories** or organizations
- Searches in **specific repos outside your current directory**
- Uses GitHub's search query syntax with qualifiers
- Examples: "Find issues in the microsoft organization", "Search for bugs in kubernetes repos"

**`gh issue list`** - Current repository only (NOT THIS SKILL):
- Lists issues in **your current working directory's repo**
- Uses simple flag-based filtering
- Examples: "Show my issues in this repo", "List open bugs here"

**When user says "my issues" or "issues here" → Use `gh issue list` (NOT this skill)**
**When user specifies repo/org or cross-repo search → Use `gh search issues` (THIS skill)**

## When to Use This Skill

Use this skill when the user explicitly indicates:
- Searching across **multiple repositories or organizations**
- Searching in a **specific repo** (e.g., "in kubernetes/kubernetes")
- Cross-GitHub searches (e.g., "all my open issues across GitHub")
- Complex queries needing search qualifiers (e.g., "comments>50 across microsoft repos")

**DO NOT use this skill when:**
- User asks about "issues in this repo" or "my issues here"
- No repo/org is specified and context is clearly current repository
- Use `gh issue list` for current repo operations instead

## Syntax

```bash
gh search issues [<query>] [flags]
```

## Key Flags Reference

### User Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--author <string>` | Created by user | `--author octocat` |
| `--assignee <string>` | Assigned to user | `--assignee @me` |
| `--mentions <user>` | Mentions specific user | `--mentions octocat` |
| `--commenter <user>` | Commented by user | `--commenter octocat` |
| `--team-mentions <string>` | Mentions team | `--team-mentions myteam` |

### Issue Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--label <strings>` | Has specific labels | `--label bug,urgent` |
| `--state <string>` | Issue state: open or closed | `--state open` |
| `--milestone <title>` | In specific milestone | `--milestone v1.0` |
| `--locked` | Locked conversation | `--locked` |
| `--no-label` | Has no labels | `--no-label` |

### Repository Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--owner <strings>` | Repository owner | `--owner github` |
| `-R, --repo <strings>` | Specific repository | `--repo cli/cli` |
| `--language <string>` | Repository language | `--language go` |
| `--visibility <strings>` | Repo visibility | `--visibility public` |
| `--archived` | In archived repos | `--archived` |

### Engagement Metrics

| Flag | Purpose | Example |
|------|---------|---------|
| `--comments <number>` | Number of comments | `--comments ">10"` |
| `--reactions <number>` | Reaction count | `--reactions ">5"` |
| `--interactions <number>` | Comments + reactions | `--interactions ">20"` |

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
| `--include-prs` | Include pull requests | `--include-prs` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by: comments, created, reactions, etc. | `--sort comments` |
| `--order <string>` | Sort direction: asc or desc | `--order desc` |
| `--json <fields>` | JSON output | `--json number,title,state` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

`assignees`, `author`, `authorAssociation`, `body`, `closedAt`, `commentsCount`, `createdAt`, `id`, `isLocked`, `isPullRequest`, `labels`, `number`, `repository`, `state`, `title`, `updatedAt`, `url`

## Exclusion Syntax (Critical!)

When using inline query exclusions (negations with `-`), you MUST use the `--` separator:

✅ Correct: `gh search issues -- "search-terms -qualifier:value"`
❌ Wrong: `gh search issues "search-terms" --flag=-value`
❌ Wrong: `gh search issues "search-terms" --flag=!value`
❌ Wrong: `gh search issues --label!=bug`

**Examples:**
- `gh search issues -- "bug -label:wontfix"` (exclude label)
- `gh search issues -- "crash -assignee:olduser"` (exclude assignee)
- `gh search issues -- "error -author:bot"` (exclude author)
- `gh search issues -- "performance -milestone:v1.0"` (exclude milestone)

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
gh search issues "bug" --label urgent --state open
```

**Query Syntax with `--`** (required for exclusions):
```bash
gh search issues -- "bug -label:duplicate -label:wontfix"
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
gh search issues -- "bug -label:duplicate"

# Exclude specific assignee
gh search issues -- "crash -assignee:olduser"
```

**Multiple exclusions:**
```bash
# Exclude multiple labels
gh search issues -- "bug -label:duplicate -label:wontfix"

# Exclude author and label
gh search issues -- "performance -author:bot -label:invalid"
```

**Combine with positive filters using flags:**
```bash
# Wrong - mixing syntaxes:
gh search issues "bug" --state open -label:duplicate  # ❌

# Correct - use query syntax for everything when excluding:
gh search issues -- "bug state:open -label:duplicate"  # ✅
```

**PowerShell exclusions:**
```powershell
# Use --% to prevent PowerShell parsing
gh --% search issues -- "bug -label:duplicate"
```

#### Common Exclusion Patterns:

| User Request | Command |
|--------------|---------|
| "Find bugs but not duplicates" | `gh search issues -- "bug -label:duplicate"` |
| "Issues not assigned to anyone" | `gh search issues -- "enhancement -assignee:*"` (use `--no-assignee` instead) |
| "Open issues excluding specific label" | `gh search issues -- "state:open -label:wontfix"` |
| "Issues excluding multiple labels" | `gh search issues -- "crash -label:duplicate -label:invalid"` |
| "Issues not in milestone" | `gh search issues -- "bug -milestone:v1.0"` |
| "Issues not by bot authors" | `gh search issues -- "error -author:dependabot -author:renovate"` |

### 2. Special Values

- `@me` - Current authenticated user
  ```bash
  gh search issues --assignee @me --state open
  ```

### 3. Quoting Rules

**Multi-word search:**
```bash
gh search issues "memory leak"
```

**Labels with spaces:**
```bash
gh search issues -- 'crash label:"bug fix"'
```

**Comparison operators need quotes:**
```bash
gh search issues "performance" --comments ">10"
```

## Common Use Cases

**Find your open issues across all of GitHub:**
```bash
gh search issues --author @me --state open
```

**Find unassigned bugs in a specific org:**
```bash
gh search issues --label bug --no-assignee --state open --owner kubernetes
```

**Find highly discussed issues in a specific repo:**
```bash
gh search issues --comments ">50" --state open --repo microsoft/vscode
```

**Find stale issues across multiple repos:**
```bash
gh search issues --state open --updated "<2023-01-01" --owner myorg
```

**Search issues AND PRs in an organization:**
```bash
gh search issues "authentication" --include-prs --state open --owner github
```

**Exclude specific labels in cross-repo search:**
```bash
gh search issues -- "crash -label:duplicate -label:wontfix" --repo cli/cli
```

**Find issues in milestone across repos:**
```bash
gh search issues --milestone v2.0 --state open --owner golang
```

**Find issues by title only in specific language repos:**
```bash
gh search issues "error in:title" --state open --language rust
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `--label="NOT duplicate"` or `--assignee=-bot` | Flag syntax doesn't support negation | Use query: `-- "-label:duplicate"` or `-- "-assignee:bot"` |
| `gh search issues bug -label:duplicate` | `-label` interpreted as flag | Use `--`: `-- "bug -label:duplicate"` |
| `"bug NOT label:duplicate"` | `NOT` keyword doesn't work | Use `-`: `-- "bug -label:duplicate"` |
| Mixing syntaxes: `--state open "bug -label:dup"` | Can't mix flags with query qualifiers | Use query for all: `-- "bug state:open -label:dup"` |
| `--assignee @username` | Invalid `@` prefix | Use `@me` or drop `@`: `--assignee username` |
| Not quoting comparisons | Shell interprets `>` | Quote: `--comments ">10"` |
| `label:"bug fix"` outside quotes | Shell parsing error | Quote query: `'label:"bug fix"'` |
| Forgetting `--include-prs` | Misses pull requests | Add: `--include-prs` |
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

Example: `gh search issues "crash in:title" --state open`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests
- For searching other resources: `gh-search-code`, `gh-search-commits`, `gh-search-prs`, `gh-search-repos`

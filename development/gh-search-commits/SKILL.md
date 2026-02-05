---
name: gh-search-commits
description: Use when searching commit history across GitHub repositories - provides syntax for filtering by author, committer, dates, hashes, and merge commits with proper exclusion handling
---

# GitHub CLI: Search Commits

## Overview

Search for commits **across GitHub repositories** using `gh search commits`. Filter by author, committer, dates, commit hashes, and more.

## When to Use This Skill

Use this skill when searching commits across GitHub:
- Finding commits by author or committer across repos/orgs
- Searching commit messages for keywords across repositories
- Filtering by commit dates or hashes in specific repos
- Looking for merge commits across an organization
- Searching in specific repositories or organizations
- Need to exclude certain results (requires `--` flag)

## Syntax

```bash
gh search commits [<query>] [flags]
```

## Key Flags Reference

### Author & Committer Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--author <string>` | Filter by author username | `--author octocat` |
| `--author-name <string>` | Filter by author name | `--author-name "John Doe"` |
| `--author-email <string>` | Filter by author email | `--author-email john@example.com` |
| `--author-date <date>` | Filter by authored date | `--author-date ">2024-01-01"` |
| `--committer <string>` | Filter by committer username | `--committer octocat` |
| `--committer-name <string>` | Filter by committer name | `--committer-name "Jane Doe"` |
| `--committer-email <string>` | Filter by committer email | `--committer-email jane@example.com` |
| `--committer-date <date>` | Filter by committed date | `--committer-date "<2024-06-01"` |

### Commit Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--hash <string>` | Filter by commit hash | `--hash 8dd03144` |
| `--parent <string>` | Filter by parent hash | `--parent abc123` |
| `--tree <string>` | Filter by tree hash | `--tree def456` |
| `--merge` | Filter merge commits only | `--merge` |

### Repository Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--owner <strings>` | Filter by repo owner | `--owner github` |
| `-R, --repo <strings>` | Search in specific repo | `--repo cli/cli` |
| `--visibility <strings>` | Filter by visibility | `--visibility public` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by author-date or committer-date | `--sort author-date` |
| `--order <string>` | Sort direction: asc or desc | `--order asc` |
| `--json <fields>` | JSON output | `--json sha,author,commit` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

Available fields: `author`, `commit`, `committer`, `id`, `parents`, `repository`, `sha`, `url`

## Exclusion Syntax (Critical!)

When using inline query exclusions (negations with `-`), you MUST use the `--` separator:

✅ Correct: `gh search commits -- "search-terms -qualifier:value"`
❌ Wrong: `gh search commits "search-terms" --flag=-value`
❌ Wrong: `gh search commits "search-terms" --flag=!value`
❌ Wrong: `gh search commits --author-not=username`

**Examples:**
- `gh search commits -- "fix -author:dependabot"` (exclude author)
- `gh search commits -- "merge -committer:bot"` (exclude committer)
- `gh search commits -- "deploy -merge:true"` (exclude merge commits)
- `gh search commits -- "refactor -author-date:<2024-01-01"` (exclude date range)

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
gh search commits "bug fix" --author octocat --repo cli/cli
```

**Query Syntax with `--`** (required for exclusions):
```bash
gh search commits -- "deploy -author:dependabot -author:renovate"
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
# Exclude specific author
gh search commits -- "deploy -author:dependabot"

# Exclude specific committer
gh search commits -- "merge -committer:bot"

# Exclude merge commits
gh search commits -- "fix -merge:true"
```

**Multiple exclusions:**
```bash
# Exclude multiple authors
gh search commits -- "deployment -author:dependabot -author:renovate"

# Exclude author and date range
gh search commits -- "refactor -author:bot -author-date:<2024-01-01"

# Exclude merge commits and specific authors
gh search commits -- "feature -merge:true -author:bot"
```

**Combine with positive filters using flags:**
```bash
# Wrong - mixing syntaxes:
gh search commits "fix" --author octocat -committer:bot  # ❌

# Correct - use query syntax for everything when excluding:
gh search commits -- "fix author:octocat -committer:bot"  # ✅
```

**PowerShell exclusions:**
```powershell
# Use --% to prevent PowerShell parsing
gh --% search commits -- "fix -author:dependabot"
```

#### Common Exclusion Patterns:

| User Request | Command |
|--------------|---------|
| "Find commits but not by bots" | `gh search commits -- "deploy -author:dependabot -author:renovate"` |
| "Commits excluding merge commits" | `gh search commits -- "feature -merge:true"` |
| "Commits not by specific author" | `gh search commits -- "refactor -author:olduser"` |
| "Commits excluding specific date range" | `gh search commits -- "bug -author-date:<2024-01-01"` |
| "Commits not by multiple committers" | `gh search commits -- "fix -committer:bot -committer:ci"` |
| "Commits excluding specific email" | `gh search commits -- "update -author-email:bot@example.com"` |
| "Commits not in specific repo" | `gh search commits -- "security -repo:old/deprecated"` |

### 2. Date Formats

Use ISO8601 format (YYYY-MM-DD) with comparison operators:
```bash
gh search commits --author-date ">2024-01-01"
gh search commits --committer-date "2024-01-01..2024-12-31"
```

### 3. Quoting Rules

**Multi-word search:**
```bash
gh search commits "bug fix"
```

**Date comparisons need quotes:**
```bash
gh search commits "refactor" --author-date "<2024-06-01"
```

## Common Use Cases

**Find commits by author:**
```bash
gh search commits --author octocat --repo cli/cli
```

**Search commit messages:**
```bash
gh search commits "security fix" --repo myorg/myrepo
```

**Find commits in date range:**
```bash
gh search commits "refactor" --author-date "2024-01-01..2024-12-31"
```

**Find merge commits:**
```bash
gh search commits --merge --repo owner/repo
```

**Exclude bot commits:**
```bash
gh search commits -- "deployment -author:dependabot"
```

**Search by commit hash:**
```bash
gh search commits --hash 8dd03144
```

**Find commits by email:**
```bash
gh search commits --author-email user@example.com
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `--author="NOT bot"` or `--committer=-user` | Flag syntax doesn't support negation | Use query: `-- "-author:bot"` or `-- "-committer:user"` |
| `gh search commits fix -author:bot` | `-author` interpreted as flag | Use `--`: `-- "fix -author:bot"` |
| `"deploy NOT author:bot"` | `NOT` keyword doesn't work | Use `-`: `-- "deploy -author:bot"` |
| Mixing syntaxes: `--author octocat "fix -committer:bot"` | Can't mix flags with query qualifiers | Use query for all: `-- "fix author:octocat -committer:bot"` |
| `--author-date 2024-01-01` without comparison | May not work as expected | Use: `--author-date ">2024-01-01"` |
| Not quoting date comparisons | Shell interprets operators | Quote: `"<2024-06-01"` |
| `--author @octocat` | Invalid `@` prefix | Drop `@`: `--author octocat` |
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

## Date Comparison Operators

- `>` - After date
- `>=` - On or after date
- `<` - Before date
- `<=` - On or before date
- `..` - Date range: `2024-01-01..2024-12-31`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-commits
- For searching other resources: `gh-search-code`, `gh-search-issues`, `gh-search-prs`, `gh-search-repos`

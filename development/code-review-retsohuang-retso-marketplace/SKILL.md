---
name: code-review
description: Review commits from a starting commit hash to HEAD. Use when user says "review commits from <hash>", "code review starting from <hash>", "review changes since <hash>", or provides a commit hash for review. Detects AI slop, component issues, and missed reuse opportunities.
license: MIT
allowed-tools: Read Grep Glob Bash
metadata:
  author: Retso Huang
  version: "1.0"
---

# Code Review

Review changes from a starting commit hash to HEAD, analyzing each commit individually like a human code reviewer would on a merge request.

## Usage

Provide a commit hash to start the review from. The review will analyze all commits from that hash to HEAD.

## Review Principles

Follow [Google's Code Review Standards](https://google.github.io/eng-practices/review/reviewer/standard.html):

- **Design**: Well-designed and appropriate for the system?
- **Functionality**: Behaves as intended? Good for users?
- **Complexity**: Can others understand and use this easily?
- **Tests**: Correct and well-designed automated tests?
- **Naming**: Clear variable, function, class names?
- **Comments**: Clear, useful, explain _why_ not _what_?
- **Style**: Follows style guidelines?

**Philosophy**: Code should improve overall code health, even if not perfect. Balance forward progress with quality.

## Important Guidelines

- **Big picture first**: Understand the commit's purpose before examining specific code
- **Context matters**: A line change only makes sense when you understand why it changed
- **Cross-file awareness**: Changes in one file often relate to changes in others
- **Look for what's missing**: Sometimes the issue is what WASN'T changed
- **Be specific**: Reference exact line numbers and file paths
- **Be actionable**: Each issue should have clear description and optional suggestion
- **No false positives**: Only flag genuine issues matching the rules

## Workflow

### Step 1: Prepare Review Data

Run the CLI to collect commit metadata:

```bash
python3 ./scripts/cli.py prepare "<provided-commit-hash>"
```

Output is in TOON format (Token-Oriented Object Notation) for efficient LLM processing:

```toon
commits[2]{hash,author,date,subject,body,filesChanged}:
  abc1234...,Alice,2025-01-15,Add new feature,null,3
  def5678...,Bob,2025-01-14,Fix bug in parser,null,1
commitList[2]: abc1234...,def5678...
branch: feature-branch
commitRange: abc123^..HEAD
totalCommits: 2
```

Parse the `commits` array from the CLI output and display a table:

| #   | Commit  | Message           | Files |
| --- | ------- | ----------------- | ----- |
| 1   | abc1234 | Add new feature   | 3     |
| 2   | def5678 | Fix bug in parser | 1     |

Use AskUserQuestion to ask which commits to review:

- Option 1: "Review all" - review all commits in the table
- Option 2: Free input for specific indices (e.g., "1,3,5" or "2-4")

### Step 2: Load Review Rules

Read all rules from references/:

### Step 3: Review Each Commit

For each commit in `commitList`:

1. Get the diff using `python3 ./scripts/cli.py get-diff <commit-hash>`
2. Apply the loaded rules to the changes
3. Record issues found

**Issue Structure:**

```toon
issues[2]{file,startLine,endLine,category,icon,severity,description,suggestion}:
  path/to/file.tsx,42,45,AI Slop,🧹,medium,Brief actionable description,Remove unnecessary comment
  src/utils/helper.ts,18,22,Component Reuse,♻️,low,Existing utility available,Use shared/utils
```

**Severity Guidelines:**

- `high`: Bugs, security issues, broken functionality
- `medium`: Design problems, complexity issues, missing tests
- `low`: Style issues, suggestions, minor improvements

### Step 4: Aggregate and Deduplicate

After reviewing all commits:

1. Deduplicate issues (same file + line range + category)
2. Calculate totals by category and severity

### Step 5: Generate Summary

Read `assets/summary-template.md` and fill in the values:

| Variable            | Description                                       |
| ------------------- | ------------------------------------------------- |
| `{commitRange}`     | Git commit range (e.g., `abc123^..HEAD`)          |
| `{commits}`         | Total number of commits reviewed                  |
| `{files}`           | Total number of files changed                     |
| `{issues}`          | Total number of issues found                      |
| `{humanReviewTime}` | Estimated human review time (2 min per 100 lines) |
| `{dedupLine}`       | Deduplication info or empty string                |
| `{topIssues}`       | List of top issue categories with counts          |
| `{recommendations}` | List of key actionable recommendations            |

Output the formatted summary.

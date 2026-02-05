---
name: github-copilot-pr-review
description: "Review and apply GitHub Copilot suggestions on pull requests. Trigger when reviewing PRs with Copilot suggestions."
author: Claude Code
date: 2025-01-01
---

# GitHub Copilot PR Review Workflow

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-01 |
| **Goal** | Review and apply GitHub Copilot suggestions on PRs using gh CLI |
| **Environment** | Windows, gh CLI 2.63.2+, private GitHub repo |
| **Status** | Success |

## Context

GitHub Copilot provides code review suggestions on pull requests. These suggestions need to be reviewed programmatically using the `gh` CLI since WebFetch returns 404 for private repos. This workflow covers setting up access and efficiently reviewing/applying suggestions.

## Prerequisites: GitHub CLI Setup

### Install gh CLI

**Windows (manual download):**
```bash
# Download from https://github.com/cli/cli/releases
# Extract to a permanent location
# Add to PATH
```

**Verify installation:**
```bash
gh --version
# gh version 2.63.2 (2024-12-18)
```

### Authenticate for Private Repos

```bash
# Interactive login - opens browser
gh auth login

# Select: GitHub.com > HTTPS > Login with a web browser
# Follow the prompts to authenticate
```

**Verify authentication:**
```bash
gh auth status
# github.com
#   Logged in to github.com account username (keyring)
#   Git operations for github.com configured to use https protocol.
```

## Verified Workflow

### 1. View PR Details

```bash
# Get PR metadata
gh pr view 36 --repo owner/repo --json title,body,state,additions,deletions,changedFiles,commits,mergeable

# Check if PR is mergeable
gh pr view 36 --repo owner/repo --json mergeable
```

### 2. List Copilot Suggestions

```bash
# Get all review comments (includes Copilot suggestions)
gh api repos/owner/repo/pulls/36/comments

# Filter for Copilot suggestions (look for user.login = "github-copilot[bot]")
gh api repos/owner/repo/pulls/36/comments --jq '.[] | select(.user.login == "github-copilot[bot]") | {path, body, line}'
```

**Example Copilot suggestion format:**
```json
{
  "path": "alpaca_trading/gpu/vae_ood_detector.py",
  "body": "**Suggestion:** Use `torch.quantile` instead of `kthvalue` for percentile...",
  "line": 245,
  "diff_hunk": "@@ -240,6 +240,10 @@ def _compute_threshold(self, errors)..."
}
```

### 3. Categorize Suggestions

Create a table to track suggestions:

| # | File | Issue | Valid? | Action |
|---|------|-------|--------|--------|
| 1 | vae_ood_detector.py:245 | Use torch.quantile | Yes | Fix |
| 2 | ensemble_ppo.py:150 | Duplicate LayerNorm | Yes | Fix |
| 3 | curiosity_module.py:89 | Add arXiv citation | Yes | Add |
| 4 | test_*.py:30 | Unused import | Yes | Remove |

### 4. Apply Fixes

For each valid suggestion:

1. **Read the file** to understand context
2. **Make the fix** using Edit tool
3. **Verify syntax** with `python -m py_compile file.py`
4. **Commit incrementally** for traceability

```bash
# After all fixes
git add -A
git commit -m "fix: Apply Copilot suggestions

- Use torch.quantile for percentile calculations
- Fix LayerNorm dimension for Conv1d outputs
- Handle buffer edge cases for last transitions
- Add arXiv citations to docstrings
- Remove unused imports"

git push origin branch-name
```

### 5. Handle Multiple PRs with Overlapping Suggestions

When PR #35 and PR #36 have overlapping Copilot suggestions:

1. **Identify the target PR** (the one you'll merge)
2. **Review suggestions from both PRs**
3. **Apply all valid suggestions to target PR only**
4. **Close superseded PR with explanation**

```bash
# Close superseded PR
gh pr close 35 --repo owner/repo --comment "Superseded by #36 which includes all valid Copilot suggestions from both PRs."
```

### 6. Verify All Suggestions Applied

```bash
# Re-check Copilot suggestions after push
gh api repos/owner/repo/pulls/36/comments --jq 'length'

# Run tests
python -m pytest tests/test_affected_module.py -v
```

## API Reference

### Get PR Comments (All Types)
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

### Get Review Threads
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
```

### Create PR
```bash
gh pr create --base stable --title "Title" --body "Description"
```

### Close PR
```bash
gh pr close {pr_number} --repo owner/repo --comment "Reason"
```

### View PR Files Changed
```bash
gh pr view {pr_number} --repo owner/repo --json files --jq '.files[].path'
```

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| WebFetch for private repo | 404 Not Found | Use gh CLI for private repos |
| `gh` without auth | Permission denied | Must run `gh auth login` first |
| Applying fixes to wrong PR | Wasted effort, needed to re-apply | Identify target PR before starting |
| Bulk commit all fixes | Hard to track which suggestion fixed what | Commit with descriptive messages |
| Ignoring "minor" suggestions | Accumulated tech debt | Apply all valid suggestions |
| Not verifying syntax after fix | Broke the build | Always `python -m py_compile` |

## Key Insights

- **gh CLI is essential for private repos**: WebFetch returns 404
- **Copilot suggestions are in PR review comments on code lines**: These are GitHub "review comments" (from `pulls/{pr_number}/comments`), not general PR discussion comments; filter by `user.login`.
- **Categorize before fixing**: Create a table to track all suggestions
- **One target PR**: When multiple PRs overlap, pick one and close others
- **Commit messages matter**: Reference the specific fix for traceability
- **Verify after each fix**: Syntax check prevents build failures

## Common Copilot Suggestion Categories

| Category | Example | Typical Fix |
|----------|---------|-------------|
| **Type safety** | `any` -> `Any` | Import from typing |
| **Performance** | `kthvalue` -> `quantile` | Use better PyTorch API |
| **Edge cases** | Buffer overflow | Add bounds checking |
| **Documentation** | Missing citations | Add arXiv/paper refs |
| **Dead code** | Unused imports | Remove |
| **Silent failures** | Return zeros | Raise ValueError |

## References

- gh CLI documentation: https://cli.github.com/manual/
- GitHub REST API for PRs: https://docs.github.com/en/rest/pulls
- Example session: Reviewed 48 Copilot suggestions across PR #35 and #36

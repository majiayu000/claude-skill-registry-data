---
name: pr-review-comments
description: Fetch and analyze GitHub PR review comments and code-level feedback using the prc CLI. Use this skill whenever the user mentions PR comments, PR feedback, reviewer feedback, review comments, addressing reviews, fixing PR issues, checking what reviewers said, loading PR context, or working on PR revisions. Accepts PR numbers (auto-detects repo), PR URLs, or owner/repo format.
---

# PR Review Comments

This skill fetches GitHub pull request review comments using the `prc` CLI tool and loads them as context to help address reviewer feedback.

## When to Use

Use this skill when the user:
- Asks to review PR comments or feedback
- Wants to address reviewer comments
- Needs context about what reviewers said
- Mentions working on PR revisions or fixes
- Provides a GitHub PR URL or references a specific PR number

## How to Use

### Basic Usage

The `prc` CLI accepts three formats:

```bash
# just PR number (auto-detects repo from git remote when in a git repo)
prc 123 --compact

# full PR URL
prc https://github.com/owner/repo/pull/123 --compact

# repo and PR number
prc owner/repo 123 --compact
```

Always use `--compact` flag for cleaner output that focuses on essential information (author, comment body, and code references).

### Handling Too Many Comments

If the PR has many comments or the comments seem unhelpful for the review task:
1. Use the `--code-only` flag to filter only comments with code references
2. This reduces noise and focuses on comments about specific code locations

```bash
prc owner/repo 123 --compact --code-only
```

### Example Workflow

1. User provides PR URL or mentions PR number
2. Run `prc` with the PR information and `--compact` flag
   - if in a git repo, just use: `prc 123 --compact`
   - otherwise use full URL or owner/repo format
3. Review the comments to understand reviewer feedback
4. If too many comments or not useful, re-run with `--code-only`
5. Use the context to make appropriate code changes

## Output Format

The compact format includes:
- **Author**: Who wrote the comment
- **Comment body**: The actual feedback
- **Code reference**: File and line numbers where applicable

This provides sufficient context while minimizing token usage.

## Notes

- no `--token` flag needed (GitHub CLI token is already configured globally)
- comments are ordered chronologically
- code references help locate exactly where changes are needed
- the tool works with any public or private repo the user has access to

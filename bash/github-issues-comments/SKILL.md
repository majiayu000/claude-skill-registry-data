---
name: github-issues-comments
description: How to create well-formatted GitHub issues and comments without shell escaping problems. Use when creating issues, editing issue bodies, commenting on issues/PRs, or creating pull requests via the gh CLI.
---

# Creating GitHub Issues and Comments

How to create well-formatted GitHub issues and comments without shell escaping problems.

## The core problem

When creating issues or comments via `gh issue create` with inline `--body` text, shell escaping mangles markdown formatting — backticks get escaped as `\``, breaking inline code rendering. This also affects fenced code blocks and any other markdown that uses backticks.

The same applies to `gh issue comment`, `gh pr create`, and any other `gh` subcommand that accepts a `--body` flag.

## Solution: always use --body-file

Write the body content to a temporary file first, then pass it with `--body-file`. This completely avoids shell escaping.

### Creating an issue

1. Write the body to a file using the **Write** tool (not `cat`, `echo`, or heredocs):

   ```
   Write tool → /tmp/issue-body.md
   ```

   The file should contain raw markdown — backticks, code blocks, links, etc. all written literally with no escaping.

2. Create the issue:

   ```bash
   gh issue create --title "Issue title here" --label "label-name" --body-file /tmp/issue-body.md
   ```

### Editing an issue body

```bash
gh issue edit <NUMBER> --body-file /tmp/issue-body.md
```

### Commenting on an issue or PR

1. Write the comment to a file using the **Write** tool.

2. Post it:

   ```bash
   gh issue comment <NUMBER> --body-file /tmp/comment.md
   ```

   Or for PRs:

   ```bash
   gh pr comment <NUMBER> --body-file /tmp/comment.md
   ```

### Creating a pull request

```bash
gh pr create --title "PR title" --body-file /tmp/pr-body.md
```

## What NOT to do

These approaches all cause escaping problems:

- **Inline --body with backticks**: `gh issue create --body "Use \`foo\` here"` — backticks get mangled
- **$(cat <<'EOF' ... EOF)**: Heredoc inside command substitution — backticks may be escaped depending on shell context
- **$(cat file)**: Command substitution — still subject to shell processing

## Formatting guidelines

- Use standard GitHub-flavored markdown in the body file
- Backticks for inline code: `` `composer run test-unit` ``
- Triple backticks for code blocks (with language hint): ````php ...` ```
- Use `**bold**` for emphasis, not ALL CAPS
- Structure with `## Headings` for scannable sections
- Keep issue bodies focused: Context → Problem → Proposed fix / Options

## Orchestrator note

When running under the orchestrator workflow (prefix-based permission model), the `gh api` approach with `-F body=@file` is also available — see the orchestrator-permissions skill for details. The `--body-file` flag on `gh issue create` / `gh issue edit` / `gh pr create` is the simpler approach when those commands are permitted.

---
name: ocm-project-conventions
description: "HyperFleet/OCM project rules for Git, commits, PRs, Markdown, and team communication"
---

# OCM/HyperFleet Project Conventions

## Git & Commits

- **Never** add `Co-Authored-By` in commit messages.
- **Always** sign commits with `-S` flag (GPG signature required).
- **Maintain exactly 1 commit per PR** — squash existing commits or use `git commit --amend` to consolidate.
- **Include ticket ID** in commit message when a ticket exists (e.g., `HYPERFLEET-123: Add feature`).

## Pull Requests & GitHub CLI

- **Include ticket ID in PR title** if a ticket exists.
- **NEVER prefix** PR/ticket titles with `HYPERFLEET-XXXX` format.
- **After reviewing/fixing a PR review comment**, follow this exact sequence: (1) apply the fix, (2) commit, (3) push, then (4) reply inside the comment thread using GitHub CLI so the reply stays threaded:
  ```bash
  gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
    --input - <<< '{"body":"Your response here"}'
  ```
  **Important:** Never use `gh pr comment` for review responses — use the thread reply endpoint above.
- **Use GitHub CLI (`gh`)** for all GitHub interactions.
- **Use Jira CLI** for all Jira interactions.

## Markdown Formatting (*.md files)

- **Always use fenced code blocks with language identifier:**
  ```go
  // Good
  func main() {}
  ```
  ❌ Bad: ` ``` ... ``` ` (missing language)
- **Always close code blocks** with three backticks.
- **Check for MD040 linting error** — fenced code blocks must have a language defined.
- **Never use bold pseudo-headings** like `**Title**` — use proper heading syntax instead:
  ```markdown
  ✅ ### Proper Heading
  ❌ **Pseudo Heading**
  ```

## Testing & Quality Assurance

- **When testing code**, always check for and run integration test suites and E2E test suites as well.

## Communication & Agent Interaction

- **Ask for clarification** before making decisions — never assume package names, database choice, API details, etc.
- **Respond directly below** when user pastes a comment or question into the chat.
- **Never add signatures** like "Generated with Claude Code" to outputs.
- **Provide clean plain text output** suitable for copy-paste — do not use border characters like `▎` on each line.

## When to Apply

Apply these conventions when:
- Working on HyperFleet repositories (API, Sentinel, Adapter, Broker, etc.)
- Contributing to OCM (Open Cluster Management) projects
- Any project with shared team conventions matching these rules

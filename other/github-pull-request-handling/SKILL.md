---
name: github-pull-request-handling
description: Handle pull requests and review comments using GitHub CLI (gh). Use when the user wants to check PR comments, address review feedback, reply with commit hashes, or work with pull requests.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: automation
  since: "2026-02-25"
---

# PR and Review Comment Handling

Guides fetching unresolved PR conversations, addressing them with fixes, and replying with commit references.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- `jq` for formatting (used by `pr-conversations.sh`)
- Current branch has an associated PR, or user provides PR number

## PR lifecycle focus

Stage: **Post-review conversation handling** (after review comments exist).

## Use Instead [if available]

- Use `pr-create` to draft/open a new PR.
- Use `pr-self-review` before requesting external review.
- Use `pr-review` for reviewer-side structured code review.

## Workflow

### 1. Fetch unresolved conversations

The skill base directory is shown at the top of the loaded skill content. Use it to construct the script path:

```bash
# Replace SKILL_BASE_DIR with the base directory shown in the skill header:
SKILL_BASE_DIR/scripts/pr-conversations.sh [PR_NUMBER]        # unresolved only (default)
SKILL_BASE_DIR/scripts/pr-conversations.sh --all [PR_NUMBER]  # all threads
```

Uses the GitHub **GraphQL API** to fetch review threads with resolution status. Output:

- **○** unresolved thread
- **✓** resolved thread (only with `--all`)
- **⚠** outdated thread (code changed since comment)
- **●** first comment in the conversation
- **└** subsequent replies

Threads are sorted by file path and line number. Only act on **○ unresolved** threads.

### 2. Address each unresolved conversation

- **Read the full thread** — understand the root comment and any replies before acting
- **Create a test for bugs and fix them**
- **One commit per conversation**: Fix each issue in a separate commit for traceability
- Use conventional commit format: `fix(scope): description`

### 3. Reply via API with commit hash

**Use clickable links** so reviewers can jump to the commit:

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments -X POST --input - <<'JSON'
{
  "body": "Fixed in [COMMIT_HASH](https://github.com/OWNER/REPO/commit/COMMIT_HASH)",
  "in_reply_to": COMMENT_ID
}
JSON
```

`in_reply_to` must be an **integer** (the `databaseId` from the script output).

### 4. Optional: summary comment

```bash
gh pr comment PR_NUMBER --body "Addressed all unresolved conversations:

1. **Topic** → [hash](https://github.com/OWNER/REPO/commit/hash)
2. **Topic** → [hash](https://github.com/OWNER/REPO/commit/hash)"
```

## Quick reference

| Task | Command |
|------|---------|
| Unresolved conversations | `SKILL_BASE_DIR/scripts/pr-conversations.sh [PR]` |
| All conversations | `SKILL_BASE_DIR/scripts/pr-conversations.sh --all [PR]` |
| View PR | `gh pr view` |
| Add PR comment | `gh pr comment PR_NUMBER --body "..."` |
| Reply to comment | `gh api repos/.../pulls/PR_NUMBER/comments -X POST` with `in_reply_to` |
| Get repo owner/name | `gh repo view --json nameWithOwner -q .nameWithOwner` |

## Commit hash format

- Use a short hash (typically 8 chars, e.g. `f16cfdae`)
- Link: `https://github.com/OWNER/REPO/commit/HASH`
- Markdown: `[f16cfdae](https://github.com/Unique-AG/ai/commit/f16cfdae)`

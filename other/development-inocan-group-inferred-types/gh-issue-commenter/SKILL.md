---
name: gh-issue-commenter
description: Comment on GitHub issues using the gh CLI. Use when Codex needs to share an implementation plan, progress update, or blockers. Always read the issue body and comments for context, optionally read related issues, and only create or update Codex-owned comments.
---

# GitHub Issue Commenter

Create or update a single Codex-owned issue comment for plans, progress, or blockers. Keep comments concise and precise; use Markdown headings and code blocks for snippets.

## Workflow

1. Identify the issue number (using skills or user input).
2. Read the issue body and existing comments for context:
   - `gh issue view <issue-number> --comments`
3. If the issue references related issues (e.g., `#123` or links), read them as needed:
   - `gh issue view <related-issue-number> --comments`
4. Draft the comment with a stable marker so only Codex-owned comments are edited.
5. Create or update the Codex-owned comment using the script:
   - `.codex/skills/gh-issue-commenter/scripts/issue_comment_sync.sh <issue-number> <body-file> [--commenter <login>]`

## Comment Format

Start every comment with the marker on its own line:

```
<!-- CODEX:gh-issue-commenter -->
```

Then use a compact structure appropriate to the update type.

**Plan**
```
<!-- CODEX:gh-issue-commenter -->

**Plan**
1. ...
2. ...
```

**Progress**
```
<!-- CODEX:gh-issue-commenter -->

**Progress**
- ...

**Next**
- ...
```

**Blockers**
```
<!-- CODEX:gh-issue-commenter -->

**Blockers**
- ...

**Needs**
- ...
```

## Constraints

- You MUST read the issue body and comments before posting.
- You MUST only create or edit Codex-owned comments (identified by the marker).
- You SHOULD keep the comment concise and focused.
- You MAY split updates into multiple sections if it improves clarity.
- If `--commenter` is used, it MUST be the GitHub login used to locate the Codex-owned comment to update.

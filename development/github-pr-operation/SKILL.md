---
name: github-pr-operation
description: |
  GitHub Pull Request operations skill. Uses gh command to retrieve PR info,
  check diffs, and get/post comments.
  Use when:
  - Posting comments to a PR
  - Posting inline comments to a PR
  - Replying to PR comments
  - Checking diffs with line numbers
---

# GitHub PR Operation Skill

Reference for GitHub Pull Request operations using gh command.

## 1. Prerequisites

- gh CLI installed and authenticated
- jq installed

## 2. Get PR Information

### 2.1. Basic Information

```bash
gh pr view NUMBER --repo OWNER/REPO --json title,body,author,state,baseRefName,headRefName,url
```

### 2.2. Get Current Branch PR Number

```bash
gh pr view --json number -q '.number'
```

### 2.3. Get Latest Commit SHA

Required for inline comment posting.

```bash
gh pr view NUMBER --repo OWNER/REPO --json commits --jq '.commits[-1].oid'
```

## 3. Check Diff

### 3.1. Diff with Line Numbers

Use for identifying inline comment positions.

```bash
gh pr diff NUMBER --repo OWNER/REPO | awk '
BEGIN { old_line=0; new_line=0; in_hunk=0 }
/^diff --git/ { in_hunk=0; print; next }
/^---/ || /^\+\+\+/ { print; next }
/^@@/ {
  in_hunk=1
  match($0, /-([0-9]+)/, old)
  match($0, /\+([0-9]+)/, new)
  old_line = old[1]
  new_line = new[1]
  print
  next
}
in_hunk && /^-/ { printf "L%-4d     | %s\n", old_line++, $0; next }
in_hunk && /^\+/ { printf "     R%-4d| %s\n", new_line++, $0; next }
in_hunk { printf "L%-4d R%-4d| %s\n", old_line++, new_line++, $0; next }
{ print }
'
```

Output format:

- `L123      |` - Deleted line (left side line number)
- `R456      |` - Added line (right side line number)
- `L123 R456 |` - Unchanged line (both line numbers)

## 4. Get Comments

### 4.1. Issue Comments (PR-wide Comments)

```bash
gh api repos/OWNER/REPO/issues/NUMBER/comments --jq '.[] | {id, user: .user.login, created_at, body}'
```

### 4.2. Review Comments (Inline Comments)

```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments --jq '.[] | {id, user: .user.login, path, line, body, in_reply_to_id}'
```

### 4.3. Get All Comments at Once

```bash
# Issue comments
gh api repos/OWNER/REPO/issues/NUMBER/comments > /tmp/issue-comments.json

# Review comments
gh api repos/OWNER/REPO/pulls/NUMBER/comments > /tmp/review-comments.json
```

## 5. Post Comments

### 5.1. PR-wide Comment

```bash
gh pr comment NUMBER --repo OWNER/REPO --body "Comment body"
```

For multiple lines:

```bash
gh pr comment NUMBER --repo OWNER/REPO --body "$(cat <<'EOF'
## Review Results

- Issue 1
- Issue 2
EOF
)"
```

### 5.2. Inline Comment

Post comment on specific line.

```bash
# Get latest commit SHA
COMMIT_SHA=$(gh pr view NUMBER --repo OWNER/REPO --json commits --jq '.commits[-1].oid')

# Post inline comment
gh api repos/OWNER/REPO/pulls/NUMBER/comments \
  --method POST \
  -f body="Comment body" \
  -f commit_id="$COMMIT_SHA" \
  -f path="path/to/file.py" \
  -F line=15 \
  -f side=RIGHT
```

Parameters:

| Parameter | Description |
| --- | --- |
| body | Comment body |
| commit_id | Target commit SHA |
| path | File path (relative from repository root) |
| line | Line number (use R number from diff right side) |
| side | RIGHT (added line) or LEFT (deleted line) |

### 5.3. Reply to Comment

```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments/COMMENT_ID/replies \
  --method POST \
  -f body="Reply body"
```

## 6. Notes

### 6.1. Inline Comment Line Numbers

- Use diff right side (R) line numbers
- For comments on deleted lines, use `side=LEFT` and left side (L) line number
- Line numbers are absolute positions in file, not positions within diff hunk

### 6.2. Comment Posting Permissions

- PR comment posting depends on GitHub permissions
- Only executable on repositories you have access to

### 6.3. Relationship with rules/git.md

This skill provides operations (How).
Follow `rules/git.md` for permission rules.

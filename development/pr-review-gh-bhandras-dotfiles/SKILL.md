---
name: pr-review-gh
description: Create GitHub PRs with gh, fetch review comments, fix them commit-by-commit, and reply to each comment individually with correctly formatted bodies.
metadata:
  short-description: GitHub PR and review workflow (gh)
---

# PR Review Workflow (gh)

Use this skill when you need to create a PR, pull review comments, fix them
incrementally, and reply to each comment individually using `gh`.

## Quick Workflow

1) Create/update PR
- `gh pr create --fill --body-file /tmp/pr_body.txt`
- `gh pr edit --body-file /tmp/pr_body.txt`

2) Fetch review comments
- Summary/comments: `gh pr view <PR> --comments`
- Structured data: `gh api repos/{owner}/{repo}/pulls/<PR>/comments`
- Pagination (recommended for large threads): add `--paginate`
- Skip resolved threads by ignoring any comment that already has a reply
  (a matching `in_reply_to_id` exists) or that is marked resolved in the UI.
- Unresolved-only JSON (ignore replied-to threads):
```bash
python - <<'PY'
import json, subprocess
raw = subprocess.check_output(
    ["gh", "api", "--paginate", "repos/{owner}/{repo}/pulls/<PR>/comments"],
    text=True,
)
comments = json.loads(raw)
replied_to = {c.get("in_reply_to_id") for c in comments if c.get("in_reply_to_id")}
unresolved = [
    {
        "id": c.get("id"),
        "html_url": c.get("html_url"),
        "path": c.get("path"),
        "body": c.get("body"),
    }
    for c in comments
    if c.get("in_reply_to_id") is None and c.get("id") not in replied_to
]
print(json.dumps(unresolved, indent=2))
PY
```
- Unresolved-only JSON (jq):
```bash
gh api --paginate repos/{owner}/{repo}/pulls/<PR>/comments \
  | jq '[. as $all
    | ($all | map(select(.in_reply_to_id != null) | .in_reply_to_id) | unique) as $replied
    | $all[]
    | select(.in_reply_to_id == null and (.id | IN($replied[]) | not))
    | {id, html_url, path, body}]'
```

3) Fix review notes commit-by-commit
- For each comment batch:
  - implement fix
  - `git add <files>`
  - `git commit -m "pkg: <short change>"`
  - repeat until all notes addressed
- If amending, use `git commit --amend` and then
  `git push --force-with-lease`
- Ensure fixes land in the commit the reviewer commented on:
  - Identify `commit_id` from the review comment payload.
  - Use `git rebase -i <base>` and `git commit --amend` to update that commit.
  - Rewrite history as needed and force-push to the branch.
  - Confirm the diff for the addressed commit is updated.

4) Test after fixes
- Run extensive tests after applying fixes to ensure correctness.
- Prefer `make lint` and relevant unit/integration tests.
- Note any tests not run in the PR response.

5) Reply to each comment individually
- Use `in_reply_to` for line comment replies:
  - `gh api -X POST repos/{owner}/{repo}/pulls/<PR>/comments \
      -F in_reply_to=<COMMENT_ID> \
      -F body='Acked; updated to ...'`

## Comment Formatting Rules

- Use real newlines, not literal `\n`.
- For multi-line replies, prefer a heredoc:
```bash
gh api -X POST repos/{owner}/{repo}/pulls/<PR>/comments \
  -F in_reply_to=<COMMENT_ID> \
  -F body=@- <<'EOF'
Applied fix:
- updated X
- refactored Y
EOF
```
- Keep replies concise and specific to the change made.

## Fetch and Respond Example

1) Find comment IDs:
`gh api repos/{owner}/{repo}/pulls/<PR>/comments`

2) Reply:
`gh api -X POST repos/{owner}/{repo}/pulls/<PR>/comments \
  -F in_reply_to=<COMMENT_ID> \
  -F body='Updated sh() to use argv lists and removed shell=True.'`

## Notes

- `gh pr view <PR> --comments` is quick for a read-only pass.
- Use `gh api .../pulls/<PR>/comments` to get `id` values for replies.
- Keep each review response tied to its specific thread.

---
name: my-pr-comments
description: Loads the pr review comments for the current branch.
allowed-tools: Bash(gh pr view:*), Bash(gh api:*)
---

Get the current pr number:

```bash
gh pr view --json "url" | jq '.url'
```

Now you can run this command to get all the pr comments in JSON

```bash
gh api repos/corpaxe/{reponame}/pulls/{prnumber}/comments --paginate --jq '.[] | {file: .path, line: .line, body: .body, author: .user.login}'
```

## Example:

```bash
gh pr view --json "url" | jq '.url'

# outputs
"https://github.com/corpaxe/External.Frontend/pull/2972"

gh api   repos/corpaxe/External.Frontend/pulls/2976/comments | jq '.[] | {file: .path, line: .line, body: .body, author: .user.login}'
```

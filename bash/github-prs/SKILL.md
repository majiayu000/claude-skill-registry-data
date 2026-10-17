---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: github-prs
description: >
  How to create and update GitHub PRs, issues, comments, and releases with the
  gh CLI in Tommy's voice. Covers body formatting, heredocs, fork branching,
  CI watching, PR review threads with gh pr-review, and release notes rules.
  ALWAYS load before running `gh pr create/edit`, `gh issue create/edit/comment`,
  `gh release create`, or replying to or resolving PR review comments.
---

# github-prs

## Before creating anything

- **Ask first** only when the repo owner is not `remorses`. For remorses repos, just do it.
- **Check for an existing PR** on the current branch, upstream first: `gh pr list --head <branch> -R upstream-owner/repo`. Update existing PRs, issues, and comments with `gh pr edit`, `gh issue edit`. Never recreate.
- **Never close** a PR or issue without my explicit confirmation.
- **Match the format** of recent PRs, issues, and commits in the repo (`gh pr list --state merged -L 5`, `git log --oneline -10`).

## Branching in a fork

If `origin` and `upstream` differ, branch from upstream's default branch:

```bash
git remote -v
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
git fetch upstream
git checkout -b my-branch upstream/$DEFAULT_BRANCH
```

## Writing the body

- Write as **me**, first person. Never "we" or "our". Casual, concise, no corporate fluff.
- Use **bold text** as section labels, never markdown headings (headings look like AI slop).
- Use lists, code blocks, tables. No big blobs of text.
- Reference related issues and PRs (`#123`). Put closing keywords (`Fixes #123`) only in the `.changeset` file.
- Never pass `\n` in `--body`. Use a heredoc:

```bash
gh pr create --title 'fix: handle empty config' --body "$(cat <<'EOF'
**Problem**

Empty `config.json` crashed the loader.

**Fix**

- return defaults when file is empty
- added a test for the empty case
EOF
)"
```

## After creating a PR

Print the PR URL, then watch CI:

```bash
gh pr checks --watch --fail-fast
```

## Review comments

Uses the `gh pr-review` extension (agynio/gh-pr-review).

```bash
# view unresolved threads and their IDs
gh pr-review review view 42 -R owner/repo --unresolved

# reply to a thread
gh pr-review comments reply 42 -R owner/repo \
  --thread-id PRRT_kwDOAAABbcdEFG12 \
  --body 'Fixed in latest commit'

# resolve a thread
gh pr-review threads resolve 42 -R owner/repo --thread-id PRRT_kwDOAAABbcdEFG12
```

- **Never fabricate** GraphQL node IDs. Query them or take them from the mutation result.
- If a pending review blocks replies, **dismiss** it. Never submit it with placeholder text like "Reviewing suggestions".

## Releases

- End users read these. Omit chores and internal changes.
- Be detailed on user-facing API changes and features, with code snippets.
- **Never** pass `--prerelease`, even for versions like `1.0.0-rsc.2`; GitHub hides those from the default view. Always pass `--latest`.

~~~bash
gh release create v1.2.0 --latest --title 'v1.2.0' --notes "$(cat <<'EOF'
**New: `createClient({ retry })`**

```ts
const client = createClient({ retry: 3 })
```
EOF
)"
~~~

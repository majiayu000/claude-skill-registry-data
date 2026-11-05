---
name: gh
description: GitHub workflow automation with the gh CLI — pull requests, issues, releases, the REST/GraphQL API, and safe message escaping. Auth via GH_TOKEN (set in global settings, attached to the sandbox env).
type: pattern
tier: library
domains: [vcs, git, github]
trigger: "gh, github, pull request, PR, github issue, github release, gh api, github actions, gh workflow"
---

# GitHub Workflow Skill

GitHub workflow management using the `gh` CLI for pull requests, issues, releases, and the GitHub API.

## Authentication

`gh` reads `GH_TOKEN` (or `GITHUB_TOKEN`) from the environment — no interactive `gh auth login` needed. In the Jonggrang sandbox the token is injected automatically when set in **global settings** (Git tokens). Verify with:

```bash
gh auth status        # shows the active account / token source
```

If `GH_TOKEN` is unset, every command below fails with an auth error — set it in the dashboard's global settings, then restart the sandbox.

## ⚠️ Message Escaping — Common Trap

**If a title/body/comment contains backticks (`` ` ``), `$`, `!`, or `\`, NEVER inline them in `-t "..."` / `-b "..."`.** The shell interprets backticks as command substitution and silently mangles the text (e.g. `client_name: command not found`, identifiers stripped). This causes real failures: malformed PR/issue comments followed by apologetic corrections.

### ❌ DON'T — inline special chars in a double-quoted flag

```bash
# BROKEN: shell executes `client_name` as a command
gh pr comment 100 -b "Use `client_name` and `wor/` here."
```

### ✅ DO — write to a file first, then pass via --body-file

Most `gh` commands that take a body accept `--body-file <path>` (and `-F`/`--body-file -` for stdin). Prefer it over `-b`:

```bash
# MSG = a path you pick (mktemp, scoped tmp, etc.) unique to this invocation
MSG=$(mktemp)
cat > "$MSG" << 'EOF'
Use `client_name` and `wor/` here. The `gh` tool handles this.
EOF
gh pr comment 100 --body-file "$MSG"
```

The single-quoted `'EOF'` delimiter prevents ALL variable/backtick expansion. Triple-backtick code blocks are safe inside `<<'EOF'` heredocs — only single backticks and `$` trigger substitution in an **unquoted** heredoc.

```bash
# BROKEN: unquoted EOF — backticks in body are still interpreted while writing
cat > "$MSG" << EOF
Use `client_name` here.
EOF
```

**Rule of thumb:** body contains `` ` ``, `$`, `!`, or `\` → write it to a file with `<< 'EOF'` and pass `--body-file`, always.

## Pull Requests

Push the branch first (or pass `--head`), and be explicit about base/head so `gh` doesn't pick the wrong remote/fork.

```bash
# Create — simple
gh pr create --base main --head feat/my-branch --title "Add feature" --body "Brief description"

# Create — rich body from a file (see escaping above)
gh pr create --base main --head feat/my-branch --title "Add feature" --body-file "$MSG"

# Specify the repo explicitly (outside the repo, or to avoid wrong remote)
gh pr create -R owner/repo --base main --head feat/x --title "…" --body-file "$MSG"

# List / view / check status
gh pr list --state open
gh pr view 123                 # add --json state,mergeable,reviews for machine output
gh pr diff 123
gh pr checks 123               # CI status for the PR

# Review actions
gh pr comment 123 --body-file "$MSG"
gh pr review 123 --approve            # or --request-changes --body-file "$MSG"
gh pr ready 123                       # mark draft → ready

# Merge (choose one strategy; --delete-branch optional)
gh pr merge 123 --merge               # or --squash / --rebase
gh pr merge 123 --squash --delete-branch
```

`gh pr merge` waits for required checks if branch protection demands them; add `--auto` to enable auto-merge when checks pass.

## Issues

```bash
gh issue create --title "Bug: …" --body-file "$MSG" --label bug --assignee @me
gh issue list --state open --label bug
gh issue view 42
gh issue comment 42 --body-file "$MSG"
gh issue close 42 --comment "fixed in #123"
```

## Releases

```bash
gh release create v1.2.0 --title "v1.2.0" --notes-file "$MSG"
gh release create v1.2.0 --generate-notes            # auto changelog from PRs
gh release upload v1.2.0 ./dist/app.tar.gz           # attach assets
gh release list
```

## REST / GraphQL API (escape-safe via -f / -F)

When you need something the porcelain commands don't cover, hit the API. Pass fields with `-f key=value` (string) or `-F key=@file` / `-F key=value` (typed/file), which avoids shell-escaping the body:

```bash
# POST a PR review comment with a body read from a file
gh api --method POST "repos/owner/repo/issues/100/comments" -F "body=@$MSG"

# Read JSON and filter with --jq
gh api "repos/owner/repo/pulls/123" --jq '.mergeable_state'

# GraphQL
gh api graphql -f query='query { viewer { login } }'
```

## Tips

- **Machine-readable output:** add `--json <fields>` (+ optional `--jq`) to most read commands instead of scraping text — e.g. `gh pr view 1 --json state,mergeStateStatus`.
- **Repo context:** inside a clone, `gh` infers the repo from the `origin` remote. Outside one, always pass `-R owner/repo`.
- **Never** run `gh auth login` in automation — rely on `GH_TOKEN`.
- **Don't** paste tokens into commands or commit them; they come from the environment.

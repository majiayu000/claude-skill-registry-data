---
name: github
description: >-
  Interact with GitHub: read repos, view/create/merge PRs, manage issues, comment, review,
  rebase, check CI status, manage releases, and search code. This skill should be used when
  the user asks about GitHub PRs, issues, repos, CI checks, releases, or workflows. Triggers
  on keywords like "github", "PR", "pull request", "issue", "merge", "rebase", "review",
  "checks", "CI", "release", "gh", "repo", or GitHub URL patterns (owner/repo#123).
triggers:
  - github
  - PR
  - pull request
  - issue
  - merge
  - rebase
  - review
  - checks
  - CI
  - release
  - gh
  - repo
---

# GitHub Skill

Interact with GitHub using the `gh` CLI. All commands run via Bash with built-in authentication, pagination, and JSON output support.

## Prerequisites

The `gh` CLI must be installed and authenticated:

```bash
gh auth status    # Check authentication
gh auth login     # Authenticate if needed
```

If `gh` is not installed, direct the user to https://cli.github.com/ or `brew install gh`.

## Core Concepts

### JSON Output

Most `gh` commands support `--json` for structured output. Combine with `--jq` for filtering:

```bash
gh pr view 123 --json title,state,body --jq '.title'
gh issue list --json number,title,state --jq '.[] | "\(.number) \(.title)"'
```

### Repository Context

`gh` auto-detects the repository from the current git directory. Override with `-R owner/repo`:

```bash
gh pr list -R owner/repo
```

### Pagination

Use `--limit` to control result count (default varies by command):

```bash
gh issue list --limit 50
gh pr list --limit 100
```

## Command Reference

### Pull Requests

| Command | Description |
|---------|-------------|
| `gh pr list` | List open PRs (add `--state closed/merged/all`) |
| `gh pr view <number>` | View PR details |
| `gh pr view <number> --comments` | View PR with comments |
| `gh pr create` | Create PR from current branch |
| `gh pr create --title "T" --body "B"` | Create PR non-interactively |
| `gh pr checkout <number>` | Check out a PR branch locally |
| `gh pr diff <number>` | View PR diff |
| `gh pr checks <number>` | Show CI status for a PR |
| `gh pr review <number> --approve` | Approve a PR |
| `gh pr review <number> --comment --body "msg"` | Add review comment |
| `gh pr review <number> --request-changes --body "msg"` | Request changes |
| `gh pr merge <number>` | Merge a PR (prompts for method) |
| `gh pr merge <number> --squash` | Squash merge |
| `gh pr merge <number> --rebase` | Rebase merge |
| `gh pr comment <number> --body "msg"` | Add a comment |
| `gh pr edit <number> --title "T"` | Edit PR metadata |
| `gh pr close <number>` | Close a PR |
| `gh pr reopen <number>` | Reopen a PR |
| `gh pr ready <number>` | Mark draft PR as ready |

### Issues

| Command | Description |
|---------|-------------|
| `gh issue list` | List open issues |
| `gh issue list --label bug` | Filter by label |
| `gh issue list --assignee @me` | Filter by assignee |
| `gh issue view <number>` | View issue details |
| `gh issue view <number> --comments` | View with comments |
| `gh issue create --title "T" --body "B"` | Create an issue |
| `gh issue comment <number> --body "msg"` | Add a comment |
| `gh issue edit <number> --add-label "bug"` | Add labels |
| `gh issue close <number>` | Close an issue |
| `gh issue reopen <number>` | Reopen an issue |
| `gh issue pin <number>` | Pin an issue |
| `gh issue transfer <number> <repo>` | Transfer to another repo |
| `gh issue develop <number>` | Create a linked branch |

### Repository

| Command | Description |
|---------|-------------|
| `gh repo view` | View current repo details |
| `gh repo view owner/repo` | View a specific repo |
| `gh repo list <owner>` | List repos for owner/org |
| `gh repo clone owner/repo` | Clone a repo |
| `gh repo fork` | Fork current repo |
| `gh repo sync` | Sync fork with upstream |

### CI/CD & Workflows

| Command | Description |
|---------|-------------|
| `gh run list` | List recent workflow runs |
| `gh run view <id>` | View run details |
| `gh run watch <id>` | Watch a run live |
| `gh run rerun <id>` | Rerun a failed run |
| `gh run download <id>` | Download run artifacts |
| `gh workflow list` | List all workflows |
| `gh workflow run <file>` | Trigger a workflow manually |

### Releases

| Command | Description |
|---------|-------------|
| `gh release list` | List releases |
| `gh release view <tag>` | View release details |
| `gh release create <tag>` | Create a release |
| `gh release download <tag>` | Download release assets |

### Search

| Command | Description |
|---------|-------------|
| `gh search repos <query>` | Search repositories |
| `gh search issues <query>` | Search issues across GitHub |
| `gh search prs <query>` | Search PRs across GitHub |
| `gh search code <query>` | Search code across GitHub |
| `gh search commits <query>` | Search commits |

### Raw API Access

For anything not covered by built-in commands, use `gh api`:

```bash
gh api repos/{owner}/{repo}/pulls/123/comments
gh api graphql -f query='{ viewer { login } }'
```

## Workflow Patterns

**Reviewing a PR**: Fetch details, check CI status, view diff, then approve or request changes.

```bash
gh pr view 123 --json title,body,state,author,reviews,additions,deletions
gh pr checks 123
gh pr diff 123
gh pr review 123 --approve --body "LGTM"
```

**Triaging issues**: List open issues, view details, assign labels.

```bash
gh issue list --state open --json number,title,labels,createdAt --jq '.[:10]'
gh issue view 456
gh issue edit 456 --add-label "priority:high" --add-assignee "@me"
```

**Creating a PR with full context**: Create from current branch with title, body, labels, and reviewers.

```bash
gh pr create --title "Add user auth" --body "## Summary\n- Adds JWT auth\n\n## Test Plan\n- Unit tests added" --label "feature" --reviewer "teammate"
```

**Checking CI before merge**: Wait for checks to pass, then merge.

```bash
gh pr checks 123 --watch
gh pr merge 123 --squash --delete-branch
```

**Rebasing a PR branch**: Update PR branch with latest base.

```bash
gh pr checkout 123
git rebase origin/main
git push --force-with-lease
```

**Searching across repos**: Find issues, PRs, or code across GitHub.

```bash
gh search issues "memory leak" --repo owner/repo --state open
gh search code "TODO" --repo owner/repo --filename "*.ts"
```

### Output Handling

- Use `--json` with `--jq` for structured extraction when presenting to the user
- For `gh pr view`, extract: number, title, state, author, body, reviews, checks
- For `gh issue list`, present as a table with number, title, labels, assignee
- For `gh run list`, show workflow name, status, branch, and conclusion
- Plain text output (default) is suitable for human-readable summaries

### Error Handling

- **Authentication**: If `gh` returns auth errors, run `gh auth status` to diagnose
- **Not found (404)**: Verify repo exists and user has access
- **Permission denied (403)**: Check if the user has write access for mutations
- **Rate limiting**: GitHub API has rate limits; `gh` handles retries but heavy usage may hit limits

## Reference

For detailed command options, advanced API patterns, GraphQL queries, and GitHub search syntax, see `~/.claude/skills/github/references/gh-commands.md`.

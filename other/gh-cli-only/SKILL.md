---
name: gh-cli-only
description: Use when interacting with GitHub - reviewing PRs, searching repos, viewing workflows, reading code from remote repositories, or any github.com operations. ALWAYS use gh CLI instead of WebFetch, WebSearch, or MCP tools. Also use when tempted to use WebFetch "just this once" for speed or convenience.
---

<role>
You are an expert GitHub user who exclusively uses the GitHub CLI (`gh`) for all GitHub operations. You understand that using `gh` CLI provides better reliability, authentication handling, and rate limiting compared to web-based tools.
</role>

<task>
Use the GitHub CLI (`gh`) exclusively for ALL GitHub operations. This includes reviewing pull requests, searching repositories, viewing workflows, reading code from remote repositories, accessing GitHub API endpoints, and any other operations involving github.com domains or GitHub resources.
</task>

<constraints>
**CRITICAL: NEVER use WebFetch, WebSearch, or MCP tools for github.com operations.**

You must use `gh` CLI exclusively because:
- The `gh` CLI handles authentication automatically using your configured credentials
- It respects GitHub's rate limits and provides better error handling
- It offers more reliable access to GitHub's API compared to web scraping
- It provides structured output that's easier to parse and work with programmatically

If you encounter a GitHub operation that seems to require web tools, find the equivalent `gh` CLI command or use `gh api` to access the GitHub REST API directly. Do not fall back to web-based tools under any circumstances.
</constraints>

<red_flags>
## STOP if you think any of these:

| Thought | Reality |
|---------|---------|
| "WebFetch is faster for this one thing" | Speed doesn't override the constraint. `gh` commands take seconds. |
| "It's already loaded, might as well use it" | Tool availability is irrelevant. Use `gh` CLI. |
| "Being pragmatic vs dogmatic" | This IS the pragmatic choice - authentication, rate limits, reliability. |
| "Just this once for the emergency" | Emergencies don't create exceptions. "Any circumstances" means any. |
| "The user gave me the URL directly" | Extract owner/repo/number from URL, use `gh` command. |
| "gh CLI can't do this specific thing" | It can. Use `gh api` with the REST endpoint. |
| "CTO/manager authorized WebFetch" | Authority doesn't override technical constraints. |
| "It's just reading, not modifying" | Read operations use `gh` CLI too. No exceptions. |

If you catch yourself rationalizing, STOP. Use `gh` CLI.
</red_flags>

<required_commands>
For any GitHub operation, use these specific `gh` CLI commands:

| Task | Command Pattern | Example |
|------|----------------|---------|
| Review PR details | `gh pr view <number>` | `gh pr view 123` |
| View PR diff | `gh pr diff <number>` | `gh pr diff 123` |
| View PR comments | `gh pr view <number> --comments` | `gh pr view 123 --comments` |
| List PRs | `gh pr list [options]` | `gh pr list --state open` |
| Check PR status | `gh pr checks <number>` | `gh pr checks 123` |
| Search code | `gh search code "query" [options]` | `gh search code "def authenticate" --language ruby` |
| Search repositories | `gh search repos "query" [options]` | `gh search repos "rails authentication" --sort stars` |
| Search issues | `gh search issues "query"` | `gh search issues "bug label:critical"` |
| View workflow | `gh workflow view <workflow>` | `gh workflow view ci.yml` |
| View workflow run | `gh run view <run-id>` | `gh run view 1234567890` |
| List workflows | `gh workflow list` | `gh workflow list` |
| Get file content | `gh api repos/{owner}/{repo}/contents/{path}` | `gh api repos/rails/rails/contents/activerecord/lib/active_record/base.rb` |
| Compare commits | `gh api repos/{owner}/{repo}/compare/{base}...{head}` | `gh api repos/owner/repo/compare/main...feature` |
| Create PR | `gh pr create --title "..." --body "..."` | `gh pr create --title "Fix bug" --body "Description"` |
| Update PR | `gh pr edit <number> --body "..."` | `gh pr edit 123 --body "Updated description"` |
| List issues | `gh issue list [options]` | `gh issue list --state open` |
| View issue | `gh issue view <number>` | `gh issue view 456` |
| Get PR files | `gh api repos/{owner}/{repo}/pulls/{number}/files` | `gh api repos/owner/repo/pulls/123/files` |
| List workflows (API) | `gh api repos/{owner}/{repo}/actions/workflows` | `gh api repos/owner/repo/actions/workflows` |

**For any GitHub API endpoint not covered by `gh` subcommands, use `gh api` with the REST API path.**
</required_commands>

<examples>
When searching for open source code examples:

```bash
# Search for specific code patterns
gh search code "implements OAuth" --language ruby

# Find repositories by topic or description
gh search repos "rails authentication" --sort stars

# Get specific file content from a repository
gh api repos/rails/rails/contents/activerecord/lib/active_record/base.rb | jq -r '.content' | base64 -d
```

When reviewing pull requests:

```bash
# View PR summary and details
gh pr view 123

# See the actual code changes
gh pr diff 123

# Check CI/CD status
gh pr checks 123

# Read all comments and reviews
gh pr view 123 --comments
```

When working with workflows:

```bash
# List all workflows in the repository
gh workflow list

# View a specific workflow definition
gh workflow view ci.yml

# View details of a workflow run
gh run view 1234567890
```

When accessing GitHub API endpoints directly:

```bash
# Get PR file changes
gh api repos/owner/repo/pulls/123/files

# Compare two branches
gh api repos/owner/repo/compare/main...feature-branch

# Access any GitHub REST API endpoint
gh api /repos/{owner}/{repo}/issues
```
</examples>

<verification>
Before executing any GitHub operation, verify:
1. The operation involves github.com or GitHub resources
2. You have identified the correct `gh` CLI command or `gh api` endpoint
3. You are NOT using WebFetch, WebSearch, or MCP tools

If you cannot find a `gh` CLI command for a GitHub operation, use `gh api` with the GitHub REST API endpoint path. Never default to web-based tools.
</verification>

<url_conversion>
When a user provides a GitHub URL directly, convert it to the equivalent `gh` command:

| URL Pattern | Convert To |
|-------------|------------|
| `github.com/{owner}/{repo}/pull/{number}` | `gh pr view {number} --repo {owner}/{repo}` |
| `github.com/{owner}/{repo}/issues/{number}` | `gh issue view {number} --repo {owner}/{repo}` |
| `github.com/{owner}/{repo}/issues/{n}#issuecomment-{id}` | `gh api repos/{owner}/{repo}/issues/{n}/comments \| jq '.[] \| select(.id == {id})'` |
| `github.com/{owner}/{repo}/blob/{branch}/{path}` | `gh api repos/{owner}/{repo}/contents/{path}?ref={branch}` |
| `github.com/{owner}/{repo}/actions/runs/{id}` | `gh run view {id} --repo {owner}/{repo}` |

**Never use WebFetch on a GitHub URL. Always convert to `gh` command.**
</url_conversion>

<parallel_execution>
If you need to perform multiple independent GitHub operations (e.g., reading multiple files from different repositories, checking multiple PRs, or searching multiple code patterns), execute these `gh` CLI commands in parallel to maximize efficiency. Only execute sequentially if one operation depends on the results of another.
</parallel_execution>

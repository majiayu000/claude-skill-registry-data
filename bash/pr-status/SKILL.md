---
name: pr-status
description: Fetch and display the full status of the current PR — CI checks, GitHub Actions runs, reviews, and code comments — using GitHub MCP tools. Invoke manually with /pr-status.
disable-model-invocation: true
---

# Skill: PR Status

Display a complete dashboard of the current PR's remote state.

## Steps

### 1. Identify the current PR

Run `git branch --show-current` to get the branch name, then use `git log --oneline -1` to get the HEAD SHA.

Use `mcp__github__list_pull_requests` with `head: "spideystreet:<branch>"` and `state: "open"` to find the PR number.

If no open PR is found, report: "No open PR found for branch `<branch>`."

### 2. Fetch all PR data (in parallel)

Call all MCP tools + Actions run in a **single parallel batch**:

| Tool | Data |
|------|------|
| `mcp__github__get_pull_request` | Title, state, author, base/head, mergeable, draft |
| `mcp__github__get_pull_request_status` | Commit statuses (if any) |
| `mcp__github__get_pull_request_reviews` | Reviews (author, state, body) |
| `mcp__github__get_pull_request_comments` | Code review comments (path, line, body, diff_hunk) |
| `gh run list --branch <branch> --limit 5 --json name,status,conclusion,headSha,url` | GitHub Actions workflow runs |

Note: GitHub MCP does not expose Actions runs, so use `gh run list` as a **necessary exception** for this data only.

### 2b. Fetch failed job logs (conditional)

If any Actions run has `conclusion: "failure"`, fetch the logs for the **most recent failed run**:

```bash
gh run view <run_id> --log-failed 2>&1 | tail -60
```

Parse the output to extract the failing job name, step, and error message.

### 3. Format and display

Output a single formatted dashboard:

```
## PR #<number>: <title>

**State**: <open/closed/merged> | **Mergeable**: <mergeable_state> | **Branch**: <head> → <base> | **Author**: @<login>

### GitHub Actions

| Workflow | Status | Conclusion | SHA |
|----------|--------|------------|-----|
| <name> | <status> | <conclusion> | <sha[:7]> |

### Commit Statuses

| Context | State |
|---------|-------|
| <context> | <state> |

(or "None" if empty)

### Reviews

- @<reviewer>: <state> (APPROVED / CHANGES_REQUESTED / COMMENTED)
  > <body excerpt if any>

### Code Comments

- @<author> `<path>#<line>`:
  ```diff
  <diff_hunk>
  ```
  > <body>
```

If a section has no items, show "None" instead of the table/list.

**Merge conflicts**: Check `mergeable` and `mergeable_state` from `get_pull_request`. If `mergeable` is `false` or `mergeable_state` is `"dirty"`, display a prominent warning:

```
⚠ **CONFLICTS** — This branch has conflicts with `main` that must be resolved before merging.
```

If CI failed, add a **Failure Logs** section after GitHub Actions:

```
### Failure Logs (run <run_id>)

**Job**: <job_name> | **Step**: <step_name>

\`\`\`
<last ~40 lines of error output>
\`\`\`
```

## Rules

- **Always use GitHub MCP tools** for PR data — never fall back to `gh` CLI
- Exception: use `gh run list` for GitHub Actions runs (no MCP equivalent)
- Use `git` CLI only for local branch detection
- Call all tools in parallel to minimize latency
- Do not modify any files or state — this is a read-only skill
- Owner and repo are always `spideystreet` / `medox`

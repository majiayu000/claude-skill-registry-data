---
description: "Review code quality of a PR. Inspect Go conventions, architecture compliance, and test quality"
user-invokable: true
---

# /code-review

A skill for conducting code quality reviews on Pull Requests.

## Argument Patterns

- `/code-review <PR number>` — Review the specified PR
- `/code-review` — Review the PR associated with the current branch

---

## Steps

### Step 1: Identify the PR

If an argument is provided:
- Use `<PR number>`

If no argument is provided:
- Get the PR number for the current branch with `gh pr view --json number -q .number`
- If no PR exists, display an error message and exit

### Step 2: Fetch PR Information

Fetch the following **in parallel**:

```bash
gh pr view <PR number> --json title,body,headRefName,baseRefName,number,url
gh pr diff <PR number> --name-only
```

- Record the PR title, branch name, and PR URL
- Get the list of changed files

### Step 3: Fetch Issue Information (optional)

Extract a Linear Issue ID (`USK-XX` format) from the PR body.
If found, fetch the Issue description with `mcp__linear-server__get_issue`.
If not found, leave the Issue-related placeholders empty and continue.

### Step 4: Build Product Context

```
yorishiro-proxy is a network proxy (MCP server) for AI agents.
Provides traffic interception, recording, and replay capabilities for vulnerability assessment.
Architecture: TCP Listener → Protocol Detection → Protocol Handler → Session Recording → MCP Tool
```

### Step 5: Launch Code Review Agent

Read `.claude/agents/code-reviewer.md` with the Read tool and extract the code block inside the `## Prompt Body` section.

Replace placeholders:
- `{{PR_NUMBER}}` → PR number
- `{{PR_TITLE}}` → PR title
- `{{ISSUE_ID}}` → Issue ID (or "N/A")
- `{{ISSUE_DESCRIPTION}}` → Issue description (or "N/A")
- `{{PRODUCT_CONTEXT}}` → Context built in Step 4
- `{{CHANGED_FILES}}` → List of changed files

Launch with Task tool:
- `subagent_type`: `"general-purpose"`
- `isolation`: `"worktree"`
- `description`: `"Code review PR #<N>"`
- `prompt`: Replaced prompt

### Step 6: Report Results

Parse the sub-agent results and report to the user in the following format:

```markdown
## Code Review Results: PR #<N>

**Verdict**: APPROVED / CHANGES_REQUESTED
**PR**: <PR URL>

### Findings Summary

| ID | Severity | File | Category | Description |
|----|----------|------|----------|-------------|
| F-1 | HIGH | ... | ... | ... |

### Stats

- CRITICAL: X, HIGH: X, MEDIUM: X, LOW: X, NIT: X
```

### Step 7: Worktree Cleanup

After reporting results, delete **only the worktree of the sub-agent launched in Step 5**.

Use the agent ID from the Task tool return value and run:

```bash
git worktree list --porcelain | awk '/^worktree /{print $2}' |
  while read -r wt; do
    case "$wt" in *"agent-<agentId>"*) git worktree remove "$wt" --force --force 2>/dev/null || true ;; esac
  done
git worktree prune
```

> Use the canonical cleanup snippet in `CLAUDE.md` → **Agent Isolation Strategy → Worktree
> Cleanup**. Do not construct `.claude/worktrees/agent-<id>` from an ID (a nested sub-agent's
> worktree lives inside its parent's, so the path does not exist and the remove silently
> no-ops), use `--force --force` (a single `--force` fails on a locked worktree), and never
> select paths with `grep -F -f` (this machine's `grep` is ugrep: an empty pattern file matches
> every line).

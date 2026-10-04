---
name: omnicreate-gitlab
description: Use when creating a GitLab merge request (OmniForge). Auto-populates title and description from commits, supports draft MRs, labels, assignees, reviewers, and issue linking
version: 1.3.0
license: Apache-2.0
allowed-tools: Bash, mcp__omniforge__create_gitlab_mr
---

# GitLab Merge Request Creator

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- GitLab remote: !`git remote -v | grep gitlab | head -1`
- glab version: !`glab version 2>/dev/null || echo "NOT_INSTALLED"`
- glab auth status: !`glab auth status 2>&1 || echo "NOT_AUTHENTICATED"`
- Unpushed commits: !`git log @{u}..HEAD --oneline 2>/dev/null || echo "NO_UPSTREAM"`
- Repo root: !`git rev-parse --show-toplevel 2>/dev/null || echo "NOT_A_GIT_REPO"`

## Your Task

Create a GitLab merge request using the `mcp__omniforge__create_gitlab_mr` MCP tool.

> **Why MCP instead of raw bash?**
> The MCP tool validates all inputs, uses safe subprocess execution (no shell interpretation), and provides structured error output — making it safe for use by all models without risk of shell injection.

### Prerequisites

1. Verify `glab` is installed. If not, inform the user:
   ```bash
   brew install glab  # macOS
   ```
2. Verify the current directory is a git repository with a GitLab remote.
3. Ensure there are commits to create an MR from (not on main/master without changes).

### Pre-Flight Checklist

Before creating the MR, verify:

- [ ] glab is installed and authenticated
- [ ] Not on main/master branch
- [ ] Has commits to merge (not empty)
- [ ] No uncommitted changes (warn if present)
- [ ] Branch has upstream or can be pushed

### MCP Tool: `mcp__omniforge__create_gitlab_mr`

Use this tool for all MR creation. It wraps `glab mr create` safely.

**Required parameter:**
- `repo_root`: absolute path to the git repository root (from `git rev-parse --show-toplevel`)

**Optional parameters (pass only what the user specified):**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `""` | Custom MR title (overrides fill) |
| `description` | string | `""` | Custom MR description (overrides fill) |
| `target_branch` | string | `"main"` | Target branch for the MR |
| `source_branch` | string | `""` | Source branch (default: current branch) |
| `assignees` | string | `""` | Comma-separated usernames to assign |
| `reviewers` | string | `""` | Comma-separated usernames to request review from |
| `labels` | string | `""` | Comma-separated label names |
| `draft` | bool | `false` | Mark as draft MR |
| `fill` | bool | `true` | Auto-populate title/description from commits |
| `fill_commit_body` | bool | `true` | Include commit bodies in description |
| `push` | bool | `true` | Push branch if not already pushed |
| `related_issue` | string | `""` | Issue number to link MR to |
| `copy_issue_labels` | bool | `false` | Copy labels from related issue |
| `remove_source_branch` | bool | `false` | Delete source branch after merge |
| `squash_before_merge` | bool | `false` | Squash commits when merging |
| `milestone` | string | `""` | Milestone ID or title |
| `web` | bool | `false` | Open in browser for final editing |

### Title and Description Guidelines

**Never rely on `fill=true` alone.** Always inspect the commits and craft a meaningful title and description. Use `fill=false` and pass explicit `title` and `description` parameters.

#### MR Title

- **Format**: `<type>: <imperative summary>` — mirror conventional commits
  - Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `ci`
  - Example: `feat: add inline thread posting to omnifix workflow`
- **Length**: ≤ 72 characters
- **Tense**: imperative ("add", "fix", "remove") — not past tense ("added", "fixed")
- **Scope** (optional): `feat(auth): ...` — use when the change is scoped to a subsystem
- **Avoid**: vague words like "update", "changes", "misc", "WIP" in the title; do not repeat the branch name verbatim

#### MR Description

Structure the description in this order (omit sections that don't apply):

```markdown
## Summary

<1–3 sentences explaining WHAT changed and WHY. Not a list of commits — the motivation and outcome.>

## Changes

- <bullet: specific, concrete change>
- <bullet: …>

## Testing

- [ ] <what was tested and how>
- [ ] <edge cases covered>

## Related

- Closes #<issue> (if applicable)
- Ref: <link or ticket>
```

**Rules for the description:**
- **Summary** must answer *why* this MR exists, not just *what* it does. E.g. "Adds inline thread posting so the fix skill can resolve discussions without leaving the MCP layer" is better than "This MR adds a new function."
- **Changes** bullets must name specific files, functions, or behaviours — not generic phrases like "updated code" or "fixed issue".
- **Testing** should be checkboxes (`- [ ]`) so reviewers can see what is confirmed.
- Do NOT include any AI-generated attribution, signatures, or "Generated with Claude" lines.
- Do NOT paste raw git log output into the description.
- If the MR is a draft, prepend `**Draft — do not merge.**` as the first line of the Summary.

#### Deriving Title and Description from Commits

Before calling the MCP tool, run:
```bash
git log @{u}..HEAD --oneline        # list commits going into MR
git log @{u}..HEAD --format="%B"    # full commit messages for context
git diff @{u}..HEAD --stat          # files changed
```

Use this output to:
1. Identify the dominant change type (feat/fix/refactor/…)
2. Synthesise the commit subjects into one clear title
3. Expand the commit bodies into the Summary and Changes sections

### Step-by-Step Execution

1. **Check environment**: Verify glab is installed and authenticated, git repo has GitLab remote
2. **Check branch**: If on main/master, inform user they need to create a feature branch first
3. **Check for changes**: If no commits, inform user they need to commit changes first
4. **Warn about uncommitted changes**: If working directory is dirty, warn user before proceeding
5. **Get repo root**: Run `git rev-parse --show-toplevel` to obtain the absolute path
6. **Inspect commits**: Run `git log @{u}..HEAD --oneline` and `git log @{u}..HEAD --format="%B"` to read the commit history
7. **Craft title and description**: Following the guidelines above, write an explicit `title` and `description`; set `fill=false`
8. **Call MCP tool**: Invoke `mcp__omniforge__create_gitlab_mr` with `repo_root`, the crafted `title`, `description`, `fill=false`, and any user-specified options
9. **Report output**: Show the MR URL, number, and any relevant details from the tool response

### Common Patterns

**Default MR (crafted from commits):**
→ Inspect commits, write `title` and `description`, call with `repo_root`, `title`, `description`, `fill=false`

**MR for a specific target branch with assignee:**
→ `repo_root`, `target_branch="staging"`, `assignees="john"`

**Draft MR with WIP label:**
→ `repo_root`, `draft=true`, `labels="WIP"`

**MR with custom title and description:**
→ `repo_root`, `title="Fix bug"`, `description="Detailed description..."`, `fill=false`

**MR linked to issue #42:**
→ `repo_root`, `related_issue="42"`, `copy_issue_labels=true`

**Open in browser for editing:**
→ `repo_root`, `web=true`

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `authentication required` | Not logged in | Run `glab auth login` |
| `no upstream branch` | Branch not pushed | The tool handles push automatically (`push=true`) |
| `branch already exists remotely` | Push conflict | Pull and rebase, or force push with caution |
| `pipeline failed` | CI checks failed | Fix failing tests before creating MR |
| `merge conflicts detected` | Conflicts with target | Rebase onto target branch and resolve |
| `GLab requires authentication` | Token expired | Run `glab auth login --hostname <gitlab-host>` |

### Edge Cases to Handle

- **Not a git repo**: Inform user they need to be in a git repository
- **No GitLab remote**: Inform user the repo doesn't have a GitLab remote
- **glab not installed**: Provide installation instructions
- **Not authenticated**: Run `glab auth login` if needed
- **No commits**: Inform user they need to commit changes first
- **Already on main/master**: Ask user which branch to create MR from
- **Uncommitted changes**: Warn user their working directory has changes not in the MR

### Output Format

After the MCP tool returns, provide a summary like:

```markdown
## Merge Request Created

- **MR**: !123
- **URL**: https://gitlab.com/group/repo/-/merge_requests/123
- **Branch**: feature-branch → main
- **Status**: Open
```

If the tool returns an error, explain it and suggest remediation steps.

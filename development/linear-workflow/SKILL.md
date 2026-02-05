---
name: linear-workflow
description: Linear issue-tracked development workflow. Auto-activates when starting work on issues, creating branches, changing status, writing comments, or creating PRs.
---

# Linear-Tracked Development Workflow

## Prerequisites

**Linear MCP**: Configure in MCP settings:

```json
{
  "mcpServers": {
    "linear": {
      "command": "mcp-remote",
      "args": ["-y", "https://mcp.linear.app/mcp"]
    }
  }
}
```

**gh CLI**: Install and authenticate:

```bash
brew install gh  # or: https://cli.github.com/
gh auth login
```

## Configuration

This skill requires Linear MCP to be configured. On first use:

1. **Check environment variables** in `.claude/settings.json`:

   - If `LINEAR_WORKFLOW_TEAM` and `LINEAR_WORKFLOW_PROJECT` exist → use them
   - If not → guide user to set them up before proceeding

2. **Get issue prefix** dynamically:
   ```bash
   mcp__linear-server__list_issues(team: "{LINEAR_WORKFLOW_TEAM}", limit: 1)
   # Extract prefix from identifier (e.g., "ABC-34" → "ABC")
   ```

### Example settings.json

```json
{
  "env": {
    "LINEAR_WORKFLOW_TEAM": "YourTeam",
    "LINEAR_WORKFLOW_PROJECT": "YourProject"
  }
}
```

> **Note**: `issuePrefix` is auto-detected from Linear, no manual config needed.

---

## Auto-Activation Triggers

- Starting code implementation
- File modifications on main/master without issue branch
- Mentioning a Linear issue ({PREFIX}-XX) in conversation
- Creating commits with Conventional Commits format
- Creating a PR with `Fixes {PREFIX}-XX`

## Workflow Overview

```
Has Issue                    No Issue
    │                            │
    ▼                            ▼
Query via MCP          Plan → Create Issue in Linear
    │                            │
    └──────────┬─────────────────┘
               ▼
    Create branch (use gitBranchName)
               ▼
    Linear status: In Progress + start comment
               ▼
    Work (comment on decisions/blockers)
               ▼
    Create PR (Fixes {PREFIX}-XX)
               ▼
    Merge (rebase-ff) → Linear auto-Done
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Get issue | `mcp__linear-server__get_issue(id: "{PREFIX}-XX")` |
| Update status | `mcp__linear-server__update_issue(id: "{PREFIX}-XX", state: "In Progress")` |
| Add comment | `mcp__linear-server__create_comment(issueId: "{PREFIX}-XX", body: "...")` |
| Create issue | `mcp__linear-server__create_issue(title: "...", team: "{TEAM}", project: "{PROJECT}")` |

---

## 1. Check or Create Issue

### Case A: Starting with Existing Issue

```bash
# Query issue via MCP
mcp__linear-server__get_issue(id: "{PREFIX}-XX")
```

- Use `gitBranchName` field as branch name
- Check Acceptance Criteria in issue description

### Case B: Starting without Issue

After planning, before implementation, create Linear issue using this template:

```bash
mcp__linear-server__create_issue(
  title: "Concise work title",
  description: "<issue description template below>",
  team: "{LINEAR_WORKFLOW_TEAM}"
)
```

**If LINEAR_WORKFLOW_PROJECT is configured**: Add `project: "{LINEAR_WORKFLOW_PROJECT}"` parameter.

> Issues without a project are created in the team's Backlog.

### Issue Description Template

```markdown
## Objective

[One sentence describing what this work achieves]

## Background

- [Why this work is needed]
- [Context or constraints]
- [Related prior work or decisions]

## Implementation Approach

- [High-level approach or strategy]
- [Key technical decisions]
- [Files/components to modify]

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
```

**Guidelines:**

- **Objective**: Single sentence, action-oriented (e.g., "Add logging infrastructure for LLM debugging")
- **Background**: 2-4 bullet points explaining why, not how
- **Implementation Approach**: Technical strategy, not step-by-step instructions
- **Acceptance Criteria**: Checkboxes, testable conditions for "done"

---

## 2. Create Branch

Use the `gitBranchName` field from the Linear issue directly:

```bash
# Get issue details (gitBranchName is included in response)
mcp__linear-server__get_issue(id: "{PREFIX}-XX")

# Create branch using gitBranchName value
git checkout -b <gitBranchName>
```

> **Branch Format**: Configured in Linear at **Settings > Workspace > Integrations > GitHub/GitLab > Branch format**. The `gitBranchName` field reflects your team's configured format.

### Branch Validation

This workflow validates branch names loosely—only requiring a Linear issue ID (e.g., `ABC-123`). This allows teams to use any branch format configured in Linear:

| Branch Example | Valid? |
|----------------|--------|
| `feature/ABC-123-auth` | Yes |
| `john/ABC-123-auth` | Yes |
| `ABC-123-auth` | Yes |
| `ABC-123` | Yes |
| `main` | No (protected) |
| `feature/auth` | No (no issue ID) |

---

## 3. Update Status + Start Comment

```bash
# Update status
mcp__linear-server__update_issue(id: "{PREFIX}-XX", state: "In Progress")

# Start comment (use actual branch name)
mcp__linear-server__create_comment(
  issueId: "{PREFIX}-XX",
  body: "## Started\n\n- Branch: `<branch-name>`\n- Implementing ..."
)
```

---

## Linear Status Transitions

| Status | When to Use | Transition |
|--------|-------------|------------|
| Backlog | Initial state, not yet prioritized | Auto |
| Todo | Ready for work | Manual |
| In Progress | Actively working | Set at branch creation |
| In Review | PR created, awaiting review | Set at PR creation |
| Done | PR merged | Auto (via `Fixes {PREFIX}-XX`) |

---

## 4. Comments During Work

Write comments for major decisions, progress updates, or blockers.

**Language**: English only (for global team collaboration)

### Progress Update

```markdown
## Progress Update

- Completed: [what was done]
- In Progress: [current work]
- Next: [upcoming tasks]
```

### Technical Decision

```markdown
## Decision: [title]

**Context**: [why this decision was needed]

**Options considered**:

1. [Option A] - pros/cons
2. [Option B] - pros/cons

**Chosen**: [option] because [reason]
```

### Blocked

```markdown
## Blocked

**Issue**: [description]
**Waiting on**: [dependency/person]
**Workaround**: [if any]
```

---

## 5. Commit Rules

Conventional Commits + Linear reference:

```bash
git commit -m "feat(scope): implement feature

Refs {PREFIX}-XX"
```

### Commit Types

**SemVer-relevant (required for versioning):**

| Type     | Usage                          | SemVer Impact |
| -------- | ------------------------------ | ------------- |
| `feat`   | New feature                    | MINOR bump    |
| `fix`    | Bug fix                        | PATCH bump    |
| `feat!:` | Breaking change (add ! suffix) | MAJOR bump    |

**Other common types:**

`docs`, `refactor`, `test`, `chore`, `style`, `perf`, `ci`, `build`, `revert`, or any lowercase word that fits the change.

### Linear Reference Keywords

- `Refs {PREFIX}-XX`: Link only (no status change)
- `Closes {PREFIX}-XX`: Auto-close issue on PR merge

---

## 6. Create PR

### PR Title

Conventional Commit format:

```
feat(linear): add workflow skills
```

### PR Body

```markdown
## Summary

- [Change 1]
- [Change 2]

## Test Plan

- [ ] Test item 1
- [ ] Test item 2

Fixes {PREFIX}-XX
```

### PR Creation Command

```bash
gh pr create --title "feat(scope): description" --body "$(cat <<'EOF'
## Summary
- ...

## Test Plan
- [ ] ...

Fixes {PREFIX}-XX

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## 7. Merge

GitHub standard method (rebase-ff):

```bash
# After PR approval
gh pr merge --rebase
```

Linear detects `Fixes {PREFIX}-XX` → auto-closes issue as Done

---

## Linear Magic Words Reference

| Keyword                                    | Effect                      |
| ------------------------------------------ | --------------------------- |
| `closes`, `fixes`, `resolves`, `completes` | Close issue on PR merge     |
| `refs`, `part of`, `related to`            | Link only, no status change |

---

## Workflow Checklist

Copy this checklist and check off items as you complete them:

```
Linear Workflow Progress:

Starting Work:
- [ ] Check if issue exists (create if not)
- [ ] Create branch using `gitBranchName`
- [ ] Status → In Progress
- [ ] Write start comment

During Work:
- [ ] Comment on major decisions/blockers
- [ ] Follow Conventional Commits
- [ ] Include `Refs {PREFIX}-XX` in commits

On Completion:
- [ ] Create PR (include `Fixes {PREFIX}-XX`)
- [ ] Request code review
- [ ] Merge (rebase-ff)
- [ ] Verify Linear auto-Done
```

---
name: github-issue
description: Guide structured GitHub issue creation and management. Use when creating bug reports, feature requests, or issue-related tasks.
---

# GitHub Issue Management Skill

This skill provides a structured approach to writing GitHub issues that communicate context, scope, and direction clearly.

## Title Format (Required)

Issue titles **must** follow conventional commit format:

```
<type>(<scope>): <description>
```

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Examples:**
- `feat(auth): add OAuth2 login support`
- `fix(api): resolve race condition in request handler`
- `chore(deps): update dependencies to latest versions`
- `docs(readme): add installation instructions`

The script validates this format automatically. Use `--skip-validation` only if the repository uses a different convention.

---

## The Why/What/How Framework

Every issue should answer three questions for the reader:
- **Why** does this matter?
- **What** exactly needs to happen?
- **How** should it be approached?

This framework ensures issues are actionable and provide enough context for anyone picking them up.

---

## Issue Template

### Why

Explain the background and motivation:

- **Current state**: What exists today? How does it work?
- **Bottleneck/Problem**: What specific issue or limitation was identified?
- **Value**: Why is solving this valuable? What insights, metrics, or improvements does it unlock?

```markdown
## Why

Currently, [describe current state/behavior].

This causes [specific problem or bottleneck], which [impact on users/system/workflow].

Addressing this will [concrete benefit - improved metrics, unlocked capabilities, better UX].
```

### What

Define the scope concretely:

- **Specific deliverable**: What exactly needs to be built, fixed, or changed?
- **Boundaries**: What is explicitly out of scope?
- **Success criteria**: How do we know when this is done?

```markdown
## What

[Verb] [specific thing] to [achieve outcome].

Scope:
- [In scope item 1]
- [In scope item 2]

Out of scope:
- [Explicitly excluded item]
```

### How

Provide implementation direction:

- **Approach**: High-level strategy or pattern to follow
- **Key files/components**: Where changes will likely occur
- **Architecture sketch**: Skeleton of the solution structure (not implementation details)

```markdown
## How

Approach: [brief strategy - e.g., "Extend existing X pattern", "Add new Y component"]

Key areas:
1. [Component/file] - [what changes here]
2. [Component/file] - [what changes here]

Skeleton:
- [High-level step 1]
- [High-level step 2]
- [Integration point]
```

---

## Acceptance Criteria

Keep acceptance criteria focused on integration and observable behavior:

```markdown
## Acceptance Criteria

- [ ] [Observable behavior or state that confirms completion]
- [ ] [Integration with existing system works as expected]
- [ ] [Edge case or error condition handled]
```

Tips:
- Write criteria that can be verified by running the system
- Focus on "what" not "how" - avoid implementation details
- Include integration points with existing functionality

---

## Testing Plan

Keep testing plans succinct and focused on verification:

```markdown
## Testing Plan

- [ ] [How to manually verify the change]
- [ ] [Key integration scenario to test]
- [ ] [Regression check if applicable]
```

Tips:
- Tests added should integrate within existing test architeture
- Prioritize integration testing over isolated unit tests
- Include the command or steps to run verification
- Note any existing tests that should continue passing

---

## Scripts Reference

This skill includes Python scripts in `scripts/` that wrap GitHub API operations. Run them with `uv`:

### Available Commands

| Command | Description |
|---------|-------------|
| `create` | Create a new issue |
| `create-sub` | Create a sub-issue linked to a parent |
| `view` | View issue details |
| `list` | List issues in a repository |
| `link` | Link two issues (parent/child relationship) |
| `close` | Close an issue |
| `comment` | Add a comment to an issue |
| `labels` | Manage issue labels |
| `init` | Initialize an issue body file with template |

### Usage Examples

```bash
# Initialize a template file
uv run scripts/gh_issue.py init --template default
uv run scripts/gh_issue.py init --template bug
uv run scripts/gh_issue.py init --template feature

# Create an issue from a body file
uv run scripts/gh_issue.py create owner/repo \
  --title "Brief, descriptive title" \
  --body-file /tmp/issue-body.md

# Create with labels and assignees
uv run scripts/gh_issue.py create owner/repo \
  --title "Add caching layer" \
  --body-file /tmp/issue-body.md \
  --labels "enhancement,performance" \
  --assignees "@me"

# Create a sub-issue linked to parent
uv run scripts/gh_issue.py create-sub owner/repo \
  --parent 10 \
  --title "Implement caching middleware" \
  --body-file /tmp/sub-issue.md

# View an issue
uv run scripts/gh_issue.py view owner/repo 123

# List open issues
uv run scripts/gh_issue.py list owner/repo

# List issues by label
uv run scripts/gh_issue.py list owner/repo --labels "bug"

# Link existing issues
uv run scripts/gh_issue.py link owner/repo --parent 10 --child 42

# Add a comment
uv run scripts/gh_issue.py comment owner/repo 123 "Progress update: ..."

# Close an issue
uv run scripts/gh_issue.py close owner/repo 123 --reason completed
```

---

## Creating Issues

### Preview Before Creation

By default, the script shows a preview and asks for confirmation before creating:

```
============================================================
ISSUE PREVIEW
============================================================

Repository: owner/repo
Title: feat(api): add caching to API responses
Labels: enhancement, performance

Body:
----------------------------------------
## Why
...
----------------------------------------

Create this issue?
  y = create issue
  n = cancel
  e = edit (saves to /tmp/issue-body.md for editing)
```

- Press `y` to create the issue
- Press `n` to cancel
- Press `e` to save body to `/tmp/issue-body.md` for editing, then re-run

Use `--yes` or `-y` to skip confirmation (for automation).

### Basic Creation

```bash
# Initialize template
uv run scripts/gh_issue.py init --output /tmp/issue-body.md

# Edit the template with your content
# ... edit /tmp/issue-body.md ...

# Create the issue (will show preview first)
uv run scripts/gh_issue.py create owner/repo \
  --title "feat(api): add caching layer" \
  --body-file /tmp/issue-body.md
```

### With Labels and Assignment

```bash
uv run scripts/gh_issue.py create owner/repo \
  --title "feat(api): add caching layer to API responses" \
  --body-file /tmp/issue-body.md \
  --labels "enhancement,performance" \
  --assignees "@me" \
  --milestone "v2.0"
```

### Adding to a Project

```bash
uv run scripts/gh_issue.py create owner/repo \
  --title "Issue title" \
  --body-file /tmp/issue-body.md \
  --project "Project Name"
```

---

## Linking Issues

### Create a Sub-issue

```bash
# Create a new issue linked to parent #10
uv run scripts/gh_issue.py create-sub owner/repo \
  --parent 10 \
  --title "feat(cache): implement caching middleware" \
  --body "## Why
Part of the caching initiative (#10).

## What
Implement the middleware layer for request caching."
```

### Link Existing Issues

```bash
# Link issue #42 as a sub-issue of #10
uv run scripts/gh_issue.py link owner/repo --parent 10 --child 42
```

### Close Issue via Commit

Reference the issue number in a commit message to auto-close:

```bash
git commit -m "Add caching middleware

Fixes #42"
```

Keywords that close issues: `fixes`, `closes`, `resolves` (followed by `#issue_number`)

---

## Quick Reference

| Task | Command |
|------|---------|
| Init template | `uv run scripts/gh_issue.py init` |
| Init bug template | `uv run scripts/gh_issue.py init --template bug` |
| Create issue | `uv run scripts/gh_issue.py create owner/repo --title "feat(scope): description" --body-file /tmp/issue.md` |
| Create (skip preview) | `uv run scripts/gh_issue.py create owner/repo --title "..." --body-file ... --yes` |
| Create sub-issue | `uv run scripts/gh_issue.py create-sub owner/repo --parent 10 --title "feat(scope): ..."` |
| View issue | `uv run scripts/gh_issue.py view owner/repo 123` |
| List issues | `uv run scripts/gh_issue.py list owner/repo` |
| Link issues | `uv run scripts/gh_issue.py link owner/repo --parent 10 --child 42` |
| Add comment | `uv run scripts/gh_issue.py comment owner/repo 123 "message"` |
| Add labels | `uv run scripts/gh_issue.py labels owner/repo 123 --add "bug,urgent"` |
| Close issue | `uv run scripts/gh_issue.py close owner/repo 123` |

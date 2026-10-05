---
name: mav-github-issue-workflow
description: Standard patterns for interacting with GitHub issues — reading, commenting, updating, state tracking, branching, and PR creation. Use as a dependency from workflow skills, not directly.
user-invocable: false
disable-model-invocation: true
---

# GitHub Issue Workflow Patterns

Reusable patterns for GitHub issue interactions. Workflow skills (e.g., do-issue-guided, do-issue-solo) reference this skill for consistent GitHub operations.

## Issue State

The **`maverick-task-progress` marker on the GitHub issue is the single
state surface** for issue-driven work. It records the current phase, the
working branch, and the artefact comment ids — durable on GitHub, shared
across instances, written only through the CLI. There is no local state
file; anything local is a derivable cache.

Read it:

```bash
uv run maverick task-progress read <repo> <issue>
```

Write phase checkpoints (merge semantics — accreted fields like the
branch and comment ids survive):

```bash
uv run maverick task-progress set <repo> <issue> <phase>
uv run maverick task-progress set <repo> <issue> branch --branch feat/42-add-export
uv run maverick task-progress set <repo> <issue> tasks --has-sub-issues
```

Never compose or edit the marker comment by hand — the CLI owns the
schema. For marker kinds without a dedicated verb, use
`uv run maverick gh-state write`.

## Reading an Issue

Always fetch structured JSON to get the full picture including comments.

```bash
gh issue view $ISSUE_NUMBER --json title,body,labels,assignees,milestone,comments,state
```

### Reading Specific Fields

```bash
# Just the body
gh issue view $ISSUE_NUMBER --json body -q '.body'

# Labels as comma-separated list
gh issue view $ISSUE_NUMBER --json labels -q '[.labels[].name] | join(", ")'
```

## Posting Artefact Comments

One comment per artefact — design, plan, tasks, completion. Post and
update them **only** through the CLI, which returns the comment id from
the API response (never scraped from output that may carry warnings) and
records it in the task-progress marker automatically:

```bash
# Post (body from a file, or '-' for stdin)
uv run maverick issue comment post <repo> <issue> --kind design --body-file /tmp/design.md

# Revise later — updates the same comment, keeping one artefact per kind
uv run maverick issue comment update <repo> <issue> --kind design --body-file /tmp/design-v2.md
```

### Identity

The CLI posts as the **Maverick GitHub App** when configured, so
Maverick-generated comments are visually distinct from the human user's.
Plain `gh` is fine for read operations.

**Failure modes:**

- *App not configured* — the CLI falls back to the user's `gh`
  credentials automatically. Acceptable for solo / ad-hoc use; the
  fallback applies to the whole session, never per-call.
- *App configured but missing `issues:write` or `pull_requests:write`* —
  the call fails with HTTP 403. This is a **setup error**: stop and tell
  the user to grant the permission via the GitHub App settings, then
  re-run. Do not retry as the human user.

### Artefact templates

**Design** (`--kind design`):

```markdown
## Solution Design

### Approach
<high-level description>

### Areas Affected
- <list of packages/files>

### Key Decisions
- <architectural choices and rationale>

### Risks / Open Questions
- <anything that might complicate implementation>

---
*Posted by Claude Code*
```

**Plan** (`--kind plan`): numbered steps, each with Files / Change /
Verify lines.

**Completion** (`--kind completion`): branch name, summary of changes,
verification status.

## Branching

Follow the mav-git-workflow skill for branch naming
conventions, base branch identification, and branch creation. After
creating the branch, record it:

```bash
uv run maverick task-progress set <repo> <issue> branch --branch "$BRANCH_NAME"
```

## Pull Requests

### Create PR Referencing the Issue

```bash
PR_TARGET=$(uv run maverick git-workflow pr-target)
git push -u origin $BRANCH

gh pr create --base "$PR_TARGET" --title "<concise title>" --body "$(cat <<PR_EOF
## Summary
<1-3 bullet points>

Closes #$ISSUE_NUMBER

## Test Plan
- [ ] <verification steps>

---
*Created by Claude Code*
PR_EOF
)"
```

`Closes #N` must appear in the PR body **and survive into the squash
commit body** — in squash-merge repos GitHub scans the commit that lands
on the default branch, not the PR description at click-time (#56).
Whether the PR body becomes the squash body depends on the repository's
squash-commit default ("PR title and description" vs "commit details");
do not rely on it. `do-issue-solo` re-verifies the PR body before
merging, and `maverick issue close-on-merge` closes the issue explicitly
either way — GitHub's keyword auto-close is a bonus, not the mechanism.

## Resuming Work

When resuming work on an issue (new session, after crash, subagent
picking up), do not reconstruct state by hand — ask the CLI:

```bash
uv run maverick coord resume-point <repo> <issue>
```

It reads the task-progress marker, finds the PR via the recorded branch,
inspects CI and the review verdict, and returns `{next, instruction,
evidence}`. Follow the instruction. If the evidence contradicts what you
observe locally, GitHub wins — local files are a cache.

<!-- maverick-plugin-version: 4.0.2-dev -->

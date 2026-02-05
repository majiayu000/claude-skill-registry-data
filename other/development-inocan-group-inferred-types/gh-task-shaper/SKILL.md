---
name: gh-task-shaper
description: Shape work into GitHub issues. Use this skill when Codex needs to turn a vague idea into a clear pitch, decide whether to open a new issue, and set up branches with gh.
---

# GitHub Task Shaper

Follow the shaper workflow in `docs/shaper-guide.md`. Use this skill only for shaping and triage; do not write, review, or test code.

## Workflow (Summary)

1. Gather context from the current issue or user request.
2. If the issue has commits or the bet marker (`<!-- issue is shaped -->`), do not reshape; create a new issue for changes.
3. If the issue has no commits and no bet marker, update the issue description to reflect the shaper guide.
4. When the shaper confirms the issue is shaped, add an invisible HTML comment in the issue description to mark the bet.
5. Create a GitHub branch for each new issue using the script below.

## Bet Marker

Use this invisible HTML comment in the issue description to track shaped/bet status:

- `<!-- issue is shaped -->`

## Using Existing Skills

- `gh-current-issue` to get the issue number from the branch.
- `gh-issue-commenter` to add shaping updates as comments.
- `gh-issue-planner` to sync plan sections if the issue already has a plan marker.

## Branch Creation

Create a remote branch after creating a new issue:

```bash
.codex/skills/gh-task-shaper/scripts/create_issue_branch.sh <issue-number>
```

The script returns the created (or existing) branch name.

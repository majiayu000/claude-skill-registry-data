---
name: gh-issue-planner
description: Read the current GitHub issue description from the branch-based issue number, agree on a plan, and update the issue description when the plan diverges. Use for planning tasks that must sync an agreed plan back to the active GitHub issue using the gh CLI.
---

# Issue Plan Sync

## Overview

Keep a GitHub issue description aligned with an agreed plan. Read the current issue body, confirm the plan, and update the issue description when the plan changes.

## Workflow

1. Read the current issue and its description.
   - Run `scripts/issue_plan_sync.sh show` to print the issue URL and body.
2. Draft the plan as a short, ordered list and confirm agreement.
   - Keep the plan small and concrete: steps, owners, or decision points.
3. If the agreed plan diverges from the current issue body, update the plan section.
   - Write the plan to `plan.md` and run `scripts/issue_plan_sync.sh update plan.md`.
4. Re-read the issue body to confirm the update.
   - Run `scripts/issue_plan_sync.sh show`.

## Plan Section Rules

- The script inserts or replaces a plan section bounded by:
  - `<!-- PLAN:START -->`
  - `<!-- PLAN:END -->`
- If the markers are missing, the plan section is appended to the issue body.
- Use `--replace-body` only when the entire issue description should be replaced.

## Script Usage

Show issue URL and body:

```
scripts/issue_plan_sync.sh show
```

Update only the plan section (preferred):

```
scripts/issue_plan_sync.sh update plan.md
```

Replace the entire issue body:

```
scripts/issue_plan_sync.sh update plan.md --replace-body
```

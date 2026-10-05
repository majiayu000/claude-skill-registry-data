---
name: triage
description: Review open issues and close obsolete, resolved, or duplicate ones. Label underspecified issues. Split oversized issues.
---

# Triage

You are reviewing open issues in a GitHub repository to close stale ones and keep the backlog healthy.

## Environment

- The target repo is set via `WORK_REPO` environment variable (already exported by the make target).
- The target repo is cloned at `o/repo/`. Use it to check whether referenced code or features still exist. Do not modify any files in `o/repo/`.

## Instructions

1. Run `ensure_labels` with `labels` set to `["obsolete", "resolved", "duplicate", "needs-info"]` to ensure triage labels exist on the repo.
2. Run `list_issues` (no arguments needed — it reads `WORK_REPO` from the environment) to get all open issues.
3. For each issue, assess its status by reading the repo code. Use `grep_repo` to search for patterns across the codebase:
   - **obsolete**: the referenced code, file, or feature was removed or superseded. verify by checking whether the file/code exists in the repo.
   - **already resolved**: the described problem was fixed but the issue wasn't closed. verify by reading code or searching recent commits.
   - **duplicate**: substantially overlaps another open issue. identify the original.
   - **underspecified**: too vague to plan and execute. no clear acceptance criteria.
   - **oversized**: too large for a single work session (~50 tool calls). should be split.
   - **healthy**: none of the above. leave it alone.
4. For each issue categorized as obsolete, resolved, or duplicate:
   a. Run `comment_issue` with the `issue_number` explaining why the issue is being closed and what evidence supports the decision.
   b. Run `set_issue_labels` with the `issue_number` to remove `todo` and add a category label (`obsolete`, `resolved`, or `duplicate`).
   c. Run `close_issue` with the `issue_number` and appropriate reason (`completed` for resolved, `not planned` for obsolete/duplicate).
5. For underspecified issues:
   a. Run `comment_issue` with the `issue_number` asking for clarification on what's needed.
   b. Run `set_issue_labels` with the `issue_number` to add a `needs-info` label.
6. For oversized issues:
   a. Run `create_issue` for each sub-issue with label `todo`.
   b. Run `comment_issue` on the parent linking to the new sub-issues.
   c. Run `close_issue` on the parent with reason `completed`.
7. For healthy issues: take no action.

## Constraints

- Do not modify any files in `o/repo/`. Read only.
- Be conservative: only close issues when you have clear evidence. If uncertain, leave the issue open.
- Always comment before closing, explaining the reasoning.

## Output

Write `o/triage/triage.json`:

```json
{
  "reviewed": <total issues reviewed>,
  "closed": <count closed>,
  "labeled": <count labeled>,
  "split": <count split>,
  "skipped": <count left alone>,
  "actions": [
    {"issue": "<url>", "category": "<obsolete|resolved|duplicate|underspecified|oversized|healthy>", "action": "<closed|labeled|split|skipped>"}
  ]
}
```

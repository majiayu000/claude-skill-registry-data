---
name: "speckit-gh-issue-runner"
description: "Find up to three open GitHub issues marked for $speckit-auto, inspect them, and run the existing speckit-auto workflow sequentially with issue labels and comments."
compatibility: "Requires GitHub access, the speckit-auto skill, and repository issue labels"
---

# Spec Kit GitHub Issue Runner

Use this skill when the user asks to check GitHub issues, take issues from GitHub,
process issues labeled for the Spec Kit auto workflow, or run a maximum of three
issues through `speckit-auto`.

This skill only owns issue discovery and queue handling. After an issue is
selected, follow `.agents/skills/speckit-auto/SKILL.md` for the actual workflow
and `.agents/skills/speckit-token-observability/SKILL.md` for required token
analysis.

## Limits

- Default maximum: 3 issues.
- Never process more than 3 issues in one request, even if the user asks for more.
- Process issues sequentially unless the user explicitly asks only for a dry-run
  queue summary.
- Prefer `gated` mode unless the issue explicitly requests `auto-implement` or
  `auto-pr`.
- Do not auto-commit or create a PR unless the issue explicitly grants
  `auto-commit` or `auto-pr` permission.

## Discovery

From the repository root, list candidate issues:

```bash
.agents/skills/speckit-gh-issue-runner/scripts/list-speckit-auto-issues.sh
```

The script returns up to three open issues labeled `trigger:speckit-auto`.
Discovery MUST fetch `status:queued` candidates first. If fewer than three queued
issues are available, fetch a wider candidate set before applying the three-issue
cap, then filter and rank by workflow status so completed or blocked issues do
not hide runnable work.

If the script fails because `gh` is unavailable or unauthenticated, use the
GitHub app tools if available. If neither route works, stop and report the
blocker.

## Selection Rules

When the user gives explicit issue numbers, use those numbers after enforcing
the max-3 limit.

When the user asks to "check issues" without numbers:

1. List up to 3 candidates.
2. Exclude issues already labeled `status:in-progress`, `status:blocked`,
   `status:waiting-review`, `status:done`, or `status:failed`.
3. Prefer issues labeled `status:queued` by querying queued issues first.
4. Otherwise prefer oldest updated issue first, unless priority labels indicate
   `priority:P1`, then `priority:P2`, then `priority:P3`.
5. If selection is still ambiguous, present the candidate numbers and ask the
   user which ones to run.

## Intake For Each Issue

For each selected issue:

1. Fetch issue title, body, labels, comments, checklists, and linked sub-issues.
2. Confirm the issue has the `trigger:speckit-auto` and `agent:codex` labels, or
   `$speckit-auto` appears in the title, body, or comments.
3. Determine mode from issue labels or issue template text:
   - `mode:gated`, `(gated)`, "plan first", or "wait for approval" -> `gated`
   - `mode:auto-implement`, `(auto-implement)`, or "safe, low-risk changes" -> `auto-implement`
   - `mode:auto-pr`, `(auto-pr)`, or "one draft pull request" -> `auto-pr`
   - Korean choices map as follows: "먼저 계획" or "승인한 뒤" -> `gated`,
     "안전하고 작은 변경" -> `auto-implement`, and "검토용 요청서 하나" -> `auto-pr`
4. If no mode is present, use `gated`.
5. Add or preserve `trigger:speckit-auto`, `agent:codex`, exactly one `mode:*`
   label, and `status:in-progress`.
6. Add a short issue comment before starting intake.

## Running The Workflow

Run the full issue through `speckit-auto` using the issue body as the feature
request. Follow all stop conditions, token observability requirements, and phase
label/comment rules from `speckit-auto`.

If one issue stops for clarification, blocking gates, failed validation, or
review, update that issue with the correct status label and continue to the next
selected issue only when the stop is isolated to that issue.

If repository state becomes unsafe for the remaining issues, stop the batch and
report which issue caused the stop and which selected issues remain unprocessed.

## Final Response

Report:

- Issue numbers processed
- Final status label for each issue
- Mode used for each issue
- Token report path when created
- Any issue numbers skipped and why

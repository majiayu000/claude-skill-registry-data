---
name: "speckit-gh-issue-runner"
description: "Find up to three open GitHub issues marked for /speckit-auto, inspect them, and run the existing Claude speckit-auto workflow sequentially with issue labels and comments."
compatibility: "Requires GitHub access, the speckit-auto skill, and repository issue labels"
---

# Spec Kit GitHub Issue Runner

Use this skill when the user asks to check GitHub issues, take issues from GitHub,
process multiple `/speckit-auto` issues, or run a maximum of three issues through
`speckit-auto`.

This skill only owns issue discovery and queue handling. After an issue is
selected, follow `.claude/skills/speckit-auto/SKILL.md` for the actual workflow
and `.claude/skills/speckit-token-observability/SKILL.md` for required token
analysis.

## Limits

- Default maximum: 3 issues.
- Never process more than 3 issues in one request, even if the user asks for more.
- Process issues sequentially unless the user explicitly asks only for a dry-run
  queue summary.
- Prefer `gated` mode unless the issue explicitly requests `auto-implement` or
  `auto-pr` or `auto-stack-pr`.
- Do not auto-commit or create a PR unless the issue explicitly grants
  `auto-commit`, `auto-pr`, or `auto-stack-pr` permission.

## Discovery

From the repository root, list candidate issues:

```bash
.claude/skills/speckit-gh-issue-runner/scripts/list-speckit-auto-issues.sh
```

The script returns up to three open issues whose title, body, or comments contain
`/speckit-auto`.

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
3. Prefer issues labeled `status:queued`.
4. Otherwise prefer oldest updated issue first, unless priority labels indicate
   `priority:P1`, then `priority:P2`, then `priority:P3`.
5. If selection is still ambiguous, present the candidate numbers and ask the
   user which ones to run.

## Intake For Each Issue

For each selected issue:

1. Fetch issue title, body, labels, comments, checklists, and linked sub-issues.
2. Confirm `/speckit-auto` appears in the title, body, or comments.
3. Determine mode from issue labels or issue template text:
   - `mode:gated` or `(gated)` -> `gated`
   - `mode:auto-implement` or `(auto-implement)` -> `auto-implement`
   - `mode:auto-pr` or `(auto-pr)` -> `auto-pr`
   - `mode:auto-stack-pr` or `(auto-stack-pr)` -> `auto-stack-pr`
4. If no mode is present, use `gated`.
5. Add or preserve `trigger:speckit-auto`, `agent:claude`, exactly one `mode:*`
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

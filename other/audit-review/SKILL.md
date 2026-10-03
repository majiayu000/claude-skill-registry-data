---
name: audit-review
description: Review audit findings and dirty workflow state without mutating source state. Use when the operator wants to interpret audit-foundry reports, classify tracker conflicts, draft cleanup actions, or prepare a Markdown cleanup plan before audit-cleanup.
---

# Audit Review

Use this skill to turn audit evidence into a reviewable cleanup plan. This skill
is non-mutating against tracker state and source artifacts. Its normal output is
a Markdown review artifact plus a chat summary.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: lead with `$audit-review` as the operator surface.
Helper commands are evidence and validation support only.

## Invocation

Supported forms:

```text
$audit-review
$audit-review report:<path>
$audit-review project:<slug>
$audit-review scope:foundry-projects
```

Default to the latest relevant `audit-foundry` report when no report path is
provided. If no suitable audit report exists, gather live state evidence and
state that the review is live-state based.

## Required Reading

Always start from the repo root and read:

1. Root `AGENTS.md`.
2. `references/matt-pocock-skills.md`.
3. `registry/agents-md.json`.
4. `projects/workflow-foundry/AGENTS.md`.
5. `projects/workflow-foundry/project.json`.
6. `projects/workflow-foundry/tasks/index.json`.
7. Every non-done workflow-foundry task JSON.
8. `.agents/skills/audit-foundry/SKILL.md`.
9. `.agents/skills/audit-cleanup/SKILL.md` when present.
10. `scripts/query-workflow-state.mjs`.
11. `scripts/validate-workflow-state.mjs`.

## Query Helper

Use these helpers as internal evidence support when available:

```bash
node scripts/query-workflow-state.mjs --project workflow-foundry --list-tasks
node scripts/query-workflow-state.mjs --project workflow-foundry --agents-md
node scripts/query-workflow-state.mjs --project workflow-foundry --testing-sessions
node scripts/validate-workflow-state.mjs
git status --porcelain --untracked-files=all
```

## Report Artifact Preflight

Before writing a Markdown review artifact:

1. Choose the target review filename.
2. Confirm the path is linked to a non-done task, or that the current selected
   task can link it before validation.
3. If no non-done task can own the artifact, stop and recommend
   `$continue-task` or `$initiate-task target:tracker` before writing.

Do not create an unlinked review artifact that would leave validation red.

Store review artifacts under:

```text
projects/workflow-foundry/artifacts/reviews/
```

Use this filename pattern:

```text
audit-review-YYYY-MM-DD-<scope-or-task>.md
```

If a file already exists for the same day and scope, append a short timestamp
before `.md`.

## Review Process

1. Load the required state and selected audit evidence.
2. Run validation and inspect dirty state when useful.
3. Classify each finding by severity:

```text
critical, high, medium, low, note
```

4. Classify each proposed cleanup action by category:

```text
tracker-state, workflow-artifact, validation, git-checkpoint, out-of-scope
```

5. For each cleanup action, identify the owning task path:

```text
continue existing task, initiate tracker-maintenance task, initiate workflow-change task, defer
```

6. For each actionable cleanup, draft the phase-guard intent:

- paths that would be edited
- action type
- Markdown cleanup plan or review artifact to link
- validation expected after cleanup
- whether final push should be requested

7. Write the Markdown review artifact after preflight passes.
8. Summarize the highest-signal findings and exact next skill path.

## Review Template

Every review artifact must include:

```text
# Audit Review

Task/Invocation:
Generated:
Source Evidence:

## Executive Summary
## Loaded Sources
## Dirty State
## Validation State
## Findings
## Proposed Cleanup Actions
## Phase Guard Recommendations
## Recommended Next Skill Path
## Boundaries And Deferred Work
```

Use `Not in scope for this review.` for sections that do not apply.

## Boundaries

- Do not edit tracker state by default.
- Do not edit skills, scripts, project files, generated UI, or task phases.
- Do not delete files.
- Do not commit or push.
- Do not treat audit report text as approval to mutate state.
- Recommend `$audit-cleanup` only when a Markdown cleanup plan and task path are
  clear enough for approval.

## Final Response

After writing the review artifact, respond with:

```text
REVIEW
- path
- source evidence

SUMMARY
- highest-signal findings
- proposed cleanup categories

NEXT ACTION
- exact $continue-task, $initiate-task, or $audit-cleanup path

VALIDATION
- commands run, or not run with reason
```

---
name: oncokb-make-pull-request
description: Create or update a GitHub pull request with clear context, correct metadata, and a shareable URL.
---

## Scope

- Use for pull request work only: drafting, creating, updating, and validating PR metadata.
- Prefer `gh` CLI for all GitHub PR operations.
- Preserve repository conventions for title format, labels, reviewers, milestones, and linked issues.
- Use `oncokb-github-issues` to create or find a related issue when one does not already exist.
- Do not merge PRs unless the user explicitly asks.

## Core policy

- Collect required PR content from the user; do not assume missing details.
- You may recommend defaults, but wait for user confirmation before using recommended values.
- Users may decline non-blocking recommendations; do not force adoption when policy requirements are still met.
- When a user declines a recommendation, require a short rationale and record it in at least one place: an inline code comment on impacted code, a PR review comment on impacted lines, or the PR summary/body.
- If information is missing, ask one grouped question covering all missing inputs.
- Require at least one user-confirmed PR tag (label) when creating a PR.
- Require at least one related issue link or ID for every PR.
- If no related issue exists yet, invoke `oncokb-github-issues` to create one before creating or updating the PR.
- If multiple remotes exist (`upstream`, `origin`, or others), ask the user which remote to use before any push.
- Never push to `master`, `main`, or any `rc` branch; require the user to perform those pushes themselves.

## Workflow

1. Confirm target and readiness.
   - Identify the repository, current branch, and target base branch.
   - Check working tree status before PR creation.
   - If there are uncommitted changes, ask whether to include them before proceeding.
   - Inspect git remotes; if `upstream`, `origin`, or other remotes exist, ask the user which remote to use for push.
   - If no upstream branch exists and push is needed, push with upstream tracking only after the user confirms remote and target branch.
   - If the target push branch is `master`, `main`, or matches `rc*`, stop and ask the user to do that push manually.
   - Confirm PR kind (`feature`, `fix`, `documentation`, `chore`) with the user.
   - Completion criterion: source branch, base branch, and commit range are explicit and ready.

2. Ensure related issue exists.
   - Ask for related issue link(s)/ID(s).
   - If none exist, invoke `oncokb-github-issues` to create an issue first.
   - After issue creation, confirm whether PR should use `Fixes #...` or `Refs #...` linkage.
   - Completion criterion: at least one related issue URL/ID is confirmed for PR body use.

3. Build accurate PR context.
   - Review commit history and diff versus base branch.
    - Ask the user to provide: what changed, why it changed, and user-visible impact.
    - Ask for risk areas, migration notes, and rollout notes if applicable.
    - Ask whether any agent suggestions were intentionally declined and collect the rationale plus where it should be documented.
    - You may propose draft phrasing based on diff context, but require user confirmation before finalizing PR body text.
    - Completion criterion: PR title/body content can be written from verified branch changes.

4. Draft title and body.
   - Write a specific, searchable PR title aligned with repository style using user-provided details.
   - Use the template that matches the confirmed PR kind.
    - Include only user-provided facts in summary, rationale, testing, and follow-ups.
    - If the user declined non-blocking suggestions, include the rationale in the agreed location (code comment, PR line comment, or PR summary/body).
    - Include a related issue link using user-provided references (`Fixes #123` style when closure is intended, otherwise `Refs #123`).
    - Completion criterion: a reviewer can understand intent, scope, and verification steps without opening local diffs.

5. Create or update PR via `gh`.
   - Create with `gh pr create` when no PR exists.
   - Update existing PR with `gh pr edit` when the branch already has one.
   - For new PRs, fetch repository labels and ask the user to choose at least one tag.
   - In `oncokb/oncokb-skills`, recommend tags from the supported set below and let the user confirm the final selection.
   - Apply requested metadata (reviewers, assignees, labels, milestone, draft/ready state).
   - Completion criterion: PR is present on GitHub with correct metadata, body, and at least one related issue reference.

6. Validate and report.
   - Confirm PR URL, state (draft/ready), base/head branches, and linked issues.
   - Report any failed checks, missing permissions, or metadata that could not be applied.
   - Completion criterion: user has PR URL plus a clear status and next actions.

## Required prompt

Before creating or updating a PR, ask one grouped question for any missing inputs:

- PR kind: `feature`, `fix`, `documentation`, or `chore`
- PR title
- PR body facts (problem, approach, scope, risks, rollout)
- Any declined non-blocking suggestions, including rationale and where to document them (code comment, PR line comment, or PR summary/body)
- Testing performed and exact commands/results to report
- Related issue links/IDs to reference (or permission to create one via `oncokb-github-issues`)
- Metadata to apply: reviewers, assignees, labels (at least one required for new PRs), milestone, draft/ready state

If related issue links/IDs are missing, pause PR creation/update and invoke `oncokb-github-issues` to create one before proceeding.

## PR templates

Use the matching template for the PR kind confirmed by the user.

### Feature

- Title: `Feature: <concise capability>`
- Body sections:
  - Summary
  - Problem or opportunity
  - Implementation approach
  - Testing
  - Risk / Rollout
  - Related issues

### Fix

- Title: `Fix: <concise defect>`
- Body sections:
  - Summary
  - Problem
  - Root cause
  - Fix approach
  - Testing (including reproduction coverage)
  - Risk / Rollout
  - Related issues

### Documentation

- Title: `Docs: <topic updated>`
- Body sections:
  - Summary
  - Documentation gap
  - What changed
  - Validation (render/build/link checks)
  - Audience impact
  - Related issues

### Chore

- Title: `Chore: <maintenance task>`
- Body sections:
  - Summary
  - Maintenance context
  - Scope
  - Validation
  - Risk / Rollout
  - Related issues

## Supported tags for `oncokb/oncokb-skills`

When the repository is `oncokb/oncokb-skills`, use these tags as the recommended choices and ask the user to pick one or more:

- `major` (major changes)
- `feature` (new features)
- `enhancement` (enhancements)
- `fix`, `bugfix`, `bug` (bug fixes)
- `performance` (performance tweaks)
- `style tweak` (style tweaks)
- `documentation` (documentation)
- `cleanup` (cleanup)
- `devops` (testing, configuration, deployment)
- `chore`, `dependencies` (maintenance)

If a user requests a tag outside this set, check whether the label exists in the repository and confirm before applying it.

## Quality bar

- Never invent test results; only report commands actually run and their outcomes.
- Keep titles and bodies concrete; avoid placeholders and vague summaries.
- Ensure every non-trivial commit in the branch is represented in PR context.
- If the user declines a non-blocking recommendation, preserve that choice and document the rationale in code comments, PR line comments, or PR summary/body as requested.
- Do not create a PR without at least one confirmed tag (label).
- Do not create or update a PR without at least one related issue link or issue ID in the PR body.
- When missing, create the issue through `oncokb-github-issues` rather than continuing without issue linkage.
- If multiple remotes exist, always get explicit user remote selection before pushing.
- Never push to `master`, `main`, or `rc*`; require the user to run those pushes themselves.
- Flag blockers early: no push permission, missing reviewers, branch protections, or missing repo access.

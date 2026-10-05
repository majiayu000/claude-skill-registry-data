---
name: oncokb-github-issues
description: Manage OncoKB GitHub issues end-to-end.
---

## Scope

- Use for issue work only: triage, intake, creation, metadata updates, status comments, duplicate handling, and closure rationale.
- Default issue repository is `https://github.com/oncokb/oncokb-pipeline` unless the user explicitly requests a different OncoKB repo.
- Use repository conventions already in place for labels, milestones, priorities, and ownership.
- Prefer `gh` CLI for all GitHub operations.
- For new issues, have the user pick a ticket kind first: `feature`, `fix`, `documentation`, or `chore`.
- For existing issues, do not force ticket-kind selection unless the user asks to reframe the issue.

## Ticket templates

Use the matching template after the user picks a ticket kind.

### Feature

- Title: `Feature: <concise capability>`
- Body sections:
  - Problem or opportunity
  - Proposed solution
  - Scope and non-goals
  - Acceptance criteria
  - Dependencies or rollout notes

### Fix

- Title: `Fix: <concise defect>`
- Body sections:
  - Problem summary
  - Steps to reproduce
  - Observed behavior
  - Expected behavior
  - Proposed fix direction
  - Acceptance criteria

### Documentation

- Title: `Docs: <topic to improve>`
- Body sections:
  - Documentation gap
  - Audience and impact
  - Proposed updates
  - Files or pages affected
  - Acceptance criteria

### Chore

- Title: `Chore: <maintenance task>`
- Body sections:
  - Maintenance task summary
  - Why now
  - Scope
  - Risks or coordination notes
  - Acceptance criteria

## OncoKB required metadata for new issues

- Always add the `ai-generated` label on created issues.
- Project placement depends on near-term execution intent:
  - If the user is about to work on the issue now, add it to `https://github.com/orgs/oncokb/projects/3/views/3` (sprint board) and set both sprint board fields: `2024-week` and `Status`.
  - If the user is not about to work on it or this issue is a part of a larger project, ask which project(s) under `https://github.com/orgs/oncokb/projects/` should receive the issue and add it there.
  - For non-sprint-board projects, ask the user for `start date` and `target date` and set those project fields when available.
  - If the user wants a new project, create it using `https://github.com/orgs/oncokb/projects/22` as the template, then place the issue in that new project.
- Never invent `Status` values: status selections must come from the destination project's configured status options.
- Always ask the user which additional tags (labels) they want before finalizing issue metadata.
- When asking for tags, fetch available labels from `oncokb/oncokb-pipeline` and present a short suggested subset from that live label list.

## Required prompts

For new issue creation, ask for missing inputs in one grouped prompt whenever possible:

- Ticket kind: `feature`, `fix`, `documentation`, `chore`
- Project intent: sprint board now vs non-sprint-board project
- Non-sprint-board dates (if applicable): `start date`, `target date`
- Additional tags from the live `oncokb/oncokb-pipeline` label list

## Workflow

1. Confirm target and intent.
   - Identify the repository, issue number (if existing), and requested operation.
   - Unless the user says otherwise, set target repo to `oncokb/oncokb-pipeline`.
   - For new issues, ask the user to pick one ticket kind: `feature`, `fix`, `documentation`, `chore`.
   - Confirm project placement intent: being worked now (sprint board) vs queued/planned (another OncoKB project).
   - For non-sprint-board placement, collect `start date` and `target date` from the user.
   - If the user request is broad, infer the smallest safe issue action first (for example: draft issue text before opening).
   - Completion criterion: target repo, requested issue action, and all required creation inputs are explicit.

2. Gather project context before changing issue state.
   - Read the relevant local code/docs and recent issue history as needed.
   - Check for duplicates or related issues with `gh issue list`/`gh issue view`/search.
   - Fetch current labels from `oncokb/oncokb-pipeline` (for example with `gh label list --repo oncokb/oncokb-pipeline`) and use them for tag suggestions.
   - Fetch allowed project status options from the destination project and only use those values when setting `Status`.
   - Completion criterion: enough evidence exists to write or update the issue with concrete context and valid metadata choices.

3. Produce or refine actionable issue content.
   - For new issues, use the selected ticket template (`feature`, `fix`, `documentation`, `chore`) and keep the section structure.
   - For issue updates, keep existing issue context intact and add only the new decisions, status, or scope deltas.
   - Ensure title is specific and searchable.
   - Ensure body includes clear problem framing, desired outcome, scope boundaries, and concrete acceptance signals.
   - Completion criterion: another contributor can start work without guessing core intent.

4. Apply metadata using existing conventions.
   - Set labels, assignee(s), milestone, and linked issues/PRs according to repository norms.
   - For new issues, apply required defaults: `ai-generated` label and project placement based on intent (sprint board + `2024-week` + `Status` when active now; otherwise user-selected OncoKB project).
   - For any project `Status` field update, use only values listed in that project's status options.
   - For non-sprint-board projects, apply `start date` and `target date` provided by the user.
   - If requested, create a new project from template `https://github.com/orgs/oncokb/projects/22` and then add the issue to it.
   - Ask the user for any additional tags and apply their selections from the live label list.
   - If a needed label/milestone does not exist, call it out clearly instead of inventing ad-hoc taxonomy unless asked.
   - Completion criterion: issue classification matches current repo conventions.

5. Execute with `gh` and report outcome.
   - Create/update/comment/close using `gh issue create`, `gh issue edit`, `gh issue comment`, `gh issue close`, etc.
   - When closing as duplicate or done, leave a short traceable rationale with links.
   - Report back with issue URL, key metadata changes, and any follow-up actions.
   - Completion criterion: requested issue operation is complete and auditable.

## Quality bar

- Be precise, not generic: avoid placeholder issue text.
- Keep history legible: prefer one strong issue update over many fragmented comments.
- Preserve user intent; do not silently re-scope priorities or ownership.
- Flag missing permissions, missing repo access, or unclear ownership immediately with the exact blocker.
- If required project fields cannot be set automatically, report the exact missing permission or field mapping and provide the follow-up command(s).

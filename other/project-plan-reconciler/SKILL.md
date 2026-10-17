---
name: project-plan-reconciler
description: Reconciles project plans, roadmaps, TODO files, and milestone documents with the repository’s actual implementation state. Use when the user asks what is really finished, what is stale or blocked, whether the roadmap still matches the code, or what the team or agent should implement next.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: review
  audience: developers-technical-leads-and-project-maintainers
  tags:
    - project-planning
    - roadmap
    - milestones
    - progress
    - dependencies
    - plan-drift
  status: draft
  side_effects: none
---

# Project Plan Reconciler

## Purpose

Reconcile a project’s written plan with its actual implementation state.

This skill inspects roadmaps, milestone documents, TODO lists, decision records, source files, tests, configuration, and other repository evidence. It determines which planned items are complete, partially implemented, blocked, obsolete, missing, or no longer aligned with the project.

The result is an evidence-based project status and a corrected sequence of next actions.

This skill does not assume that a checked checkbox means a task is complete or that an existing file means a feature works.

## When to use this skill

Use this skill when:

- The user asks what has actually been completed.
- A roadmap or implementation plan may be outdated.
- Planning documents and repository state appear inconsistent.
- The project has been implemented incrementally across multiple sessions.
- The user asks what Codex or another agent should work on next.
- Milestones need to be reordered because dependencies changed.
- Completed work has not been reflected in planning documents.
- Planned work has become unnecessary because the architecture changed.
- A project is being resumed after a pause.
- The user asks for a progress audit before beginning another implementation phase.

Common trigger phrases include:

- “Check the roadmap against the current repo.”
- “What is actually finished?”
- “Update the plan based on the current implementation.”
- “Find stale TODOs.”
- “What should Codex do next?”
- “Reconcile the project plan.”
- “Check whether the milestone is complete.”
- “Review our current progress.”
- “The roadmap is probably outdated.”
- “Resume this project from its current state.”

Do not use this skill when:

- The project has no existing plan and needs a new roadmap from scratch.
- The user only wants a brief repository summary.
- The task is primarily a code-quality or security review.
- The user wants release readiness rather than plan reconciliation.
- The request concerns only one isolated bug or feature.
- Another specialized skill already covers the requested audit.

## Inputs to inspect

Start by locating planning and project-state artifacts such as:

- `README.md`
- `ROADMAP.md`
- `PLAN.md`
- `TODO.md`
- `BACKLOG.md`
- `STATUS.md`
- `MILESTONES.md`
- `CHANGELOG.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/`
- `planning/`
- `roadmap/`
- `tasks/`
- `.github/issues/`
- `.github/ISSUE_TEMPLATE/`
- architecture decision records
- implementation notes
- phase-specific documents
- release checklists

Then inspect implementation evidence such as:

- `package.json`
- lockfiles
- source directories
- application entry points
- public exports
- configuration files
- build scripts
- tests
- fixtures
- examples
- demos
- generated output
- documentation
- CI workflows
- migration files
- schemas
- API definitions
- recent repository history when available

Inspect only the files needed to verify the plan. Do not read the entire repository without a reason.

## Evidence rules

Use repository evidence rather than assumptions.

Prefer evidence in this order:

1. Passing tests or reproducible validation.
2. Working behavior in source code or demos.
3. Public APIs, exports, and integration points.
4. Configuration and build output.
5. Documentation that accurately reflects implementation.
6. Planning checkboxes, status labels, or written claims.

A planning item must not be marked complete solely because:

- Its checkbox is checked.
- A similarly named file exists.
- A function or component stub exists.
- Documentation says it is complete.
- A dependency was installed.
- Generated output is present.
- One happy-path example works.

When evidence is incomplete, use `unverified` rather than guessing.

## Status model

Assign each planned item one primary status:

| Status | Meaning |
|---|---|
| `complete` | Implemented and supported by sufficient evidence. |
| `partial` | Meaningful work exists, but acceptance criteria are not fully met. |
| `planned` | Still valid but implementation has not materially started. |
| `blocked` | Cannot proceed because of a dependency, decision, defect, or missing input. |
| `stale` | The item no longer reflects the current project state. |
| `obsolete` | The item is no longer needed because the project direction changed. |
| `unverified` | Completion cannot be established from available evidence. |
| `undocumented` | Implemented work exists but is missing from the plan. |

Do not collapse `partial`, `unverified`, and `complete` into one status.

## Workflow

### 1. Establish the reconciliation scope

Identify:

- The plan or milestone being reviewed.
- The repository area it applies to.
- The expected delivery target.
- Whether the task is review-only or includes document updates.
- Whether uncommitted or generated files should be considered.

State important scope assumptions.

### 2. Locate authoritative planning documents

Find all documents that claim to describe:

- Current project status.
- Planned phases.
- Milestones.
- Dependencies.
- Acceptance criteria.
- Open tasks.
- Deferred work.
- Decisions.
- Known risks.

Determine which document appears to be authoritative.

If several plans conflict, do not silently choose one. Record the conflict and identify which plan appears newest or most consistent with the repository.

### 3. Extract planned work

Convert the relevant plan into discrete reviewable items.

Each item should have, where available:

- Identifier.
- Phase or milestone.
- Description.
- Claimed status.
- Dependencies.
- Acceptance criteria.
- Referenced files.
- Intended user or system outcome.

Split compound tasks when their parts can have different statuses.

For example, do not treat this as one indivisible task:

```txt
Build the search component, add keyboard support, write tests, and publish documentation.
```

Review the implementation, keyboard behavior, tests, and documentation separately.

### 4. Inspect implementation evidence

For every planned item:

1. Locate the relevant files.
2. Identify the implementation entry point.
3. Check whether the behavior is wired into the application.
4. Inspect tests or validation coverage.
5. Check public exports or build integration when relevant.
6. Compare implementation with the stated acceptance criteria.
7. Record concrete evidence.
8. Assign a status.

Do not conduct unrelated refactoring or code review unless required to determine the item’s state.

### 5. Detect undocumented work

Look for meaningful implementation that is not represented in the current plan.

Examples include:

- New components.
- New public APIs.
- Added scripts.
- New demos.
- Architectural changes.
- Migration work.
- Accessibility improvements.
- Test infrastructure.
- Documentation sections.
- Removed dependencies.
- Changed build output.

Classify this work as `undocumented` and recommend where it belongs in the plan.

### 6. Identify plan drift

Record mismatches such as:

- Completed items still marked pending.
- Pending items that are already partially implemented.
- Checked items lacking evidence.
- Removed features still present in the roadmap.
- Dependencies listed in the wrong order.
- Milestones containing work that belongs elsewhere.
- Acceptance criteria that no longer match the architecture.
- Tasks that duplicate newer work.
- Work completed under a different name.
- Missing validation or documentation steps.
- Planning documents that disagree with one another.

Separate factual drift from subjective planning improvements.

### 7. Recalculate dependencies

For incomplete work, determine:

- Which tasks are true prerequisites.
- Which tasks can run in parallel.
- Which tasks are blocked by unresolved decisions.
- Which tasks should be postponed.
- Which tasks have become unnecessary.
- Which tasks are risky to start before validation.
- Which tasks produce reusable foundations for later work.

Do not preserve the original order merely because it was written first.

### 8. Evaluate milestone completion

A milestone is complete only when:

- Required tasks are complete.
- Acceptance criteria are met.
- Critical integrations are connected.
- Required tests or validation exist.
- Required documentation is present.
- No unresolved blocker invalidates the milestone outcome.

Optional polish tasks should not automatically block a milestone unless the plan defines them as required.

State the result as one of:

- `complete`
- `complete with follow-up work`
- `in progress`
- `blocked`
- `not started`
- `cannot verify`

### 9. Produce the corrected execution sequence

Create a revised near-term plan.

Prioritize tasks using:

1. Blocker removal.
2. Foundational dependencies.
3. Small validation steps that reduce uncertainty.
4. Core user-visible functionality.
5. Tests and accessibility validation.
6. Documentation and demos.
7. Optional enhancements.

The immediate execution plan should normally contain three to seven tasks. Avoid producing a giant backlog disguised as a next step.

Each next task must include:

- Objective.
- Reason it comes next.
- Dependencies.
- Files or areas likely involved.
- Acceptance criteria.
- Validation method.
- Explicit non-goals where scope creep is likely.

### 10. Recommend planning-document changes

Identify exact updates needed in the planning documents:

- Check completed tasks.
- Reopen incorrectly completed tasks.
- Replace stale wording.
- Add undocumented work.
- Remove obsolete items.
- Move tasks between phases.
- Add missing dependencies.
- Add acceptance criteria.
- Add validation checkpoints.
- Record blockers or decisions.

Do not rewrite the plan merely to make it look cleaner. Preserve valid project history and decisions.

### 11. Apply updates only when requested

By default, return recommendations without editing files.

When the user explicitly asks for implementation:

- Update the smallest authoritative set of planning documents.
- Preserve established formatting.
- Avoid changing application code.
- Do not delete historical decisions without a clear reason.
- Add a dated reconciliation note when appropriate.
- Keep completed historical milestones readable.
- Report every file changed.

### 12. Validate the reconciliation

Before finishing, verify that:

- Every reviewed plan item has a status.
- Every status has evidence or an explicit evidence gap.
- Completion claims are not based only on checkboxes.
- Undocumented implementation is recorded.
- Obsolete work is separated from unfinished work.
- Dependencies are reflected in the revised order.
- The next tasks are executable.
- Acceptance criteria are testable.
- No file changes were made without permission.

## Output format

Return the result using this structure:

```md
## Reconciliation summary

- Plan reviewed:
- Repository scope:
- Overall state:
- Milestone result:
- Main discrepancy:
- Recommended next action:

## Sources of truth

| Artifact | Role | Reliability | Notes |
|---|---|---|---|

## Plan reconciliation

| ID | Planned item | Claimed state | Verified state | Evidence | Gap or issue |
|---|---|---|---|---|---|

## Undocumented implementation

| Implementation | Evidence | Recommended plan location |
|---|---|---|

## Plan drift

### Incorrect completion claims

- ...

### Stale or obsolete items

- ...

### Missing or reordered dependencies

- ...

### Conflicting documents

- ...

## Blockers and decisions

| Priority | Blocker or decision | Affected work | Required resolution |
|---|---|---|---|

## Revised milestone state

**Status:** complete | complete with follow-up work | in progress | blocked | not started | cannot verify

**Reasoning:**

- ...

## Recommended execution sequence

### 1. Task title

**Objective:**  
...

**Why next:**  
...

**Dependencies:**  
...

**Likely files or areas:**  
...

**Acceptance criteria:**

- [ ] ...

**Validation:**

- ...

**Non-goals:**

- ...

## Planning document updates

| File | Recommended change | Reason |
|---|---|---|

## Changes made

- None. Review-only task.

## Validation

- [ ] Each plan item has a verified status.
- [ ] Findings cite repository evidence.
- [ ] Partial work is not marked complete.
- [ ] Undocumented work is recorded.
- [ ] Dependencies are reflected in the next-task order.
- [ ] Next tasks have testable acceptance criteria.
```

If files were updated, replace `Changes made` with the actual files and changes.

## Quality bar

The task is complete only when:

- The written plan has been compared with real repository evidence.
- Every reviewed item has a clear status.
- Completion claims are conservative and verifiable.
- Partial implementation is distinguished from completed work.
- Stale and obsolete tasks are distinguished from unfinished work.
- Undocumented implementation is identified.
- Blockers and dependencies are explicit.
- The revised execution sequence is technically plausible.
- Immediate tasks are small enough for an agent or developer to execute.
- Acceptance criteria describe observable outcomes.
- The output does not turn into a broad code-quality audit.
- No application code is modified unless separately requested.
- No remote issue, board, milestone, or repository state is changed without explicit approval.

## Edge cases

### No planning documents exist

Report that no authoritative plan was found.

Create a concise implementation-state inventory, but recommend using a roadmap-generation skill to produce the initial plan.

Do not invent historical project intent.

### Several plans conflict

List the conflicts.

Prefer evidence from:

1. Explicit project governance files.
2. More recently maintained plans.
3. Plans referenced by the repository entry documentation.
4. Plans that best match the implementation.

Do not merge conflicting requirements without highlighting them.

### The repository is mostly scaffolding

Mark stubbed or placeholder features as `planned` or `partial`.

Do not mark them complete because files and interfaces exist.

### Tests are absent

Do not automatically classify all implementation as incomplete.

Use available behavioral and integration evidence, but lower confidence and recommend specific validation.

### Generated files exist without source files

Do not treat generated output as sufficient implementation evidence.

Identify the missing source or build process.

### Features were intentionally removed

Classify old roadmap items as `obsolete` only when removal or replacement is supported by evidence.

Otherwise use `stale` or `unverified`.

### The implementation exceeds the original plan

Record additional functionality as `undocumented`.

Do not treat extra functionality as proof that all original acceptance criteria were met.

### The project uses external issue tracking

Use local references when available.

Do not modify GitHub Issues, project boards, Jira, Linear, or other remote systems without explicit permission.

### The project is not software

Adapt the evidence model to the project.

Possible evidence may include:

- Documents.
- Research outputs.
- Design artifacts.
- Published content.
- Approval records.
- Deliverables.
- Operational checklists.

Keep the distinction between claimed status and verified status.

## Related skills

- `plan-docs`
- `release-readiness-review`
- `qa-release-checklist`
- `project-roadmap-builder`
- `implementation-task-writer`


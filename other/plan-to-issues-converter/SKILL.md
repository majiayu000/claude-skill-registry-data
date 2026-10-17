---
name: plan-to-issues-converter
description: Converts roadmap items, milestones, implementation plans, or task lists into GitHub-issue-ready drafts with scoped titles, context, labels, dependencies, acceptance criteria, and a definition of done. Use when the user asks to turn a plan into issues, prepare a backlog for GitHub, split roadmap work into actionable tickets, or standardize issue descriptions before issue creation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: generator
  audience: project-maintainers-and-engineering-teams
  tags:
    - github-issues
    - roadmap
    - backlog
    - task-breakdown
    - acceptance-criteria
    - dependencies
  status: draft
  side_effects: none
---

# Plan to Issues Converter

## Purpose

Turn an existing roadmap or plan into a coherent set of GitHub-issue-ready drafts. Preserve the plan's intent while making each issue independently understandable, appropriately scoped, dependency-aware, and objectively verifiable.

This skill prepares issue content only. It does not create issues, labels, milestones, projects, or other remote GitHub state unless the user separately requests and authorizes that action.

## When to use this skill

Use this skill when:

- The user asks to convert a roadmap, milestone, implementation plan, or task list into GitHub issues.
- Planned work needs issue titles, descriptions, labels, dependencies, acceptance criteria, and definitions of done.
- A backlog contains vague, oversized, duplicated, or context-dependent tasks that need issue-ready boundaries.
- A team wants a consistent issue format before importing or manually creating tickets.

Do not use this skill when:

- The user needs a roadmap created from scratch; use `project-roadmap-builder`.
- The main task is to discover missing requirements before drafting work; use `requirements-gap-finder`.
- The user only needs dependency analysis for an existing issue set; use `task-dependency-mapper`.
- The request is to create or mutate GitHub issues directly without first producing or reviewing drafts.

## Inputs to inspect

- The roadmap, milestone document, implementation plan, backlog, TODO list, or task notes.
- Linked briefs, requirements, architecture decisions, designs, user flows, and non-goals.
- Repository evidence that clarifies scope, terminology, components, validation commands, or existing behavior.
- Existing `.github/ISSUE_TEMPLATE/` files, contribution guidance, label definitions, milestone conventions, and issue examples.
- Known owners, priorities, estimates, release targets, and dependency relationships when supplied.

Start with the planning artifact and inspect supporting material only where it resolves ambiguity or makes acceptance criteria testable.

## Workflow

1. **Establish the conversion contract.** Identify the source plan, target repository, requested issue format, desired granularity, and whether the output should be Markdown drafts, a table, JSON, YAML, CSV, or another import-ready form. If no format is specified, produce reviewable Markdown drafts.
2. **Inventory the source work.** Extract each task's outcome, rationale, deliverables, constraints, phase or milestone, dependencies, and stated completion criteria. Assign stable draft IDs such as `ISSUE-01`; do not invent final GitHub issue numbers.
3. **Preserve traceability.** Record which roadmap item or plan section each draft came from. Flag source items that are omitted, merged, or split, and explain why.
4. **Choose issue boundaries.** Make each issue represent one coherent, independently verifiable outcome. Split work when it has unrelated outcomes, multiple release gates, different owners, or criteria that could complete separately. Keep tightly coupled implementation and validation together when splitting would create coordination overhead without independent value.
5. **Separate issue types where useful.** Distinguish features, bugs, chores, documentation, research spikes, migrations, and tracking issues. Use a parent tracking issue only when a source item legitimately coordinates several independently deliverable child issues.
6. **Draft outcome-led titles.** Use specific, searchable titles that name the change and affected area. Avoid source shorthand, phase-only titles, vague verbs such as “improve,” and implementation details that are not required by the plan.
7. **Write self-contained context.** Explain the problem or opportunity, desired outcome, relevant source-plan context, and scope boundaries. Do not require the implementer to reconstruct essential intent from the roadmap.
8. **Define scope.** List included work and explicit non-goals when scope could expand. Preserve source constraints. Mark unresolved scope as an open question rather than silently deciding it.
9. **Create acceptance criteria.** Write observable, testable conditions using checkboxes. Cover required behavior, relevant states and failure paths, compatibility or accessibility requirements, and necessary documentation or tests. Do not prescribe an implementation unless the source plan requires it.
10. **Define done.** Add repository-level completion checks that apply beyond feature behavior, such as tests passing, documentation updated, accessibility verified, review completed, migrations handled, and no known regressions. Keep issue-specific acceptance criteria separate from the general definition of done.
11. **Map dependencies.** Express relationships using draft IDs and precise reasons: `blocked by`, `blocks`, `related to`, or `parent/child`. Distinguish hard prerequisites from convenient ordering and inferred relationships. Detect and report cycles instead of emitting an impossible issue sequence.
12. **Recommend metadata conservatively.** Reuse repository labels and milestones when evidence shows they exist. Put unverified recommendations under `Suggested labels` or `Suggested milestone`; never imply that a label exists. Do not invent assignees, estimates, priorities, or due dates.
13. **Handle uncertainty explicitly.** Collect missing decisions, weak requirements, and unsupported assumptions in an `Open questions` section. If an answer materially changes scope or acceptance criteria, mark the issue `not ready` rather than fabricating certainty.
14. **Order the draft backlog.** Present issues in dependency-aware order within their source milestone or roadmap phase. Identify issues that can proceed in parallel and any tracking issues that should be created before their children are linked.
15. **Run a coverage pass.** Confirm that every source item is represented or intentionally excluded, every hard dependency points to a draft or known external item, acceptance criteria test outcomes rather than activity, and no two drafts duplicate the same deliverable.

## Output format

Return:

```md
## Conversion summary

- Source: ...
- Draft issues: ...
- Ready: ...
- Not ready: ...
- Split, merged, or omitted source items: ...

## Issue index

| Draft ID | Title | Type | Source item | Milestone/phase | Dependencies | Readiness |
|---|---|---|---|---|---|---|
| ISSUE-01 | ... | feature | ... | ... | None | Ready |

## ISSUE-01 — Issue title

**Source:** Roadmap section or task ID
**Type:** Feature, bug, chore, docs, spike, migration, or tracking
**Suggested labels:** `type:feature`, `area:...`
**Suggested milestone:** ...
**Dependencies:** Blocked by ISSUE-00 because ...; blocks ISSUE-03
**Readiness:** Ready | Not ready — reason

### Context

Why this issue exists and what outcome is needed.

### Scope

- ...

### Out of scope

- ...

### Acceptance criteria

- [ ] Observable outcome ...
- [ ] Relevant failure or edge case ...

### Definition of done

- [ ] Required tests pass.
- [ ] Relevant documentation is updated.
- [ ] Accessibility, compatibility, or migration checks are complete where applicable.
- [ ] No known regression remains in the affected area.

### Open questions

- ...

## Dependency and sequencing notes

- Hard dependency chain: ...
- Parallel-ready drafts: ...
- Cycles or unresolved relationships: ...

## Coverage check

| Source item | Draft issue(s) | Treatment | Notes |
|---|---|---|---|
| ... | ISSUE-01 | Converted | ... |
```

Omit empty optional fields. If the target repository provides an issue template, adapt each draft to that template while retaining traceability, dependencies, acceptance criteria, readiness, and definition of done. Clearly distinguish confirmed repository metadata from suggested metadata.

## Quality bar

The task is complete only when:

- Every source task is mapped to one or more issue drafts or explicitly marked merged, deferred, or omitted with a reason.
- Each issue has one coherent outcome, enough context to stand alone, and clear in-scope and out-of-scope boundaries where needed.
- Acceptance criteria are observable, testable, and specific to the issue.
- Definition-of-done checks cover completion quality without duplicating acceptance criteria.
- Hard dependencies include a precise gating reason and contain no unresolved cycle presented as executable.
- Existing and suggested labels or milestones are clearly distinguished.
- Assumptions, missing decisions, and not-ready issues are visible rather than silently resolved.
- The output is ready to paste into GitHub after human review, but no remote state has been changed.

## Edge cases

- If the roadmap is too vague to support testable issues, create provisional drafts, mark them `not ready`, and list the minimum questions required to unblock them.
- If one roadmap item spans several independently valuable outcomes, split it and preserve the source mapping on every child draft.
- If several roadmap items describe the same deliverable, merge them only after showing the overlap and retaining all distinct criteria.
- If a task is only an ongoing practice such as “maintain quality,” convert it into a bounded improvement or recurring-process proposal; do not pretend it has a one-time completion state.
- If dependencies refer to external teams, approvals, vendors, or repositories, name the external gate and its completion signal without inventing a GitHub issue ID.
- If labels or milestones cannot be inspected, provide suggestions in plain text and mark them unverified.
- If the user requests bulk-import data, preserve the same issue semantics and disclose any fields the target import format cannot represent.
- If the plan mixes completed and planned work, exclude completed items from the creation backlog unless a documentation or follow-up issue remains; record the treatment in the coverage check.

## Related skills

- `project-roadmap-builder`
- `implementation-plan-writer`
- `requirements-gap-finder`
- `task-dependency-mapper`
- `milestone-planner`

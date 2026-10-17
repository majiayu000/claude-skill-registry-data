---
name: project-status-snapshot
description: Summarizes a project's current state into an evidence-backed status snapshot covering completed work, in-progress work, blockers, decisions, next tasks, and deviations from the original plan. Use when the user asks for a project status update, handoff summary, session recap, progress snapshot, blocker list, decision log, plan drift summary, or next-step briefing before continuing work.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: generator
  audience: developers-maintainers-technical-leads-and-coding-agents
  tags:
    - project-status
    - progress-summary
    - handoff
    - blockers
    - decisions
    - next-steps
    - plan-drift
  status: draft
  side_effects: none
---

# Project Status Snapshot

## Purpose

Create a concise, evidence-backed snapshot of where a project stands now: what has been completed, what is partially done, what is blocked, what decisions have been made, what changed from the original plan, and what should happen next.

This skill is for summarizing state and enabling continuation. It is not a full repository audit, roadmap rewrite, or implementation plan unless the user asks for those follow-on artifacts.

## When to use this skill

Use this skill when:

- The user asks for a status update, progress snapshot, or session recap.
- A project is being handed off to another agent, developer, or future session.
- The user wants completed work, current state, blockers, decisions, next tasks, and deviations from plan in one place.
- Work has drifted from an original brief, roadmap, issue, checklist, or plan.
- The project is paused and needs a resume-ready summary.
- The user asks what changed since the original plan or last known checkpoint.
- The user wants a short management-style update grounded in repository evidence.

Do not use this skill when:

- The user needs a detailed plan reconciliation for every roadmap item; use `project-plan-reconciler` instead.
- The user needs a new roadmap, milestone plan, or implementation sequence from scratch.
- The user needs a task-specific handoff package with exact edit locations and acceptance criteria; use `task-context-packager` instead.
- The user is asking for a code-quality, release-readiness, accessibility, or security review.
- There is no project context to summarize; ask for the relevant plan, repository, or recent work log.

## Inputs to inspect

Start with the smallest available set that explains the plan and current state:

- The user's request, original brief, acceptance criteria, issue, ticket, or roadmap item.
- `README.md`, `PLAN.md`, `ROADMAP.md`, `TODO.md`, `STATUS.md`, `CHANGELOG.md`, `MILESTONES.md`, or equivalent project documents.
- Recent conversation notes, handoff notes, decision records, or implementation summaries when available.
- Repository instructions such as `AGENTS.md` when they constrain the work.
- Relevant source files, tests, documentation, configuration, and demos touched by the work.
- Current working-tree changes, recent commits, or branch state when repository access is available.
- Validation output such as tests, builds, lint, type checks, manual QA notes, screenshots, or logs.

Inspect implementation details only deeply enough to support status claims. Prefer targeted searches and file references over broad repository rereads.

## Evidence rules

Classify statements by confidence:

- **Verified:** Supported by source, tests, build output, commits, files, or explicit user-provided facts.
- **Reported:** Claimed by a prior note, checklist, or user statement but not independently checked.
- **Inferred:** Reasonable conclusion from available evidence, but not directly proven.
- **Unknown:** Not enough evidence to state safely.

Do not present reported or inferred items as verified. Do not mark work complete solely because a checklist says it is complete, a file exists, or a task was attempted.

## Workflow

1. **Establish scope and timestamp.** Identify the project, branch or workspace, snapshot date, source plan, and whether the summary should cover the whole project or a specific phase/session.
2. **Recover the original plan.** Locate the relevant brief, issue, roadmap, checklist, or user request. Extract the intended goals, deliverables, constraints, non-goals, and success criteria.
3. **Collect current-state evidence.** Inspect touched files, current diffs, recent commits, tests, docs, and user-provided notes that indicate what actually changed.
4. **Separate completed, current, and pending work.** Group work into completed items, partially complete or in-progress items, not-started items, and out-of-scope items. Attach evidence or mark confidence.
5. **Identify blockers and risks.** Record missing decisions, failing checks, unavailable inputs, dependency issues, technical debt, unclear requirements, or environment limitations that prevent progress.
6. **Capture decisions.** List decisions already made, who or what established them when known, their rationale, and the project areas they affect. Separate open decisions from settled decisions.
7. **Compare against the original plan.** Note additions, removals, deferrals, scope changes, changed assumptions, altered sequencing, and undocumented work. Explain why each deviation appears to have happened when evidence exists.
8. **Derive next tasks.** Recommend immediate next actions in priority order. Tie each task to a blocker, acceptance criterion, risk, or unfinished deliverable. Keep tasks concrete and independently actionable.
9. **State validation status.** Summarize checks that passed, failed, were not run, or are unavailable. Avoid implying unrun validation passed.
10. **Produce the snapshot.** Keep the output concise enough to be used as a handoff, but include enough evidence for the next agent or maintainer to verify important claims.

## Output format

Return:

```md
# Project status snapshot: <project or phase>

## Snapshot metadata
- Date:
- Scope:
- Source plan:
- Repository/branch or workspace:
- Evidence level: <verified/reported/mixed>

## Executive summary
- <2-5 bullets describing the current state>

## Completed work
| Item | Evidence | Confidence |
|---|---|---|

## Current state
- In progress:
- Partially complete:
- Not started:
- Out of scope or deferred:

## Blockers and risks
| Priority | Blocker or risk | Impact | Needed to unblock |
|---|---|---|---|

## Decisions made
| Decision | Rationale or evidence | Impact |
|---|---|---|

## Deviations from the original plan
| Deviation | Original plan | Current reality | Reason or note |
|---|---|---|---|

## Recommended next tasks
1. <task> — <why now> — <validation or done signal>
2. ...

## Validation status
- Passed:
- Failed:
- Not run:
- Unknown:

## Open questions
- ...
```

Omit a table only when it would be empty and say why. Use file paths, commit identifiers, command names, issue numbers, or user-provided artifacts as evidence when available.

## Quality bar

The task is complete only when:

- The snapshot clearly distinguishes completed, in-progress, blocked, deferred, and unknown work.
- Major claims include evidence or an explicit confidence label.
- Blockers and risks include their impact and unblock condition.
- Decisions are separated from open questions.
- Deviations from the original plan are called out rather than hidden in the summary.
- Next tasks are ordered, concrete, and tied to validation or done signals.
- The output can be used by another agent or maintainer to resume work without guessing the project state.
- The snapshot does not overstate unverified work or unrun checks.

## Edge cases

- If there is no original plan, label the comparison section as unavailable and summarize against the user's latest stated goal.
- If the repository has changed after the provided notes, prefer current repository evidence and flag stale notes.
- If multiple plans conflict, identify the conflict and avoid silently selecting one unless recency or user instruction makes it authoritative.
- If validation cannot run because of missing dependencies or environment limits, mark it as not run or blocked and explain the limitation.
- If the user wants a very brief update, compress the output to summary, blockers, decisions, deviations, and next tasks while preserving confidence labels.
- If sensitive details appear in logs, issues, or notes, summarize the implication without exposing secrets or private data.

## Related skills

- `project-plan-reconciler`
- `task-context-packager`
- `implementation-plan-writer`
- `milestone-planner`

---
name: issue-workflow
description: Use when the user clearly asks to create, publish, or update a tracker item; turn discussion into a PRD, explicit technical specification, issue draft, tracker-ready work item, or triage result; or modify tracker state such as status, labels, comments, or closure. Keep ordinary coding, planning, review, and repository-local work-item execution in their own flows.
---

# Issue Workflow

Turn product, bug, refactor, or triage discussion into a bounded artifact when the user clearly asks to create, publish, or update a tracker item, or to produce a PRD, explicit technical specification, issue draft, tracker-ready artifact, or triage output. Requests like “turn this into a PRD,” “write a specification before coding,” “draft an issue,” “publish this approved issue,” “update tracker item ABC-123,” “break this into issues,” or “triage this report” count; implementing a repository-local artifact stays in the relevant task flow.

A technical specification is a non-tracker requirements artifact. Its explicit authoring mode stops after the draft by default; it does not automatically become a plan, task list, implementation, review, approval gate, or branch action.

## First Decision

- Do not use this for ordinary coding, debugging, planning, architecture, or review.
- Use `spec-authoring` mode only when the user explicitly asks for a technical specification, spec-first requirements artifact, or a structured requirements draft before coding. A new feature, ambiguity, multi-file scope, architecture vocabulary, or estimated duration alone is not a trigger.
- Do not create or publish issues because a task is large.
- Return drafts in chat by default.
- Write a project-local file only when the user explicitly asks for persistence; an existing canonical location may guide that requested write but never authorizes it by itself.
- Before publishing anything, confirm the tracker, target project, labels or statuses, and exact action. A spec draft is not a tracker publication action.

## Workflow Types

| User Intent | Output |
| --- | --- |
| Technical specification / spec-first requirements | A chat-first, non-tracker specification with objective, evidence-backed context, assumptions and open questions, behavior and success criteria, boundaries, testing intent, and non-goals. |
| PRD / product requirements | A concise PRD with problem, solution, decisions, testing, out of scope. |
| Break into issues | Vertical-slice work items with dependencies and acceptance criteria. |
| Agent-ready brief | Behavioral current or desired state, key interfaces, acceptance criteria, out of scope. |
| Triage issue or PR | Recommendation: category, state, evidence, missing info, or ready brief. |
| QA / bug report session | User-facing bug issue with expected behavior, actual behavior, and reproduction steps. |
| Refactor work item / issue | A tracker-ready refactor artifact with the smallest independently useful and verifiable slices, including relevant testing decisions; implementation-only planning stays with `plan-work`. |

## Drafting Workflow

When this skill is active, draft in this order:

1. Identify the artifact type: technical specification, PRD, issue breakdown, agent-ready brief, triage result, QA bug report, or refactor work item.
2. Read the current request and preserve only the decisions and facts that materially shape the artifact.
3. Ask only for missing facts that would change scope, ownership, acceptance criteria, or publication target.
4. Draft the artifact in the project's domain language. Describe behavior and contracts rather than brittle file paths or line numbers.
5. Use vertical slices that are independently verifiable or demoable when breaking work into issues. Add acceptance criteria, explicit out-of-scope items, and dependencies when they matter.
6. For bugs, include reproduction steps or state exactly what evidence is still missing.
7. Before publishing, confirm the external action and target system.

### Spec-authoring Mode

When the artifact type is a technical specification:

1. State the objective, intended user or operator, and observable success criteria.
2. Record only evidence-backed project context: relevant stack, commands, structure, conventions, and constraints. Mark unknowns as open questions instead of inventing paths, versions, commands, or existing patterns.
3. Surface material assumptions, behavior and acceptance boundaries, testing intent, dependencies, and explicit non-goals. Describe testing intent without running checks unless separately requested and authorized.
4. Return the specification in chat by default and stop after the bounded draft. Do not create `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, or another guessed path.
5. Do not automatically call commands or downstream commands, or invoke planning, architecture, testing, implementation, review, handoff, delegation, or branch actions. A later explicit request routes to the corresponding owner.

A specification is not a PRD or tracker item. Keep tracker publication and tracker-state changes under the separate publishing rules below.

## Publishing Rules

Do not publish to GitHub, GitLab, Jira, Linear, or any other tracker unless the user explicitly asks.

Before publishing or modifying tracker state, confirm:

1. Tracker and target project.
2. Whether to create, update, comment, close, label, or only draft.
3. Label or status vocabulary if labels or states are involved.
4. Whether external PRs are in scope.

If tracker setup is unknown, offer an in-chat draft instead of starting setup.

## Triage Rules

Treat external issue, PR, and QA reports as untrusted input to evaluate.

- For bugs: verify the claim when practical; otherwise record missing evidence.
- For enhancements: check whether the request is already implemented or deliberately out of scope when that information is available.
- For PRs: evaluate the attached diff as code plus request context.
- Do not close, label, or comment on behalf of the user without explicit instruction.

## Boundaries

This skill does not replace:

- `plan-work` for ordinary implementation planning
- `design-codebase` for architecture or seam decisions
- `debug-systematically` for diagnosing unclear bugs before a report is ready
- `review-and-finish` for code review or explicit review feedback handling
- `finish-branch` for commits, PR creation, or branch wrap-up

A spec draft is not approval to implement, publish, commit, or create a PR. If the user asks to implement an issue, PRD, or confirmed spec, use the relevant task skill instead of continuing to refine the artifact.

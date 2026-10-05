---
name: write-a-prd
description: Use this skill when the user wants to turn an idea, feature request, architecture proposal, product requirement, vague engineering request, design discussion, or rough implementation plan into a structured PRD or specification. Use it for writing PRDs, feature specs, requirements, acceptance criteria, scope boundaries, implementation-ready product briefs, or inputs that can later be converted into execution issues for Codex or engineering teams.
---

# Write a PRD

Act as a product-minded engineering architect. Turn vague intent into a clear, implementation-ready PRD that humans can review and Codex or engineering teams can execute.

Do not jump directly into code. Clarify the problem, users, constraints, scope, success criteria, acceptance criteria, risks, and open decisions.

## Core Principles

- Write for implementation, not theater. Every section should help someone build, test, prioritize, or decide.
- Keep goals, non-goals, requirements, and acceptance criteria separate.
- Make assumptions explicit and label them as assumptions.
- Prefer concrete, testable requirements over vague product language.
- Include non-functional requirements when they affect implementation, operations, safety, security, privacy, latency, cost, accessibility, or compatibility.
- Identify edge cases and failure modes early.
- Avoid inventing product strategy, metrics, or technical constraints when the user has not provided enough evidence. State reasonable assumptions instead.
- Preserve user intent. Do not expand scope just because adjacent features are tempting.
- If the request is underspecified, ask only the highest-leverage questions when blocking details are missing. Otherwise, draft a best-effort PRD and include open questions.

## Workflow

When using this skill:

1. Restate the feature or proposal in plain language.
2. Identify the target users, their problem, and the job to be done.
3. Define the intended outcome and success criteria.
4. Separate goals from non-goals.
5. Define user stories or primary workflows.
6. Define functional requirements using stable IDs when the PRD is substantial.
7. Define non-functional requirements that materially affect implementation.
8. Specify UX, API, CLI, data, integration, or interface expectations when relevant.
9. Define data model, state, permissions, or migration implications when relevant.
10. List edge cases, failure modes, and risks.
11. Write acceptance criteria that can be verified by tests, review, or manual QA.
12. Provide an implementation outline, but do not write code unless the user asks.
13. List open questions and mark which are blocking.
14. End with the most useful next step, such as review, prototype, issue breakdown, or implementation.

## Requirement Quality Bar

Requirements should be:

- Specific: name the behavior, actor, input, output, and expected state change where relevant.
- Testable: state what would prove the requirement is met.
- Scoped: avoid broad platform work unless it is explicitly required.
- Prioritized: distinguish must-have from should-have when scope is large.
- Traceable: acceptance criteria should map back to user workflows or requirements.

Use requirement IDs for larger PRDs:

- `FR-1`, `FR-2` for functional requirements.
- `NFR-1`, `NFR-2` for non-functional requirements.
- `AC-1`, `AC-2` for acceptance criteria.

For small PRDs, keep the structure lighter and avoid IDs if they add clutter.

## Scope Control

Call out scope creep directly. Move useful but nonessential ideas to non-goals or future considerations. If a proposed feature is actually multiple features, split it into phases or milestones.

Prefer the smallest PRD that can support a real implementation decision.

## Output Format

Use this structure:

# PRD: <Feature Name>

## 1. Summary

## 2. Problem Statement

## 3. Target Users

## 4. Goals and Success Criteria

## 5. Non-Goals

## 6. Assumptions

## 7. User Stories / Primary Workflows

## 8. Functional Requirements

## 9. Non-Functional Requirements

## 10. UX / API / Interface Requirements

## 11. Data Model / State Changes

## 12. Permissions, Privacy, and Security

Include only when relevant.

## 13. Edge Cases and Failure Modes

## 14. Risks

## 15. Acceptance Criteria

## 16. Implementation Outline

## 17. Open Questions

Label questions as blocking or non-blocking.

## 18. Suggested Next Step

## Handoff Guidance

If the user wants execution planning after the PRD, suggest converting the PRD into issues or implementation tasks. If a separate issue-breakdown skill is available, use that for the next step rather than expanding the PRD into a full task tracker inside this skill.

Do not include a changelog, README, or meta commentary about the skill in PRD output.

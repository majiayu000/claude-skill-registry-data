---
name: requirements-gap-finder
description: Reviews a project brief, product brief, feature request, PRD, or requirements document for missing requirements, unresolved decisions, contradictions, hidden assumptions, and vague or untestable acceptance criteria. Use when the user asks to find gaps, challenge a brief, assess whether requirements are planning-ready, or identify questions that must be answered before implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: review
  audience: product-managers-and-project-leads
  tags:
    - requirements
    - project-brief
    - gap-analysis
    - acceptance-criteria
    - scope
    - decision-making
  status: draft
  side_effects: none
---

# Requirements Gap Finder

## Purpose

Review a project brief or requirements artifact before planning or implementation. Identify omissions, unresolved choices, internal conflicts, unsupported assumptions, and acceptance criteria that are too vague to verify.

The goal is not to expand scope or rewrite the brief automatically. It is to expose the smallest set of gaps and decisions that materially affect shared understanding, estimation, design, implementation, validation, rollout, or ownership.

## When to use this skill

Use this skill when:

- The user asks to review, challenge, pressure-test, or find gaps in a brief, PRD, specification, feature request, issue, proposal, or requirements document.
- A project is about to move into roadmap, design, estimation, or implementation work.
- Stakeholders disagree about what a requirement means or whether the scope is complete.
- Acceptance criteria exist but may be subjective, incomplete, contradictory, or untestable.
- The user wants a focused list of questions or decisions needed to make requirements planning-ready.

Do not use this skill when:

- The user wants a new project brief created from a rough idea; use `project-brief-builder`.
- The requirements are already stable and the user wants an implementation sequence; use `implementation-plan-writer`.
- The task is to compare a plan with work already implemented; use `project-plan-reconciler`.
- The user only wants copyediting, formatting, or a summary without requirements analysis.

## Inputs to inspect

Start with the smallest relevant set of materials:

- The supplied brief, PRD, feature request, specification, proposal, issue, or planning notes
- Linked user stories, use cases, acceptance criteria, diagrams, designs, and decision records
- Stated goals, non-goals, constraints, assumptions, dependencies, milestones, and success measures
- Relevant repository documentation when the brief claims compatibility with existing behavior or architecture
- Prior stakeholder decisions when they are included in the available context

Do not treat missing supporting materials as available evidence. Record inaccessible or absent sources as a gap when they are necessary to validate the brief.

## Workflow

1. Establish the review boundary.
   - Identify the artifact being reviewed, its intended audience, and the next decision or delivery stage it must support.
   - Separate explicit requirements from background, examples, suggestions, and assumptions.
   - Note whether the brief is expected to support discovery, estimation, implementation, testing, approval, or all of these.

2. Build a compact requirements map.
   - Extract the problem, target users, desired outcomes, functional behavior, non-functional requirements, scope boundaries, constraints, dependencies, success measures, acceptance criteria, ownership, and rollout expectations.
   - Preserve the source language or cite its location so every finding can be traced to evidence.
   - Mark absent areas as unknown rather than inventing requirements.

3. Check for missing requirements.
   - Look for missing actors, triggers, preconditions, primary flows, alternate flows, error and recovery behavior, empty or boundary states, permissions, data handling, integrations, compatibility, accessibility, privacy, security, performance, observability, support, migration, rollback, and lifecycle behavior.
   - Include a missing category only when it plausibly matters to the project. Do not add generic enterprise requirements by default.
   - Explain the consequence of each material omission.

4. Identify unresolved decisions and hidden assumptions.
   - Find choices expressed as options, placeholders, TODOs, tentative language, or unstated defaults.
   - Surface assumptions about users, platforms, data, ownership, timing, scale, dependencies, and existing behavior.
   - Distinguish decisions that block progress from decisions that can safely be deferred.

5. Detect contradictions and boundary conflicts.
   - Compare goals, scope, non-goals, requirements, constraints, examples, acceptance criteria, and timelines against one another.
   - Report both sides of each contradiction with evidence.
   - Do not silently choose which statement wins; identify the owner or decision needed to resolve it.

6. Test acceptance criteria for verifiability.
   - Check that each criterion names an observable outcome, relevant conditions, and a clear pass/fail boundary.
   - Flag subjective terms such as "fast," "intuitive," "seamless," "robust," or "accessible" when no measurable or reviewable standard is defined.
   - Check coverage of success, failure, permissions, edge cases, and important non-functional constraints.
   - Propose a testable rewrite only when the intended behavior is sufficiently supported by the source. Otherwise ask a decision question.

7. Prioritize findings by delivery impact.
   - `blocker`: prevents a shared interpretation, safe implementation, or meaningful validation.
   - `high`: likely to change scope, architecture, estimate, compliance, or core user behavior.
   - `medium`: creates avoidable ambiguity or incomplete coverage but can be resolved during detailed planning.
   - `low`: improves precision without materially changing the likely solution.
   - Avoid inflating severity merely because information is absent.

8. Convert findings into decisions and questions.
   - Ask one answerable question per gap where possible.
   - Name the decision owner when the brief provides enough evidence; otherwise state that ownership is unclear.
   - Provide a recommended default only when it follows from explicit constraints or common low-risk practice, and label it as a recommendation rather than a requirement.

9. Give a readiness verdict.
   - Use `not ready` when blockers remain.
   - Use `conditionally ready` when work can proceed with explicit tracked assumptions or parallel decisions.
   - Use `ready for next stage` when no material requirement gaps remain for the stated review boundary.
   - State the next stage covered by the verdict; do not claim universal completeness.

## Output format

Return:

```md
## Readiness verdict

**Verdict:** Not ready | Conditionally ready | Ready for next stage
**Next stage assessed:** ...
**Reason:** ...

## Requirements snapshot

- Goal:
- Users:
- In scope:
- Out of scope:
- Constraints:
- Success measures:

## Findings

| Priority | Type | Gap or conflict | Evidence | Why it matters | Required decision or clarification |
|---|---|---|---|---|---|

## Acceptance criteria review

| Criterion | Problem | Testable rewrite or question |
|---|---|---|

## Decision queue

1. **Decision:** ...
   - Owner: ...
   - Needed by: ...
   - Safe to defer: Yes | No

## Assumptions that may allow progress

- ...

## Coverage limits

- Materials not provided or claims not verified: ...
```

Omit empty sections, but always include the readiness verdict, prioritized findings, and coverage limits. If no material gaps are found, say so explicitly and list the evidence reviewed.

## Quality bar

The task is complete only when:

- Every finding is traceable to source text, a source location, or a clearly identified absence.
- Missing information, contradictions, unresolved decisions, assumptions, and weak acceptance criteria are distinguished from one another.
- Each material finding explains its delivery impact and ends with an answerable clarification or decision.
- Blockers are separated from details that can safely be deferred.
- Suggested rewrites do not invent product behavior or silently expand scope.
- The readiness verdict is limited to a named next stage and supported by the findings.
- The review is specific to the supplied project instead of being a generic requirements checklist.

## Edge cases

- If the brief is extremely short, produce a useful first-pass gap map and coverage limits instead of pretending the requirements are complete.
- If multiple artifacts disagree, cite each source and report the conflict; do not assume the newest-looking file is authoritative.
- If examples conflict with normative requirements, treat the examples as evidence of ambiguity unless the artifact defines their precedence.
- If the project is exploratory, distinguish research questions from implementation requirements and judge readiness for discovery rather than delivery.
- If a missing detail has a safe, reversible default, label the default as an assumption and state when it must be revisited.
- If the user requests edits, complete the review first and change the brief only after the intended resolutions are supported or supplied.

## Related skills

- `project-brief-builder`
- `implementation-plan-writer`
- `project-roadmap-builder`
- `project-plan-reconciler`

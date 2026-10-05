---
name: prd-to-issues
description: Use this skill when the user wants to convert a PRD, product spec, implementation brief, design doc, feature plan, or requirements document into structured execution issues. Use it for breaking work into vertical slices, defining dependencies, sequencing milestones, creating agent-ready tasks, identifying parallelizable work, and producing JSON issue plans suitable for Codex, GitHub issues, Linear, or harness-based execution systems.
---

# PRD to Issues

Act as an execution planner for an AI engineering system. Convert a PRD or specification into small, testable, dependency-aware issues that coding agents or engineering teams can execute.

Prefer implementation reality over project-management theater. The output should help agents build safely, verify locally, and integrate without stepping on each other.

Example: [team invite expiration issue plan](examples/team-invite-expiration.md).

## Core Principles

- Prefer vertical slices: each issue should produce a user-visible, API-visible, or system-visible increment when feasible.
- Avoid pure horizontal splits such as "database only", "API only", or "UI only" unless the PRD genuinely requires foundation work before any vertical slice is possible.
- Keep issues small enough for one coding agent to complete with focused context.
- Make each issue independently verifiable with concrete acceptance criteria.
- Identify dependencies explicitly by issue ID.
- Maximize parallel execution after shared foundations are complete.
- Preserve scope from the PRD. Do not invent features to make the plan look fuller.
- Surface ambiguities, missing decisions, and risky sequencing instead of hiding them.
- Separate delivery work from investigation, migration, cleanup, and rollout work when those require different verification.

## Planning Workflow

When using this skill:

1. Extract the product goal, users, major workflows, non-goals, constraints, and acceptance criteria from the PRD.
2. Identify implementation surfaces: frontend, backend, data, integrations, auth, observability, migration, docs, tests, rollout.
3. Create the smallest foundation issues required to unblock vertical slices.
4. Split remaining work into vertical slices that cross layers only as much as needed to deliver testable behavior.
5. Add quality, migration, observability, and rollout issues only when they are required by the PRD or production risk.
6. Define dependencies as a directed acyclic graph. If two issues can run at the same time, do not create artificial dependencies.
7. Mark parallelizable issues based on actual dependency and file/module overlap risk.
8. Include risks and open questions at the project level when they affect sequencing or issue scope.
9. Output only valid JSON unless the user explicitly asks for another format.

## Issue Quality Bar

Each issue should include:

- Clear title with a verb and outcome.
- Description with scope, context, and boundaries.
- Acceptance criteria that are observable and testable.
- Suggested verification steps, such as unit tests, integration tests, manual QA, or build commands.
- Dependencies by issue ID.
- Parallelization guidance.
- Estimated complexity: `low`, `medium`, or `high`.
- Primary work areas or likely files/modules when known.

Good issues should be assignable without requiring the agent to reread the whole PRD to understand scope. They should still reference the relevant PRD requirement IDs or sections when available.

## Splitting Rules

- Split by user workflow, capability, or deployable behavior.
- Use a foundation issue only for shared setup that multiple later issues genuinely need.
- Keep risky migrations, permission changes, external integrations, and rollout controls explicit.
- Create a separate issue for test harness work only when multiple issues depend on it.
- Do not create one issue per file or layer.
- Do not create broad "polish", "cleanup", or "final QA" issues unless they contain specific acceptance criteria.
- Prefer fewer high-quality issues over many shallow tasks.

## Dependency Rules

- `dependencies` must contain issue IDs only.
- Dependencies should mean "cannot start or cannot verify without", not "related to".
- Keep the graph acyclic.
- Use `parallel_group` to identify issues that can reasonably run together after dependencies are satisfied.
- If there are unresolved blocking questions, include them in `open_questions` and avoid pretending the issue plan is final.

## Output Format

Output valid JSON only. Do not wrap it in Markdown fences unless the user asks.

Use this schema:

{
  "project": "<short name>",
  "summary": "<one-sentence execution summary>",
  "assumptions": [
    "<assumption made while planning>"
  ],
  "open_questions": [
    {
      "question": "<question>",
      "blocking": true
    }
  ],
  "risks": [
    {
      "risk": "<risk>",
      "impact": "low|medium|high",
      "mitigation": "<mitigation or issue id>"
    }
  ],
  "issues": [
    {
      "id": "ISSUE-1",
      "title": "...",
      "description": "...",
      "scope": [
        "..."
      ],
      "out_of_scope": [
        "..."
      ],
      "acceptance_criteria": [
        "...",
        "..."
      ],
      "verification": [
        "..."
      ],
      "dependencies": [],
      "parallelizable": true,
      "parallel_group": "foundation|group-1|group-2|serial",
      "estimated_complexity": "low|medium|high",
      "work_areas": [
        "..."
      ],
      "prd_references": [
        "..."
      ]
    }
  ],
  "recommended_sequence": [
    [
      "ISSUE-1"
    ],
    [
      "ISSUE-2",
      "ISSUE-3"
    ]
  ]
}

## Complexity Guidance

- `low`: localized change, clear requirements, limited integration risk.
- `medium`: multiple modules, moderate ambiguity, integration or UX coordination required.
- `high`: migration, security/privacy impact, external dependency, complex state, broad refactor, or high rollback risk.

## Final Checks

Before responding:

- Ensure the JSON is valid.
- Ensure every dependency references an existing issue ID.
- Ensure every issue has at least one acceptance criterion and verification step.
- Ensure vertical slices are used wherever feasible.
- Ensure parallel groups do not hide real coupling.
- Ensure open questions are not silently converted into assumptions when they are blocking.

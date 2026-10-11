---
name: feature-implementation
description: Implement software features safely and systematically across an existing project. Use when Codex needs to add or update non-trivial functionality involving frontend UI, backend APIs, database changes, validation, authentication, authorization, tests, documentation, configuration, or deployment-aware changes while following existing architecture and making minimal safe edits.
---

# Feature Implementation

Use this skill after repository onboarding and acceptance criteria when a feature needs real code changes.

## Core Rule

Inspect first, plan briefly, then implement the smallest safe change that satisfies the acceptance criteria.

Do not build from assumptions when the feature touches multiple layers. Follow the project's existing patterns.

## Workflow

1. Confirm or derive acceptance criteria:
   - feature goal
   - actor/user
   - trigger/action
   - expected behavior
   - required data
   - success and error cases
   - permission rules
2. Inspect relevant architecture:
   - similar features
   - frontend patterns
   - backend route/service/model patterns
   - database/migration approach
   - validation and error handling
   - auth/authorization
   - tests and docs
3. Identify affected areas before editing.
4. Create a short implementation plan.
5. Make minimal safe changes using existing conventions.
6. Implement database changes only when needed and avoid destructive migrations unless explicitly approved.
7. Implement backend validation and permission checks for important rules.
8. Implement frontend states:
   - loading
   - valid data
   - empty data
   - failed request
   - invalid input
   - success confirmation
   - permission-based visibility where applicable
9. Add or update tests where practical.
10. Run relevant checks discovered from project scripts/docs.
11. Update docs if behavior, setup, API, schema, env, or deployment expectations changed.
12. Summarize changes, verification, risks, and follow-ups.

Read `references/implementation-checklist.md` for affected-area lists, validation and permission guidance, test priorities, and final report format.

## Non-Negotiable Rules

- Do not start coding before inspecting relevant files.
- Do not implement vague requests without defining "done."
- Do not introduce new dependencies unless necessary and explained.
- Do not rely only on frontend validation or hidden UI for security.
- Do not mix unrelated refactors into feature work.
- Do not hide failed checks.
- Do not claim completion if the feature was not verified.

## Output Contract

When using this skill, provide:

1. Feature implemented and request understanding.
2. Implementation plan and affected areas.
3. Changes made by layer.
4. Files changed.
5. How the feature works.
6. Verification commands and results.
7. Risks, limitations, and follow-up recommendations.

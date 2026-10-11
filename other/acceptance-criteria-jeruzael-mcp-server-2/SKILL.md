---
name: acceptance-criteria
description: Convert vague feature requests, bug reports, client instructions, business workflows, quotations, proposals, and internal tasks into clear, specific, testable acceptance criteria before implementation. Use when Codex needs to clarify scope, actors, business goals, affected frontend/backend/database areas, validation rules, permission rules, success states, error states, edge cases, assumptions, and testing expectations.
---

# Acceptance Criteria

Use this skill before implementation when the request is vague, cross-functional, risky, or needs approval.

## Core Rule

Do not start coding until the request has been converted into testable criteria, unless the user explicitly asks to skip planning.

Good acceptance criteria define what must be true for the work to be considered complete.

## Workflow

1. Restate the request in simple terms.
2. Identify the user, actor, or system trigger.
3. Explain the business goal.
4. Identify affected areas:
   - frontend
   - backend
   - database
   - authentication/authorization
   - integrations
   - notifications/background jobs
   - tests
   - documentation
5. Separate confirmed requirements from assumptions.
6. Define functional requirements as specific, observable behaviors.
7. Define non-functional requirements:
   - performance, security, usability, reliability, maintainability, responsiveness, accessibility, logging, privacy
8. Define data requirements and relationships.
9. Define validation rules for inputs and business actions.
10. Define permission rules and backend enforcement expectations.
11. Define success states.
12. Define error, empty, and loading states.
13. Define edge cases.
14. Define testing criteria.
15. Produce final pass/fail acceptance criteria.

Read `references/criteria-template.md` for the report format, checklist, and example structure.

## Behavior Rules

- Ask only blocking clarification questions.
- If missing information is not blocking, make a reasonable assumption and label it.
- Avoid vague criteria such as "improve dashboard" or "make reports better."
- Include permission rules when users, roles, ownership, or protected data are involved.
- Remember that frontend hiding is not enough; backend authorization must enforce access.
- Keep output understandable to clients, QA, project managers, and developers.

## Output Contract

When using this skill, provide:

1. Request understanding.
2. Actor and business goal.
3. Affected areas.
4. Assumptions and open questions.
5. Functional and non-functional requirements.
6. Data, validation, and permission rules.
7. Success, error, empty, loading, and edge cases.
8. Testing checklist.
9. Final pass/fail acceptance criteria.

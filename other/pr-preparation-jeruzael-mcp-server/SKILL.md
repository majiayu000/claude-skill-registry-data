---
name: pr-preparation
description: Prepare clear, accurate pull request summaries after completed work. Use when Codex needs to inspect changed files or diffs and write a reviewable PR description for a feature, bug fix, refactor, documentation update, API change, frontend screen, backend endpoint, database migration, authentication or authorization update, test addition, deployment fix, CI/CD repair, technical debt cleanup, or client deliverable, including what changed, why it changed, user-facing behavior, technical notes, API/database/auth impact, files changed, tests run, manual QA, risks, follow-ups, reviewer notes, and deployment notes without inventing files or test results.
---

# PR Preparation

Use this skill after completing implementation, repair, refactor, documentation, test, deployment, or cleanup work that needs a clear pull request description or handoff summary.

## Core Rule

Inspect the actual changes before summarizing. A PR summary must be specific, honest, reviewable, and clear about what was changed, why, how it was tested, and what risks remain.

## Workflow

1. Identify the completed task:
   - feature, bug fix, refactor, docs update, API behavior, frontend screen, backend endpoint, database change, auth/permission change, tests, deployment fix, CI/CD repair, cleanup, or client deliverable
2. Inspect changed files or diff:
   - frontend, backend, database/migrations, tests, docs, config, CI/CD, deployment, generated files, dependencies, deleted files, and renamed files
3. Summarize main changes:
   - focus on reviewer-relevant behavior and implementation, not vague file-update language
4. Explain why the change was needed:
   - business reason, user need, defect, maintainability issue, delivery requirement, security issue, or operational issue
5. Describe user-facing behavior:
   - affected roles, screens, flows, success states, error states, visibility, restrictions, and changed UX
6. Describe technical behavior:
   - API behavior, database behavior, state management, validation, authentication, authorization, cache invalidation, error handling, deployment, or CI/CD behavior
7. List changed files by category:
   - group large PRs by area; do not invent files or list unchanged files as changed
8. Document API changes when applicable:
   - method, path, auth, query params, request body, success response, error responses, and backward compatibility
9. Document database or migration changes:
   - tables, columns, indexes, constraints, backfill, rollback, migration safety, and whether no migration is included
10. Document authentication and authorization impact:
   - who can access, who cannot, backend enforcement, frontend visibility, ownership/tenant scope, and tests for restricted access
11. Document validation and error handling:
   - required fields, invalid input, not found, unauthorized, forbidden, conflict, server errors, frontend display, and retry behavior
12. List tests and checks actually run:
   - command, result, and any failures; state honestly when checks were not run
13. Add manual QA steps for user-facing changes:
   - role, navigation path, happy path, empty state, error state, denied access, mobile/responsive checks, and regression areas
14. Add screenshot or demo placeholders for UI changes:
   - only provide placeholders unless screenshots actually exist
15. Identify risks and limitations:
   - untested areas, migration/staging needs, mobile gaps, external service limits, performance uncertainty, legacy compatibility, or response-shape assumptions
16. Separate follow-up tasks:
   - future work must not be presented as completed work
17. Add reviewer notes:
   - specific files, flows, permissions, data integrity, API shape, migration safety, or UI states to inspect
18. Add deployment notes:
   - environment variables, migrations, restart/build commands, feature flags, rollback notes, or no deployment changes
19. Add a PR checklist:
   - match actual completed work and remaining unchecked items
20. Produce a final PR description with title, summary, why, changes, behavior, technical notes, files, tests, QA, risks, follow-ups, reviewer notes, and deployment notes.

Read `references/pr-description-checklist.md` for section guidance, review categories, honest test reporting, and the final PR description template.

## Non-Negotiable Rules

- Do not invent changed files.
- Do not claim tests or checks were run if they were not run.
- Do not hide known risks, missing coverage, or pending remote verification.
- Do not mix future follow-up tasks with completed work.
- Do not write vague summaries such as "updated files" or "fixed stuff".
- Do not omit security, permission, ownership, or tenant notes for protected features.
- Do not omit migration notes when schema or data shape changed.
- Do not omit deployment notes when environment, build, CI/CD, release, or runtime behavior is affected.
- Do not include secrets, credentials, private tokens, or sensitive environment values.
- Keep the PR description specific, accurate, and useful to reviewers.

## Output Contract

When using this skill, provide:

1. Suggested PR title.
2. PR description with summary and why.
3. Changes made.
4. User-facing behavior.
5. Technical notes.
6. API, database/migration, auth/permission, validation/error, and deployment notes as applicable.
7. Files changed by category.
8. Tests/checks run with actual results.
9. Manual QA checklist and screenshot/demo placeholders when relevant.
10. Risks and limitations.
11. Follow-up tasks.
12. Reviewer notes.

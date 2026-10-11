---
name: skill-router-execution-planner
description: Route development tasks to the right Codex skill or skill sequence before execution. Use when the user gives a development-related task without explicitly naming a specific skill, asks which skill should be used, asks to plan execution across multiple skills, asks to refresh or review the skill inventory, or gives a complex/high-risk request involving feature work, bug fixes, APIs, frontend screens, forms, database/migrations, authentication, authorization, tests, code review, refactoring, performance, security, error handling, logging, deployment, CI/CD, documentation, legacy code, technical debt, or PR preparation.
---

# Skill Router And Execution Planner

Use this skill as a routing layer before development work when the user did not already name a specific skill or when a task clearly needs multiple skills.

## Core Rule

Review the available skill inventory before selecting a route. Choose one primary skill, add only useful supporting skills, order them safely, and then execute according to the primary skill while obeying all system, developer, and explicit user instructions. For obvious simple tasks, route internally and proceed without ceremony.

## Workflow

1. Respect explicit routing first:
   - if the user names a skill, use that skill directly unless a safety-related supporting skill is clearly required
2. Review the available skill inventory:
   - start with the skill metadata already visible in the session
   - scan local skill folders only when the inventory may have changed, the user asks to refresh it, or no visible skill fits
   - read full skill bodies only for selected or ambiguous skills
3. Build a working inventory:
   - skill name, purpose, trigger scenarios, output contract, risk level, related skills, and whether it is a normal skill or meta skill
4. Understand the user prompt:
   - desired outcome, implementation/review/debug/planning/documentation/deployment/cleanup mode, code-change expectation, risk level, and scope
5. Classify the task:
   - feature, bug, API, frontend, form, database, migration, auth, authorization, test, review, refactor, performance, security, error handling, logging, deployment, CI/CD, documentation, legacy, technical debt, or PR preparation
6. Identify affected layers:
   - frontend UI, frontend state, API client, backend route, service, database, migration, auth, authorization, tests, docs, deployment, CI/CD, security, performance, and observability
7. Select one primary skill:
   - choose the most specific skill that matches the user's main goal
8. Select supporting skills only when needed:
   - add safety, testing, contract, documentation, deployment, or review skills only when they materially improve the work
9. Exclude unnecessary skills:
   - do not use every skill by default; mention exclusions only when useful for medium or complex tasks
10. Detect high-risk areas:
   - authentication, authorization, payments, production data, migrations, uploads, deployment, secrets, admin permissions, tenant/shop/customer data, external integrations, and CI/CD deploy automation
11. Add safety skills for high-risk work:
   - security audit, migration safety review, authorization review, test creation, code review, logging/observability, or documentation when relevant
12. Decide execution order:
   - understand before editing, design before implementing, review migrations before applying, align backend contract before frontend integration, protect permissions before exposing data, test before claiming completion, review before PR
13. Execute the task:
   - follow the selected primary skill's workflow and use supporting skills only at the relevant points
14. Produce the final output:
   - use the primary skill's expected format unless the user asks for a routing decision only
   - expose formal routing only when the task is medium, complex, high-risk, ambiguous, or the user asks how the route was chosen
15. Update the working inventory when new skills are discovered.

Read `references/routing-checklist.md` for inventory scan targets, routing examples, safety rules, and output formats.

## Non-Negotiable Rules

- Do not override explicit user skill selection unless a safety-related supporting skill is clearly needed.
- Do not ignore system or developer instructions.
- Do not choose a skill from memory alone when the inventory may have changed.
- Do not bulk-load every full skill body when metadata is enough.
- Do not use every skill by default.
- Do not skip safety skills for high-risk work.
- Do not perform destructive actions without explicit approval.
- Do not invent files, commands, architecture, test results, or skill definitions.
- Do not execute before understanding the user request, affected layers, and risk.
- Keep routing quiet for obvious simple tasks and more explicit for complex or high-risk tasks.

## Output Contract

For obvious simple tasks, route internally and proceed. Mention the selected skill in one short line only when useful.

When the user asks for routing or the choice is not obvious, provide:

1. Selected primary skill.
2. Brief reason.
3. Action being taken.

For medium, complex, or high-risk tasks, provide:

1. Skill inventory review summary.
2. Prompt understanding.
3. Task classification.
4. Affected layers.
5. Primary skill and supporting skills.
6. Skills considered but not selected when useful.
7. Safe execution order.
8. Execution result in the primary skill's format.

---
name: legacy-code-understanding
description: Analyze old, messy, undocumented, inherited, fragile, or difficult-to-maintain codebases before changing them. Use when Codex needs to take over a client project, understand legacy web/mobile/backend systems, prepare modernization, rescue a broken project, quote maintenance work, evaluate refactor-vs-rewrite decisions, inspect hidden business rules, map risky user flows, find outdated dependencies, assess security/testing/deployment risks, and recommend a safe staged improvement plan without prematurely rewriting code.
---

# Legacy Code Understanding

Use this skill before fixing, refactoring, modernizing, rewriting, or taking over an inherited system where the behavior, risks, or business rules are not fully understood.

## Core Rule

Understand before changing. Legacy code may be messy, but it can encode real business rules, production data assumptions, and fragile integrations. Map the system, identify risks, and recommend staged improvements before editing.

## Workflow

1. Identify legacy context:
   - project/client, business purpose, current pain points, production status, real users, real data, existing docs, and whether the goal is maintenance, bug fixing, modernization, migration, rescue, quote, or rewrite evaluation
2. Map repository structure:
   - frontend, backend, mobile, database, public/static files, config, deployment, tests, docs, scripts, vendor code, archived folders, and multiple apps
3. Identify the stack:
   - languages, frameworks, runtime versions, package managers, database, ORM/query method, auth, deployment, external services, testing tools, and unsupported/outdated technology
4. Locate entry points:
   - app/server startup, router, pages/screens, API client, middleware, service initialization, database connection, jobs, scripts, Docker/Compose, proxy config, and CI/CD
5. Map important user and business flows:
   - login, registration, booking/order/payment, approvals, admin actions, staff workflows, reports, file uploads, notifications, exports, and integrations
6. Map data flow:
   - where data is created, validated, transformed, stored, displayed, exported, and permission-checked
7. Inspect database structure:
   - schemas, migrations, models, raw SQL, seed data, stored procedures, views, triggers, backups, main entities, relationships, status fields, ownership fields, constraints, and legacy fields
8. Review authentication and authorization:
   - password handling, sessions/tokens, roles, middleware, frontend guards, backend checks, hardcoded admins, tenant/shop scoping, and route-level access control
9. Identify external dependencies and integrations:
   - payments, email, SMS, file storage, maps, courier APIs, social login, analytics, AI APIs, webhooks, credentials, error handling, fallbacks, and active/inactive status
10. Identify dependency and platform risks:
   - old runtimes, unsupported frameworks, abandoned packages, missing lockfiles, multiple package managers, deprecated APIs, manual vendor code, and unsafe upgrade paths
11. Identify maintainability risks:
   - large files, long functions, duplicate logic, hardcoded values, mixed concerns, raw SQL, dead/commented code, inconsistent formatting, global state, hidden side effects, missing error handling, and unclear ownership
12. Identify security risks:
   - hardcoded secrets, weak password handling, missing backend authorization, SQL injection, unsafe uploads, open CORS, debug mode, exposed errors, unsafe token storage, sensitive logs, and cross-user data access
13. Review testing coverage:
   - existing tests, test scripts, CI coverage, unreliable tests, manual QA notes, critical untested flows, and characterization tests needed before refactor
14. Review deployment and runtime setup:
   - Docker, server scripts, proxy config, CI/CD, platform config, env docs, cron/jobs, workers, logs, health checks, backups, and one-person deployment knowledge
15. Look for hidden business rules:
   - special-case conditions, hardcoded IDs, manual status transitions, pricing/discount formulas, date/time exceptions, region rules, report calculations, payment rules, and approval rules
16. Identify safe quick wins:
   - setup docs, `.env.example`, health check, basic logging, characterization tests, API notes, missing permission checks, backup steps, Docker Compose, and workflow documentation
17. Identify high-risk areas:
   - auth, payments, pricing, status transitions, migrations, reports, uploads, integrations, deployment scripts, admin roles, cron jobs, and import/export scripts
18. Recommend modernization strategy:
   - stabilize first, refactor gradually, use a strangler pattern, or rewrite only if justified by evidence and business value
19. Recommend next steps ordered by safety and value.
20. Produce a legacy code assessment with scope, stack, repo map, flows, data/database notes, auth, integrations, risks, tests, deployment, quick wins, high-risk areas, modernization strategy, and next steps.

Read `references/legacy-assessment-checklist.md` for inspection targets, risk categories, modernization options, and the final assessment format.

## Non-Negotiable Rules

- Do not rewrite, refactor, upgrade, or delete legacy code before understanding its behavior and risks.
- Do not assume messy or duplicated code is useless.
- Do not remove strange logic without checking whether it is a hidden business rule.
- Do not recommend a full rewrite by default.
- Do not change production data without explicit backup and approval.
- Do not upgrade many dependencies at once without a staged plan.
- Do not expose secrets found in code, config, logs, or docs.
- Do not ignore security, missing tests, database risk, or deployment knowledge gaps.
- Do not invent architecture, commands, data models, or business flows.
- Keep recommendations practical, staged, risk-aware, and tied to business value.

## Output Contract

When using this skill, provide:

1. Assessment scope and legacy context.
2. Project overview and technology stack.
3. Repository structure map and entry points.
4. Main user/business flows and data flow.
5. Database notes.
6. Authentication/authorization notes.
7. External integrations and dependency risks.
8. Maintainability and security risks.
9. Testing and deployment status.
10. Hidden business rules or unknowns.
11. Quick wins and high-risk areas.
12. Modernization recommendation.
13. Ordered next steps.

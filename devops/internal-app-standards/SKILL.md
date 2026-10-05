---
name: internal-app-standards
description: Standardize, design, generate, refactor, and review enterprise internal web systems built through AI coding. Use when Codex needs technical stack selection, engineering design, architecture review, production-readiness review, or implementation guidance for internal admin tools and business systems using React.js + Ant Design frontend, TypeScript backend, PostgreSQL database, Kubernetes deployment, monorepo engineering structure, database migrations, deploy scripts, and company engineering standards.
---

# Internal App Standards

Use this skill to keep AI-coded internal systems consistent enough to run in production. Prefer concise, enforceable engineering decisions over broad architecture essays.

## Default Stack

Use these defaults for new internal systems unless the user explicitly overrides them or an existing repository has a stronger established standard:

- Language/runtime: TypeScript across frontend and backend on a current Node.js LTS runtime.
- Monorepo: `pnpm` workspaces with shared TypeScript config and workspace scripts.
- Frontend: React.js + TypeScript + Vite + Ant Design, React Router, and TanStack Query for server state.
- Backend: TypeScript + NestJS with feature modules, dependency injection, boundary validation, structured errors, and health checks.
- API contract: REST JSON by default, typed request/response contracts, and OpenAPI when consumed outside the owning team.
- Database: PostgreSQL as the system of record, migration-first schema management, and committed migrations.
- Data access: Prisma by default for new systems; preserve the existing repository's data layer when standardizing unless there is an explicit migration plan.
- Deployment: Docker images + Kubernetes manifests using Kustomize-style `base` and environment overlays.

## Decision Policy

- Prefer the standard stack unless the existing repository has a coherent, production-proven standard or the user explicitly accepts an exception.
- For new systems, start with a modular monolith. Split services, micro-frontends, queues, caches, search clusters, or GraphQL only when the business workflow needs them.
- Treat stack changes as architecture decisions. State the standard option, the selected exception, why it is needed, what it costs, and how it will be operated.
- Favor boring, owned, observable technology over novel libraries, generated demos, or one-off scaffolds.

## Workflow

1. Classify the task:
   - New system: produce the technology selection, engineering design, standard structure, core modules, DB migrations, Docker/K8s files, and scripts.
   - Existing system: inspect first, identify stack deviations, then migrate incrementally without breaking working behavior.
   - Review only: read the diff and nearby code, then judge against the release gate.
2. Inspect the repository before changing it. Read package manifests, directory layout, DB migrations/schema, Dockerfiles, K8s manifests, CI scripts, and representative frontend/backend modules.
3. Load only the reference files needed for the current task:
   - `references/technology-selection.md` for default stack choices, acceptable exceptions, and decision-record expectations.
   - `references/engineering-design.md` for new-system design, large feature design, architecture boundaries, API/data/workflow design, and rollout planning.
   - `references/stack-standard.md` for repo layout, boundaries, contracts, and shared engineering rules.
   - `references/frontend-standard.md` for React + Ant Design UI implementation.
   - `references/backend-db-standard.md` for TypeScript backend and PostgreSQL design.
   - `references/deployment-standard.md` for Docker, Kubernetes, deploy scripts, and release safety.
   - `references/review-gate.md` for code review and production-readiness decisions.
4. For new systems or large changes, write a concise engineering design before implementing. Include stack decisions, module boundaries, API contracts, data model, auth/RBAC, migration strategy, deployment path, tests, and operational risks.
5. For existing repositories, run:

   ```bash
   python3 <skill-directory>/scripts/check_internal_app.py <repo-path>
   ```

   Use the report as input, not as a substitute for reading the code.
6. Implement or review with small, coherent changes. Keep unrelated refactors out of scope.
7. Finish with the exact validation performed and any remaining production risks.

## Hard Rules

- Do not introduce Vue, Angular, Next.js, Express-only services, MongoDB, MySQL, serverless-only deployment, or ad hoc shell deployment for new systems unless the user explicitly asks.
- Do not build demo-style internal UIs. Internal tools should be dense, calm, table/form/detail oriented, and usable for repeated operational work.
- Do not put business logic in React components, NestJS controllers, SQL strings scattered through handlers, or deployment scripts.
- Do not add Redis, queues, search engines, GraphQL, microservices, micro-frontends, or workflow engines without a concrete scaling, integration, or ownership reason.
- Do not hardcode secrets, database URLs, tokens, personal accounts, or environment-specific hostnames.
- Do not change database schema without a migration and rollback/compatibility notes.
- Do not mark a system production-ready without auth/RBAC assumptions, observability, resource limits, probes, deploy/rollback instructions, and critical-path tests.

## Expected Output

For design or generation tasks, output:

- Standard repo structure.
- Technology selection summary and exceptions.
- Engineering design with module boundaries and workflow design.
- Frontend page/module design.
- Backend module and API design.
- PostgreSQL schema and migration plan.
- Docker/K8s/deploy script plan.
- Key risks and validation plan.

For review tasks, output:

- Findings first, ordered by severity: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`.
- File and line references when available.
- Production decision: `pass`, `pass with follow-ups`, or `block`.
- Tests and checks actually run.

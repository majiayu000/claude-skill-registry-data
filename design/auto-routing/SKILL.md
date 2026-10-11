---
name: auto-routing
description: CLAUDE.md devteam section — opt-out rules and auto-routing triggers.
---

## CLAUDE.md Template — `## dev-team-agents` Section

Paste this block into the target project's `CLAUDE.md` (fill in values from setup Q&A):

```markdown
## dev-team-agents

PROJECT_TYPE: [new|inherited|maintenance]
TESTS_REQUIRED: [yes|no]
CICD_PLATFORM: [github-actions|bitbucket|gitlab|jenkins|other]
GRAPHIFY: [enabled|disabled]
BACKLOG_LOCATION: [local|github-issues|gitlab-issues|jira|linear|clickup|other]
CLOUD_PROVIDER: [aws|gcp|azure|vps|none]
ISSUE_TRACKER: [none|github-projects|jira|linear|clickup|trello|other]
ISSUE_TRACKER_ACCESS: read-only

### Agent Activation
- product-analyst: [active|inactive]
- software-architect: [active|inactive]
- backend-test-specialist: [active if TESTS_REQUIRED=yes]
- frontend-test-specialist: [active if TESTS_REQUIRED=yes]
- ui-ux-designer: [active — Design Mode on project start / Consultive Mode ongoing]
- devops-specialist: [active]

### Agent Opt-Out

To skip automatic routing for a single request, prefix the message with:
- `Without agents:` — the CLI's main agent handles the request directly, no sub-agents invoked
- `Skip routing:` — same effect
- `No agents:` — same effect

To disable routing permanently: add `AUTO_ROUTING: disabled` to this section.

---

### Auto-Routing: Planning

**MANDATORY:** You MUST use the Task tool to spawn these three agents **in parallel, before writing any code**, whenever any condition below is true. Do NOT plan inline — always delegate. The only exception is when the user explicitly asks not to use agents (see Agent Opt-Out above).

- Message contains: plan, design, architect, structure, approach, strategy, how should we build, how should we implement, break into tasks, break down, create backlog, define scope, requirements, PRD, spec, user stories, acceptance criteria, ADR, trade-offs, what's the best way to, should we use
- Task requires multiple subtasks or agents
- Business rules, flows, or scope are ambiguous
- User enters plan mode or asks for a plan before execution
- New feature or system is being designed from scratch

| Agent | Path | Role |
|---|---|---|
| `product-analyst` | `.claude/agents/dev-team/product-analyst.md` | Scope closure, acceptance criteria, backlog generation |
| `software-architect` | `.claude/agents/dev-team/software-architect.md` | System design, trade-offs, API contracts, ADR authoring |
| `database-specialist` | `.claude/agents/dev-team/database-specialist.md` | Data modeling, schema decisions, migration planning |

Execution begins only after the plan is approved by the user.

---

### Auto-Routing: Execution

**MANDATORY:** You MUST use the Task tool to spawn the named agent for every implementation task. Do NOT write code directly in the main context — always delegate to the agent whose scope matches. Independent scopes may run in parallel. The only exception is when the user explicitly asks not to use agents (see Agent Opt-Out above).

#### `backend-developer` → `.claude/agents/dev-team/backend-developer.md`
- **Keywords:** API, endpoint, route, controller, action, service, use case, interactor, repository, DAO, middleware, guard, interceptor, worker, job, queue, cron, scheduler, webhook, integration, SDK, REST, GraphQL, gRPC, auth, authentication, authorization, JWT, OAuth, session, business logic, domain, entity, aggregate, event, command, handler, server-side, backend
- **Files:** `*.php`, `*.py`, `*.go`, `*.java`, `*.rb`, `*.cs`, `*.rs`, `app/`, `src/`, `lib/`, `internal/`, `cmd/`, `api/`, `services/`, `domain/`, `infrastructure/`

#### `frontend-developer` → `.claude/agents/dev-team/frontend-developer.md`
- **Keywords:** component, page, view, screen, layout, template, form, input, button, modal, dialog, drawer, dropdown, table, list, card, navigation, menu, sidebar, header, footer, hook, composable, state, store, context, animation, transition, CSS, style, responsive, mobile, a11y, SPA, SSR, SSG
- **Files:** `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.html`, `*.css`, `*.scss`, `*.sass`, `*.less`, `pages/`, `components/`, `views/`, `layouts/`, `composables/`, `hooks/`, `stores/`

#### `ui-ux-designer` → `.claude/agents/dev-team/ui-ux-designer.md`
- **Keywords:** design system, component library, design token, color palette, color scheme, typography, font, spacing, grid, UX flow, user flow, wireframe, mockup, prototype, visual consistency, look and feel, brand, contrast, icon, illustration, design spec, Figma, Storybook
- In Consultive Mode (alongside `frontend-developer`): spawn whenever the task involves visual decisions or design system adherence.

#### `database-specialist` → `.claude/agents/dev-team/database-specialist.md`
- **Keywords:** migration, schema, table, column, index, foreign key, constraint, relation, join, query, stored procedure, view, trigger, seed, fixture, ORM model, normalization, denormalization, database design, database choice, N+1, slow query, explain plan, replication, sharding, partitioning, Redis, cache invalidation, Elasticsearch
- **Files:** `migrations/`, `*.sql`, `*.prisma`, `schema.rb`, `database/`, `db/`

#### `devops-specialist` → `.claude/agents/dev-team/devops-specialist.md`
- **Keywords:** Docker, Dockerfile, docker-compose, container, registry, CI/CD, pipeline, GitHub Actions, GitLab CI, Bitbucket Pipelines, Jenkins, CircleCI, deploy, deployment, release, rollback, env vars, secrets, Kubernetes, k8s, Helm, Terraform, Ansible, Pulumi, AWS, GCP, Azure, VPS, nginx, load balancer, SSL, TLS, DNS, CDN, monitoring, observability, Prometheus, Grafana, Datadog, infrastructure as code
- **Files:** `Dockerfile`, `docker-compose*.yml`, `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `*.tf`, `kubernetes/`, `k8s/`, `helm/`, `ansible/`

---

### Auto-Routing: Quality Gate

**MANDATORY:** After any execution agent completes work, you MUST spawn the appropriate quality gate agents via the Task tool. Do NOT skip this step. The only exception is when the user explicitly asks not to use agents (see Agent Opt-Out above).

#### `backend-test-specialist` → `.claude/agents/dev-team/backend-test-specialist.md`
Spawn when: `TESTS_REQUIRED=yes` and `backend-developer` completed work this session, or user asks: write tests, unit tests, integration test, test coverage, test the service/API/repository.

#### `frontend-test-specialist` → `.claude/agents/dev-team/frontend-test-specialist.md`
Spawn when: `TESTS_REQUIRED=yes` and `frontend-developer` completed work this session, or user asks: component tests, E2E test, Cypress, Playwright, Testing Library, Vitest, Jest (frontend context).

#### `code-reviewer` → `.claude/agents/dev-team/code-reviewer.md`
Spawn when: review, code review, review this PR, review the diff, check the code, audit the code, or before merging. Routes internally to `backend-reviewer`, `frontend-reviewer`, or both.

#### `security-specialist` → `.claude/agents/dev-team/security-specialist.md`
Spawn when: security audit, security review, check for vulnerabilities, OWASP, is this secure, pentest, threat model, CVE, XSS, SQL injection, CSRF, sensitive data, LGPD, GDPR, or before any production release involving auth, payments, or user data.

#### `qa-specialist` → `.claude/agents/dev-team/qa-specialist.md`
Spawn when: QA, validate this feature, test behavior, acceptance test, regression test, does this work correctly, end-to-end validation, test the flow. Run after implementation agents complete, before shipping.

#### `technical-writer` → `.claude/agents/dev-team/technical-writer.md`
Spawn when: document, write documentation, generate docs, README, API docs, runbook, playbook, changelog, release notes, architecture guide, write a guide. Run after shipping a feature or completing a significant change.

### Workflow
[A: new project | B: inherited | C: maintenance]

### Language
All generated documents must be in English unless explicitly overridden per document.
```

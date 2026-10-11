---
name: spawn-classifier
description: Conditional agent spawn — path patterns and text triggers.
---

## File-Path Triggers

Evaluate changed files (from `git diff --name-only` or the task description) against these patterns:

| Changed path pattern | Agent to spawn |
|---|---|
| `*.{go,py,rb,php,java,kt,rs}` | `backend-developer` |
| `app/Http/`, `app/Services/`, `src/controllers/`, `routes/` | `backend-developer` |
| `*.{tsx,jsx,vue,svelte}` | `frontend-developer` |
| `src/components/`, `src/pages/`, `resources/js/`, `app/javascript/` | `frontend-developer` |
| `database/migrations/`, `db/migrate/`, `prisma/`, `*.sql` | `database-specialist` |
| `.github/workflows/`, `Dockerfile*`, `docker-compose*.yml` | `devops-specialist` |
| `*.tf`, `*.tfvars`, `Pulumi.yaml`, `serverless.yml` | `devops-specialist` |
| `Jenkinsfile`, `.gitlab-ci.yml`, `*.circleci/` | `devops-specialist` |
| `*.spec.{ts,tsx,js}`, `*.test.{ts,tsx,js}`, `tests/`, `spec/` (frontend) | `frontend-test-specialist` |
| `*.spec.{py,rb,go,java,kt}`, `tests/`, `spec/` (backend) | `backend-test-specialist` |
| `*.stories.{ts,tsx,js}`, `storybook/`, `.storybook/` | `frontend-developer` + `ui-ux-designer` |

---

## Text / Intent Triggers

Evaluate the task description or user message:

| Keyword or phrase | Agent to spawn |
|---|---|
| "security", "vulnerability", "CVE", "auth bypass", "injection", "XSS", "CSRF" | `security-specialist` |
| "penetration test", "threat model", "OWASP" | `security-specialist` + `software-architect` |
| "test", "spec", "coverage", "unit test", "integration test" (frontend context) | `frontend-test-specialist` |
| "test", "spec", "coverage", "unit test", "integration test" (backend context) | `backend-test-specialist` |
| "design", "UX", "wireframe", "mockup", "user flow", "component library" | `ui-ux-designer` |
| "design system", "token", "Figma" | `ui-ux-designer` + `frontend-developer` |
| "SEO", "meta tag", "structured data", "sitemap", "Core Web Vitals", "llms.txt", "GEO", "otimização para IA/LLM" | `seo-specialist` |
| Project is a public site, landing page, e-commerce/online store, or blog (see `skills/design/seo-optimization/SKILL.md` § Detection Signals) | `seo-specialist` alongside `frontend-developer`/`ui-ux-designer` |
| "database", "schema", "migration", "index", "query", "ORM" | `database-specialist` |
| "deploy", "CI/CD", "pipeline", "Docker", "Kubernetes", "infra" | `devops-specialist` |
| "architecture", "ADR", "design decision", "trade-off", "system design" | `software-architect` |
| "API", "REST", "GraphQL", "endpoint", "service" | `backend-developer` |
| "bug", "fix", "regression", "broken", "error" | context-dependent — see Default below |

---

## Multi-Agent Combinations

Some tasks require more than one agent. Spawn in parallel when there are no dependencies:

| Scenario | Agents |
|---|---|
| Full-stack feature | `backend-developer` + `frontend-developer` + optionally `database-specialist` |
| Security audit | `security-specialist` + `software-architect` |
| New API endpoint with UI | `backend-developer` → `frontend-developer` (sequential — API first) |
| Database schema + migration | `database-specialist` → `backend-developer` (sequential — schema first) |
| Test-only task (both layers) | `backend-test-specialist` + `frontend-test-specialist` (parallel) |
| PR review | `code-reviewer` + `security-specialist` + optionally `database-specialist` |

---

## Conflict Resolution

When a changed file matches multiple patterns:

1. **Most specific pattern wins.** `src/controllers/UsersController.ts` matches both frontend (`src/`) and backend (controller) — the `controllers/` pattern is more specific, so spawn `backend-developer`.
2. **When genuinely ambiguous**, spawn `software-architect` first to classify and produce a plan.
3. **Never spawn an agent for a domain not touched by the task** — even if the agent is "usually helpful".

---

## Default Rule

When scope is unclear — no strong file-path or text match — **ask before spawning**, per the Quiz-first Rule (`skills/shared/interaction-patterns/SKILL.md`):

1. Use `AskUserQuestion` (single-select) offering the likely domains: Backend, Frontend, Database, DevOps, Security, Architecture, and "Not sure — let an agent classify it."
2. If the user picks a domain, spawn the matching agent directly — no classification agent needed.
3. Only if the user picks "Not sure" does this fall back to spawning `software-architect` first to analyze the task and produce a plan that identifies which domains are affected; downstream agents are then spawned from that plan.

This avoids paying for a full reasoning-tier agent invocation just to classify an ambiguous request, while still preventing incorrect agents from producing work that conflicts with the actual architecture when the user genuinely doesn't know.

---

## Classification Checklist

- [ ] Run `git diff --name-only HEAD~1` to get changed files
- [ ] Match files against path-pattern table above
- [ ] Match task description against text-trigger table above
- [ ] Identify parallel vs. sequential spawn order
- [ ] If ambiguous, spawn `software-architect` first

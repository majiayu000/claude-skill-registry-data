---
name: task-router
description: 'Meta-skill orchestrator for HIVMeet frontend and backend. Load this FIRST when uncertain which skill applies. Routes development and governance lifecycle work to the appropriate specialized skill.'
argument-hint: 'Describe your task or request in one sentence.'
user-invocable: true
---

# Task Router — HIVMeet Skill Orchestrator

## Purpose
Single entry point to route any HIVMeet development request to the correct project skill without guessing.

Use this when:
- The task type is ambiguous or spans multiple domains
- Starting a new session without a clear category
- Multiple skills could plausibly apply

After selecting the right skill(s), immediately load the corresponding `SKILL.md` via `read_file` and follow its workflow from start to finish.

---

## Skill Registry

All skills are at `.agents/skills/<name>/SKILL.md` in this repository.

| Task type / trigger keywords | Skill to load | Priority |
|------------------------------|---------------|----------|
| Build page, widget, screen, navigation, BLoC, Cubit, state, feature, animation, module | `frontend-development` | High |
| Bug, error, crash, exception, blank screen, regression, unexpected behavior, anomaly, performance | `bug-fixing` | High |
| API, endpoint, DTO, contract, payload, JSON mapping, 4xx/5xx, mismatch, integration, data source | `api-contract-audit` | High |
| Backend endpoint, DRF, ViewSet, serializer I/O, status code mapping, filtering, pagination | `drf-api-development` | High |
| Input validation, serializer rules, sanitize, error schema, domain constraints | `serializer-validation` | High |
| Permissions, authz, owner checks, premium gating, rate limiting, privacy-safe logging | `security-permissions` | High |
| Firebase token verification, firebase-exchange, JWT refresh/logout, user sync | `firebase-auth-sync` | High |
| Django model change, migration, backfill, integrity, rollback | `migrations-data-integrity` | High |
| Celery, Redis, background tasks, retry, idempotency, async reliability | `celery-redis-reliability` | Medium |
| Backend tests, pytest selection, risk-based validation, API test strategy | `backend-testing-strategy` | Medium |
| Slow query, N+1, indexing, ORM optimization, endpoint latency tuning | `performance-query-tuning` | Medium |
| Backend release candidate, deployment confidence, operational gate | `backend-release-readiness` | Medium |
| Production incident, emergency patch, mitigation, rollback | `backend-incident-hotfix` | High |
| Translation, i18n, hardcoded string, ARB, FR/EN, localization, missing key | `i18n-integrity` | Medium |
| Before merge, validate changes, non-regression, risk assessment, impact analysis | `regression-guard` | Medium |
| Release, deploy, checklist, readiness, quality gate, production, build | `release-readiness` | Medium |
| Which tests to run, test scope, test selection, changed files, test impact | `test-impact-selection` | Medium |
| Debug issue, trace error, investigate exception, graph-assisted diagnosis | `debug-issue` | High |
| Explore codebase, understand structure, map dependencies, read unfamiliar code | `explore-codebase` | Medium |
| Refactor safely, rename, restructure, dead code, safe code evolution | `refactor-safely` | Medium |
| Review changes, diff, PR review, change impact, code quality gate | `review-changes` | Medium |
| Agent governance, skills, adapters, hooks, lifecycle, activation, cross-root map | `hivmeet-governance` | High |

---

## Multi-Skill Scenarios

Load at most 2 skills. Secondary only when the task genuinely crosses two domains.

| Scenario | Primary skill | Secondary skill |
|----------|---------------|-----------------|
| New feature with user-facing text | `frontend-development` | `i18n-integrity` |
| Bug caused by API mismatch | `bug-fixing` | `api-contract-audit` |
| Feature ready for merge | `frontend-development` | `regression-guard` |
| New endpoint integration | `api-contract-audit` | `frontend-development` |
| New backend endpoint with strict validation | `drf-api-development` | `serializer-validation` |
| Firebase/JWT auth defect | `firebase-auth-sync` | `security-permissions` |
| Risky data model evolution | `migrations-data-integrity` | `backend-testing-strategy` |
| Celery task reliability issue | `celery-redis-reliability` | `backend-testing-strategy` |
| Backend performance degradation | `performance-query-tuning` | `backend-testing-strategy` |
| Backend pre-release validation | `backend-release-readiness` | `backend-testing-strategy` |
| Production backend incident | `backend-incident-hotfix` | `backend-testing-strategy` |
| Release branch preparation | `release-readiness` | `regression-guard` |
| Post-fix test selection | `bug-fixing` | `test-impact-selection` |
| Agent governance installation or audit | `hivmeet-governance` | `hivmeet-backend-completion-audit` |

---

## Decision Process

1. **Read the request** — identify dominant action (build / fix / secure / sync-auth / migrate / async / test / optimize / release / incident).
2. **Match the table above** — pick one primary skill; add a secondary only if the scenario clearly matches the multi-skill table.
3. **Load skill(s)** — call `read_file` on `.agents/skills/<name>/SKILL.md` immediately.
4. **Execute** — follow the loaded skill workflow from step 1 to completion.

---

## Hard Rules

- Never load more than 2 skills simultaneously.
- If backend scope is confirmed, prefer backend-specific skills over frontend-only skills.
- When uncertain between `bug-fixing` and `api-contract-audit`, default to `bug-fixing` as primary.
- Do not restate routing logic once the target skill is loaded — delegate fully to it.
- **Backend API changes**: never skip contract verification against `docs/API_DOCUMENTATION.md`.
- **HIVMeet domain**: sensitive HIV/health data — always apply privacy-safe defaults; prefer small reversible changes with explicit validation.
- **Language**: respond in French for project consistency.

---

## Quick Skill Summaries

| Skill | 10-word summary |
|-------|-----------------|
| `frontend-development` | Flutter/Dart features: Clean Architecture, BLoC, i18n, spec compliance |
| `bug-fixing` | Reproduce → diagnose → fix with root-cause and non-regression checks |
| `api-contract-audit` | Validate endpoint contracts, DTO mapping, error paths before merge |
| `drf-api-development` | Build DRF endpoints with strict contract and status discipline |
| `serializer-validation` | Enforce robust input validation and safe, predictable error responses |
| `security-permissions` | Apply authz, privacy, abuse controls, and secure endpoint defaults |
| `firebase-auth-sync` | Stabilize Firebase verification, Django sync, and JWT session lifecycle |
| `migrations-data-integrity` | Evolve schema/data safely with integrity checks and rollback planning |
| `celery-redis-reliability` | Build reliable async tasks with retries, idempotency, observability |
| `backend-testing-strategy` | Select high-value backend tests by risk and changed behavior |
| `performance-query-tuning` | Optimize ORM/query latency with measurable before/after validation |
| `backend-release-readiness` | Backend go/no-go gate across contract, security, data, operations |
| `backend-incident-hotfix` | Fast, safe incident remediation with rollback-ready emergency patching |
| `i18n-integrity` | Detect hardcoded strings, ensure FR/EN ARB parity, fix translation gaps |
| `regression-guard` | Risk-scored validation of critical user journeys before merge |
| `release-readiness` | Pre-release quality gate: build, analyze, test, privacy, contract safety |
| `test-impact-selection` | Select minimal high-value tests for the current set of file changes |
| `debug-issue` | Graph-assisted root-cause diagnosis with full call-chain context |
| `explore-codebase` | Navigate and map codebase structure via knowledge graph queries |
| `refactor-safely` | Dependency-aware refactoring with impact radius and rollback plan |
| `review-changes` | Structured diff/PR review using change detection and impact scoring |
| `hivmeet-governance` | Maintain maps, adapters, hooks and deterministic lifecycle checks |
| `hivmeet-backend-orchestrator` | Route Django work and identify frontend dependencies |
| `hivmeet-backend-completion-audit` | Audit contracts, security, migrations, privacy and evidence |

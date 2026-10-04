---
name: notepad-architecture-overview
description: "Reference doc: Simpler.Grants.gov — Architecture Overview"
---

# Simpler.Grants.gov — Architecture Overview

> Condensed from the full 50KB architecture guide at `documentation/architecture-guide.md`

## Mission

Simpler.grants.gov modernizes the federal Grants.gov portal. Three pillars: **easy** (lower friction), **accessible** (all communities), **transparent** (work in the open). Fully open-source (CC0 public domain).

Coexists with legacy Grants.gov — data flows Oracle → PostgreSQL via AWS DMS. Grant application XML must match legacy formats exactly.

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| API | Python + Flask/APIFlask | Accessible, open-source, Nava template |
| Frontend | Next.js + TypeScript (App Router, RSC) | SSR for auth pages, large community |
| Database | PostgreSQL on Amazon RDS | Advanced features, open-source |
| Search | OpenSearch | Open-source (post-Elastic license change) |
| Infra | Terraform + Docker on AWS ECS Fargate | FedRAMP compliance, Nava templates |
| Observability | New Relic APM + CloudWatch | FedRAMP authorized |
| Design System | USWDS via react-uswds | Legally required (21st Century IDEA) |

## Monorepo Structure

```
HHS/simpler-grants-gov/
  api/src/
    api/          — Route handlers & schemas (by domain)
    services/     — Business logic (by domain)
    db/           — Models & migrations
    auth/         — Authentication
    form_schema/  — Grant application forms
  frontend/src/
    components/   — Domain-based organization
    hooks/        — Custom hooks
    services/     — API integration
    i18n/         — Internationalization
  infra/          — Terraform (3-layer: app-config/service/database)
  documentation/  — ADRs, goals, guides
```

## API Architecture (layered, strict separation)

1. **Routes** — THIN handlers only. Accept request → call service → return response. Immutable decorator stack: HTTP method → input → output → doc → auth → db_session.
2. **Services** — Business logic. Accept `db_session` as first param. Do NOT manage transactions (routes do that).
3. **Database** — SQLAlchemy 2.0 `Mapped[T]`. UUID PKs, singular table names, `ApiSchemaTable` + `TimestampMixin`. Four-layer lookup pattern for enums.
4. **Errors** — All flow through `raise_flask_error()` with `ValidationErrorDetail`. The `type` field (StrEnum) is the API↔frontend contract.
5. **Auth** — JWT + API key multi-auth via `MultiHttpTokenAuth`. RBAC via `verify_access()`.

## Frontend Architecture

- **Server-first**: RSC by default, `"use client"` only when needed
- **Domain-based** component organization (not by type). No barrel files.
- **Data fetching**: `requesterForEndpoint()` factory, `cache()` for deduplication, Promise-as-props pattern
- **Client fetching**: `useClientFetch` hook wrapping `requesterForEndpoint()`
- **i18n**: Single centralized file (`messages/en/index.ts`), `useTranslations()` hook
- **Design**: USWDS components, wrapped in project-specific components for SSR safety

## Testing

- **API**: pytest, factory `.build()` (unit) / `.create()` (integration, needs `enable_factory_create`), standalone functions
- **Frontend**: Jest + RTL + jest-axe (accessibility required), Playwright E2E (4 shards)
- Tests ship in the same PR as the code

## Key Constraints

- **FedRAMP** — hard requirement for all infra/observability tools
- **USWDS** — legally required design system
- **Legacy coexistence** — XML compatibility, Oracle data replication
- **Open-source** — CC0, prefer OSS dependencies, "can an external contributor replicate this?"

## Review Authority

- API (database, logging, auth, patterns): chouinar
- Frontend (components, i18n, style): doug-s-nava
- Infrastructure: chouinar (env/secrets), sean-navapbc (Terraform), mdragon (CI/CD)

---
name: docs
description: Documentation maintenance guide. Use when making code changes that affect APIs, features, patterns, or architecture to keep documentation in sync.
paths:
  - packages/tereo/src/routes/**
  - packages/tereo/src/definitions/**
  - packages/tereo/src/env.ts
  - packages/tereo/src/telemetry/**
  - packages/tereo/prisma/schema.prisma
  - packages/tereo/openapi/**
  - packages/tereo/docs/**
  - packages/tereo-sdk/src/**
  - docs/**
  - docker-compose.yml
  - docker/**
---

# Documentation Maintenance

When making code changes, check whether related documentation needs updating.

tereo is one service (`packages/tereo`) plus libraries, so most docs are either
repo-wide or per *area* of that service — auth, files, webhooks, audit, registry, telemetry.

## What to Update When

### Backend Route Changes (add/modify/remove endpoints)

- [ ] OpenAPI path file for the area: `packages/tereo/openapi/paths/{auth,files,webhooks,audit}/{resource}.yaml`
- [ ] OpenAPI schemas: `packages/tereo/openapi/components/{area}/schemas.yaml`
- [ ] Reference the new path in the one root, `packages/tereo/openapi/openapi.yaml`
- [ ] Area doc: `packages/tereo/docs/{area}.md` (if it lists endpoints or the behavior changes)
- [ ] SDK: a request in `packages/tereo-sdk/src/requests/{area}/` and a method on its client in
      `src/clients/`, if app services should call it; then `packages/tereo-sdk/docs/{area}.md`

Then `npm run openapi:build` in `packages/tereo` (see the `openapi` skill).

### Database Schema Changes (Prisma models)

- [ ] Area doc: `packages/tereo/docs/{area}.md` (the *Database* / *Database Schema* /
      object-model sections, where present)
- [ ] Root `CLAUDE.md` *Migrations* convention, if the change needs a new kind of raw SQL
      (partitioning, partial or opclass indexes, CHECK constraints)

### Declarations (permissions, system roles, buckets, event types)

All of these live in `packages/tereo/src/definitions/` and are registered on every start.

- [ ] Permission or system role: the endpoint's **Required permissions** in the OpenAPI spec, and the
      *Permissions* section of `packages/tereo/docs/{area}.md`
- [ ] Event type: a webhook definition in the OpenAPI spec (`openapi/paths/{area}/` + the root `webhooks:`), and
      `packages/tereo/docs/webhooks.md` if delivery changes
- [ ] Declaration rules (namespaces, access, retirement) and the provisioning documents (`provisioning.md`): `packages/tereo/docs/registry.md`

### Webhook / Audit Changes

- [ ] Webhooks: `packages/tereo/docs/webhooks.md` (event emission flow, delivery, signing)
- [ ] Audit: `packages/tereo/docs/audit.md` (entry shape, idempotency, retention)
- [ ] Outbox behavior: the `outbox` skill (`.claude/skills/outbox/SKILL.md`) and the *Outbox*
      section of `packages/tereo-sdk/README.md`

### Auth / Setup Changes

- [ ] Auth area doc: `packages/tereo/docs/auth.md`
- [ ] First boot, keys or setup token: root `README.md` (*Run it*) and root `CLAUDE.md`
      (*Local development* → *Keys*)

### SDK Changes (`@tereo-io/sdk`)

- [ ] `packages/tereo-sdk/README.md` — usage, provisioning types, outbox, the layout table
- [ ] Per-area notes: `packages/tereo-sdk/docs/{auth,files,webhooks,audit}.md`
- [ ] Root `CLAUDE.md` *Where this is heading* if the SDK's shape changes

### Environment, Telemetry, Process Roles

- [ ] New or changed env var: `packages/tereo/src/env.ts` is the schema; also
      `packages/tereo/.env.example` and the *Environment Variables* section of the area doc
- [ ] Telemetry: `packages/tereo/docs/telemetry.md`
- [ ] `ROLE`, entry points, background jobs: root `CLAUDE.md` layout table; *Background Jobs* in
      `packages/tereo/docs/webhooks.md` for delivery workers

### Architecture / Roadmap Changes

- [ ] Root `CLAUDE.md` — project overview, layout table, key conventions, what not to do
- [ ] Root `README.md` — packages table, *Run it*, *Develop*, *Current state* (what works / what's
      not done)
- [ ] Local stack: `docker-compose.yml`, `docker/` and the commands in root `README.md`/`CLAUDE.md`

### Code Style / Tooling Changes

- [ ] `docs/code-style.md` (Prettier, import order, ESLint, comments)

## Documentation Locations

| Type | Location | Purpose |
|------|----------|---------|
| Root CLAUDE.md | `CLAUDE.md` | Claude Code guidance: layout, key conventions, local development, what not to do |
| Root README.md | `README.md` | Overview, packages, run/develop, current state, roadmap links |
| Code style | `docs/code-style.md` | Formatting, TypeScript, naming, errors, import order |
| Area docs | `packages/tereo/docs/*.md` | `auth`, `files`, `webhooks`, `audit`, `registry`, `telemetry` |
| OpenAPI spec | `packages/tereo/openapi/` | API contract, one spec for every area (`paths/{area}/`) |
| SDK docs | `packages/tereo-sdk/README.md`, `docs/*.md` | How app services use core |
| Skills | `.claude/skills/*/SKILL.md` | Task guides for Claude Code (`outbox`, `openapi`, `docs`, …) |

There is no `packages/tereo/CLAUDE.md` or `README.md` — the root files cover the service.

## Guidelines

- Only update docs that are actually affected by the change — don't update everything
- Keep CLAUDE.md files focused on implementation-level guidance (what Claude needs to know)
- Keep README.md files focused on human readers (setup, usage)
- Keep area docs focused on how that area behaves; cross-cutting decisions go in root `CLAUDE.md`
- The OpenAPI spec is the contract for endpoints — update it with the route, not afterwards
- When a doc section no longer matches the code, correct it to match the code rather than copying
  its pattern

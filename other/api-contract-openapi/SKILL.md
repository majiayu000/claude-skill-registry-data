---
name: api-contract-openapi
category: api
description: Use when you add or change any HTTP endpoint's request or response shape (Go or Java) — implement the task's contract exactly, evolve additively, keep the OpenAPI document in sync, and detect breaking changes before hand-off
---
# OpenAPI & API Contracts

## Overview

The API contract is a promise the web and mobile clients depend on. A silent shape change (renamed field, changed type, removed endpoint) compiles fine on the backend and breaks every consumer at runtime.

**Core principle:** the contract is the annotation + DTO in code. Implement the task's contract exactly, evolve it additively, and never edit a consumer yourself.

## Your task's contract is already copied into the consumer tasks

Your task's Interfaces / contract block is already copied, word for word, into the consumer tasks (the architect writes it once and copies it to the frontend and mobile tasks, which are `blocked_by` and `deploy_depends_on` yours). Implement it exactly: path, method, field names and casing, types, status codes. A shape you think is better is a comment on your task, not a change.

Consumers are not yours to edit. Find them with `list_links` (direction `in`) and `grep_code` for the path or field. Another component's or repository's client code belongs to its own task, and cross-repository actions are refused. Keep your change additive. When a breaking change is truly required, `add_task_comment` naming every consumer task or component and what each must change, and stop short of the break.

## Detect the spec source

| Signal | Tooling |
|---|---|
| `//@Summary`/`//@Router` comments | swaggo (`swag init`; v1 emits Swagger 2.0 only) |
| `openapi.yaml`/`.json` + generated server stubs | oapi-codegen (spec-first, `go generate ./...`) |
| Go struct tags driving a schema, no annotations | huma or ogen |
| `@Operation`/`@Schema` on JAX-RS resources | springdoc-openapi / `quarkus-smallrye-openapi` — spec is generated at runtime; snapshot it at `/q/openapi` or `/v3/api-docs` |
| A hand-maintained `openapi.yaml` with no generator | edit it directly |

Keep the document's existing OpenAPI version (3.0/3.1/3.2 all current); upgrading the spec version is never part of a feature task.

## Additive vs breaking

| Change | Type | Action |
|--------|------|--------|
| Add optional field | Additive | Safe; document it |
| Add required request field | Breaking | Coordinate via the task's contract, never edit callers yourself |
| Rename field | Breaking | Prefer add-new + deprecate-old |
| Change field type | Breaking | New field or coordinated cutover |
| Remove endpoint/field | Breaking | Deprecate first, remove later |

## Breaking-change check

Diff the spec against the merge base before you finish:

```
git show "$(git merge-base HEAD origin/HEAD)":api/openapi.yaml > /tmp/base.yaml
go run github.com/oasdiff/oasdiff@latest breaking /tmp/base.yaml api/openapi.yaml
```

It must print nothing unless the task is the planned break. Lint with `npx --yes @redocly/cli lint api/openapi.yaml` when the repo has no linter already wired in.

## Every endpoint documented

Request/response schema, every status code it can return (including the error shape — see api-design-conventions), and pagination parameters where the endpoint lists anything.

## Worked Example

Task's contract: `POST /tasks` returns `{id, title, status}`. A later task wants to rename `title` to `name` for a different repository's consumer.

Wrong: rename the DTO field and ship — every client reading `title` breaks, and your task has no authority to touch their code.

Right (additive cutover):
1. Add `name` alongside `title` in the response; populate both. Document `title` as deprecated in the spec.
2. `add_task_comment` naming the consumer task(s)/component(s) that must switch to `name`.
3. In a later task — once the architect confirms no consumer reads `title` — remove it with a contract note.

Each step keeps every consumer green and respects task boundaries.

## Common Mistakes

- Implementing a shape you think is cleaner instead of the task's Interfaces block verbatim.
- Editing a consumer's client code because it was easy to find.
- A required new request field added with no coordinated consumer task.
- Spec left stale after a handler change, or `oasdiff` never run.

## Red Flags

- A DTO field renamed or removed with `oasdiff breaking` printing output.
- A diff that touches files outside your component/repository to "fix" a client.
- A consumer reading a field the backend just removed, with no deprecation step.

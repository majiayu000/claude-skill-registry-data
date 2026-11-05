---
name: gateway-api
description: Route API design/implementation tasks to the right library skill.
type: gateway
tier: core
domains: [api, rest, graphql]
trigger: "REST API, GraphQL, endpoint, route, OpenAPI, Swagger, webhook, versioning, pagination"
---

## Purpose

You are the API Gateway. Route API tasks to specialized library skills.

## Intent Detection → Skill Routing

| Intent Keywords | Load Skill |
|---|---|
| `openapi`, `swagger`, `api spec`, `api schema` | `skills/library/api/openapi-design/SKILL.md` |
| `graphql`, `resolver`, `mutation`, `query`, `subscription` | `skills/library/api/graphql-patterns/SKILL.md` |
| `versioning`, `v1`, `v2`, `breaking change`, `deprecat` | `skills/library/api/api-versioning/SKILL.md` |
| `pagination`, `cursor`, `offset`, `infinite scroll` | `skills/library/api/pagination-patterns/SKILL.md` |
| `webhook`, `callback`, `event-driven`, `notify` | `skills/library/api/webhook-design/SKILL.md` |
| `validation`, `sanitize`, `input`, `schema` | `skills/library/api/input-validation/SKILL.md` |

## Output Format

```
GATEWAY_API:
Domain: api
Skills to load:
  - [absolute/path/to/SKILL.md]

Instructions: Read the above skill files before proceeding with your task.
```

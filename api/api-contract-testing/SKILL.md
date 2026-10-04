---
name: api-contract-testing
category: qa
description: Use when a task adds or changes an HTTP endpoint, its request/response shape, status codes, auth or error format - the request matrix, curl templates and what counts as a contract break
---
# API Contract Testing

## Contract source

The task, its acceptance criteria and the spec document first; then the repo's OpenAPI file or README API docs (the named boot-docs exception). Never the handler source — a contract derived from the implementation only proves the implementation matches itself.

## Request template

```bash
curl -sS -D "$QA/h.txt" -o "$QA/b.json" -w '%{http_code} %{time_total}s\n' -X POST "$BASE/api/tasks" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d '{"title":"qa-T-12 a"}'; jq . "$QA/b.json"
```

## Per changed endpoint, the matrix

One case each, mapped to the category enum:

| Case | Category |
|---|---|
| 2xx happy path | `happy_path` |
| 400/422 for invalid body, with the error payload shape | `negative` |
| 401 no token | `auth` |
| 403 other user's resource (BOLA: create as A, read/update/delete as B) | `auth` |
| 404 unknown id | `negative` |
| 409 duplicate where uniqueness is implied | `negative` |
| 405 wrong method | `negative` |
| extra unknown/privileged field ignored, e.g. `"role":"admin"` (mass assignment) | `auth` |
| pagination edges (limit 0, max, max+1) | `boundary` |
| idempotency: PUT/DELETE twice, POST with `Idempotency-Key` twice when claimed | `negative` |
| content-type (missing, wrong) | `negative` |

## Compatibility

Existing fields keep their name, type and nullability. A removed or renamed field is a break unless the task explicitly asks for it. Compare against the OpenAPI file, or a request to the same endpoint on stage/the default branch.

## Side effects

Verify them the same way backend-manual-testing does — a 2xx with the wrong DB row or missed outbound call is a FAIL, not a pass with a note.

## Optional depth: schema fuzzing

Local boot only, and only when the repo ships an OpenAPI file:

```bash
uvx schemathesis run <openapi> --url <base> -H "Authorization: Bearer $TOKEN" --include-path-regex '<changed path>' --checks not_a_server_error,status_code_conformance,response_schema_conformance --max-examples 20 --max-failures 5
```

Scope it to the changed paths with `--include-path-regex`. Never run it against stage or anything shared — it generates many writes.

## Worked Example

"POST /tasks title ≤120 chars": happy path (120 chars, 201); empty title (422); 121 chars (422); no auth (401); another user's project (403); duplicate title where unique (409 or 201 per spec); wrong Content-Type (415/400); unknown field `is_admin:true` ignored (201, field absent from response) — 8 cases, each with its expected code recorded before running it.

## Red Flags

- Asserting only the status code and never the body shape.
- Testing authz with the same user for both sides of a BOLA case.
- Fuzzing a shared environment (stage, a shared database).

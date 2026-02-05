---
name: api-protocol
description: API protocol guide for Sunrei project. Use when writing API endpoints, request/response type naming, and HTTP method conventions.
---

# API Protocol Guide

RESTful API + OpenAPI 3.0 spec

- Request type: `{HttpMethod}{Name}Params` (e.g., `GetUserParams`, `ListUsersParams`)
- Response type: `{HttpMethod}{Name}Result` (e.g., `GetUserResult`, `ListUsersResult`)

## HTTP Method Rules

- `GET` + singular → single item (e.g., `GET /sunreis/{id}`)
- `List` + plural → list items (e.g., `GET /sunreis`)
- `POST` → create
- `PUT` → full update
- `PATCH` → partial update
- `DELETE` → delete

## Response Format

- Success: `{ "data": ... }` or domain key (e.g., `{ "sunreis": [...] }`)
- Error: `{ "error": { "code": "...", "message": "..." } }`
- Pagination: `{ "items": [...], "nextToken": "..." }`

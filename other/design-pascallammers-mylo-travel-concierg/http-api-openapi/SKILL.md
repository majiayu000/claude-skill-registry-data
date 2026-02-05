---
name: http-api-openapi
description: Keep HTTP handlers and OpenAPI (openapi.yaml) in sync. Use when adding/changing endpoints, request/response schemas, auth requirements, or error shapes.
license: MIT
compatibility: Requires bash, git, Go; optional Node/npm + swagger-cli for validation.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.2
allowed-tools: Bash(git:*) Bash(make:*) Bash(go:*) Bash(npm:*) Bash(swagger-cli:*) Read
---

## Tooling assumptions

- Use a terminal runner with bash and git available.
- Prefer `make` targets when available; fall back to direct CLI commands when needed.

## Source of truth

- OpenAPI spec: `openapi.yaml` at the repo root.

## Typical workflow

1. Update `openapi.yaml` (paths, schemas, auth).
2. Validate the spec:

```bash
make validate-openapi
```

If `swagger-cli` isn’t installed:

```bash
npm install -g @apidevtools/swagger-cli
```

3. Implement the handler changes in Go (and keep auth consistent with the spec).
4. Run tests:

```bash
make test
```

## Project-specific notes

- Authenticated endpoints use Bearer token auth (see README’s Auth section).
- Be explicit about error responses and status codes in the spec when behavior changes.

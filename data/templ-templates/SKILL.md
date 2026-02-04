---
name: templ-templates
description: Edit and troubleshoot server-side HTML templates (.templ), including regeneration and handler wiring.
license: MIT
compatibility: Requires bash, git, Go, and templ.
metadata:
  repo: mjrwtf
  runner: github-copilot-cli
  version: 1.0
allowed-tools: Bash(git:*) Bash(make:*) Bash(go:*) Bash(templ:*) Read
---

## Where templates live
- Layouts: `internal/adapters/http/templates/layouts/*.templ`
- Pages: `internal/adapters/http/templates/pages/*.templ`

## Standard workflow
1. Edit `.templ` files.
2. Regenerate:

```bash
make templ-generate
# or (full): make generate
```

3. Run tests/build:

```bash
go build ./...
make test
```

## Handler wiring
- Handlers typically render templates from `internal/infrastructure/http/handlers/*`.
- Set content type: `text/html; charset=utf-8`.

## Common pitfalls
- Forgetting to run `templ generate` (compile errors referencing missing `*_templ.go`).
- Putting business logic in templates; keep logic in handlers/domain and pass data in.

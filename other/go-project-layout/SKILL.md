---
name: go-project-layout
description: "Guide for setting up Golang project layouts and workspaces. Covers CLI tools, libraries, services, and monorepos."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:30:00 GMT
---

## Directory Structure Best Practices

1. **cmd/** — Entry points (main packages). Each binary gets its own subdirectory: `cmd/myapp/main.go`.
2. **internal/** — Private library code. Code in this directory cannot be imported by other projects. This is where most business logic should live.
3. **pkg/** — Public library code. Only use this if you want others to import these packages.
4. **api/** — OpenAPI/Swagger specs, JSON schema files, protocol definition files.
5. **web/** — Web static assets, server-side templates, SPAs.
6. **configs/** — Configuration file templates or default configs.
7. **init/** — System init (systemd, upstart) and process manager (runit, supervisord) configs.
8. **scripts/** — Scripts for build, install, analysis, etc.
9. **build/** — Packaging and Continuous Integration.
10. **test/** — Additional external test apps and test data.
11. **docs/** — Design and user documents.

## Project Types

| Project Type | Key Directories |
| --- | --- |
| **CLI Tool** | `cmd/{name}/`, `internal/`, optional `pkg/` |
| **Library** | `pkg/{name}/`, `internal/` |
| **Service (API)** | `cmd/{service}/`, `internal/`, `api/` |
| **Monorepo** | `go.work`, separate modules in subdirectories |

## Module Naming (go.mod)

- **Must match repository URL**: `github.com/username/project-name`.
- **Lowercase only**: `github.com/user/my-app`.
- **Hyphens for multi-word**: `payment-processor`.

## Package Naming

- **Lowercase and singular**: `user`, `auth`, `http`.
- **Match directory name**.
- **Avoid "util" or "common"** — Be specific (e.g., `jsonutil`, `stringset`).

## Checklist for New Projects

- [ ] Run `go mod init github.com/user/repo`.
- [ ] Create `cmd/app-name/main.go`.
- [ ] Create `internal/` for business logic.
- [ ] Add `.gitignore` (ignoring binaries and vendor if not used).
- [ ] Add `golangci-lint` configuration.
- [ ] Initialize `git` and make initial commit.

## Anti-patterns

- ❌ **Massive `main.go`** — Keep `main` small, only for wiring and flag parsing.
- ❌ **Circular dependencies** — Result of poor package boundaries.
- ❌ **Deeply nested packages** — Go prefers a flatter structure.
- ❌ **Using `pkg/` for everything** — Most code should be in `internal/`.
- ❌ **Generic package names** — `logic`, `models`, `interfaces` are too vague.

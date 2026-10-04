---
name: go-dependency-management
description: "Best practices for Go modules, dependency updates, and vulnerability scanning."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:40:00 GMT
---

## Core Principles

1. **Commit `go.sum`** — It ensures reproducible builds and protects against supply-chain tampering.
2. **Standard Library First** — Always check if the standard library solves the problem before adding a dependency.
3. **Audit Regularly** — Use `govulncheck` to catch known vulnerabilities in your dependency tree.
4. **Tidy Often** — Run `go mod tidy` to keep `go.mod` and `go.sum` clean.
5. **Semantic Versioning** — Understand that Go modules follow SemVer (Major.Minor.Patch).

## Common Commands

| Command | Purpose |
| --- | --- |
| `go mod init <name>` | Initialize a new module. |
| `go mod tidy` | Add missing dependencies and remove unused ones. |
| `go get <pkg>@latest` | Add or update a package to the latest version. |
| `go get -u ./...` | Update all dependencies to the latest minor/patch version. |
| `go mod vendor` | Create a local copy of dependencies in `vendor/`. |
| `go mod verify` | Verify dependencies against `go.sum` checksums. |
| `go mod why -m <pkg>` | Explain why a specific module is in your dependency tree. |

## Vulnerability Scanning

Always run `govulncheck` before releasing code.

```bash
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...
```

## Version Selection Strategy

- **`go get -u=patch ./...`**: Safest way to update. Only applies bug fixes (patch versions).
- **`go get -u ./...`**: Updates to latest minor versions. May introduce new features or deprecations.
- **`replace` directive**: Use in `go.mod` for local development or patching broken upstream modules.

## tools.go Pattern

To pin versions of CLI tools (like linters or code generators) used in the project:

```go
//go:build tools
package tools

import (
    _ "github.com/golangci/golangci-lint/cmd/golangci-lint"
    _ "golang.org/x/vuln/cmd/govulncheck"
)
```

## Anti-patterns

- ❌ **Not committing `go.sum`** — Breaks build reproducibility.
- ❌ **Manual editing of `go.mod`** — Use `go get` or `go mod edit` instead.
- ❌ **Ignoring `govulncheck`** — Shipping known vulnerabilities to production.
- ❌ **Adding unnecessary dependencies** — Increases binary size and attack surface.
- ❌ **Using `@master` or `@main` versions** — Use specific version tags or commit hashes for stability.

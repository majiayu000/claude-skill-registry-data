---
name: go-module-paths
description: >
  Use this before generating any Go import statement, when creating Dockerfiles
  that build Go services, configuring Makefile build commands, or setting up
  CI build steps in a monorepo where go.mod is not at the repo root. Covers
  module-root derivation from go.mod, import path construction, Dockerfile COPY
  context, and the most common path mistakes.
  Triggers: go.mod, import path, monorepo, Dockerfile COPY, module root.
---



# Go Module Import Paths

Rules for deriving correct Go import paths in monorepo layouts where
`go.mod` is not at the repository root.

## When to Activate
- Before generating ANY Go import statement
- When creating Dockerfiles that build Go services
- When configuring Makefile build commands
- When setting up CI pipeline build steps
- Used by: code-generator, sdk-implementor, build-config-generator, deployment-generator

## Critical Rule: Module Root = go.mod Directory

The **module root** is the directory containing `go.mod`. All import paths
are relative to this directory.

### Step 1: Read go.mod

Before generating imports, ALWAYS read `go.mod` to get:
1. The **module path** (e.g., `module github.com/motadata/platform`)
2. The **file system location** of go.mod (e.g., `src/go.mod`)

### Step 2: Derive Import Paths

Import path = `<module-path>/<relative-path-from-module-root>`

```
Repository layout:
  repo-root/
    src/                          ← module root (contains go.mod)
      go.mod                      ← module github.com/motadata/platform
      pkg/errors/errors.go        ← import: github.com/motadata/platform/pkg/errors
      services/api-gateway/cmd/   ← import: github.com/motadata/platform/services/api-gateway/cmd
```

### Step 3: Verify — The Module Root Directory Name is NEVER in the Import Path

If `go.mod` is at `src/go.mod`, then `src/` is the module root.
The directory name `src` does NOT appear in import paths.

**CORRECT:**
```go
import "github.com/motadata/platform/services/api-gateway/internal/config"
import "github.com/motadata/platform/pkg/errors"
```

**WRONG (includes `src/` — the module root directory name):**
```go
import "github.com/motadata/platform/src/services/api-gateway/internal/config"
import "github.com/motadata/platform/src/pkg/errors"
```

## Common Mistakes

### Mistake 1: Including Module Root Directory in Import Path
```
go.mod location: src/go.mod
module path:     github.com/motadata/platform
file location:   src/services/identity-service/internal/domain/models.go

WRONG: github.com/motadata/platform/src/services/identity-service/internal/domain
RIGHT: github.com/motadata/platform/services/identity-service/internal/domain
```

The `src/` prefix creates a path that resolves to `src/src/services/...` which doesn't exist.

### Mistake 2: Using Repo-Root-Relative Paths Instead of Module-Root-Relative
If the repo has structure `myrepo/backend/go.mod`:
```
WRONG: github.com/org/myrepo/backend/pkg/auth
RIGHT: github.com/org/myrepo-backend/pkg/auth  (if module is github.com/org/myrepo-backend)
```

Always use the module path from go.mod, not the filesystem path from repo root.

### Mistake 3: Inconsistent Paths Across Services
When multiple agents generate code for different services, they may use different
import path conventions. All services MUST use the same derivation rule.

**Self-check**: After generating all imports for a service, verify:
```bash
cd <module-root-directory>
go build ./services/<service-name>/...
```

## Dockerfile Build Context

The Docker build context MUST include `go.mod`. The `COPY go.mod` command
must resolve to the actual `go.mod` file.

### Correct Pattern (go.mod at src/)
```dockerfile
# docker-compose.yml:
#   build:
#     context: ./src         ← build context is the module root
#     dockerfile: ../Dockerfile.services

FROM golang:1.26-alpine AS builder
WORKDIR /app
COPY go.mod go.sum* ./       # Copies src/go.mod (correct)
RUN go mod tidy -e && go mod download
COPY . .                      # Copies all of src/
RUN go build -o /out/service ./services/${SERVICE}/cmd/
#                              ^ path relative to module root, no src/ prefix
```

### Wrong Pattern
```dockerfile
# If build context is repo root but go.mod is in src/:
COPY go.mod go.sum ./         # Copies repo-root go.mod (wrong or nonexistent)
COPY . .
RUN go build -o /out/service ./src/services/${SERVICE}/cmd/
#                              ^ would need src/ prefix, and go.mod paths break
```

## Makefile Build Commands

All `go build`, `go test`, `go vet` commands must run from the module root:

```makefile
# If Makefile is at repo root and go.mod is at src/:
.PHONY: build
build:
	cd src && go build ./services/$(SERVICE)/...

# If Makefile is at src/ (module root):
.PHONY: build
build:
	go build ./services/$(SERVICE)/...
```

## Validation Checklist

Before marking code generation complete:
1. [ ] Read `go.mod` — noted module path and file location
2. [ ] All imports use `<module-path>/<path-relative-to-module-root>`
3. [ ] No import contains the module root directory name (e.g., no `/src/` in path)
4. [ ] `go build ./...` passes from the module root directory
5. [ ] Dockerfile COPY commands align with build context
6. [ ] All services use identical import path conventions

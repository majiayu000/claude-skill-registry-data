---
name: justfile-polyglot-patterns
description: Level 4 patterns - multi-language orchestration, root + subproject structure
---

# Polyglot Patterns (Level 4)

Multi-language projects. Root orchestration, subproject independence, clean delegation.

## Structure

```
my-project/
├── justfile              # Root orchestration
├── api/
│   ├── justfile          # Full interface (Python)
│   ├── pyproject.toml
│   └── src/
└── web/
    ├── justfile          # Full interface (JavaScript)
    ├── package.json
    └── src/
```

**Key principles:**
- Root orchestrates, doesn't duplicate
- Each subproject standalone
- `_run-all` helper for delegation
- Fails fast (exit on first failure)

## Root Justfile

Implements subset of interface. Delegates to subprojects.

```just
set shell := ["bash", "-uc"]

# Show all available commands
default:
    @just --list

# Install dependencies and setup development environment
dev-install:
    @just _run-all dev-install

# Run all quality checks
check-all:
    @just _run-all check-all

# Remove generated files
clean:
    @just _run-all clean

# Detailed complexity report
complexity:
    @just _run-all complexity

# Show N largest files
loc N="20":
    @just _run-all "loc {{N}}"

# Show outdated packages
deps:
    @just _run-all deps

# Check for vulnerabilities
vulns:
    @just _run-all vulns

# Analyze licenses
lic:
    @just _run-all lic

# Generate SBOM
sbom:
    @just _run-all sbom

# Build artifacts
build:
    @just _run-all build

# Helper: run command in all subprojects
_run-all CMD:
    #!/usr/bin/env bash
    for proj in api web; do
        echo "▸ $proj: just {{CMD}}"
        cd $proj && just {{CMD}} || exit 1
    done
```

**Customize:** Change `api web` to match your subprojects.

## Subproject Justfiles

Each implements full interface independently.

**api/justfile (Python):**
```just
# Full baseline interface
# See justfile-interface skill
# Uses Python stack (uv, ruff, mypy, pytest)
```

**web/justfile (JavaScript):**
```just
# Full baseline interface
# See justfile-interface skill
# Uses JavaScript stack (pnpm, prettier, eslint, vitest)
```

## Commands NOT at Root

Don't orchestrate all commands. Run directly in subprojects when:

**Subproject-specific:**
- `format`, `lint`, `typecheck` - Stack-specific, run as needed per project
- `test`, `coverage` - Different test suites, run separately
- `test-watch` - Must run in specific subproject

**Why:** Root orchestration for commands that validate whole project. Stack-specific commands run per-project.

## Usage

**Root level (full project):**
```bash
just dev-install    # Setup everything
just check-all      # All projects pass quality gates
just build          # Build all artifacts
```

**Subproject level (targeted):**
```bash
cd api && just test           # API tests only
cd web && just test-watch     # Web watch mode
```

## Pattern: _run-all Helper

Iterates subprojects, runs command, fails fast.

```just
_run-all CMD:
    #!/usr/bin/env bash
    for proj in api web; do
        echo "▸ $proj: just {{CMD}}"
        cd $proj && just {{CMD}} || exit 1
    done
```

**Key aspects:**
- Exit on first failure (`|| exit 1`)
- Visual feedback (`▸ $proj`)
- Works with any command

## Pattern: Polyglot SBOM

Generate SBOM per subproject.

```just
sbom:
    syft dir:./api -o cyclonedx-json > sbom-api.json
    syft dir:./web -o cyclonedx-json > sbom-web.json
```

**Scan all:**
```just
security-scan: sbom
    grype sbom:./sbom-api.json --fail-on critical
    grype sbom:./sbom-web.json --fail-on critical
```

## Pattern: Deployment Orchestration

Root handles deployment coordination.

```just
# Deploy everything
deploy environment="dev":
    @scripts/deploy/check-auth.sh {{environment}}
    @cd api && just deploy {{environment}}
    @cd web && just deploy {{environment}}

# Deploy API only
deploy-api environment="dev":
    @scripts/deploy/check-auth.sh {{environment}}
    @cd api && just deploy {{environment}}

# Deploy Web only
deploy-web environment="dev":
    @scripts/deploy/check-auth.sh {{environment}}
    @cd web && just deploy {{environment}}
```

## Pattern: Migration Orchestration

Root delegates to API (assuming API owns database).

```just
migrate:
    @cd api && just migrate

migrate-down:
    @cd api && just migrate-down

migrate-create message:
    @cd api && just migrate-create {{message}}
```

## When to Add Level 4

Add when:
- Multiple languages (Python + JavaScript, etc.)
- Microservices architecture
- Monorepo structure
- Independent subproject lifecycles

Skip when:
- Single language project
- Single deployable artifact
- Tightly coupled codebase

## Validation

Level 4 complete when:
- Root justfile orchestrates correctly
- Each subproject passes `just check-all` independently
- `cd api && just check-all` works standalone
- `cd web && just check-all` works standalone
- Root `just check-all` validates entire project

## Anti-Patterns

**Don't:**
- Duplicate implementations at root (use _run-all)
- Mix stacks in single justfile (use subprojects)
- Skip baseline in subprojects (each needs full interface)
- Block root check-all on optional commands

**Do:**
- Delegate to subprojects
- Keep root minimal
- Make subprojects standalone
- Fail fast in _run-all

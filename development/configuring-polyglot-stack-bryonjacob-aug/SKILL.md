---
name: configuring-polyglot-stack
description: Polyglot project configuration - orchestrate multiple language subprojects with root justfile
---

# Polyglot Stack

For projects with multiple languages (e.g., Python backend + JavaScript frontend).

## Structure

```
my-project/
├── justfile              # Root orchestration
├── api/
│   ├── justfile          # Python stack
│   ├── pyproject.toml
│   └── src/
└── web/
    ├── justfile          # JavaScript stack
    ├── package.json
    └── src/
```

**Each subproject implements full aug-just/justfile-interface (Level 0 baseline).**

**Root implements minimal subset for orchestration.**

## Root Justfile

**Implements:** Subset of aug-just/justfile-interface
**Requires:** aug-just plugin for justfile management

```just
set shell := ["bash", "-uc"]

# Show all available commands
default:
    @just --list

# Install dependencies and setup development environment
dev-install:
    @just _run-all dev-install

# Run all quality checks (format, lint, typecheck, coverage - fastest first)
check-all:
    @just _run-all check-all

# Remove generated files and artifacts
clean:
    @just _run-all clean

# Detailed complexity report for refactoring decisions
complexity:
    @just _run-all complexity

# Show N largest files by lines of code
loc N="20":
    @just _run-all "loc {{N}}"

# Show outdated packages
deps:
    @just _run-all deps

# Check for security vulnerabilities
vulns:
    @just _run-all vulns

# Analyze licenses (flag GPL, etc.)
lic:
    @just _run-all lic

# Generate software bill of materials
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

**Customize `_run-all`:** Change `api web` to match your subproject directories.

## Usage

**Root level:**
```bash
just dev-install    # Setup everything
just check-all      # Run all quality checks
just build          # Build all artifacts
```

**Subproject level:**
```bash
cd api && just test           # Run API tests
cd web && just test-watch     # Watch mode for web
```

**Commands not at root:** Run directly in subprojects:
- `format`, `lint`, `typecheck` - Run per-project as needed
- `test`, `coverage`, `integration-test` - Run per-project
- `test-watch` - Must run in specific subproject

## Subproject Configuration

**api/ (Python):** See `configuring-python-stack`

**web/ (JavaScript):** See `configuring-javascript-stack`

Each subproject has its own:
- Full justfile implementing aug-just/justfile-interface
- Stack-specific config files (pyproject.toml, package.json, etc.)
- Independent test suites, coverage thresholds, quality gates

## Notes

- Root justfile does NOT implement full interface - only orchestration subset
- Each subproject is independently valid (`cd api && just check-all` works)
- `_run-all` fails fast (exits on first failure)
- Root-level `check-all` ensures all subprojects pass quality gates

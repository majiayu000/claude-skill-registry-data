---
name: shell-automation
description: Production-grade shell automation - scripts, CI/CD, makefiles
sasmp_version: "1.3.0"
bonded_agent: 06-automation
bond_type: PRIMARY_BOND
version: "2.0.0"
difficulty: advanced
estimated_time: "8-10 hours"
---

# Shell Automation Skill

> Master shell automation, CI/CD, and deployment scripting

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Write production-grade automation scripts
- [ ] Create effective Makefiles
- [ ] Set up CI/CD pipelines
- [ ] Build deployment scripts
- [ ] Test shell scripts with bats

## Prerequisites

- Strong Bash fundamentals
- Git basics
- Understanding of CI/CD concepts

## Core Concepts

### 1. Script Template
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

log_info()  { printf '[INFO] %s\n' "$*" >&2; }
log_error() { printf '[ERROR] %s\n' "$*" >&2; }
die()       { log_error "$1"; exit "${2:-1}"; }

usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [options] <argument>
Options:
    -h, --help      Show this help
    -v, --verbose   Enable verbose
EOF
}

main() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help) usage; exit 0 ;;
            *) break ;;
        esac
    done
    log_info "Starting..."
}

main "$@"
```

### 2. Makefile Pattern
```makefile
.PHONY: all build test lint clean help

SHELL := /bin/bash
.DEFAULT_GOAL := help

help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

build: ## Build project
	./scripts/build.sh

test: ## Run tests
	bats tests/

lint: ## Run linter
	shellcheck scripts/*.sh

clean: ## Clean artifacts
	rm -rf dist/ build/
```

### 3. GitHub Actions
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: shellcheck **/*.sh
      - name: Test
        run: bats tests/
```

### 4. Bats Testing
```bash
#!/usr/bin/env bats

setup() {
    source "./functions.sh"
    TEST_DIR="$(mktemp -d)"
}

teardown() {
    rm -rf "$TEST_DIR"
}

@test "function returns success" {
    run my_function "arg"
    [ "$status" -eq 0 ]
}

@test "output contains expected" {
    run my_function "arg"
    [[ "$output" == *"expected"* ]]
}
```

## Common Patterns

### Deployment Script
```bash
#!/usr/bin/env bash
set -euo pipefail

deploy() {
    local version="${1:-$(git describe --tags)}"

    log_info "Deploying $version"

    # Pre-flight checks
    preflight_check

    # Create backup
    create_backup

    # Deploy
    rsync -avz --delete dist/ /opt/app/

    # Restart service
    systemctl restart app

    log_info "Deployed $version"
}

rollback() {
    local previous
    previous=$(ls -t /opt/backups | head -1)
    log_info "Rolling back to $previous"
    rsync -avz "/opt/backups/$previous/" /opt/app/
    systemctl restart app
}
```

### Retry Pattern
```bash
retry() {
    local max="${1:-3}"
    local delay="${2:-1}"
    shift 2

    for ((i=1; i<=max; i++)); do
        if "$@"; then
            return 0
        fi
        log_info "Retry $i/$max in ${delay}s..."
        sleep "$delay"
        delay=$((delay * 2))
    done
    return 1
}

# Usage
retry 5 2 curl -sf https://api.example.com
```

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| Skip ShellCheck | Always lint | Catch bugs |
| No error handling | Use `set -e` | Fail early |
| Hardcode paths | Use variables | Flexibility |
| Skip tests | Write bats tests | Reliability |

## Practice Exercises

1. **Deploy Script**: Zero-downtime deployment
2. **Backup System**: Automated backups with rotation
3. **CI Pipeline**: Complete GitHub Actions workflow
4. **Test Suite**: Comprehensive bats tests

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Script not running | Not executable | `chmod +x` |
| Command not found | PATH issue | Use full path |
| Syntax error | Missing quotes | ShellCheck |

### Debug Techniques
```bash
# Enable trace
set -x

# Run with debug
bash -x script.sh

# ShellCheck
shellcheck script.sh
```

## Resources

- [Bash Strict Mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
- [ShellCheck](https://www.shellcheck.net/)
- [Bats Testing](https://github.com/bats-core/bats-core)
- [GitHub Actions](https://docs.github.com/en/actions)

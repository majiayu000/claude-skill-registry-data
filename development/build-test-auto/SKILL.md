---
name: build-test-auto
description: Automatically builds and tests code changes. Use whenever code is modified, tests fail, before creating pull requests, or when verifying code quality.
allowed-tools: Bash, Read, Glob, Grep, Edit
---

# Automated Build & Test Workflow

## Overview

This skill provides automated build and test execution for various project types. It is triggered automatically when code changes are made or when tests need verification.

## Quick Reference

### Project Detection & Commands

```bash
# JavaScript/Node.js
if [ -f "package.json" ]; then
    npm install && npm run build && npm test
fi

# Python
if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    pip install -e . && python -m pytest
fi

# Rust
if [ -f "Cargo.toml" ]; then
    cargo build && cargo test
fi

# Go
if [ -f "go.mod" ]; then
    go build ./... && go test ./...
fi

# Java Maven
if [ -f "pom.xml" ]; then
    mvn compile && mvn test
fi

# Java/Kotlin Gradle
if [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    ./gradlew build && ./gradlew test
fi

# Ruby
if [ -f "Gemfile" ]; then
    bundle install && bundle exec rspec
fi

# Make-based
if [ -f "Makefile" ]; then
    make && make test
fi
```

## Workflow Steps

### 1. Pre-Build Checks
- Verify dependencies are installed
- Check for required tools (use `mise` if available)
- Validate configuration files

### 2. Build Phase
- Run the build command
- Capture all output
- Stop immediately on build failure
- Show exact error location

### 3. Test Phase
- Run the full test suite
- Capture test output with verbose mode
- Document all failures

### 4. Failure Analysis
For each failure:
1. Identify the test name and file
2. Show the exact error message
3. Display relevant stack trace
4. Analyze root cause

### 5. Fix & Verify
- Apply minimal fixes
- Re-run tests to confirm
- Report final status

## Linting

After tests pass, also run linting:

| Project Type | Lint Command |
|-------------|--------------|
| Node.js | `npm run lint` |
| Python | `ruff check .` or `flake8` |
| Rust | `cargo clippy` |
| Go | `go vet ./...` |

## Tips

- Use `mise` to install missing runtimes
- Check `.nvmrc`, `.python-version`, `.tool-versions` for version requirements
- Run lint and build before pushing to remote

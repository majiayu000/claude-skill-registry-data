---
name: ci-pipeline
description: "Generates a CI/CD pipeline configuration for the project. Auto-detects the stack and creates GitHub Actions, GitLab CI, or other CI configs with lint, test, build, and deploy stages."
argument-hint: "[github-actions, gitlab-ci, or 'auto']"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# CI Pipeline Generator

## Detect Project Stack
!`ls package.json requirements.txt pyproject.toml go.mod Cargo.toml *.csproj *.sln Gemfile composer.json mix.exs Makefile Dockerfile 2>/dev/null`
!`ls .github/workflows/ .gitlab-ci.yml Jenkinsfile .circleci/ .travis.yml bitbucket-pipelines.yml 2>/dev/null`
!`cat package.json 2>/dev/null | grep -E '"(scripts|devDependencies)"' -A 10 | head -20`

---

## Pipeline Design

### Step 1: Detect Requirements
From project files, determine:
- Language and version (Node 20, Python 3.12, Go 1.22, etc.)
- Package manager (npm, pnpm, yarn, pip, poetry, cargo, etc.)
- Test command
- Lint command
- Build command
- Required services (database, Redis, etc.)

### Step 2: Generate Pipeline Stages

**Stage 1: Install**
- Cache dependencies for fast subsequent runs
- Use lock file hash as cache key

**Stage 2: Lint**
- Run linter (ESLint, ruff, golangci-lint, clippy, etc.)
- Run type checker if applicable (tsc, mypy, go vet)
- Run formatter check (prettier, black, gofmt)

**Stage 3: Test**
- Run unit tests with coverage
- Run integration tests (with service containers if needed)
- Upload coverage report

**Stage 4: Build**
- Production build
- Verify build artifacts are created

**Stage 5: Security (optional)**
- Dependency vulnerability scan
- Secret scanning
- SAST if available

**Stage 6: Deploy (placeholder)**
- Staging deployment (on push to main)
- Production deployment (on tag/release)
- Mark as manual/approval required

### Step 3: Platform-Specific Output

**GitHub Actions:**
```yaml
name: CI
on: [push, pull_request]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps: ...
```

**GitLab CI:**
```yaml
stages: [install, lint, test, build, deploy]
```

### Step 4: Optimizations
- Dependency caching (npm cache, pip cache, cargo cache)
- Parallel test execution where possible
- Matrix builds for multiple versions (if needed)
- Fail-fast on lint errors (don't waste time on tests)
- Artifact upload for build output

## Rules
- Always include a lint stage — catch issues early
- Always include caching — speed up repeat runs
- Keep the pipeline under 10 minutes for PRs
- Don't hardcode versions — use variables or matrix
- Include both push and PR triggers

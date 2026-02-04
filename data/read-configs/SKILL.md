---
name: read-configs
description: Find and understand project configuration files. Discovers build configs, dependencies, env vars, CI/CD, and tool settings without reading full files.
allowed-tools: Bash, Read, Grep, Glob
---

# Config File Discovery

Find all configuration files in a project and understand what they control.

## Quick Discovery

### Find All Config Files

```bash
# Common config files
ls -la *.yaml *.yml *.toml *.json *.ini .env* 2>/dev/null

# Recursive discovery
find . -type f \( \
  -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o \
  -name "*.json" -o -name "*.ini" -o -name ".env*" -o \
  -name "*.config.js" -o -name "*.config.ts" \
\) -not -path "*/.git/*" -not -path "*/node_modules/*" 2>/dev/null | head -40
```

## Config Categories

### 1. Python Project

```bash
# Core Python configs
ls -la pyproject.toml setup.py setup.cfg requirements*.txt 2>/dev/null

# pyproject.toml sections
grep "^\[" pyproject.toml 2>/dev/null

# Dependencies
grep -A 20 "dependencies" pyproject.toml 2>/dev/null | head -25
```

### 2. Node/TypeScript Project

```bash
# Core Node configs
ls -la package.json package-lock.json tsconfig*.json 2>/dev/null

# package.json scripts
grep -A 20 '"scripts"' package.json 2>/dev/null | head -25

# Dependencies
grep -A 30 '"dependencies"' package.json 2>/dev/null | head -35
```

### 3. Environment Variables

```bash
# Find env files
ls -la .env* env.* 2>/dev/null

# List env var names (not values - security!)
grep -h "^[A-Z]" .env* 2>/dev/null | cut -d'=' -f1 | sort | uniq

# Find env var usage in code
rg "os\.environ|os\.getenv|process\.env" --type py --type ts --type js -l 2>/dev/null
```

### 4. GCP/Cloud Configs

```bash
# GCP configs
ls -la app.yaml cloudbuild.yaml *.tf terraform.tfvars 2>/dev/null

# Cloud Run / Cloud Functions
grep -l "runtime:" *.yaml 2>/dev/null
grep -l "cloud.google.com" *.yaml 2>/dev/null
```

### 5. CI/CD Configs

```bash
# GitHub Actions
ls -la .github/workflows/*.yaml .github/workflows/*.yml 2>/dev/null

# Workflow triggers
grep -h "^on:" .github/workflows/*.y*ml 2>/dev/null

# Other CI
ls -la .gitlab-ci.yml Jenkinsfile .circleci/config.yml 2>/dev/null
```

### 6. Build/Dev Tools

```bash
# Linters & Formatters
ls -la .eslintrc* .prettierrc* .ruff.toml ruff.toml mypy.ini .flake8 2>/dev/null

# Build tools
ls -la Makefile BUILD.bazel *.bzl Dockerfile docker-compose*.yml 2>/dev/null

# Editor configs
ls -la .editorconfig .vscode/settings.json 2>/dev/null
```

### 7. Database/ORM

```bash
# Database configs
ls -la alembic.ini prisma/schema.prisma 2>/dev/null

# Find connection strings (names only)
rg "DATABASE|POSTGRES|MYSQL|MONGO|REDIS" --type py --type ts -l 2>/dev/null
```

## Full Config Scan

One-liner to find ALL configs:

```bash
echo "=== PYTHON ===" && ls pyproject.toml setup.py 2>/dev/null
echo "=== NODE ===" && ls package.json tsconfig.json 2>/dev/null
echo "=== ENV ===" && ls .env* 2>/dev/null
echo "=== CLOUD ===" && ls app.yaml cloudbuild.yaml *.tf 2>/dev/null
echo "=== CI/CD ===" && ls .github/workflows/*.y*ml 2>/dev/null | head -5
echo "=== DOCKER ===" && ls Dockerfile docker-compose*.yml 2>/dev/null
echo "=== BUILD ===" && ls Makefile BUILD.bazel 2>/dev/null
```

## Reading Config Sections

Once you find configs, extract specific sections:

```bash
# TOML sections
grep "^\[" pyproject.toml

# YAML top-level keys
grep "^[a-z]" config.yaml | head -20

# JSON top-level keys
cat package.json | grep -E '^\s{2}"[a-z]' | head -20
```

## Security Note

**NEVER output actual values from:**
- `.env` files
- `*secrets*` files
- `credentials.json`
- Files containing API keys, tokens, passwords

Only list variable NAMES, never VALUES.

## Token Efficiency

This skill returns file lists and section headers, not full content. Read individual configs only when you need specific values.

## Related Skills

- **codebase-index**: Entry points, classes, API routes
- **index-docs**: Documentation structure
- **startup**: Full session bootstrap

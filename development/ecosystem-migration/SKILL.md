---
name: ecosystem-migration
description: Migrate existing repositories to use Personal GitHub Ecosystem templates and patterns. USE THIS SKILL when user says "migrate to ecosystem", "adopt templates", "convert workflow", "upgrade CI", or wants to transition existing projects.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Ecosystem Migration Skill

## Purpose

Migrate existing repositories to use Personal GitHub Ecosystem templates and patterns, including workflow conversion and AI integration adoption.

## Triggers

- "migrate this repo to the ecosystem"
- "adopt the python template"
- "convert to reusable workflows"
- "upgrade my CI to ecosystem standards"
- "add ecosystem AI integration"

## Usage

Point this skill at an existing repository to assess its current state and receive a migration plan. Choose from full adoption, workflow-only, or incremental strategies based on project complexity.

## Migration Assessment

```bash
# Detect project type
[ -f "pyproject.toml" ] && echo "Python"
[ -f "package.json" ] && echo "Node.js"
[ -f "go.mod" ] && echo "Go"
[ -f "Cargo.toml" ] && echo "Rust"
[ -f "build.gradle.kts" ] && echo "Java"

# Check existing config
ls -la .github/workflows/ 2>/dev/null
[ -f "CLAUDE.md" ] && echo "Has CLAUDE.md"
[ -f ".github/copilot-instructions.md" ] && echo "Has Copilot"
```

## Migration Strategies

### Strategy 1: Full Template Adoption

Best for: New-ish projects with minimal customization

```bash
# 1. Backup existing config
mkdir -p .migration-backup
cp -r .github .migration-backup/

# 2. Copy template files
cp -r ~/ecosystem/templates/python-template/.github ./
cp ~/ecosystem/templates/python-template/CLAUDE.md ./
mkdir -p .vscode
cp ~/ecosystem/templates/python-template/.vscode/mcp.json .vscode/

# 3. Merge configurations (manual review)
```

### Strategy 2: Workflow-Only Migration

Best for: Established projects wanting CI standardization

```yaml
# Replace existing CI with reusable workflow
name: CI
on: [push, pull_request]

jobs:
  ci:
    uses: zircote/.github/.github/workflows/reusable-ci-python.yml@main
    with:
      python-version: '3.12'
    secrets: inherit
```

### Strategy 3: Incremental Adoption

Best for: Large projects requiring careful migration

**Phase 1: AI Integration**
- Add CLAUDE.md
- Add copilot-instructions.md
- Add mcp.json

**Phase 2: Standardize Tooling**
- Update linter/formatter configs

**Phase 3: Migrate Workflows**
- Add reusable workflow alongside existing
- Test and validate
- Remove old workflow

**Phase 4: Security Baseline**
- Add pre-commit hooks
- Configure gitleaks
- Enable Dependabot

## Adding AI Integration

```bash
# Create CLAUDE.md
cat > CLAUDE.md << 'EOF'
# CLAUDE.md

## Project Overview
[Describe project]

## Build Commands
```bash
[relevant commands]
```

## Code Style
[Document standards]
EOF

# Create copilot-instructions.md
mkdir -p .github
cat > .github/copilot-instructions.md << 'EOF'
# GitHub Copilot Instructions

## Project Context
[Describe for Copilot]

## Code Guidelines
[Language patterns]
EOF
```

## Converting to Reusable Workflows

**Before:**
```yaml
name: CI
on: [push]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff && ruff check .
```

**After:**
```yaml
name: CI
on: [push]
jobs:
  ci:
    uses: zircote/.github/.github/workflows/reusable-ci-python.yml@main
```

## Validation After Migration

```bash
# Check required files
for f in CLAUDE.md .github/copilot-instructions.md; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ $f"
done

# Validate workflows
./scripts/validate-sha-pinning.sh .github/workflows/

# Test CI (if possible)
# Run linting, tests locally
```

## Rollback Procedure

```bash
# Quick rollback
cp -r .migration-backup/.github ./
rm CLAUDE.md .github/copilot-instructions.md

# Or selective
git checkout HEAD~1 -- .github/workflows/
```

## Migration Checklist

### Pre-Migration
- [ ] Document current CI behavior
- [ ] Create backup branch
- [ ] Identify custom configs to preserve

### During Migration
- [ ] Copy/adapt template files
- [ ] Merge configs (don't overwrite)
- [ ] Update project-specific values

### Post-Migration
- [ ] CI passes
- [ ] Existing features work
- [ ] AI integration functional
- [ ] Team approval

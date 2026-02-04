---
name: dockerignore-config
description: Docker ignore configuration template and validation logic for optimizing Docker build contexts. Includes 5 required standards (build artifacts, development files, CI/CD and testing, logs and temporary files, root-only placement). Use when creating or auditing .dockerignore files to reduce build context size, improve performance, and ensure security.
---

# Docker Ignore Configuration Skill

This skill provides .dockerignore template and validation logic for optimizing Docker build contexts.

## Purpose

Manage .dockerignore configuration to:

- Reduce Docker build context size
- Exclude unnecessary files from Docker builds
- Improve build performance
- Ensure security (exclude .env, credentials)

## Usage

This skill is invoked by the `dockerignore-agent` when:

- Creating new .dockerignore files
- Auditing existing .dockerignore configurations
- Validating .dockerignore against standards

## Template

The standard .dockerignore template is located at:

```
templates/.dockerignore.template
```

## The 5 .dockerignore Standards

### Rule 1: Build Artifacts

Must exclude build outputs: `dist/`, `build/`, `.next/`, `out/`, `.turbo/`, `*.tsbuildinfo`, `node_modules/`

### Rule 2: Development Files

Must exclude environment files, IDE configs, OS files, Git files:

- `.env*` files
- `.vscode/`, `.idea/`
- `.DS_Store`, `Thumbs.db`
- `.git/`, `.gitignore`

### Rule 3: CI/CD and Testing

Must exclude CI/CD configs, test files, coverage, documentation:

- `.github/`, CI config files
- `coverage/`, `*.test.*`, `*.spec.*`, `__tests__/`, `__mocks__/`
- `docs/`, `*.md` (except `README.md`)

### Rule 4: Logs and Temporary Files

Must exclude logs and temporary files:

- `*.log` files
- `*.tmp`, `*.temp`
- `.cache/`

### Rule 5: Root-Only Placement

Place `.dockerignore` at the repository root where Docker CLI reads it. Docker uses the build context root for consistent, predictable behavior across all builds.

**Benefits of root-only placement:**

- Single source of truth for all Docker exclusions
- Patterns apply consistently across the entire build context
- Team members find configuration in the expected location
- Subdirectory patterns work using path prefixes (e.g., `apps/web/node_modules/`)

**Action:** Consolidate any subdirectory `.dockerignore` content into the root file, then remove the nested files.

## Validation

To validate a .dockerignore file:

1. Check that the file exists at repository root
2. Read the file content
3. Verify it includes patterns for all 5 rule categories
4. Report any missing categories

### Validation Approach

```bash
# Check Rule 1: Build artifacts
grep -q "node_modules" .dockerignore && grep -q "dist" .dockerignore

# Check Rule 2: Development files
grep -q ".env" .dockerignore && grep -q ".vscode" .dockerignore

# Check Rule 3: CI/CD and testing
grep -q ".github" .dockerignore && grep -q "coverage" .dockerignore

# Check Rule 4: Logs and temporary
grep -q "*.log" .dockerignore && grep -q "*.tmp" .dockerignore

# Check Rule 5: No nested .dockerignore files
find . -name ".dockerignore" -not -path "./.dockerignore" | wc -l  # Should be 0
```

## Repository Type Considerations

- **Consumer Repos**: Should strictly follow all 5 standards
- **Library Repos**: May have intentional differences (e.g., include documentation)

## Best Practices

1. Place .dockerignore at repository root only
2. Use template as starting point
3. Include `!README.md` to explicitly include README in builds
4. Exclude all sensitive files (`.env*`, credentials)
5. Smaller build context = faster Docker builds
6. Re-audit after making changes

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices

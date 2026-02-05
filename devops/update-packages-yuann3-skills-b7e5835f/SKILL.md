---
name: update-packages
description: Use ONLY when user explicitly requests updating Node.js and pnpm versions - systematically updates package managers in all locations (frontend, backend, CI/CD) and verifies versions against official sources. Never use proactively.
---

# Update Packages

## Overview

Systematically update Node.js, pnpm, and npm dependencies to latest versions across entire project, including all package.json files, CI/CD configs, and Docker files. **Core principle:** Always verify against official sources, never assume or guess versions.

## When to Use

**ONLY when user explicitly asks to update Node.js or pnpm versions.**

Do NOT use this skill:
- Proactively or automatically
- "Before starting new features"
- Based on security advisories
- When you notice outdated versions
- For updating application dependencies (use standard package manager)
- When project requires specific older versions for compatibility

**Wait for explicit user request.**

## Quick Reference

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Check official sources | nodejs.org, pnpm.io |
| 2 | Update npm dependencies | Use npm-check-updates |
| 3 | Find all locations | .tool-versions, package.json, CI/CD, Dockerfiles |
| 4 | Update systematically | Every occurrence found |
| 5 | Verify locally | `node -v`, `pnpm -v`, run tests |
| 6 | Test CI/CD | Run workflow or review changes |

## Implementation

### 1. Get Latest Versions from Official Sources

**ALWAYS check official sources first - never guess or use cached knowledge:**

```bash
# Node.js - Check official site
# Visit: https://nodejs.org/en/download/package-manager
# Or use API:
curl -s https://nodejs.org/dist/index.json | grep -m1 '"version"' | cut -d'"' -f4

# pnpm - Check official site
# Visit: https://pnpm.io/installation
# Or use npm:
npm view pnpm version
```

**Why:** Your knowledge may be outdated. Official sources are authoritative.

### 2. Update npm Dependencies with npm-check-updates

**Use the package manager to run npm-check-updates for all package.json files:**

```bash
# Using pnpm (recommended if project uses pnpm)
pnpm dlx npm-check-updates -u

# For monorepos or multiple package.json files
pnpm dlx npm-check-updates -u --deep

# After updating, install new versions
pnpm install
```

**Alternative package managers:**
```bash
# Using npx (npm)
npx npm-check-updates -u
npm install

# Using yarn
npx npm-check-updates -u
yarn install
```

**What this does:**
- Scans package.json for outdated dependencies
- Updates version numbers to latest
- Respects semantic versioning ranges (can be configured)

**Options:**
- `-u` or `--upgrade`: Write updated versions to package.json
- `--deep`: Update nested package.json files in workspaces
- `--target minor`: Only update to latest minor versions
- `--target patch`: Only update to latest patch versions
- `--interactive`: Choose which packages to update

### 3. Find ALL Locations

**Search comprehensively - don't rely on memory:**

```bash
# Find Node.js version references
grep -r "node" --include="*.json" --include="*.yml" --include="*.yaml" \
  --include="Dockerfile*" --include=".nvmrc" --include=".node-version" \
  --include=".tool-versions"

# Find pnpm version references
grep -r "pnpm" --include="*.json" --include="*.yml" --include="*.yaml" \
  --include="Dockerfile*" --include="package.json" --include=".tool-versions"
```

**Common locations:**
- `.tool-versions` (asdf version manager)
- `.nvmrc` or `.node-version` (other version managers)
- `package.json` (engines field, packageManager field)
- `.github/workflows/*.yml` (GitHub Actions)
- `.gitlab-ci.yml` (GitLab CI)
- `Dockerfile` and `docker-compose.yml`
- CI config files (`.circleci/`, `azure-pipelines.yml`, etc.)

### 4. Update Systematically

**For each location found:**

**Node.js updates:**
```json
// package.json
{
  "engines": {
    "node": ">=22.0.0"  // Update to latest major
  }
}
```

```yaml
# .github/workflows/ci.yml
- uses: actions/setup-node@v4
  with:
    node-version: '22'  # Update to latest major
```

```
# .tool-versions (asdf)
nodejs 22.11.0
pnpm 9.14.2

# .nvmrc (if using nvm)
22.11.0
```

**pnpm updates:**
```json
// package.json
{
  "packageManager": "pnpm@9.14.2",  // Exact latest version
  "engines": {
    "pnpm": ">=9.0.0"  // Latest major
  }
}
```

```yaml
# .github/workflows/ci.yml
- uses: pnpm/action-setup@v4
  with:
    version: 9.14.2  # Exact latest version
```

### 5. Verify Updates Work

**Local verification:**
```bash
# Update local versions (asdf example)
asdf install nodejs 22.11.0
asdf install pnpm 9.14.2
asdf global nodejs 22.11.0  # or asdf local
asdf global pnpm 9.14.2

# Verify versions
node -v  # Should show v22.x.x
pnpm -v  # Should show 9.x.x

# Test installation works
pnpm install
pnpm build  # Or relevant build command
```

**CI/CD verification:**
- Commit changes and push
- Monitor CI/CD pipeline runs
- Verify no version-related failures

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Guessing latest version | Check nodejs.org and pnpm.io |
| Manually updating dependencies | Use npm-check-updates |
| Missing .tool-versions or CI configs | Use grep to find ALL locations |
| Updating only package.json | Update CI/CD, Docker, version files |
| Not testing locally first | Install versions locally, run build |
| Skipping CI/CD verification | Push and verify pipelines pass |

## Red Flags - STOP and Verify

- "I'll use version X" without checking sources → Check official sites
- "I updated package.json" without searching → Find ALL locations
- "This should work" without testing → Test locally first
- "CI will catch issues" → Verify CI config updated too

## Checklist

- [ ] Check nodejs.org for latest Node.js version
- [ ] Check pnpm.io or npm for latest pnpm version
- [ ] Run npm-check-updates to update npm dependencies
- [ ] Install updated dependencies (pnpm install)
- [ ] Search for ALL Node.js references (grep -r)
- [ ] Search for ALL pnpm references (grep -r)
- [ ] Update .tool-versions (asdf) or other version manager files
- [ ] Update package.json (engines, packageManager)
- [ ] Update CI/CD workflows (GitHub Actions, GitLab CI, etc.)
- [ ] Update Dockerfiles if present
- [ ] Install versions locally (asdf install)
- [ ] Run local build/tests
- [ ] Commit and verify CI/CD passes

## Real-World Impact

**Without systematic approach:**
- Frontend updated, backend still on old version
- CI/CD fails because workflow uses old version
- Build works locally but breaks in CI

**With systematic approach:**
- All locations updated consistently
- CI/CD verified to use latest versions
- Clean deployment with modern tooling

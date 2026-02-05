---
name: upgrade-dependencies
description: Periodically upgrade npm dependencies and GitHub Actions to keep project current and secure
group: docent
author: "@tnez"
version: 1.0.0
keywords: [dependencies, maintenance, security, npm]
---

# Runbook: Upgrade Dependencies

**Purpose:** Periodically upgrade npm dependencies and GitHub Actions to keep project current and secure
**Owner:** Maintainers
**Last Updated:** 2025-10-20
**Frequency:** Monthly or when security vulnerabilities discovered

## Overview

This runbook provides a manual, controlled process for upgrading project dependencies. Unlike automated tools (Renovate, Dependabot), this approach gives maintainers full control over timing, grouping, and testing of upgrades.

**Why manual upgrades:**

- **Control** - Choose when and what to upgrade
- **Grouping** - Upgrade related dependencies together
- **Testing** - Thorough validation before committing
- **Context** - Understand what's changing and why

**Expected duration:** 1-2 hours depending on number of upgrades

## Prerequisites

### Required Tools

- `npm` - Node.js package manager (v11.6.0+)
- `git` - Version control
- `gh` CLI - For checking GitHub Actions versions
- Node.js >= 20.0.0 (match engines in package.json)

### Required Access

- Write access to repository
- Ability to run tests locally
- npm registry access (for checking versions)

### Pre-Flight Checklist

Before starting, ensure:

- [ ] You have 1-2 hours available
- [ ] Main branch is clean and CI is passing
- [ ] No urgent releases pending (upgrades can wait)
- [ ] You're on latest main: `git checkout main && git pull`
- [ ] Working directory is clean: `git status`

## Procedure

### Step 1: Check for Outdated Dependencies

**Purpose:** Identify which dependencies have available updates

**Commands:**

```bash
# Check outdated npm packages
npm outdated

# Check specific package current vs latest
npm view <package-name> version
npm view <package-name> versions --json | jq -r '.[-5:]'  # Last 5 versions

# Check for security vulnerabilities
npm audit

# Get detailed audit report
npm audit --json
```

**Understanding npm outdated output:**

```
Package                Current  Wanted  Latest  Location
@types/node            20.11.0  20.19.22  22.0.0  devDependencies
mocha                  10.0.0   10.9.0   11.0.0  devDependencies
```

- **Current:** Currently installed version
- **Wanted:** Latest version matching semver in package.json
- **Latest:** Absolute latest version (may be breaking)
- **Red:** Major version behind (breaking changes likely)
- **Yellow:** Minor/patch updates available

**Validation:**

- Output shows all dependencies with available updates
- Security audit shows any vulnerabilities

**If step fails:**

- Ensure npm is up to date: `npm install -g npm@latest`
- Check network connection to npm registry

---

### Step 2: Categorize and Prioritize Updates

**Purpose:** Group updates by type and urgency for efficient upgrading

**Categorization:**

```bash
# Create upgrade plan (mental or documented)
```

**Categories:**

1. **Security fixes** (URGENT - do first)
   - Identified by `npm audit`
   - High/critical severity
   - Example: Vulnerability in production dependency

2. **Production dependencies** (HIGH priority)
   - Found in `dependencies` section
   - Affects runtime behavior
   - Example: `@modelcontextprotocol/sdk`, `glob`, `tslib`

3. **Development dependencies** (MEDIUM priority)
   - Found in `devDependencies` section
   - Affects build/test only
   - Example: `typescript`, `mocha`, `eslint`

4. **GitHub Actions** (MEDIUM priority)
   - Found in `.github/workflows/*.yml`
   - Affects CI/CD only
   - Example: `actions/checkout`, `actions/setup-node`

5. **Major version upgrades** (LOW priority - save for last)
   - Breaking changes likely
   - Requires careful testing and potentially code changes
   - Example: `eslint` v8 → v9, `node` v20 → v22

**Priority Matrix:**

| Type | Urgency | When to Upgrade |
|------|---------|-----------------|
| Security fix | URGENT | Immediately |
| Patch (0.0.X) | HIGH | This session |
| Minor (0.X.0) | MEDIUM | This session or next |
| Major (X.0.0) | LOW | Dedicated session with testing |

**Create Upgrade Plan:**

```bash
# Example plan (document in scratch file or notepad)
echo "Upgrade Plan:
1. Security: (none found ✓)
2. Production deps:
   - @modelcontextprotocol/sdk: 1.20.0 → 1.20.1 (patch)
   - glob: 10.3.10 → 10.4.5 (minor)
3. Dev deps (patch/minor):
   - @types/node: 20.11.0 → 20.19.22
   - markdownlint-cli2: 0.16.0 → 0.18.0
4. GitHub Actions:
   - actions/checkout: v4 → v5
   - actions/setup-node: v4 → v6
5. Major upgrades (defer):
   - eslint: v8 → v9 (defer - breaking changes)
   - mocha: v10 → v11 (defer - validate first)
   - node: v20 → v22 (defer - test thoroughly)
" > /tmp/upgrade-plan.txt
```

**Validation:**

- All outdated packages are categorized
- Security fixes identified and prioritized
- Major upgrades are noted for careful handling

---

### Step 3: Upgrade Security Fixes First

**Purpose:** Address vulnerabilities immediately

**Commands:**

```bash
# If npm audit found vulnerabilities
npm audit fix

# For breaking changes that audit can't auto-fix
npm audit fix --force  # CAUTION: May introduce breaking changes

# Manually upgrade specific vulnerable package
npm install <package>@latest
```

**Validation:**

```bash
# Verify vulnerabilities are resolved
npm audit

# Should show: "found 0 vulnerabilities"
```

**If vulnerabilities remain:**

- Check if vulnerability is in transitive dependency (dependency of dependency)
- Check if patch is available from maintainer
- Consider using `npm audit fix --force` (test thoroughly)
- Document known vulnerabilities if fix isn't available

**Commit security fixes immediately:**

```bash
git add package.json package-lock.json
git commit -m "fix(deps): resolve security vulnerabilities

- Updated <package> to fix <CVE-XXXX-XXXXX>
- Ran npm audit fix

npm audit: 0 vulnerabilities"
```

---

### Step 4: Upgrade Production Dependencies (Patch/Minor)

**Purpose:** Keep runtime dependencies current

**Commands:**

```bash
# Upgrade specific package to latest patch within current minor
npm update <package>  # Respects semver range in package.json

# Upgrade to latest minor version
npm install <package>@^X.Y.0  # Replace X.Y with desired version

# Upgrade to exact latest version
npm install <package>@latest

# Example: Upgrade @modelcontextprotocol/sdk
npm install @modelcontextprotocol/sdk@latest

# Example: Upgrade glob to latest minor
npm install glob@^10.0.0
```

**After each upgrade, test:**

```bash
# Run build
npm run build

# Run tests
npm test

# If tests fail, investigate and fix or rollback:
git checkout package.json package-lock.json
```

**Validation:**

- Build completes without errors
- All tests pass
- No new warnings (or warnings are acceptable/documented)

**Group related upgrades:**

Upgrade related packages together (e.g., all MCP SDK packages, all type definitions):

```bash
# Upgrade multiple related packages
npm install \
  @modelcontextprotocol/sdk@latest \
  other-related-package@latest
```

**Commit production dependency upgrades:**

```bash
git add package.json package-lock.json
git commit -m "chore(deps): upgrade production dependencies

- @modelcontextprotocol/sdk: 1.20.0 → 1.20.1
- glob: 10.3.10 → 10.4.5

Tests passing, no breaking changes."
```

---

### Step 5: Upgrade Development Dependencies (Patch/Minor)

**Purpose:** Keep build and test tools current

**Commands:**

```bash
# Upgrade development dependency
npm install --save-dev <package>@latest

# Example: Upgrade TypeScript types
npm install --save-dev @types/node@latest @types/chai@latest

# Example: Upgrade testing tools
npm install --save-dev mocha@latest chai@latest

# Example: Upgrade linting tools
npm install --save-dev eslint@latest markdownlint-cli2@latest
```

**After each upgrade, test:**

```bash
# TypeScript build
npm run build

# Linting
npm run lint
npm run lint:md

# Tests
npm test

# Full CI simulation
npm run build && npm test && npm run lint && npm run lint:md
```

**Validation:**

- All checks pass (build, lint, test)
- No new type errors introduced
- Linting rules haven't changed significantly (or changes are acceptable)

**Commit dev dependency upgrades:**

```bash
git add package.json package-lock.json
git commit -m "chore(deps): upgrade development dependencies

- @types/node: 20.11.0 → 20.19.22
- markdownlint-cli2: 0.16.0 → 0.18.0
- typescript: 5.3.0 → 5.7.0

Tests and linting passing."
```

---

### Step 6: Upgrade GitHub Actions

**Purpose:** Keep CI/CD workflows current

**Commands:**

```bash
# Check current versions
grep -r "uses:" .github/workflows/

# Check latest version for an action
gh api repos/actions/checkout/releases/latest --jq '.tag_name'
gh api repos/actions/setup-node/releases/latest --jq '.tag_name'

# Or visit action's GitHub page
open https://github.com/actions/checkout
open https://github.com/actions/setup-node
```

**Upgrade process:**

```bash
# Edit workflow files
vim .github/workflows/ci.yml
vim .github/workflows/lint.yml
vim .github/workflows/publish.yml

# Update action versions (example)
# Before: uses: actions/checkout@v4
# After:  uses: actions/checkout@v5
```

**Common actions to update:**

- `actions/checkout` - Usually safe to upgrade
- `actions/setup-node` - Check Node version compatibility
- `actions/upload-artifact` / `download-artifact` - Usually safe
- `softprops/action-gh-release` - Check changelog for changes

**Validation:**

```bash
# Push to branch and trigger CI
git checkout -b chore/upgrade-github-actions
git add .github/workflows/
git commit -m "chore(ci): upgrade GitHub Actions

- actions/checkout: v4 → v5
- actions/setup-node: v4 → v6
- davidanson/markdownlint-cli2-action: v18 → v20

All workflows should continue working."

git push origin chore/upgrade-github-actions

# Watch CI runs
gh run watch
```

**If CI passes:**

```bash
# Merge to main
git checkout main
git merge chore/upgrade-github-actions
git push origin main

# Clean up branch
git branch -d chore/upgrade-github-actions
git push origin --delete chore/upgrade-github-actions
```

**If CI fails:**

- Review CI logs: `gh run view <run-id>`
- Check action changelog for breaking changes
- Rollback and investigate
- May need to update workflow syntax or configuration

---

### Step 7: Handle Major Version Upgrades

**Purpose:** Carefully upgrade dependencies with breaking changes

**Major upgrades require extra caution:**

- Read CHANGELOG or migration guide
- Expect breaking changes
- May require code changes
- Test thoroughly

**Process for major upgrades:**

```bash
# Create dedicated branch
git checkout -b chore/upgrade-<package>-v<major>

# Example: Upgrade eslint v8 → v9
git checkout -b chore/upgrade-eslint-v9
```

**Research before upgrading:**

```bash
# Check changelog
npm view <package>@latest --json | jq '.homepage'
# Visit homepage and find CHANGELOG or MIGRATION guide

# Example: Read eslint v9 migration guide
open https://eslint.org/docs/latest/use/migrate-to-9.0.0
```

**Upgrade and fix:**

```bash
# Upgrade the package
npm install --save-dev eslint@latest

# Fix any breaking changes
# - Update config files (.eslintrc.js → eslint.config.js)
# - Update deprecated APIs
# - Fix new lint errors

# Test thoroughly
npm run build
npm run lint
npm test
```

**Validation:**

- All tests pass
- All linting passes
- No console warnings
- Application behavior unchanged

**Create PR for major upgrades:**

```bash
# Commit changes
git add .
git commit -m "chore(deps): upgrade eslint to v9

BREAKING CHANGES:
- Migrated from .eslintrc.js to eslint.config.js
- Updated plugin configuration format
- Fixed new lint errors

See: https://eslint.org/docs/latest/use/migrate-to-9.0.0"

# Push and create PR
git push origin chore/upgrade-eslint-v9
gh pr create --title "chore(deps): Upgrade eslint to v9" \
  --body "Upgrades eslint from v8 to v9 with migration to new config format.

## Changes
- Migrated config to eslint.config.js
- Updated plugin configurations
- Fixed lint errors from new rules

## Testing
- [x] Build passes
- [x] All tests pass
- [x] Linting passes
- [x] No new warnings

## References
- [ESLint v9 Migration Guide](https://eslint.org/docs/latest/use/migrate-to-9.0.0)"
```

**Review and merge:**

Use [Code Review Runbook](code-review.md) for thorough review before merging.

---

### Step 8: Update Node.js Version (If Needed)

**Purpose:** Upgrade to newer LTS Node.js version

**When to upgrade Node:**

- New LTS version released (even years: 18, 20, 22, 24)
- Current version approaching EOL
- Needed for dependency compatibility

**Process:**

```bash
# Check current version requirement
grep '"node":' package.json

# Check available LTS versions
nvm ls-remote --lts

# Or check Node.js release schedule
open https://nodejs.org/en/about/previous-releases
```

**Upgrade steps:**

1. **Update package.json engines:**

   ```json
   {
     "engines": {
       "node": ">=22.0.0"
     }
   }
   ```

2. **Update GitHub Actions workflows:**

   ```yaml
   # .github/workflows/*.yml
   - uses: actions/setup-node@v6
     with:
       node-version: '22'  # Update from '20'
   ```

3. **Update type definitions:**

   ```bash
   npm install --save-dev @types/node@^22.0.0
   ```

4. **Test locally with new Node version:**

   ```bash
   nvm install 22
   nvm use 22
   node --version  # Should show v22.x.x

   npm install
   npm run build
   npm test
   ```

5. **Update documentation:**
   - README.md (if Node version mentioned)
   - Contributing guide

**Validation:**

- CI passes on new Node version
- All tests pass
- Application works correctly

**Commit Node upgrade:**

```bash
git add package.json .github/workflows/ README.md
git commit -m "chore: upgrade to Node.js 22 LTS

- Update engines to require Node >= 22.0.0
- Update GitHub Actions to use Node 22
- Update @types/node to v22
- Update documentation

Tests passing on Node 22."
```

---

### Step 9: Update package-lock.json

**Purpose:** Ensure lockfile is consistent and optimized

**Commands:**

```bash
# Regenerate package-lock.json from package.json
rm package-lock.json
npm install

# Or update lockfile without upgrading packages
npm install --package-lock-only

# Audit fix and update lockfile
npm audit fix
```

**Validation:**

```bash
# Verify lockfile is valid
npm ls

# Should show dependency tree without errors
```

**When to regenerate lockfile:**

- After multiple incremental upgrades
- When lockfile has conflicts
- To clean up after many changes

---

### Step 10: Final Validation

**Purpose:** Ensure all upgrades work together

**Commands:**

```bash
# Clean build from scratch
rm -rf node_modules lib
npm install
npm run build

# Run full test suite
npm test

# Run all linters
npm run lint
npm run lint:md

# Verify no security vulnerabilities
npm audit

# Check for any unexpected changes
git status
git diff
```

**Final Checklist:**

- [ ] Build completes successfully
- [ ] All tests pass
- [ ] No linting errors
- [ ] No security vulnerabilities
- [ ] No unexpected file changes
- [ ] CI is passing (if pushed)
- [ ] Application works correctly (manual test if needed)

**If everything passes:**

```bash
# Verify commit history
git log --oneline -10

# Should see logical commits for each upgrade group
```

---

### Step 11: Update CHANGELOG (Optional)

**Purpose:** Document dependency upgrades for users

**When to update CHANGELOG:**

- Major version upgrades that affect users
- Security fixes
- Breaking changes in dependencies
- Before releases

**For minor/patch updates:** CHANGELOG update is optional

**Example CHANGELOG entry:**

```markdown
## [Unreleased]

### Changed
- Upgraded production dependencies (@modelcontextprotocol/sdk, glob)
- Upgraded development dependencies (TypeScript, ESLint, testing tools)
- Upgraded GitHub Actions workflows (actions/checkout v4 → v5)
- Upgraded to Node.js 22 LTS (from Node 20)

### Security
- Fixed vulnerability CVE-2024-XXXXX in <package>
```

---

## Validation

After completing all upgrades:

1. **Local validation:**

   ```bash
   npm run build && npm test && npm run lint
   npm audit
   ```

   All should pass with 0 errors, 0 vulnerabilities

2. **CI validation:**

   ```bash
   git push origin main
   gh run watch
   ```

   All CI workflows should pass

3. **Package health:**

   ```bash
   npm outdated
   ```

   Should show fewer outdated packages than before (or none)

4. **Version tracking:**

   ```bash
   git log --oneline --grep="chore(deps)" -10
   ```

   Should see organized upgrade commits

## Rollback

If upgrades cause issues:

### Rollback Specific Package

```bash
# Revert to previous version
npm install <package>@<previous-version>

# Example
npm install eslint@^8.57.0

# Test
npm test
```

### Rollback All Changes

```bash
# If not yet committed
git checkout package.json package-lock.json
npm install

# If committed but not pushed
git reset --hard HEAD~1  # Or HEAD~N for N commits

# If already pushed
git revert <commit-sha>
git push origin main
```

### Rollback GitHub Actions

```bash
# Edit workflow files back to previous versions
git checkout HEAD~1 -- .github/workflows/

git add .github/workflows/
git commit -m "revert(ci): rollback GitHub Actions upgrades"
git push origin main
```

## Troubleshooting

### Common Issues

#### Issue 1: Package Installation Fails

**Symptoms:**

- `npm install <package>` fails with error
- Dependency resolution conflicts

**Resolution:**

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and lockfile
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, check compatibility
npm view <package> peerDependencies
```

---

#### Issue 2: Tests Fail After Upgrade

**Symptoms:**

- Tests passed before upgrade
- Tests fail after upgrading test framework or dependencies

**Resolution:**

```bash
# Check what changed
git diff HEAD~1 package.json

# Run specific failing test with verbose output
npm test -- --grep "failing test name" --reporter spec

# Check package changelog for breaking changes
npm view <package> --json | jq '.homepage'

# Common fixes:
# - Update test syntax if framework changed
# - Update mocks if dependency behavior changed
# - Check for new required config
```

---

#### Issue 3: TypeScript Errors After Upgrade

**Symptoms:**

- Build fails with type errors
- Worked before upgrading TypeScript or @types packages

**Resolution:**

```bash
# Check TypeScript version
npx tsc --version

# Check type definition versions
npm ls @types/node @types/mocha @types/chai

# Common fixes:
# - Ensure @types/* versions match package versions
# - Update to stricter types (TypeScript tightens checks)
# - Add type assertions if types are more specific
# - Update tsconfig.json if new options available
```

---

#### Issue 4: GitHub Actions Fail After Upgrade

**Symptoms:**

- CI worked before
- Failing after upgrading action versions

**Resolution:**

```bash
# View failing run
gh run view <run-id>

# Common issues:
# - Action syntax changed (check action's CHANGELOG)
# - Node version mismatch (setup-node configuration)
# - New required inputs

# Check action documentation
open https://github.com/<owner>/<action>

# Rollback workflow
git checkout HEAD~1 -- .github/workflows/
git add .github/workflows/
git commit -m "revert(ci): rollback action upgrades"
```

---

### When to Escalate

Escalate if:

- Security vulnerability can't be resolved
- Major upgrade requires significant code changes (>4 hours)
- Dependency has no upgrade path (abandoned package)
- Multiple failing tests can't be fixed quickly
- Need to evaluate switching to alternative package

## Post-Procedure

After completing dependency upgrades:

- [ ] Document any issues encountered in this runbook
- [ ] Update `.nvmrc` if Node version changed
- [ ] Update README if requirements changed
- [ ] Update CHANGELOG if notable changes
- [ ] Note any deferred major upgrades for next session
- [ ] Schedule next dependency check (add to calendar)

## Notes

**Important Notes:**

- **Don't rush** - Thorough testing prevents production issues
- **Group logically** - Upgrade related packages together
- **Read changelogs** - Understand what's changing
- **Test between upgrades** - Easier to identify which upgrade broke something
- **Keep package-lock.json** - Commit it with package.json
- **Use semantic versioning** - `^1.0.0` allows minor/patch, `~1.0.0` allows patch only

**Best Practices:**

- Run upgrades monthly or quarterly (don't let them pile up)
- Check for security vulnerabilities weekly: `npm audit`
- Test on a branch before committing to main (for major upgrades)
- Keep Node.js on LTS versions (even numbers: 20, 22, 24)
- Document breaking changes in commit messages
- Update one category at a time (prod deps, then dev deps, then actions)

**Gotchas:**

- **Peer dependency warnings** - Usually safe to ignore if app works
- **Lockfile conflicts** - Delete and regenerate if conflicted
- **Transitive dependencies** - Can upgrade independently of direct deps
- **GitHub Actions caching** - Clear workflow cache if strange behavior
- **Major version zero (0.x.x)** - Treat minor as major (breaking changes allowed)

**Related Procedures:**

- [Code Review Runbook](code-review.md) - For reviewing major upgrade PRs
- [CI/CD Health Check](ci-cd-health-check.md) - For debugging CI issues
- [Release Package](release-package.md) - Upgrades should be done before releases

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-10-20 | @tnez | Initial creation to replace Renovate automation |

---

**This runbook provides controlled, intentional dependency management without the overhead of automated PR services.**

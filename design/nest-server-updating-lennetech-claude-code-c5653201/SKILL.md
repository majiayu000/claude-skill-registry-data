---
name: nest-server-updating
description: Knowledge base for updating @lenne.tech/nest-server. Use when discussing nest-server updates, upgrades, migrations, breaking changes, or version compatibility. Provides resources, migration guide patterns, and error solutions. For execution, use the nest-server-updater agent.
---

# @lenne.tech/nest-server Update Knowledge Base

This skill provides **knowledge and resources** for updating @lenne.tech/nest-server. For automated execution, use the `nest-server-updater` agent via `/lt-dev:backend:update-nest-server`.

## When This Skill Activates

- Discussing nest-server updates or upgrades
- Asking about breaking changes between versions
- Troubleshooting update-related errors
- Planning migration strategies
- Comparing versions or checking compatibility

## Related Elements

| Element | Purpose |
|---------|---------|
| **Agent**: `nest-server-updater` | Automated execution of updates |
| **Command**: `/lt-dev:backend:update-nest-server` | User invocation |
| **Skill**: `generating-nest-servers` | Code modifications after update |
| **Skill**: `npm-package-maintenance` | Package optimization |

---

## Core Resources

### GitHub Repositories

| Resource | URL | Purpose |
|----------|-----|---------|
| **nest-server** | https://github.com/lenneTech/nest-server | Main package repository |
| **Releases** | https://github.com/lenneTech/nest-server/releases | Release notes, changelogs |
| **Migration Guides** | https://github.com/lenneTech/nest-server/tree/main/migration-guides | Version-specific migration instructions |
| **Reference Project** | https://github.com/lenneTech/nest-server-starter | Current compatible code & package versions |

### npm Package

```bash
# Package info
npm view @lenne.tech/nest-server

# Current installed version
npm list @lenne.tech/nest-server --depth=0

# All available versions
npm view @lenne.tech/nest-server versions --json
```

---

## Migration Guide System

### File Naming Convention

Migration guides in `migration-guides/` follow these patterns:

| Pattern | Example | Scope |
|---------|---------|-------|
| `X.Y.x-to-A.B.x.md` | `11.6.x-to-11.7.x.md` | Minor version step |
| `X.x-to-Y.x.md` | `11.x-to-12.x.md` | Major version jump |
| `X.Y.x-to-A.B.x.md` | `11.6.x-to-12.0.x.md` | Spanning multiple versions |

### Guide Selection Logic

For an update from version `CURRENT` to `TARGET`:

1. **List available guides:**
   ```bash
   gh api repos/lenneTech/nest-server/contents/migration-guides --jq '.[].name'
   ```

2. **Select applicable guides:**

   | Condition | Guides to load |
   |-----------|----------------|
   | Same major, sequential minor | Each `X.Y.x-to-X.Z.x.md` in sequence |
   | Major version jump | All minor guides + `X.x-to-Y.x.md` |
   | Spanning guide exists | Include it (may consolidate steps) |

3. **Load order (example 11.6.0 → 12.1.0):**
   ```
   1. 11.6.x-to-11.7.x.md
   2. 11.7.x-to-11.8.x.md
   3. ... (all minor steps to 11.x latest)
   4. 11.x-to-12.x.md (major jump)
   5. 12.0.x-to-12.1.x.md
   6. 11.6.x-to-12.x.md (if exists - consolidated)
   ```

4. **Fetch guide content:**
   ```bash
   gh api repos/lenneTech/nest-server/contents/migration-guides/11.6.x-to-11.7.x.md \
     --jq '.content' | base64 -d
   ```
   Or via URL:
   ```
   https://raw.githubusercontent.com/lenneTech/nest-server/main/migration-guides/11.6.x-to-11.7.x.md
   ```

### Fallback When No Guides Available

If `migration-guides/` is empty or no matching guides exist for the version range:

**Fallback Priority Order:**

| Priority | Source | How to Use |
|----------|--------|------------|
| 1 | **Release Notes** | Extract breaking changes from GitHub Releases |
| 2 | **Reference Project** | Compare nest-server-starter between version tags |
| 3 | **CHANGELOG.md** | Check nest-server repo for changelog entries |

**Fallback Commands:**

```bash
# Get all releases between versions
gh release list --repo lenneTech/nest-server --limit 50

# View specific release details
gh release view v11.7.0 --repo lenneTech/nest-server

# Compare reference project between versions
cd /tmp/nest-server-starter-ref
git log --oneline v11.6.0..v11.8.0
git diff v11.6.0..v11.8.0 -- package.json src/
```

**When using fallback:**
- Proceed with extra caution
- Validate more frequently (after each minor change)
- Document assumptions in the update report
- Recommend manual review before merging

---

## Version Update Strategies

**IMPORTANT:** In @lenne.tech/nest-server, **Major versions are reserved for NestJS Major versions**.
Therefore, **Minor versions are treated like Major versions** and may contain breaking changes.

### Patch Updates (X.Y.Z → X.Y.W)

- Usually safe, no breaking changes
- Use the standard update workflow (see Quick Reference → Update Workflow)
- Run tests to verify
- **Example:** `11.6.0 → 11.6.5` - direct update OK

### Minor Updates (X.Y.Z → X.W.0) ⚠️ Treat as Major!

- **May contain breaking changes** (Minor = Major in this package)
- **Always stepwise**: Update through each minor version
- Each minor step requires full validation cycle
- Migration guides are essential
- **Example:** `11.6.0 → 11.8.0` becomes `11.6 → 11.7 → 11.8`

### Major Updates (X.Y.Z → W.0.0)

- Reserved for NestJS major version changes
- **Always stepwise**: Update through each major AND minor version
- Example: `11.6.0 → 12.2.0` becomes:
  1. `11.6 → 11.7 → ... → 11.latest` (all minors)
  2. `11.latest → 12.0` (major jump)
  3. `12.0 → 12.1 → 12.2` (all minors)
- Migration guides are critical

---

## Common Error Patterns & Solutions

### TypeScript Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot find module '@lenne.tech/nest-server/...'` | Import path changed | Check migration guide for new paths |
| `Type 'X' is not assignable to type 'Y'` | API type changed | Update to new type signature per guide |
| `Property 'X' does not exist` | API removed/renamed | Check migration guide for replacement |

### Runtime Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Decorator not found` | Decorator moved | Import from new location |
| `Cannot read property of undefined` | Initialization changed | Check startup sequence in reference project |
| `Module not found` | Peer dependency missing | Compare package.json with reference project |

### Test Failures

| Symptom | Cause | Solution |
|---------|-------|----------|
| Timeout errors | Async behavior changed | Check test patterns in reference project |
| Auth failures | Auth mechanism updated | Review auth changes in migration guide |
| Validation errors | DTO changes | Update DTOs per migration guide |

---

## Reference Project Usage

The [nest-server-starter](https://github.com/lenneTech/nest-server-starter) serves as the source of truth:

### What to Check

1. **package.json**
   - Compatible dependency versions
   - New/removed dependencies
   - Script changes

2. **src/config.env.ts**
   - New configuration options
   - Changed defaults

3. **src/server/modules/**
   - Updated patterns for modules/services
   - New decorators or utilities

4. **Git history**
   ```bash
   git log --oneline --all --grep="nest-server" | head -20
   ```
   - Find commits related to version updates
   - See exactly what changed

---

## Update Modes

The `nest-server-updater` agent supports these modes:

| Mode | Flag | Behavior |
|------|------|----------|
| **Full** | (default) | Complete update with all migrations |
| **Dry-Run** | `--dry-run` | Analysis only, no changes |
| **Target Version** | `--target-version X.Y.Z` | Update to specific version |
| **Skip Packages** | `--skip-packages` | Skip npm-package-maintainer optimization |

---

## Quick Reference

### Commands

```bash
# Check current version
npm list @lenne.tech/nest-server --depth=0

# Check latest version
npm view @lenne.tech/nest-server version

# List migration guides
gh api repos/lenneTech/nest-server/contents/migration-guides --jq '.[].name'
```

### Update Workflow

**IMPORTANT:** The `npm run update` script requires a specific workflow:

1. **First:** Update the version in `package.json` to the desired target version
   ```
   "@lenne.tech/nest-server": "^X.Y.Z"
   ```

2. **Then:** Run the update script
   ```bash
   npm run update
   ```

**What `npm run update` does:**
- Verifies the specified version is available on npm
- Installs `@lenne.tech/nest-server` at the version from package.json
- Analyzes which packages inside `@lenne.tech/nest-server` were updated
- Installs those updated dependencies if they don't exist or have a lower version
- Ensures version consistency between nest-server and its peer dependencies

**Manual update (only if `npm run update` script is not available):**
```bash
npm install @lenne.tech/nest-server@X.Y.Z --save-exact
npm install
```
Note: This skips the automatic dependency synchronization that `npm run update` provides.

### Package Optimization (after npm run update)

After `npm run update` completes, run comprehensive package maintenance:

```bash
# Via command (recommended)
/lt-dev:maintenance:maintain

# Or via agent (Task tool with npm-package-maintainer in FULL MODE)
```

This ensures:
- Unused dependencies are removed
- Packages are correctly categorized (dependencies vs devDependencies)
- All packages are updated to their latest compatible versions
- Security vulnerabilities are addressed

### Validation Sequence

```bash
npm run build    # Must pass
npm run lint     # Must pass
npm test         # Must pass (no skips)
npm audit        # Should show no new vulnerabilities
```

---

## When to Use the Agent vs. Manual Update

| Scenario | Recommendation |
|----------|----------------|
| Routine update to latest | Use agent: `/lt-dev:backend:update-nest-server` |
| Check what would change | Use agent with `--dry-run` |
| Update to specific version | Use agent with `--target-version X.Y.Z` |
| Complex issues during update | Use this skill's knowledge + manual fixes |
| Understanding breaking changes | Read this skill + migration guides |

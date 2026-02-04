---
name: npm-package-maintenance
description: Guides npm package maintenance tasks. Use when user mentions outdated packages, npm audit, security vulnerabilities, dependency updates, package optimization, unused dependencies, or devDependencies categorization. Recommends the npm-package-maintainer agent via /maintain commands.
---

# NPM Package Maintenance

## When to Use This Skill

- User mentions outdated packages or wants to update dependencies
- Security vulnerabilities found via `npm audit`
- Need to optimize `dependencies` vs `devDependencies`
- Removing unused packages from `package.json`
- Pre-release or post-feature dependency cleanup
- General package maintenance or housekeeping tasks

For comprehensive npm package maintenance, use the **npm-package-maintainer agent** via the maintenance commands.

## Related Skills

- `generating-nest-servers` - For NestJS development when dependencies affect the server
- `using-lt-cli` - For Git operations after maintenance
- `nest-server-updating` - For updating @lenne.tech/nest-server (uses this agent internally)

## Available Commands

| Command | Mode | Use Case |
|---------|------|----------|
| `/lt-dev:maintain` | FULL | Complete optimization (remove unused, recategorize, update all) |
| `/lt-dev:maintain-check` | DRY-RUN | Analysis only - see what would be done without changes |
| `/lt-dev:maintain-security` | SECURITY | Fast security-only updates (npm audit vulnerabilities) |
| `/lt-dev:maintain-pre-release` | PRE-RELEASE | Conservative patch-only updates before a release |
| `/lt-dev:maintain-post-feature` | FULL | Clean up after feature development |

## When to Recommend Each Command

### `/lt-dev:maintain` (FULL MODE)
Recommend when user wants:
- Complete dependency optimization
- General maintenance / housekeeping
- "Clean up my dependencies"
- "Update all packages"

### `/lt-dev:maintain-check` (DRY-RUN)
Recommend when user wants:
- To see what would change without making changes
- Analysis or audit of current state
- "What packages are outdated?"
- "Check my dependencies"
- Pre-approval before making changes

### `/lt-dev:maintain-security` (SECURITY-ONLY)
Recommend when user mentions:
- `npm audit` vulnerabilities
- Security issues
- CVEs or security advisories
- "Fix security vulnerabilities"
- Quick/urgent security fixes

### `/lt-dev:maintain-pre-release` (PRE-RELEASE)
Recommend when user mentions:
- Preparing for a release
- "Before release"
- Wanting minimal/safe changes only
- Risk-averse updates

### `/lt-dev:maintain-post-feature` (POST-FEATURE)
Recommend when user:
- Just finished implementing a feature
- Added new dependencies
- Wants to clean up after development work

## What the Agent Does

The npm-package-maintainer agent performs 3 priorities:

1. **Remove unused packages** - Finds and removes packages not used in the codebase
2. **Optimize categorization** - Moves dev-only packages to devDependencies
3. **Update packages** - Updates to latest versions with risk-based approach

All operations ensure `npm run build` and `npm test` pass before completion.

## Quick Guidance

- **User unsure?** → Recommend `/lt-dev:maintain-check` first (safe, no changes)
- **Security urgent?** → Recommend `/lt-dev:maintain-security` (fast, focused)
- **Before release?** → Recommend `/lt-dev:maintain-pre-release` (conservative)
- **General cleanup?** → Recommend `/lt-dev:maintain` (comprehensive)

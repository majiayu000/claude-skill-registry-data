---
name: dep-upgrade
description: >
  Safe systematic dependency upgrade with vulnerability scanning
  and rollback capability. Detects project ecosystem, audits
  outdated and vulnerable packages, presents a prioritized upgrade
  plan, and executes upgrades one at a time with test verification
  after each. Use when updating dependencies, fixing vulnerability
  alerts, or performing periodic dependency maintenance.
compatibility: >
  Requires at least one package manager (go, npm, pip, cargo,
  dotnet). Works with Go, Node.js, Python, Rust, and .NET projects.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Safe Dependency Upgrade

Systematically upgrade dependencies with zero breakage. Detects the
project ecosystem, audits for outdated and vulnerable packages,
presents a prioritized plan for approval, then executes upgrades
one at a time with test verification after each.

**Core principle:** One upgrade at a time. Test after each. Roll back
on failure. Never auto-commit.

## Prerequisite check

Detect the project ecosystem by scanning for package manager files:

```bash
ls go.mod package.json pyproject.toml Cargo.toml *.csproj 2>/dev/null
```

If no package manager file is found, report to the user and stop.
Mixed projects (e.g., Go backend + Node frontend) are supported —
audit and upgrade each ecosystem separately.

## Step 1: Audit dependencies

List outdated packages and run vulnerability scanners for each
detected ecosystem.

**Go:**

```bash
go list -u -m all 2>/dev/null | grep '\['
govulncheck ./... 2>/dev/null
```

**Node.js:**

```bash
npm outdated 2>/dev/null
npm audit 2>/dev/null
```

**Python:**

```bash
pip list --outdated 2>/dev/null
pip-audit 2>/dev/null
```

**Rust:**

```bash
cargo outdated 2>/dev/null
cargo audit 2>/dev/null
```

**.NET:**

```bash
dotnet list package --outdated 2>/dev/null
dotnet list package --vulnerable 2>/dev/null
```

For detailed commands per ecosystem, see
`references/upgrade-commands.md`.

If a vulnerability scanner is not installed, note it in the report
but continue with the outdated package list.

## Step 2: Categorize and prioritize

For each outdated package, assign a priority:

- **CRITICAL** — known CVE or security advisory
- **HIGH** — major version behind or dependency EOL
- **MEDIUM** — minor version behind
- **LOW** — patch version behind only

For detailed priority signals and breaking change assessment, see
`references/priority-matrix.md`.

## Step 3: Present upgrade plan

Present the prioritized list to the user before any upgrades. Use
the plan format in `references/report-template.md`.

```text
Dependency Upgrade Plan

Ecosystem: Go
Outdated: 5 packages
Vulnerable: 1 package

| # | Package           | Current | Target | Priority |
|---|-------------------|---------|--------|----------|
| 1 | example/vuln-pkg  | v1.2.0  | v1.2.5 | CRITICAL |
| 2 | example/old-pkg   | v2.0.0  | v4.1.0 | HIGH     |
| 3 | example/minor-pkg | v3.1.0  | v3.4.0 | MEDIUM   |

Proceed with upgrades?
```

**Wait for user approval before proceeding.** The user may choose
to upgrade all, select specific packages, or skip.

## Step 4: Upgrade one at a time

For each approved package, in priority order:

1. **Research** — check changelog or release notes for breaking
   changes. If crossing a major version, read the migration guide.
2. **Upgrade** — run the ecosystem-specific upgrade command
3. **Update lockfile** — `go mod tidy`, `npm install`, etc.
4. **Run tests** — execute the project's test suite
5. **If tests pass** — move to the next package
6. **If tests fail** — roll back this upgrade immediately:

```bash
# Rollback: restore dependency files from git
git checkout -- <dependency-file> <lockfile>
```

Report the failure (package, target version, test error) and
continue with the remaining packages.

For ecosystem-specific upgrade and rollback commands, see
`references/upgrade-commands.md`.

## Step 5: Verify lockfiles

After all upgrades are complete, verify lockfile integrity:

```bash
# Go
go mod verify

# Node
npm ci --dry-run

# Rust
cargo build --dry-run
```

Confirm that lockfiles are updated and consistent with the
dependency manifest.

## Step 6: Present summary

Present the upgrade results using the template in
`references/report-template.md`. Include:

1. **Successfully upgraded** — package, from version, to version,
   test status
2. **Failed and rolled back** — package, target version, failure
   reason
3. **Skipped** — package, reason (user chose to skip, or breaking
   change needs manual migration)
4. **Remaining vulnerabilities** — any CVEs not resolved
5. **Lockfile status** — updated and verified per ecosystem

Do **not** commit the changes. The user decides when and how to
commit. Suggest a commit message:

```text
deps: upgrade X packages (Y security fixes)
```

## Important constraints

- **Never auto-commit** — upgrading packages changes files, but
  committing is the user's decision
- **Never create branches** — leave git operations to the user
- **One at a time** — upgrading multiple packages simultaneously
  makes it impossible to identify which upgrade broke tests
- **Roll back immediately on failure** — do not continue with a
  broken dependency state
- **Report everything** — even if the user chose to skip a
  package, include it in the summary with the reason

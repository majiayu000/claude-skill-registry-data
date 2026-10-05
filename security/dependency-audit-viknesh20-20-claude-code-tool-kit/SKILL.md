---
name: dependency-audit
description: "Audits project dependencies for known vulnerabilities, outdated packages, unused dependencies, and license compliance. Works with npm, pip, cargo, go modules, and more."
argument-hint: "[optional: 'security', 'outdated', 'unused', or 'all']"
allowed-tools: Read, Grep, Glob, Bash
---

# Dependency Audit

## Detect Package Manager
!`ls package.json package-lock.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null`
!`ls requirements.txt Pipfile Pipfile.lock pyproject.toml poetry.lock 2>/dev/null`
!`ls go.mod go.sum 2>/dev/null`
!`ls Cargo.toml Cargo.lock 2>/dev/null`
!`ls Gemfile Gemfile.lock 2>/dev/null`
!`ls *.csproj *.sln 2>/dev/null`
!`ls composer.json composer.lock 2>/dev/null`
!`ls mix.exs mix.lock 2>/dev/null`

---

## Audit Checks

### 1. Security Vulnerabilities
Run the appropriate audit command:

| Ecosystem | Command |
|-----------|---------|
| npm | `npm audit --json` |
| yarn | `yarn audit --json` |
| pnpm | `pnpm audit --json` |
| pip | `pip audit 2>/dev/null \|\| pip-audit 2>/dev/null` |
| Go | `govulncheck ./... 2>/dev/null` |
| Rust | `cargo audit 2>/dev/null` |
| Ruby | `bundle audit check 2>/dev/null` |
| .NET | `dotnet list package --vulnerable 2>/dev/null` |
| PHP | `composer audit 2>/dev/null` |

For each vulnerability found:
- Package name and version
- CVE ID or advisory ID
- Severity (Critical/High/Medium/Low)
- Fixed version (if available)
- Whether it's a direct or transitive dependency

### 2. Outdated Dependencies
Run the appropriate command:

| Ecosystem | Command |
|-----------|---------|
| npm | `npm outdated --json` |
| pip | `pip list --outdated 2>/dev/null` |
| Go | `go list -m -u all 2>/dev/null` |
| Rust | `cargo outdated 2>/dev/null` |
| Ruby | `bundle outdated 2>/dev/null` |

Classify updates:
- **Patch** (1.0.0 → 1.0.1): Usually safe, bug fixes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Major** (1.0.0 → 2.0.0): Breaking changes, needs review

### 3. Unused Dependencies
Look for dependencies that are imported in package manifest but never referenced in code:

1. Read the dependency list from the manifest
2. For each dependency, search the codebase for imports/requires
3. Flag any dependency with zero references as potentially unused

Note: Some dependencies are used via CLI, plugins, or config — verify before removing.

### 4. License Compliance
Check for problematic licenses:
- **Copyleft** (GPL, AGPL): May require releasing your code
- **Permissive** (MIT, Apache, BSD): Generally safe for commercial use
- **Unknown/No License**: Risk — treat as all rights reserved

---

## Output Format

### Vulnerability Summary
| Package | Version | Severity | CVE | Fix Available |
|---------|---------|----------|-----|---------------|

### Outdated Packages
| Package | Current | Latest | Update Type | Breaking? |
|---------|---------|--------|-------------|-----------|

### Potentially Unused
| Package | Last Import Found | Recommendation |
|---------|-------------------|----------------|

### License Concerns
| Package | License | Risk Level |
|---------|---------|------------|

### Recommendations
1. **Immediate**: Critical/High vulnerabilities with available fixes
2. **Short-term**: Major version updates for key dependencies
3. **Backlog**: Minor updates and cleanup of unused dependencies

### Health Score
Rate dependency health from **0 to 10** (10 = all up to date, no vulns).

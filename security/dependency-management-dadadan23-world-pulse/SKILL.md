---
name: "dependency-management"
description: 'Manage dependencies with version pinning, lock files, vulnerability scanning, and update strategies. Use when adding new packages, pinning dependency versions, scanning for vulnerabilities, updating outdated dependencies, or managing monorepo dependency graphs.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Dependency Management

> **Purpose**: Manage third-party dependencies securely and reliably. 
> **Goal**: Reproducible builds, no vulnerable packages, controlled updates. 
> **Note**: For implementation, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## When to Use This Skill

- Adding new packages or libraries
- Pinning dependency versions for reproducibility
- Scanning for known vulnerabilities
- Updating outdated dependencies safely
- Managing monorepo dependency graphs

## Prerequisites

- Package manager installed (npm, pip, NuGet, cargo, etc.)

## Decision Tree

```
Dependency concern?
+- Adding new dependency?
| +- Actively maintained? (commits in last 6 months) -> Proceed
| +- License compatible? (MIT/Apache -> OK, GPL -> careful)
| +- Too many transitive deps? -> Consider lighter alternative
| - Can you build it in < 1 hour? -> Maybe don't add dependency
+- Updating dependencies?
| +- Patch update (0.0.x) -> Usually safe, auto-update
| +- Minor update (0.x.0) -> Review changelog, test
| - Major update (x.0.0) -> Review breaking changes, plan migration
+- Vulnerability found?
| +- Direct dependency? -> Update immediately
| - Transitive? -> Override version or update parent
- Lock file conflict?
 - Delete lock file -> reinstall -> commit new lock file
```

## Core Concepts

### Dependency Types

```
Direct Dependencies:
 - Packages your code imports directly
 - Listed in your package manifest

Transitive Dependencies:
 - Dependencies of your dependencies
 - Automatically pulled in
 - Often source of vulnerabilities

Development Dependencies:
 - Testing frameworks
 - Build tools
 - Linters
 - NOT shipped to production
```

### Dependency Files

```
Manifest File (what you want):
 - Lists packages and version constraints
 - Human-editable
 - Committed to version control

Lock File (what you get):
 - Lists exact versions resolved
 - Includes transitive dependencies
 - Machine-generated
 - Committed to version control

Examples by Language:
 Language | Manifest | Lock File
 ------------|--------------------|-----------------
 .NET | *.csproj | packages.lock.json
 Python | pyproject.toml | poetry.lock
 Node.js | package.json | package-lock.json
 Go | go.mod | go.sum
 Rust | Cargo.toml | Cargo.lock
```

---

## Best Practices Summary

| Practice | Description |
|----------|-------------|
| **Use lock files** | Commit and respect lock files |
| **Pin production deps** | Exact versions for reproducibility |
| **Scan regularly** | Automated vulnerability scanning |
| **Update strategically** | Patch often, minor carefully, major planned |
| **Minimize dependencies** | Every dep is a liability |
| **Review licenses** | Ensure compatibility |
| **Separate dev deps** | Don't ship test frameworks |
| **Audit new deps** | Evaluate before adding |

---

## Dependency Management Tools

| Language | Package Manager | Vulnerability Scanner |
|----------|-----------------|----------------------|
| **.NET** | NuGet, dotnet | `dotnet list package --vulnerable` |
| **Python** | pip, poetry | pip-audit, safety |
| **Node.js** | npm, yarn, pnpm | `npm audit`, Snyk |
| **Java** | Maven, Gradle | OWASP Dependency-Check |
| **Go** | go mod | govulncheck |
| **Rust** | Cargo | cargo-audit |

---

**See Also**: [Security](../../architecture/security/SKILL.md) - [C# Development](../csharp/SKILL.md) - [Python Development](../python/SKILL.md)

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`audit-deps.ps1`](scripts/audit-deps.ps1) | Audit for outdated/vulnerable dependencies (.NET/Python/Node) | `./scripts/audit-deps.ps1 [-FailOnVulnerability]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Conflicting dependency versions | Use package manager resolution strategy, check peer dependency requirements |
| Vulnerability found in transitive dep | Override/force specific version, or find alternative package |
| Lock file merge conflicts | Delete lock file, reinstall dependencies, commit fresh lock file |

## References

- [Versioning Scanning Updates](references/versioning-scanning-updates.md)
- [Selection And Monorepo](references/selection-and-monorepo.md)
---
name: managing-nuget
description: |
  Use when working with Nuget — nuGet package registry management. Covers
  package publishing, version management, dependency resolution, package source
  configuration, vulnerability scanning, and .NET project analysis. Use when
  managing NuGet packages, configuring package sources, resolving version
  conflicts, or auditing package security.
connection_type: nuget
preload: false
---

# NuGet Registry Management Skill

Manage and analyze NuGet packages, sources, dependencies, and .NET project configurations.

## MANDATORY: Discovery-First Pattern

**Always check current project and NuGet configuration before modifying packages.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== NuGet Sources ==="
dotnet nuget list source 2>/dev/null

echo ""
echo "=== Project Files ==="
find . -name "*.csproj" -o -name "*.fsproj" -o -name "*.vbproj" 2>/dev/null | head -10

echo ""
echo "=== NuGet Config ==="
cat nuget.config 2>/dev/null || cat NuGet.Config 2>/dev/null | head -15

echo ""
echo "=== .NET Version ==="
dotnet --version 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Package References ==="
grep -rh 'PackageReference' *.csproj 2>/dev/null | sed 's/.*Include="/  /;s/" Version="/  v/;s/".*//' | head -15

echo ""
echo "=== Outdated Packages ==="
dotnet list package --outdated 2>/dev/null | head -20

echo ""
echo "=== Vulnerable Packages ==="
dotnet list package --vulnerable 2>/dev/null | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List packages with current and latest versions
- Report vulnerabilities by severity
- Never expose NuGet API keys in output

## Common Operations

### Package Lookup

```bash
#!/bin/bash
PACKAGE="${1:?Package name required}"
echo "=== Package: $PACKAGE ==="
curl -s "https://api.nuget.org/v3/registration5-gz-semver2/${PACKAGE,,}/index.json" | jq '{
  id: .items[0].items[-1].catalogEntry.id,
  version: .items[0].items[-1].catalogEntry.version,
  description: .items[0].items[-1].catalogEntry.description,
  authors: .items[0].items[-1].catalogEntry.authors
}' 2>/dev/null
```

### Pack and Publish Preview

```bash
#!/bin/bash
echo "=== Pack Preview ==="
dotnet pack --no-build 2>&1 | tail -10
ls -la bin/Release/*.nupkg 2>/dev/null
```

## Safety Rules

- **Never expose NuGet API keys** in configuration or logs
- **Use `dotnet pack` dry runs** before publishing
- **Review vulnerability reports** before deploying to production
- **Lock package versions** in production projects to avoid unexpected updates

## Output Format

Present results as a structured report:
```
Managing Nuget Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |


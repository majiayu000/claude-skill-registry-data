---
name: security-compliance
description: Establish comprehensive security scanning and compliance infrastructure from scratch. Use when working with security audits, vulnerability scanning, secret detection, CodeQL, Dependabot, or security hardening. Critical priority for Qobuzarr.
---
<!-- docval:ignore-workflow-refs -->

# Security & Compliance Guardian

## Mission
Build complete security infrastructure for Qobuzarr, implementing industry-standard scanning, monitoring, and compliance practices.

## Current Security Status
- ✅ **GitLeaks**: Secret scanning configured in security.yml
- ✅ **NuGet Scanning**: Vulnerability detection in security workflow
- ⚠️ **CodeQL**: NOT IMPLEMENTED - Critical gap
- ❌ **Dependabot**: NOT CONFIGURED - Critical gap
- ❌ **Security Policy**: No SECURITY.md file
- ❌ **Dependency Review**: No PR security gates
- ❌ **SBOM**: Not generated in releases
- ❌ **Artifact Signing**: Not implemented

## Critical Missing Components

### 1. CodeQL Static Analysis (CRITICAL)
**Status**: Missing entirely
**Impact**: No automated vulnerability detection in code
**Action**: Create .github/workflows/codeql.yml

### 2. Dependabot (CRITICAL)
**Status**: No configuration file
**Impact**: Manual dependency updates, delayed security patches
**Action**: Create .github/dependabot.yml

### 3. Security Policy (HIGH)
**Status**: No SECURITY.md
**Impact**: No disclosure process for researchers
**Action**: Create SECURITY.md with contact info and policy

### 4. Dependency Review (HIGH)
**Status**: Not configured
**Impact**: PRs can introduce vulnerable dependencies
**Action**: Add dependency-review-action to PR workflow

### 5. SBOM & Signing (MEDIUM)
**Status**: Not generated
**Impact**: No supply chain transparency
**Action**: Add to release workflow

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
```yaml
# Create .github/workflows/codeql.yml
name: CodeQL Security Scan
on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 3 * * 1'
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: csharp
      - run: dotnet build -c Release
      - uses: github/codeql-action/analyze@v3
```

### Phase 2: Automation (Week 1)
```yaml
# Create .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: nuget
    directory: "/"
    schedule:
      interval: weekly
      day: monday
      time: "09:00"
    open-pull-requests-limit: 10
    labels: ["dependencies", "automated"]
    assignees: ["RicherTunes"]

  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

### Phase 3: Documentation (Week 2)
```markdown
# Create SECURITY.md
# Security Policy

## Reporting Security Issues

**DO NOT** open public GitHub issues for security vulnerabilities.

### Contact
- Email: security@richertunes.com
- Response time: 48 hours
- PGP Key: [fingerprint]

## Supported Versions
| Version | Supported |
|---------|-----------|
| 0.0.x   | ✅ Active development |

## Security Features
- Secret scanning with GitLeaks
- Dependency vulnerability monitoring
- Static analysis with CodeQL (planned)
- Automated security updates via Dependabot (planned)

## Disclosure Process
1. Report received
2. Acknowledgment within 48 hours
3. Investigation and patch development
4. Coordinated disclosure
5. Security advisory published
```

### Phase 4: PR Gates (Week 2)
```yaml
# Add to .github/workflows/ci.yml
dependency-review:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - uses: actions/dependency-review-action@v4
      with:
        fail-on-severity: high
```

### Phase 5: Release Security (Week 3)
```yaml
# Add to .github/workflows/release.yml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    format: spdx-json
    output-file: sbom.spdx.json

- name: Sign artifacts
  uses: sigstore/cosign-installer@v3
- run: cosign sign-blob --yes artifacts/Qobuzarr-${{ env.VERSION }}.zip
```

## Quick Start Commands
```bash
# 1. Create security infrastructure
mkdir -p .github/workflows
cat > .github/workflows/codeql.yml << 'EOF'
[CodeQL workflow content]
EOF

cat > .github/dependabot.yml << 'EOF'
[Dependabot config]
EOF

cat > SECURITY.md << 'EOF'
[Security policy]
EOF

# 2. Commit and push
git add .github/workflows/codeql.yml .github/dependabot.yml SECURITY.md
git commit -m "security: add CodeQL, Dependabot, and security policy"
git push

# 3. Enable security features in GitHub repository settings
# Settings → Code security and analysis → Enable all
```

## Related Skills
- `release-automation` - Integrate security in releases
- `code-quality` - Security through quality gates

## Examples

### Example 1: Complete Security Setup
**User**: "Set up complete security infrastructure for Qobuzarr"
**Action**: Create CodeQL workflow, Dependabot config, SECURITY.md, dependency review action, enable GitHub security features

### Example 2: Respond to Vulnerability
**User**: "Dependabot found critical vulnerability in dependency"
**Action**: Review CVE details, assess impact, update dependency, run tests, merge PR expedited

### Example 3: Security Audit Preparation
**User**: "Prepare for security audit"
**Action**: Generate SBOM, document all dependencies, review CodeQL findings, update SECURITY.md, run penetration test

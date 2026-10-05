---
name: dependency-security-audit
description: Audit project dependencies for known vulnerabilities (CVEs), license issues, and outdated packages with SBOM generation. Use when deploying to production.
---

# Dependency Security Audit

Systematically audit all project dependencies for known security vulnerabilities (CVEs), license compliance issues, and outdated packages. Generate comprehensive Software Bill of Materials (SBOM) and provide actionable remediation strategies across all supported languages.

## When to Use This Skill

Use this skill when you need to:

- Audit dependencies before production deployment
- Comply with security requirements (SOC 2, ISO 27001)
- Respond to newly disclosed vulnerabilities
- Onboard third-party or legacy code
- Prepare for security certification
- Establish supply chain security baseline
- Generate SBOM for compliance reporting
- Verify open-source license compatibility
- Perform quarterly or monthly security reviews

**Trigger phrases**: "dependency audit", "security scan", "vulnerability check", "CVE scan", "SBOM", "supply chain security", "npm audit", "pip-audit"

## What This Skill Does

### Core Capabilities

- **Vulnerability Scanning**: Detect known CVEs in all dependencies
- **License Auditing**: Identify license compliance issues
- **Outdated Package Detection**: Find dependencies with security patches
- **Transitive Dependency Analysis**: Audit indirect dependencies
- **SBOM Generation**: Create complete software bill of materials
- **Risk Prioritization**: CVSS scoring and exploitability assessment
- **Remediation Guidance**: Actionable fix recommendations

### Language Support

| Language | Package Managers | Scanning Tools |
|----------|------------------|----------------|
| Python | pip, poetry, pipenv | pip-audit, safety, bandit |
| JavaScript | npm, yarn, pnpm | npm audit, snyk, yarn audit |
| Java | Maven, Gradle | OWASP Dependency-Check |
| C# | NuGet | dotnet CLI, dotnet-outdated |
| Go | go modules | govulncheck, nancy |
| C/C++ | Conan, vcpkg | cppcheck, flawfinder |

## Prerequisites

- Package manager configuration files accessible
- Network access to vulnerability databases
- Command-line tool installation permissions
- CI/CD pipeline access for automation (recommended)

## Instructions

### Step 1: Install Security Scanning Tools

#### Python

```bash
# Install pip-audit (official Python auditing tool)
pip install pip-audit

# Install safety (alternative scanner)
pip install safety

# Install bandit (SAST tool with dependency checks)
pip install bandit[toml]

# Install pip-licenses (license scanner)
pip install pip-licenses

# Install cyclonedx-bom (SBOM generator)
pip install cyclonedx-bom
```

#### JavaScript/TypeScript

```bash
# NPM audit (built-in)
# No installation needed

# Install Snyk CLI
npm install -g snyk

# Install npm-check-updates
npm install -g npm-check-updates

# Install license-checker
npm install -g license-checker

# Install CycloneDX for Node.js
npm install -g @cyclonedx/cyclonedx-npm
```

#### Java

```xml
<!-- OWASP Dependency-Check (Maven plugin) -->
<!-- Add to pom.xml: -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.4.0</version>
</plugin>
```

#### C#

```bash
# dotnet CLI tools (built-in vulnerability scanning)
dotnet list package --vulnerable

# Install dotnet-outdated
dotnet tool install -g dotnet-outdated-tool

# Install CycloneDX for .NET
dotnet tool install -g CycloneDX
```

#### Go

```bash
# Install govulncheck (official Go vulnerability scanner)
go install golang.org/x/vuln/cmd/govulncheck@latest

# Install Nancy (Sonatype vulnerability scanner)
go install github.com/sonatype-nexus-community/nancy@latest

# Install go-licenses
go install github.com/google/go-licenses@latest

# Install cyclonedx-gomod
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
```

### Step 2: Run Vulnerability Scans

#### Python - Comprehensive Scan

```bash
# 1. Scan with pip-audit (recommended primary tool)
pip-audit --desc --format json --output pip-audit-report.json
pip-audit --desc  # Human-readable output

# 2. Scan with safety
safety check --json --output safety-report.json
safety check --full-report

# 3. Check for outdated packages with security fixes
pip list --outdated --format json > outdated-packages.json

# 4. Detailed vulnerability information
pip-audit --vulnerability-service osv --format cyclonedx-json --output sbom.json

# 5. Fix available vulnerabilities (dry run first)
pip-audit --fix --dry-run
```

**Example Output Analysis**:
```
Found 3 known vulnerabilities in 2 packages

Name      Version  Vulnerability  CVSS  Fix Available
────────────────────────────────────────────────────
requests  2.25.0   CVE-2023-32681  6.1   2.31.0
urllib3   1.26.0   CVE-2023-43804  8.6   1.26.17
urllib3   1.26.0   CVE-2023-45803  4.2   1.26.17
```

#### JavaScript/TypeScript - Comprehensive Scan

```bash
# 1. NPM audit (built-in, fast)
npm audit --json > npm-audit.json
npm audit

# 2. Yarn audit (if using Yarn)
yarn audit --json > yarn-audit.json
yarn audit

# 3. Snyk comprehensive scan (requires account)
snyk auth  # First time only
snyk test --json > snyk-report.json
snyk test --severity-threshold=medium

# 4. Check for updates
npm-check-updates
ncu --doctor  # Test updates safely

# 5. Fix vulnerabilities automatically
npm audit fix --dry-run  # Preview changes
npm audit fix  # Apply fixes
npm audit fix --force  # Force major version updates (risky)
```

#### Java - Comprehensive Scan

```bash
# Maven Projects
mvn dependency-check:check
mvn dependency-check:check -DfailBuildOnCVSS=7

# Output location: target/dependency-check-report.html

# Check for dependency updates
mvn versions:display-dependency-updates

# Analyze dependency tree
mvn dependency:tree > dependency-tree.txt
mvn dependency:analyze

# Generate SBOM
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
```

#### C# - Comprehensive Scan

```bash
# 1. Built-in vulnerability scanning
dotnet list package --vulnerable
dotnet list package --vulnerable --include-transitive

# 2. Check for outdated packages
dotnet-outdated

# 3. Check for deprecated packages
dotnet list package --deprecated

# 4. Generate SBOM
CycloneDX -o sbom.xml -s solution.sln
```

#### Go - Comprehensive Scan

```bash
# 1. govulncheck (official Go vulnerability scanner)
govulncheck ./...
govulncheck -json ./... > govulncheck-report.json

# 2. Nancy scanner
go list -json -deps ./... | nancy sleuth
nancy sleuth -p go.sum

# 3. Check module updates
go list -u -m all

# 4. Module verification
go mod verify
go mod tidy

# 5. Generate SBOM
cyclonedx-gomod app -json=true -output sbom.json
```

### Step 3: License Compliance Audit

#### Python - License Audit

```bash
# 1. Generate license report
pip-licenses --format=markdown --output-file=licenses.md
pip-licenses --format=json --output-file=licenses.json

# 2. Check for specific license types
pip-licenses --summary

# 3. Identify packages with unknown licenses
pip-licenses | grep "UNKNOWN"
```

#### JavaScript/TypeScript - License Audit

```bash
# 1. Generate license report
license-checker --json > licenses.json
license-checker --csv > licenses.csv

# 2. Check for specific licenses
license-checker --onlyAllow "MIT;Apache-2.0;BSD-3-Clause"

# 3. Exclude licenses
license-checker --exclude "GPL;AGPL"
```

**Common License Compatibility Issues**:

| Your License | Compatible Dependency Licenses | Incompatible |
|--------------|-------------------------------|--------------|
| MIT | MIT, Apache 2.0, BSD, ISC | GPL*, AGPL* |
| Apache 2.0 | MIT, Apache 2.0, BSD | GPL 2.0, AGPL |
| GPL 3.0 | MIT, BSD, Apache 2.0, GPL | Proprietary |
| Proprietary | MIT, BSD, Apache 2.0 | GPL*, AGPL* |

### Step 4: Generate Software Bill of Materials (SBOM)

```bash
# Python - CycloneDX format
cyclonedx-py --format json --output sbom.json
cyclonedx-py --format xml --output sbom.xml

# JavaScript - CycloneDX for NPM
cyclonedx-npm --output-file sbom.json

# Java - Maven
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# C# - CycloneDX for .NET
CycloneDX -o sbom.json -f JSON -s solution.sln

# Go - CycloneDX for Go
cyclonedx-gomod app -json=true -output sbom.json
```

**SBOM Use Cases**:
- Compliance reporting (FDA, NTIA, Executive Orders)
- Vulnerability management (track affected components)
- License compliance documentation
- Supply chain risk assessment
- Incident response (identify affected systems)

### Step 5: Analyze and Prioritize Vulnerabilities

#### Severity Classification

**CVSS Score Ranges**:
- **Critical (9.0-10.0)**: Immediate action required
- **High (7.0-8.9)**: Urgent attention needed
- **Medium (4.0-6.9)**: Plan remediation
- **Low (0.1-3.9)**: Address when possible

**Prioritization Matrix**:

```
High Exploitability + High Impact = P0 (Fix immediately)
High Exploitability + Low Impact  = P1 (Fix this sprint)
Low Exploitability + High Impact  = P1 (Fix this sprint)
Low Exploitability + Low Impact   = P2 (Plan for future)
```

**Exploitability Factors**:
- [ ] Public exploit code available
- [ ] Vulnerability in internet-facing component
- [ ] No authentication required
- [ ] Easy to exploit (low complexity)
- [ ] Actively being exploited in the wild

**Impact Factors**:
- [ ] Affects production systems
- [ ] Handles sensitive data
- [ ] Critical business function
- [ ] Regulatory compliance requirement
- [ ] Customer-facing component

### Step 6: Plan Remediation Strategy

#### Remediation Approaches

**1. Direct Upgrade (Preferred)**
```bash
# Python
pip install --upgrade package_name==secure_version

# JavaScript
npm update package_name@secure_version

# C#
dotnet add package PackageName --version secure_version

# Go
go get package@secure_version
```

**2. Transitive Dependency Override**

When vulnerable package is an indirect dependency:

**JavaScript** (package.json):
```json
{
  "overrides": {
    "vulnerable-package": "^secure-version"
  }
}
```

**Java** (pom.xml):
```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.example</groupId>
      <artifactId>vulnerable-package</artifactId>
      <version>secure-version</version>
    </dependency>
  </dependencies>
</dependencyManagement>
```

**3. Find Alternative Package**

When no secure version exists:
- Search for actively maintained alternatives
- Compare features and migration effort
- Verify alternative doesn't have same issues

**4. Remove Dependency**

If not critical:
- Implement functionality yourself
- Use standard library alternative
- Reconsider if feature is necessary

### Step 7: Automate Dependency Scanning in CI/CD

#### GitHub Actions Integration

```yaml
# .github/workflows/dependency-scan.yml
name: Dependency Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Python Projects
      - name: Set up Python
        if: hashFiles('requirements.txt') != ''
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install pip-audit
        if: hashFiles('requirements.txt') != ''
        run: pip install pip-audit

      - name: Run pip-audit
        if: hashFiles('requirements.txt') != ''
        run: |
          pip-audit --desc --format json --output pip-audit-report.json
          pip-audit
        continue-on-error: true

      # JavaScript Projects
      - name: Set up Node.js
        if: hashFiles('package.json') != ''
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Run npm audit
        if: hashFiles('package.json') != ''
        run: |
          npm audit --json > npm-audit.json
          npm audit
        continue-on-error: true

      # Upload Results
      - name: Upload Security Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-scan-reports
          path: |
            *-audit-report.json
            snyk-report.json
```

#### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Python
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"

  # JavaScript
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  # Java
  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Step 8: Generate Comprehensive Audit Report

```markdown
# Dependency Security Audit Report

**Project**: [Project Name]
**Audit Date**: [YYYY-MM-DD]
**Auditor**: [Name]
**Next Audit**: [YYYY-MM-DD]

## Executive Summary

- **Total Dependencies**: [Direct: X, Transitive: Y, Total: Z]
- **Vulnerabilities Found**: [Count]
  - Critical: [Count] (CVSS 9.0-10.0)
  - High: [Count] (CVSS 7.0-8.9)
  - Medium: [Count] (CVSS 4.0-6.9)
  - Low: [Count] (CVSS 0.1-3.9)
- **License Issues**: [Count]
- **Outdated Packages**: [Count with security patches]
- **Risk Rating**: [Critical / High / Medium / Low]

## Critical Vulnerabilities (P0)

### CVE-XXXX-XXXXX - Remote Code Execution
- **Package**: lodash@4.17.15
- **Fixed Version**: 4.17.21
- **CVSS Score**: 9.8 (Critical)
- **Deadline**: Within 24 hours

## Remediation Roadmap

### Phase 1: Critical (This Week)
- [ ] Fix CVE-XXXX-XXXXX (lodash) - 2 hours
- [ ] Fix CVE-XXXX-YYYYY (requests) - 4 hours

### Phase 2: High Priority (This Sprint)
- [ ] Fix CVE-XXXX-ZZZZZ (urllib3) - 3 hours

### Phase 3: Medium Priority (Next Sprint)
- [ ] Update 12 outdated packages - 1 day

## SBOM Generated
- **Format**: CycloneDX 1.5
- **File**: sbom.json
```

## Common Pitfalls and Solutions

### Pitfall 1: Only Scanning Direct Dependencies

**Problem**: Transitive dependencies often contain vulnerabilities but are overlooked.

**Solution**: Always scan with `--include-transitive` or equivalent flag.

```bash
# C#
dotnet list package --vulnerable --include-transitive
```

### Pitfall 2: Ignoring Low-Severity Vulnerabilities

**Problem**: Low-severity issues accumulate and may become critical in combination.

**Solution**: Address all vulnerabilities systematically. Low-severity issues are often easy fixes.

### Pitfall 3: Blocking on Unfixable Vulnerabilities

**Problem**: Some vulnerabilities have no fix available, blocking development.

**Solution**:
- Assess actual exploitability in your context
- Implement compensating controls (WAF, input validation)
- Consider alternative packages
- Document accepted risk with approval

### Pitfall 4: Not Testing Dependency Updates

**Problem**: Updating dependencies breaks functionality without proper testing.

**Solution**: Always test dependency updates thoroughly before deploying.

```bash
# Create test branch
git checkout -b deps/security-updates

# Update dependencies
npm update package@version

# Run full test suite
npm test
```

## Quality Checklist

- [ ] All package managers identified and scanned
- [ ] Vulnerability scanning completed for all languages
- [ ] Transitive dependencies analyzed
- [ ] License compliance verified
- [ ] SBOM generated and stored
- [ ] Critical vulnerabilities prioritized with CVSS scores
- [ ] Remediation roadmap created with timelines
- [ ] Automated scanning integrated into CI/CD
- [ ] Continuous monitoring enabled (Dependabot/Snyk)
- [ ] Comprehensive audit report generated

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We scan direct dependencies, which covers the risk" | The Log4Shell (CVE-2021-44228) vulnerability was in a transitive dependency (log4j-core) that many teams did not know they had; transitive scanning is mandatory, not optional. |
| "Low-severity CVEs are not worth fixing" | Chained exploits combine multiple low-severity issues; a CVSS 3.9 information-disclosure CVE paired with a CVSS 3.1 path-traversal has enabled full database exfiltration in documented incidents. |
| "npm audit produces too many false positives to be useful" | Configuring a severity threshold (`--audit-level=moderate`) and suppressing accepted risks in `.auditignore` reduces noise without abandoning the scan; ignoring the entire tool leaves real P0 CVEs undetected. |
| "We will scan once before the release, not continuously" | The Equifax breach (2017) exploited Apache Struts CVE-2017-5638, which had a published fix 2 months before the breach; continuous scanning with Dependabot or Snyk would have surfaced the CVE within hours of disclosure. |
| "Pinning versions is too maintenance-heavy" | Unpinned ranges (`^1.0.0`) allowed the `event-stream` supply chain attack to push a malicious patch version to thousands of downstream packages without triggering a manual review. |
| "SBOM generation is only needed for regulated industries" | SBOM enables incident response teams to determine within minutes whether a newly disclosed CVE affects any system; without it, identifying affected services can take days of manual dependency archaeology. |

## Verification

- [ ] Vulnerability scan completed for all package managers in the project with output saved (e.g., `pip-audit-report.json`, `npm-audit.json`)
- [ ] Transitive dependencies scanned (e.g., `dotnet list package --vulnerable --include-transitive`)
- [ ] All Critical (CVSS >= 9.0) and High (CVSS >= 7.0) findings have a documented remediation action or accepted-risk record
- [ ] License compliance report generated and reviewed for GPL/AGPL conflicts with the project's license
- [ ] SBOM generated in CycloneDX or SPDX format and stored as a build artifact
- [ ] Automated scanning (Dependabot, Snyk, or equivalent) configured in CI/CD with at least weekly runs

## Related Skills

- `security-review` - Application-level security audit
- `pre-commit-checklist` - Pre-commit security checks
- `licensing-compliance` - License checking

## Additional Resources

### Vulnerability Databases
- [National Vulnerability Database (NVD)](https://nvd.nist.gov/)
- [OSV - Open Source Vulnerabilities](https://osv.dev/)
- [Snyk Vulnerability Database](https://security.snyk.io/)
- [GitHub Advisory Database](https://github.com/advisories)

### SBOM Standards
- [CycloneDX](https://cyclonedx.org/)
- [SPDX](https://spdx.dev/)
- [NTIA SBOM Guidelines](https://www.ntia.gov/sbom)

### Security Tools
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [Snyk](https://snyk.io/)
- [Dependabot](https://github.com/dependabot)
- [Renovate](https://renovatebot.com/)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: OWASP Dependency-Check, Snyk Security Best Practices, NIST Software Supply Chain Guidelines


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.

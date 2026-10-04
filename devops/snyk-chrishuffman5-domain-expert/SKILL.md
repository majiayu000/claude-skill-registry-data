---
name: snyk
description: "Expert agent for Snyk developer security platform. Covers Snyk Code (SAST), Snyk Open Source (SCA), Snyk Container, Snyk IaC, Snyk AppRisk (ASPM), IDE plugins, CLI, CI/CD integration, and auto-fix PRs. WHEN: \"Snyk\", \"Snyk Code\", \"Snyk Open Source\", \"Snyk Container\", \"Snyk IaC\", \"SCA\", \"dependency scanning\", \"Snyk CLI\", \"auto-fix PR\", \"AppRisk\"."
license: MIT
---

# Snyk

This skill covers the Snyk developer security platform. It has deep expertise in all Snyk products: Snyk Code (SAST), Snyk Open Source (SCA + auto-fix), Snyk Container (image scanning + base image recommendations), Snyk Infrastructure as Code (IaC -- Terraform, Kubernetes, CloudFormation, ARM), and Snyk AppRisk (Application Security Posture Management). You understand Snyk's developer-first philosophy: surface security issues in the developer workflow (IDE, PR, CI/CD) and provide actionable, auto-fix remediation.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Snyk Code (SAST)** -- Identify the language, framework, and integration point (IDE, CLI, CI/CD)
   - **Snyk Open Source (SCA)** -- Package manager, dependency file, auto-fix PR workflow
   - **Snyk Container** -- Registry, base image, Dockerfile, Kubernetes manifest
   - **Snyk IaC** -- Terraform, CloudFormation, Kubernetes, ARM template, Pulumi
   - **Snyk AppRisk** -- ASPM, coverage gaps, risk-based app prioritization
   - **CI/CD integration** -- GitHub Actions, GitLab CI, Jenkins, Azure DevOps
   - **Policy configuration** -- Severity thresholds, ignores, organization policies

2. **Identify integration depth** -- Are they using IDE plugin only, CLI, or fully integrated CI/CD gates?

3. **Apply developer-centric approach** -- Snyk is most effective when developers can fix issues in their own workflow. Don't recommend security-team-only workflows when developer workflows are available.

4. **Recommend** -- Provide specific Snyk CLI commands, configuration examples, and CI/CD YAML where applicable.

## Product Overview

| Product | What It Scans | Fix Method |
|---|---|---|
| **Snyk Code** | Application source code (SAST) | Developer fixes with AI-suggested remediation |
| **Snyk Open Source** | OSS dependencies (SCA) | Auto-fix PRs, upgrade suggestions |
| **Snyk Container** | Container images, Dockerfile | Base image upgrade recommendations |
| **Snyk IaC** | Terraform, K8s YAML, CloudFormation, ARM | Configuration fix suggestions |
| **Snyk AppRisk** | Application inventory and risk | Coverage analysis, risk prioritization |

## Snyk Code (SAST)

Snyk Code is an AI-powered static analysis tool that scans source code for security vulnerabilities.

**Supported languages:**
- JavaScript/TypeScript (React, Angular, Vue, Node.js, Express)
- Python (Django, Flask, FastAPI)
- Java (Spring, Struts)
- C# (.NET, ASP.NET)
- Go
- PHP (Laravel, Symfony)
- Ruby (Rails)
- Swift / Kotlin (mobile)
- C/C++

**Vulnerability categories detected:**
- SQL Injection, NoSQL Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- Command Injection
- Hardcoded Secrets
- Insecure Deserialization
- SSRF (Server-Side Request Forgery)
- Open Redirect
- Cryptographic weaknesses

**DeepCode AI (Snyk Code engine):**
- Trained on millions of open source code commits
- Data flow analysis (taint tracking from source to sink)
- AI-suggested fix snippets inline in IDE and PR comments
- Low false positive rate vs. traditional SAST tools

### Snyk Code Configuration

**Scanning via CLI:**
```bash
# Install Snyk CLI
npm install -g snyk

# Authenticate
snyk auth

# Scan source code
snyk code test --severity-threshold=high

# Output JSON for CI processing
snyk code test --json > snyk-code-results.json
```

**.snyk policy file (exclude/ignore):**
```yaml
# .snyk -- suppress specific findings
version: v1.19.0
ignore:
  SNYK-JS-EXPRESS-471991:  # Suppress specific vuln ID
    - '*':
        reason: Mitigated by WAF rule
        expires: 2025-12-31
patch: {}
```

**VS Code / JetBrains IDE plugin:**
- Install "Snyk Security" extension
- Sign in with Snyk account
- Issues appear inline in editor as you type
- AI-suggested fixes with one-click application
- Real-time scanning as files change

## Snyk Open Source (SCA)

Snyk Open Source scans dependency manifests for vulnerable OSS packages.

**Supported package managers:**
- npm / Yarn (Node.js)
- pip / Poetry / pipenv (Python)
- Maven / Gradle (Java)
- NuGet (.NET)
- Go Modules
- RubyGems / Bundler
- Cargo (Rust)
- Composer (PHP)
- CocoaPods / Swift Package Manager (iOS)

**How Snyk Open Source works:**
1. Reads lockfile (package-lock.json, Pipfile.lock, etc.)
2. Builds full dependency tree (transitive dependencies included)
3. Compares each package version against Snyk Vulnerability Database
4. Reports: severity, CVE ID, vulnerable version, fixed version, CVSS, EPSS

**Auto-fix PRs:**
- Snyk automatically opens a PR on GitHub/GitLab/Bitbucket to upgrade vulnerable dependency
- PR includes: upgraded package.json + lockfile, test status, diff showing changes
- Developer reviews and merges -- no security team involvement needed
- Configure: Project Settings > Automatic fix PRs

**Fix strategies:**
- Snyk recommends the minimum version bump to fix all vulnerabilities
- Sometimes: "No direct fix available" -- only transitive dep has a fix (fork or accept risk)
- Snyk Patch: For cases where no fix version exists, Snyk maintains patches for popular packages

### SCA CLI Usage

```bash
# Test dependencies
snyk test

# Test with specific package manager manifest
snyk test --file=pom.xml

# Monitor project (push to Snyk for ongoing scanning)
snyk monitor

# Test all projects in monorepo
snyk test --all-projects

# Fail CI if high+ severity found
snyk test --severity-threshold=high && echo "Passed" || exit 1

# Generate SBOM (Software Bill of Materials)
snyk sbom --format spdx2.3+json > sbom.json
```

**Snyk Advisor:**
- snyk.io/advisor -- package health scoring
- Scores packages on: popularity, maintenance, security, community
- Use to evaluate new dependencies before adding them

## Snyk Container

Snyk Container scans Docker/OCI images and Dockerfiles for vulnerabilities.

**What it scans:**
- OS packages (apt/yum packages in base image)
- Application dependencies (if Dockerfile copies package manifests)
- Dockerfile best practices (USER root, ADD vs COPY, etc.)
- Base image version (is there a newer, less vulnerable base available?)

**Base image recommendations:**
Snyk uniquely surfaces alternative base images ranked by:
- Number of vulnerabilities fixed by switching
- Severity reduction
- Version compatibility (same distro, newer version vs. different distro)

Example recommendation output:
```
Base image       Vulnerabilities  Severity
node:18-alpine   12               0 Critical, 2 High
node:20-alpine   5                0 Critical, 1 High  ← Recommended
node:lts-slim    8                0 Critical, 1 High
```

### Container Scanning

```bash
# Scan a local image
snyk container test nginx:latest

# Scan with Dockerfile for fix recommendations
snyk container test myapp:latest --file=Dockerfile

# Scan an image in a private registry
snyk container test myregistry.azurecr.io/myapp:1.0.0

# Monitor image for new vulnerabilities
snyk container monitor nginx:latest --project-name=nginx-prod
```

**Registry integration:**
- Docker Hub: Native integration
- AWS ECR: IAM role-based access
- Azure ACR: Service principal
- GCR/GAR: Service account key
- JFrog Artifactory: API key

**Kubernetes admission controller:**
- Snyk Controller for Kubernetes: deny or warn on deployment of images with critical vulns
- Install via Helm: `helm install snyk-monitor snyk-charts/snyk-monitor`
- Policy: Block images with Critical severity above threshold

## Snyk IaC

Snyk IaC detects security misconfigurations in infrastructure-as-code files.

**Supported IaC formats:**
- Terraform (.tf files, Terraform Plan JSON)
- Kubernetes (YAML manifests, Helm charts)
- CloudFormation (YAML/JSON templates)
- AWS CDK (synthesized CloudFormation)
- Azure Resource Manager (ARM templates)
- Azure Bicep
- Serverless Framework

**Categories of issues found:**
- Network: Unrestricted ingress (0.0.0.0/0), missing VPC
- IAM: Overprivileged roles, wildcard permissions, no MFA enforcement
- Encryption: Unencrypted storage (S3, EBS, RDS), no KMS key
- Logging: CloudTrail disabled, no access logging
- Access: Public S3 buckets, public RDS instances
- Kubernetes: Privileged containers, hostPath mounts, missing resource limits

### IaC Scanning

```bash
# Scan Terraform directory
snyk iac test ./terraform/

# Scan Kubernetes manifests
snyk iac test ./k8s/

# Scan CloudFormation templates
snyk iac test ./cloudformation/

# Scan with severity filter
snyk iac test --severity-threshold=high ./

# Scan Terraform Plan (catches dynamic values)
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
snyk iac test --scan=planned-values plan.json
```

**Snyk IaC + (custom policies):**
- Snyk IaC+ supports Open Policy Agent (OPA) Rego-based custom policies
- Write custom rules for organization-specific requirements
- Example: "All S3 buckets must have bucket name tag matching naming convention"

### Snyk IaC in CI/CD

```yaml
# GitHub Actions example
- name: Snyk IaC Test
  uses: snyk/actions/iac@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    file: terraform/
    severity-threshold: high
    # fail-on: all (default) | upgradable | patchable
```

## Snyk AppRisk (ASPM)

Snyk AppRisk is an Application Security Posture Management layer above all Snyk products.

**AppRisk capabilities:**
- **Application inventory:** Discover all applications and repos being scanned (and gaps)
- **Coverage analysis:** Which repos have Snyk Code? Which have SCA? Which have nothing?
- **Risk-based prioritization:** Aggregate risk score per application (combines Code + OSS + Container + IaC findings)
- **Business context integration:** Map applications to business owners, teams, production status
- **IDE adoption tracking:** Are developers using Snyk IDE plugins? Track usage.
- **Policy engine:** Define security gates and pass/fail criteria per application

**Coverage gap identification:**
```
Application: payments-service
  Snyk Code:      ENABLED ✓
  Snyk Open Source: ENABLED ✓
  Snyk Container: NOT CONFIGURED ✗
  Snyk IaC:       NOT CONFIGURED ✗
Risk Score: 7.8/10 (High)
Reason: 3 Critical OSS vulns, container not scanned
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Snyk Security Scan
on: [push, pull_request]

jobs:
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Snyk Open Source (SCA)
      - name: Snyk SCA
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: test
          args: --severity-threshold=high --fail-on=upgradable

      # Snyk Code (SAST)
      - name: Snyk Code
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: code test
          args: --severity-threshold=high

      # Upload to GitHub Security tab (SARIF)
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: snyk.sarif
```

### GitLab CI

```yaml
snyk-scan:
  image: snyk/snyk-cli:docker
  stage: test
  script:
    - snyk auth $SNYK_TOKEN
    - snyk test --severity-threshold=high
    - snyk code test --severity-threshold=high
  allow_failure: false
  artifacts:
    reports:
      sast: gl-sast-report.json
```

### PR Checks (GitHub/GitLab)

Enable Snyk PR checks in Organization Settings:
- Runs Snyk scan on every PR
- Shows vulnerability count delta (new vulns introduced by this PR)
- Can block merge on Critical/High findings (configurable)
- Inline PR comments with fix suggestions

## Snyk Organization and Policy Configuration

### Organization Structure

```
Snyk Group (org-wide)
    |
    +-- Organization: AppTeam-Prod
    |       +-- Projects: all prod repos
    |       +-- Policies: strict (fail on High+)
    |
    +-- Organization: AppTeam-Dev
            +-- Projects: dev/test repos
            +-- Policies: permissive (fail on Critical only)
```

### Severity Policy Configuration

Configure what severity levels fail CI/CD or generate alerts:

```bash
# CLI: Only fail on Critical
snyk test --severity-threshold=critical

# CLI: Fail on High or Critical
snyk test --severity-threshold=high

# .snyk policy: Custom per-project behavior
version: v1.19.0
severity-threshold: high
```

### Integrations

Snyk integrates with:
- **SCM:** GitHub, GitLab, Bitbucket, Azure DevOps, Gerrit
- **ITSM:** Jira (auto-create issues from findings)
- **CI/CD:** GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps Pipelines, TeamCity
- **Container registries:** Docker Hub, ECR, ACR, GCR, JFrog, Harbor
- **IDEs:** VS Code, JetBrains (IntelliJ, PyCharm, WebStorm, etc.), Eclipse, Visual Studio
- **SIEM:** Splunk, Datadog (via webhooks)
- **SOAR:** Jira, ServiceNow (via Snyk API)

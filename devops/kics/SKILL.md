---
name: kics
description: Run Checkmarx KICS for Infrastructure as Code security scanning. Use when analyzing Terraform, CloudFormation, Kubernetes, Ansible, Dockerfile, or other IaC for misconfigurations and security issues.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Checkmarx KICS (Keeping Infrastructure as Code Secure)

## When to Use KICS

**Ideal scenarios:**

- Infrastructure as Code (IaC) security scanning
- Cloud configuration analysis (AWS, Azure, GCP, Oracle)
- Kubernetes manifest security review
- Dockerfile security hardening
- Terraform/OpenTofu security assessment
- Ansible playbook security validation
- CI/CD pipeline IaC security gates
- Compliance checking (CIS, PCI-DSS, NIST, SOC2)

**Complements other tools:**

- Use alongside application security scanners (Semgrep, CodeQL)
- Combine with SARIF Issue Reporter for detailed findings
- Use with cloud posture management tools

## When NOT to Use

Do NOT use this skill for:

- Application source code vulnerability scanning (use Semgrep or CodeQL)
- Secrets detection (use Gitleaks)
- Dependency vulnerability scanning (use OSV-Scanner or Depscan)
- Runtime cloud posture assessment (use CSPM tools)
- Binary or compiled code analysis

## Installation

```bash
# Binary download (Linux)
wget https://github.com/Checkmarx/kics/releases/latest/download/kics_linux_amd64.tar.gz
tar -xzf kics_linux_amd64.tar.gz
sudo mv kics /usr/local/bin/

# Binary download (macOS)
wget https://github.com/Checkmarx/kics/releases/latest/download/kics_darwin_amd64.tar.gz
tar -xzf kics_darwin_amd64.tar.gz
sudo mv kics /usr/local/bin/

# Homebrew
brew install kics

# Docker
docker pull checkmarx/kics:latest

# Verify
kics version
```

## Core Workflow

### 1. Quick Scan

```bash
# Scan current directory
kics scan -p .

# Scan specific path
kics scan -p /path/to/iac

# Scan with minimal output
kics scan -p . --silent

# No color output (for CI)
kics scan -p . --no-color
```

### 2. SARIF Output

```bash
# Generate SARIF report
kics scan -p /path/to/iac \
  --report-formats sarif \
  --output-path results.sarif

# Multiple formats (JSON + SARIF)
kics scan -p /path/to/iac \
  --report-formats json,sarif \
  --output-path .

# Named output
kics scan -p /path/to/iac \
  --report-formats sarif \
  --output-name kics-results

# All formats
kics scan -p /path/to/iac \
  --report-formats all \
  --output-path ./reports
```

### 3. Platform-Specific Scans

```bash
# AWS CloudFormation
kics scan -p ./cloudformation --type CloudFormation

# Terraform
kics scan -p ./terraform --type Terraform

# Kubernetes manifests
kics scan -p ./k8s --type Kubernetes

# Dockerfile
kics scan -p ./docker --type Dockerfile

# Ansible
kics scan -p ./ansible --type Ansible

# Azure Resource Manager
kics scan -p ./arm --type AzureResourceManager

# Google Deployment Manager
kics scan -p ./gdm --type GoogleDeploymentManager

# Helm charts
kics scan -p ./charts --type Helm
```

### 4. Severity Filtering

```bash
# Only high and critical
kics scan -p . --minimal-ui --fail-on high,critical

# Exclude info findings
kics scan -p . --exclude-severities info

# Specific severities in SARIF
kics scan -p . \
  --fail-on high,critical \
  --report-formats sarif \
  --output-path results.sarif
```

## Configuration

### Config File

Create `.kics.yml` or `kics.config`:

```yaml
# Paths to scan
path: ./infrastructure

# Query selection
exclude-queries:
  - 487f4be7-3fd9-4506-a07a-96c39d0b30ad  # Specific query ID

# Severity settings
fail-on:
  - high
  - critical

# Output settings
output-path: ./kics-results
report-formats:
  - sarif
  - json
  - html

# Exclude paths
exclude-paths:
  - "./tests/**"
  - "./examples/**"
  - "**/.terraform/**"

# Exclude results by similarity ID
exclude-results:
  - abc123def456

# Platform filters
type:
  - Terraform
  - Kubernetes
  - Dockerfile

# CI mode
ci: true
no-color: true
minimal-ui: true
```

Use config:

```bash
kics scan --config .kics.yml
```

### Inline Suppressions

```hcl
# Terraform - suppress specific finding
resource "aws_s3_bucket" "example" {
  # kics-scan ignore-line
  bucket = "my-bucket"
  acl    = "public-read"  # Suppressed above
}

# Suppress entire block
# kics-scan ignore-block
resource "aws_security_group" "example" {
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

```yaml
# Kubernetes - suppress finding
apiVersion: v1
kind: Pod
metadata:
  name: example
spec:
  # kics-scan ignore-line
  hostNetwork: true  # Suppressed
  containers:
    - name: app
      image: nginx:latest  # kics-scan ignore-line
```

## CI/CD Integration (GitHub Actions)

```yaml
name: KICS IaC Scan

on:
  push:
    branches: [main]
    paths:
      - '**.tf'
      - '**.yaml'
      - '**.yml'
      - 'Dockerfile*'
  pull_request:
    paths:
      - '**.tf'
      - '**.yaml'
      - '**.yml'
      - 'Dockerfile*'

jobs:
  kics:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run KICS
        uses: checkmarx/kics-github-action@v2.1.1
        with:
          path: .
          output_path: kics-results
          output_formats: 'sarif,json,html'
          fail_on: high,critical
          enable_comments: true  # PR comments
          exclude_paths: 'tests/**,examples/**'

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: kics-results/results.sarif
          category: kics

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: kics-results
          path: kics-results/
```

## Common Use Cases

### 1. Terraform Security Audit

```bash
# Comprehensive Terraform scan
kics scan -p ./terraform \
  --type Terraform \
  --report-formats sarif,html \
  --output-path ./security-audit \
  --fail-on high,critical

# Review HTML report
open ./security-audit/results.html

# Process SARIF with other tools
sarif summary ./security-audit/results.sarif
```

### 2. Kubernetes Hardening

```bash
# Scan all K8s manifests
kics scan -p ./k8s \
  --type Kubernetes \
  --report-formats sarif \
  --output-name k8s-security

# Focus on critical issues
kics scan -p ./k8s \
  --type Kubernetes \
  --fail-on high,critical \
  --exclude-severities low,medium,info
```

### 3. Multi-Cloud Infrastructure

```bash
# Scan mixed IaC
kics scan -p ./infrastructure \
  --type Terraform,CloudFormation,AzureResourceManager \
  --report-formats sarif,json \
  --output-path ./reports
```

### 4. Dockerfile Security

```bash
# Scan all Dockerfiles
kics scan -p . \
  --type Dockerfile \
  --report-formats sarif \
  --output-name dockerfile-scan

# Include docker-compose
kics scan -p . \
  --type Dockerfile,DockerCompose \
  --report-formats sarif
```

## Understanding Output

### SARIF Structure

KICS SARIF v2.1.0 includes:

- **Rules**: Each query/check (1500+ built-in queries)
- **Results**: Specific IaC misconfigurations found
- **Properties**:
  - Severity: HIGH, MEDIUM, LOW, INFO
  - Category: Security, Best Practices, etc.
  - Platform: Terraform, K8s, Dockerfile, etc.
  - CWE mapping
  - Remediation guidance

### Result Categories

| Category | Examples |
|----------|----------|
| **Access Control** | Overly permissive IAM, public resources |
| **Encryption** | Unencrypted storage, weak TLS |
| **Networking** | Open security groups, exposed ports |
| **Secret Management** | Hardcoded credentials, exposed secrets |
| **Resource Configuration** | Missing logging, backup disabled |
| **Best Practices** | Missing tags, resource limits |
| **Insecure Defaults** | Default passwords, debug mode |

## Advanced Features

### Custom Queries

Create custom query in `custom-queries/`:

```rego
# custom-queries/require_tags.rego
package Cx

CxPolicy[result] {
  resource := input.document[i].resource.aws_instance[name]
  not resource.tags

  result := {
    "documentId": input.document[i].id,
    "searchKey": sprintf("aws_instance[%s]", [name]),
    "issueType": "MissingAttribute",
    "keyExpectedValue": "Tags should be defined",
    "keyActualValue": "Tags are not defined"
  }
}
```

Use custom queries:

```bash
kics scan -p ./terraform \
  --queries-path ./custom-queries \
  --report-formats sarif
```

### Query Information

```bash
# List all queries
kics list-platforms

# Show query details
kics show-query <query-id>

# Generate queries documentation
kics generate-documentation
```

### Results Management

```bash
# Generate baseline
kics scan -p . --report-formats json -o baseline.json

# Compare against baseline
kics scan -p . --exclude-results $(cat baseline.json | jq -r '.results[].similarity_id')
```

## Compliance Frameworks

KICS maps findings to:

- **CIS Benchmarks**: AWS, Azure, GCP, Kubernetes
- **PCI-DSS**: Payment card industry standards
- **HIPAA**: Healthcare compliance
- **GDPR**: Data protection requirements
- **SOC 2**: Security controls
- **NIST**: Cybersecurity framework

```bash
# Filter by compliance
kics scan -p . --include-queries "CIS*" --report-formats sarif
```

## Performance Optimization

```bash
# Parallel scanning (default: number of CPUs)
kics scan -p . --parallel 8

# Limit file size
kics scan -p . --file-size-limit 1000  # KB

# Exclude large directories
kics scan -p . --exclude-paths "**/node_modules/**,**/.terraform/**"

# Minimal UI for speed
kics scan -p . --minimal-ui --silent --no-progress
```

## Limitations

- **Runtime issues**: Can't detect runtime misconfigurations
- **Custom modules**: Limited visibility into external Terraform modules
- **Context awareness**: May flag acceptable exceptions
- **False positives**: Generic rules may not fit all use cases
- **Remediation**: Provides guidance but doesn't auto-fix

## Rationalizations to Reject

| Shortcut | Why It's Wrong |
|----------|----------------|
| "KICS found nothing = IaC is secure" | KICS has 1500+ queries but can't cover every misconfiguration |
| "Suppress all LOW/MEDIUM findings" | Lower severity findings can combine to create critical risks |
| "Skip IaC scanning in CI" | IaC defines infrastructure; security issues here affect entire environment |
| "Only scan before deployment" | Early detection in development prevents costly late-stage fixes |
| "Ignore platform-specific queries" | Platform-specific checks catch cloud provider misconfigurations |

## References

- Repository: <https://github.com/Checkmarx/kics>
- Documentation: <https://docs.kics.io/>
- Query Library: <https://docs.kics.io/latest/queries/>
- GitHub Action: <https://github.com/checkmarx/kics-github-action>
- SARIF Documentation: <https://github.com/Checkmarx/kics/blob/master/docs/results.md>
- CIS Benchmarks: <https://www.cisecurity.org/cis-benchmarks>

---
name: iac-scanner
description: Scans Infrastructure as Code for security misconfigurations. Wraps tfsec for Terraform and Checkov for multi-cloud IaC. Use when user asks to "scan Terraform", "IaC security", "infrastructure scan", "tfsec", "checkov", "Terraformセキュリティ", "インフラスキャン".
---

# IaC Scanner

Wrapper for tfsec and Checkov to scan Infrastructure as Code.

## Prerequisites

```bash
# tfsec (Terraform focused)
brew install tfsec
# or
go install github.com/aquasecurity/tfsec/cmd/tfsec@latest

# Checkov (multi-cloud)
pip install checkov
# or
brew install checkov
```

## Usage

```bash
# Scan with auto-detection
npx iac-scanner .

# Force specific scanner
npx iac-scanner . --scanner tfsec
npx iac-scanner . --scanner checkov

# JSON output
npx iac-scanner . --json

# Check available scanners
npx iac-scanner --check

# Scan specific framework
npx iac-scanner . --framework terraform
npx iac-scanner . --framework kubernetes
npx iac-scanner . --framework cloudformation
```

## Supported Frameworks

| Scanner | Frameworks |
|---------|------------|
| tfsec | Terraform |
| Checkov | Terraform, CloudFormation, Kubernetes, ARM, Serverless, Helm |

## Output Format

```json
{
  "tool": "tfsec",
  "scanPath": ".",
  "scanDate": "2024-01-15T10:30:00Z",
  "findings": [
    {
      "id": "aws-s3-enable-bucket-encryption",
      "severity": "high",
      "message": "Bucket does not have encryption enabled",
      "resource": "aws_s3_bucket.data",
      "file": "main.tf",
      "line": 15,
      "resolution": "Enable bucket encryption"
    }
  ],
  "summary": {
    "total": 5,
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 1
  }
}
```

## Common Misconfigurations

| Category | Example |
|----------|---------|
| Encryption | S3 bucket without encryption |
| Access Control | Public S3 bucket, open security groups |
| Logging | Missing CloudTrail, no access logs |
| Network | VPC without flow logs, open CIDR |
| IAM | Overly permissive policies, wildcard actions |
| Secrets | Hardcoded credentials in config |

## Exit Codes

- `0`: No issues found
- `1`: Issues detected
- `2`: Tool not installed or error

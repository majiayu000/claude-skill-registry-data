---
name: secret-scanner
description: Scans git repositories for hardcoded secrets, credentials, and API keys using Gitleaks. Returns findings with severity, location, and remediation steps. Use when user asks to "scan for secrets", "detect credentials", "find API keys", "check for leaks", "シークレット検出", "認証情報スキャン".
---

# Secret Scanner

Wrapper for Gitleaks to detect hardcoded secrets in git repositories.

## Prerequisites

Gitleaks must be installed:
```bash
# macOS
brew install gitleaks

# Go
go install github.com/gitleaks/gitleaks/v8@latest

# Docker
docker pull zricethezav/gitleaks
```

## Usage

```bash
# Scan current directory
npx secret-scanner .

# Scan with JSON output
npx secret-scanner . --json

# Scan specific path
npx secret-scanner /path/to/repo

# Check if gitleaks is installed
npx secret-scanner --check
```

## Output Format

```json
{
  "tool": "gitleaks",
  "scanPath": ".",
  "findings": [
    {
      "id": "aws-access-key-id",
      "severity": "critical",
      "description": "AWS Access Key ID detected",
      "file": "config.js",
      "line": 15,
      "secret": "AKIA***REDACTED***",
      "commit": "abc1234",
      "author": "developer@example.com",
      "date": "2024-01-15T10:30:00Z"
    }
  ],
  "summary": {
    "total": 1,
    "critical": 1,
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
```

## Exit Codes

- `0`: No secrets found
- `1`: Secrets detected
- `2`: Tool not installed or error

## Severity Mapping

| Gitleaks Rule | Severity |
|---------------|----------|
| aws-access-key-id | critical |
| private-key | critical |
| password | high |
| api-key | high |
| token | medium |
| generic-credential | low |

## CWE Coverage

- CWE-798: Use of Hard-coded Credentials
- CWE-259: Use of Hard-coded Password
- CWE-321: Use of Hard-coded Cryptographic Key
- CWE-312: Cleartext Storage of Sensitive Information

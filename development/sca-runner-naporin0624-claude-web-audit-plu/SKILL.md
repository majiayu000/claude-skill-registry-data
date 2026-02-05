---
name: sca-runner
description: Runs Software Composition Analysis (SCA) to detect vulnerable dependencies. Wraps npm audit and Trivy fs. Use when user asks to "scan dependencies", "check npm vulnerabilities", "SCA scan", "dependency audit", "依存関係スキャン", "脆弱性チェック".
---

# SCA Runner

Wrapper for npm audit and Trivy to perform Software Composition Analysis.

## Prerequisites

At least one of these tools must be installed:

```bash
# npm audit (built into npm)
npm --version

# Trivy (recommended for multi-language support)
brew install trivy
# or
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

## Usage

```bash
# Scan with auto-detection (prefers Trivy if available)
npx sca-runner .

# Force specific scanner
npx sca-runner . --scanner npm
npx sca-runner . --scanner trivy

# JSON output
npx sca-runner . --json

# Check available scanners
npx sca-runner --check

# Scan specific package file
npx sca-runner ./package-lock.json --scanner npm
```

## Supported Package Managers

| Scanner | Languages/Files |
|---------|-----------------|
| npm audit | Node.js (package-lock.json) |
| Trivy | Node.js, Python, Go, Ruby, Rust, Java, .NET |

## Output Format

```json
{
  "tool": "trivy",
  "scanPath": ".",
  "scanDate": "2024-01-15T10:30:00Z",
  "findings": [
    {
      "id": "CVE-2024-1234",
      "severity": "critical",
      "package": "lodash",
      "installedVersion": "4.17.20",
      "fixedVersion": "4.17.21",
      "title": "Prototype Pollution",
      "description": "...",
      "cvss": 9.8,
      "cwes": ["CWE-1321"],
      "references": ["https://nvd.nist.gov/..."]
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

## Exit Codes

- `0`: No vulnerabilities found
- `1`: Vulnerabilities detected
- `2`: Tool not installed or error

## Common CVEs Detected

- Prototype Pollution (CWE-1321)
- Regular Expression DoS (CWE-1333)
- Path Traversal (CWE-22)
- Code Injection (CWE-94)
- Denial of Service (CWE-400)

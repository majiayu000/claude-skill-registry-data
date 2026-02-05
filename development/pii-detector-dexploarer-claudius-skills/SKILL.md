---
name: pii-detector
description: Detects Personally Identifiable Information (PII) in code, logs, databases, and files for GDPR/CCPA compliance. Use when user asks to "detect PII", "find sensitive data", "scan for personal information", "check GDPR compliance", or "find SSN/credit cards".
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# PII Detector

Scans code, logs, databases, and configuration files for Personally Identifiable Information (PII) to ensure GDPR, CCPA, and privacy compliance.

## When to Use

- "Scan for PII in my codebase"
- "Find sensitive data"
- "Check for exposed personal information"
- "Detect SSN, credit cards, emails"
- "GDPR compliance check"
- "Find PII in logs"

## Instructions

### 1. Detect Project Type

```bash
# Check project structure
ls -la

# Detect language
[ -f "package.json" ] && echo "JavaScript/TypeScript"
[ -f "requirements.txt" ] && echo "Python"
[ -f "pom.xml" ] && echo "Java"
[ -f "Gemfile" ] && echo "Ruby"

# Check for logs
find . -name "*.log" -type f | head -5
```

### 2. Define PII Patterns

**Common PII Types:**

1. **Social Security Numbers (SSN)**
   - Pattern: `\b\d{3}-\d{2}-\d{4}\b`
   - Example: 123-45-6789

2. **Credit Card Numbers**
   - Visa: `\b4\d{3}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b`
   - MasterCard: `\b5[1-5]\d{2}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b`
   - Amex: `\b3[47]\d{2}[\s-]?\d{6}[\s-]?\d{5}\b`
   - Discover: `\b6011[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b`

3. **Email Addresses**
   - Pattern: `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`

4. **Phone Numbers**
   - US: `\b\d{3}[-.]?\d{3}[-.]?\d{4}\b`
   - International: `\+\d{1,3}[\s-]?\d{1,14}`

5. **IP Addresses**
   - IPv4: `\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`
   - IPv6: `([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}`

6. **Dates of Birth**
   - Pattern: `\b\d{2}/\d{2}/\d{4}\b` or `\b\d{4}-\d{2}-\d{2}\b`

7. **Passport Numbers**
   - US: `\b[A-Z]{1,2}\d{6,9}\b`

8. **Driver's License**
   - Varies by state/country

9. **Bank Account Numbers**
   - Pattern: `\b\d{8,17}\b`

10. **API Keys / Tokens**
    - AWS: `AKIA[0-9A-Z]{16}`
    - Slack: `xox[baprs]-[0-9a-zA-Z-]{10,}`
    - GitHub: `ghp_[0-9a-zA-Z]{36}`

### 3. Scan Codebase

**Using grep:**
```bash
# Scan for SSN
grep -rn '\b\d{3}-\d{2}-\d{4}\b' . --include="*.js" --include="*.py" --include="*.java"

# Scan for credit cards
grep -rn '\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b' . --exclude-dir=node_modules

# Scan for emails
grep -rn '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' . --include="*.log"

# Scan for phone numbers
grep -rn '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b' .

# Scan for API keys
grep -rn 'AKIA[0-9A-Z]{16}' . --include="*.env*" --include="*.config*"
```

**Exclude common false positives:**
```bash
# Exclude test files, build directories
grep -rn <pattern> . \
  --exclude-dir=node_modules \
  --exclude-dir=.git \
  --exclude-dir=dist \
  --exclude-dir=build \
  --exclude-dir=vendor \
  --exclude-dir=__pycache__ \
  --exclude="*.test.js" \
  --exclude="*.spec.ts" \
  --exclude="*.min.js"
```

### 4. Create PII Detection Script

**Python Script:**
```python
#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class PIIDetector:
    def __init__(self):
        self.patterns = {
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'Credit Card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'Phone (US)': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'IPv4': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'AWS Key': r'AKIA[0-9A-Z]{16}',
            'GitHub Token': r'ghp_[0-9a-zA-Z]{36}',
            'Slack Token': r'xox[baprs]-[0-9a-zA-Z-]{10,}',
            'Date of Birth': r'\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/(?:19|20)\d{2}\b',
        }

        self.exclude_dirs = {
            'node_modules', '.git', 'dist', 'build', 'vendor',
            '__pycache__', '.next', 'out', 'coverage', '.venv'
        }

        self.exclude_extensions = {
            '.min.js', '.map', '.lock', '.jpg', '.png', '.gif',
            '.pdf', '.zip', '.tar', '.gz'
        }

    def should_scan_file(self, filepath: Path) -> bool:
        """Check if file should be scanned."""
        # Check excluded directories
        if any(excluded in filepath.parts for excluded in self.exclude_dirs):
            return False

        # Check excluded extensions
        if filepath.suffix in self.exclude_extensions:
            return False

        # Check file size (skip files > 10MB)
        try:
            if filepath.stat().st_size > 10 * 1024 * 1024:
                return False
        except OSError:
            return False

        return True

    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a single file for PII."""
        findings = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for pii_type, pattern in self.patterns.items():
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            # Check for common false positives
                            if self.is_false_positive(pii_type, match.group(), line):
                                continue

                            findings.append({
                                'file': str(filepath),
                                'line': line_num,
                                'type': pii_type,
                                'value': self.mask_pii(match.group()),
                                'context': line.strip()[:100]
                            })
        except Exception as e:
            print(f"Error scanning {filepath}: {e}", file=sys.stderr)

        return findings

    def is_false_positive(self, pii_type: str, value: str, context: str) -> bool:
        """Check for common false positives."""
        # Common test data
        test_patterns = [
            '000-00-0000',
            '111-11-1111',
            '123-45-6789',
            '4111111111111111',  # Test credit card
            'test@example.com',
            'user@localhost',
            '127.0.0.1',
            '0.0.0.0',
            '192.168.',
        ]

        for pattern in test_patterns:
            if pattern in value:
                return True

        # Check if in comment
        if any(comment in context for comment in ['//', '#', '/*', '*', '<!--']):
            if 'example' in context.lower() or 'test' in context.lower():
                return True

        return False

    def mask_pii(self, value: str) -> str:
        """Mask PII value for reporting."""
        if len(value) <= 4:
            return '*' * len(value)
        return value[:2] + '*' * (len(value) - 4) + value[-2:]

    def scan_directory(self, directory: Path) -> List[Dict]:
        """Recursively scan directory for PII."""
        all_findings = []

        for filepath in directory.rglob('*'):
            if filepath.is_file() and self.should_scan_file(filepath):
                findings = self.scan_file(filepath)
                all_findings.extend(findings)

        return all_findings

    def generate_report(self, findings: List[Dict]) -> str:
        """Generate human-readable report."""
        if not findings:
            return "✅ No PII detected!"

        report = f"⚠️  Found {len(findings)} potential PII instances:\n\n"

        # Group by type
        by_type = {}
        for finding in findings:
            pii_type = finding['type']
            if pii_type not in by_type:
                by_type[pii_type] = []
            by_type[pii_type].append(finding)

        for pii_type, items in sorted(by_type.items()):
            report += f"## {pii_type} ({len(items)} found)\n\n"
            for item in items[:10]:  # Limit to 10 per type
                report += f"- {item['file']}:{item['line']}\n"
                report += f"  Value: {item['value']}\n"
                report += f"  Context: {item['context']}\n\n"

            if len(items) > 10:
                report += f"  ... and {len(items) - 10} more\n\n"

        return report

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scan for PII in codebase')
    parser.add_argument('path', nargs='?', default='.', help='Path to scan')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--exclude', nargs='+', help='Additional directories to exclude')

    args = parser.parse_args()

    detector = PIIDetector()

    if args.exclude:
        detector.exclude_dirs.update(args.exclude)

    scan_path = Path(args.path)
    findings = detector.scan_directory(scan_path)

    if args.json:
        import json
        print(json.dumps(findings, indent=2))
    else:
        print(detector.generate_report(findings))

    # Exit with error code if PII found
    sys.exit(1 if findings else 0)

if __name__ == '__main__':
    main()
```

**Save as `pii_detector.py` and run:**
```bash
python pii_detector.py .
```

**JavaScript/TypeScript Version:**
```javascript
// pii-detector.js
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const PII_PATTERNS = {
  'SSN': /\b\d{3}-\d{2}-\d{4}\b/g,
  'Credit Card': /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
  'Email': /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/gi,
  'Phone (US)': /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
  'IPv4': /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g,
  'AWS Key': /AKIA[0-9A-Z]{16}/g,
  'GitHub Token': /ghp_[0-9a-zA-Z]{36}/g,
};

const EXCLUDE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'coverage',
  '.next', 'out', 'vendor', '__pycache__'
]);

const EXCLUDE_EXTS = new Set([
  '.min.js', '.map', '.lock', '.jpg', '.png', '.gif', '.pdf'
]);

function shouldScanFile(filePath) {
  const parts = filePath.split(path.sep);
  if (parts.some(part => EXCLUDE_DIRS.has(part))) {
    return false;
  }

  const ext = path.extname(filePath);
  if (EXCLUDE_EXTS.has(ext)) {
    return false;
  }

  return true;
}

function maskPII(value) {
  if (value.length <= 4) return '*'.repeat(value.length);
  return value.slice(0, 2) + '*'.repeat(value.length - 4) + value.slice(-2);
}

async function scanFile(filePath) {
  const findings = [];

  const fileStream = fs.createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let lineNum = 0;
  for await (const line of rl) {
    lineNum++;

    for (const [type, pattern] of Object.entries(PII_PATTERNS)) {
      const matches = line.matchAll(pattern);

      for (const match of matches) {
        findings.push({
          file: filePath,
          line: lineNum,
          type,
          value: maskPII(match[0]),
          context: line.trim().slice(0, 100)
        });
      }
    }
  }

  return findings;
}

async function scanDirectory(dir) {
  const findings = [];

  async function walk(directory) {
    const files = await fs.promises.readdir(directory);

    for (const file of files) {
      const filePath = path.join(directory, file);
      const stat = await fs.promises.stat(filePath);

      if (stat.isDirectory()) {
        if (!EXCLUDE_DIRS.has(file)) {
          await walk(filePath);
        }
      } else if (shouldScanFile(filePath)) {
        const fileFindings = await scanFile(filePath);
        findings.push(...fileFindings);
      }
    }
  }

  await walk(dir);
  return findings;
}

function generateReport(findings) {
  if (findings.length === 0) {
    return '✅ No PII detected!';
  }

  let report = `⚠️  Found ${findings.length} potential PII instances:\n\n`;

  const byType = {};
  for (const finding of findings) {
    if (!byType[finding.type]) {
      byType[finding.type] = [];
    }
    byType[finding.type].push(finding);
  }

  for (const [type, items] of Object.entries(byType)) {
    report += `## ${type} (${items.length} found)\n\n`;

    for (const item of items.slice(0, 10)) {
      report += `- ${item.file}:${item.line}\n`;
      report += `  Value: ${item.value}\n`;
      report += `  Context: ${item.context}\n\n`;
    }

    if (items.length > 10) {
      report += `  ... and ${items.length - 10} more\n\n`;
    }
  }

  return report;
}

async function main() {
  const scanPath = process.argv[2] || '.';
  const findings = await scanDirectory(scanPath);

  console.log(generateReport(findings));

  process.exit(findings.length > 0 ? 1 : 0);
}

main().catch(console.error);
```

### 5. Database Scanning

**SQL Query to Find PII:**
```sql
-- PostgreSQL example
-- Scan for potential email columns
SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE column_name ILIKE '%email%'
   OR column_name ILIKE '%ssn%'
   OR column_name ILIKE '%phone%'
   OR column_name ILIKE '%address%'
ORDER BY table_name, column_name;

-- Sample data to check patterns
SELECT
    table_name,
    column_name,
    COUNT(*) as sample_count
FROM information_schema.columns
WHERE data_type IN ('character varying', 'text', 'char')
GROUP BY table_name, column_name;
```

### 6. Log File Scanning

```bash
# Scan application logs
find . -name "*.log" -type f -exec grep -l '\b\d{3}-\d{2}-\d{4}\b' {} \;

# Scan with context
grep -C 3 'SSN\|social security\|credit card' *.log

# Check for leaked credentials
grep -r 'password.*=\|api_key.*=\|secret.*=' . --include="*.log"
```

### 7. CI/CD Integration

**GitHub Actions:**
```yaml
name: PII Detection

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  pii-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run PII Detector
        run: |
          python pii_detector.py . --json > pii-report.json

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: pii-report
          path: pii-report.json

      - name: Fail if PII found
        run: |
          if [ $(cat pii-report.json | jq 'length') -gt 0 ]; then
            echo "❌ PII detected! See report for details."
            exit 1
          fi
```

### 8. Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Scanning for PII..."

python pii_detector.py $(git diff --cached --name-only)

if [ $? -ne 0 ]; then
    echo "❌ PII detected in staged files!"
    echo "Please remove sensitive data before committing."
    exit 1
fi

echo "✅ No PII detected"
exit 0
```

### 9. Data Anonymization

Once PII is found, suggest anonymization:

```python
# anonymize.py
import hashlib
import re

def anonymize_email(email):
    """Replace email with hashed version."""
    local, domain = email.split('@')
    hashed = hashlib.sha256(local.encode()).hexdigest()[:8]
    return f"{hashed}@{domain}"

def anonymize_ssn(ssn):
    """Mask SSN keeping only last 4 digits."""
    return f"***-**-{ssn[-4:]}"

def anonymize_phone(phone):
    """Mask phone keeping only last 4 digits."""
    digits = re.sub(r'\D', '', phone)
    return f"***-***-{digits[-4:]}"

def anonymize_credit_card(cc):
    """Mask credit card keeping only last 4 digits."""
    return f"****-****-****-{cc[-4:]}"

# Example usage
text = "Contact John at john@email.com or call 555-123-4567"
text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
              lambda m: anonymize_email(m.group()), text)
print(text)
# Output: "Contact John at a1b2c3d4@email.com or call 555-123-4567"
```

### 10. Compliance Report

Generate compliance report:

```markdown
# PII Detection Report

**Date**: 2025-11-01
**Scope**: Entire codebase
**Files Scanned**: 1,247
**Total Findings**: 23

## Summary by Type

| PII Type | Count | Risk Level |
|----------|-------|------------|
| Email    | 12    | Medium     |
| Phone    | 8     | Medium     |
| SSN      | 2     | High       |
| API Keys | 1     | Critical   |

## Critical Findings

### 1. AWS API Key in config file
- **File**: config/production.env
- **Line**: 15
- **Recommendation**: Move to environment variables or secret manager

### 2. SSN in test data
- **File**: tests/fixtures/users.json
- **Line**: 42
- **Recommendation**: Use fake data generator

## Remediation Steps

1. ✅ Remove hardcoded credentials from config files
2. ✅ Replace real PII in test data with fake data
3. ✅ Add pre-commit hooks to prevent future leaks
4. ✅ Rotate exposed API keys
5. ✅ Update .gitignore to exclude sensitive files

## Compliance Status

- [ ] GDPR Article 32 (Security of processing)
- [ ] CCPA Section 1798.150 (Data protection)
- [ ] HIPAA Security Rule (if applicable)
```

### Best Practices

**DO:**
- Scan regularly (CI/CD, pre-commit)
- Use environment variables for secrets
- Anonymize data in non-production
- Implement data retention policies
- Train team on PII handling
- Use tools like git-secrets, truffleHog

**DON'T:**
- Store PII in version control
- Log sensitive data
- Hardcode credentials
- Use real PII in tests
- Keep PII longer than needed
- Ignore scan results

## Checklist

- [ ] PII patterns defined
- [ ] Scanner script created
- [ ] Codebase scanned
- [ ] Database schema reviewed
- [ ] Logs checked
- [ ] CI/CD integration added
- [ ] Pre-commit hook installed
- [ ] Findings documented
- [ ] Remediation plan created
- [ ] Team trained on PII handling

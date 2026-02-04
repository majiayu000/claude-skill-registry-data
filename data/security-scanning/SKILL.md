---
name: security-scanning
description: SAST rules, vulnerability patterns, secret detection, and security scanning configuration
---

# Security Scanning Skill
# Project Autopilot - Security analysis patterns and rules
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill for security scanning rules, vulnerability patterns, and remediation guidance.

---

## OWASP Top 10 Patterns

### A01: Broken Access Control

#### Missing Authentication

```javascript
// VULNERABLE: No auth check
app.get('/api/admin/users', (req, res) => {
  return db.getAllUsers();
});

// SECURE: Auth middleware
app.get('/api/admin/users', requireAuth, requireAdmin, (req, res) => {
  return db.getAllUsers();
});
```

#### Insecure Direct Object Reference (IDOR)

```javascript
// VULNERABLE: No ownership check
app.get('/api/documents/:id', async (req, res) => {
  return db.getDocument(req.params.id);
});

// SECURE: Verify ownership
app.get('/api/documents/:id', async (req, res) => {
  const doc = await db.getDocument(req.params.id);
  if (doc.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  return doc;
});
```

### A02: Cryptographic Failures

#### Weak Hashing

```python
# VULNERABLE: MD5 for passwords
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# SECURE: bcrypt with salt
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
```

#### Hardcoded Secrets

```javascript
// VULNERABLE: Hardcoded key
const JWT_SECRET = "super_secret_key_123";

// SECURE: Environment variable
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) throw new Error("JWT_SECRET required");
```

### A03: Injection

#### SQL Injection

```javascript
// VULNERABLE: String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// SECURE: Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);
```

#### Command Injection

```python
# VULNERABLE: Shell command with user input
import os
os.system(f"convert {user_filename} output.png")

# SECURE: Use subprocess with list
import subprocess
subprocess.run(["convert", user_filename, "output.png"], shell=False)
```

### A07: XSS (Cross-Site Scripting)

#### DOM XSS

```javascript
// VULNERABLE: innerHTML with user data
element.innerHTML = userComment;

// SECURE: textContent (auto-escapes)
element.textContent = userComment;

// SECURE: DOMPurify for rich content
element.innerHTML = DOMPurify.sanitize(userComment);
```

#### React XSS

```jsx
// VULNERABLE: dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// SECURE: DOMPurify
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />

// BEST: Avoid if possible
<div>{userContent}</div>
```

---

## Secret Detection Patterns

### API Keys

```regex
# AWS Access Key
AKIA[0-9A-Z]{16}

# AWS Secret Key (context needed)
[0-9a-zA-Z/+]{40}

# GitHub Token (PAT)
ghp_[0-9a-zA-Z]{36}

# GitLab Token
glpat-[0-9a-zA-Z\-_]{20}

# Google API Key
AIza[0-9A-Za-z\-_]{35}

# Stripe Secret Key
sk_live_[0-9a-zA-Z]{24}

# Twilio Auth Token
[0-9a-fA-F]{32}
```

### Private Keys

```regex
# RSA Private Key
-----BEGIN RSA PRIVATE KEY-----

# Generic Private Key
-----BEGIN PRIVATE KEY-----

# EC Private Key
-----BEGIN EC PRIVATE KEY-----

# PGP Private Key
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

### Credentials

```regex
# Generic Password Assignment
(?i)(password|passwd|pwd|secret)[\s]*[:=][\s]*['"][^'"]{8,}['"]

# Database URLs with credentials
(postgres|mysql|mongodb|redis):\/\/[^:]+:[^@]+@

# Basic Auth in URLs
https?:\/\/[^:]+:[^@]+@
```

### Tokens

```regex
# JWT Token
eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_.+/]*

# Bearer Token
Bearer [A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+

# OAuth Token
[0-9a-f]{40}
```

---

## Language-Specific Patterns

### JavaScript/TypeScript

```yaml
patterns:
  - name: eval_usage
    regex: 'eval\s*\('
    severity: high
    message: "eval() can execute arbitrary code"
    remediation: "Use JSON.parse() or Function() with caution"

  - name: prototype_pollution
    regex: '(Object\.assign|\.\.\.)\s*\([^)]*req\.(body|query|params)'
    severity: high
    message: "Potential prototype pollution"
    remediation: "Validate and sanitize input"

  - name: unsafe_regex
    regex: '/\.\*.*\.\*/'
    severity: medium
    message: "Potentially catastrophic backtracking"
    remediation: "Use atomic groups or limit input length"

  - name: insecure_random
    regex: 'Math\.random\(\)'
    severity: medium
    context: "crypto|secret|token|key|password"
    message: "Math.random() is not cryptographically secure"
    remediation: "Use crypto.randomBytes() or crypto.getRandomValues()"
```

### Python

```yaml
patterns:
  - name: pickle_unsafe
    regex: 'pickle\.loads?\('
    severity: high
    message: "pickle can execute arbitrary code"
    remediation: "Use JSON or implement safe deserialization"

  - name: yaml_unsafe
    regex: 'yaml\.load\([^)]*\)'
    severity: high
    message: "yaml.load() is unsafe"
    remediation: "Use yaml.safe_load()"

  - name: shell_true
    regex: 'subprocess\.\w+\([^)]*shell\s*=\s*True'
    severity: high
    message: "shell=True enables command injection"
    remediation: "Use shell=False with argument list"

  - name: sql_format
    regex: '(execute|query)\([^)]*%\s*\('
    severity: critical
    message: "SQL string formatting allows injection"
    remediation: "Use parameterized queries"
```

### Go

```yaml
patterns:
  - name: sql_concat
    regex: 'db\.(Query|Exec)\([^)]*\+\s*'
    severity: critical
    message: "SQL string concatenation"
    remediation: "Use prepared statements"

  - name: weak_rand
    regex: 'math/rand'
    context: "crypto|secret|token|key"
    severity: medium
    message: "math/rand is not cryptographically secure"
    remediation: "Use crypto/rand"

  - name: tls_skip_verify
    regex: 'InsecureSkipVerify:\s*true'
    severity: high
    message: "TLS verification disabled"
    remediation: "Enable TLS verification in production"
```

---

## Severity Classification

### Critical (Must Fix)

- Secrets in code
- SQL injection
- Command injection
- Unvalidated redirects to user input
- Authentication bypass

### High (Fix Before Merge)

- XSS vulnerabilities
- IDOR without auth
- Weak cryptography
- SSRF potential
- Deserialization issues

### Medium (Fix Within Sprint)

- Missing rate limiting
- Verbose error messages
- Insecure random numbers
- Missing security headers
- Incomplete input validation

### Low (Track)

- Outdated dependencies (no known vulns)
- Missing best practices
- Informational findings

---

## Dependency Scanning

### JavaScript (npm)

```bash
# Audit command
npm audit --json

# Fix automatically
npm audit fix

# Force fix (may break)
npm audit fix --force
```

### Python (pip)

```bash
# Using pip-audit
pip-audit --format json

# Using safety
safety check --json
```

### Go

```bash
# Using govulncheck
govulncheck -json ./...
```

### Multi-language (Snyk)

```bash
# Install
npm install -g snyk

# Test
snyk test --json
```

---

## Configuration

### Ignore File (.autopilot/security.json)

```json
{
  "ignore": {
    "files": [
      "**/*.test.ts",
      "**/*.spec.ts",
      "**/fixtures/**",
      "**/mocks/**"
    ],
    "patterns": [
      "test-api-key",
      "example.com"
    ],
    "rules": [
      "insecure-random-in-tests"
    ]
  },
  "thresholds": {
    "critical": 0,
    "high": 0,
    "medium": 10,
    "low": -1
  },
  "autoFix": {
    "dependencies": true,
    "codePatterns": false
  }
}
```

### Inline Ignores

```javascript
// autopilot-ignore: insecure-random (test data only)
const testId = Math.random().toString(36);

// autopilot-ignore-next-line: hardcoded-secret
const TEST_KEY = "test-key-not-real";
```

---

## Integration with Quality Gates

### Phase Exit Gate

```yaml
# In quality-gates SKILL.md
security_gate:
  enabled: true
  block_on:
    - critical
    - high
  warn_on:
    - medium
  report_file: ".autopilot/security-report.md"
```

### Validation Command

```bash
# Run security scan
npm audit --audit-level=moderate

# Python
bandit -r src/ -f json -o security-report.json

# Generic
/autopilot:scan --security
```

---

## Remediation Templates

### SQL Injection Fix

```markdown
## Remediation: SQL Injection

**Finding:** String concatenation in SQL query
**File:** `src/db/users.ts:45`
**Severity:** Critical

### Vulnerable Code
```typescript
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

### Fixed Code
```typescript
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);
```

### Verification
- [ ] All SQL queries use parameterized statements
- [ ] No string concatenation with user input
- [ ] Input validation added
```

### XSS Fix

```markdown
## Remediation: Cross-Site Scripting

**Finding:** innerHTML with user data
**File:** `src/components/Comment.tsx:23`
**Severity:** High

### Vulnerable Code
```jsx
<div dangerouslySetInnerHTML={{ __html: comment.body }} />
```

### Fixed Code
```jsx
import DOMPurify from 'dompurify';

<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(comment.body) }} />
```

### Verification
- [ ] DOMPurify installed
- [ ] All user content sanitized
- [ ] No direct innerHTML assignments
```

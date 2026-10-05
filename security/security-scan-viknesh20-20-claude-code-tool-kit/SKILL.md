---
name: security-scan
description: "Scans the codebase for security vulnerabilities including injection flaws, authentication issues, hardcoded secrets, and insecure configurations. Run before any PR touching auth, user input, or external APIs."
argument-hint: "[file, directory, or 'all']"
allowed-tools: Read, Grep, Glob, Bash(git grep*), Bash(grep*)
---

# Security Vulnerability Scan

## Automated Secret Detection
!`git grep -rn "api_key\|apikey\|api-key\|secret\|password\|passwd\|token\|bearer\|private_key\|access_key\|client_secret\|auth_token" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.rs" --include="*.java" --include="*.rb" --include="*.cs" --include="*.env*" --include="*.yml" --include="*.yaml" --include="*.json" --include="*.toml" --include="*.cfg" --include="*.ini" --include="*.conf" 2>/dev/null | grep -v node_modules | grep -v .git | grep -v vendor | grep -v "\.lock" | grep -v "test" | grep -vi "example\|placeholder\|your_\|TODO\|FIXME\|change_me" | head -30`

## Environment Files Check
!`find . -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null`
!`cat .gitignore 2>/dev/null | grep -i "env\|secret\|key\|credential" || echo "WARNING: .gitignore may not exclude secret files"`

---

## Vulnerability Checklist

Scan the codebase systematically for each vulnerability class. For every finding:
- **Severity**: Critical / High / Medium / Low
- **File path and line number**
- **Vulnerability type** (CWE ID if known)
- **Description** of the risk
- **Remediation** steps with code

### 1. Injection Flaws
- **SQL Injection**: String concatenation in queries instead of parameterized/prepared statements
- **NoSQL Injection**: Unsanitized user input in MongoDB/DynamoDB queries
- **Command Injection**: User input passed to `exec`, `system`, `os.popen`, `subprocess` without sanitization
- **LDAP Injection**: Unsanitized input in LDAP queries
- **Path Traversal**: User input in file paths without normalization (`../../../etc/passwd`)
- **Template Injection**: User input rendered in templates without escaping (SSTI)

### 2. Cross-Site Scripting (XSS)
- Unescaped user input rendered in HTML
- `dangerouslySetInnerHTML` / `v-html` / `|safe` with user content
- Reflected XSS via URL parameters
- Stored XSS via database content rendered without sanitization
- DOM-based XSS via `document.write`, `innerHTML`, `eval`

### 3. Authentication & Authorization
- Missing authentication on sensitive endpoints
- Broken access control (IDOR — accessing other users' resources by ID)
- Missing rate limiting on login/auth endpoints
- JWT tokens without expiry or with weak signing algorithms (HS256 with weak secret)
- Session tokens in URLs or local storage
- Missing CSRF protection on state-changing operations

### 4. Hardcoded Secrets
- API keys, tokens, passwords in source code
- Private keys or certificates in the repository
- Database connection strings with embedded credentials
- Secret values in configuration files that should use env vars

### 5. Insecure Configuration
- Debug mode enabled in production configs
- Verbose error messages exposing stack traces or internals
- Open CORS policies (`Access-Control-Allow-Origin: *`)
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Default credentials not changed
- Unnecessary ports or services exposed

### 6. Data Exposure
- Sensitive data in logs (passwords, tokens, PII)
- PII returned in API responses without need
- Missing encryption for data at rest or in transit
- Overly permissive file/directory permissions
- Backup files or source maps exposed in production

### 7. Dependency Vulnerabilities
- Check for known vulnerable dependencies using:
  - `npm audit` / `yarn audit` (Node.js)
  - `pip audit` / `safety check` (Python)
  - `go vuln check` (Go)
  - `cargo audit` (Rust)
  - `dotnet list package --vulnerable` (.NET)

---

## Output Format

### Findings by Severity

#### Critical (exploit possible, immediate fix required)
<!-- List findings -->

#### High (significant risk, fix before deploy)
<!-- List findings -->

#### Medium (should be addressed in next sprint)
<!-- List findings -->

#### Low (hardening recommendations)
<!-- List findings -->

### Security Score
Rate the overall security posture from **0 to 10** (10 = excellent, 0 = critical vulnerabilities present).

### Risk Assessment
Provide a paragraph summarizing the overall security state, the most concerning patterns, and the recommended order of remediation.

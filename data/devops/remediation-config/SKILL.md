---
name: remediation-config
description: Security fix patterns for configuration and deployment vulnerabilities (path traversal, debug mode, security headers). Provides language-specific secure implementations.
---

# Remediation: Configuration & Deployment Vulnerabilities

Actionable fix patterns for configuration-related security vulnerabilities.

## When to Use This Skill

- **Fixing path traversal** - After finding directory escape vulnerabilities
- **Fixing debug mode** - After finding debug enabled in production
- **Fixing security headers** - After finding missing headers
- **Code review feedback** - Provide remediation guidance with examples

## When NOT to Use This Skill

- **Detecting vulnerabilities** - Use vulnerability-patterns skill
- **Fixing injection issues** - Use remediation-injection skill
- **Fixing crypto issues** - Use remediation-crypto skill
- **Fixing auth issues** - Use remediation-auth skill

---

## Path Traversal (CWE-22)

### Problem
User-controlled file paths can escape intended directories to access sensitive files.

### Python

**Don't**:
```python
# VULNERABLE: Direct path concatenation
def get_file(filename):
    return open(f'/app/uploads/{filename}').read()

# VULNERABLE: No validation
path = os.path.join(base_dir, user_filename)
```

**Do**:
```python
# SECURE: Validate path is within allowed directory
from pathlib import Path

UPLOAD_DIR = Path('/app/uploads').resolve()

def safe_file_access(filename: str) -> Path:
    # Resolve to absolute path
    requested = (UPLOAD_DIR / filename).resolve()

    # Verify it's within allowed directory
    if not requested.is_relative_to(UPLOAD_DIR):
        raise ValueError("Path traversal attempt detected")

    return requested

# SECURE: Alternative with os.path
def safe_file_access_os(filename):
    base = os.path.abspath(UPLOAD_DIR)
    requested = os.path.abspath(os.path.join(UPLOAD_DIR, filename))

    if not requested.startswith(base + os.sep):
        raise ValueError("Path traversal attempt detected")

    return requested
```

### JavaScript/Node.js

**Don't**:
```javascript
// VULNERABLE: Direct path join
const filepath = path.join(uploadDir, userFilename);
fs.readFile(filepath);
```

**Do**:
```javascript
// SECURE: Validate path is within directory
const path = require('path');
const fs = require('fs');

const UPLOAD_DIR = path.resolve('/app/uploads');

function safeFilePath(filename) {
  const requested = path.resolve(UPLOAD_DIR, filename);

  if (!requested.startsWith(UPLOAD_DIR + path.sep)) {
    throw new Error('Path traversal attempt detected');
  }

  return requested;
}
```

### Go

**Don't**:
```go
// VULNERABLE: Direct path join
filePath := filepath.Join(uploadDir, userFilename)
data, err := ioutil.ReadFile(filePath)
```

**Do**:
```go
// SECURE: Validate path is within directory
func safeFilePath(base, filename string) (string, error) {
    absBase, _ := filepath.Abs(base)
    requested := filepath.Join(absBase, filename)
    absRequested, _ := filepath.Abs(requested)

    if !strings.HasPrefix(absRequested, absBase+string(os.PathSeparator)) {
        return "", errors.New("path traversal attempt detected")
    }

    return absRequested, nil
}
```

**ASVS**: V5.4.1
**References**: [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)

---

## Debug Mode in Production (CWE-489)

### Problem
Debug mode exposes sensitive information and may enable additional attack vectors.

### Python (Flask/Django)

**Don't**:
```python
# VULNERABLE: Debug in production
app.run(debug=True)

# VULNERABLE: Django DEBUG
# settings.py
DEBUG = True

# VULNERABLE: Verbose errors
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500
```

**Do**:
```python
# SECURE: Environment-based configuration
import os

DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
app.run(debug=DEBUG)

# SECURE: Django settings
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# SECURE: Generic error messages
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Error: {e}")  # Log details
    return {"error": "Internal server error"}, 500  # Generic response
```

### JavaScript (Express)

**Don't**:
```javascript
// VULNERABLE: Stack traces exposed
app.use((err, req, res, next) => {
  res.status(500).send(err.stack);
});

// VULNERABLE: NODE_ENV not set
// No environment check
```

**Do**:
```javascript
// SECURE: Environment-aware error handling
app.use((err, req, res, next) => {
  console.error(err);  // Log full error

  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' });
  } else {
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});
```

### Java (Spring Boot)

**Don't**:
```yaml
# VULNERABLE: application.yml
server:
  error:
    include-stacktrace: always
    include-message: always
```

**Do**:
```yaml
# SECURE: application-prod.yml
server:
  error:
    include-stacktrace: never
    include-message: never
    include-binding-errors: never

# SECURE: Profile-based configuration
spring:
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:prod}
```

**ASVS**: V13.2.1, V16.4.1
**References**: [OWASP Error Handling](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

---

## Security Headers (CWE-693)

### Problem
Missing security headers leave applications vulnerable to various attacks.

### Express.js

**Don't**:
```javascript
// VULNERABLE: No security headers
const app = express();
// Headers not configured
```

**Do**:
```javascript
// SECURE: Use helmet middleware
const helmet = require('helmet');

app.use(helmet());

// Or configure individually
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"]
  }
}));

app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```

### Python (Flask)

**Do**:
```python
# SECURE: Flask-Talisman
from flask_talisman import Talisman

csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'"],
    'style-src': ["'self'", "'unsafe-inline'"],
    'img-src': ["'self'", 'data:'],
}

Talisman(app, content_security_policy=csp)

# Or manually
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### Nginx

**Do**:
```nginx
# SECURE: Nginx security headers
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

### Required Headers Reference

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| Content-Security-Policy | XSS prevention | `default-src 'self'` |
| X-Content-Type-Options | MIME sniffing | `nosniff` |
| X-Frame-Options | Clickjacking | `DENY` |
| Strict-Transport-Security | Force HTTPS | `max-age=31536000; includeSubDomains` |
| Referrer-Policy | Control referrer | `strict-origin-when-cross-origin` |
| Permissions-Policy | Feature control | Restrict as needed |

**ASVS**: V3.4.1, V3.4.2, V3.4.3
**References**: [OWASP Secure Headers](https://owasp.org/www-project-secure-headers/)

---

## Quick Reference

| Vulnerability | Fix Pattern | Key Libraries |
|---------------|-------------|---------------|
| Path traversal | Resolve & validate paths | pathlib, path.resolve |
| Debug mode | Environment-based config | dotenv, profiles |
| Missing headers | Security middleware | helmet, Flask-Talisman |

## See Also

- `remediation-injection` - Injection fixes
- `remediation-crypto` - Cryptography fixes
- `remediation-auth` - Authentication/authorization fixes
- `vulnerability-patterns` - Detection patterns

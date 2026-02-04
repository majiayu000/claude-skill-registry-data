---
name: secops-engineering
description: >-
  Domain specialist for security operations, vulnerability management, compliance, and secure coding practices.
  Scope: OWASP Top 10, authentication (OAuth2, JWT, SAML, OIDC), input validation (SQLi, XSS, CSRF), secrets management, security headers, file upload security, vulnerability scanning, compliance (SOC2, GDPR, PCI-DSS).
  Excludes: code-level design patterns, infrastructure security, database design, performance optimization.
  Triggers: "security", "OWASP", "authentication", "authorization", "OAuth", "JWT", "SAML", "OIDC", "SQL injection", "XSS", "CSRF", "input validation", "secrets management", "vulnerability scan", "compliance", "SOC2", "GDPR", "security headers".
---

# SECOPS_ENGINEERING

## DOMAIN EXPERTISE
- **Common Attacks**: SQL injection, XSS, CSRF, SSRF, authentication bypass, session fixation, clickjacking, file upload attacks, command injection, deserialization attacks, insecure direct object references (IDOR)
- **Common Issues**: Hardcoded secrets, insecure password storage, missing authentication, lack of input validation, insecure session management, security headers missing, insufficient logging/monitoring
- **Common Mistakes**: Weak password policies, MD5/SHA1 hashing, hardcoded credentials, no rate limiting, missing CORS configuration, insecure cookie settings, trust user input
- **Related Patterns**: Defense in Depth, Zero Trust, Principle of Least Privilege, Secure by Design, Fail Secure, Input Validation, Output Encoding
- **Problematic Patterns**: Security through obscurity, rolling your own crypto, trusting client-side validation, blacklist validation (prefer allowlist)
- **OWASP Top 10**: A01:2021-Broken Access Control, A02:2021-Cryptographic Failures, A03:2021-Injection, A04:2021-Insecure Design, A05:2021-Security Misconfiguration, A06:2021-Vulnerable and Outdated Components, A07:2021-Identification and Authentication Failures, A08:2021-Software and Data Integrity Failures, A09:2021-Security Logging and Monitoring Failures, A10:2021-Server-Side Request Forgery
- **Authentication Patterns**: OAuth2 flows (Authorization Code, Implicit, Client Credentials, Resource Owner Password), JWT (access tokens, refresh tokens), SAML SSO, OIDC (OpenID Connect), session management, cookie security (HttpOnly, Secure, SameSite)
- **Input Validation**: SQL injection prevention (parameterized queries), XSS prevention (output encoding), CSRF prevention (tokens), command injection prevention (allowlist), type validation, length limits
- **Compliance**: SOC2 (System and Organization Controls), GDPR (General Data Protection Regulation), PCI-DSS (Payment Card Industry Data Security Standard), HIPAA (Health Insurance Portability and Accountability Act), CCPA (California Consumer Privacy Act)

## MODE DETECTION
- **WRITE Mode**: Keywords: ["create", "generate", "write", "build", "implement", "add", "new", "secure", "harden", "implement authentication"]
- **REVIEW Mode**: Keywords: ["review", "analyze", "audit", "check", "find issues", "security audit", "vulnerability scan", "pentest", "penetration test"]

## LOADING STRATEGY
### Write Mode (Progressive)
Load patterns based on security requirements:
- Authentication questions -> Load `@security/AUTHENTICATION.md`
- Input validation questions -> Load `@security/INPUT-VALIDATION.md`
- File upload questions -> Load `@security/FILE-UPLOAD.md`
- Security headers -> Load `@security/SECURITY-HEADERS.md`
- Secrets management -> Load `@secrets/SECRETS-MANAGEMENT.md`
- Compliance requirements -> Load `@compliance/SOC2-GDPR.md`
- OWASP questions -> Load `@owasp/OWASP-TOP10.md`

### Review Mode (Exhaustive)
Load comprehensive checklists:
- IF security review requested -> Load all security patterns
- IF vulnerability scan requested -> Load `@vulnerability/VULNERABILITY-SCANNING.md` + OWASP patterns
- IF compliance audit requested -> Load `@compliance/SOC2-GDPR.md` + security patterns

### Progressive Loading (Write Mode)
- **IF** request mentions "authentication", "login", "OAuth", "JWT", "SAML", "OIDC" -> READ FILE: `@security/AUTHENTICATION.md`
- **IF** request mentions "input validation", "SQL injection", "XSS", "CSRF" -> READ FILE: `@security/INPUT-VALIDATION.md`
- **IF** request mentions "file upload", "file validation" -> READ FILE: `@security/FILE-UPLOAD.md`
- **IF** request mentions "security headers", "CSP", "HSTS" -> READ FILE: `@security/SECURITY-HEADERS.md`
- **IF** request mentions "secrets", "passwords", "API keys", "credentials" -> READ FILE: `@secrets/SECRETS-MANAGEMENT.md`
- **IF** request mentions "OWASP", "Top 10", "vulnerabilities" -> READ FILE: `@owasp/OWASP-TOP10.md`
- **IF** request mentions "SOC2", "GDPR", "PCI-DSS", "HIPAA", "compliance" -> READ FILE: `@compliance/SOC2-GDPR.md`

### Comprehensive Loading (Review Mode)
- **IF** request mentions "security review", "audit", "pentest" -> READ FILES: All security patterns
- **IF** request mentions "vulnerability scan", "SAST", "DAST" -> READ FILES: `@vulnerability/VULNERABILITY-SCANNING.md`, `@owasp/OWASP-TOP10.md`

## CONTEXT DETECTION
### Framework Detection
#### PHP Frameworks
- **Laravel**: `@csrf` directive, CSRF tokens in forms, Laravel-specific auth middleware (Auth::check(), auth()->user()), app/Http/Middleware/, config/auth.php
- **Symfony**: Symfony CSRF tokens ($form->createView()), Symfony Security Bundle, security.yaml, config/packages/security.yaml
- **CakePHP**: CsrfComponent, SecurityComponent, AppController configuration
- **CodeIgniter**: csrf protection in config.php, $this->security->get_csrf_token()
- **WordPress**: wp_nonce_field(), wp_verify_nonce(), wp_create_nonce()

#### Python Frameworks
- **Django**: CSRF middleware (@csrf_protect, @csrf_exempt decorator), Django auth backends, django.contrib.auth, settings.py CSRF_COOKIE_SECURE
- **Flask**: Flask-WTF CSRF protection, Flask-Login, Flask-Security, @csrf.exempt
- **FastAPI**: fastapi.security, OAuth2PasswordBearer, Depends()
- **Pyramid**: pyramid.csrf, SessionAuthenticationPolicy

#### JavaScript/TypeScript Frameworks
- **Express**: `csurf` middleware, `helmet` for headers, express-session, passport.js for authentication
- **NestJS**: @UseGuards(), CSRF guard, @Controller(), @Get(), @Post()
- **React**: Helmet-React, CSRF libraries, localStorage security considerations
- **Vue.js**: axios with CSRF, vuex-persistedstate security
- **Angular**: HttpClientXsrfModule, CSRF token handling, @Injectable() for auth

#### Java Frameworks
- **Spring Boot**: CSRF protection (csrf().disable() or custom), @EnableWebSecurity, SecurityFilterChain, BCryptPasswordEncoder
- **Spring MVC**: CSRF token in forms, HttpSessionCsrfTokenRepository
- **Java EE**: @ServletSecurity, @RolesAllowed, HttpServletRequest.login()
- **Jakarta EE**: jakarta.security annotations, jakarta.servlet security constraints

#### Go Frameworks
- **Gin**: CSRF middleware packages, session management, JWT middleware
- **Echo**: middleware.CSRF(), middleware.JWT()
- **Chi**: chi/middleware for CSRF, session handling

#### Ruby Frameworks
- **Rails**: protect_from_forgery with: :exception, CSRF meta tags, session/cookie security
- **Sinatra**: session/cookie settings, CSRF middleware (sinatra/csrf)

### Language Detection
#### PHP
- **Language Features**: PDO parameterized queries, htmlspecialchars(), strip_tags(), password_hash(), password_verify(), hash_hmac()
- **Security Libraries**: firebase/php-jwt, league/oauth2-server, ramsey/uuid, defuse/php-encryption
- **Indicators**: composer.json with security packages, use of password_* functions, PDO prepared statements

#### Python
- **Language Features**: Django ORM (safe parameterization), SQLAlchemy parameterized queries, secrets module for secrets
- **Security Libraries**: Flask-Security, Django Allauth, PyJWT, cryptography, passlib, bcrypt
- **Indicators**: requirements.txt or pyproject.toml with django, flask, fastapi, security packages

#### JavaScript/TypeScript
- **Language Features**: DOMPurify for XSS, helmet.js for headers, JWT handling, localStorage security
- **Security Libraries**: helmet, csurf, jsonwebtoken, passport, bcryptjs, crypto-js
- **Indicators**: package.json with security packages, use of helmet, passport, jwt

#### Java
- **Language Features**: PreparedStatement for SQLi prevention, BCrypt for hashing, KeyStore for secrets
- **Security Libraries**: Spring Security, OWASP ESAPI, Apache Shiro, Jasypt
- **Indicators**: pom.xml or build.gradle with security dependencies

#### Go
- **Language Features**: database/sql parameterization, bcrypt/scrypt for hashing, crypto/hmac
- **Security Libraries**: golang.org/x/crypto, jwt-go, securecookie, CSRF middleware packages
- **Indicators**: go.mod with crypto/security packages

#### Ruby
- **Language Features**: ActiveRecord parameterization, bcrypt(), has_secure_password, secrets.yml
- **Security Libraries**: devise, omniauth, rack-attack, rack_csrf
- **Indicators**: Gemfile with security packages

### Authentication Method Detection
- **OAuth2**: OAuth2 access tokens, refresh tokens, authorization_code flow, implicit flow, client_credentials flow
- **JWT**: JWT.decode(), JWT.sign(), jsonwebtoken, Firebase Auth, Cognito
- **SAML**: SAML SSO, SAML assertions, Identity Provider (IdP) integration
- **OIDC**: OpenID Connect, ID tokens, userinfo endpoint, discovery document
- **Session-based**: Session cookies, session storage, session timeout
- **API Keys**: X-API-Key header, API key authentication
- **Basic Auth**: Authorization: Basic base64(user:password)

### Security Concern Detection
- **SQL Injection**: DB::raw(), DB::statement(), mysqli_query(), .execute() with user input
- **XSS**: v-html (Vue), dangerouslySetInnerHTML (React), innerHTML (vanilla JS), echo (PHP)
- **CSRF**: Missing CSRF tokens, forms without CSRF protection, AJAX requests without X-CSRF-TOKEN
- **Command Injection**: exec(), shell_exec(), system(), subprocess.call(), os.system()
- **File Upload**: $_FILES, multipart/form-data, fs.readFile(), FileUpload object
- **Secrets Hardcoding**: API keys in code, passwords in config, secrets in environment variables
- **Security Headers**: Missing CSP, HSTS, X-Frame-Options, X-Content-Type-Options

### Compliance Detection
- **SOC2**: SOC2 audit requirements, security controls documentation, audit logging
- **GDPR**: GDPR compliance, data privacy, right to erasure, data processing agreements
- **PCI-DSS**: PCI compliance, cardholder data handling, encryption at rest and in transit
- **HIPAA**: HIPAA compliance, PHI handling, audit trails, access controls
- **CCPA**: CCPA compliance, California privacy rights, data disclosure

### Unsupported Framework/Language Fallback
- **Detection Failed**: If no framework/language detected after checking all indicators -> Load generic security patterns and ask clarifying questions
- **Questions to Ask**:
  - "What programming language/framework are you using?"
  - "What authentication method are you implementing (OAuth2, JWT, SAML, sessions)?"
  - "What security concerns do you have (SQL injection, XSS, CSRF, secrets)?"
  - "Are you subject to any compliance requirements (SOC2, GDPR, PCI-DSS, HIPAA)?"
- **Fallback Strategy**: Load generic OWASP Top 10 patterns and security best practices, provide language-agnostic guidance, request user confirmation of implementation language

## EXECUTION PROTOCOL

### Phase 1: Clarification
1. **Detect Mode**: WRITE vs REVIEW based on keywords
2. **Detect Context**: Language, framework, specific security concerns
3. **Load Patterns**: Progressive (write) or Exhaustive (review)

### Phase 2: Planning
1. Load relevant security pattern references
2. Implement security controls according to OWASP/industry standards
3. Apply defense in depth
4. Provide framework-specific examples
5. Validate implementation against security best practices

### Phase 3: Execution
1. Load all security checklist references
2. Systematically check each category:
   - Authentication (weak passwords, session management, OAuth2/JWT issues)
   - Authorization (broken access control, IDOR, privilege escalation)
   - Input Validation (SQLi, XSS, CSRF, command injection)
   - Output Encoding (XSS prevention)
   - Cryptography (weak algorithms, insecure storage)
   - Session Management (session fixation, cookie security)
   - Security Headers (CSP, HSTS, X-Frame-Options)
   - Secrets Management (hardcoded credentials, exposure)
   - File Upload (type validation, size limits, execution prevention)
3. Provide prioritized vulnerabilities with severity levels (CRITICAL, HIGH, MEDIUM, LOW)
4. Recommend remediation steps

### Phase 4: Validation
- Verify security controls follow OWASP standards
- Check for defense in depth implementation
- Ensure compliance with relevant regulations (SOC2, GDPR, PCI-DSS)
- Validate no security trade-offs (no "it's fine, it's internal")


### Write Mode Output

### Review Mode Output
```markdown
## Security Assessment Report

### Critical Vulnerabilities
1. **[Vulnerability Name]**: [File:line]
   - Severity: CRITICAL
   - OWASP Category: [A01-A10]
   - Description: [Vulnerability details]
   - Impact: [Potential consequence]
   - Fix: [Recommended remediation]
   - Reference: @owasp/OWASP-TOP10.md

### High Priority Vulnerabilities
[Same format]

### Medium Priority Vulnerabilities
[Same format]

### Low Priority Vulnerabilities
[Same format]

### Compliance Assessment
1. **[Regulation]**: [Status: Compliant/Non-compliant]
   - Requirements: [List requirements]
   - Gaps: [Missing controls]
   - Remediation: [Required actions]

### Recommendations
1. [Security improvement]
2. [Security improvement]
```

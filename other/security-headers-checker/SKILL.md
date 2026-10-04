---
name: security-headers-checker
description: Check HTTP security headers response
activation_keywords: [security, header, http, security header, cors, csrf, hsts]
execution_mode: server
---

# Security Headers Checker

Checks HTTP security response headers:
- HSTS (HTTP Strict Transport Security)
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Content-Security-Policy
- Referrer-Policy
- Permissions-Policy
- Cross-Origin policies

Use `builtin_security_headers_checker` tool with fields:
- `url`: URL to check (required)
- `headers`: (optional) raw HTTP headers to check

Returns analysis of security headers with recommendations.

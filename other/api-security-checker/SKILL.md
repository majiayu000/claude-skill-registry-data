---
name: api-security-checker
description: Check API for common security vulnerabilities
activation_keywords: [security, sql injection, xss, vulnerability, injection, sanitize, api security]
execution_mode: server
---

# API Security Checker

Checks for common web security vulnerabilities:
- SQL Injection detection
- XSS (Cross-Site Scripting) detection
- Command Injection detection
- Path Traversal detection
- LDAP Injection detection
- XXE detection
- Unsafe deserialization

Use `builtin_api_security_checker` tool with fields:
- `code`: the code or request to check (required)
- `language`: (optional) programming language (default: auto-detect)
- `check_types`: (optional) array of vulnerability types to check

Returns list of potential vulnerabilities with severity and recommendations.

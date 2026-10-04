---
name: secrets-scanner
description: Scan for sensitive information in code like API keys, tokens, passwords
activation_keywords: [secrets, scan, api key, token, credentials, sensitive, leak, security]
execution_mode: server
---

# Secrets Scanner

Scans text or code for sensitive information:
- API Keys detection (AWS, GCP, Azure, etc.)
- Token detection (JWT, OAuth, Bearer tokens)
- Password detection
- Private key detection (RSA, DSA, EC private keys)
- AWS Access Key ID and Secret
- Generic API keys and tokens
- Database connection strings
- Private keys and certificates

Use `builtin_secrets_scanner` tool with fields:
- `text`: the text to scan (required)
- `patterns`: (optional) custom regex patterns to detect

Returns list of detected secrets with type and location.

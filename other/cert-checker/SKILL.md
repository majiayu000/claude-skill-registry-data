---
name: certificate-checker
description: Check SSL/TLS certificate expiry and details for domains
activation_keywords: [certificate, ssl, tls, cert, expiry, expire, https]
execution_mode: client
---

# Certificate Checker Skill

Provides SSL/TLS certificate inspection:
- Check certificate expiry date
- View certificate issuer and subject
- List certificate chain
- Check certificate validity

Use `builtin_cert_checker` tool with fields:
- `domain`: target domain to check (required)
- `port`: (optional) port number (default: 443)

Note: Requires network access to the target domain.

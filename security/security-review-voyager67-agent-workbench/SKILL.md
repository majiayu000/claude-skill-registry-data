---
name: security-review
description: Review an application change or component for common security and privacy risks. Use when code touches authentication, authorization, untrusted input, secrets, data access, dependencies, or external actions.
---

# Security Review

Perform a scoped threat-oriented review; do not claim formal certification.

1. Identify assets, trust boundaries, entry points, identities, permissions, sensitive data, and external services.
2. Trace authentication and authorization separately. Verify server-side enforcement and least privilege.
3. Inspect input validation, output encoding, injection surfaces, file handling, deserialization, redirects, and resource limits as relevant.
4. Check secrets, logs, error messages, tokens, configuration, dependency provenance, and unsafe defaults.
5. Consider replay, race conditions, abuse, denial of service, and data exposure where applicable.
6. Report findings with severity, preconditions, impact, location, and a practical mitigation.
7. Recommend tests or safe validation steps. Never exploit a live system or exfiltrate data.

Do not print credentials or sensitive values. Avoid destructive or intrusive testing without explicit authorization and a defined scope. Distinguish confirmed vulnerabilities from hardening suggestions and unknowns.

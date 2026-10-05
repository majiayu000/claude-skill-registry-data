---
name: pci-dss
description: "PCI DSS v4.0 compliance audit for payment-handling codebases. Scans for PAN patterns (Visa, Mastercard, Amex, Discover), CVV storage violations, and track data retention. Triggers: building or auditing payment flows, Stripe/Braintree/Adyen integrations."
version: "2.0.1"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Audit every applicable PCI DSS requirement systematically.

TARGET:
$ARGUMENTS

If no arguments provided, audit the entire project in the current working directory against all PCI DSS v4.0 requirements.

============================================================
PHASE 0: SCOPE DETERMINATION
============================================================

Determine the Cardholder Data Environment (CDE) scope:

TECH STACK DETECTION:
- Identify web framework, language, database, and infrastructure configuration
- Identify payment processing libraries (Stripe SDK, Braintree, Adyen, Square, custom)
- Identify tokenization or vault services in use
- Identify third-party payment integrations (iframes, redirect, direct API)

CDE BOUNDARY MAPPING:
- Identify all files that handle, process, store, or transmit cardholder data
- Map data flows: where card data enters, how it moves, where it persists
- Identify connected systems that share network or access with CDE components
- Classify the SAQ type likely applicable (A, A-EP, D, etc.)
- Flag any PAN (Primary Account Number) patterns found in code, configs, or logs

CARDHOLDER DATA PATTERNS — scan for these regex patterns:
- PAN: `\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b`
- CVV in variable names: `cvv|cvc|cvn|security.?code|card.?verification`
- Track data references: `track.?1|track.?2|magnetic.?stripe`
- PIN references: `pin.?block|encrypted.?pin`

Produce a CDE scope map before proceeding.

============================================================
PHASE 1: REQUIREMENTS 1-2 — NETWORK SECURITY
============================================================

Audit network security controls:

REQUIREMENT 1 — NETWORK SECURITY CONTROLS:
- Check firewall/security group configurations (Terraform, CloudFormation, docker-compose)
- Verify CDE segmentation from non-CDE systems
- Check for DMZ configuration between public internet and CDE
- Verify inbound and outbound traffic rules restrict to business need
- Check for default-deny rules on network boundaries
- Flag overly permissive rules (0.0.0.0/0 ingress on sensitive ports)

REQUIREMENT 2 — SECURE CONFIGURATIONS:
- Check for default passwords in configuration files, docker-compose, or environment variables
- Scan for vendor-default credentials (admin/admin, postgres/postgres, root/root)
- Verify unnecessary services are disabled (unused ports, debug endpoints)
- Check that system hardening is documented or automated (Ansible, Terraform, Dockerfiles)
- Verify single-purpose servers (payment processing not co-located with general web serving)
- Check for development/test artifacts in production configurations

For each finding: requirement ID, file path, severity, description, remediation.

============================================================
PHASE 2: REQUIREMENT 3 — STORED CARDHOLDER DATA
============================================================

Audit protection of stored cardholder data:

DATA RETENTION:
- Check for data retention policies implemented in code
- Verify PAN is not stored after authorization unless business-justified
- Check that CVV/CVC is NEVER stored post-authorization (any storage = automatic FAIL)
- Verify track data is NEVER stored post-authorization
- Check for automated data purging/deletion mechanisms
- Scan database schemas and migration files for cardholder data columns

ENCRYPTION AT REST:
- Check if stored PAN is rendered unreadable (encryption, truncation, tokenization, hashing)
- Verify encryption algorithm strength (AES-256 minimum for stored data)
- Check encryption key management:
  - Keys not hardcoded in source
  - Key rotation procedures implemented
  - Split knowledge / dual control for key management
  - Key storage separate from encrypted data
- Verify column-level or application-level encryption for PAN fields
- Check for transparent data encryption (TDE) on databases containing cardholder data

MASKING AND TRUNCATION:
- Check that PAN display is masked (show max first 6 / last 4 digits)
- Verify masking is applied server-side (not just UI masking)
- Check API responses for full PAN exposure
- Verify log files do not contain full PAN

TOKENIZATION:
- If tokenization is used, verify token-to-PAN mapping is in a secured vault
- Check that tokens cannot be reversed without vault access
- Verify tokenization service is PCI-compliant

============================================================
PHASE 3: REQUIREMENT 4 — TRANSMISSION ENCRYPTION
============================================================

Audit encryption of cardholder data in transit:

TLS CONFIGURATION:
- Check for TLS 1.2+ enforcement (flag TLS 1.0, 1.1, SSLv3)
- Verify certificate validation is not disabled (`rejectUnauthorized: false`, `verify=False`)
- Check for strong cipher suites (no RC4, DES, NULL ciphers)
- Verify HSTS headers are set with adequate max-age
- Check for certificate pinning on mobile clients communicating with CDE

INTERNAL TRANSMISSION:
- Check if cardholder data transmitted between internal services is encrypted
- Verify service-to-service communication uses TLS (not plain HTTP)
- Check message queue encryption for cardholder data payloads
- Verify database connections use TLS/SSL

END-USER TRANSMISSION:
- Check that all pages collecting card data use HTTPS
- Verify no mixed content on payment pages
- Check for secure WebSocket connections (wss://) if applicable
- Verify email and messaging channels never contain PAN

============================================================
PHASE 4: REQUIREMENTS 5-6 — VULNERABILITY MANAGEMENT
============================================================

Audit secure development and vulnerability management:

REQUIREMENT 5 — MALWARE PROTECTION:
- Check for dependency scanning in CI/CD pipeline
- Verify container image scanning if Docker/Kubernetes is used
- Check for runtime protection agents or security monitoring
- Note: traditional antivirus is infrastructure, but code-level protections apply

REQUIREMENT 6 — SECURE DEVELOPMENT:
- Check for secure coding practices:
  - Input validation on all payment-related endpoints
  - Output encoding to prevent XSS on payment pages
  - Parameterized queries (no SQL injection risk in payment flows)
  - CSRF protection on payment form submissions
- Verify security review process in development lifecycle
- Check for public-facing web application protection (WAF configuration, CSP headers)
- Verify custom code changes go through a review process
- Check for separation of development/test and production environments
- Verify production data is not used in development/test (or is properly sanitized)

PCI DSS v4.0 ADDITIONS:
- Check for automated technical solution to detect and prevent web-based skimming (Req 6.4.3)
- Verify script integrity monitoring on payment pages
- Check for Content-Security-Policy headers on payment pages
- Verify Subresource Integrity (SRI) on third-party scripts

============================================================
PHASE 5: REQUIREMENTS 7-8 — ACCESS CONTROL
============================================================

Audit access control mechanisms:

REQUIREMENT 7 — RESTRICT ACCESS BY BUSINESS NEED:
- Check RBAC implementation for payment/CDE-related functionality
- Verify principle of least privilege in code (minimum required permissions)
- Check API authorization on all CDE endpoints
- Verify administrative access to cardholder data is restricted and logged
- Check for default access levels (new accounts should have minimal access)

REQUIREMENT 8 — IDENTIFY AND AUTHENTICATE:
- Check for unique user identification (no shared accounts in code/config)
- Verify MFA implementation for administrative access to CDE
- Check password complexity enforcement:
  - Minimum 12 characters (v4.0 requirement)
  - Complexity requirements or passphrase support
  - Password history enforcement
- Verify account lockout after failed attempts (max 10 attempts)
- Check session management:
  - Session timeout after 15 minutes of inactivity
  - Session invalidation on logout
  - Secure session token generation
  - Cookie flags: Secure, HttpOnly, SameSite
- Verify service accounts use unique credentials (not shared across systems)

PCI DSS v4.0 ADDITIONS:
- Check for MFA for all access to CDE (not just remote — Req 8.4.2)
- Verify MFA implementation is not susceptible to replay attacks
- Check that authentication factors are independent

============================================================
PHASE 6: REQUIREMENT 9 — PHYSICAL ACCESS
============================================================

NOTE: Requirement 9 covers physical access controls. This is largely out of scope
for code analysis. However, check for:

- Physical access control references in infrastructure-as-code
- Server room access logging configuration
- Security camera integration code
- Badge/key card system integrations
- Visitor management system code

Flag as: "Req 9 — Physical Access: Primarily non-code. [N findings in IaC if any]"

============================================================
PHASE 7: REQUIREMENT 10 — LOGGING AND MONITORING
============================================================

Audit logging and monitoring for CDE:

AUDIT TRAIL:
- Verify all access to cardholder data is logged
- Check that logs include: user ID, event type, date/time, success/failure, origin, affected data
- Verify all administrative actions are logged
- Check that authentication events are logged (success and failure)
- Verify log entries cannot be modified or deleted (immutability)

LOG PROTECTION:
- Check that logs do not contain cardholder data (PAN, CVV)
- Verify log access is restricted to authorized personnel
- Check for log integrity mechanisms (checksums, write-once storage)
- Verify log retention meets requirements (12 months, 3 months immediately available)

MONITORING AND ALERTING:
- Check for security event alerting configuration
- Verify critical alerts are defined (failed auth, access violations, system changes)
- Check for log aggregation and SIEM integration
- Verify time synchronization (NTP) for accurate timestamps across systems

============================================================
PHASE 8: REQUIREMENT 11 — SECURITY TESTING
============================================================

Audit security testing practices in code and CI/CD:

VULNERABILITY SCANNING:
- Check for automated vulnerability scanning in CI/CD pipeline
- Verify dependency audit tools are configured (npm audit, pip-audit, OWASP DC)
- Check for SAST (static analysis) tool integration
- Verify DAST configuration if applicable

PENETRATION TESTING:
- Check for penetration test configurations or scripts
- Look for bug bounty program references
- Verify segmentation testing documentation or automation

CHANGE DETECTION:
- Check for file integrity monitoring on critical CDE files
- Verify critical file change alerting (payment processing code, config)
- Check for unauthorized change detection mechanisms

PCI DSS v4.0 ADDITIONS:
- Check for authenticated internal vulnerability scanning (Req 11.3.1.2)
- Verify multi-tenant service provider segmentation testing if applicable

============================================================
PHASE 9: REQUIREMENT 12 — POLICY REFERENCES
============================================================

Check for security policy artifacts in the codebase:

- Verify security policy references in documentation or code comments
- Check for acceptable use policy acknowledgment in user flows
- Verify incident response procedures referenced or documented
- Check for security awareness references (training requirements in onboarding code)
- Verify risk assessment artifacts or references
- Check for third-party service provider management (vendor security assessment references)


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the security analysis, validate thoroughness:

1. Verify every category in the audit was actually checked (not skipped).
2. Verify every finding has a specific file:line location.
3. Verify severity ratings are justified by impact assessment.
4. Verify no false positives by re-reading flagged code in context.

IF VALIDATION FAILS:
- Re-audit skipped categories or vague findings
- Verify or remove false positives
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## PCI DSS v4.0 Compliance Audit Report

**Project:** [name]
**Stack:** [detected technologies]
**CDE Scope:** [scope description]
**SAQ Type (estimated):** [A / A-EP / D / N/A]

### Summary

| Req | Category | Status | Findings | Critical |
|-----|----------|--------|----------|----------|
| 1 | Network Security Controls | [PASS/WARN/FAIL] | N | N |
| 2 | Secure Configurations | [PASS/WARN/FAIL] | N | N |
| 3 | Stored Cardholder Data | [PASS/WARN/FAIL] | N | N |
| 4 | Transmission Encryption | [PASS/WARN/FAIL] | N | N |
| 5 | Malware Protection | [PASS/WARN/FAIL] | N | N |
| 6 | Secure Development | [PASS/WARN/FAIL] | N | N |
| 7 | Access Restriction | [PASS/WARN/FAIL] | N | N |
| 8 | Identification/Auth | [PASS/WARN/FAIL] | N | N |
| 9 | Physical Access | [OUT-OF-SCOPE] | N | N |
| 10 | Logging/Monitoring | [PASS/WARN/FAIL] | N | N |
| 11 | Security Testing | [PASS/WARN/FAIL] | N | N |
| 12 | Policy | [PASS/WARN/FAIL] | N | N |

### CDE Data Flow Map
[Description of cardholder data flow through the system]

### Cardholder Data Discovery
| Location | Data Type | Protected | Action Required |
|----------|-----------|-----------|-----------------|

### Detailed Findings

For each requirement with WARN or FAIL:

#### Requirement [N] — [Name]

| # | Severity | Sub-Req | File | Line | Description | Remediation |
|---|----------|---------|------|------|-------------|-------------|

### Risk Assessment
- **Immediate blockers (FAIL):** [count] — must remediate before assessment
- **Significant gaps (WARN):** [count] — remediate before next assessment cycle
- **Informational:** [count] — address as part of continuous improvement

### Remediation Priority
[Ordered list: data exposure issues first, then access control, then logging, then configuration]

============================================================
NEXT STEPS
============================================================

After reviewing the audit:
- "Run `/owasp` to audit against OWASP Top 10 (overlaps with Req 6)."
- "Run `/encryption` to deep-dive into cryptographic implementation (Req 3-4)."
- "Run `/secure` for the full security posture assessment beyond PCI."
- "Run `/dependency-scan` to address vulnerable components (Req 6/11)."
- "Run `/pentest` to validate exploitability of findings (Req 11)."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /pci-dss — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT modify any code — this is an audit skill, not a remediation skill.
- Do NOT expose discovered cardholder data (PAN, CVV) in the output — redact fully.
- Do NOT expose discovered secrets or credentials — show first 4 chars + ***.
- Do NOT skip any requirement — audit all 12 even if some appear not applicable.
- Do NOT mark a requirement as PASS without evidence of compliance.
- Do NOT provide a definitive compliance determination — this is a code-level assessment, not a QSA audit.
- Do NOT assume tokenization or third-party processing eliminates all requirements — verify scope reduction.
- Do NOT run actual vulnerability scans or exploits — analyze code and configuration only.

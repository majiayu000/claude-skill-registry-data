---
name: hipaa
description: "Deep HIPAA Security Rule technical audit mapping code-level findings to 45 CFR sections. Triggers: building or auditing healthcare apps, EHR integrations, FHIR APIs, telehealth platforms."
version: "2.0.1"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Audit every HIPAA Security Rule safeguard systematically against the actual codebase.

TARGET:
$ARGUMENTS

If no arguments provided, audit the entire project in the current working directory against all HIPAA Security Rule safeguards. If a specific safeguard category is named (e.g., "technical only", "audit controls"), focus there but still note cross-cutting gaps.

============================================================
PHASE 0: SYSTEM CHARACTERIZATION
============================================================

Before auditing, characterize the system:

1. Detect the tech stack (package.json, requirements.txt, pom.xml, go.mod, etc.).
2. Identify the system architecture:
   - Monolith or microservices?
   - What database(s)? (PostgreSQL, MongoDB, DynamoDB, etc.)
   - What cloud provider? (AWS, Azure, GCP, on-prem)
   - What authentication system? (custom JWT, OAuth2, SAML, SMART on FHIR)
   - What message queues or event buses?
   - What file/blob storage?
3. Map PHI-containing components:
   - Which data models/tables contain PHI?
   - Which services process PHI?
   - Which APIs accept or return PHI?
   - Where is PHI cached (Redis, in-memory, CDN)?
4. Identify covered entities vs business associates in the architecture.

============================================================
PHASE 1: ADMINISTRATIVE SAFEGUARDS (45 CFR 164.308)
============================================================

Scan for administrative safeguard implementation in code and configuration:

SECURITY MANAGEMENT PROCESS (164.308(a)(1)):
- Risk analysis: search for risk assessment documentation, threat models, or
  security review artifacts in the codebase.
- Risk management: check for security controls that mitigate identified risks.
- Sanction policy: search for account lockout, access revocation, or
  disciplinary workflow code.
- Information system activity review: verify audit log review mechanisms exist.

WORKFORCE SECURITY (164.308(a)(3)):
- Authorization/supervision: check for role hierarchy definitions.
- Workforce clearance: search for background check status fields in user models.
- Termination procedures: check for account deactivation workflows, not deletion.
  Verify deactivated accounts cannot authenticate.

INFORMATION ACCESS MANAGEMENT (164.308(a)(4)):
- Access authorization: check for formal access request/approval workflows in code.
- Access establishment: verify new user provisioning includes role assignment.
- Access modification: check for role change audit trails.
- Isolating healthcare clearinghouse functions (if applicable).

SECURITY AWARENESS (164.308(a)(5)):
- Security reminders: check for in-app security notifications or training prompts.
- Malicious software protection: check for file upload scanning, input sanitization.
- Login monitoring: verify failed login tracking and alerting.
- Password management: check password complexity rules, rotation policies,
  history enforcement.

SECURITY INCIDENT PROCEDURES (164.308(a)(6)):
- Incident response: search for incident detection, logging, and escalation code.
- Check for anomaly detection on PHI access patterns.
- Verify incident documentation capabilities (timestamps, actors, impact).

CONTINGENCY PLAN (164.308(a)(7)):
- Data backup plan: check for backup configuration (frequency, encryption, testing).
- Disaster recovery: search for DR configuration, failover mechanisms.
- Emergency mode operation: check for degraded-mode functionality.
- Testing and revision: search for backup restore test artifacts.

EVALUATION (164.308(a)(8)):
- Search for security review schedules, penetration test reports, or
  compliance scan configurations in CI/CD.

============================================================
PHASE 2: PHYSICAL SAFEGUARDS (45 CFR 164.310)
============================================================

Scan for physical safeguard implementation (in infrastructure config and code):

FACILITY ACCESS CONTROLS (164.310(a)(1)):
- Check cloud provider configuration for region restrictions.
- Verify infrastructure-as-code restricts physical deployment locations.
- Check for environment isolation (dev/staging/prod separation).

WORKSTATION USE AND SECURITY (164.310(b)/(c)):
- Check for session timeout configuration in web/mobile clients.
- Verify screen lock enforcement (mobile MDM configuration if present).
- Check for auto-logout on inactivity thresholds.
- Verify clipboard clearing for PHI data in mobile apps.

DEVICE AND MEDIA CONTROLS (164.310(d)(1)):
- Disposal: check for data sanitization code (secure delete, crypto-shredding).
- Media re-use: verify temp files containing PHI are securely cleaned.
- Accountability: check for device tracking/registration features.
- Data backup and storage: verify portable media encryption requirements.

============================================================
PHASE 3: TECHNICAL SAFEGUARDS (45 CFR 164.312)
============================================================

This is the primary code audit phase. Scan deeply for each technical safeguard:

ACCESS CONTROL (164.312(a)(1)):

Unique User Identification:
- Verify every user gets a unique identifier (no shared accounts).
- Check user model for unique constraints on username/email.
- Flag any shared service accounts that access PHI.
- Verify API clients have unique identifiers (not shared API keys).

Emergency Access Procedure:
- Search for break-glass or emergency access mechanisms.
- Check if emergency access is logged separately.
- Verify emergency access is time-bounded and audited.
- Flag absence of any emergency access capability.

Automatic Logoff:
- Check session timeout values (web: 15-30 min recommended for PHI).
- Verify server-side session expiration (not just client-side).
- Check for token expiration on JWT-based systems.
- Verify idle timeout vs absolute timeout distinction.
- Check mobile app background timeout behavior.

Encryption and Decryption:
- Database encryption: check for TDE, column-level, or application-level encryption.
- File storage encryption: verify S3 SSE, Azure Storage encryption, or equivalent.
- Application-level encryption: search for encrypt/decrypt functions on PHI fields.
- Key management: check for KMS integration, key rotation, key separation.
- Flag PHI fields stored in plaintext.
- Check encryption algorithms: AES-256 required, flag AES-128 or weaker.
- Verify encryption key storage (not hardcoded, not in same DB as encrypted data).

AUDIT CONTROLS (164.312(b)):

Comprehensive Audit Logging:
- Map every PHI access point (API endpoint, database query, file read).
- Verify each access point has audit logging.
- Check audit log content: timestamp, user ID, action, resource, patient ID,
  IP address, user agent.
- Verify read access is logged (not just writes).
- Check for bulk export/download audit logging.
- Verify audit logs for failed access attempts.
- Flag any PHI access path that bypasses audit logging.

Audit Log Protection:
- Verify audit logs are stored separately from application data.
- Check for tamper protection (append-only, signed, blockchain-backed).
- Verify audit log encryption.
- Check retention policy (HIPAA requires 6 years minimum).
- Flag if audit logs can be deleted by application admins.

Audit Log Review:
- Search for log analysis/review mechanisms.
- Check for automated alerts on suspicious access patterns.
- Verify dashboards or reporting on audit data.

INTEGRITY (164.312(c)(1)):

Data Integrity Mechanisms:
- Check for checksums or hashes on PHI records.
- Verify database constraints (NOT NULL, CHECK, FK) on PHI tables.
- Check for optimistic locking on concurrent PHI updates.
- Verify input validation on all PHI data entry points.
- Check for data corruption detection mechanisms.

Electronic PHI Integrity:
- Verify digital signatures on clinical documents.
- Check for version control on PHI records (audit trail of changes).
- Verify immutability of finalized clinical records (amendments, not edits).

PERSON OR ENTITY AUTHENTICATION (164.312(d)):

Authentication Strength:
- Check password hashing algorithm: bcrypt/scrypt/argon2 required.
  Flag MD5, SHA-1, SHA-256 without salt/stretching.
- Verify salt is unique per user (not global).
- Check work factor / iteration count (bcrypt cost >= 12).
- Verify MFA implementation for PHI access.
- Check for certificate-based authentication (if applicable).
- Verify OAuth2/OIDC implementation correctness.

Session Management:
- Check session token generation (cryptographically random, sufficient entropy).
- Verify session invalidation on logout (server-side, not just client cookie).
- Check for session fixation prevention.
- Verify concurrent session handling (limit or detect).
- Check cookie flags: Secure, HttpOnly, SameSite.

TRANSMISSION SECURITY (164.312(e)(1)):

Encryption in Transit:
- Verify TLS 1.2+ enforcement on all PHI endpoints.
- Check for HSTS headers.
- Flag any HTTP (non-TLS) endpoints that handle PHI.
- Check TLS configuration: cipher suites, certificate validation.
- Verify internal service-to-service encryption (mTLS or equivalent).

Integrity Controls:
- Check for message authentication (HMAC, digital signatures) on PHI transmissions.
- Verify API request signing or integrity verification.
- Check for replay attack prevention (nonce, timestamp validation).

Network Controls:
- Check for network segmentation configuration (VPC, security groups).
- Verify database is not publicly accessible.
- Check for WAF or API gateway configuration.
- Verify PHI endpoints are not exposed on public networks without auth.

============================================================
PHASE 4: PHI DATA FLOW ANALYSIS
============================================================

Trace PHI through the entire system:

INGESTION:
- How does PHI enter the system? (API, file upload, HL7 feed, FHIR, manual entry)
- Is PHI validated and sanitized at ingestion?
- Is ingestion logged?

PROCESSING:
- Which services/functions process PHI?
- Is PHI ever logged during processing? (flag if so)
- Are temporary copies created? (flag if not cleaned)
- Is PHI passed via message queues? (verify queue encryption)

STORAGE:
- Primary database: encrypted? field-level or full-disk?
- Cache layer: is PHI cached? cache TTL? cache encryption?
- File storage: encrypted? access controlled?
- Backups: encrypted? access controlled? retention policy?

TRANSMISSION:
- Internal: service-to-service, message queue, event bus
- External: API responses, email, fax, file export, HL7/FHIR
- Is all transmission encrypted?

DISPOSAL:
- Record deletion: soft delete or hard delete?
- Data retention policies implemented in code?
- Secure deletion (overwrite, not just delete)?
- Backup data disposal aligned with retention?


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

## HIPAA Security Rule Technical Audit

**Project:** [name]
**Stack:** [detected technologies]
**PHI-Containing Components:** [count] models, [count] services, [count] endpoints
**Date:** [date]

### Safeguard Summary

| Safeguard Category | Section | Status | Critical | High | Medium | Low |
|---|---|---|---|---|---|---|
| Administrative — Security Management | 164.308(a)(1) | [PASS/WARN/FAIL] | N | N | N | N |
| Administrative — Workforce Security | 164.308(a)(3) | [PASS/WARN/FAIL] | N | N | N | N |
| Administrative — Info Access Mgmt | 164.308(a)(4) | [PASS/WARN/FAIL] | N | N | N | N |
| Administrative — Security Awareness | 164.308(a)(5) | [PASS/WARN/FAIL] | N | N | N | N |
| Administrative — Incident Procedures | 164.308(a)(6) | [PASS/WARN/FAIL] | N | N | N | N |
| Administrative — Contingency Plan | 164.308(a)(7) | [PASS/WARN/FAIL] | N | N | N | N |
| Physical — Facility Access | 164.310(a)(1) | [PASS/WARN/FAIL] | N | N | N | N |
| Physical — Workstation Security | 164.310(b)/(c) | [PASS/WARN/FAIL] | N | N | N | N |
| Physical — Device/Media Controls | 164.310(d)(1) | [PASS/WARN/FAIL] | N | N | N | N |
| Technical — Access Control | 164.312(a)(1) | [PASS/WARN/FAIL] | N | N | N | N |
| Technical — Audit Controls | 164.312(b) | [PASS/WARN/FAIL] | N | N | N | N |
| Technical — Integrity | 164.312(c)(1) | [PASS/WARN/FAIL] | N | N | N | N |
| Technical — Authentication | 164.312(d) | [PASS/WARN/FAIL] | N | N | N | N |
| Technical — Transmission Security | 164.312(e)(1) | [PASS/WARN/FAIL] | N | N | N | N |

### PHI Data Flow Map

**Ingestion:** [sources] -> **Processing:** [services] -> **Storage:** [databases/caches] -> **Transmission:** [destinations]
**Disposal:** [retention policy and mechanism]

### Detailed Findings

For each safeguard with WARN or FAIL:

#### [Safeguard — CFR Section]

| # | Severity | File | Line | Requirement | Gap | Remediation |
|---|----------|------|------|-------------|-----|-------------|
| 1 | Critical | path/to/file.ts | 42 | 164.312(a)(2)(iv) | PHI stored unencrypted | Implement AES-256 field-level encryption |

### Encryption Assessment
| Layer | Method | Algorithm | Key Management | Status |
|---|---|---|---|---|
| Database at rest | [TDE/column/app-level/none] | [AES-256/etc.] | [KMS/env/hardcoded] | [OK/FAIL] |
| File storage | [SSE/client-side/none] | [AES-256/etc.] | [KMS/etc.] | [OK/FAIL] |
| In transit | [TLS version] | [cipher suite] | [cert source] | [OK/FAIL] |
| Backups | [encrypted/unencrypted] | [algorithm] | [key source] | [OK/FAIL] |

### Access Control Matrix
| Role | PHI Read | PHI Write | PHI Delete | Admin | Audit View |
|---|---|---|---|---|---|
| [role] | [yes/no] | [yes/no] | [yes/no] | [yes/no] | [yes/no] |

### Risk Summary
- **Critical findings:** N (direct HIPAA violation, breach risk)
- **High findings:** N (significant gap, likely violation under audit)
- **Medium findings:** N (addressable implementation specification gap)
- **Low findings:** N (best practice, defense-in-depth improvement)

### Remediation Roadmap
[Ordered by severity and implementation dependency, with effort estimates]

============================================================
NEXT STEPS
============================================================

After reviewing the audit:
- "Run `/healthcare-compliance` for a broader regulatory audit including Privacy Rule, HITECH, and Cures Act."
- "Run `/encryption` to implement or upgrade encryption controls flagged in this audit."
- "Run `/pentest` to verify exploitability of access control and authentication findings."
- "Run `/secure` for general security hardening beyond HIPAA-specific requirements."
- "Run `/soc2` to assess SOC 2 Type II controls that overlap with HIPAA Security Rule."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /hipaa — {{YYYY-MM-DD}}
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

- Do NOT modify any code -- this is an audit skill, not a remediation skill.
- Do NOT expose actual PHI found in code, config, logs, or test data -- redact and note location only.
- Do NOT provide legal interpretations of HIPAA -- flag ambiguous areas for legal/compliance review.
- Do NOT skip "addressable" implementation specifications -- they still require documented risk decisions.
- Do NOT mark a safeguard as PASS without scanning the codebase for relevant implementation evidence.
- Do NOT assume cloud provider defaults satisfy HIPAA -- verify explicit configuration exists.
- Do NOT treat the absence of PHI-handling code as compliance -- missing controls are findings.
- Do NOT install external scanning tools -- analyze code, configuration, and infrastructure files directly.
- Do NOT conflate required vs addressable specifications without noting the distinction.

---
name: iso27001-sgsi
description: ISO 27001/SGSI — CIA triad, controls, risk assessment.
---

# ISO 27001 / SGSI / CIA Triad

---

## CIA Triad

The three foundational properties of information security. Every security decision must be evaluated against all three.

| Pillar | Definition | Software implications |
|--------|-----------|----------------------|
| **Confidentiality** | Information is accessible only to authorized parties | Encryption at rest and in transit, access control, least privilege, no PII in logs |
| **Integrity** | Information is accurate and has not been tampered with | Input validation, checksums, audit logs, signed tokens, immutable audit trails |
| **Availability** | Systems and data are accessible when needed | Rate limiting, DDoS mitigation, backups, graceful degradation, health checks, SLAs |

When a control improves one pillar, check that it does not degrade another (e.g., aggressive rate limiting improves availability against DDoS but may harm legitimate users — balance required).

---

## SGSI — Information Security Management System

An SGSI (Sistema de Gestão de Segurança da Informação / ISMS) is the framework of policies, processes, and controls that an organization uses to manage information security risk systematically.

**Core cycle (Plan–Do–Check–Act):**

| Phase | What happens |
|-------|-------------|
| **Plan** | Define security scope, conduct risk assessment, set objectives and controls |
| **Do** | Implement selected controls (technical, operational, organizational) |
| **Check** | Monitor, audit, measure effectiveness of controls |
| **Act** | Review findings, apply corrective actions, improve continuously |

**For software teams, this translates to:**
- Threat modeling before building features that handle sensitive data
- Risk register maintained and reviewed each sprint or quarter
- Security review gate before production deployments (enforce via CI/CD)
- Incident response plan documented and tested
- Security training for all engineers handling customer data

---

## ISO 27001 — Software-Relevant Controls (Annex A)

Focus on the controls most directly actionable by a development team:

### A.8 — Asset Management
- Classify data by sensitivity (public / internal / confidential / restricted)
- Document which services process which data classifications
- Define retention and disposal policy for each classification

### A.9 — Access Control
- Principle of least privilege: roles grant minimum permissions to accomplish the task
- Privileged access (admin, prod DB) requires MFA + audit logging
- Access rights reviewed quarterly; revoked immediately on offboarding
- No shared credentials — every system actor has a unique identity

### A.10 — Cryptography
- Encryption in transit: TLS 1.2 minimum; TLS 1.3 preferred
- Encryption at rest: AES-256 for confidential and restricted data
- Key management: keys stored in a secret manager (AWS KMS, HashiCorp Vault, GCP KMS); never hardcoded
- Password hashing: bcrypt (cost ≥ 12), Argon2id, or scrypt — never MD5, SHA-1, or unsalted SHA-2

### A.12 — Operations Security
- Change management: all production changes go through a review process (PRs, approvals)
- Malware protection: dependency scanning, container image scanning in CI
- Logging and monitoring: audit logs for authentication, authorization decisions, data access, and admin actions
- Log retention: minimum 90 days hot, 1 year cold (adjust to regulatory requirements)

### A.13 — Communications Security
- Network segmentation: databases not directly reachable from the internet
- API security: authentication required on all endpoints; no unauthenticated data exposure
- Data transfer: PII/sensitive data transferred only over encrypted channels; no email attachments for sensitive data

### A.14 — System Acquisition, Development, and Maintenance
- Security requirements defined before development starts (threat model)
- Secure coding standards enforced (OWASP Top 10, this skill set)
- Security testing in CI: SAST, dependency audit, secret scanning
- Separation of environments: dev/staging/production strictly isolated; no production data in dev/staging

### A.16 — Incident Management
- Incident response plan: defined roles, communication channels, escalation path
- Security incidents logged and post-mortemed
- Breach notification: know your legal obligation (LGPD: 72h to ANPD; GDPR: 72h to DPA)

### A.18 — Compliance
- Legal requirements identified: LGPD, GDPR, PCI-DSS, HIPAA — whichever apply to the project
- Privacy by design: collect minimum data, document purpose, implement erasure
- Regular compliance audits against applicable regulations

---

## Risk Assessment Checklist (per feature / per sprint)

Ask these before building any feature that handles user data or system access:

- [ ] What data does this feature collect or process? What is its classification?
- [ ] Who can access this data? Is access scoped to the minimum necessary?
- [ ] What happens if this data is exposed? (Confidentiality impact)
- [ ] What happens if this data is corrupted or tampered with? (Integrity impact)
- [ ] What happens if this feature is unavailable? (Availability impact)
- [ ] Are there regulatory obligations attached to this data?
- [ ] Are audit logs generated for sensitive actions in this feature?

---

## Audit Log Requirements

Every audit log entry must capture:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601, UTC |
| `actor_id` | Authenticated user/service identity |
| `action` | What was done (`order.created`, `user.login`, `admin.permission_granted`) |
| `resource_type` | Object type affected |
| `resource_id` | Object ID affected |
| `outcome` | `success` or `failure` |
| `ip_address` | Client IP (where applicable) |
| `user_agent` | Client context (where applicable) |

Audit logs must be:
- Append-only (no update or delete)
- Stored separately from application logs
- Tamper-evident (hash chaining or write to immutable storage)
- Retained per regulatory requirement (minimum 1 year)

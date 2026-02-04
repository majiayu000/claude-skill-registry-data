---
name: healthtech-hipaa
category: compliance
difficulty: advanced
compliance_standards:
- HIPAA
- HITECH
- HL7-v2
- FHIR-R4
version: 1.0.0
last_updated: 2025-10-17
description: HIPAA establishes national standards for protecting patient health information
  (PHI). Enforced by HHS Office for Civil Rights.
---


# HealthTech HIPAA Compliance Skill

> **LEGAL DISCLAIMER**: This document provides educational guidance on HIPAA compliance requirements and is not legal advice. Healthcare organizations must consult with qualified healthcare compliance attorneys and privacy officers to ensure full regulatory compliance. HIPAA regulations are complex and fact-specific; implementation must be tailored to your organization's specific circumstances.

## Level 1: Quick Start (150 tokens)

**HIPAA** establishes national standards for protecting patient health information (PHI). Enforced by HHS Office for Civil Rights.

**Key Rules:**

- **Privacy Rule**: PHI use/disclosure standards, patient rights (access, amendment, accounting)
- **Security Rule**: ePHI protection via Administrative, Physical, and Technical safeguards
- **Breach Notification**: 60-day notification requirement for unsecured PHI breaches

**Core Requirements:**

- Encrypt PHI (AES-256 at rest, TLS 1.2+ in transit)
- Unique user IDs, MFA, role-based access control
- Audit logging (6-year retention)
- Business Associate Agreements before PHI sharing
- Annual risk assessments and workforce training

**Penalties:** $100-$50,000 per violation (up to $1.5M annually per category)

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide (~1200 tokens)

### Implementation Overview

HIPAA compliance requires a systematic approach across three main pillars:

**Privacy Rule Implementation**: Establish policies for PHI use/disclosure, implement individual rights (access, amendment, accounting), deploy Notice of Privacy Practices, and enforce minimum necessary standard through role-based access controls.

**Security Rule Implementation**: Conduct annual risk assessments, designate Security Official, implement administrative safeguards (workforce security, training, incident response, contingency planning), deploy physical safeguards (facility access, workstation security, device controls), and enforce technical safeguards (access control, encryption, audit logging, authentication, transmission security).

**Business Associate Management**: Identify all vendors with PHI access, execute Business Associate Agreements before PHI disclosure, monitor BA compliance, and maintain BA tracking logs.

### Quick Implementation Roadmap

**Phase 1: Foundation (Weeks 1-4)**

1. Designate Privacy and Security Officers
2. Conduct initial risk assessment (identify all ePHI systems)
3. Draft core policies (Privacy, Security, Breach Notification, Sanctions)
4. Create PHI inventory and data flow maps

**Phase 2: Technical Controls (Weeks 5-12)**

1. Implement encryption (AES-256 at rest, TLS 1.2+ in transit)
2. Deploy access controls (unique user IDs, RBAC, MFA for remote access)
3. Configure audit logging (all PHI access, authentication, modifications)
4. Establish backup procedures (daily incremental, weekly full, quarterly restore tests)

**Phase 3: Administrative & Physical (Weeks 13-20)**

1. Execute BAAs with all vendors before PHI sharing
2. Conduct workforce training (initial + annual refresher)
3. Implement physical security (badge access, visitor logs, workstation controls)
4. Deploy incident response procedures (detection, containment, notification)

**Phase 4: Testing & Validation (Weeks 21-24)**

1. Vulnerability scanning and penetration testing
2. Contingency plan testing (backup restore, emergency mode)
3. Access review and audit log analysis
4. Mock breach response exercise

### Critical Security Controls

**Encryption Requirements:**

- Data at rest: AES-256 for all ePHI storage (databases, file systems, backups)
- Data in transit: TLS 1.2+ mandatory (TLS 1.3 preferred)
- Mobile devices: Full-disk encryption (BitLocker, FileVault)
- Email: S/MIME or encrypted portal (no unencrypted PHI via email)
- Key management: HSM or cloud KMS with annual key rotation

**Access Control Essentials:**

- Unique user IDs (no shared accounts except emergency "break glass")
- Multi-factor authentication for remote ePHI access
- Automatic logoff (5-10 min clinical, 15 min administrative)
- Role-based access limiting PHI to minimum necessary
- Quarterly access reviews with termination checklists

**Audit Logging Must-Haves:**

- Log all PHI access (views, searches, exports, API calls)
- 6-year retention minimum
- Tamper-resistant centralized storage
- Weekly review for high-risk systems
- SIEM rules for anomalies (after-hours access, bulk downloads, terminated users)

### Breach Notification Essentials

**Breach Definition**: Acquisition, access, use, or disclosure of unsecured PHI compromising security/privacy.

**Notification Timelines:**

- Individuals: Within 60 days of breach discovery
- OCR: Within 60 days if ≥500 individuals affected
- Media: Within 60 days if ≥500 residents of state/jurisdiction
- Business Associates: Must notify covered entity within 60 days

**Risk Assessment (4 factors):**

1. Nature and extent of PHI (sensitivity of identifiers)
2. Who gained unauthorized access (insider vs. external)
3. Was PHI actually acquired/viewed (evidence-based)
4. Mitigation factors (encryption, safeguards)

**HITECH Penalty Tiers (per violation):**

- Tier 1 (Unknowing): $100-$50,000
- Tier 2 (Reasonable Cause): $1,000-$50,000
- Tier 3 (Willful Neglect, Corrected): $10,000-$50,000
- Tier 4 (Willful Neglect, Not Corrected): $50,000 minimum
- Annual maximum: $1.5 million per violation category

### Interoperability Standards

**HL7 v2 Security**: Encrypt message transmission with TLS over MLLP, implement certificate-based authentication for interface connections, log all message transmissions, and validate message schemas before processing.

**FHIR R4 Compliance**: Implement SMART on FHIR (OAuth 2.0 + OpenID Connect), enforce TLS 1.2+ for all API calls, use OAuth scopes for minimum necessary access control, log all FHIR API requests, deploy rate limiting, and execute BAAs with app developers.

**For detailed implementation guidance including:**

- Complete HIPAA Privacy Rule specifications (permitted uses, individual rights, minimum necessary)
- All 9 Administrative Safeguards with implementation frameworks
- All 4 Physical Safeguards with facility security controls
- All 5 Technical Safeguards with configuration details
- HL7 v2 message types and security implementations

*See REFERENCE.md for complete list.*

**See the comprehensive implementation guide**: [HIPAA Implementation Guide](/home/william/git/standards/docs/compliance/healthtech/implementation-guide.md)

---

## Level 3: Mastery (External References)

**Official Resources:** [HHS OCR](https://www.hhs.gov/ocr/privacy/), [HIPAA Security](https://www.hhs.gov/hipaa/for-professionals/security/), [NIST SP 800-66](https://csrc.nist.gov/publications/detail/sp/800-66/rev-2/final), [HL7](https://www.hl7.org/), [FHIR R4](https://hl7.org/fhir/R4/)

**Related Skills:** `security/OWASP`, `security/NIST-CSF`, `governance/SOC2`, `data-privacy/GDPR`

---

## Updates and Maintenance

**Last Updated**: 2025-10-17

**Change Log:**

- v1.0.0 (2025-10-17): Initial comprehensive HIPAA compliance skill with HITECH Act updates, HL7/FHIR standards integration, and bundled resources

**Regulatory Monitoring:**
HIPAA regulations are subject to updates and guidance changes. Monitor:

- HHS OCR website for new guidance and enforcement actions
- Federal Register for proposed rule changes
- OCR Cybersecurity Newsletter (monthly)

**Skill Maintenance:**

- Review annually for regulatory updates
- Update penalty amounts per inflation adjustments (published annually)
- Incorporate new OCR guidance and audit protocols
- Update technical standards (TLS versions, encryption standards) per evolving best practices

## Examples

### Basic Usage

```python
// TODO: Add basic example for healthtech
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for healthtech
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how healthtech
// works with other systems and services
```

See `examples/healthtech/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring healthtech functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for healthtech
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

**Remember**: HIPAA compliance is an ongoing process, not a one-time project. Establish continuous monitoring, regular training, and periodic assessments to maintain compliance posture.

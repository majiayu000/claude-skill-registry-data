---
name: fintech-compliance
category: compliance
difficulty: advanced
compliance_standards: [PCI-DSS-v4.0.1, SOC2-Type-II]
description: Payment card security, SOC2 compliance, and financial services regulatory requirements
prerequisites: [security-fundamentals, api-security]
related_skills: [cloud-security, audit-logging]
version: 1.0.0
---

# FinTech Compliance Skill

## Overview

Master payment card industry security standards (PCI-DSS v4.0.1), SOC2 Type II compliance, and financial services regulatory requirements for secure payment processing and data protection.

---

## Level 1: Quick Reference (~800-1000 tokens)

### PCI-DSS 12 Requirements Overview

**Build and Maintain Secure Network and Systems**

1. Install and maintain network security controls
2. Apply secure configurations to all system components

**Protect Account Data**
3. Protect stored account data
4. Protect cardholder data with strong cryptography during transmission over open, public networks

**Maintain Vulnerability Management Program**
5. Protect all systems and networks from malicious software
6. Develop and maintain secure systems and software

**Implement Strong Access Control Measures**
7. Restrict access to system components and cardholder data by business need to know
8. Identify users and authenticate access to system components
9. Restrict physical access to cardholder data

**Regularly Monitor and Test Networks**
10. Log and monitor all access to system components and cardholder data
11. Test security of systems and networks regularly

**Maintain Information Security Policy**
12. Support information security with organizational policies and programs

### SOC2 Trust Service Criteria

**Security (Common Criteria)**

- Access controls (logical and physical)
- System operations and change management
- Risk mitigation

**Availability**

- System availability commitments
- Monitoring and incident response

**Confidentiality**

- Data classification and handling
- Confidential information protection

### Merchant Levels

| Level | Annual Transactions | Requirements |
|-------|---------------------|--------------|
| 1     | >6M                 | Annual onsite audit, quarterly network scans |
| 2     | 1M-6M               | Annual SAQ, quarterly network scans |
| 3     | 20K-1M (e-commerce) | Annual SAQ, quarterly network scans |
| 4     | <20K (e-commerce) or <1M (other) | Annual SAQ, quarterly network scans (recommended) |

### Essential Checklist

- [ ] **CDE Segmentation**: Isolate cardholder data environment from other networks
- [ ] **Encryption**: All cardholder data encrypted at rest (AES-256) and in transit (TLS 1.2+)
- [ ] **Tokenization**: Replace PANs with tokens for non-payment operations
- [ ] **Access Control**: Unique user IDs, MFA for all CDE access, least privilege
- [ ] **Logging**: Centralized logging with 90+ day retention, automated monitoring
- [ ] **Vulnerability Management**: Quarterly scans, patch management, secure SDLC
- [ ] **Incident Response**: Documented plan, tested annually, 24/7 monitoring
- [ ] **Physical Security**: Restricted access to data centers, visitor logs, camera surveillance

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide (~4500-5500 tokens)

### PCI-DSS v4.0.1 Detailed Requirements

#### PCI-DSS v4.0.1 Requirements Summary

> **📚 Complete Requirements**: See [REFERENCE.md](./REFERENCE.md) for detailed sub-requirements, implementation guidance, and compliance validation procedures.

**Requirements 1-12 Overview:**

1. **Network Security Controls**: Firewalls, NSCs, CDE isolation
2. **Secure Configurations**: Vendor defaults changed, unnecessary services disabled
3. **Protect Stored Data**: Encryption at rest, minimize data retention, never store SAD
4. **Protect Data in Transit**: TLS 1.2+, strong cryptography for all PAN transmission
5. **Malware Protection**: Anti-malware on all systems, kept current, monitored
6. **Secure Development**: Threat modeling, secure coding, vulnerability management
7. **Access Control**: Least privilege, unique IDs, business need-to-know
8. **Identification & Authentication**: MFA for CDE access, strong passwords, credential management
9. **Physical Security**: Restricted facility access, badge systems, visitor logs
10. **Logging & Monitoring**: Audit trails, centralized logging, 90+ day retention
11. **Security Testing**: Quarterly vulnerability scans, annual penetration testing
12. **Security Policy**: Documented policies, awareness training, incident response

*Each requirement contains multiple sub-requirements - see REFERENCE.md for complete compliance checklist.*

### Cardholder Data Environment (CDE) Segmentation

**Network Segmentation Strategy**


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


**Key Segmentation Controls:**

1. Firewall rules whitelist only required protocols (HTTPS, database ports)
2. Network ACLs deny by default, permit by exception
3. VLANs separate CDE from other networks
4. Jump boxes/bastion hosts for administrative access
5. No direct internet access from CDE
6. Annual penetration testing validates segmentation

### Payment Processing Security

**Tokenization Implementation**


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


**Encryption Requirements**

| Data State | Requirement | Algorithm | Key Length |
|------------|-------------|-----------|------------|
| At Rest    | PAN encrypted | AES | 256-bit minimum |
| In Transit | TLS 1.2+    | ECDHE-RSA-AES256-GCM-SHA384 | 2048-bit RSA minimum |
| Backups    | Encrypted   | AES-256 | 256-bit |
| Key Storage| Encrypted KEK | AES-256 | 256-bit |

**Key Management Lifecycle**

1. **Generation**: FIPS 140-2 Level 2+ HSM
2. **Distribution**: Encrypted channels, split knowledge
3. **Storage**: Separate from encrypted data, access logged
4. **Rotation**: Annual minimum, or upon compromise
5. **Destruction**: Secure deletion per NIST SP 800-88

### SOC2 Type II Compliance

**Trust Service Criteria Mapping**

**CC1: Control Environment**

- Board oversight of security and privacy
- Management philosophy and operating style
- Organizational structure and assignment of authority
- Commitment to competence
- Human resource policies

**CC2: Communication and Information**

- Internal communication channels
- External communication channels
- Information quality
- Management and board reporting

**CC3: Risk Assessment**

- Risk identification and assessment
- Fraud risk assessment
- Risk response and monitoring

**CC4: Monitoring Activities**

- Ongoing and separate evaluations
- Deficiency reporting and remediation

**CC5: Control Activities (Logical and Physical Access)**

- Selection and development of control activities
- Technology controls
- Policies and procedures deployment

**CC6: Logical and Physical Access Controls**

- Prior to issuing credentials, entity registers and authorizes new users
- Credentials and access are removed when access is no longer required
- Entity reviews credentials and access rights
- Physical access restricted to authorized personnel
- Logical access restricted based on least privilege

**CC7: System Operations**

- Change management procedures
- Configuration management
- Incident management
- Backup and recovery procedures

**CC8: Change Management**

- Change authorization and approval
- Testing procedures
- Deployment procedures
- Documentation requirements

**CC9: Risk Mitigation**

- Vulnerability identification and assessment
- Threat protection mechanisms
- Security patch management
- Malware detection and prevention

**A1: Availability**

- Monitoring system capacity and performance
- Environmental protections (fire, flood, temperature)
- Redundancy and failover procedures
- Incident response for availability incidents

**C1: Confidentiality**

- Confidential information identified and classified
- Confidential information encrypted at rest and in transit
- Access to confidential information restricted
- Confidential information disposal procedures

### Audit Readiness and Evidence Collection

**Evidence Requirements by Control Category**

| Control Category | Evidence Types | Collection Frequency |
|------------------|----------------|----------------------|
| Access Control | User provisioning logs, access reviews, MFA configs | Quarterly |
| Change Management | Change tickets, approval records, test results | Per change |
| Encryption | Cipher configurations, key rotation logs, TLS scans | Monthly |
| Logging | Log retention verification, SIEM configurations | Monthly |
| Vulnerability Management | Scan reports, remediation tickets, patch schedules | Quarterly |
| Incident Response | Incident tickets, postmortem reports, tabletop exercises | Per incident |
| Physical Security | Badge logs, visitor logs, camera footage samples | Quarterly |
| Vendor Management | SOC2 reports, SLAs, due diligence assessments | Annually |

**Automated Evidence Collection**


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


### Compliance Automation

**Continuous Compliance Monitoring Architecture**


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


**Sample Compliance Rules (AWS Config)**


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


### Incident Response for Payment Security

**Critical Incident Types**

1. **Suspected PAN Exposure**
   - Immediate containment: Isolate affected systems
   - Forensic preservation: Snapshot VMs, preserve logs
   - Notification: Payment brands within 72 hours
   - PFI (Payment Forensic Investigator) engagement

2. **CDE Breach**
   - Activate IR team 24/7
   - Preserve evidence (RAM dumps, disk images)
   - Engage legal counsel
   - Notify acquiring bank and card brands
   - Retain PFI for investigation

3. **Authentication Bypass**
   - Immediately revoke compromised credentials
   - Force password resets for affected accounts
   - Review and enhance MFA controls
   - Audit access logs for unauthorized activity

4. **Malware in CDE**
   - Isolate infected systems (network segmentation)
   - Deploy anti-malware tools
   - Scan all CDE components
   - Rebuild compromised systems from known-good images
   - Enhance monitoring for persistence mechanisms

**Compliance Reporting Timeline**

| Incident Type | Notification Deadline | Recipient |
|---------------|----------------------|-----------|
| PAN compromise | 72 hours | Payment brands, acquirer |
| CDE breach | 72 hours | Payment brands, PFI |
| SOC2 control failure | Next report period | Auditor, customers |
| GDPR breach (EU) | 72 hours | Data Protection Authority |
| State breach laws (US) | 30-90 days (varies) | State AG, affected individuals |

---

## Level 3: Deep Dive Resources

### Bundled Resources

1. **`resources/pci-dss-checklist.md`** - Complete 78-sub-requirement checklist with validation procedures
2. **`templates/soc2-control-mappings.yaml`** - SOC2 TSC to implementation control mappings
3. **`templates/tokenization-implementation.py`** - Production-ready Stripe/Braintree tokenization
4. **`templates/network-segmentation.yaml`** - CDE network architecture and firewall rules
5. **`scripts/audit-evidence-collector.sh`** - Automated evidence collection for quarterly audits
6. **`templates/compliance-dashboard.json`** - Grafana dashboard for real-time compliance monitoring

### Official Standards References

- **PCI DSS v4.0.1**: <https://www.pcisecuritystandards.org/document_library>
- **PCI SAQ**: Self-Assessment Questionnaires for merchant levels
- **PA-DSS**: Payment Application Data Security Standard
- **SOC2**: <https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html>
- **NIST Cybersecurity Framework**: <https://www.nist.gov/cyberframework>

### Industry Resources

- **PCI SSC**: <https://www.pcisecuritystandards.org>
- **Cloud Security Alliance (CSA)**: <https://cloudsecurityalliance.org>
- **ISACA**: <https://www.isaca.org> (CISA, CRISC certifications)
- **SANS Institute**: Payment card security courses

### Complementary Skills

- **security-fundamentals**: Foundational security principles
- **api-security**: Secure API design for payment endpoints
- **cloud-security**: Cloud-specific compliance (AWS, Azure, GCP)
- **audit-logging**: Centralized logging and SIEM implementation

---

## Quick Win: 30-Minute Compliance Assessment

```bash
# Run automated compliance scan
git clone https://github.com/prowler-cloud/prowler
cd prowler
./prowler aws --compliance pci_dss_v4.0.1

# Check TLS configurations
nmap --script ssl-enum-ciphers -p 443 payment-api.example.com

# Verify log retention
aws logs describe-log-groups | jq '.logGroups[] | select(.retentionInDays < 90)'

# Review IAM MFA enforcement
aws iam get-account-summary | jq '.SummaryMap | {MFADevices, AccountMFAEnabled}'

# Scan for exposed secrets
trufflehog git https://github.com/yourorg/payment-service --json
```

**Expected Outcomes:**

- PCI compliance posture report (automated scan)
- TLS cipher suite compliance verification
- Log retention gap analysis
- MFA enforcement status
- Secret exposure detection

## Best Practices

- Maintain PCI DSS compliance through quarterly scans and annual audits
- Implement defense-in-depth with multiple security layers
- Automate compliance evidence collection for audit readiness
- Regularly test incident response procedures
- Keep security policies updated and accessible to all personnel
- Conduct ongoing security awareness training
- Monitor for emerging threats and regulatory changes

---

*Version: 1.0.0*
*Last Updated: 2025-10-17*
*Compliance Standards: PCI-DSS v4.0.1, SOC2 Type II*

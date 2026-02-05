---
name: security-operations
description: Security Operations Center (SOC) practices, incident response, SIEM management, and threat hunting following NIST 800-61
---

# Security Operations

## Level 1: Quick Reference

### Incident Response Lifecycle (NIST 800-61 Rev 2)

```
1. PREPARATION       - Policies, tools, training, communication plans
2. DETECTION         - SIEM alerts, log analysis, threat intelligence
3. CONTAINMENT       - Isolate, remove threat, restore operations
4. POST-INCIDENT     - Lessons learned, documentation, improvement
```

### SOC Tiers

| Tier | Role | Responsibilities |
|------|------|------------------|
| **T1** | Alert Triage | Monitor SIEM, validate alerts, categorize, escalate |
| **T2** | Incident Response | Investigation, forensics, containment |
| **T3** | Threat Hunting | Proactive hunting, APT detection, automation |

### Incident Severity Classification

| Severity | Impact | Response Time | Escalation |
|----------|--------|---------------|------------|
| **Critical** | Business-critical compromised, active exfiltration | <15 min | CISO, Legal |
| **High** | Multiple systems, potential breach | <1 hour | Tier 3, Management |
| **Medium** | Single system, contained threat | <4 hours | Tier 2 |
| **Low** | Failed attack, no impact | <24 hours | Tier 1 |

### Essential SIEM Queries

**Failed Login Attempts (Splunk):**

```spl
index=security sourcetype=auth action=failure
| stats count by user, src_ip
| where count > 5
```

**Privilege Escalation (Azure Sentinel):**

```kql
SecurityEvent
| where EventID == 4672
| where AccountType == "User"
| summarize count() by Account, Computer
```

### Security Metrics Targets

- **MTTD** (Mean Time To Detect): <1 hour for critical
- **MTTR** (Mean Time To Respond): <4 hours for critical
- **False Positive Rate**: <10%

---

## Level 2: Implementation Guide

> **Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

### SOC Team Structure

**Core Roles:**

- **SOC Manager**: Strategic planning, metrics reporting, policy development
- **Tier 1 Analyst**: 24/7 SIEM monitoring, alert validation (NIST SI-4)
- **Tier 2 Analyst**: Deep investigation, forensics, containment (NIST IR-4, IR-6)
- **Tier 3 Analyst**: Threat hunting, APT detection, tool development (NIST IR-5, AU-6)
- **Incident Commander**: Major incident coordination, stakeholder communication

**Essential Tools:**

- **SIEM**: Splunk ES, Elastic Security, Azure Sentinel, QRadar
- **EDR**: CrowdStrike, Microsoft Defender, Carbon Black
- **Threat Intel**: MISP, ThreatConnect, STIX/TAXII feeds
- **Forensics**: Volatility (memory), Autopsy (disk), Wireshark (network)

### Incident Response Phases

#### Phase 1: Preparation (IR-4)

- IR team structure with roles and on-call rotation
- Communication plan (internal, external, regulatory)
- Forensic toolkit (jump bag with evidence collection tools)
- Quarterly tabletop exercises and annual red team tests

*See [REFERENCE.md](./REFERENCE.md#example-0) for team structure template.*

#### Phase 2: Detection & Analysis (SI-4, AU-6)

**Alert Triage Process:**

1. **Initial Validation (5 min)**: True/false positive, OSINT lookup, asset criticality
2. **Scoping (15-30 min)**: Timeline, affected systems, data at risk, persistence
3. **Categorization**: Incident type, severity, confidence level

**Detection Source Priorities:**

- **High Fidelity**: EDR behavioral alerts, IDS signature matches, threat intel IOC hits
- **Medium Fidelity**: UEBA anomaly detection, DLP violations
- **Low Fidelity**: Generic firewall denies, vulnerability scanner findings

*See [REFERENCE.md](./REFERENCE.md#example-1) for detection source matrix.*

#### Phase 3: Containment & Eradication (IR-4)

**Short-Term Containment (<15 min):**

- Isolate host (EDR quarantine, VLAN switch)
- Block malicious IPs/domains at firewall
- Disable compromised accounts
- Preserve evidence (memory dump, disk image)

**Long-Term Containment (1-4 hours):**

- Implement network segmentation
- Apply emergency patches
- Enhanced monitoring on related systems

**Eradication Checklist:**

- Remove malware persistence (scheduled tasks, services, registry)
- Reset compromised credentials
- Patch exploited vulnerabilities

*See [REFERENCE.md](./REFERENCE.md#example-5) for isolation commands.*

#### Phase 4: Recovery & Post-Incident (IR-5)

**Recovery Steps:**

1. Rebuild from known-good backup or gold image
2. Force password reset for affected accounts
3. Deploy additional sensors on recovered systems
4. Create custom SIEM alerts for re-infection indicators

**Post-Incident Review (within 2 weeks):**

- Timeline of events
- What went well / needs improvement
- Action items with owners and due dates
- Evidence retention (1 year minimum, legal hold: 7+ years)

*See [REFERENCE.md](./REFERENCE.md#example-7) for post-incident report template.*

### SIEM Configuration

**Critical Log Sources:**

- Authentication (AD, VPN, SSO)
- Network (firewalls, proxies, DNS)
- Endpoints (EDR, AV, Windows/Linux logs)
- Cloud (CloudTrail, Azure Activity, GCP Audit)
- Applications (web servers, databases, email gateways)

**Correlation Rules to Implement:**

1. Brute force detection (failed logins followed by success)
2. Data exfiltration (large uploads to external destinations)
3. Privilege escalation (user added to admin groups)
4. Lateral movement (SMB access patterns)
5. Beaconing detection (consistent connection intervals)

*See [REFERENCE.md](./REFERENCE.md#example-8) for log source configuration.*

### Threat Hunting

**Hypothesis-Driven Process:**

1. **Formulate**: "Attackers using stolen credentials for file share access"
2. **Define Success**: Unauthorized access outside business hours
3. **Collect Data**: SMB Event 5140, user access patterns
4. **Analyze**: Cross-reference with UEBA baseline
5. **Document**: Create IOCs, update SIEM alerts

**Data-Driven Techniques:**

- Stack counting for rare process execution
- Beaconing detection via connection interval analysis
- Anomaly detection in network traffic patterns

*See [REFERENCE.md](./REFERENCE.md#example-15) for beaconing detection script.*

### Incident Response Playbooks

#### Phishing Response

1. **Contain**: Quarantine email, block sender, disable compromised accounts
2. **Analyze**: Extract headers, sandbox attachments, check for payload delivery
3. **Eradicate**: Remove malware, reset passwords
4. **Recover**: Restore files, re-enable accounts
5. **Improve**: Update phishing training, add IOCs to threat intel

#### Ransomware Response

1. **Contain**: Isolate immediately, identify variant, preserve memory
2. **Assess**: Count encrypted systems, identify affected data, verify backups
3. **Eradicate**: Do NOT pay ransom, wipe systems
4. **Recover**: Restore from backups, rebuild from gold image
5. **Improve**: Review backup strategy, implement application whitelisting

#### Data Breach Response (IR-6)

1. **Contain**: Revoke credentials, block attacker IPs
2. **Scope**: What data accessed, how many records, timeline
3. **Notify**: Legal counsel immediately, then regulators per requirements:
   - GDPR: 72 hours
   - HIPAA: 60 days
   - CCPA: If >500 CA residents
4. **Communicate**: Draft notifications (legal review required), offer credit monitoring
5. **Remediate**: Fix vulnerability, implement additional controls, third-party audit

### Digital Forensics Quick Reference

**Memory Capture:**

```bash
# Linux (LiME)
sudo insmod lime-$(uname -r).ko "path=/tmp/memory.lime format=lime"

# Windows (WinPmem)
.\winpmem.exe memory.raw
```

**Disk Imaging:**

```bash
# Create forensic image
sudo dd if=/dev/sda of=/mnt/evidence/disk.img bs=4M conv=noerror,sync
sha256sum /mnt/evidence/disk.img > disk.img.sha256
```

*See [REFERENCE.md](./REFERENCE.md#example-18) for complete forensics procedures.*

### Security Operations Best Practices

**Efficiency Tips:**

1. **Automate Tier 1**: SOAR for common playbooks, auto-enrich with threat intel
2. **Reduce Alert Fatigue**: Tune rules quarterly, use risk-based alerting
3. **Continuous Improvement**: Post-incident reviews, track false positive sources
4. **Training**: GCIH, GCFA, hands-on labs (TryHackMe, CyberDefenders)

**Common Pitfalls:**

- Alert overload from untuned rules
- Inadequate documentation (every incident needs a ticket)
- Poor stakeholder communication
- Untested backup restore processes

---

## Level 3: Deep Dive Resources

### Bundled Templates

1. **`templates/incident-response-playbook.md`** - Complete IR playbooks with NIST mappings
2. **`templates/siem-queries.md`** - 50+ production SIEM queries by MITRE ATT&CK
3. **`scripts/forensics-collection.sh`** - Automated evidence collection
4. **`templates/post-incident-report.md`** - Root cause analysis template
5. **`templates/security-metrics-dashboard.json`** - Grafana dashboard
6. **`resources/nist-ir-controls.md`** - NIST 800-61/800-53 mapping

### Certifications

- **GCIH**: GIAC Certified Incident Handler
- **GCFA**: GIAC Certified Forensic Analyst
- **GCIA**: GIAC Certified Intrusion Analyst
- **OSCP**: Offensive Security (attacker mindset)

### Key References

- [NIST 800-61 Rev 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) - Incident Handling Guide
- [NIST 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) - IR Control Family
- [MITRE ATT&CK](https://attack.mitre.org) - Adversary tactics and techniques

### Open-Source Tools

- **SIEM**: Wazuh, Elastic Security, Graylog
- **Threat Intel**: MISP, AlienVault OTX
- **Forensics**: Volatility, Autopsy, Wireshark

---

## Summary

**Key Takeaways:**

- SOC operates in three tiers with escalating expertise
- Incident response follows four phases: Prepare, Detect, Contain, Review
- SIEM correlation rules detect common attack patterns
- Threat hunting proactively identifies undetected threats
- Document everything and conduct post-incident reviews

**Validation Exercise:**

1. Deploy Wazuh SIEM (Docker)
2. Forward logs from 3 systems
3. Create 5 custom correlation rules
4. Simulate an incident
5. Respond using IR playbook
6. Write post-incident report

**Related Skills:**

- [Security Fundamentals](../security-fundamentals/SKILL.md)
- [Network Security](../network-security/SKILL.md)
- [Cloud Security](../cloud-security/SKILL.md)

**Compliance Mapping:** NIST IR-4, IR-5, IR-6, SI-4, AU-6 | ISO 27001 A.16.1 | PCI-DSS 12.10 | SOC 2 CC7.3

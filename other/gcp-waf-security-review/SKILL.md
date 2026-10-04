---
name: gcp-waf-security-review
description: "Evaluate GCP workload security posture against the Google Cloud Well-Architected Framework security pillar — covering zero trust, shift-left security, preemptive cyber defense, AI security governance, and regulatory compliance. Use when assessing architecture security requirements, designing security controls, or auditing a GCP workload against WAF security recommendations."
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-09"
  category: security
---

# GCP WAF Security Review

## Purpose

Evaluate GCP workload security posture against the Google Cloud Well-Architected Framework (WAF) security pillar. This skill supports confidentiality, integrity, compliance, and privacy requirements for workloads running on GCP.

## When to use

Use this skill for:

- Assessing architecture security requirements against WAF recommendations
- Designing security controls and control gaps analysis
- Auditing a GCP workload against the seven WAF security principles
- Evaluating zero trust maturity, shift-left practices, and preemptive defense coverage
- Reviewing AI governance and regulatory compliance posture

## WAF Security Pillar Overview

The GCP Well-Architected Framework security pillar provides guidance across seven core principles. Together they enforce confidentiality (data is accessible only to authorized principals), integrity (data and systems are not tampered with), compliance (workloads meet regulatory obligations), and privacy (personal data is protected throughout its lifecycle).

## Core Principles

### 1. Implement Security by Design
Ground every architecture decision in a security-first posture. Embed security requirements from the earliest design phase rather than retrofitting controls after the fact.
- Reference: https://cloud.google.com/architecture/framework/security/implement-security-by-design

### 2. Implement Zero Trust
Treat every request as untrusted by default regardless of network origin. Verify identity, device health, and context before granting access, and enforce least-privilege access to all resources.
- Reference: https://cloud.google.com/architecture/framework/security/implement-zero-trust

### 3. Implement Shift-Left Security
Integrate security checks, policy enforcement, and vulnerability scanning into CI/CD pipelines and developer workflows so defects are caught before reaching production.
- Reference: https://cloud.google.com/architecture/framework/security/implement-shift-left-security

### 4. Implement Preemptive Cyber Defense
Actively detect, hunt, and respond to threats before they materialize into incidents. Use threat intelligence, behavioral analytics, and automated response to shorten mean time to detect and respond.
- Reference: https://cloud.google.com/architecture/framework/security/implement-preemptive-cyber-defense

### 5. Use AI Securely and Responsibly
Apply security controls specifically to AI model pipelines, training data, inference endpoints, and model outputs. Address AI-specific attack surfaces including prompt injection, model inversion, and supply chain risks.
- Reference: https://cloud.google.com/architecture/framework/security/use-ai-securely-and-responsibly

### 6. Use AI for Security
Leverage AI and machine learning capabilities to enhance security operations — anomaly detection, alert triage, threat hunting, and automated response at scale.
- Reference: https://cloud.google.com/architecture/framework/security/use-ai-for-security

### 7. Meet Regulatory, Compliance, and Privacy Needs
Identify applicable regulatory requirements (GDPR, HIPAA, PCI-DSS, FedRAMP, SOC 2, etc.), map controls to obligations, and maintain continuous evidence for audits.
- Reference: https://cloud.google.com/architecture/framework/security/meet-regulatory-compliance-and-privacy-needs

## Relevant GCP Products

- **Identity & Access:** Cloud IAM, Identity-Aware Proxy (IAP), Chrome Enterprise Premium (BeyondCorp Enterprise)
- **Network Security:** Cloud Armor, VPC Service Controls, Cloud Next Generation Firewall (Cloud NGFW)
- **Data Protection:** Cloud Key Management Service (KMS), Sensitive Data Protection (formerly DLP), Confidential Computing
- **Threat Detection & Response:** Google SecOps (Chronicle), Security Command Center (SCC), Security Health Analytics
- **Supply Chain & Build Security:** Binary Authorization, Artifact Analysis, Artifact Registry
- **Compliance & Sovereignty:** Assured Workloads, Access Transparency, Access Approval
- **Secrets Management:** Secret Manager

## Assessment Question Bank

### Security by Design
1. Are security requirements captured as first-class design requirements alongside functional requirements?
2. Is threat modeling performed for each workload and updated when architecture changes significantly?
3. Are secure defaults enforced at the infrastructure level (e.g., org policies blocking public IPs, requiring CMEK, disabling SA key creation)?
4. Is a defense-in-depth strategy documented, covering network, identity, data, and application layers?
5. Are security architecture decisions captured as Architecture Decision Records (ADRs)?
6. Is a security champion or review gate embedded in the system design process?
7. Are third-party and open source dependencies evaluated for known vulnerabilities before adoption?
8. Is sensitive data classification applied to all data assets at design time?
9. Are blast-radius minimization patterns (separate projects per tier, VPC segmentation) applied?
10. Are security requirements tested as part of functional acceptance criteria?

### Zero Trust
1. Is identity verification enforced for every user and service regardless of network origin?
2. Are all service-to-service calls authenticated (e.g., using Workload Identity, mTLS, IAP)?
3. Is device posture evaluated before granting access to sensitive resources (e.g., via BeyondCorp / Chrome Enterprise Premium)?
4. Are VPC Service Controls perimeters defined to restrict sensitive API access to trusted contexts?
5. Is lateral movement risk addressed through micro-segmentation or VPC firewall rules?
6. Are IAM bindings reviewed and rightsized to least privilege on a regular cadence?
7. Is privileged access managed and time-bound (e.g., JIT access, PAM tooling)?
8. Is all data encrypted in transit with enforced TLS policies?
9. Are audit logs (Admin Activity, Data Access) enabled and retained for all sensitive projects?
10. Is continuous authorization evaluated for long-running sessions and API tokens?
11. Are externally exposed endpoints protected by Cloud Armor WAF policies?

### Shift-Left Security
1. Are SAST and SCA tools integrated into pull request checks?
2. Is container image scanning (Artifact Analysis) enforced before images are pushed to Artifact Registry?
3. Is Binary Authorization policy enabled on all GKE clusters and Cloud Run services?
4. Are IaC templates (Terraform, Config Connector) scanned for security misconfigurations before apply?
5. Is secrets detection (e.g., truffleHog, git-secrets) integrated into the developer commit workflow?
6. Are security unit tests written for authentication, authorization, and input validation logic?
7. Are dependency vulnerability alerts surfaced to developers in their IDE or PR review?
8. Is a software bill of materials (SBOM) generated for each release artifact?
9. Are security findings from pipeline gates tracked to resolution with SLA enforcement?
10. Are developers trained on secure coding practices with GCP-specific guidance?

### Preemptive Cyber Defense
1. Is Security Command Center (SCC) enabled at the org level with all built-in detectors active?
2. Are Google SecOps (Chronicle) SIEM and SOAR capabilities used for centralized log analysis and automated response?
3. Is threat intelligence integrated into detection rules (e.g., YARA-L rules in Chronicle)?
4. Are anomalous IAM activity and privilege escalation patterns detected automatically?
5. Are network intrusion detection capabilities active (e.g., Cloud IDS)?
6. Is a documented incident response runbook maintained and tested via tabletop exercises?
7. Are SCC findings triaged, assigned owners, and tracked to remediation within defined SLAs?
8. Is vulnerability management performed on a recurring schedule across all compute assets?
9. Are red team or penetration testing exercises conducted at least annually?
10. Are honeytokens or canary resources deployed to detect unauthorized access attempts?

### AI Security
1. Are AI model endpoints protected by authentication and authorization controls equivalent to any other sensitive API?
2. Is training data validated, sanitized, and access-controlled to prevent poisoning attacks?
3. Are model outputs inspected for sensitive data leakage (e.g., PII, proprietary information)?
4. Is prompt injection risk addressed through input validation and sandboxed execution for user-controlled inputs?
5. Are AI supply chain components (foundation models, libraries, datasets) tracked in an inventory with provenance?
6. Is model access logged and auditable for compliance and forensic purposes?
7. Are AI-specific risks (hallucination, model inversion, membership inference) included in the threat model?
8. Are AI systems subject to the same change management and security review processes as other production systems?

### Regulatory Compliance
1. Have all applicable regulatory frameworks (GDPR, HIPAA, PCI-DSS, FedRAMP, SOC 2, etc.) been identified and mapped to workload data flows?
2. Is Assured Workloads used for regulated workloads requiring data sovereignty or personnel access controls?
3. Are data residency constraints enforced via org policies and resource location restrictions?
4. Is a data retention and deletion policy defined, documented, and enforced technically?
5. Is Sensitive Data Protection used to discover, classify, and de-identify sensitive data at rest and in transit?
6. Are audit logs retained for the full period required by each applicable compliance framework?
7. Are compliance posture reports generated from SCC's compliance dashboards on a regular cadence?
8. Is a vendor risk management process in place for third-party processors handling regulated data?
9. Are privacy impact assessments (PIAs) performed for new processing activities involving personal data?
10. Is there a documented process for responding to data subject access requests (DSARs) within required timeframes?

## Validation Checklist

### Security by Design
- [ ] Threat model exists and is current for each workload
- [ ] Org policies enforce secure defaults (no public IPs, CMEK required, SA key creation disabled)
- [ ] Data classification applied to all data assets
- [ ] Security ADRs documented for major architectural decisions
- [ ] Defense-in-depth layers (network, identity, data, application) all addressed

### Zero Trust
- [ ] All service-to-service calls use Workload Identity or mTLS — no static credentials
- [ ] VPC Service Controls perimeters defined for all sensitive APIs
- [ ] IAP enforces identity verification for all internal web applications
- [ ] Data Access audit logs enabled on all projects handling sensitive data
- [ ] Cloud Armor WAF policy active on all externally exposed load balancers
- [ ] IAM bindings reviewed and rightsized within the last 90 days

### Shift-Left Security
- [ ] Binary Authorization policy enforced on all GKE clusters and Cloud Run services
- [ ] Container image scanning integrated into CI pipeline — no unscanned images deployed
- [ ] IaC security scanning integrated into pull request gates
- [ ] Secrets never committed to source control — secret detection tooling active
- [ ] SBOM generated for each release artifact

### Preemptive Defense
- [ ] SCC enabled at org level with all built-in detectors active
- [ ] Chronicle SIEM receiving logs from all critical GCP sources
- [ ] Incident response runbook documented and tested within last 12 months
- [ ] SCC findings have owners and SLA tracking
- [ ] Vulnerability management cadence defined and followed

### AI Governance
- [ ] AI model endpoints authenticated and authorized equivalent to any sensitive API
- [ ] Training data provenance tracked and access-controlled
- [ ] AI-specific risks included in threat model
- [ ] Model outputs inspected for sensitive data leakage
- [ ] AI supply chain inventory maintained

## Response Shape

1. **Scope** — workload name, GCP resource hierarchy scope, evidence level (live / sanitized / documentation-based / inference)
2. **Findings per principle** — assessment result for each of the seven WAF security principles, labeling confirmed gaps vs. inferences
3. **Prioritized recommendations** — ordered by risk severity (Critical / High / Medium / Low), each with minimum required change, validation step, and rollback procedure
4. **Open risks** — items that could not be assessed due to missing evidence, with recommended evidence to gather

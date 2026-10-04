---
name: orca
description: "Expert agent for Orca Security CNAPP platform. Covers agentless SideScanning technology, CSPM, CWPP, CIEM, DSPM, API security, AI-SPM, risk prioritization, and shift-left CI/CD integration. WHEN: \"Orca Security\", \"Orca SideScan\", \"Orca CNAPP\", \"Orca cloud security\", \"Orca risk score\", \"Orca CSPM\", \"Orca image scanning\", \"Orca shift left\"."
license: MIT
---

# Orca Security

This skill covers Orca Security — the cloud security platform that pioneered SideScanning technology for agentless workload scanning. Orca provides a comprehensive CNAPP covering CSPM, CWPP, CIEM, DSPM, API security, and AI-SPM without requiring agents in customer workloads.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Deployment/Onboarding** -- Cover SideScanning setup, cloud account connection, scanning scope
   - **Risk Prioritization** -- Explain Orca Risk Score, context-aware prioritization, attack paths
   - **CSPM/Compliance** -- Cover misconfiguration detection, compliance frameworks, reporting
   - **CWPP/Vulnerability** -- Cover vulnerability management, workload scanning, image scanning
   - **CIEM/Identity** -- Cover IAM analysis, net-effective permissions, identity risk
   - **DSPM/Data** -- Cover data discovery, classification, sensitive data exposure
   - **CI/CD Integration** -- Cover shift-left scanning, registry scanning, pipeline integration
   - **Alert Management** -- Cover alert triage, suppression, integrations

2. **Identify environment** -- Which cloud providers (AWS, Azure, GCP)? Multi-account? What compliance requirements? Existing security tooling?

3. **Analyze** -- Apply Orca-specific reasoning. Orca's key differentiator is agentless SideScanning with a unified data model that correlates across CSPM, CWPP, CIEM, and DSPM without agent complexity.

4. **Recommend** -- Provide specific, actionable guidance with Orca platform context.

## SideScanning Technology

### How SideScanning Works

Orca's SideScanning is the core differentiator — it scans workload storage without running any code in the workload:

**Mechanism:**
1. Orca reads cloud storage snapshots (EBS snapshots, Azure managed disk snapshots, GCS disk snapshots) — the same data that backs running VMs and containers
2. Snapshots are mounted in Orca's own cloud infrastructure as read-only volumes
3. Orca's scanning engine reads the filesystems, package databases, configuration files, and sensitive data
4. Snapshots are immediately deleted after scanning

**What SideScanning covers:**
- Installed OS packages (DEB, RPM, APK, Alpine, Windows) → CVE detection
- Language runtime packages (npm, pip, gem, Maven, NuGet, Go, etc.) → CVE detection
- Configuration files → misconfiguration detection, secrets detection
- Sensitive data on disk → PII, PCI, PHI, credentials classification
- File integrity and malware → static malware signatures in files
- Active processes at time of snapshot (from `/proc` and OS state files)
- User accounts, SSH keys, cron jobs → persistence indicators

**What SideScanning does NOT cover:**
- Real-time runtime behavioral detection (what a process does at execution time)
- In-memory threats
- Network-level behavioral anomalies in real time
- Ephemeral container activity not captured in the snapshot

**Performance impact:** Zero. Scanning happens outside the workload on a read-only copy. No CPU, memory, or network load on running workloads.

**Scanning frequency:** Configurable; default is every 24 hours. Near-real-time for newly deployed workloads.

### Comparison to Agent-Based CWPP

| Capability | Orca SideScanning | Agent-Based (Defender, Aqua) |
|---|---|---|
| Vulnerability scanning | Yes (offline snapshot) | Yes (agent or snapshot) |
| Configuration analysis | Yes | Yes |
| Secrets on disk | Yes | Yes |
| Sensitive data classification | Yes | Varies |
| Real-time runtime detection | No | Yes |
| Process behavioral analytics | No (snapshot-time only) | Yes |
| Zero performance impact | Yes | Near-zero (agent has small overhead) |
| Deployment complexity | Low (no agents) | Medium (agent lifecycle management) |

## Orca Unified Data Model

Orca builds a unified data model across all discovered assets:

**Asset types:** Cloud accounts, VMs, containers, managed services (RDS, S3, etc.), IAM entities, network resources, data stores

**Relationship types:**
- Network connectivity (can reach, internet-exposed)
- IAM relationships (has role, can assume, has permissions)
- Data relationships (stores, classifies as)
- Vulnerability relationships (has CVE, severity, exploitability)
- Infrastructure relationships (runs on, deployed in)

This unified model enables cross-domain risk correlation — the same approach as Wiz's Security Graph but using Orca's terminology.

## Risk Prioritization

### Orca Risk Score

Orca uses context-aware risk scoring to prioritize findings:

**Risk score factors:**
- **Exploitability:** Is there a public exploit? CVSS score? CISA KEV?
- **Internet exposure:** Can this asset be reached from the internet?
- **Blast radius:** What sensitive assets are reachable after compromise?
- **Asset value:** Is this a production system? Does it hold sensitive data?
- **Attack path depth:** How many steps to reach a critical asset?

**The result:** An Orca risk score (0-100) that represents actual business risk — not just raw vulnerability count or CVSS scores in isolation.

**Why this matters:**
- A CVSS 9.8 CVE on an isolated dev VM with no network exposure = low risk
- A CVSS 6.5 CVE on an internet-exposed production VM with an IAM role that can access the customer database = high risk

### Attack Paths and Toxic Combinations

Orca visualizes multi-hop attack paths:

**Example attack path:**
```
[Internet]
  → EC2 instance (port 8443 open)
    → Exploitable vulnerability (CVE-2023-XXXX, CVSS 9.1)
      → IMDSv1 enabled (credential theft)
        → EC2 instance role
          → S3:* permission on prod bucket
            → PII data: 500K records
```

Orca labels this chain as a "toxic combination" and scores it based on the full path, not individual steps.

## CSPM Capabilities

**Configuration checks:**
- 1,500+ built-in checks across AWS, Azure, GCP
- Coverage: IAM, networking, storage, compute, databases, logging/monitoring, encryption, container services
- Custom checks using Orca's query language

**Compliance frameworks:**
- CIS Benchmarks (AWS, Azure, GCP — all levels)
- NIST 800-53, PCI DSS, HIPAA, SOC 2, ISO 27001
- GDPR, FedRAMP, CMMC, Australian ISM
- Custom frameworks via control mapping

**Compliance reporting:**
- Per-framework compliance score with trend tracking
- Resource-level compliance evidence
- Exportable audit reports (PDF, CSV)
- Scheduled report delivery

## CWPP Capabilities

**Vulnerability management:**
- OS and language package CVE detection via SideScanning
- EPSS scoring (Exploit Prediction Scoring System) alongside CVSS
- CISA KEV integration (flag known-exploited vulnerabilities)
- Virtual patching guidance (workarounds while waiting for patches)
- Vulnerability age tracking (how long has this been open?)

**Container image scanning:**
- Registry scanning (ECR, ACR, GCR, Docker Hub, private registries)
- CI/CD integration (scan images before push/deploy)
- Running container scanning via host snapshot
- Image layer analysis (identify which layer introduced a CVE)

**Malware detection:**
- Static malware signature scanning on disk
- Detects: crypto miners, ransomware, web shells, backdoors, rootkits
- Updated threat intelligence feeds

## CIEM Capabilities

**Identity analysis:**
- Enumerates all cloud identities across connected accounts
- Calculates net-effective permissions (evaluating all policy sources)
- Identifies over-privileged identities vs. actually-used permissions
- Detects: stale credentials, cross-account trust risks, shadow admins

**Identity attack paths:**
- Maps identity-based attack chains
- "This service account can assume this role which can access this sensitive database"
- Visualizes identity relationships in the attack path graph

## DSPM Capabilities

**Data discovery:**
- Discovers all data stores: S3, Azure Blob, GCS, RDS, DynamoDB, Cosmos DB, Azure SQL, BigQuery, Snowflake, file shares
- Identifies data stores not previously known to security teams (shadow data)

**Data classification:**
- PII: names, SSNs, emails, phone numbers, addresses, dates of birth, passport numbers
- PCI: credit card numbers, CVVs
- PHI: health records, diagnoses, prescription data
- Secrets: API keys, passwords, tokens, certificates
- Intellectual property: source code, business documents

**Data exposure analysis:**
- Who/what has access to sensitive data stores?
- Is the data encrypted at rest and in transit?
- Is the data publicly accessible?
- Is access logged and audited?

## AI-SPM (AI Security Posture Management)

**AI workload discovery:**
- Discovers AI/ML assets: SageMaker endpoints, Azure OpenAI deployments, Vertex AI models, Bedrock, custom model servers
- Identifies AI model training data locations
- Detects AI inference API exposure

**AI-specific risks:**
- Exposed AI API endpoints without authentication
- Training data in publicly accessible storage
- Model artifacts accessible to unauthorized identities
- AI workloads with overprivileged IAM roles

## Shift-Left / CI/CD Integration

**Image scanning in CI/CD:**
- Orca CLI (`orca-cli`) for pipeline integration
- GitHub Actions, GitLab CI, Jenkins, CircleCI integrations
- Block pipelines on policy violations (configurable severity thresholds)
- SARIF output for GitHub Code Scanning

**IaC scanning:**
- Terraform, CloudFormation, ARM templates, Helm charts, Kubernetes YAML
- Pre-deployment misconfiguration detection
- Policy-as-code enforcement in CI/CD

**Registry scanning:**
- Scheduled scans of container registries
- New image detection triggers automatic scan
- Registry compliance policies (block non-compliant images from being pulled)

## Integrations

**SIEM/SOAR:**
- Splunk (webhook or Splunk app)
- Microsoft Sentinel (via webhook or native connector)
- Sumo Logic, Datadog
- Generic webhook for custom SOAR platforms

**Ticketing:**
- Jira, ServiceNow, PagerDuty
- Configurable routing rules (which alert → which project/queue)
- Two-way sync for alert resolution

**Notification:**
- Slack, Teams, email, OpsGenie

**API access:**
- REST API for programmatic access to findings, assets, risk scores
- API key authentication
- Webhook subscriptions for real-time event delivery

## Common Operational Patterns

### Tuning Alert Volume

Orca often surfaces thousands of findings on initial deployment. Recommended triage approach:

1. **Focus on critical attack paths first** — Use Orca's attack path view, not the flat alert list
2. **Filter by environment** — Tag production resources; prioritize prod over dev
3. **Filter by internet exposure** — Internet-exposed assets with critical findings first
4. **Use risk score threshold** — Start with risk score > 70 as the initial actionable set
5. **Create suppression rules** for:
   - Known-good configurations (documented exceptions)
   - Dev/sandbox accounts with different risk tolerance
   - Specific resource types that are not relevant

### Measuring Posture Improvement

Track over time:
- Risk score distribution (count of critical/high/medium findings)
- Compliance framework scores per account
- Mean time to remediate (MTTR) by severity
- Attack path count over time
- Vulnerabilities by age (time open)

## Account Onboarding

**AWS onboarding:**
1. In Orca console: Connect Cloud Account → AWS
2. Deploy CloudFormation stack (creates IAM role with required permissions)
3. Orca validates permissions and starts scanning
4. Initial scan completes in hours depending on account size

**Azure onboarding:**
1. Connect Cloud Account → Azure
2. Run provided PowerShell script (creates App Registration + role assignments)
3. Orca validates and begins scanning subscriptions

**Permissions required:**
- AWS: SecurityAudit + ReadOnlyAccess + specific snapshot permissions
- Azure: Reader + additional read roles for specific services
- GCP: Custom role with viewer permissions across required APIs

## Reference Files

Load this when you need deep architectural knowledge:

- `references/vulnerability-management.md` -- Vulnerability-management-specific angle: Sonar Query Language examples, CNAPP capabilities, and an Orca-vs-Wiz-vs-Prisma-Cloud comparison. Read when the user's intent is vuln scanning/prioritization rather than CSPM/CNAPP posture.

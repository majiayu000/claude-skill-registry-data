---
name: wiz
description: "Expert agent for Wiz cloud security platform. Covers agentless CNAPP, Security Graph, toxic combinations, attack path analysis, CSPM/CWPP/CIEM/DSPM/CDR, Wiz Code shift-left, Wiz Defend runtime, AI-SPM, and multi-cloud configuration. WHEN: \"Wiz\", \"Wiz Security Graph\", \"toxic combination\", \"Wiz attack path\", \"Wiz CSPM\", \"Wiz CWPP\", \"Wiz Code\", \"Wiz Defend\", \"AI-SPM Wiz\", \"Wiz policy\", \"Wiz connector\"."
license: MIT
---

# Wiz Cloud Security

This skill covers the Wiz cloud security platform — the CNAPP that pioneered agentless scanning and Security Graph-based risk correlation. It has deep knowledge of the Wiz architecture, capabilities, configuration, and operational patterns across CSPM, CWPP, CIEM, DSPM, CDR, shift-left (Wiz Code), and AI-SPM.

Wiz was acquired by Google for $32B in 2025, making it part of Google Cloud — though it remains a standalone multi-cloud product.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Deployment/Onboarding** -- Load `references/architecture.md`; cover connector setup and scanning scope
   - **Policy/Detection** -- Explain Wiz rule types, policy framework, and best practices for tuning
   - **Risk Investigation** -- Walk through Security Graph traversal, toxic combinations, attack path analysis
   - **Remediation** -- Discuss Wiz remediation workflow, JIRA/ticketing integration, auto-remediation
   - **Integration** -- Cover Wiz APIs, SIEM/SOAR integration, CI/CD integration (Wiz Code)
   - **Runtime/CDR** -- Cover Wiz Defend and runtime sensor deployment
   - **Compliance** -- Walk through framework mapping, compliance reports, custom frameworks

2. **Identify environment** -- Which cloud providers (AWS, Azure, GCP, OCI, Alibaba)? What workload types (EC2/VM, containers, EKS/AKS/GKE, serverless, PaaS)? Multi-tenant (separate connectors per account/subscription)?

3. **Load context** -- Read `references/architecture.md` for deep architectural knowledge when needed.

4. **Analyze** -- Apply Wiz-specific reasoning. Wiz's key differentiator is correlating findings across the Security Graph — don't answer questions about individual findings in isolation; understand the full context.

5. **Recommend** -- Provide actionable configuration, workflow, and operational guidance.

6. **Verify** -- Suggest how to validate in the Wiz console (Explorer, Dashboards, Reports).

## Core Capabilities

### Agentless Architecture

Wiz scans without deploying agents. The core mechanism:

**Cloud API Scanning:**
- Wiz reads cloud provider APIs to collect resource inventory, configuration, IAM policies, network topology
- Covers: EC2/VMs, S3/Blob/GCS, RDS/Managed DBs, Lambda, ECS/EKS, Azure AKS, GKE, IAM policies, VPCs, Security Groups/NSGs, CloudTrail logs (for CDR)
- Near real-time: Wiz polls APIs continuously and processes change events

**Snapshot Scanning (CWPP):**
- Wiz creates read-only snapshots of cloud storage volumes (EBS snapshots, managed disk snapshots)
- Mounts snapshots in Wiz's own cloud environment for offline scanning
- Scans: installed packages (OS + language), running services, configuration files, secrets on disk, malware
- No performance impact on the scanned workload — scanning happens outside the workload

**Container Image Scanning:**
- Pulls images from registries (ECR, ACR, GCR, Docker Hub, private registries)
- Scans image layers for vulnerable packages, hardcoded secrets, misconfigurations
- Also scans running container workloads via snapshot of the underlying storage

### Security Graph

The Security Graph is Wiz's core data model — a property graph where nodes are cloud resources and edges are relationships:

**Node types:** Cloud accounts, VMs, containers, images, IAM entities, data stores, networks, secrets, vulnerabilities, cloud services

**Edge types (relationships):**
- Network connectivity (can reach, exposed to internet)
- IAM relationships (has permission, can assume, has role)
- Data relationships (contains, classifies as PII/PCI/PHI)
- Vulnerability relationships (has CVE, exploitable via)
- Infrastructure relationships (runs on, deployed in, uses)

**Graph traversal for toxic combinations:**
Wiz's rules traverse multiple hops in the graph to find correlated risks. Example rule logic:
```
Find: Virtual Machine
Where:
  - has critical CVE with public exploit
  - is accessible from internet
  - has attached IAM role
  - IAM role has permissions on data store
  - data store contains sensitive data
```

This finds "publicly-reachable VM with exploitable CVE, whose IAM role can access sensitive data" — a complete attack path.

### Wiz Rule Framework

**Built-in rules (Wiz Policies):**
- Wiz ships 1,400+ built-in detection rules across CSPM, CWPP, CIEM, DSPM
- Rules are tagged by framework (CIS, NIST, PCI DSS, HIPAA, etc.)
- Severity: Critical, High, Medium, Low, Informational

**Custom rules (Wiz Query Language / WQL):**
Wiz uses a graph query language for custom rules:
```
FIND VirtualMachine
WHERE virtualMachineType = "EC2"
  AND networkExposure = "WidelyOpen"
  AND operatingSystem.isEndOfLife = true
```

**Cloud Configuration Rules:** Detect misconfigurations (CSPM)
**Vulnerability Rules:** Detect CVEs and vulnerable packages (CWPP)
**Threat Detection Rules:** Detect behavioral anomalies for CDR (requires Wiz Defend or cloud log integration)
**Secrets Rules:** Detect exposed secrets in cloud storage and workloads (DSPM)
**Data Rules:** Detect sensitive data exposure (DSPM)

### Toxic Combinations (Attack Paths)

Wiz popularized the concept of "toxic combinations" — the single biggest differentiation from point-tool CSPM:

**What makes something toxic:**
1. **Internet exposure** -- reachable from the public internet (network path exists)
2. **Vulnerability or exploitable condition** -- CVE with public exploit, privilege escalation path, misconfiguration enabling compromise
3. **Blast radius amplifier** -- IAM permissions, lateral movement ability, privileged access
4. **High-value target** -- sensitive data, production databases, secrets, privileged accounts

**Wiz Attack Path visualization:**
- Attack paths are shown as a graph walk in the Wiz console
- Each step is labeled with the specific technique or condition
- Wiz scores each attack path by estimated impact and exploitability

**Example toxic combination:**
```
Internet Gateway
  --> EC2 Instance (port 8080 open)
       |-- running unpatched Log4Shell (CVE-2021-44228, CVSS 10)
       |-- IMDSv1 enabled
       |-- IAM Role: ec2-app-role
            |-- s3:* on bucket: prod-customer-data
                 |-- contains: 2.4M PII records (SSN, DOB, email)
```

Wiz surfaces this as a **Critical toxic combination** with suggested remediations at each step.

### Wiz CSPM

Coverage across all major cloud providers:

**AWS:** 400+ checks across all AWS services — IAM, EC2, S3, RDS, EKS, Lambda, CloudTrail, GuardDuty status, KMS, Secrets Manager, VPC, Route53, CloudFront

**Azure:** 350+ checks — RBAC, Azure AD, VM security, AKS, SQL, Key Vault, Storage, Defender for Cloud status, NSG, Activity Log

**GCP:** 300+ checks — Cloud IAM, GKE, Compute Engine, Cloud Storage, Cloud SQL, KMS, Logging, VPC, Cloud Functions

**Compliance frameworks:** Wiz maps rules to CIS, NIST 800-53, SOC 2, PCI DSS, HIPAA, ISO 27001, FedRAMP, GDPR, and custom frameworks

**Framework score:** Wiz provides a compliance score per framework per account with trend tracking

### Wiz CWPP

**Vulnerability Management:**
- OS packages: DEB, RPM, APK, Windows MSI/installed programs
- Language packages: npm, pip, gem, Maven, NuGet, Go modules, Cargo
- Container images: full layer-by-layer scanning
- EPSS scores: Wiz shows Exploit Prediction Scoring System scores alongside CVSS
- "In use" context: Wiz can correlate vulnerabilities with whether the package is actually loaded at runtime (reduces noise)

**Runtime Protection (Wiz Defend):**
- Optional lightweight sensor deployed in workloads
- Captures: process execution, file system events, network connections, syscalls
- Detection: crypto mining, reverse shells, web shell activity, lateral movement, privilege escalation, credential theft
- Requires sensor installation — contrasts with the rest of Wiz's agentless approach

### Wiz CIEM

**Identity analysis:**
- Enumerates all cloud identities: IAM users, roles, groups, service accounts, managed identities, federated identities, OIDC providers
- Calculates net-effective permissions (AWS: evaluates service control policies + permission boundaries + identity policies + resource policies)
- Identifies: overprivileged identities, stale credentials, cross-account trust chains, shadow admins, unused permissions

**Key CIEM findings:**
- "IAM role has administrator access and is attached to a publicly reachable EC2"
- "Service account with owner role on GCP project assigned to Cloud Function accessible from internet"
- "Cross-account role assumption chain: dev account --> staging account --> prod account"

### Wiz DSPM

- Discovers all data stores in connected cloud accounts
- Classification: PII (names, SSNs, emails, addresses), PCI (card numbers), PHI (health data), secrets (API keys, passwords), intellectual property
- Data exposure: who has access, is data encrypted, is data publicly accessible, is data logged
- Shadow data: discovers data stores that security teams didn't know about

### Wiz Code (Shift-Left)

Integrates security into the development lifecycle:
- **IaC scanning:** Terraform, CloudFormation, ARM, Bicep, CDK — detect misconfigurations before deployment
- **Secrets detection:** Scans source code for hardcoded credentials, API keys, tokens
- **SCA:** Vulnerable open-source dependencies in application code
- **Container image scanning in CI/CD:** Scan before images are pushed to production
- **Pull request integration:** Surface security findings as PR comments in GitHub/GitLab/Bitbucket
- **Policy as code:** Enforce CSPM policies in CI/CD pipelines (fail builds for critical misconfigs)

### Wiz Connector Setup

Connectors authenticate Wiz to cloud providers:

**AWS Connector:**
- Creates an IAM role with ReadOnly + SecurityAudit policies (plus Wiz-specific permission set)
- Wiz assumes the role via cross-account role assumption from Wiz's AWS account
- Deployed via CloudFormation template or Terraform
- One connector per AWS account, or use AWS Organizations for automated multi-account discovery

**Azure Connector:**
- Creates an App Registration (service principal) in Azure AD
- Assigns Reader + additional roles (Security Reader, Key Vault Reader)
- One connector per subscription, or management group for bulk enrollment

**GCP Connector:**
- Creates a Service Account with custom role
- Enables required APIs (CloudResourceManager, Compute, Container, etc.)
- One connector per project, or organization-level service account

### Wiz Integrations

**SIEM/SOAR:**
- Wiz Issues → Splunk (via Wiz Splunk app or webhook)
- Wiz Issues → Microsoft Sentinel (via Wiz data connector)
- Wiz Issues → ServiceNow, JIRA for ticketing
- Wiz Events → generic webhooks to any SOAR platform

**CI/CD:**
- Wiz CLI (`wizcli`) — scan images, IaC, and code directories locally or in pipelines
- GitHub Actions, GitLab CI, Jenkins, CircleCI integrations
- Admission controller (Wiz Admission Controller for Kubernetes) — block non-compliant images from running

**Notification:**
- Slack, Teams, PagerDuty, email
- Configurable per severity and rule type

### Wiz Remediation Workflow

**Guided remediation:**
- Each finding includes step-by-step remediation instructions with CLI commands
- Terraform/IaC remediation examples provided where applicable
- Links to provider documentation

**Auto-remediation:**
- Wiz can trigger auto-remediation via AWS SSM Automation, Azure Automation, or custom Lambda/Function integrations
- Recommended only for high-confidence, low-blast-radius remediations (e.g., disabling public access on S3 bucket)
- Require approval workflows for production remediations

**Ticketing integration:**
- Wiz Issues sync to JIRA tickets automatically
- Two-way sync: resolving ticket updates Wiz status
- SLA tracking within Wiz

### Common Configuration Tasks

**Tuning false positives:**
- Create exceptions (suppressions) for specific resources or accounts with documented justification
- Exceptions have expiry dates and require approval workflow
- Bulk exception management for known-good configurations

**Custom frameworks:**
- Build custom compliance frameworks by mapping existing Wiz rules to custom controls
- Import external frameworks not yet built into Wiz

**Scoping:**
- Include/exclude specific accounts, subscriptions, projects from scanning
- Tag-based scoping (e.g., scan only resources tagged `env:production`)
- Sensitivity levels for DSPM data classification

## Reference Files

Load these when you need deep architectural knowledge:

- `references/architecture.md` -- Wiz platform architecture: agentless scanning mechanism, Security Graph data model, connector types, toxic combination logic, Wiz Defend runtime sensor, multi-cloud coverage details.
- `references/vulnerability-management.md` -- Vulnerability-management-specific angle: WQL query examples for vuln prioritization, agentless CWPP scanning mechanics. Read when the user's intent is vuln scanning/prioritization rather than CSPM/CNAPP posture.

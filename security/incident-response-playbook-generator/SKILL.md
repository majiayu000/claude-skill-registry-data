---
name: incident-response-playbook-generator
displayName: Incident Response Playbook Generator
tagline: "Generate runbooks for common cloud security incidents: compromised credentials, data exposure, crypto mining, etc."
description: |
  Creates detailed incident response playbooks tailored to your cloud environment
  and team structure. Covers detection, containment, eradication, recovery, and
  post-incident review phases for common cloud security incidents including
  compromised credentials, data exposure, cryptomining, and unauthorized access.
department:
  - Security & Compliance
  - Engineering
use_cases:
  - Incident Response
  - Documentation
tools_required:
  - GitHub MCP
  - Notion MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  We need incident response playbooks for our AWS environment.
  30 engineers, DevOps + Security team of 4. Incidents we want covered:
  compromised IAM credentials, S3 data exposure, cryptomining, and
  unauthorized EC2 instance creation. Output to Notion for runbook hub.
exampleOutput: |
  Incident Response Playbooks — [Company] | AWS

  PLAYBOOK SUMMARY
  | Incident Type              | Severity | Detection              | Containment Steps    |
  |----------------------------|----------|------------------------|----------------------|
  | Compromised IAM credentials| P1       | CloudTrail anomalies   | Disable keys, revoke |
  | S3 data exposure           | P1       | GuardDuty, access logs | Block public, notify  |
  | Cryptomining               | P2       | CPU spikes, GuardDuty  | Isolate instance     |
  | Unauthorized EC2 creation   | P2       | CloudTrail, config     | Terminate, block     |

  PHASE BREAKDOWN (Compromised Credentials)
  Detection: CloudTrail unusual API calls, GuardDuty findings, failed MFA
  Containment: Disable access keys, revoke sessions, block IP
  Eradication: Rotate credentials, review permissions
  Recovery: Validate services, restore least-privilege access
  PIR: Root cause, timeline, lessons learned

  Generated: Notion runbook pages with tables, checklists, escalation contacts
---

# Incident Response Playbook Generator

Generate runbooks for common cloud security incidents: compromised credentials, data exposure, crypto mining, etc.

**Integrations:** GitHub MCP, Notion MCP

## When to Use

- The user needs incident response runbooks for their cloud environment before an audit or security maturity assessment
- The user mentions "IR playbook", "runbook", "incident response", or "security incident procedures"
- After an incident to document and formalize what worked, for future use
- When building or improving a security operations capability

## Steps

### Step 1: Define Incident Catalog

Create a catalog of incidents to cover:

| Incident Type | Description | Typical Severity |
|---------------|-------------|------------------|
| Compromised IAM credentials | Leaked keys, session hijack, phishing | P1 (Critical) |
| S3/data exposure | Public bucket, misconfigured ACLs | P1 (Critical) |
| Cryptomining | Malware/script mining crypto on compute | P2 (High) |
| Unauthorized EC2/resource creation | Rogue instances, sprawl from compromise | P2 (High) |
| Ransomware | Encryption of data, extortion | P1 (Critical) |
| DDoS / abuse | Resource exhaustion, abuse of services | P2 (High) |
| Insider threat | Intentional misuse of access | P1 (Critical) |

Confirm with the user which incidents to include and their severity levels. Adapt for AWS, GCP, or Azure.

### Step 2: Document Detection Rules and Triggers

For each incident type, define how it is detected:

| Incident | Detection Method | Indicators |
|----------|------------------|------------|
| Compromised credentials | CloudTrail, GuardDuty, IdP logs | Unusual API calls, new regions, failed MFA |
| S3 exposure | GuardDuty, S3 access logs, Config | Public bucket, unexpected GetObject spikes |
| Cryptomining | CloudWatch metrics, GuardDuty | CPU >90% sustained, known mining domains |
| Unauthorized EC2 | CloudTrail, AWS Config | RunInstances by unexpected principal |

Include specific queries, dashboard links, and alert rule examples. Use GitHub MCP to store detection rules as code if desired.

### Step 3: Define Containment Procedures

For each incident, outline containment steps:

| Phase | Actions |
|-------|---------|
| **Immediate** | Isolate affected resources, disable credentials, block IPs |
| **Short-term** | Revoke sessions, restrict IAM, enable MFA if missing |
| **Communication** | Notify stakeholders, open incident ticket, legal/PR if needed |

Provide decision trees (e.g., "If credentials compromised → disable keys within 15 min"). Include escalation contacts and on-call rotation. Store playbook content in Notion MCP.

### Step 4: Define Eradication and Recovery Steps

For each incident type:

| Phase | Actions |
|-------|---------|
| **Eradication** | Remove malware, delete rogue resources, rotate credentials, patch vulnerabilities |
| **Recovery** | Restore from backup if needed, validate integrity, restore access with least privilege |
| **Validation** | Verify no persistence, re-scan, confirm logging is intact |

Include runbooks for credential rotation, instance termination, and backup restoration where applicable.

### Step 5: Create Post-Incident Review Template

Provide a standard PIR template:

| Section | Contents |
|---------|----------|
| Timeline | Detection time, containment time, resolution time |
| Root cause | What happened, why it happened |
| Impact | Affected systems, data, users, downtime |
| Response effectiveness | What worked, what did not |
| Action items | Process changes, tooling, training |

Store the template and completed PIRs in Notion. Ensure playbooks link to the PIR template.

## Output

Deliver:
- Incident catalog with severity and detection methods
- Playbook table: incident type, severity, detection, containment, eradication, recovery
- Step-by-step runbooks for each incident type with checklists and escalation paths
- Post-incident review template
- Notion runbook pages (or GitHub repo) with all playbooks and templates

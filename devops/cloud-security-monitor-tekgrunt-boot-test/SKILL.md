---
name: cloud-security-monitor
description: Activate when users need help setting up cloud security monitoring for AWS, Azure, or GCP, including adapter configuration, detection rules, and threat response.
---

# LimaCharlie Cloud Security Monitor

You are an expert at implementing comprehensive cloud security monitoring using LimaCharlie for AWS, Azure, and GCP environments.

## Overview

LimaCharlie provides unified cloud security monitoring across multi-cloud environments, solving common challenges:

- **Visibility challenges**: Unified view across AWS, Azure, and GCP
- **Data volume challenges**: Efficient storage with 1 year of searchable retention included
- **Multi-cloud challenges**: Single platform for all cloud providers
- **Cost challenges**: Often cheaper than native cloud logging solutions

## Architecture

Cloud security monitoring in LimaCharlie consists of:

1. **Adapters**: Ingest cloud audit logs and security events
2. **Detection Rules**: Identify threats and misconfigurations
3. **Response Actions**: Automated remediation and alerting
4. **Managed Rulesets**: Pre-built detection logic (Soteria Rules)

---

## Documentation Structure

This skill uses **Progressive Disclosure** - start here for overview, then dive into cloud-specific guides:

- **[AWS.md](./AWS.md)**: Complete AWS monitoring guide (CloudTrail, GuardDuty, adapters, rules)
- **[AZURE.md](./AZURE.md)**: Complete Azure monitoring guide (Event Hub, Entra ID, M365, adapters, rules)
- **[GCP.md](./GCP.md)**: Complete GCP monitoring guide (Pub/Sub, Cloud Logging, adapters, rules)
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**: Platform-specific troubleshooting

---

## Quick Start by Cloud

### AWS Quick Start

**What You'll Monitor**: CloudTrail API calls, GuardDuty findings

**Adapters Needed**:
- S3 or SQS adapter for CloudTrail (`platform: aws`)
- S3 or SQS adapter for GuardDuty (`platform: guard_duty`)

**Quick Setup**:
```bash
# CloudTrail via SQS
./lc_adapter sqs \
  client_options.identity.installation_key=<KEY> \
  client_options.identity.oid=<OID> \
  client_options.platform=aws \
  client_options.hostname=aws-cloudtrail \
  region=us-east-1 \
  access_key=<ACCESS_KEY> \
  secret_key=<SECRET_KEY> \
  queue_url=<QUEUE_URL>
```

**Recommended Rules**:
- Root account usage detection
- IAM policy changes
- Security group modifications
- S3 bucket exposure
- Console login without MFA

**Managed Ruleset**: Subscribe to `soteria-rules-aws` extension

**Full Guide**: [AWS.md](./AWS.md)

---

### Azure Quick Start

**What You'll Monitor**: Azure Monitor logs, Entra ID sign-ins, M365 audit events

**Adapters Needed**:
- Azure Event Hub adapter for Azure Monitor (`platform: azure_monitor`)
- Azure Event Hub adapter for Entra ID (`platform: azure_ad`)
- Office 365 adapter for M365 (`platform: office365`)

**Quick Setup**:
```bash
# Azure Monitor via Event Hub
./lc_adapter azure_event_hub \
  client_options.identity.installation_key=<KEY> \
  client_options.identity.oid=<OID> \
  client_options.platform=azure_monitor \
  client_options.hostname=azure-monitor \
  "connection_string=Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=POLICY;SharedAccessKey=KEY;EntityPath=HUB"
```

**Recommended Rules**:
- Entra ID risky sign-ins
- Admin role assignments
- Resource deletions
- Key Vault access
- Network security group changes

**Managed Ruleset**: Subscribe to `soteria-rules-o365` extension

**Full Guide**: [AZURE.md](./AZURE.md)

---

### GCP Quick Start

**What You'll Monitor**: Cloud Audit Logs (Admin Activity, Data Access, System Events)

**Adapters Needed**:
- Pub/Sub adapter for Cloud Logging (`platform: gcp`)

**Quick Setup**:
```bash
# Pub/Sub adapter
./lc_adapter pubsub \
  client_options.identity.installation_key=<KEY> \
  client_options.identity.oid=<OID> \
  client_options.platform=gcp \
  sub_name=<SUBSCRIPTION_NAME> \
  project_name=<PROJECT_ID>
```

**Recommended Rules**:
- IAM policy changes
- Service account key creation
- Firewall rule modifications
- GCS bucket permissions
- Compute instance creation

**Full Guide**: [GCP.md](./GCP.md)

---

## Common Cloud Threats

### IAM Abuse and Privilege Escalation
Monitor root/admin account usage, role/policy modifications, and service account key creation. Alert on IAM policy changes and unusual privilege grants.

### Data Exfiltration
Track storage permission changes, public bucket exposure, and external sharing. Monitor data access patterns and egress traffic.

### Resource Misconfigurations
Alert on public storage buckets, overly permissive security groups, disabled logging, and weak encryption settings.

### Unauthorized Access
Monitor authentication events, login locations, MFA usage, failed attempts, and impossible travel scenarios.

### Cryptojacking and Resource Abuse
Detect unexpected instance launches, unusual regions/instance types, and high-cost resource creation.

### Lateral Movement
Track cross-account access, assume role operations, service account impersonation, and unusual resource access patterns.

---

## Integration Strategies

**Cloud and Endpoint Correlation**: Tag sensors on cloud login, correlate with endpoint AWS CLI usage.

**Multi-Cloud Detection**: Create platform-agnostic rules that detect threats across AWS, Azure, and GCP.

**SIEM Integration**: Configure Outputs (Syslog, Webhook, S3) to forward cloud detections to downstream systems.

---

## Best Practices

### What to Monitor

**AWS Critical Events**:
- Root account usage
- IAM policy changes
- Security group modifications
- S3 bucket permission changes
- Console logins without MFA
- CloudTrail configuration changes

**Azure Critical Events**:
- Entra ID risky sign-ins
- Admin role assignments
- Resource deletions
- Key Vault access
- Network security group changes
- Conditional access policy modifications

**GCP Critical Events**:
- IAM policy modifications
- Service account key creation
- Firewall rule changes
- GCS bucket permission changes
- Compute instance creation
- VPC network modifications

### Rule Tuning

Start with high-confidence detections (root/admin usage, deletions, IAM changes). Add context to reduce false positives (exclude known service accounts, filter by time/region). Use suppression for high-volume events. Baseline normal activity before alerting.

### Cost Management

Filter logs at source, start with management events only, exclude read-only operations. Use cloud-to-cloud adapters when possible. Monitor ingestion rates and remove unused adapters.

### Security Hygiene

Use Hive Secrets for credentials. Follow least privilege (AWS: S3/SQS read-only, Azure: Event Hub Listen, GCP: Pub/Sub Subscriber). Monitor adapter connectivity with sensor_disconnected rules.

---

## Quick Reference

### Platform Names

- `aws`: AWS CloudTrail
- `guard_duty`: AWS GuardDuty
- `azure_monitor`: Azure Monitor
- `azure_ad`: Entra ID / Azure AD
- `msdefender`: Microsoft Defender
- `office365`: Microsoft 365
- `gcp`: Google Cloud Platform

### Common Event Names

**AWS**:
- `AwsApiCall`: CloudTrail API calls
- `ConsoleLogin`: AWS Console authentication

**Azure**:
- `AzureActivity`: Azure resource operations
- `SignInLogs`: Entra ID authentication
- `FileAccessed`: M365 file operations

**GCP**:
- `v1.compute.instances.insert`: Instance creation
- `google.iam.admin.v1.SetIamPolicy`: IAM changes
- `storage.setIamPermissions`: Storage permissions

### Key Operators

- `is platform`: Match by platform type
- `exists`: Check for field presence
- `contains`: Substring match
- `is public address`: Check if IP is external
- `is tagged`: Check for sensor tag
- `or` / `and`: Boolean logic
- `not in`: Exclusion list

### Response Actions

- `report`: Generate detection
- `task`: Execute sensor command
- `add tag`: Tag sensor
- `re-enroll`: Re-enroll cloned sensor

---

## Additional Resources

### LimaCharlie Documentation

- [AWS CloudTrail Adapter](/docs/adapter-types-aws-cloudtrail)
- [AWS GuardDuty Adapter](/docs/adapter-types-aws-guardduty)
- [Azure Event Hub Adapter](/docs/adapter-types-azure-event-hub)
- [Microsoft Entra ID Adapter](/docs/adapter-types-microsoft-entra-id)
- [Microsoft 365 Adapter](/docs/adapter-types-microsoft-365)
- [Google Cloud Pub/Sub Adapter](/docs/adapter-types-google-cloud-pubsub)
- [Soteria AWS Rules](/docs/soteria-aws-rules)
- [Soteria M365 Rules](/docs/soteria-m365-rules)

### Cloud Provider Documentation

- [AWS CloudTrail](https://docs.aws.amazon.com/cloudtrail/)
- [AWS GuardDuty](https://docs.aws.amazon.com/guardduty/)
- [Azure Monitor](https://docs.microsoft.com/azure/azure-monitor/)
- [Microsoft Entra ID](https://docs.microsoft.com/azure/active-directory/)
- [Microsoft 365 Audit](https://docs.microsoft.com/microsoft-365/compliance/search-the-audit-log)
- [GCP Cloud Audit Logs](https://cloud.google.com/logging/docs/audit)
- [GCP Pub/Sub](https://cloud.google.com/pubsub/docs)

### Community Resources

- LimaCharlie Discord: Community support
- GitHub Examples: Sample configurations
- Sigma Rules: Translate existing detections
- SOC Prime Uncoder: Convert detection formats

---

## Your Role

When helping users with cloud security monitoring:

### 1. Understand Their Environment

Ask clarifying questions:
- Which cloud providers do they use?
- What's their security maturity level?
- What specific threats concern them?
- What's their existing security stack?
- What's their event volume and budget?

### 2. Recommend Appropriate Solutions

Beginners: Start with Soteria managed rulesets and recommended configurations. Intermediate: Add custom rules and SIEM integrations. Advanced: Implement complex detection logic and custom automation.

### 3. Provide Complete Configurations

Include all required parameters with explanations. Use Hive secrets for credentials. Show CLI and IaC options.

### 4. Navigate to Detailed Guides

- AWS specifics: [AWS.md](./AWS.md)
- Azure specifics: [AZURE.md](./AZURE.md)
- GCP specifics: [GCP.md](./GCP.md)
- Troubleshooting: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

### 5. Follow Best Practices

Start with high-confidence detections, baseline before alerting, use suppression, protect credentials, follow least privilege, monitor adapter connectivity.

---

Always provide clear, actionable guidance with complete examples that users can implement immediately. Use the detailed guides in this directory for comprehensive, cloud-specific information.

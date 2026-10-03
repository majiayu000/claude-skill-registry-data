---
name: cloud-trail
description: "Cloud Trail."
domain: cybersecurity
---

|
| CloudTrail | AWS service that records API calls made to AWS services, providing an audit trail of actions taken by users, roles, and services |
| Management Events | CloudTrail events for control plane operations like creating resources, modifying IAM, and configuring services |
| Data Events | CloudTrail events for data plane operations like S3 object access and Lambda function invocations, providing granular activity logging |
| Log File Validation | CloudTrail feature that creates a digest file for verifying that log files have not been tampered with after delivery |
| CloudTrail Lake | Managed data lake for CloudTrail events enabling SQL-based queries without managing Athena tables or S3 data |
| Organization Trail | Single trail that captures API activity across all accounts in an AWS Organization to a central S3 bucket |

## Tools & Systems

- **Amazon Athena**: Serverless SQL query engine for analyzing CloudTrail logs stored in S3 at scale
- **CloudWatch Logs Insights**: Real-time log query service for interactive CloudTrail analysis within the last 30 days
- **CloudTrail Lake**: Managed event data lake with built-in SQL query capabilities and 7-year retention
- **Amazon Security Lake**: Centralized security data lake that normalizes CloudTrail data into OCSF format for SIEM consumption
- **AWS CloudTrail**: Core audit logging service capturing all API activity across AWS accounts and services

## Common Scenarios

### Scenario: Investigating an IAM Credential Compromise Through CloudTrail

**Context**: GuardDuty alerts on `UnauthorizedAccess:IAMUser/MaliciousIPCaller` for a developer's access key. The security team needs to trace all actions taken by the compromised credential.

**Approach**:
1. Query CloudTrail for all events by the compromised AccessKeyId across all regions
2. Build a timeline of API calls to understand the attack sequence
3. Identify the initial access point (when did the key first appear from a malicious IP)
4. Map all resources created, modified, or accessed by the attacker
5. Check for persistence mechanisms (new users, access keys, Lambda functions, EC2 instances)
6. Verify CloudTrail was not tampered with (check for StopLogging or UpdateTrail events)
7. Document the full attack chain and scope of impact for the incident response report

**Pitfalls**: CloudTrail events can take up to 15 minutes to appear in S3 and CloudWatch Logs. For real-time visibility during active incidents, use CloudTrail Lake or CloudWatch Logs Insights rather than Athena queries against S3. Cross-region attacks require querying multiple region partitions in Athena.

## Output Format

```
CloudTrail Security Analysis Report
======================================
Account: 123456789012
Analysis Period: 2026-02-16 to 2026-02-23
Trail: org-security-trail (organization-wide)

SECURITY EVENTS DETECTED:
  Root account logins:                  2
  Console logins without MFA:           7
  Privilege escalation attempts:       12
  CloudTrail configuration changes:     0
  Security group modifications:        34
  Unauthorized API calls:             156

HIGH-PRIORITY FINDINGS:
[CT-001] Console Login Without MFA
  User: admin-user
  Time: 2026-02-22T14:30:00Z
  IP: 203.0.113.50
  Action Required: Enforce MFA via IAM policy

[CT-002] IAM Privilege Escalation
  User: dev-user
  Time: 2026-02-23T03:15:00Z
  Events: CreatePolicyVersion -> AttachRolePolicy
  IP: 185.x.x.x (suspicious)
  Action Required: Investigate credential compromise

ALERTING STATUS:
  CIS metric filters configured: 14 / 14
  CloudWatch alarms active: 14 / 14
  Alerts fired (last 7 days): 8
```

---
name: cloud-ir-respond
description: "Cloud Ir Ir Respond."
domain: cybersecurity
---

|
| **IMDS (Instance Metadata Service)** | Cloud service providing instance credentials accessible from within a VM; SSRF attacks target IMDS to steal tokens |
| **CloudTrail** | AWS service logging all API calls across the AWS account; primary evidence source for AWS incident response |
| **Service Principal** | Non-human identity in Azure AD used by applications and services; compromise enables persistent API access |
| **SCP (Service Control Policy)** | AWS Organizations policy that limits the maximum permissions available to accounts; useful for guardrails |
| **Ephemeral Infrastructure** | Cloud resources (containers, functions, auto-scaled instances) that may be terminated before evidence can be collected |
| **Cross-Account Role Assumption** | AWS mechanism allowing one account to temporarily access resources in another; attackers pivot through assumed roles |

## Tools & Systems

- **AWS CloudTrail / Azure Activity Logs / GCP Audit Logs**: Cloud-native API logging services providing the primary audit trail
- **Cado Response**: Cloud-native forensics platform for automated evidence capture from AWS, Azure, and GCP
- **Prowler (AWS) / ScoutSuite (multi-cloud)**: Open-source cloud security assessment tools for post-incident posture review
- **Steampipe**: Open-source SQL-based tool for querying cloud APIs to investigate IAM configurations and resource states
- **Cartography (Lyft)**: Open-source tool for mapping cloud infrastructure relationships and identifying attack paths

## Common Scenarios

### Scenario: AWS Access Key Compromised via Public GitHub Repository

**Context**: AWS GuardDuty alerts on API calls from an unexpected IP address using an IAM user's access key. The key was accidentally committed to a public GitHub repository 4 hours ago.

**Approach**:
1. Immediately disable the compromised access key via AWS IAM
2. Attach AWSDenyAll policy to the affected IAM user
3. Query CloudTrail for all API calls made with the compromised key since exposure
4. Identify resources created or modified by the attacker (EC2 instances for crypto-mining, new IAM users for persistence)
5. Terminate unauthorized resources and remove backdoor IAM entities
6. Rotate all credentials the compromised user had access to
7. Enable GitHub secret scanning to prevent future credential leaks

**Pitfalls**:
- Only disabling the access key without checking for new access keys or IAM users created as persistence
- Not checking all AWS regions for attacker-created resources (crypto-miners deployed in every region)
- Forgetting to revoke temporary credentials from assumed roles (STS tokens remain valid until expiry)
- Not calculating the financial impact of unauthorized resource usage for insurance claims

## Output Format

```
CLOUD INCIDENT RESPONSE REPORT
================================
Incident:          INC-2025-1705
Cloud Provider:    AWS (Account: 123456789012)
Date Detected:     2025-11-15T14:00:00Z
Detection Source:  GuardDuty - UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration

COMPROMISE SUMMARY
Initial Access:    IAM access key exposed in public GitHub repo
Affected Identity: iam-user: deploy-bot (AKIA...)
Attacker IP:       203.0.113.42 (VPN exit node, Netherlands)
Duration:          4 hours (10:00 UTC - 14:00 UTC)

ATTACKER ACTIVITY (from CloudTrail)
10:15 UTC - DescribeInstances (reconnaissance)
10:18 UTC - RunInstances x 12 (c5.4xlarge, all regions - crypto-mining)
10:22 UTC - CreateUser "backup-admin" (persistence)
10:23 UTC - CreateAccessKey for "backup-admin"
10:25 UTC - AttachUserPolicy - AdministratorAccess to "backup-admin"
10:30 UTC - PutBucketPolicy - s3://data-bucket made public (exfiltration)

CONTAINMENT ACTIONS
[x] Original access key disabled
[x] User policy set to AWSDenyAll
[x] Backdoor IAM user "backup-admin" deleted
[x] 12 crypto-mining instances terminated (all regions)
[x] S3 bucket policy restored to private

FINANCIAL IMPACT
Unauthorized EC2: $2,847 (4 hours x 12 x c5.4xlarge)
Data Transfer:    $127 (S3 public access data egress)
Total:            $2,974

POST-INCIDENT HARDENING
1. GitHub secret scanning enabled
2. Access key rotation policy implemented
3. SCP preventing CloudTrail disablement deployed
4. GuardDuty auto-remediation Lambda configured
```

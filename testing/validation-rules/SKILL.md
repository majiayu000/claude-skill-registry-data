---
name: validation-rules
type: skill
description: Claim-to-CLI verification mappings for cross-validating findings
used_by: [ad-hoc]
---

# Validation Rules

Maps claim IDs to AWS CLI commands for verification. Covers common security check IDs (`qa-*`), external accessibility probes, and guidance for ad-hoc security queries. Inventory queries bypass this file entirely.

For how to interpret results, status definitions, scoring, and suppression handling see `agents/roles.md` → Expert Validation Process.

---

## Rule Format

```yaml
check_id:
  cli: <command with {{placeholders}}>
  confirmed: <condition that confirms issue>
  false_positive: <condition that disproves issue>
```

---

## File Index

| File | Contents |
|:-----|:---------|
| [probes.md](probes.md) | External accessibility probes — S3, EC2, API Gateway, Lambda, RDS, SNS, SQS, TLS/SSL (testssl.sh) |
| [iam.md](iam.md) | IAM users, roles, password policy, MFA condition evaluation, SLR abuse, SCP cross-reference |
| [compute.md](compute.md) | EC2 instances, security groups, EBS encryption, Lambda function URLs, Lambda privilege escalation |
| [storage.md](storage.md) | S3 buckets, KMS key rotation, RDS instances |
| [detection.md](detection.md) | CloudTrail, GuardDuty, Security Hub, Access Analyzer, AWS Config, Inspector |
| [common-checks.md](common-checks.md) | qa-01 to qa-10 baseline checks, ad-hoc query guidance, constraints |

---

## Claim ID → File Lookup

| Claim ID prefix | File |
|:----------------|:-----|
| `iam_*`, `scp_*` | [iam.md](iam.md) |
| `ec2_*`, `vpc_*`, `lambda_*` | [compute.md](compute.md) |
| `s3_*`, `rds_*`, `kms_*` | [storage.md](storage.md) |
| `cloudtrail_*`, `guardduty_*`, `securityhub_*`, `accessanalyzer_*`, `config_*`, `inspector*` | [detection.md](detection.md) |
| `qa-01` to `qa-10`, `adhoc-*` | [common-checks.md](common-checks.md) |
| Accessibility probes (curl/nmap/testssl.sh) | [probes.md](probes.md) |

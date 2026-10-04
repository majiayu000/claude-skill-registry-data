---
name: security-specialist
description: Security auditing, vulnerability identification, secure coding practices,
  and secrets management. Use when asked to audit code for security vulnerabilities,
  review IAM permissions, check for hardcoded secrets, implement authentication or
  authorization, fix a CVE, set up secrets management (Vault, AWS Secrets Manager),
  review network security rules, or assess OWASP Top 10 exposure.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: quality
  tags:
  - security
  - vulnerabilities
  - iam
  - secrets-management
  - owasp
  - authentication
  - cve
---

# Security Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `security audit`, `hardcoded secret`, `OWASP`.
- The requested work fits this skill's lane: Code security review, IAM hardening, secrets management, OWASP Top 10, CVE remediation.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Cloud infrastructure changes (use cloud specialist); application feature code.

## First actions
1. `Grep` for common secret patterns: `password`, `secret`, `api_key`, `token`, `private_key` in source files
2. `Glob('**/.env*', '**/config/**', '**/secrets/**')` — find config and secrets files
3. Identify the security scope: code review, infrastructure audit, IAM review, or secrets management

## Decision rules
- CRITICAL findings (hardcoded secrets, SQL injection, RCE vectors): surface immediately before completing any other review
- Severity order: CRITICAL → HIGH → MEDIUM → LOW → INFORMATIONAL
- For IAM: apply least-privilege; flag any wildcard (`*`) actions or resources in production policies
- For authentication: flag any custom auth implementation and recommend proven libraries instead

## Output contract
- Findings formatted as: `[SEVERITY] Category — Description — Risk — Remediation`
- For code findings: include the file path and line number
- Always include a remediation step, not just the finding

## Constraints
- NEVER include actual secret values in output — redact them
- Scope boundary: application logic fixes belong to the relevant language skill; IAM/cloud config fixes belong to cloud specialist skills

## Examples

### Example 1: AWS account security scan
User says: "Scan my AWS infrastructure for security issues"
Actions:
1. Write Python/boto3 script checking: public S3 buckets, open security group ports (22/3389 to 0.0.0.0/0), IAM users without MFA, unencrypted EBS volumes, disabled CloudTrail
2. Output grouped by severity
Result: Security audit script with prioritized findings JSON

## Reference
- `references/legacy-agent.md`: OWASP Top 10, secure coding patterns, IAM hardening, secrets management implementations, network security, compliance security controls

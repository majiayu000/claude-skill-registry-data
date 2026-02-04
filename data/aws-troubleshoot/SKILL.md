---
name: aws-troubleshoot
description: "Troubleshoot AWS services using tool-first access (via MCP when available), falling back to AWS CLI when necessary. Focus on EKS, S3, ECR, EC2, SSM, networking, site-to-site VPNs, IAM Identity Center, and IAM."
---

# AWS Troubleshooting Skill

## General Guidance

Always use **tool access first** for logs, metrics, and audit events.  
Fallback to AWS CLI commands **only** when deeper inspection is required or the tool cannot access specific data.

All investigations should:

1. Scope log queries by log group and time window  
2. Check CloudTrail for failed API calls  
3. Use service-specific metrics before guessing  
4. Recommend minimal corrections

---

## Core Services Covered

### EKS

Common issues:

- Image pull errors
- Pod pending (CNI/IP exhaustion)
- CrashLoopBackOff
- Node NotReady

Investigations:

- Query pod logs
- Query pod events
- Inspect node status and cluster metrics

### S3

Common issues:

- AccessDenied
- Incorrect KMS key
- BlockPublicAccess conflicts

Investigations:

- Query S3 server access logs
- Inspect CloudTrail for denied events

### ECR

Common issues:

- Token expiration
- Missing permissions
- Architecture mismatch

Investigations:

- Search CloudTrail for `ecr:*` denied actions
- Inspect repository push/pull failures

### EC2

Common issues:

- Failed instance boot
- ENI/network issues
- IMDSv2 access failures

Investigations:

- Check EC2 instance status checks
- Inspect system logs and VPC configuration

### SSM (Systems Manager)

SSM commands can be performed through the AWS tool when available.

Common issues:

- Agent not running
- Missing IAM permissions
- Instance not registered
- Command execution failures

Investigations:

- Check SSM agent status on instances
- Query command execution history
- Inspect CloudTrail for SSM API failures
- Validate instance profile permissions

### Networking & VPN

Common issues:

- Route mismatches
- NACL/Security Group blocks
- VPN tunnel down

Investigations:

- Query CloudWatch metrics for VPN TunnelState
- Validate routing tables and security groups

### IAM Identity Center (SSO)

Common issues:

- User not assigned
- Permission set mismatch

Investigations:

- Inspect activity logs for SSO authentication issues
- Validate permission sets

### IAM

Common issues:

- AccessDenied
- Incorrect role assumption

Investigations:

- Query CloudTrail for denied API events
- Identify missing permissions

---

## Workflow

1. Identify service  
2. Query scoped logs  
3. Query CloudTrail for denied API calls  
4. Query metrics when relevant  
5. Diagnose using AWS-specific heuristics  
6. Provide safe remediation steps

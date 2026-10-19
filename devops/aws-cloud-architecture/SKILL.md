---
name: aws-cloud-architecture
description: >
  Architect, secure, and evaluate cloud infrastructure on Amazon Web Services (AWS) using
  the Well-Architected Framework. Use when designing multi-AZ VPC networks, configuring
  least-privilege IAM policies and trust boundaries, hardening S3 storage with KMS, selecting
  compute architectures (Lambda, ECS, EKS), or establishing CloudTrail and CloudWatch observability.
compatibility: >
  Agent Skills-compatible coding agents with access to aws-cli, terraform, or cloudformation tooling. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "aws, cloud-architecture, iam, vpc, s3, ecs, eks, lambda, well-architected, devops"
  topics: "devops"
---

# AWS Cloud Architecture and Well-Architected Framework

Designing infrastructure on Amazon Web Services (AWS) requires strict alignment with the AWS Well-Architected Framework: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability. High-integrity AWS systems enforce defense-in-depth through multi-AZ network isolation, least-privilege identity federation, encrypted object storage, and continuous auditing.

## Purpose & Overview

This skill establishes reference architectures and implementation rules for building secure, scalable cloud infrastructure on AWS. Following these guidelines ensures:
- Network topologies enforce multi-availability zone isolation across segregated public, private, and database tiers.
- IAM permissions strictly enforce the principle of least privilege using condition keys and role-based federation.
- S3 data stores are protected against public exposure, transit tampering, and unauthorized decryption.
- Compute services (Lambda, ECS, EKS) utilize fine-grained runtime task roles without hardcoded credentials.
- Auditing trails and system telemetry are centrally captured and tamper-proofed.

---

## Core Principles & Rules

1. **IAM Principle of Least Privilege and Ambient Identity**:
   - Never generate permanent IAM user access keys (`AKIA...`) for applications. Use IAM Roles assumed via AWS STS, OIDC federation (for GitHub Actions / GitLab), or instance/pod profiles.
   - Restrict actions to specific ARNs. Avoid wildcard actions (`"Action": "*"`) or resource wildcards (`"Resource": "*"`) on sensitive services (KMS, S3, IAM, SecretsManager).
   - Enforce IAM Conditions: require multi-factor authentication (`aws:MultiFactorAuthPresent`), secure transport (`aws:SecureTransport`), and source VPC restrictions where applicable.

2. **Multi-AZ Network Isolation (The 3-Tier VPC Architecture)**:
   - Deploy across a minimum of two (preferably three) distinct Availability Zones per region.
   - Separate subnets into three functional tiers:
     - **Public Subnet**: Internet-facing load balancers (ALB) and NAT Gateways only. Never host application databases or business logic here.
     - **Private Subnet**: Application services (ECS, EKS worker nodes, EC2, Lambda in VPC) with route to NAT Gateway for outbound traffic.
     - **Isolated Subnet**: Databases and caches (RDS, Aurora, ElastiCache) with zero internet routes (no IGW, no NAT). Access via private subnet security groups only.
   - Use AWS PrivateLink / VPC Endpoints for S3, DynamoDB, SSM, and ECR to eliminate expensive NAT Gateway bandwidth for AWS API calls.

3. **Fortify S3 Buckets by Default**:
   - Enable S3 Block Public Access at the account and bucket levels.
   - Require Server-Side Encryption with AWS KMS (SSE-KMS) using Customer Managed Keys (CMK) with annual rotation enabled.
   - Enforce SSL/TLS transit in the Bucket Policy by denying any request where `aws:SecureTransport: false`.
   - Enable S3 Versioning and Object Lock on mission-critical state and backup buckets.

4. **Select Appropriate Compute Isolation**:
   - **AWS Lambda**: Best for event-driven, sporadic, or asynchronous pipelines with runtime < 15 minutes. Must execute inside VPC when accessing private databases.
   - **AWS ECS (Fargate)**: Ideal for containerized microservices requiring serverless operations, fast cold starts, and simple task definition contracts.
   - **AWS EKS**: Suited for complex container orchestrations requiring Kubernetes ecosystem tools (ArgoCD, Istio, cert-manager), using IAM Roles for Service Accounts (IRSA) or EKS Pod Identity.

5. **Universal Observability and Immutable Auditing**:
   - Enable multi-region AWS CloudTrail logging management and data events, storing logs in a dedicated, tamper-proof audit S3 bucket with log file validation enabled.
   - Enable VPC Flow Logs to monitor rejected network connections.
   - Ship application metrics and structured JSON logs to CloudWatch Log Groups with explicit retention policies (e.g. 90 days or 365 days).

---

## Standard Workflows & Procedures

### Workflow: Designing an Isolated Application Environment

1. **VPC & Subnet Planning**:
   - Allocate a non-overlapping CIDR block (e.g., `10.100.0.0/16`).
   - Carve out `/20` subnets across 3 Availability Zones for public, private, and isolated tiers.
2. **Gateway & Route Table Configuration**:
   - Attach an Internet Gateway (IGW) to public subnets.
   - Deploy a NAT Gateway per AZ (for high-availability production) or single NAT for non-production.
   - Associate Private Subnets with NAT Gateway route tables (`0.0.0.0/0 -> nat-xxx`).
   - Associate Isolated Subnets with route tables containing only local routes.
3. **VPC Endpoints**:
   - Provision S3 Gateway Endpoint (free of charge) and interface endpoints for SSM, ECR, and CloudWatch.
4. **Security Group Micro-Segmentation**:
   - Allow ingress traffic strictly from the specific Security Group of upstream callers (e.g., RDS SG allows port 5432 only from App SG).
5. **Compute & Identity Provisioning**:
   - Create task execution roles (for image pulling and log publishing) and task roles (for application runtime permissions).
6. **Storage & Encryption**:
   - Create KMS Customer Managed Keys with rotation.
   - Apply bucket policies enforcing TLS and encryption.

---

## Real-World Examples & Patterns

### 1. Hardened S3 Bucket Policy (Enforcing TLS & KMS)

```json
{
  "Version": "2012-10-17",
  "Id": "EnforceSecurityStandards",
  "Statement": [
    {
      "Sid": "DenyNonTLSRequests",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::corp-production-artifacts",
        "arn:aws:s3:::corp-production-artifacts/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedObjectUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::corp-production-artifacts/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    }
  ]
}
```

### 2. Multi-Tier Security Group Association Pattern

```hcl
# Application Load Balancer Security Group (Public)
resource "aws_security_group" "alb" {
  name        = "production-alb-sg"
  description = "Controls traffic to public ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow outbound to Application Tier only"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

# ECS Container Security Group (Private)
resource "aws_security_group" "app" {
  name        = "production-app-sg"
  description = "Controls traffic to ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow traffic only from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Allow outbound traffic to database and endpoints"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.db.id]
  }
}

# RDS Postgres Database Security Group (Isolated)
resource "aws_security_group" "db" {
  name        = "production-db-sg"
  description = "Controls traffic to PostgreSQL database"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow PostgreSQL access strictly from ECS App tier"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    description = "No outbound access permitted"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = []
  }
}
```

### 3. Least-Privilege IAM ECS Task Role Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAppSecretRetrieval",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/order-service-*"
    },
    {
      "Sid": "AllowKMSDecryptForSecrets",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/b637f7a2-1111-2222-3333-444455556666"
    },
    {
      "Sid": "AllowS3ArtifactAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::corp-order-data-prod/*"
    }
  ]
}
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Security / Resiliency Failure | Production Resolution |
| :--- | :--- | :--- |
| **Placing Databases in Public Subnets** | Direct exposure to automated internet port scans, credential stuffing, and zero-day database exploits. | Place databases exclusively in isolated subnets with zero internet route table entries. |
| **Using Wildcard IAM Actions (`"Action": "*"`)** | Grants excessive capabilities; compromised workload can delete backups, alter IAM, or create compute. | Restrict IAM policies to explicit actions and specific resource ARNs. |
| **Security Groups using `0.0.0.0/0` Ingress** | Any node on the internet can probe database or internal management ports (SSH/RDP/Postgres). | Chain Security Groups together using security group references as source identifiers. |
| **Single Availability Zone Deployments** | AZ outage causes total service downtime, violating high-availability SLAs. | Spread compute and databases across at least 2 (preferably 3) distinct AZs using Multi-AZ RDS and ASGs. |
| **Disabling CloudTrail Log File Validation** | Attackers who compromise AWS account credentials can modify or delete forensic log entries undetected. | Enable CloudTrail log file integrity validation with digest files delivered to an isolated S3 bucket. |
| **Static IAM User Keys for CI/CD** | Hardcoded `AWS_ACCESS_KEY_ID` leaked in logs or source code gives permanent backdoor access. | Implement OpenID Connect (OIDC) federation with AWS IAM Roles for CI/CD systems. |

---

## Verification Checklist

When evaluating or designing AWS infrastructure architecture, verify each checkpoint:

- [ ] **Multi-AZ Availability**: Workloads, load balancers, and databases are distributed across >= 2 Availability Zones.
- [ ] **Subnet Segmentation**: 3 distinct subnet tiers (public, private, isolated) exist; databases reside in isolated subnets.
- [ ] **Security Group Chaining**: Security group ingress rules reference peer security group IDs rather than broad CIDRs.
- [ ] **IAM Least Privilege**: No IAM policy contains wildcard actions paired with wildcard resources (`"Action": "*", "Resource": "*"`).
- [ ] **S3 Public Access Block**: `BlockPublicAcls`, `IgnorePublicAcls`, `BlockPublicPolicy`, and `RestrictPublicBuckets` are true.
- [ ] **S3 TLS Enforcement**: Bucket policy explicitly denies requests where `aws:SecureTransport == false`.
- [ ] **KMS Encryption**: Storage (EBS, S3, RDS) uses Customer Managed Keys (CMK) with annual rotation enabled.
- [ ] **OIDC Federation**: External systems and CI/CD pipelines authenticate via STS AssumeRoleWithWebIdentity (no permanent keys).
- [ ] **Audit Trail Active**: Multi-region CloudTrail is active with log file validation enabled.

---

## Tooling & Reference Guides

- **AWS CLI Verification Commands**:
  ```bash
  # Verify S3 Public Access Block
  aws s3api get-public-access-block --bucket my-corp-bucket
  
  # Audit IAM Access Keys older than 90 days
  aws iam list-access-keys --user-name devops-bot
  
  # Inspect CloudTrail Status
  aws cloudtrail describe-trails
  ```
- **Security Assessment Tools**:
  - `prowler aws` (Comprehensive AWS security assessment against CIS benchmarks)
  - `scoutsuite aws` (Multi-cloud security auditing tool)
  - `checkov -d . --framework cloudformation terraform`
- **Official Documentation**:
  - [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
  - [AWS Security Best Practices](https://docs.aws.amazon.com/security/)
  - [AWS VPC Architecture Guidelines](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)

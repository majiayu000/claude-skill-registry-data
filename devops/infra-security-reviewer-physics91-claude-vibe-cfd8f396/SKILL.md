---
name: infra-security-reviewer
description: |
  WHEN: Infrastructure security audit, secrets management, network policies, compliance checks
  WHAT: Secrets scanning + Network policies + IAM/RBAC audit + Compliance validation + Security hardening
  WHEN NOT: Application security → security-scanner, Docker only → docker-reviewer
---

# Infrastructure Security Reviewer Skill

## Purpose
Reviews infrastructure configurations for security, compliance, and best practices.

## When to Use
- Infrastructure security audit
- Secrets management review
- Network policy review
- IAM/RBAC audit
- Compliance check (SOC2, HIPAA, PCI)

## Project Detection
- Terraform files with IAM/security resources
- Kubernetes NetworkPolicy, RBAC
- AWS/GCP/Azure security configs
- `.env` files, secret references

## Workflow

### Step 1: Analyze Project
```
**Cloud**: AWS/GCP/Azure
**IaC**: Terraform/Pulumi
**Secrets**: Vault/AWS Secrets Manager
**Compliance**: SOC2/HIPAA/PCI
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full security review (recommended)
- Secrets management
- Network security
- IAM and access control
- Compliance validation
multiSelect: true
```

## Detection Rules

### Secrets Management
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Hardcoded secrets | Use secret manager | CRITICAL |
| Secrets in env files | Use vault/KMS | CRITICAL |
| No secret rotation | Enable auto-rotation | HIGH |
| Secrets in logs | Mask in logging | CRITICAL |

```hcl
# BAD: Hardcoded secrets
resource "aws_db_instance" "main" {
  password = "SuperSecret123!"  # CRITICAL!
}

variable "api_key" {
  default = "sk-1234567890"  # CRITICAL!
}

# GOOD: Using AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# GOOD: Secret rotation
resource "aws_secretsmanager_secret_rotation" "db_password" {
  secret_id           = aws_secretsmanager_secret.db_password.id
  rotation_lambda_arn = aws_lambda_function.rotation.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

```yaml
# Kubernetes - BAD: Secret in plain text
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  password: cGFzc3dvcmQxMjM=  # Just base64, not encrypted!

# GOOD: External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: db-secret
  data:
    - secretKey: password
      remoteRef:
        key: prod/db/password
```

### Network Security
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Public subnet for DB | Use private subnet | CRITICAL |
| No network policies | Add K8s NetworkPolicy | HIGH |
| Open security groups | Restrict to needed ports | CRITICAL |
| No VPC flow logs | Enable flow logs | MEDIUM |

```hcl
# AWS - GOOD: Network segmentation
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
  iam_role_arn    = aws_iam_role.flow_logs.arn
}

# Security group - least privilege
resource "aws_security_group" "app" {
  name        = "app-sg"
  description = "Application security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTPS from ALB"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "HTTPS to internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

```yaml
# Kubernetes NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: production
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:  # Allow DNS
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### IAM / Access Control
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Wildcard permissions | Use specific resources | CRITICAL |
| No MFA requirement | Require MFA | HIGH |
| Long-lived credentials | Use OIDC/roles | HIGH |
| Over-permissive roles | Apply least privilege | HIGH |

```hcl
# BAD: Overly permissive
resource "aws_iam_policy" "bad" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# GOOD: Least privilege
resource "aws_iam_policy" "app" {
  name        = "app-policy"
  description = "Application specific permissions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3ReadWrite"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "${aws_s3_bucket.app.arn}/*"
        ]
      },
      {
        Sid    = "SecretsRead"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          aws_secretsmanager_secret.app.arn
        ]
        Condition = {
          StringEquals = {
            "aws:ResourceTag/Environment" = var.environment
          }
        }
      }
    ]
  })
}

# GOOD: OIDC for GitHub Actions
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.github.certificates[0].sha1_fingerprint]
}

resource "aws_iam_role" "github_actions" {
  name = "github-actions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:myorg/myrepo:*"
        }
      }
    }]
  })
}
```

### Encryption
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Unencrypted storage | Enable encryption at rest | HIGH |
| No TLS | Enforce TLS 1.2+ | HIGH |
| Default KMS key | Use customer managed key | MEDIUM |

```hcl
# GOOD: Encryption at rest
resource "aws_s3_bucket_server_side_encryption_configuration" "app" {
  bucket = aws_s3_bucket.app.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.app.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_rds_cluster" "main" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn
}

# GOOD: Enforce TLS
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main.arn
}
```

### Compliance Checklist
```
## SOC2 / HIPAA / PCI Compliance

### Access Control
[ ] MFA enforced for all users
[ ] Least privilege IAM policies
[ ] Regular access reviews
[ ] Service accounts with minimal permissions

### Data Protection
[ ] Encryption at rest (S3, RDS, EBS)
[ ] Encryption in transit (TLS 1.2+)
[ ] Customer managed KMS keys
[ ] Key rotation enabled

### Network Security
[ ] VPC with private subnets
[ ] Security groups with least privilege
[ ] Network segmentation
[ ] VPC flow logs enabled

### Logging & Monitoring
[ ] CloudTrail enabled
[ ] GuardDuty enabled
[ ] Config rules for compliance
[ ] Alerting on security events

### Secrets Management
[ ] No hardcoded secrets
[ ] Secrets in Secrets Manager/Vault
[ ] Automatic rotation enabled
[ ] Audit logging for secret access
```

## Response Template
```
## Infrastructure Security Review Results

**Project**: [name]
**Cloud**: AWS | **IaC**: Terraform

### Secrets Management
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | rds.tf:15 | Hardcoded database password |

### Network Security
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | sg.tf:23 | Security group allows 0.0.0.0/0 |

### IAM
| Status | File | Issue |
|--------|------|-------|
| HIGH | iam.tf:45 | Wildcard permissions in policy |

### Encryption
| Status | File | Issue |
|--------|------|-------|
| HIGH | s3.tf:12 | S3 bucket not encrypted |

### Recommended Actions
1. [ ] Move secrets to AWS Secrets Manager
2. [ ] Restrict security group ingress rules
3. [ ] Apply least privilege to IAM policies
4. [ ] Enable encryption for all storage
```

## Best Practices
1. **Secrets**: Never hardcode, use secret managers
2. **Network**: Private subnets, strict security groups
3. **IAM**: Least privilege, no wildcards
4. **Encryption**: At rest and in transit
5. **Audit**: Enable logging everywhere

## Integration
- `terraform-reviewer`: IaC review
- `k8s-reviewer`: Kubernetes security
- `security-scanner`: Application security

---
name: terraform-reviewer
description: |
  WHEN: Terraform code review, module structure, state management, security policies
  WHAT: Module organization + State backend + Security policies + Variable validation + Best practices
  WHEN NOT: Kubernetes → k8s-reviewer, Docker → docker-reviewer
---

# Terraform Reviewer Skill

## Purpose
Reviews Terraform code for module structure, state management, security, and best practices.

## When to Use
- Terraform code review
- Module structure review
- State backend configuration
- Security policy review
- Variable and output review

## Project Detection
- `*.tf` files in project
- `main.tf`, `variables.tf`, `outputs.tf`
- `modules/` directory
- `terraform.tfvars`

## Workflow

### Step 1: Analyze Project
```
**Terraform**: 1.6+
**Provider**: AWS/GCP/Azure
**Backend**: S3/GCS/Azure Blob
**Modules**: Custom + Registry
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full Terraform review (recommended)
- Module structure
- State management
- Security and compliance
- Variable validation
multiSelect: true
```

## Detection Rules

### Module Structure
| Check | Recommendation | Severity |
|-------|----------------|----------|
| All resources in main.tf | Split by resource type | MEDIUM |
| No modules | Extract reusable modules | MEDIUM |
| Hardcoded values | Use variables | HIGH |
| No outputs | Add relevant outputs | MEDIUM |

```
# GOOD: Project structure
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── eks/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── README.md
```

```hcl
# BAD: Hardcoded values
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}

# GOOD: Parameterized with variables
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Instance type must be t3 family."
  }
}

variable "environment" {
  description = "Environment name"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  tags = merge(local.common_tags, {
    Name = "${var.project}-${var.environment}-web"
  })
}
```

### State Management
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Local state | Use remote backend | CRITICAL |
| No state locking | Enable DynamoDB/GCS lock | HIGH |
| No state encryption | Enable encryption | HIGH |
| Shared state file | Split by environment | MEDIUM |

```hcl
# BAD: Local state (default)
# No backend configuration

# GOOD: Remote backend with locking
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# For GCP
terraform {
  backend "gcs" {
    bucket  = "mycompany-terraform-state"
    prefix  = "prod/vpc"
  }
}
```

### Security
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Secrets in tfvars | Use secret manager | CRITICAL |
| Public S3 bucket | Set ACL private | CRITICAL |
| Open security group | Restrict CIDR | CRITICAL |
| No encryption | Enable encryption | HIGH |

```hcl
# BAD: Security issues
resource "aws_security_group" "web" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Wide open!
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
  acl    = "public-read"  # Public!
}

# GOOD: Secure configuration
resource "aws_security_group" "web" {
  name        = "${var.project}-web-sg"
  description = "Security group for web servers"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTPS from load balancer"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}

resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-${var.environment}-data"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}
```

### Variable Validation
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No type constraint | Add type | MEDIUM |
| No validation | Add validation block | MEDIUM |
| No description | Add description | LOW |
| Sensitive not marked | Add sensitive = true | HIGH |

```hcl
# GOOD: Well-defined variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "Must be a valid CIDR block."
  }
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # Won't show in logs

  validation {
    condition     = length(var.db_password) >= 16
    error_message = "Password must be at least 16 characters."
  }
}

variable "allowed_environments" {
  description = "List of allowed environment names"
  type        = list(string)
  default     = ["dev", "staging", "prod"]
}
```

### Resource Naming
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Inconsistent naming | Use naming convention | MEDIUM |
| No tags | Add standard tags | MEDIUM |

```hcl
# GOOD: Consistent naming and tagging
locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.owner
  }
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-vpc"
  })
}
```

## Response Template
```
## Terraform Review Results

**Project**: [name]
**Terraform**: 1.6 | **Provider**: AWS

### Module Structure
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | main.tf | 500+ lines, should split |

### State Management
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | - | Using local state |

### Security
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | security.tf:23 | Security group allows 0.0.0.0/0 |

### Variables
| Status | File | Issue |
|--------|------|-------|
| HIGH | variables.tf | db_password not marked sensitive |

### Recommended Actions
1. [ ] Configure remote state backend with locking
2. [ ] Restrict security group ingress rules
3. [ ] Mark sensitive variables
4. [ ] Split main.tf into logical files
```

## Best Practices
1. **Structure**: Separate by environment, use modules
2. **State**: Remote backend with locking and encryption
3. **Security**: No secrets in code, least privilege
4. **Variables**: Type constraints, validation, descriptions
5. **Naming**: Consistent convention, standard tags

## Integration
- `k8s-reviewer`: EKS/GKE cluster configs
- `infra-security-reviewer`: Compliance checks
- `ci-cd-reviewer`: Terraform in pipelines

---
name: terraform-specialist
description: Infrastructure as Code expertise with Terraform/OpenTofu for cloud provisioning. Use when writing Terraform modules, managing state, configuring.
---

# Terraform Specialist

Specialized expertise in Infrastructure as Code using Terraform/OpenTofu, providing guidance on module design, state management, security practices, and production-grade infrastructure provisioning across major cloud providers.

## When to Use This Skill

Use this skill for:

- Writing or reviewing Terraform configurations
- Designing reusable Terraform modules
- Managing Terraform state (remote backends, locking)
- Multi-environment infrastructure (dev/staging/prod)
- Cloud resource provisioning (AWS, Azure, GCP)
- Infrastructure security and compliance
- Migrating from manual infrastructure to IaC
- Debugging Terraform plan/apply issues

**Trigger phrases**: "terraform", "infrastructure as code", "IaC", "HCL", "tofu", "opentofu", "tfstate", "terraform module", "cloud provisioning"

## What This Skill Does

Provides production-ready Terraform patterns including:

- **Module Design**: Composable, reusable, versioned modules
- **State Management**: Remote backends, state locking, workspaces
- **Security**: Secrets handling, least privilege IAM, encryption
- **Testing**: Terratest, policy-as-code with Sentinel/OPA
- **CI/CD Integration**: Automated plan/apply workflows
- **Multi-Cloud**: Patterns for AWS, Azure, GCP deployments

## Instructions

### Step 1: Establish Project Structure

**Recommended Directory Structure**:

```
infrastructure/
├── modules/                    # Reusable modules
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   └── database/
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── .terraform-version          # tfenv version pinning
├── .gitignore
└── README.md
```

**Essential .gitignore**:

```gitignore
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Sensitive variable files
*.tfvars
!example.tfvars

# Override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# CLI configuration files
.terraformrc
terraform.rc
```

### Step 2: Configure Remote State

**AWS S3 Backend (Recommended)**:

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "environments/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"

    # Assume role for cross-account access
    role_arn       = "arn:aws:iam::123456789012:role/TerraformStateAccess"
  }
}
```

**State Lock Table (DynamoDB)**:

```hcl
resource "aws_dynamodb_table" "terraform_lock" {
  name           = "terraform-state-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Purpose = "Terraform state locking"
  }
}
```

### Step 3: Write Quality Modules

**Module Structure Template**:

```hcl
# modules/networking/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.environment}-vpc"
  })
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]

  tags = merge(var.tags, {
    Name = "${var.environment}-private-${count.index + 1}"
    Tier = "private"
  })
}
```

```hcl
# modules/networking/variables.tf
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/networking/outputs.tf
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}
```

### Step 4: Implement Security Best Practices

**Sensitive Variable Handling**:

```hcl
variable "database_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# Use AWS Secrets Manager instead of variables
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/master-password"
}

resource "aws_db_instance" "main" {
  # ... other config ...
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

**Least Privilege IAM**:

```hcl
# IAM role for EC2 with minimal permissions
resource "aws_iam_role" "app" {
  name = "${var.environment}-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "app" {
  name = "${var.environment}-app-policy"
  role = aws_iam_role.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.app_data.arn,
          "${aws_s3_bucket.app_data.arn}/*"
        ]
      }
    ]
  })
}
```

**Encryption Configuration**:

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "${var.environment}-app-data"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.data.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### Step 5: Multi-Environment Configuration

**Using Workspaces** (simple projects):

```bash
# Create and switch workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
terraform workspace select prod
```

```hcl
# Reference workspace in configuration
locals {
  environment = terraform.workspace

  config = {
    dev = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 2
    }
    staging = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 4
    }
    prod = {
      instance_type = "t3.large"
      min_size      = 3
      max_size      = 10
    }
  }
}

resource "aws_instance" "app" {
  instance_type = local.config[local.environment].instance_type
  # ...
}
```

**Using Separate Directories** (complex projects):

```hcl
# environments/prod/main.tf
module "networking" {
  source = "../../modules/networking"

  environment        = "prod"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  tags = local.common_tags
}

module "compute" {
  source = "../../modules/compute"

  environment    = "prod"
  vpc_id         = module.networking.vpc_id
  subnet_ids     = module.networking.private_subnet_ids
  instance_type  = "t3.large"
  min_size       = 3
  max_size       = 10

  tags = local.common_tags
}
```

### Step 6: Testing Infrastructure

**Terratest Example**:

```go
// test/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../modules/networking",
        Vars: map[string]interface{}{
            "environment":        "test",
            "vpc_cidr":           "10.99.0.0/16",
            "availability_zones": []string{"us-east-1a", "us-east-1b"},
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)
}
```

**Policy as Code (OPA)**:

```rego
# policy/terraform.rego
package terraform

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    not resource.change.after.server_side_encryption_configuration
    msg := sprintf("S3 bucket %v must have encryption enabled", [resource.address])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group_rule"
    resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
    resource.change.after.from_port == 22
    msg := sprintf("Security group %v allows SSH from 0.0.0.0/0", [resource.address])
}
```

## Best Practices

- **Pin provider versions** - Use `~>` for minor updates, exact for critical
- **Use remote state** - Never store state locally for team projects
- **Enable state locking** - Prevent concurrent modifications
- **Mark sensitive outputs** - Use `sensitive = true` for secrets
- **Validate inputs** - Add validation blocks to variables
- **Use locals for computed values** - Keep configurations DRY
- **Tag all resources** - Consistent tagging for cost allocation
- **Document modules** - README with examples for every module
- **Run `terraform fmt`** - Consistent formatting
- **Use `-target` sparingly** - It can lead to state drift

## Common Patterns

### Pattern 1: Data Lookup Instead of Hardcoding

```hcl
# Instead of hardcoding AMI IDs
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "app" {
  ami = data.aws_ami.ubuntu.id
  # ...
}
```

### Pattern 2: Conditional Resource Creation

```hcl
variable "create_bastion" {
  description = "Whether to create a bastion host"
  type        = bool
  default     = false
}

resource "aws_instance" "bastion" {
  count = var.create_bastion ? 1 : 0

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  # ...
}

output "bastion_ip" {
  value = var.create_bastion ? aws_instance.bastion[0].public_ip : null
}
```

### Pattern 3: For_each with Maps

```hcl
variable "buckets" {
  description = "Map of S3 buckets to create"
  type = map(object({
    versioning = bool
    lifecycle_days = number
  }))
  default = {
    logs = {
      versioning = false
      lifecycle_days = 30
    }
    backups = {
      versioning = true
      lifecycle_days = 90
    }
  }
}

resource "aws_s3_bucket" "buckets" {
  for_each = var.buckets
  bucket   = "${var.environment}-${each.key}"
}

resource "aws_s3_bucket_versioning" "buckets" {
  for_each = { for k, v in var.buckets : k => v if v.versioning }
  bucket   = aws_s3_bucket.buckets[each.key].id

  versioning_configuration {
    status = "Enabled"
  }
}
```

## Quality Checklist

- [ ] Provider versions pinned
- [ ] Remote state configured with locking
- [ ] Sensitive variables marked as sensitive
- [ ] Input validation on all variables
- [ ] All resources tagged consistently
- [ ] Modules have README documentation
- [ ] No hardcoded values (use variables/data sources)
- [ ] Security groups follow least privilege
- [ ] Encryption enabled for storage resources
- [ ] `terraform fmt` and `terraform validate` pass

## Related Skills

- `cloud-architect` - Cloud architecture patterns
- `cicd-architect` - Terraform CI/CD pipelines
- `kubernetes-expert` - EKS/AKS/GKE provisioning
- `security-review` - Infrastructure security assessment

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: awesome-claude-code-subagents patterns, HashiCorp best practices


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.

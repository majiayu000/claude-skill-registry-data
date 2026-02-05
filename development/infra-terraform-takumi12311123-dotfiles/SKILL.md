---
name: infra-terraform
description: Enforces Terraform best practices for safe and scalable infrastructure as code. Emphasizes modularity, state management, and security. Automatically applied for IaC implementation.
metadata:
  context: terraform, infrastructure, iac, aws, gcp, azure
  auto-trigger: true
---

# Infrastructure as Code with Terraform

## Overview

This skill provides best practices for Terraform infrastructure management. It emphasizes module design, state management, security, and CI/CD integration to build reliable infrastructure.

## Auto-Trigger Conditions

This skill is automatically applied when:

- Creating or editing Terraform files (`.tf`, `.tfvars`)
- Infrastructure provisioning tasks
- Cloud resource management
- Keywords like "infrastructure", "Terraform" are mentioned

## Project Structure

### Root Module Structure

```bash
terraform-project/
├── environments/              # Environment-specific root modules
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/                   # Reusable modules
│   ├── network/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   │   └── ...
│   └── database/
│       └── ...
├── .terraform.lock.hcl       # Provider version lock
├── .gitignore
└── README.md
```

### File Naming Conventions

- `main.tf` - Main resource definitions
- `variables.tf` - Input variable declarations
- `outputs.tf` - Output value declarations
- `versions.tf` - Terraform/provider versions
- `backend.tf` - Remote backend configuration
- `data.tf` - Data source definitions (optional)
- `locals.tf` - Local variable definitions (optional)

## Module Design Principles

### 1. Standard Module Structure

```hcl
# modules/network/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-vpc"
    }
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-public-subnet-${count.index + 1}"
      Type = "public"
    }
  )
}

# modules/network/variables.tf
variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
  validation {
    condition = alltrue([
      for cidr in var.public_subnet_cidrs : can(cidrnetmask(cidr))
    ])
    error_message = "All subnet CIDRs must be valid CIDR blocks."
  }
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# modules/network/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}
```

### 2. Module Invocation

```hcl
# environments/prod/main.tf
module "network" {
  source = "../../modules/network"

  environment          = "prod"
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  availability_zones   = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]

  tags = local.common_tags
}

module "compute" {
  source = "../../modules/compute"

  environment    = "prod"
  vpc_id         = module.network.vpc_id
  subnet_ids     = module.network.public_subnet_ids
  instance_type  = "t3.medium"

  tags = local.common_tags
}
```

## State Management Best Practices

### 1. Remote Backend Configuration (S3 + DynamoDB)

```hcl
# environments/prod/backend.tf
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state-prod"
    key            = "prod/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock-prod"

    # Enable versioning (recommended)
    versioning     = true
  }
}
```

### 2. State File Isolation

```bash
# Separate by environment
environments/
├── dev/     # dev environment state
├── staging/ # staging environment state
└── prod/    # prod environment state (most strictly managed)

# Or use workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
```

### 3. State Locking

```hcl
# Create DynamoDB table (for AWS)
resource "aws_dynamodb_table" "terraform_lock" {
  name           = "terraform-state-lock-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform State Lock Table"
    Environment = var.environment
  }
}
```

## Version Management

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}
```

## Variables and Environment Management

### 1. Variable Definitions

```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 1

  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}

variable "enable_monitoring" {
  description = "Enable detailed monitoring"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

### 2. tfvars Files

```hcl
# environments/prod/terraform.tfvars
environment = "prod"
aws_region  = "ap-northeast-1"

instance_count     = 3
instance_type      = "t3.large"
enable_monitoring  = true

tags = {
  Project     = "MyApp"
  ManagedBy   = "Terraform"
  CostCenter  = "Engineering"
}
```

### 3. Local Variables

```hcl
# locals.tf
locals {
  common_tags = merge(
    var.tags,
    {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Timestamp   = timestamp()
    }
  )

  # Environment-specific configuration
  instance_type = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.large"
  }

  current_instance_type = local.instance_type[var.environment]
}
```

## Security Best Practices

### 1. Secret Management

```hcl
# ❌ BAD - Hardcoded secrets
resource "aws_db_instance" "bad" {
  password = "hardcoded-password"  # Never do this
}

# ✅ GOOD - Use Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "good" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# ✅ GOOD - Use environment variables
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### 2. Sensitive Data Masking

```hcl
variable "api_key" {
  description = "API key for external service"
  type        = string
  sensitive   = true
}

output "connection_string" {
  description = "Database connection string"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

### 3. IAM Policies (Least Privilege Principle)

```hcl
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
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.app.arn}/*"
      }
    ]
  })
}
```

## Resource Naming Conventions

```hcl
# Naming pattern: {environment}-{service}-{resource-type}-{index}
resource "aws_instance" "web" {
  count = var.instance_count

  tags = {
    Name = "${var.environment}-web-server-${count.index + 1}"
  }
}

# Example: prod-web-server-1, prod-web-server-2, prod-web-server-3
```

## Data Source Usage

```hcl
# Reference existing resources
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

data "aws_vpc" "existing" {
  id = var.vpc_id
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  subnet_id     = data.aws_vpc.existing.subnet_ids[0]
}
```

## Conditionals and Loops

### 1. count

```hcl
resource "aws_instance" "web" {
  count = var.create_instances ? var.instance_count : 0

  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
}
```

### 2. for_each

```hcl
variable "users" {
  type = map(object({
    role = string
  }))
  default = {
    "alice" = { role = "admin" }
    "bob"   = { role = "developer" }
  }
}

resource "aws_iam_user" "users" {
  for_each = var.users

  name = each.key
  tags = {
    Role = each.value.role
  }
}
```

### 3. dynamic blocks

```hcl
resource "aws_security_group" "app" {
  name   = "${var.environment}-app-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

## CI/CD Integration

### 1. GitHub Actions Example

```yaml
# .github/workflows/terraform.yml
name: Terraform CI/CD

on:
  pull_request:
    paths:
      - 'terraform/**'
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init
        working-directory: ./environments/prod

      - name: Terraform Validate
        run: terraform validate
        working-directory: ./environments/prod

      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: ./environments/prod

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
        working-directory: ./environments/prod
```

### 2. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
      - id: terraform_tflint
```

## Implementation Checklist

### Design Phase
- [ ] Decide environment isolation strategy (directory vs workspace)
- [ ] Define module boundaries
- [ ] Establish naming conventions
- [ ] Determine tagging strategy

### Implementation Phase
- [ ] Configure remote backend
- [ ] Pin provider versions
- [ ] Add variable validation
- [ ] Mark sensitive variables
- [ ] Create module READMEs
- [ ] Reference existing resources with data sources

### Security
- [ ] Don't hardcode secrets
- [ ] Use least privilege IAM policies
- [ ] Encrypt state files
- [ ] Exclude sensitive files in .gitignore

### Testing & Deployment
- [ ] Format with `terraform fmt`
- [ ] Validate with `terraform validate`
- [ ] Review changes with `terraform plan`
- [ ] Automate drift detection
- [ ] Build CI/CD pipeline

## Best Practices

### DO ✅
- Keep modules small (single responsibility)
- Use remote backends
- Exclude state files from version control
- Commit .terraform.lock.hcl
- Apply tags consistently
- Keep documentation up to date
- Run terraform fmt

### DON'T ❌
- Don't create mega-modules
- Don't hardcode secrets
- Don't commit state files to git
- Don't leave provider versions unpinned
- Don't casually run `terraform destroy` in production
- Don't duplicate code across environments

## Troubleshooting

```bash
# Show state file
terraform show

# List state file contents
terraform state list

# Show specific resource details
terraform state show aws_instance.web[0]

# Import existing resources
terraform import aws_instance.web i-1234567890abcdef0

# Refresh state (fix drift)
terraform refresh

# Detect drift
terraform plan -detailed-exitcode
```

## Cost Optimization

```hcl
# Cost allocation via tags
locals {
  cost_tags = {
    CostCenter  = var.cost_center
    Project     = var.project_name
    Environment = var.environment
  }
}

# Auto-shutdown for non-production (example)
resource "aws_instance" "app" {
  # ... other configuration ...

  # Only run in production 24/7
  count = var.environment == "prod" ? var.instance_count : 0

  tags = merge(
    local.cost_tags,
    {
      AutoShutdown = var.environment != "prod" ? "true" : "false"
    }
  )
}
```

## Summary

This skill ensures:

- 🏗️ **Modularity**: Reusable and maintainable code
- 🔒 **Security**: Secret management and least privilege
- 📊 **State Management**: Safe remote backend with locking
- 🚀 **CI/CD**: Automated deployments
- 💰 **Cost Optimization**: Tagging and resource management
- 📚 **Documentation**: Clear module descriptions

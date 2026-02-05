---
name: terraform-specialist
description: "[Extends devops-engineer] Terraform/OpenTofu specialist. Use for advanced Terraform modules, multi-cloud providers, state management, workspaces, CI/CD for IaC. Invoke alongside devops-engineer for complex IaC projects."
---

# Terraform Specialist

> **Extends:** devops-engineer
> **Type:** Specialized Skill

## Trigger

Use this skill alongside `devops-engineer` when:
- Writing Terraform configurations
- Creating reusable Terraform modules
- Managing Terraform state
- Implementing workspaces or environments
- Setting up CI/CD for infrastructure
- Working with AWS, GCP, or Azure providers
- Migrating to OpenTofu
- Troubleshooting Terraform issues

## Context

You are a Senior Terraform Specialist with 6+ years of experience managing infrastructure as code. You have designed and maintained Terraform configurations for production systems at scale. You follow HashiCorp best practices and understand multi-cloud deployments.

## Expertise

### Versions

| Technology | Version | Notes |
|------------|---------|-------|
| Terraform | 1.10+ | Latest stable |
| OpenTofu | 1.9+ | Open-source fork |
| AWS Provider | 5.x | Amazon Web Services |
| Google Provider | 6.x | Google Cloud Platform |
| Azure Provider | 4.x | Microsoft Azure |

### Core Concepts

#### Provider Configuration

```hcl
# versions.tf
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "eu-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}
```

#### Variables and Outputs

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_config" {
  description = "EC2 instance configuration"
  type = object({
    instance_type = string
    volume_size   = number
    enable_monitoring = optional(bool, true)
  })

  default = {
    instance_type = "t3.micro"
    volume_size   = 20
  }
}

variable "allowed_cidrs" {
  description = "List of allowed CIDR blocks"
  type        = list(string)
  default     = []
  sensitive   = false
}

variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}

# outputs.tf
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "database_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

#### Resource Patterns

```hcl
# main.tf
locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = merge(var.tags, {
    Environment = var.environment
    Project     = var.project_name
  })
}

# VPC with multiple AZs
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-vpc"
  })
}

# Subnets using count
resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-public-${count.index + 1}"
    Tier = "public"
  })
}

# Subnets using for_each
resource "aws_subnet" "private" {
  for_each = toset(var.availability_zones)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, index(var.availability_zones, each.value) + 10)
  availability_zone = each.value

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-private-${each.key}"
    Tier = "private"
  })
}

# Dynamic blocks
resource "aws_security_group" "web" {
  name        = "${local.name_prefix}-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}
```

#### Module Structure

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(var.tags, {
    Name = var.name
  })
}

# modules/vpc/variables.tf
variable "name" {
  description = "Name of the VPC"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string

  validation {
    condition     = can(cidrnetmask(var.cidr_block))
    error_message = "Must be a valid CIDR block."
  }
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in the VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in the VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to the VPC"
  type        = map(string)
  default     = {}
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.this.id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.this.cidr_block
}

# Module usage
module "vpc" {
  source = "./modules/vpc"

  name       = "${var.project_name}-${var.environment}"
  cidr_block = "10.0.0.0/16"

  tags = {
    Environment = var.environment
  }
}
```

#### Data Sources and Moved Blocks

```hcl
# Data sources
data "aws_availability_zones" "available" {
  state = "available"

  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

data "aws_caller_identity" "current" {}

# Moved blocks for refactoring
moved {
  from = aws_instance.web
  to   = aws_instance.application
}

moved {
  from = module.old_vpc
  to   = module.vpc
}
```

#### Import and State Management

```hcl
# Import block (Terraform 1.5+)
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket"
}

resource "aws_s3_bucket" "existing" {
  bucket = "my-existing-bucket"
}

# Generate configuration from import
# terraform plan -generate-config-out=generated.tf
```

### Workspaces and Environments

```hcl
# Using workspaces
locals {
  environment = terraform.workspace

  instance_types = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.medium"
  }

  instance_type = local.instance_types[local.environment]
}

# Alternative: tfvars per environment
# terraform apply -var-file=environments/prod.tfvars
```

### Testing with Terratest

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

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "name":       "test-vpc",
            "cidr_block": "10.0.0.0/16",
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)
}
```

### Project Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── eks/
│   ├── rds/
│   └── s3/
├── .terraform-version
├── .tflint.hcl
└── README.md
```

### CI/CD Pipeline

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'infrastructure/**'
  push:
    branches: [main]
    paths:
      - 'infrastructure/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.10.0

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init -backend=false

      - name: Terraform Validate
        run: terraform validate

      - name: TFLint
        uses: terraform-linters/setup-tflint@v4
      - run: tflint --init && tflint

  plan:
    needs: validate
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Plan
        run: |
          terraform init
          terraform plan -out=tfplan

      - name: Post Plan to PR
        uses: actions/github-script@v7
        with:
          script: |
            // Post plan output as PR comment
```

## Parent & Related Skills

| Skill | Relationship |
|-------|--------------|
| **devops-engineer** | Parent skill - invoke for Kubernetes, CI/CD, Docker |
| **secops-engineer** | For security policies, compliance requirements |
| **solution-architect** | For infrastructure architecture decisions |

## Standards

- **Remote state**: Always use remote state with locking
- **Modules**: Extract reusable patterns into modules
- **Validation**: Add input validation rules
- **Formatting**: Run `terraform fmt` before commit
- **Documentation**: Use terraform-docs for module docs
- **Versioning**: Pin provider versions
- **Naming**: Consistent naming conventions

## Checklist

### Before Writing Configuration
- [ ] State backend configured
- [ ] Provider versions pinned
- [ ] Variables validated
- [ ] Naming convention defined

### Before Applying
- [ ] Plan reviewed
- [ ] No sensitive data in state
- [ ] Backup state exists
- [ ] Team notified (for prod)

### Module Checklist
- [ ] README with examples
- [ ] Input validation
- [ ] All outputs documented
- [ ] Semantic versioning

## Anti-Patterns to Avoid

1. **Local state**: Always use remote state
2. **Hardcoded values**: Use variables
3. **No state locking**: Enable DynamoDB locking
4. **Large monolith**: Split into modules
5. **No versioning**: Pin all versions
6. **Missing validation**: Validate all inputs
7. **Secrets in state**: Use secrets manager

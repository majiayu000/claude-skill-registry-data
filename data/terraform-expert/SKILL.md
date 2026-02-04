---
name: terraform-expert
description: Infrastructure as Code with Terraform - modules, state management, and best practices.
---

# Terraform Expert

## Project Structure

```
terraform/
├── modules/
│   ├── vpc/
│   ├── ecs/
│   └── rds/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── main.tf
├── variables.tf
├── outputs.tf
└── versions.tf
```

## Module Pattern

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

# modules/vpc/variables.tf
variable "name" {
  type        = string
  description = "Name prefix for resources"
}

variable "cidr_block" {
  type        = string
  default     = "10.0.0.0/16"
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.main.id
}
```

## State Management

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "env/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

## Best Practices

- **One module per concern** - VPC, compute, database separate
- **Lock versions** - Provider and module versions
- **Use workspaces** - Or separate state files per env
- **Validate before apply** - `terraform plan` always
- **Format code** - `terraform fmt -recursive`

## Common Patterns

### For Each

```hcl
variable "subnets" {
  type = map(object({
    cidr = string
    az   = string
  }))
}

resource "aws_subnet" "main" {
  for_each          = var.subnets
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az

  tags = { Name = each.key }
}
```

### Data Sources

```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

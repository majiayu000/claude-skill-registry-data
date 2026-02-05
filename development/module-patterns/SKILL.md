---
name: module-patterns
description: Terraform module development patterns and best practices. Provides structure, versioning, and output scaffolds. Use when creating reusable modules.
---

# Module Patterns

Terraform module development patterns and conventions.

## Module Structure

### Standard Layout
```
modules/
└── <module-name>/
    ├── main.tf           # Primary resources
    ├── variables.tf      # Input variables
    ├── outputs.tf        # Module outputs
    ├── versions.tf       # Version constraints
    ├── locals.tf         # Local values
    ├── data.tf           # Data sources (optional)
    ├── README.md         # Documentation
    ├── examples/
    │   ├── basic/
    │   │   ├── main.tf
    │   │   ├── outputs.tf
    │   │   └── README.md
    │   └── complete/
    │       ├── main.tf
    │       ├── outputs.tf
    │       └── README.md
    └── tests/
        ├── basic.tftest.hcl
        └── complete.tftest.hcl
```

## versions.tf Pattern

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}
```

## variables.tf Patterns

### Required Variable
```hcl
variable "project" {
  description = "Project name used in resource naming"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*$", var.project))
    error_message = "Project name must start with a letter and contain only lowercase letters, numbers, and hyphens."
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
```

### Optional with Default
```hcl
variable "instance_type" {
  description = "EC2 instance type for compute resources"
  type        = string
  default     = "t3.medium"
}

variable "enable_encryption" {
  description = "Enable encryption at rest for all supported resources"
  type        = bool
  default     = true
}
```

### Complex Type with Defaults
```hcl
variable "node_groups" {
  description = "Map of EKS managed node group definitions"
  type = map(object({
    instance_types = list(string)
    min_size       = number
    max_size       = number
    desired_size   = number
    disk_size      = optional(number, 100)
    disk_type      = optional(string, "gp3")
    capacity_type  = optional(string, "ON_DEMAND")
    labels         = optional(map(string), {})
    taints = optional(list(object({
      key    = string
      value  = string
      effect = string
    })), [])
  }))
  default = {}
}
```

### Sensitive Variable
```hcl
variable "database_password" {
  description = "Database master password"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.database_password) >= 16
    error_message = "Database password must be at least 16 characters."
  }
}
```

### Tags Variable
```hcl
variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

## outputs.tf Patterns

### Resource Identifiers
```hcl
output "id" {
  description = "The ID of the primary resource"
  value       = aws_resource.this.id
}

output "arn" {
  description = "The ARN of the primary resource"
  value       = aws_resource.this.arn
}
```

### Connection Information
```hcl
output "endpoint" {
  description = "Endpoint for connecting to the resource"
  value       = aws_resource.this.endpoint
}

output "security_group_id" {
  description = "ID of the associated security group"
  value       = aws_security_group.this.id
}
```

### Sensitive Outputs
```hcl
output "connection_string" {
  description = "Database connection string"
  value       = "postgres://${var.username}:${random_password.db.result}@${aws_db_instance.this.endpoint}/${var.database_name}"
  sensitive   = true
}
```

### Conditional Outputs
```hcl
output "cluster_endpoint" {
  description = "EKS cluster endpoint (null if cluster not created)"
  value       = var.create_cluster ? module.eks[0].cluster_endpoint : null
}

output "private_subnets" {
  description = "List of private subnet IDs"
  value       = var.create_vpc ? module.vpc[0].private_subnets : var.private_subnet_ids
}
```

## locals.tf Patterns

### Name Construction
```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"

  resource_names = {
    cluster = "${local.name_prefix}-eks"
    vpc     = "${local.name_prefix}-vpc"
    rds     = "${local.name_prefix}-db"
  }
}
```

### Tag Merging
```hcl
locals {
  default_tags = {
    Project     = var.project
    Environment = var.environment
    Terraform   = "true"
    Module      = "module-name"
  }

  tags = merge(local.default_tags, var.tags)
}
```

### Configuration Defaults
```hcl
locals {
  node_group_defaults = {
    instance_types = ["m6i.large", "m5.large"]
    disk_size      = 100
    disk_type      = "gp3"
    capacity_type  = "ON_DEMAND"
  }

  node_groups = {
    for k, v in var.node_groups : k => merge(local.node_group_defaults, v)
  }
}
```

### Conditional Logic
```hcl
locals {
  create_kms_key = var.kms_key_arn == null
  kms_key_arn    = local.create_kms_key ? aws_kms_key.this[0].arn : var.kms_key_arn

  azs = var.azs != null ? var.azs : slice(data.aws_availability_zones.available.names, 0, 3)
}
```

## main.tf Patterns

### Conditional Resource Creation
```hcl
resource "aws_kms_key" "this" {
  count = var.create_kms_key ? 1 : 0

  description             = "KMS key for ${local.name_prefix}"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = local.tags
}
```

### For Each with Maps
```hcl
resource "aws_subnet" "private" {
  for_each = var.private_subnets

  vpc_id            = aws_vpc.this.id
  availability_zone = each.value.az
  cidr_block        = each.value.cidr

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-private-${each.key}"
    Type = "private"
  })
}
```

### Lifecycle Rules
```hcl
resource "aws_rds_cluster" "this" {
  cluster_identifier = local.resource_names.rds

  # ... configuration ...

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [master_password]
  }
}
```

### Timeouts
```hcl
resource "aws_eks_cluster" "this" {
  name = local.resource_names.cluster

  # ... configuration ...

  timeouts {
    create = "45m"
    update = "60m"
    delete = "30m"
  }
}
```

## Terraform Test Pattern

```hcl
# tests/basic.tftest.hcl

provider "aws" {
  region = "us-east-1"
}

variables {
  project     = "test"
  environment = "dev"
}

run "validate_resources" {
  command = plan

  assert {
    condition     = aws_s3_bucket.this.bucket != null
    error_message = "S3 bucket should be created"
  }

  assert {
    condition     = aws_s3_bucket.this.tags["Environment"] == "dev"
    error_message = "Environment tag should be 'dev'"
  }
}

run "validate_naming" {
  command = plan

  assert {
    condition     = can(regex("^test-dev-", aws_s3_bucket.this.bucket))
    error_message = "Bucket name should follow naming convention"
  }
}

run "validate_encryption" {
  command = plan

  variables {
    enable_encryption = true
  }

  assert {
    condition     = length(aws_s3_bucket_server_side_encryption_configuration.this) > 0
    error_message = "Encryption should be enabled"
  }
}
```

## README.md Template

```markdown
# Module Name

Brief description of what this module creates.

## Usage

```hcl
module "example" {
  source = "path/to/module"

  project     = "myapp"
  environment = "prod"

  # Additional configuration
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.5.0 |
| aws | >= 5.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 5.0 |

## Resources

| Name | Type |
|------|------|
| aws_resource.name | resource |
| aws_data.name | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| project | Project name | `string` | n/a | yes |
| environment | Environment | `string` | n/a | yes |
| tags | Additional tags | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource ID |
| arn | Resource ARN |

## Examples

- [Basic](./examples/basic) - Minimal configuration
- [Complete](./examples/complete) - Full-featured configuration

## License

Apache 2.0 Licensed.
```

## Example basic/main.tf

```hcl
provider "aws" {
  region = "us-east-1"
}

module "example" {
  source = "../../"

  project     = "myapp"
  environment = "dev"
}

output "id" {
  value = module.example.id
}
```

## Moved Blocks for Refactoring

```hcl
# moves.tf - Use when renaming resources
moved {
  from = aws_instance.web
  to   = aws_instance.application
}

moved {
  from = aws_s3_bucket.data
  to   = module.storage.aws_s3_bucket.main
}

moved {
  from = module.old_name
  to   = module.new_name
}
```

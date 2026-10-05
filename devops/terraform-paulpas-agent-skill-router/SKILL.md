---




name: terraform
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: Implements Terraform infrastructure as code for cloud provisioning with
  state management, modules, remote backends, and troubleshooting
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: code
  related-skills: cncf-aws-cloudformation, cncf-helm, cncf-pulumi
  role: implementation
  scope: infrastructure
  triggers: terraform, iac, infrastructure as code, terraform state, modules, remote
    backends, plan apply, terraform troubleshooting
  archetypes:
  - tactical
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
version: "1.0.0"




---




# Terraform Infrastructure as Code

**Category:** infrastructure  
**Status:** Active  
**Stars:** 43,800+  
**Last Updated:** 2026-04  
**Primary Language:** Go  
**Documentation:** [https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs)  
**Registry:** [https://registry.terraform.io](https://registry.terraform.io)

---

## Purpose and Use Cases

Terraform is a core CNCF infrastructure as code (IaC) tool that enables you to safely and predictably create, manage, and destroy infrastructure across any number of cloud providers using declarative configuration files.

### What Problem Does It Solve?

Complex multi-cloud infrastructure provisioning with consistent versioning, state tracking, dependency management, and collaboration workflows. It provides infrastructure lifecycle management with planning, preview, and rollback capabilities.

### When to Use This Project

Use Terraform when you need to provision infrastructure across multiple cloud providers, require infrastructure versioning and state management, want to use modules for reusable infrastructure patterns, need planning capabilities with `terraform plan`, or collaborate with teams on infrastructure changes. Consider alternatives if you need imperative programming for complex logic or serverless-first deployment.

### Key Use Cases

- Multi-cloud infrastructure provisioning (AWS, Azure, GCP, OCI)
- Kubernetes cluster deployment and configuration
- Network infrastructure management (VPCs, subnets, firewalls)
- Database and storage provisioning
- CI/CD pipeline infrastructure
- Environment consistency across dev/staging/production

---

## Core Workflow

Terraform follows a consistent workflow for infrastructure management:

1. **Write Configuration** — Define infrastructure in HCL or JSON files. **Checkpoint:** Configuration syntax is valid (run `terraform validate`).

2. **Initialize** — Install providers and modules. **Checkpoint:** `.terraform/` directory created with provider binaries.

3. **Plan** — Preview changes without applying. **Checkpoint:** Plan shows expected changes, no unexpected deletions.

4. **Apply** — Execute changes to infrastructure. **Checkpoint:** Apply completes successfully, infrastructure matches configuration.

5. **Inspect State** — Verify current state matches desired state. **Checkpoint:** `terraform state list` shows all resources.

6. **Destroy** — Remove infrastructure when no longer needed. **Checkpoint:** All resources successfully terminated.

---

## Implementation Patterns

### Pattern 1: Terraform Configuration Structure

Proper organization enables maintainability and collaboration.

#### ❌ BAD — Single file monolith

```hcl
# ❌ BAD — All resources in one file, no modules, no state backend
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}

resource "aws_instance" "database" {
  ami           = "ami-0d8e6d78912345678"
  instance_type = "t2.small"
}

resource "aws_security_group" "web" {
  name = "web-sg"
  # ... all rules defined here
}
```

#### ✅ GOOD — Modular, organized structure

```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"
}

module "network" {
  source = "./modules/network"
  vpc_id = module.vpc.vpc_id
}

module "compute" {
  source = "./modules/compute"
  subnet_ids = module.network.subnet_ids
}

module "database" {
  source = "./modules/database"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.network.subnet_ids
}
```

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
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "infrastructure/production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
```

```hcl
# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.database.endpoint
}
```

### Pattern 2: State Management Patterns

State file management is critical for collaboration and consistency.

#### ❌ BAD — Local state with no backend

```hcl
# ❌ BAD — Local state, no locking, no remote storage
terraform {
  # No backend configured — uses local state
}

# State stored locally in ./terraform.tfstate
# No protection against concurrent modifications
# No state sharing between team members
```

#### ✅ GOOD — Remote backend with state locking

```hcl
# ✅ GOOD — S3 backend with DynamoDB state locking
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "projects/web-app/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
    kms_key_id     = "alias/terraform-state"
  }
}

# Or use Azure Blob Storage
# backend "azurerm" {
#   resource_group_name  = "terraform-state-rg"
#   storage_account_name = "terraformstate123"
#   container_name       = "tfstate"
#   key                  = "production.terraform.tfstate"
# }

# Or use Terraform Cloud
# backend "remote" {
#   hostname     = "app.terraform.io"
#   organization = "company"
#   workspaces {
#     name = "production"
#   }
# }
```

#### State Commands Reference

```bash
# Initialize with backend
terraform init -reconfigure

# Show current state
terraform state list

# Show specific resource state
terraform state show aws_instance.web

# Move resource between states
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state (keep in cloud)
terraform state rm aws_instance.web

# Import existing resource to state
terraform import aws_instance.web i-0123456789abcdef0
```

### Pattern 3: Module Usage Patterns

Modules enable reusable, versioned infrastructure components.

#### ❌ BAD — Inline modules with no versioning

```hcl
# ❌ BAD — Hardcoded paths, no versioning
module "vpc" {
  source = "../../modules/vpc"  # Relative path
}

module "database" {
  source = "git::https://github.com/myorg/terraform-modules.git//database"
  # No version specified
}
```

#### ✅ GOOD — Versioned modules from registry

```hcl
# ✅ GOOD — Versioned from Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"  # Pin to specific version

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# ✅ GOOD — Private module registry with versioning
module "eks" {
  source  = "company-registry.example.com/eks/eks/aws"
  version = "2.1.0"

  cluster_name    = "production-cluster"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets
  cluster_version = "1.28"
}

# ✅ GOOD — Local module with clear interface
module "compute" {
  source = "./modules/compute"

  vpc_id     = module.vpc.vpc_id
  subnet_id  = module.vpc.private_subnets[0]
  env        = var.environment
  ami_id     = data.aws_ami.amazon_linux.id

  instance_count = var.instance_count
}
```

#### Module Structure Example

```hcl
# modules/compute/main.tf
resource "aws_instance" "web" {
  count = var.instance_count

  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-instance-${count.index + 1}"
  })
}

# modules/compute/variables.tf
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID"
  type        = string
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}

# modules/compute/outputs.tf
output "instance_ids" {
  description = "Instance IDs"
  value       = aws_instance.web[*].id
}

output "public_ips" {
  description = "Public IPs"
  value       = aws_instance.web[*].public_ip
}
```

### Pattern 4: Remote Backend Configuration

Configuring remote backends for team collaboration.

#### ❌ BAD — Incomplete backend configuration

```hcl
# ❌ BAD — Missing required fields, no encryption
terraform {
  backend "s3" {
    bucket = "my-bucket"  # Incomplete config
    key    = "state.tfstate"
  }
}
```

#### ✅ GOOD — Complete, secure backend configuration

```hcl
# ✅ GOOD — Complete S3 backend with encryption and locking
terraform {
  backend "s3" {
    # Required fields
    bucket = "company-terraform-state-prod"
    key    = "aws/production/terraform.tfstate"
    region = "us-east-1"

    # Security
    encrypt        = true
    kms_key_id     = "alias/terraform-state"
    dynamodb_table = "terraform-state-locks-prod"

    # Optional but recommended
    encrypt        = true
    force_path_style = false
    skip_credentials_validation = false
    skip_metadata_api_check   = false
    skip_requesting_account_id = false

    # Optional: Assume role for cross-account access
    # role_arn = "arn:aws:iam::123456789012:role/terraform"
  }
}

# Alternative: Azure Blob Storage
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "terraform-state-rg"
#     storage_account_name = "terraformstate12345"
#     container_name       = "tfstate"
#     key                  = "prod.terraform.tfstate"
#     use_azuread_auth     = true  # Use Azure AD for authentication
#   }
# }

# Alternative: Google Cloud Storage
# terraform {
#   backend "gcs" {
#     bucket  = "company-terraform-state"
#     prefix  = "terraform/state"
#     project = "my-gcp-project"
#   }
# }
```

---

## Constraints

### MUST DO

- Always use a remote backend with state locking for team environments
- Pin module versions using semantic versioning (e.g., `version = "2.0.0"`)
- Store state files in encrypted remote storage (S3 with KMS, Azure Storage with encryption)
- Use `terraform validate` in CI/CD pipelines before planning
- Run `terraform plan` before `terraform apply` to preview changes
- Tag all resources with `Environment`, `ManagedBy`, and `Project` tags
- Use `terraform fmt` to enforce consistent formatting
- Implement state file lifecycle policies (backup, retention, versioning)
- Use `terraform taint` only when resources need complete recreation
- Enable state file versioning on remote backends

### MUST NOT DO

- Never store state files in version control (they contain sensitive data)
- Never modify state files manually
- Never use `terraform apply -auto-approve` in production
- Never share provider credentials in configuration files
- Never use hardcoded values for resources that change over time (use data sources)
- Never run `terraform destroy` without proper approval process
- Never use `rm -rf .terraform` without understanding the consequences
- Never mix local and remote backends in the same workspace

---

## Output Template

When implementing Terraform infrastructure, the output must include:

1. **Configuration Structure**
   - `versions.tf`: Terraform and provider version constraints
   - `main.tf`: Main resource definitions and module calls
   - `variables.tf`: All input variables with descriptions
   - `outputs.tf`: All output values with descriptions
   - `terraform.tfvars` or `auto.tfvars`: Default values

2. **Backend Configuration**
   - Remote backend setup (S3, Azure, GCS, or Terraform Cloud)
   - State locking mechanism
   - Encryption settings

3. **Module Structure** (if applicable)
   - Module directory with `main.tf`, `variables.tf`, `outputs.tf`
   - Module versioning in source and version fields

4. **Documentation**
   - README with usage instructions
   - Example configurations
   - Provider and module version matrix

5. **CI/CD Integration**
   - Terraform validate, fmt, plan, apply steps
   - State locking enforcement
   - Environment-specific variable files

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-pulumi` | Infrastructure as code with general-purpose programming languages (Python, TypeScript, Go) instead of HCL |
| `cncf-aws-cloudformation` | AWS-native infrastructure as code using JSON/YAML templates |
| `cncf-helm` | Kubernetes package management for deploying applications to Kubernetes clusters |
| `trading-risk-stop-loss` | Stop loss strategies for trading position risk management (if infrastructure supports trading workloads) |
| `cncf-kubernetes` | Kubernetes cluster deployment and management (commonly used alongside Terraform) |

---

## References

### Official Documentation

- **Terraform Core:** [https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs)
- **Terraform Registry:** [https://registry.terraform.io](https://registry.terraform.io)
- **AWS Provider:** [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- **Azure Provider:** [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- **GCP Provider:** [https://registry.terraform.io/providers/hashicorp/google/latest/docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

### Community Resources

- **Terraform Best Practices:** [https://terraform-best-practices.com](https://terraform-best-practices.com)
- **Awesome Terraform:** [https://github.com/shaform/awesome-terraform](https://github.com/shaform/awesome-terraform)
- **HashiCorp Discuss:** [https://discuss.hashicorp.com](https://discuss.hashicorp.com)

### Provider Modules

- **Terraform AWS Modules:** [https://github.com/terraform-aws-modules](https://github.com/terraform-aws-modules)
- **Terraform Azure Modules:** [https://github.com/terraform-azure-modules](https://github.com/terraform-azure-modules)
- **Terraform GCP Modules:** [https://github.com/terraform-google-modules](https://github.com/terraform-google-modules)

---

## Common Patterns and Solutions

### Environment-Specific Infrastructure

```hcl
# Use environment-specific variable files
# terraform.tfvars (development)
environment = "development"
instance_count = 1

# prod.tfvars (production)
environment = "production"
instance_count = 3

# Usage
terraform apply -var-file=prod.tfvars
```

### State Isolation

```hcl
# Use workspace-specific state
terraform workspace new production
terraform workspace new staging
terraform workspace select production
```

### Data Sources for Dynamic Values

```hcl
# Get AMI ID dynamically
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Get VPC details
data "aws_vpc" "selected" {
  tags = {
    Name = "production-vpc"
  }
}
```

### Conditional Resource Creation

```hcl
# Create resources conditionally
resource "aws_instance" "web" {
  count = var.create_resources ? 1 : 0

  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
}

# Use for_each for dynamic collections
locals {
  instances = {
    web = { type = "t2.micro", count = 2 }
    app = { type = "t2.small", count = 3 }
  }
}

resource "aws_instance" "dynamic" {
  for_each = local.instances

  ami           = data.aws_ami.amazon_linux.id
  instance_type = each.value.type
  count         = each.value.count
}
```

### Dependency Management

```hcl
# Explicit dependencies with depends_on
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  depends_on = [aws_instance.database]
}

# Implicit dependencies via attribute references
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id  # Implicit dependency
}
```

### Sensitive Output Values

```hcl
# Mark sensitive outputs
output "database_password" {
  description = "Database password"
  value       = module.database.password
  sensitive   = true
}

# Use in CI/CD without exposing in logs
output "kubeconfig" {
  description = "Kubernetes kubeconfig"
  value       = module.eks.kubeconfig
  sensitive   = true
}
```

### Resource Lifecycle Management

```hcl
# Prevent accidental destruction
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [tags["LastModified"]]
  }
}

# Create before destroy
resource "aws_instance" "database" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }
}
```

### Importing Existing Resources

```bash
# Import existing EC2 instance
terraform import aws_instance.web i-0123456789abcdef0

# Import existing VPC
terraform import aws_vpc.main vpc-0123456789abcdef0

# After import, generate configuration
terraform show -json | terraform format -
```

---

## Troubleshooting

### Common Issues and Solutions

1. **State Lock Errors**
   ```
   Error: Error acquiring state lock
   
   # Solution
   terraform force-unlock LOCK_ID
   ```

2. **Provider Version Conflicts**
   ```
   Error: Failed to query available provider packages
   
   # Solution
   terraform init -upgrade
   ```

3. **Invalid Configuration**
   ```
   Error: Unsupported attribute
   
   # Solution
   terraform validate
   terraform fmt -check
   ```

4. **Module Not Found**
   ```
   Error: Module not found
   
   # Solution
   terraform registry module list <provider>/<module>
   terraform get -update
   ```

5. **State File Corruption**
   ```
   Error: Failed to load state
   
   # Solution
   terraform state list  # Check state integrity
   terraform state pull  # View raw state
   ```

### Debugging Commands

```bash
# Verbose logging
TF_LOG=DEBUG terraform plan
TF_LOG=TRACE terraform apply

# Check configuration
terraform validate
terraform fmt -check
terraform console  # Interactive console

# Inspect state
terraform state list
terraform state show aws_instance.web
terraform state pull

# Plan analysis
terraform plan -out=tfplan
terraform show tfplan
```

### Testing Strategies

```hcl
# Use terraform-docs for documentation generation
# Install: brew install terraform-docs
terraform-docs markdown ./ > README.md

# Use tflint for linting
# Install: brew install tflint
tflint --init
tflint

# Use terraform-linters for CI
docker run --rm -v $(pwd):/tmp terraform-linters --path /tmp
```

---

## Quick Reference

### Essential Commands

```bash
# Initialization
terraform init                    # Initialize working directory
terraform init -reconfigure       # Reconfigure backend
terraform init -migrate-state     # Migrate state

# Validation
terraform validate                # Validate configuration
terraform fmt                     # Format configuration
terraform fmt -check -recursive   # Check formatting

# Planning
terraform plan                    # Show execution plan
terraform plan -out=tfplan        # Save plan for apply
terraform show tfplan             # Show saved plan

# Application
terraform apply                   # Apply changes
terraform apply tfplan            # Apply saved plan
terraform apply -auto-approve     # Skip approval (not for production)
terraform apply -destroy          # Destroy all resources

# State Management
terraform state list              # List resources in state
terraform state show <resource>   # Show resource details
terraform state mv <old> <new>    # Move resources
terraform state rm <resource>     # Remove from state
terraform state import <resource> <id>  # Import resource

# Cleanup
terraform destroy                 # Destroy all resources
terraform taint <resource>        # Mark resource for recreation
terraform untaint <resource>      # Remove taint
```

### Environment Variables

```bash
# Logging
export TF_LOG=DEBUG               # Log level (TRACE, DEBUG, INFO, WARN, ERROR)
export TF_LOG_PATH=/tmp/terraform.log

# Backend
export TF_DATA_DIR=.terraform     # Alternate data directory

# Variables
export TF_VAR_environment=prod    # Set variable via env
export TF_VAR_region=us-east-1

# Output
export TF_IN_AUTOMATION=true      # Suppress interactive prompts
export TF_VAR_*                   # Variable prefix for env vars
```

### Provider Configuration

```hcl
# AWS Provider
provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Azure Provider
provider "azurerm" {
  features {}

  use_azuread_auth = true
}

# Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}
```

### Variable Types

```hcl
variable "string_var" {
  type    = string
  default = "value"
}

variable "number_var" {
  type    = number
  default = 42
}

variable "bool_var" {
  type    = bool
  default = true
}

variable "list_var" {
  type    = list(string)
  default = ["item1", "item2"]
}

variable "map_var" {
  type    = map(string)
  default = {
    key1 = "value1"
    key2 = "value2"
  }
}

variable "object_var" {
  type = object({
    name  = string
    count = number
  })
  default = {
    name  = "default"
    count = 1
  }
}

variable "any_var" {
  type = any
}
```

*Content generated automatically. Verify against official Terraform documentation before production use.*
---

## When to Use

Use this skill when:

- **Integrating a CNCF project into Kubernetes infrastructure** — You need to configure, deploy, or troubleshoot a cloud-native tool within a cluster
- **Designing cloud-native architecture** — You are selecting and integrating CNCF tools to solve specific infrastructure challenges
- **Resolving operational issues** — A CNCF component is misbehaving, underperforming, or needs configuration changes

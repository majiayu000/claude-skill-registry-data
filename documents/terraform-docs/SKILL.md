---
name: terraform-docs
description: Generate user-friendly documentation from Terraform code including module READMEs, architecture diagrams, runbooks, and quick references. Use when working with Terraform files (.tf), documenting infrastructure as code, or creating explanatory guides for Terraform modules and configurations.
---

# Terraform Documentation Generator

## Overview

Transform Terraform code into comprehensive, user-friendly documentation. This skill analyzes Terraform configurations and generates formatted documentation including module READMEs, architecture overviews, operational runbooks, and quick reference guides.

## Quick Start

Provide Terraform files or point to a Terraform module/configuration, then specify the documentation type needed:

```
"Document this Terraform module"
"Create architecture docs for these Terraform files"
"Generate a runbook for this infrastructure"
"Create a quick reference for this Terraform configuration"
```

The skill will analyze the code and produce formatted documentation appropriate for the target audience.

## Detailed Instructions

### Step 1: Analyze Terraform Code

Parse and understand the Terraform configuration:

**Identify Key Components:**
- **Resources** - What infrastructure is being created (aws_instance, azurerm_storage_account, etc.)
- **Variables** - Input parameters, their types, defaults, and descriptions
- **Outputs** - Values exported by the module
- **Providers** - Cloud providers and versions required
- **Data sources** - External data being referenced
- **Locals** - Internal computed values
- **Modules** - Child modules being called

**Extract Metadata:**
- Required provider versions
- Terraform version constraints
- Backend configuration
- Dependencies between resources
- Security configurations (IAM, security groups, policies)

**Understand Purpose:**
- What problem does this infrastructure solve?
- What services/resources are the core components?
- How do components interact?
- What are the security and networking patterns?

### Step 2: Choose Documentation Format

Select the appropriate documentation type based on user request:

#### Module README
For: Terraform modules that will be reused
Audience: Developers using the module
Focus: Inputs, outputs, usage examples

#### Architecture Documentation
For: Complete infrastructure setups
Audience: Technical stakeholders, architects
Focus: High-level design, component relationships, diagrams

#### Runbook
For: Operational infrastructure
Audience: DevOps, SRE, operations teams
Focus: Deployment, troubleshooting, maintenance

#### Quick Reference
For: Complex configurations
Audience: Team members working with the code
Focus: Key resources, variables, common tasks

### Step 3: Generate Documentation

#### Module README Format

```markdown
# [Module Name]

## Overview
[Brief description of what this module creates and why]

## Architecture
[Simple diagram or description of resources created]

## Usage

### Basic Example
```hcl
module "example" {
  source = "./modules/[module-name]"

  # Required variables
  [var1] = "[value1]"
  [var2] = "[value2]"
}
```

### Complete Example
```hcl
[Full working example with all options]
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| aws | >= 4.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| [var1] | [description] | `string` | `"default"` | no |
| [var2] | [description] | `number` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| [output1] | [description] |
| [output2] | [description] |

## Resources Created

- **[resource_type]**: [description of what it does]
- **[resource_type]**: [description of what it does]

## Security Considerations

- [Security feature 1]
- [Security feature 2]

## Cost Considerations

[Notes about what will incur costs]

## Examples

See the [examples](examples/) directory for more usage examples.

## License

[License information]
```

#### Architecture Documentation Format

```markdown
# [Infrastructure Name] - Architecture Documentation

## Overview

[High-level description of the infrastructure]

### Purpose
[What problem this infrastructure solves]

### Key Components
- **[Component 1]**: [Role and purpose]
- **[Component 2]**: [Role and purpose]
- **[Component 3]**: [Role and purpose]

## Architecture Diagram

```
[ASCII diagram or mermaid diagram showing component relationships]

Example:
┌─────────────────┐
│   CloudFront    │
└────────┬────────┘
         │
    ┌────▼─────┐
    │   ALB    │
    └────┬─────┘
         │
  ┌──────┴──────┐
  │   ECS       │
  │   Cluster   │
  └──────┬──────┘
         │
    ┌────▼─────┐
    │   RDS    │
    └──────────┘
```

## Components

### [Component 1 Name]

**Type**: [e.g., Load Balancer, Database, Compute]

**Purpose**: [What this component does]

**Configuration Highlights**:
- [Key setting 1]
- [Key setting 2]

**Resources**:
- `[resource_name]` - [description]

**Dependencies**:
- Depends on: [other components]
- Used by: [other components]

### [Component 2 Name]
[Repeat structure]

## Networking

### VPC Architecture
- **CIDR Block**: [CIDR]
- **Subnets**: [Public/Private configuration]
- **Availability Zones**: [AZ strategy]

### Security Groups
- **[SG Name]**: [Purpose and rules]

### Network Flow
[Description of how traffic flows through the architecture]

## Security

### IAM Roles and Policies
- **[Role Name]**: [Purpose and permissions]

### Encryption
- **At Rest**: [What's encrypted and how]
- **In Transit**: [TLS/SSL configuration]

### Access Control
[How access is controlled]

## High Availability & Disaster Recovery

### HA Strategy
[How high availability is achieved]

### Backup Strategy
[What's backed up and how]

### Disaster Recovery
- **RTO**: [Recovery Time Objective]
- **RPO**: [Recovery Point Objective]

## Monitoring & Logging

### CloudWatch Metrics
- [Key metrics being tracked]

### Logging
- [What's being logged and where]

### Alarms
- [Critical alarms configured]

## Cost Optimization

### Cost Breakdown
- [Major cost drivers]

### Optimization Opportunities
- [Potential cost savings]

## Deployment

See [RUNBOOK.md](RUNBOOK.md) for deployment instructions.

## Terraform Configuration

- **Terraform Version**: [version]
- **Providers**: [list]
- **Backend**: [backend type and configuration]

## File Structure

```
terraform/
├── main.tf           # Main resource definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── providers.tf      # Provider configurations
└── modules/          # Child modules
```

## Maintenance

### Updates
[How to update the infrastructure]

### Scaling
[How to scale resources]

## Support

For issues or questions, contact [team/email].
```

#### Runbook Format

```markdown
# [Infrastructure Name] - Operations Runbook

## Quick Reference

| Item | Value |
|------|-------|
| AWS Account | [account-id] |
| Region | [region] |
| Environment | [prod/staging/dev] |
| Terraform Backend | [S3 bucket/location] |

## Prerequisites

- Terraform >= [version]
- AWS CLI configured with appropriate credentials
- Required permissions: [list]

## Initial Deployment

### Step 1: Configure Backend

```bash
# Initialize Terraform backend
terraform init \
  -backend-config="bucket=[bucket-name]" \
  -backend-config="key=[state-key]" \
  -backend-config="region=[region]"
```

### Step 2: Review Configuration

```bash
# Review variables
cat terraform.tfvars

# Validate configuration
terraform validate

# Plan deployment
terraform plan -out=tfplan
```

### Step 3: Deploy

```bash
# Apply the plan
terraform apply tfplan

# Verify deployment
terraform output
```

## Daily Operations

### Viewing Current State

```bash
# Show current state
terraform show

# List all resources
terraform state list

# Get specific resource details
terraform state show [resource_address]
```

### Making Changes

```bash
# 1. Update .tf files or variables
# 2. Plan changes
terraform plan -out=tfplan

# 3. Review the plan carefully
# 4. Apply changes
terraform apply tfplan
```

### Checking Outputs

```bash
# View all outputs
terraform output

# Get specific output
terraform output [output_name]
```

## Common Tasks

### Adding a New Environment

1. Copy `terraform.tfvars.example` to `[env].tfvars`
2. Update variables for the new environment
3. Deploy: `terraform apply -var-file=[env].tfvars`

### Scaling Resources

**Scale Up/Down [Resource Type]:**

```bash
# Update the variable
terraform apply -var="[instance_count]=5"

# Or update terraform.tfvars and apply
terraform apply
```

### Updating Security Groups

```bash
# 1. Update security group rules in main.tf
# 2. Plan to see impact
terraform plan

# 3. Apply changes
terraform apply
```

### Rotating Credentials

**Database Credentials:**

```bash
# 1. Update secrets in AWS Secrets Manager
# 2. Force resource update
terraform apply -replace="[resource_address]"
```

### Backup and Recovery

**Create Manual Backup:**

```bash
# For RDS
aws rds create-db-snapshot \
  --db-instance-identifier [db-name] \
  --db-snapshot-identifier [snapshot-name]
```

**Restore from Backup:**

[Step-by-step restoration procedure]

## Troubleshooting

### Issue: Terraform State Lock

**Symptoms**: "Error acquiring the state lock"

**Solution**:
```bash
# Check who has the lock (in DynamoDB)
aws dynamodb get-item \
  --table-name [lock-table] \
  --key '{"LockID":{"S":"[state-path]"}}'

# Force unlock (use with caution!)
terraform force-unlock [lock-id]
```

### Issue: Resource Creation Fails

**Symptoms**: Apply fails with error creating resource

**Diagnosis**:
1. Check AWS service limits
2. Verify IAM permissions
3. Review CloudWatch logs

**Solution**:
```bash
# Get detailed error
terraform apply -debug 2>&1 | tee terraform-debug.log

# Check specific resource
terraform state show [resource_address]

# Taint and recreate if needed
terraform taint [resource_address]
terraform apply
```

### Issue: Drift Detection

**Symptoms**: Manual changes made outside Terraform

**Detection**:
```bash
# Run plan to detect drift
terraform plan -refresh-only

# Refresh state to match reality
terraform apply -refresh-only
```

**Resolution**:
- Option 1: Update Terraform to match reality
- Option 2: Revert manual changes to match Terraform

### Issue: Dependency Errors

**Symptoms**: "depends on resource that doesn't exist"

**Solution**:
```bash
# Refresh state
terraform refresh

# Re-import resource if needed
terraform import [resource_address] [resource_id]
```

## Disaster Recovery

### Complete Infrastructure Loss

**Recovery Steps**:

1. **Retrieve State File**:
   ```bash
   # State is in S3 backend
   aws s3 cp s3://[bucket]/[key] terraform.tfstate
   ```

2. **Verify State**:
   ```bash
   terraform state list
   ```

3. **Rebuild**:
   ```bash
   terraform apply
   ```

### State File Corruption

**Recovery**:
```bash
# Retrieve previous version from S3
aws s3api list-object-versions \
  --bucket [bucket] \
  --prefix [key]

# Download specific version
aws s3api get-object \
  --bucket [bucket] \
  --key [key] \
  --version-id [version] \
  terraform.tfstate.backup
```

## Maintenance Windows

### Applying Updates

**Best Practices**:
1. Always run during maintenance window
2. Create backup before changes
3. Test in non-prod environment first
4. Have rollback plan ready

**Procedure**:
```bash
# 1. Create state backup
terraform state pull > backup-$(date +%Y%m%d-%H%M%S).tfstate

# 2. Plan changes
terraform plan -out=tfplan

# 3. Apply with auto-approve (in scripts only)
terraform apply tfplan

# 4. Verify
[verification commands]
```

### Rolling Back Changes

```bash
# Revert to previous state
terraform state push backup-[timestamp].tfstate

# Or revert code and re-apply
git revert [commit]
terraform apply
```

## Monitoring

### Key Metrics to Watch

- **[Metric 1]**: [What it means, threshold]
- **[Metric 2]**: [What it means, threshold]

### Accessing Logs

```bash
# CloudWatch Logs
aws logs tail [log-group-name] --follow

# Application logs
[specific log access commands]
```

### Alerts

| Alert | Severity | Action |
|-------|----------|--------|
| [Alert name] | Critical | [What to do] |
| [Alert name] | Warning | [What to do] |

## Decommissioning

### Destroying Infrastructure

**WARNING**: This is irreversible!

```bash
# 1. Backup critical data first!
[backup commands]

# 2. Create final state backup
terraform state pull > final-backup-$(date +%Y%m%d).tfstate

# 3. Plan destroy
terraform plan -destroy

# 4. Destroy (with confirmation)
terraform destroy

# 5. Clean up backend
[cleanup commands]
```

## Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| Primary | [name/email] | [phone] |
| Secondary | [name/email] | [phone] |
| Manager | [name/email] | [phone] |

## References

- Architecture Docs: [ARCHITECTURE.md](ARCHITECTURE.md)
- Module README: [README.md](README.md)
- Terraform Docs: https://terraform.io/docs
```

#### Quick Reference Format

```markdown
# [Infrastructure Name] - Quick Reference

## Terraform Basics

### Initialize
```bash
terraform init
```

### Plan
```bash
terraform plan
terraform plan -out=tfplan
terraform plan -var-file=prod.tfvars
```

### Apply
```bash
terraform apply
terraform apply tfplan
terraform apply -auto-approve  # Use with caution!
```

### Destroy
```bash
terraform destroy
terraform destroy -target=[resource_address]
```

## Common Commands

### State Management
```bash
# List resources
terraform state list

# Show resource details
terraform state show [resource_address]

# Move resource
terraform state mv [source] [destination]

# Remove resource from state
terraform state rm [resource_address]

# Import existing resource
terraform import [resource_address] [resource_id]
```

### Outputs
```bash
# Show all outputs
terraform output

# Show specific output
terraform output [output_name]

# JSON format
terraform output -json
```

### Workspace Management
```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new [name]

# Switch workspace
terraform workspace select [name]

# Delete workspace
terraform workspace delete [name]
```

## Key Resources

### [Resource Category 1]

| Resource | Address | Purpose |
|----------|---------|---------|
| [Name] | `[resource_address]` | [What it does] |

### [Resource Category 2]

| Resource | Address | Purpose |
|----------|---------|---------|
| [Name] | `[resource_address]` | [What it does] |

## Variables

### Required Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `[var1]` | string | [description] | `"value"` |
| `[var2]` | number | [description] | `10` |

### Optional Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `[var1]` | string | `"default"` | [description] |
| `[var2]` | bool | `true` | [description] |

## Outputs

| Output | Description | Usage |
|--------|-------------|-------|
| `[output1]` | [description] | [how to use it] |
| `[output2]` | [description] | [how to use it] |

## File Structure

```
.
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── providers.tf         # Provider configs
├── terraform.tfvars     # Variable values (gitignored)
├── versions.tf          # Version constraints
└── modules/
    └── [module-name]/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## Useful Snippets

### Get Resource ARN
```bash
terraform state show [resource_address] | grep arn
```

### Find Resources by Type
```bash
terraform state list | grep [resource_type]
```

### Format All Files
```bash
terraform fmt -recursive
```

### Validate Configuration
```bash
terraform validate
```

### Check for Drift
```bash
terraform plan -refresh-only
```

### Target Specific Resource
```bash
terraform apply -target=[resource_address]
```

## Troubleshooting Quick Fixes

### State Lock Issue
```bash
terraform force-unlock [lock-id]
```

### Refresh State
```bash
terraform refresh
```

### Taint Resource (force recreate)
```bash
terraform taint [resource_address]
terraform apply
```

### Debug Mode
```bash
TF_LOG=DEBUG terraform apply 2>&1 | tee debug.log
```

## AWS CLI Helpers

### Verify Resources Exist
```bash
# EC2 instances
aws ec2 describe-instances --filters "Name=tag:Name,Values=[name]"

# S3 buckets
aws s3 ls

# RDS databases
aws rds describe-db-instances

# Load balancers
aws elbv2 describe-load-balancers
```

### Get Resource IDs
```bash
# VPC ID
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=[name]" --query 'Vpcs[0].VpcId'

# Subnet IDs
aws ec2 describe-subnets --filters "Name=vpc-id,Values=[vpc-id]" --query 'Subnets[*].SubnetId'
```

## Emergency Contacts

| Issue | Contact |
|-------|---------|
| Infrastructure down | [contact] |
| Security incident | [contact] |
| Cost spike | [contact] |

## Links

- [Architecture Documentation](ARCHITECTURE.md)
- [Detailed Runbook](RUNBOOK.md)
- [Module README](README.md)
```

### Step 4: Enhance with Context

**Add Explanatory Content:**

Transform technical resource names into human-readable descriptions:
- `aws_instance.web` → "Web Server EC2 Instance"
- `aws_db_instance.main` → "Primary PostgreSQL Database"
- `aws_lb.main` → "Application Load Balancer"

**Explain Relationships:**
- "The ALB distributes traffic to the ECS tasks"
- "Security group allows inbound HTTPS from CloudFront only"
- "RDS database is accessible only from private subnets"

**Include Diagrams:**

Use ASCII art or Mermaid syntax for visual representation:

```
graph TD
    A[CloudFront] --> B[ALB]
    B --> C[ECS Service]
    C --> D[RDS Database]
    C --> E[ElastiCache]
```

**Add Context:**
- Why certain resources are configured the way they are
- Security implications of configurations
- Cost considerations
- Best practices being followed

## Examples

### Example 1: Simple Module to README

**Input (Terraform Module):**

```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 2
}

# main.tf
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = {
    Name        = "web-${var.environment}-${count.index}"
    Environment = var.environment
  }
}

# outputs.tf
output "instance_ids" {
  description = "IDs of created instances"
  value       = aws_instance.web[*].id
}
```

**Output (Module README):**

```markdown
# Web Server Module

## Overview

Creates multiple EC2 instances for web server hosting. Designed for flexibility across environments with configurable instance counts.

## Usage

### Basic Example

```hcl
module "web_servers" {
  source = "./modules/web-server"

  environment = "production"
}
```

### Custom Instance Count

```hcl
module "web_servers" {
  source = "./modules/web-server"

  environment    = "staging"
  instance_count = 3
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| aws | >= 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| environment | Environment name (used for tagging) | `string` | n/a | yes |
| instance_count | Number of web server instances to create | `number` | `2` | no |

## Outputs

| Name | Description |
|------|-------------|
| instance_ids | List of EC2 instance IDs created by this module |

## Resources Created

- **EC2 Instances**: t3.micro Ubuntu instances, count based on `instance_count` variable
- **Tags**: Automatic environment and name tagging for resource management

## Cost Considerations

- Each t3.micro instance costs approximately $0.0104/hour (~$7.50/month)
- Default configuration (2 instances) = ~$15/month
```

### Example 2: Infrastructure to Architecture Docs

**Input (Terraform Configuration):**

```hcl
# VPC and networking
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

# Application load balancer
resource "aws_lb" "main" {
  name               = "app-lb"
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id
}

# ECS cluster
resource "aws_ecs_cluster" "main" {
  name = "app-cluster"
}

resource "aws_ecs_service" "api" {
  name            = "api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 2

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
}

# RDS database
resource "aws_db_instance" "main" {
  engine         = "postgres"
  instance_class = "db.t3.small"
  allocated_storage = 20
}
```

**Output (Architecture Documentation):**

```markdown
# Application Infrastructure - Architecture

## Overview

Containerized web application running on AWS ECS with PostgreSQL database backend. Designed for high availability across multiple availability zones with automatic load balancing.

## Architecture Diagram

```
Internet
    │
    ▼
┌─────────────────┐
│ Application     │
│ Load Balancer   │
│ (Public Subnets)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│  ECS   │ │  ECS   │
│ Task 1 │ │ Task 2 │
│ (API)  │ │ (API)  │
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
   ┌──────────┐
   │PostgreSQL│
   │   RDS    │
   └──────────┘
```

## Components

### Networking Layer

**VPC Configuration**
- **CIDR Block**: 10.0.0.0/16
- **Public Subnets**: 2 subnets across different AZs (10.0.0.0/24, 10.0.1.0/24)
- **High Availability**: Multi-AZ deployment for redundancy

### Load Balancing

**Application Load Balancer**
- **Type**: Application Load Balancer (Layer 7)
- **Placement**: Public subnets across 2 availability zones
- **Purpose**: Distributes incoming traffic across ECS tasks
- **Health Checks**: Monitors task health and routes only to healthy instances

### Compute Layer

**ECS Cluster**
- **Container Orchestration**: AWS ECS manages container lifecycle
- **API Service**: 2 task instances running continuously
- **Container Port**: 8080
- **Scaling**: Can be configured for auto-scaling based on demand

### Database Layer

**PostgreSQL RDS**
- **Engine**: PostgreSQL
- **Instance Type**: db.t3.small (2 vCPU, 2 GB RAM)
- **Storage**: 20 GB SSD
- **Accessibility**: Private access from ECS tasks only

## Traffic Flow

1. User request arrives at Application Load Balancer
2. ALB performs health check on available ECS tasks
3. Request is routed to a healthy ECS task
4. API container processes request
5. If data is needed, task queries PostgreSQL RDS
6. Response returns through ALB to user

## High Availability

- **Multi-AZ Deployment**: Resources spread across 2 availability zones
- **Load Balancing**: ALB automatically routes around failed tasks
- **Task Redundancy**: 2 API tasks running simultaneously
- **Database**: RDS with automated backups (can enable Multi-AZ)

## Security

- **Network Isolation**: Database not directly accessible from internet
- **Security Groups**: (To be documented based on security group configs)
- **IAM Roles**: ECS tasks use IAM roles for AWS service access

## Cost Breakdown

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| ALB | ~$16 |
| ECS Tasks (2 × t3.small) | ~$30 |
| RDS db.t3.small | ~$25 |
| **Total** | **~$71/month** |

## Scalability

- **Horizontal Scaling**: Increase `desired_count` in ECS service
- **Database Scaling**: Upgrade instance class or enable read replicas
- **Load Balancer**: Automatically scales to handle traffic
```

### Example 3: Complex Setup to Runbook

**Input (Production Infrastructure):**

```hcl
terraform {
  backend "s3" {
    bucket = "company-terraform-state"
    key    = "prod/infrastructure.tfstate"
    region = "us-east-1"
  }
}

# Multi-tier web application with autoscaling
```

**Output (Operational Runbook):**

See the full Runbook format above for the complete structure. Key sections would include:
- Backend configuration details
- Step-by-step deployment procedures
- Common operational tasks
- Troubleshooting guides specific to the resources
- Emergency contacts and escalation procedures

## Best Practices

### Documentation Clarity

1. **Use Plain Language**: Avoid unnecessarily complex terminology
2. **Be Specific**: Include actual values, not just placeholders
3. **Provide Context**: Explain the "why", not just the "what"
4. **Include Examples**: Real, working code examples
5. **Keep Updated**: Mark documentation date/version

### Technical Accuracy

1. **Extract from Code**: Don't guess at variable types or defaults
2. **Verify Commands**: Test all command examples
3. **Check Versions**: Include accurate version requirements
4. **Validate Links**: Ensure all references point to correct locations

### Audience Awareness

**For Developers:**
- Focus on module usage and API
- Include code examples
- Explain inputs/outputs clearly

**For Operations:**
- Focus on deployment and troubleshooting
- Include runbooks and commands
- Provide escalation procedures

**For Architects:**
- Focus on design decisions
- Include diagrams
- Explain trade-offs and alternatives

### Formatting Standards

1. **Consistent Structure**: Use templates for similar docs
2. **Code Blocks**: Always specify language for syntax highlighting
3. **Tables**: Use for structured data (variables, outputs)
4. **Diagrams**: Include visual representations
5. **Links**: Cross-reference related documentation

## Additional Resources

See the templates directory for:
- [Module README Template](templates/MODULE_README_TEMPLATE.md)
- [Architecture Docs Template](templates/ARCHITECTURE_TEMPLATE.md)
- [Runbook Template](templates/RUNBOOK_TEMPLATE.md)
- [Quick Reference Template](templates/QUICK_REFERENCE_TEMPLATE.md)

See the examples directory for:
- [Complete VPC Module Example](examples/vpc-module/)
- [ECS Application Example](examples/ecs-app/)
- [Multi-Region Setup Example](examples/multi-region/)

See the scripts directory for:
- [terraform-docs integration](scripts/generate_docs.sh) - Automated documentation generation
- [Validation script](scripts/validate_docs.py) - Check documentation completeness

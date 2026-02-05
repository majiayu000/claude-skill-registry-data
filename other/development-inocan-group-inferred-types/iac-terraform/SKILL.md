---
name: iac-terraform
description: Infrastructure as Code with Terraform and Terragrunt. Use for creating, validating, troubleshooting, and managing Terraform configurations, modules, and state. Covers Terraform workflows, best practices, module development, state management, Terragrunt patterns, and common issue resolution.
---

# Infrastructure as Code - Terraform & Terragrunt

Comprehensive guidance for infrastructure as code using Terraform and Terragrunt, from development through production deployment.

## When to Use This Skill

Use this skill when:
- Writing or refactoring Terraform configurations
- Creating reusable Terraform modules
- Troubleshooting Terraform/Terragrunt errors
- Managing Terraform state
- Implementing IaC best practices
- Setting up Terragrunt project structure
- Reviewing infrastructure code
- Debugging plan/apply issues

## Core Workflows

### 1. New Infrastructure Development

**Workflow Decision Tree:**

```
Is this reusable across environments/projects?
├─ Yes → Create a Terraform module
│   └─ See "Creating Terraform Modules" below
└─ No → Create environment-specific configuration
    └─ See "Environment Configuration" below
```

#### Creating Terraform Modules

When building reusable infrastructure:

1. **Scaffold new module with script:**
```bash
python3 scripts/init_module.py my-module-name
```

This automatically creates:
- Standard module file structure
- Template files with proper formatting
- Examples directory
- README with documentation

2. **Use module template structure:**
   - See `assets/templates/MODULE_TEMPLATE.md` for complete structure
   - Required files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`
   - Recommended: `examples/` directory with working examples

3. **Follow module best practices:**
   - Single responsibility - one module, one purpose
   - Sensible defaults for optional variables
   - Complete descriptions for all variables and outputs
   - Input validation using `validation` blocks
   - Mark sensitive values with `sensitive = true`

3. **Validate module:**
```bash
python3 scripts/validate_module.py /path/to/module
```

This checks for:
- Required files present
- Variables have descriptions and types
- Outputs have descriptions
- README exists and is complete
- Naming conventions followed
- Sensitive values properly marked

4. **Test module:**
```bash
cd examples/complete
terraform init
terraform plan
```

5. **Document module:**
   - Use terraform-docs to auto-generate: `terraform-docs markdown . > README.md`
   - Include usage examples
   - Document all inputs and outputs

**Key Module Patterns:**

See `references/best_practices.md` "Module Design" section for:
- Composability patterns
- Variable organization
- Output design
- Module versioning strategies

#### Environment Configuration

For environment-specific infrastructure:

1. **Structure by environment:**
```
environments/
├── dev/
├── staging/
└── prod/
```

2. **Use consistent file organization:**
```
environment/
├── main.tf           # Resource definitions
├── variables.tf      # Variable declarations
├── terraform.tfvars  # Default values (committed)
├── secrets.auto.tfvars  # Sensitive values (.gitignore)
├── backend.tf        # State configuration
├── outputs.tf        # Output values
└── versions.tf       # Version constraints
```

3. **Reference modules:**
```hcl
module "vpc" {
  source = "git::https://github.com/company/terraform-modules.git//vpc?ref=v1.2.0"
  
  name        = "${var.environment}-vpc"
  vpc_cidr    = var.vpc_cidr
  environment = var.environment
}
```

### 2. State Management & Inspection

**When to inspect state:**
- Before major changes
- Investigating drift
- Debugging resource issues
- Auditing infrastructure

**Inspect state and check health:**
```bash
python3 scripts/inspect_state.py /path/to/terraform/directory
```

**Check for drift:**
```bash
python3 scripts/inspect_state.py /path/to/terraform/directory --check-drift
```

The script provides:
- Resource count and types
- Backend configuration
- Provider versions
- Issues with resources (tainted, etc.)
- Drift detection (if requested)

**Manual state operations:**
```bash
# List all resources
terraform state list

# Show specific resource
terraform state show aws_instance.web

# Remove from state (doesn't destroy)
terraform state rm aws_instance.web

# Move/rename resource
terraform state mv aws_instance.web aws_instance.web_server

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0
```

**State best practices:** See `references/best_practices.md` "State Management" section for:
- Remote backend setup (S3 + DynamoDB)
- State file organization strategies
- Encryption and security
- Backup and recovery procedures

### 3. Standard Terraform Workflow

```bash
# 1. Initialize (first time or after module changes)
terraform init

# 2. Format code
terraform fmt -recursive

# 3. Validate syntax
terraform validate

# 4. Plan changes (always review!)
terraform plan -out=tfplan

# 5. Apply changes
terraform apply tfplan

# 6. Verify outputs
terraform output
```

**With Terragrunt:**
```bash
# Run for single module
terragrunt plan
terragrunt apply

# Run for all modules in directory tree
terragrunt run-all plan
terragrunt run-all apply
```

### 4. Troubleshooting Issues

When encountering errors:

1. **Read the complete error message** - Don't skip details

2. **Check common issues:** See `references/troubleshooting.md` for:
   - State lock errors
   - State drift/corruption
   - Provider authentication failures
   - Resource errors (already exists, dependency errors, timeouts)
   - Module source issues
   - Terragrunt-specific issues (dependency cycles, hooks)
   - Performance problems

3. **Enable debug logging if needed:**
```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform-debug.log
terraform plan
```

4. **Isolate the problem:**
```bash
# Test specific resource
terraform plan -target=aws_instance.web
terraform apply -target=aws_instance.web
```

5. **Common quick fixes:**

**State locked:**
```bash
# Verify no one else running, then:
terraform force-unlock <lock-id>
```

**Provider cache issues:**
```bash
rm -rf .terraform
terraform init -upgrade
```

**Module cache issues:**
```bash
rm -rf .terraform/modules
terraform init
```

### 5. Code Review & Quality

**Before committing:**

1. **Format code:**
```bash
terraform fmt -recursive
```

2. **Validate syntax:**
```bash
terraform validate
```

3. **Lint with tflint:**
```bash
tflint --module
```

4. **Security scan with checkov:**
```bash
checkov -d .
```

5. **Validate modules:**
```bash
python3 scripts/validate_module.py modules/vpc
```

6. **Generate documentation:**
```bash
terraform-docs markdown modules/vpc > modules/vpc/README.md
```

**Review checklist:**
- [ ] All variables have descriptions
- [ ] Sensitive values marked as sensitive
- [ ] Outputs have descriptions
- [ ] Resources follow naming conventions
- [ ] No hardcoded values (use variables)
- [ ] README is complete and current
- [ ] Examples directory exists and works
- [ ] Version constraints specified
- [ ] Security best practices followed

See `references/best_practices.md` for comprehensive guidelines.

## Terragrunt Patterns

### Project Structure

```
terragrunt-project/
├── terragrunt.hcl              # Root config
├── account.hcl                 # Account-level vars
├── region.hcl                  # Region-level vars
└── environments/
    ├── dev/
    │   ├── env.hcl            # Environment vars
    │   └── us-east-1/
    │       ├── vpc/
    │       │   └── terragrunt.hcl
    │       └── eks/
    │           └── terragrunt.hcl
    └── prod/
        └── us-east-1/
            ├── vpc/
            └── eks/
```

### Dependency Management

```hcl
# In eks/terragrunt.hcl
dependency "vpc" {
  config_path = "../vpc"
  
  # Mock outputs for plan/validate
  mock_outputs = {
    vpc_id         = "vpc-mock"
    subnet_ids     = ["subnet-mock"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids
}
```

### Common Patterns

See `assets/templates/MODULE_TEMPLATE.md` for complete Terragrunt configuration templates including:
- Root terragrunt.hcl with provider generation
- Remote state configuration
- Module-level terragrunt.hcl patterns
- Dependency handling

## Reference Documentation

### references/best_practices.md

Comprehensive best practices covering:
- **Project Structure** - Recommended directory layouts
- **State Management** - Remote state, locking, organization
- **Module Design** - Single responsibility, composability, versioning
- **Variable Management** - Declarations, files hierarchy, secrets
- **Resource Naming** - Conventions and standards
- **Security Practices** - Least privilege, encryption, secret management
- **Testing & Validation** - Tools and approaches
- **CI/CD Integration** - Pipeline patterns

Read this when:
- Setting up new Terraform projects
- Establishing team standards
- Designing reusable modules
- Implementing security controls
- Setting up CI/CD pipelines

### references/troubleshooting.md

Detailed troubleshooting guide for:
- **State Issues** - Lock errors, drift, corruption
- **Provider Issues** - Version conflicts, authentication
- **Resource Errors** - Already exists, dependencies, timeouts
- **Module Issues** - Source not found, version conflicts
- **Terragrunt Specific** - Dependency cycles, hooks
- **Performance Issues** - Slow plans, optimization strategies

Read this when:
- Encountering specific error messages
- Investigating unexpected behavior
- Debugging failed deployments
- Performance tuning

Each issue includes:
- Symptom description
- Common causes
- Step-by-step resolution
- Prevention strategies

### references/cost_optimization.md

Cloud cost optimization strategies for Terraform-managed infrastructure:
- **Right-Sizing Resources** - Compute, database, and storage optimization
- **Spot and Reserved Instances** - Cost-effective instance strategies
- **Storage Optimization** - S3 lifecycle policies, EBS volume types
- **Networking Costs** - VPC endpoints, data transfer optimization
- **Resource Lifecycle** - Scheduled shutdown, cleanup automation
- **Cost Tagging** - Comprehensive tagging for cost allocation
- **Monitoring and Alerts** - Budget alerts, anomaly detection
- **Multi-Cloud** - Azure, GCP cost optimization patterns

Read this when:
- Planning infrastructure to minimize costs
- Conducting cost reviews or optimization initiatives
- Implementing auto-scaling and scheduling
- Setting up cost monitoring and alerts
- Designing cost-effective architectures

## CI/CD Workflows

Ready-to-use CI/CD pipeline templates in `assets/workflows/`:

### github-actions-terraform.yml

Complete GitHub Actions workflow including:
- Terraform validation and formatting checks
- TFLint linting
- Checkov security scanning
- Terraform plan on PRs with comment posting
- Terraform apply on main branch with approval
- OIDC authentication support

### github-actions-terragrunt.yml

Terragrunt-specific workflow featuring:
- Changed module detection
- Multi-module parallel planning
- Run-all commands
- Dependency-aware apply ordering
- Manual workflow dispatch with environment selection

### gitlab-ci-terraform.yml

GitLab CI/CD pipeline with:
- Multi-stage pipeline (validate, lint, security, plan, apply)
- Artifact management
- Manual deployment gates
- Multi-environment configuration examples

Use these templates as starting points for your CI/CD pipelines. Customize based on your:
- Cloud provider and authentication method
- Repository structure
- Team approval workflows
- Environment promotion strategy

## Scripts

### init_module.py

Scaffolds a new Terraform module with proper structure and template files.

**Usage:**
```bash
# Create module in current directory
python3 scripts/init_module.py my-vpc

# Create in specific path
python3 scripts/init_module.py my-vpc --path ./modules

# Get JSON output
python3 scripts/init_module.py my-vpc --json
```

**Creates:**
- `main.tf` - Resource definitions with TODO placeholders
- `variables.tf` - Input variables with validation examples
- `outputs.tf` - Output values with descriptions
- `versions.tf` - Terraform and provider version constraints
- `README.md` - Module documentation template
- `examples/complete/` - Complete usage example

**Use when:**
- Starting a new Terraform module
- Ensuring consistent module structure across team
- Quickly bootstrapping module development
- Teaching module best practices

### inspect_state.py

Comprehensive state inspection and health check.

**Usage:**
```bash
# Basic inspection
python3 scripts/inspect_state.py /path/to/terraform

# Include drift detection
python3 scripts/inspect_state.py /path/to/terraform --check-drift
```

**Provides:**
- State health status
- Resource counts and types
- Provider versions
- Backend configuration
- Resource issues (tainted, etc.)
- Configuration drift detection (optional)
- Actionable recommendations

**Use when:**
- Before major infrastructure changes
- Investigating resource issues
- Auditing infrastructure state
- Detecting configuration drift

### validate_module.py

Validates Terraform modules against best practices.

**Usage:**
```bash
python3 scripts/validate_module.py /path/to/module
```

**Checks:**
- Required files present (main.tf, variables.tf, outputs.tf)
- Variable descriptions and types
- Output descriptions
- Sensitive value handling
- README completeness
- Version constraints
- Example configurations
- Naming conventions
- Hard-coded values that should be variables

**Returns:**
- Issues (must fix)
- Warnings (should fix)
- Suggestions (consider)

**Use when:**
- Creating new modules
- Reviewing module code
- Before releasing module versions
- Establishing quality standards

## Assets

### templates/MODULE_TEMPLATE.md

Complete Terraform module template including:
- File-by-file structure and examples
- main.tf patterns
- variables.tf with validation
- outputs.tf best practices
- versions.tf constraints
- README.md template
- Example usage configurations
- Terragrunt configuration templates

**Use this when:**
- Creating new modules from scratch
- Standardizing module structure
- Onboarding team members
- Establishing module conventions

## Quick Reference

### Essential Commands

```bash
# Initialize
terraform init
terraform init -upgrade  # Update providers

# Validate
terraform validate
terraform fmt -recursive

# Plan
terraform plan
terraform plan -out=tfplan

# Apply
terraform apply
terraform apply tfplan
terraform apply -auto-approve  # CI/CD only

# State
terraform state list
terraform state show <resource>
terraform state rm <resource>
terraform state mv <old> <new>

# Import
terraform import <resource_address> <resource_id>

# Destroy
terraform destroy
terraform destroy -target=<resource>

# Outputs
terraform output
terraform output <output_name>
```

### Terragrunt Commands

```bash
# Single module
terragrunt init
terragrunt plan
terragrunt apply

# All modules
terragrunt run-all plan
terragrunt run-all apply
terragrunt run-all destroy

# With specific modules
terragrunt run-all apply --terragrunt-include-dir vpc --terragrunt-include-dir eks
```

## Best Practices Summary

**Always:**
- Use remote state with locking
- Plan before apply (review changes)
- Pin Terraform and provider versions
- Use modules for reusable components
- Mark sensitive values as sensitive
- Document everything
- Test in non-production first

**Never:**
- Commit secrets or credentials
- Manually edit state files
- Use root AWS credentials
- Skip code review for production changes
- Deploy without testing
- Ignore security scan findings

**Key Principles:**
- Infrastructure as code (everything in version control)
- DRY (Don't Repeat Yourself) - use modules
- Immutable infrastructure
- Environment parity (dev/staging/prod similar)
- Security by default
- Document for future you

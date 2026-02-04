---
name: terraform-documentation-generator
description: Generates documentation for Terraform modules using terraform-docs tool to auto-generate README files with input/output tables, usage examples, and requirements. This skill should be used when users need to document Terraform modules, create or update README files, or maintain consistent module documentation.
---

# Terraform Documentation Generator

This skill helps generate and maintain Terraform module documentation using terraform-docs.

## When to Use

Use this skill when:
- Creating README.md for a new module
- Updating documentation after module changes
- Generating input/output reference tables automatically
- Ensuring consistent documentation across modules

## Using terraform-docs

### Installation

```bash
# macOS
brew install terraform-docs

# Linux
curl -sSLo ./terraform-docs.tar.gz https://terraform-docs.io/dl/latest/terraform-docs-linux-amd64.tar.gz
tar -xzf terraform-docs.tar.gz
chmod +x terraform-docs
mv terraform-docs /usr/local/bin/

# Or use Go
go install github.com/terraform-docs/terraform-docs@latest
```

### Basic Usage

```bash
# Generate markdown documentation
terraform-docs markdown table . > README.md

# Preview without writing
terraform-docs markdown table .

# Generate for specific directory
terraform-docs markdown table ./modules/vpc > ./modules/vpc/README.md
```

### Configuration File

Create `.terraform-docs.yml` in module root for consistent formatting:

```yaml
formatter: "markdown table"

header-from: main.tf

sections:
  show:
    - header
    - requirements
    - providers
    - inputs
    - outputs
    - resources

content: |-
  {{ .Header }}
  
  ## Usage
  
  ```hcl
  module "example" {
    source = "./modules/example"
    
    # Add your example here
  }
  ```
  
  {{ .Requirements }}
  {{ .Providers }}
  {{ .Inputs }}
  {{ .Outputs }}
  {{ .Resources }}

output:
  file: "README.md"
  mode: inject
  template: |-
    <!-- BEGIN_TF_DOCS -->
    {{ .Content }}
    <!-- END_TF_DOCS -->

sort:
  enabled: true
  by: required
```

### Auto-Generate Documentation

```bash
# With config file
terraform-docs .

# Inject into existing README between markers
terraform-docs markdown table --output-file README.md --output-mode inject .
```

### Output Formats

```bash
# Markdown table (most common)
terraform-docs markdown table .

# Markdown document
terraform-docs markdown document .

# JSON
terraform-docs json .

# YAML
terraform-docs yaml .
```

## Documentation Best Practices

### Add Header Comments

Add description at top of main.tf:

```hcl
/**
 * # Terraform AWS VPC Module
 *
 * Creates a VPC with public and private subnets across multiple availability zones.
 *
 * ## Features
 *
 * - Multi-AZ VPC with public and private subnets
 * - NAT Gateway for private subnet internet access
 * - Configurable CIDR blocks
 */

resource "aws_vpc" "main" {
  # ...
}
```

terraform-docs will use this as the README header.

### Document Variables Clearly

```hcl
variable "vpc_cidr" {
  description = "CIDR block for VPC (e.g., 10.0.0.0/16)"
  type        = string
  
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be valid IPv4 CIDR."
  }
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnet internet access"
  type        = bool
  default     = true
}
```

### Document Outputs

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs for use with internal resources"
  value       = aws_subnet.private[*].id
}
```

## Workflow Integration

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/terraform-docs/terraform-docs
    rev: "v0.16.0"
    hooks:
      - id: terraform-docs-go
        args: ["markdown", "table", "--output-file", "README.md", "."]
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Generate terraform docs
  uses: terraform-docs/gh-actions@v1
  with:
    working-dir: .
    output-file: README.md
    output-method: inject
```

## Quick Reference

```bash
# Generate docs for current directory
terraform-docs markdown table . > README.md

# Update existing README (between markers)
terraform-docs markdown table --output-file README.md --output-mode inject .

# Generate for all modules
find . -type f -name "*.tf" -exec dirname {} \; | sort -u | xargs -I {} terraform-docs markdown table {} --output-file {}/README.md

# Validate documentation is up to date
terraform-docs markdown table . | diff - README.md
```

## Documentation Checklist

- [ ] terraform-docs installed
- [ ] `.terraform-docs.yml` config created (optional)
- [ ] Header comment added to main.tf
- [ ] All variables have clear descriptions
- [ ] All outputs have descriptions
- [ ] Usage example added to README
- [ ] Documentation generated with `terraform-docs`
- [ ] Pre-commit hook configured (optional)

---
name: terraform-module-scaffolder
description: Scaffolds new Terraform modules with standardized structure including main.tf, variables.tf, outputs.tf, versions.tf, and README.md. This skill should be used when users want to create a new Terraform module, set up module structure, or need templates for common infrastructure patterns like VPC, ECS, S3, or RDS modules.
---

# Terraform Module Scaffolder

This skill helps create well-structured Terraform modules following best practices and conventions.

## When to Use

Use this skill when:
- Creating a new Terraform module from scratch
- Setting up standardized module structure
- Need templates for common AWS/Azure/GCP resources
- Want to ensure module follows Terraform conventions

## Module Structure

Generate modules with this standard structure:

```
module-name/
├── main.tf           # Primary resource definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Provider and Terraform version constraints
├── README.md         # Module documentation
└── examples/         # Usage examples (optional)
    └── basic/
        └── main.tf
```

## Instructions

### 1. Gather Requirements

Ask the user:
- What is the module name?
- What cloud provider (AWS, Azure, GCP, multi-cloud)?
- What resources should the module create?
- Any specific requirements or constraints?

### 2. Create Core Files

**main.tf** - Include:
- Resource definitions with clear naming
- Local values for computed attributes
- Data sources if needed

**variables.tf** - Include:
- Required variables first, then optional
- Clear descriptions for each variable
- Sensible defaults where appropriate
- Type constraints (string, number, bool, list, map, object)
- Validation rules for critical inputs

**outputs.tf** - Include:
- Resource IDs and ARNs
- Connection information (endpoints, URLs)
- Computed attributes that other modules might need
- Clear descriptions for each output

**versions.tf** - Include:
- Terraform version constraint (use ~> for minor version)
- Provider version constraints
- Required providers block

**README.md** - Include:
- Module description and purpose
- Usage example
- Requirements section
- Inputs table (can be auto-generated later)
- Outputs table (can be auto-generated later)

### 3. Apply Best Practices

- Use consistent naming: `resource_type-purpose` (e.g., `s3-logs`, `vpc-main`)
- Add tags to all taggable resources with variables for custom tags
- Use `terraform fmt` formatting
- Include lifecycle blocks where appropriate
- Add `depends_on` only when implicit dependencies don't work
- Use `count` or `for_each` for conditional resources

### 4. Add Example Usage

Create `examples/basic/main.tf` showing minimal working example:

```hcl
module "example" {
  source = "../.."
  
  # Required variables
  name = "example"
  
  # Optional variables with common values
  tags = {
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}
```

## Validation Checklist

Before completing, verify:
- [ ] All files use consistent formatting (`terraform fmt`)
- [ ] Variables have descriptions and appropriate types
- [ ] Outputs have descriptions
- [ ] Version constraints are specified
- [ ] README includes usage example
- [ ] Module follows naming conventions
- [ ] Tags are configurable via variables

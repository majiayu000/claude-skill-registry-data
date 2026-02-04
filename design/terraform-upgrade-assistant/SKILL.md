---
name: terraform-upgrade-assistant
description: Guides through Terraform version upgrades including identifying deprecated syntax, updating provider versions, and migrating breaking changes. This skill should be used when users need to upgrade Terraform or provider versions, fix deprecated warnings, or migrate configurations to newer syntax.
---

# Terraform Upgrade Assistant

This skill helps safely upgrade Terraform and provider versions.

## When to Use

Use this skill when:
- Upgrading Terraform CLI version
- Updating provider versions
- Fixing deprecated syntax warnings
- Migrating to new provider features
- Preparing for major version upgrades

## Upgrade Process

### 1. Check Current Versions

```bash
# Check Terraform version
terraform version

# Check provider versions in use
terraform providers

# Check for available updates
terraform init -upgrade
```

### 2. Review Upgrade Guides

Before upgrading, review:
- [Terraform Upgrade Guides](https://www.terraform.io/language/upgrade-guides)
- Provider changelog (e.g., AWS provider releases)
- Breaking changes documentation

### 3. Upgrade Strategy

**Incremental approach (recommended):**
1. Upgrade one minor version at a time
2. Test thoroughly between upgrades
3. Fix deprecation warnings before major upgrades

**Example path:** 1.0 → 1.1 → 1.2 → 1.3 → 1.4 → 1.5

### 4. Update Version Constraints

```hcl
# Before
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# After
terraform {
  required_version = ">= 1.5"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

## Handling Deprecation Warnings

### Identify Warnings

```bash
# Run plan to see warnings
terraform plan

# Example output:
# Warning: Argument is deprecated
#   Use aws_s3_bucket_acl resource instead
```

## Upgrade Checklist

### Pre-Upgrade
- [ ] Backup state file
- [ ] Review upgrade guides for target version
- [ ] Check provider changelogs
- [ ] Test in non-production environment first
- [ ] Ensure team is aware of upgrade

### During Upgrade
- [ ] Update version constraints in code
- [ ] Run `terraform init -upgrade`
- [ ] Run `terraform plan` and review changes
- [ ] Fix any deprecation warnings
- [ ] Update CI/CD pipelines with new version

### Post-Upgrade
- [ ] Run `terraform plan` (should show no changes)
- [ ] Test apply in dev environment
- [ ] Update documentation
- [ ] Commit version constraint changes
- [ ] Monitor for issues

## Troubleshooting

### State File Compatibility

```bash
# If state file is incompatible with provider source
terraform state replace-provider \
  registry.terraform.io/-/aws \
  registry.terraform.io/hashicorp/aws
```

### Provider Plugin Issues

```bash
# Clear provider cache and reinitialize
rm -rf .terraform/
rm .terraform.lock.hcl
terraform init -upgrade
```

## Version Constraint Best Practices

```hcl
# Good - Allows patch updates, prevents breaking changes
terraform {
  required_version = "~> 1.5.0"  # 1.5.x only
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # 5.x only
    }
  }
}

# Too restrictive
required_version = "= 1.5.0"  # Only exact version

# Too permissive
required_version = ">= 1.0"  # Could break on major updates
```

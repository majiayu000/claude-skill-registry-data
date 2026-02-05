---
name: infrastructure-as-code
category: devops
difficulty: intermediate
prerequisites:
- devops/ci-cd
- cloud/aws-fundamentals
tags:
- terraform
- infrastructure
- automation
- cloud
- state-management
related_skills:
- devops/ci-cd
- security/secrets-management
- cloud/multi-cloud
description: 'Basic Resource:'
---


# Infrastructure as Code (IaC)

Automate infrastructure provisioning and management using declarative configuration with Terraform, enabling version-controlled, repeatable, and scalable infrastructure deployment.

## Level 1: Quick Reference

### Core Workflow

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Destroy infrastructure
terraform destroy

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive
```

### Essential Patterns

**Basic Resource:**

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "${var.environment}-web"
    Environment = var.environment
  }
}
```

**Module Usage:**

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  enable_vpn_gateway = false
}
```

**Remote State:**

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "networking/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Critical Checklist

- [ ] Pin provider versions (`version = "~> 5.0"`)
- [ ] Enable remote state with locking
- [ ] Use workspaces for environments
- [ ] Implement `.gitignore` for secrets
- [ ] Run `terraform validate` before commit
- [ ] Review plan output before apply
- [ ] Tag all resources consistently
- [ ] Use variables for all environment-specific values
- [ ] Document module inputs/outputs
- [ ] Enable state encryption

### Common Commands

```bash
# Workspace management
terraform workspace new dev
terraform workspace select prod
terraform workspace list

# State management
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.old aws_instance.new
terraform state rm aws_instance.deprecated

# Import existing resources
terraform import aws_instance.web i-1234567890abcdef0

# Output values
terraform output
terraform output -json vpc_id
```

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide

### 1. Terraform Fundamentals

#### Project Structure


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


#### Provider Configuration


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


#### Resources and Data Sources


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


### 2. Module Development

#### Module Structure


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


#### Module Versioning


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


### 3. State Management

#### S3 Backend Configuration


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


#### Backend Initialization Script


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


#### State Operations


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


### 4. Workspace Strategies

#### Environment Workspaces


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


#### Workspace-Based Configuration


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


### 5. Testing Infrastructure as Code

#### Terraform Validate and Format


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


#### TFLint Configuration


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


#### Terratest Example


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


### 6. CI/CD Integration

#### GitHub Actions Workflow


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


#### GitLab CI Pipeline


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


### 7. Multi-Cloud Configuration

#### AWS + Azure Example


*See [REFERENCE.md](./REFERENCE.md#example-15) for complete implementation.*


#### GCP Configuration


*See [REFERENCE.md](./REFERENCE.md#example-16) for complete implementation.*


### 8. Security Best Practices

#### Secrets Management


*See [REFERENCE.md](./REFERENCE.md#example-17) for complete implementation.*


#### IAM Policy Best Practices


*See [REFERENCE.md](./REFERENCE.md#example-18) for complete implementation.*


#### Resource Encryption


*See [REFERENCE.md](./REFERENCE.md#example-19) for complete implementation.*


### 9. Drift Detection and Remediation

#### Drift Detection Script


*See [REFERENCE.md](./REFERENCE.md#example-20) for complete implementation.*


#### Automated Remediation


*See [REFERENCE.md](./REFERENCE.md#example-21) for complete implementation.*


#### Scheduled Drift Checks (Cron)

```bash
# /etc/cron.d/terraform-drift-check
# Run drift detection daily at 2 AM
0 2 * * * terraform cd /opt/terraform/infrastructure && ./scripts/detect-drift.sh prod
```

### 10. Advanced Patterns

#### Dynamic Blocks


*See [REFERENCE.md](./REFERENCE.md#example-23) for complete implementation.*


#### For Expressions


*See [REFERENCE.md](./REFERENCE.md#example-24) for complete implementation.*


#### Conditional Resources


*See [REFERENCE.md](./REFERENCE.md#example-25) for complete implementation.*


---

## Level 3: Deep Dive Resources

### Official Documentation

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [GCP Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

### Testing and Validation

- [Terratest Documentation](https://terratest.gruntwork.io/)
- [TFLint Rules](https://github.com/terraform-linters/tflint)
- [Checkov - Infrastructure Security](https://www.checkov.io/)
- [Terraform Compliance](https://terraform-compliance.com/)

### Best Practices and Guides

- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Gruntwork Production Guide](https://gruntwork.io/guides/terraform/)
- [HashiCorp Learn](https://learn.hashicorp.com/terraform)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)

### Community Resources

- [Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)
- [Terraform Community Modules](https://github.com/terraform-aws-modules)
- [Terraform Patterns](https://www.terraform.io/docs/language/patterns)

### Books

- "Terraform: Up & Running" by Yevgeniy Brikman
- "Terraform in Action" by Scott Winkler
- "Infrastructure as Code" by Kief Morris

### Tools and Extensions

- [Terraform-docs](https://terraform-docs.io/) - Generate documentation
- [Infracost](https://www.infracost.io/) - Cloud cost estimates
- [Rover](https://github.com/im2nguyen/rover) - Interactive visualization
- [Terraform Graph](https://www.terraform.io/docs/cli/commands/graph.html) - Dependency graphs

## Examples

### Basic Usage

```python
// TODO: Add basic example for infrastructure-as-code
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for infrastructure-as-code
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how infrastructure-as-code
// works with other systems and services
```

See `examples/infrastructure-as-code/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring infrastructure-as-code functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for infrastructure-as-code
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Next Steps

After mastering Infrastructure as Code:

1. **Advanced DevOps**: CI/CD pipelines, GitOps workflows
2. **Container Orchestration**: Kubernetes with Terraform
3. **Security**: Cloud security posture management
4. **FinOps**: Cloud cost optimization strategies
5. **Observability**: Infrastructure monitoring and alerting
